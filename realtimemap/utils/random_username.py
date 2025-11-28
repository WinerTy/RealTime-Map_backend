import uuid


def generate_random_username() -> str:
    return str(uuid.uuid4())
