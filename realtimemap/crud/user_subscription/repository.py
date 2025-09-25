from datetime import datetime
from typing import TYPE_CHECKING, Optional

from sqlalchemy import select

from crud import BaseRepository
from models import UserSubscription
from models.user_subscription.schemas import (
    CreateUserSubscription,
    ReadUserSubscription,
    UpdateUserSubscription,
)

if TYPE_CHECKING:
    from sqlalchemy.ext.asyncio import AsyncSession


class UserSubscriptionRepository(
    BaseRepository[
        UserSubscription,
        CreateUserSubscription,
        ReadUserSubscription,
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
