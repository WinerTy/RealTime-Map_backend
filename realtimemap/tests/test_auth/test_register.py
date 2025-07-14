from typing import Dict, Any

import pytest

from .data import VALID_REGISTER_DATA, INVALID_REGISTER_CASES


@pytest.mark.order(1)
@pytest.mark.anyio
async def test_register_success(async_client):
    response = await async_client.post(
        "/api/v1/auth/register", json=VALID_REGISTER_DATA
    )
    assert response.status_code == 201
    result = response.json()

    assert result["email"] == VALID_REGISTER_DATA["email"]
    assert "password" not in result


@pytest.mark.anyio
@pytest.mark.parametrize(
    "data, status_code, _",
    INVALID_REGISTER_CASES,
    ids=[test_id[2].lower() for test_id in INVALID_REGISTER_CASES],
)
async def test_invalid_register(
    async_client, data: Dict[str, Any], status_code: int, _: str
):
    response = await async_client.post("/api/v1/auth/register", json=data)
    assert response.status_code == status_code
