from abc import ABC, abstractmethod
from datetime import datetime
from typing import TYPE_CHECKING, Optional, Sequence

from sqlalchemy import select, func

from core.common import BaseRepository, IBaseRepository
from modules import Level, ExpAction, UserExpHistory
from modules.gamefication.schemas import UpdateUserExpHistory, CreateUserExpHistory

if TYPE_CHECKING:
    from sqlalchemy.ext.asyncio import AsyncSession


class LevelRepository(ABC):

    @abstractmethod
    async def get_next_lelel(self, current_level: int) -> Optional[Level]:
        raise NotImplementedError("get next level or none ")

    @abstractmethod
    async def get_levels(self) -> Sequence[Level]:
        raise NotImplementedError("get all awailebels levels for gamefication system")


class NewLevelRepository(BaseRepository[Level, None, None], LevelRepository):
    def __init__(self, session: "AsyncSession"):
        super().__init__(session=session, model=Level)

    async def get_next_lelel(self, current_level: int) -> Optional[Level]:
        stmt = select(self.model).where(
            self.model.level == current_level + 1, self.model.is_active
        )
        raw_result = await self.session.execute(stmt)
        result = raw_result.scalar_one_or_none()
        return result

    async def get_levels(self) -> Sequence[Level]:
        pass


class ExpActionRepository(ABC):
    @abstractmethod
    async def get_action_by_type(self, action_type: str) -> Optional[ExpAction]:
        raise NotImplementedError("get action by type or none ")


class NewExpActionRepository(
    BaseRepository[ExpAction, None, None], ExpActionRepository
):
    def __init__(self, session: "AsyncSession"):
        super().__init__(session=session, model=ExpAction)

    async def get_action_by_type(self, action_type: str) -> Optional[ExpAction]:
        stmt = select(self.model).where(
            self.model.action_type == action_type, self.model.is_active
        )
        raw_result = await self.session.execute(stmt)
        result = raw_result.scalar_one_or_none()
        return result


class UserExpHistoryRepository(IBaseRepository):
    @abstractmethod
    async def get_user_daily_limit_by_action(
        self, user_id: int, action_id: int
    ) -> Optional[int]:
        raise NotImplementedError("check user daily limit or none ")

    @abstractmethod
    async def check_if_user_alredy_granted(self, user_id: int, action_id: int) -> bool:
        raise NotImplementedError("check user exp for not repitable action ")


class NewUserExpHistoryRepository(
    BaseRepository[UserExpHistory, CreateUserExpHistory, UpdateUserExpHistory],
    UserExpHistoryRepository,
):
    def __init__(self, session: "AsyncSession"):
        super().__init__(model=UserExpHistory, session=session)

    async def get_user_daily_limit_by_action(
        self, user_id: int, action_id: int
    ) -> Optional[int]:
        now = datetime.now()
        day_start = now.replace(hour=0, minute=0, second=0, microsecond=0)
        day_end = now.replace(hour=23, minute=59, second=59, microsecond=999999)

        stmt = select(func.count(self.model.id)).where(
            self.model.user_id == user_id,
            self.model.action_id == action_id,
            self.model.created_at >= day_start,
            self.model.created_at <= day_end,
        )
        raw_result = await self.session.execute(stmt)
        result = raw_result.scalar_one_or_none()
        return result

    async def check_if_user_alredy_granted(self, user_id: int, action_id: int) -> bool:
        stmt = (
            select(func.count())
            .select_from(self.model)
            .where(
                self.model.user_id == user_id,
                self.model.action_id == action_id,
                self.model.is_revoked == False,
            )
        )
        raw_result = await self.session.execute(stmt)
        result = raw_result.scalar()
        return result > 0
