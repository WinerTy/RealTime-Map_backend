from typing import Optional

from fastapi_users.db import BaseUserDatabase
from fastapi_users.models import ID, UP


class MyBaseUserDatabase(BaseUserDatabase[UP, ID]):
    async def validate_user_credentials(
        self, phone: str, username: str, email: str
    ) -> Optional[UP]:
        raise NotImplementedError()

    async def get_by_phone(self, phone: str):
        raise NotImplementedError()

    async def get_by_username(self, username: str):
        raise NotImplementedError()
