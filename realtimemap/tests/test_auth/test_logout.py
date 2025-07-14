import pytest


@pytest.mark.anyio
async def test_logout_success(auth_async_client):
    response = await auth_async_client.post("/api/v1/auth/logout")
    assert response.status_code == 204


@pytest.mark.anyio
async def test_logout_invalid(async_client):
    response = await async_client.post("/api/v1/auth/logout")
    assert response.status_code == 401
