from typing import Dict, Any, List, Tuple

VALID_REGISTER_DATA: Dict[str, Any] = {
    "email": "Testing@realtimemap.ru",
    "password": "TestingPassword123",
    "username": "UserForTesting",
}


INVALID_REGISTER_CASES: List[Tuple[Dict[str, Any], int, str]] = [
    ({"username": "", "password": "", "email": ""}, 422, "Empty_fields"),
    (
        {
            "username": "Testing",
            "email": "testmail.ru",
            "password": "SuperSecretPassword",
        },
        422,
        "Not_valid_email",
    ),
    (
        {
            "username": "Testing",
            "email": "Testing1@realtimemap.ru",
            "password": "12345",
        },
        422,
        "Short_password",
    ),
    (
        {
            "username": "UserForTesting",
            "email": "Testing@realtimemap.ru",
            "password": "TestingPassword123",
        },
        400,
        "User_already_exist",
    ),
]

LOGIN_DATA = {"username": "UserForTesting", "password": "TestingPassword123"}


INVALID_LOGIN_CASES: List[Tuple[Dict[str, Any], int, str]] = [
    (
        {
            "username": "Testing@realtimemap.ru",
            "password": "<PASSWORD>",
        },
        400,
        "incorrect_password",
    ),
    (
        {
            "username": "Testing@realtimemap1.ru",
            "password": "TestingPassword123",
        },
        400,
        "incorrect_username",
    ),
    (
        {
            "username": "",
            "password": "",
        },
        400,
        "empty_fields",
    ),
]
