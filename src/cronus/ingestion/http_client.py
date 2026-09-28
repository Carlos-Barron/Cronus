"""Capa de ingestión: descarga de datos desde el API. """

import httpx
import asyncio
import logging
import random

from collections.abc import Sequence
from cronus.ingestion.dto import ApiUser

DEFAULT_CONCURRENCY = 5
BASE_URL = "https://jsonplaceholder.typicode.com"
DEFAULT_TIMEOUT = httpx.Timeout(10.0, connect=5)
RETRYABLE_STATUS = {429, 500, 502, 503, 504}

FetchResult = tuple[list[ApiUser], list[tuple[int, BaseException]]]
logger = logging.getLogger(__name__)

def is_retryable(exc: BaseException) -> bool:
    """ Timeouts y errores de red si; 5xx y 429; el resto de 4xx no. """
    if isinstance(exc, (httpx.TimeoutException, httpx.ConnectError)):
        return True
    if isinstance(exc, httpx.HTTPStatusError):
        return exc.response.status_code in RETRYABLE_STATUS
    return False


async def fetch_user(
        client: httpx.AsyncClient, 
        user_id: int,
        *,
        attempts: int = 3,
        base_delay: float = 0.5
        ) -> ApiUser:
    for try_number in range(1, attempts + 1):
        try:

            response = await client.get(f"/users/{user_id}")
            response.raise_for_status()
            return ApiUser.model_validate(response.json())
        except httpx.HTTPError as exc:
            if not is_retryable(exc) or try_number == attempts:
                raise
            wait = base_delay * 2 ** (try_number - 1) + random.uniform(0, 0.1)
            logger.warning(
                "id=%s try nimber %s/%s failed (%s); retry in %.2fs",
                user_id, try_number, attempts, type(exc).__name__, wait,
            )
            await asyncio.sleep(wait)

    raise AssertionError("Unreachable")

async def fetch_users(
        client: httpx.AsyncClient,
        user_ids: Sequence[int],
        *,
        concurrency: int = DEFAULT_CONCURRENCY
) -> list[ApiUser]:
    """ Devuelve (usuarios_ok, fallos). Un id que falla no cancela el resto. """

    semaphore = asyncio.Semaphore(concurrency)

    async def with_limit(user_id: int) -> ApiUser:
        async with semaphore:
            return await fetch_user(client, user_id)

        # return await asyncio.gather(*(with_limit(uid) for uid in user_ids))

        results = await asyncio.gather(
            *(with_limit(uid) for uid in user_ids),
            return_exceptions=True
        )

        ok: list[ApiUser] = []
        fails: list[tuple[int, BaseException]] = []
        for user_id, result in zip(user_ids, results, strict=True):
            if isinstance(result, BaseException):
                logger.warning("id=%s failed: %s: %s", user_id, type(result).__name__, result)
                fails.append((user_id, result))
            else:
                ok.append(result)
        return ok, fails

async def ingest(
        user_ids: Sequence[int],
        *,
        concurrency: int = DEFAULT_CONCURRENCY
) -> FetchResult:
    """ Punto de entrada de la capa de ingestión: Crea el cliente y descarga todo. """
    limits = httpx.Limits(max_connections=concurrency)
    async with httpx.AsyncClient(
        base_url=BASE_URL,
        timeout=DEFAULT_TIMEOUT,
        limits=limits
    ) as client:
        return await fetch_users(client, user_ids, concurrency=concurrency)