from typing import Dict, Any

import pytest

from .data import VALID_REGISTER_DATA, INVALID_CASES


@pytest.mark.asyncio
async def test_register_success(async_client):
    response = await async_client.post(
        "/api/v1/auth/register", json=VALID_REGISTER_DATA
    )
    assert response.status_code == 201
    result = response.json()

    assert result["email"] == VALID_REGISTER_DATA["email"]
    assert "password" not in result


@pytest.mark.asyncio
@pytest.mark.parametrize("invalid_data", INVALID_CASES)
async def test_invalid_register(async_client, invalid_data: Dict[str, Any]):
    response = await async_client.post("/api/v1/auth/register", json=invalid_data)
    assert response.status_code == 422
