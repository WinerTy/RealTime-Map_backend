import pytest


@pytest.mark.asyncio
async def test_docs_available(async_client):
    response = await async_client.get("/")
    assert response.status_code == 307
