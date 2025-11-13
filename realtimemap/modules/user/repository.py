from datetime import datetime
from typing import TYPE_CHECKING, Sequence, Optional

from sqlalchemy import select, and_, or_

from core.common import BaseRepository
from modules.gamefication.model import Level
from modules.user.schemas import UserCreate, UserUpdate
from modules.user_ban.model import UsersBan
from .model import User

if TYPE_CHECKING:
    from sqlalchemy.ext.asyncio import AsyncSession


class UserRepository(BaseRepository[User, UserCreate, UserUpdate]):
    def __init__(self, session: "AsyncSession"):
        super().__init__(User, session)

    async def update_user(self, user: User, update_data: UserUpdate) -> User:
        return await self.update(user.id, update_data)

    async def delete_user(self, user: User) -> User:
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

    async def level_up(self, user_id: int) -> int:
        user = await self.get_by_id(user_id)
        level_stmt = select(Level).where(Level.is_active).order_by(Level.level.asc())
        raw_levels = await self.session.execute(level_stmt)
        levels: Sequence[Level] = raw_levels.scalars().all()

        if not levels:
            return user.level  # noqa

        new_level = 0
        for level in levels:
            if user.total_exp >= level.required_exp:
                new_level = level.level
            else:
                break

        if new_level > 0:
            current_level = next(
                (level for level in levels if level.level == new_level), None
            )
            if current_level:
                user.current_exp = user.total_exp - current_level.required_exp
        else:
            user.current_exp = user.total_exp

        user.level = new_level

        return new_level

    async def get_users_for_leaderboard(self) -> Optional[Sequence[User]]:
        stmt = (
            select(self.model)
            .where(self.model.is_active)
            .order_by(self.model.level.desc())
            .limit(10)
        )
        raw_users = await self.session.execute(stmt)
        users = raw_users.scalars().all()
        return users
