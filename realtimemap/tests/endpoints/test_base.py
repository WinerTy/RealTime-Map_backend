# import pytest
#
#
# class TestApiDocs:
#     @pytest.mark.asyncio
#     async def test_docs_redirect(self, client):
#         response = await client.get("/")
#         assert response.status_code == 307
#
#     @pytest.mark.asyncio
#     async def test_swagger_docs(self, client):
#         response = await client.get("/docs")
#         assert response.status_code == 200
#
#     @pytest.mark.asyncio
#     async def test_redoc_docs(self, client):
#         response = await client.get("/redoc")
#         assert response.status_code == 200
#
#     @pytest.mark.asyncio
#     async def test_user_reg(self, client):
#         user_data = {
#             "email": "test@email.ru",
#             "username": "testUser",
#             "password": "strongPass1",
#         }
#         response = await client.post("/api/v1/auth/register", json=user_data)
#         assert response.status_code == 201
#         data = response.json()
#         assert data["email"] == user_data["email"]
#         assert data["username"] == user_data["username"]
