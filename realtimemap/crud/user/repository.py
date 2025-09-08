from datetime import datetime
from typing import TYPE_CHECKING

from sqlalchemy import select, and_, or_
from starlette.responses import Response

from crud import BaseRepository
from models import User, UsersBan
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

    async def user_is_banned(self, user_id: int) -> bool:
        """
        Check if the user is banned.

        Args:
            user_id (int): The id of the user.

        Returns:
            bool: Whether the user is banned.
        """
        current_time = datetime.now()
        stmt = (
            select(UsersBan)
            .where(
                and_(
                    UsersBan.user_id == user_id,
                    or_(
                        UsersBan.is_permanent,
                        and_(
                            not UsersBan.is_permanent,
                            UsersBan.banned_until > current_time,
                        ),
                    ),
                )
            )
            .order_by(UsersBan.banned_at.desc())
        )
        result = await self.session.execute(stmt)
        active_ban = result.scalar_one_or_none()

        return active_ban is not None
