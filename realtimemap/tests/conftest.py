import pytest
from httpx import AsyncClient, ASGITransport

from main import app
from tests.test_auth.data import LOGIN_DATA


@pytest.fixture(scope="session")
def anyio_backend():
    return "asyncio"


@pytest.fixture(scope="session")
async def async_client():
    async with AsyncClient(
        transport=ASGITransport(app=app), base_url="http://test"
    ) as client:
        print("Client is ready")
        yield client


@pytest.fixture(scope="session")
async def auth_async_client():
    async with AsyncClient(
        transport=ASGITransport(app=app), base_url="http://test"
    ) as client:
        response = await client.post(
            "api/v1/auth/login",
            data=LOGIN_DATA,
            headers={"Content-Type": "application/x-www-form-urlencoded"},
        )
        token = response.json().get("access_token")
        client.headers.update({"Authorization": f"Bearer {token}"})
        yield client
