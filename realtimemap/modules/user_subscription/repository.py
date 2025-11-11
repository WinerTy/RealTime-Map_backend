from datetime import datetime
from typing import TYPE_CHECKING, Optional, Sequence

from sqlalchemy import select

from core.common import BaseRepository
from .model import UserSubscription
from .schemas import (
    CreateUserSubscription,
    UpdateUserSubscription,
)

if TYPE_CHECKING:
    from sqlalchemy.ext.asyncio import AsyncSession


class UserSubscriptionRepository(
    BaseRepository[
        UserSubscription,
        CreateUserSubscription,
        UpdateUserSubscription,
    ]
):
    def __init__(self, session: "AsyncSession"):
        super().__init__(session=session, model=UserSubscription)

    async def check_active_subscription(
        self, user_id: int
    ) -> Optional[UserSubscription]:
        current_date = datetime.now()
        stmt = select(self.model).where(
            self.model.user_id == user_id,
            self.model.is_active,
            self.model.expires_at > current_date,
        )
        result = await self.session.execute(stmt)
        result = result.scalar_one_or_none()
        return result is not None

    async def get_user_subscriptions(
        self, user_id: int
    ) -> Sequence[Optional[UserSubscription]]:
        stmt = (
            select(self.model)
            .where(
                self.model.user_id == user_id,
            )
            .order_by(self.model.expires_at.desc())
        )
        result = await self.session.execute(stmt)
        return result.scalars().all()

    async def create_user_subscription(
        self, data: CreateUserSubscription
    ) -> UserSubscription:
        result = await self.create(data=data)
        return result
