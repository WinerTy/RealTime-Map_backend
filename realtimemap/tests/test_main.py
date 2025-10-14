# @pytest.mark.asyncio
# async def test_root_redirect(client):
#     response = await client.get("/")
#     assert response.status_code == 307
import pytest


@pytest.mark.parametrize(
    "username, email, password, status_code",
    [
        ("admin1", "admin1@mail.ru", "admin1", 201),
        ("admin1", "admin1@mail.ru", "admin1", 400),
    ],
)
def test_register(username, email, password, status_code, client):
    response = client.post(
        "/api/v1/auth/register",
        json={"username": username, "email": email, "password": password},
    )
    assert response.status_code == status_code


# @pytest.mark.parametrize(
#     "x, y, res",
#     [
#         (1, 2, 0.5),
#         (1, 1, 1),
#         (1, -2, -0.5),
#         (1, 0, -0.5),
#     ],
# )
# def test_devide(x, y, res):
#     assert devide(x, y) == res


# @pytest.mark.parametrize(
#     "x, y, res, expected",
#     [
#         (1, 2, 0.5, does_not_raise()),
#         (1, 1, 1, does_not_raise()),
#         (1, -2, -0.5, does_not_raise()),
#         (1, 0, -0.5, pytest.raises(ZeroDivisionError)),
#     ],
# )
# def test_devide(x, y, res, expected):
#     with expected:
#         assert devide(x, y) == res
