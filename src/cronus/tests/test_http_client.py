import httpx
import pytest
import respx

from cronus.ingestion.http_client import BASE_URL, fetch_user, fetch_users

@respx.mock
async def test_fetch_user_ok(api_payload):
    route = respx.get(f"{BASE_URL}/users/1").mock(
        return_value=httpx.Response(200, json=api_payload)
    )

    async with httpx.AsyncClient(base_url=BASE_URL) as client:
        user = await fetch_user(client, 1)

    assert route.call_count == 1
    assert user.id == 1
    assert user.address.city == "Morelia"


@respx.mock
async def test_404_dont_retry():
    route = respx.get(f"{BASE_URL}/users/9999").mock(return_value=httpx.Response(404))

    async with httpx.AsyncClient(base_url=BASE_URL) as client:
        with pytest.raises(httpx.HTTPStatusError):
            await fetch_user(client, 9999, attempts=3, base_delay=0)

    assert route.call_count == 1

@respx.mock
async def test_500_retry_and_continue(api_payload):
    route = respx.get(f"{BASE_URL}/users/1").mock(
        httpx.Response(500),
        httpx.Response(500),
        httpx.Response(200, json=api_payload)
    )

    async with httpx.AsyncClient(base_url=BASE_URL) as client:
        user = await fetch_user(client, 1, attempts=3, base_delay=0)

    assert route.call_count == 3
    assert user.id == 1

@respx.mock
async def test_timeout_failed_retries():
    route = respx.get(f"{BASE_URL}/users/1").mock(
        side_effect=httpx.TimeoutException("Too late")
    )

    async with httpx.AsyncClient(base_url=BASE_URL) as client:
        with pytest.raises(httpx.TimeoutException):
            await fetch_user(client, 1, attempts=3, base_delay=0)

    assert route.call_count == 3


@respx.mock
async def test_fetch_users_after_a_fail(api_payload):
    respx.get(f"{BASE_URL}/users/1").mock(
        return_value=httpx.Response(200, json=api_payload)
    )

    respx.get(f"{BASE_URL}/users/2").mock(return_value=httpx.Response(404))
    respx.get(f"{BASE_URL}/users/3").mock(
        return_value=httpx.Response(200, json=api_payload | {"id": 3})
    )

    async with httpx.AsyncClient(base_url=BASE_URL) as client:
        ok, failed = await fetch_users(client, [1,2,3])

    assert len(ok) == 2
    assert [uid for uid, _ in failed] == [2]
    assert isinstance(failed[0][1], httpx.HTTPStatusError)