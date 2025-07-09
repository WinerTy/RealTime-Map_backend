from typing import Dict, Any

VALID_REGISTER_DATA: Dict[str, Any] = {
    "email": "Testing@realtimemap.ru",
    "password": "TestingPassword123",
    "username": "UserForTesting",
}
INVALID_CASES = [
    # Отсутствует обязательное поле email
    {
        "password": "strongpassword123",
        "username": "Test",
    },
    # Неверный формат email
    {
        "email": "not-an-email",
        "password": "strongpassword123",
        "username": "Test",
    },
    # Слишком короткий пароль
    {
        "email": "test@example.com",
        "password": "short",
        "username": "Test",
    },
    # Отсутствует username
    {
        "email": "test@example.com",
        "password": "strongpassword123",
    },
    # Все поля отсутствуют
    {},
    # Неверный тип данных для username (должен быть строкой)
    {
        "email": "test@example.com",
        "password": "strongpassword123",
        "username": 12345,
    },
]

INVALID_REGISTER_DATA = [
    # Случай 1: Нет email
    (
        {"password": "strongpassword123", "username": "Test"},
        422,  # Ожидаемый статус-код
        "missing_email",  # Уникальный ID для этого тестового случая
    ),
    # Случай 2: Слабый пароль
    (
        {"email": "test2@example.com", "password": "123", "username": "Test"},
        422,
        "short_password",
    ),
    # Случай 3: Невалидный email
    (
        {
            "email": "not-an-email",
            "password": "strongpassword123",
            "username": "Test",
        },
        422,
        "invalid_email",
    ),
]


LOGIN_DATA = {"username": "UserForTesting", "password": "TestingPassword123"}
