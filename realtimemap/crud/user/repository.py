from typing import TYPE_CHECKING

from starlette.responses import Response

from crud import BaseRepository
from models import User
from models.user.schemas import UserCreate, UserRead, UserUpdate

if TYPE_CHECKING:
    from sqlalchemy.ext.asyncio import AsyncSession


class UserRepository(BaseRepository[User, UserCreate, UserRead, UserUpdate]):
    def __init__(self, session: "AsyncSession"):
        super().__init__(User, session)

    async def update_user(self, user: User, update_data: UserUpdate) -> User:
        return await self.update(user.id, update_data)

    async def delete_user(self, user: User) -> Response:
        return await self.delete(user.id)
