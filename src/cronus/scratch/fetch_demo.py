import asyncio
import httpx

from cronus.ingestion.http_client import BASE_URL, DEFAULT_TIMEOUT, fetch_user

async def main() -> None:
    async with httpx.AsyncClient(base_url=BASE_URL, timeout=DEFAULT_TIMEOUT) as client:
        print(await fetch_user(client, 1))


asyncio.run(main())