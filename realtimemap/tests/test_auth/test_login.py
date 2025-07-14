from typing import Any, Dict

import pytest

from tests.test_auth.data import LOGIN_DATA, INVALID_LOGIN_CASES


@pytest.mark.anyio
async def test_login_success(async_client):
    response = await async_client.post(
        "api/v1/auth/login",
        data=LOGIN_DATA,
        headers={"Content-Type": "application/x-www-form-urlencoded"},
    )
    result = response.json()
    assert response.status_code == 200
    assert isinstance(result.get("access_token"), str)


@pytest.mark.anyio
@pytest.mark.parametrize(
    "data, status_code, _",
    INVALID_LOGIN_CASES,
    ids=[test_id[2].lower() for test_id in INVALID_LOGIN_CASES],
)
async def test_login_invalid(async_client, data: Dict[str, Any], status_code: int, _):
    response = await async_client.post(
        "api/v1/auth/login",
        data=data,
        headers={"Content-Type": "application/x-www-form-urlencoded"},
    )
    assert response.status_code == status_code
