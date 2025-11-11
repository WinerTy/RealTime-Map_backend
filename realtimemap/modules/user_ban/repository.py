from datetime import datetime
from typing import TYPE_CHECKING, Sequence

from sqlalchemy import select, and_, or_, Select

from core.common import BaseRepository
from .model import UsersBan
from .schemas import UsersBanCreate, UpdateUsersBan

if TYPE_CHECKING:
    from sqlalchemy.ext.asyncio import AsyncSession


class UsersBanRepository(BaseRepository[UsersBan, UsersBanCreate, UpdateUsersBan]):
    def __init__(self, session: "AsyncSession"):
        super().__init__(session=session, model=UsersBan)

    def _base_query(self, user_id: int) -> Select:
        current_time = datetime.now()
        stmt = (
            select(self.model)
            .where(
                and_(
                    self.model.user_id == user_id,
                    self.model.unbanned_at.is_(None),
                    or_(
                        self.model.is_permanent,
                        self.model.banned_until > current_time,
                    ),
                )
            )
            .order_by(self.model.banned_at.desc())
        )
        return stmt

    async def check_active_user_ban(self, user_id: int) -> bool:
        stmt = self._base_query(user_id)
        result = await self.session.execute(stmt)
        active_ban = result.scalar_one_or_none()
        return active_ban is not None

    async def ban_user(self, data: UsersBanCreate) -> UsersBan:
        result = await self.create(data)
        return result

    async def unban_user(self, user_id: int, data: UpdateUsersBan) -> UsersBan:
        stmt = self._base_query(user_id)
        result = await self.session.execute(stmt)
        active_ban: UsersBan = result.scalar_one()
        result = await self.update(active_ban.id, data)
        return result

    async def get_user_bans(self, user_id: int) -> Sequence[UsersBan]:
        stmt = (
            select(self.model)
            .where(self.model.user_id == user_id)
            .order_by(self.model.banned_at.desc())
        )
        result = await self.session.execute(stmt)
        active_bans = result.scalars().all()
        return active_bans
