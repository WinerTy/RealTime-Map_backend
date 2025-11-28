from datetime import datetime
from typing import TYPE_CHECKING, Optional, List

from sqlalchemy import select
from sqlalchemy.orm import joinedload

from core.common.repository import UserSubscriptionRepository
from database.adapter import PgAdapter
from .model import UserSubscription, PaymentStatus
from .schemas import (
    CreateUserSubscription,
    UpdateUserSubscription,
)

if TYPE_CHECKING:
    pass


class PgUserSubscriptionRepository(UserSubscriptionRepository):
    def __init__(
        self,
        adapter: PgAdapter[
            UserSubscription, CreateUserSubscription, UpdateUserSubscription
        ],
    ):
        super().__init__(adapter)
        self.adapter = adapter

    async def check_active_subscription(
        self, user_id: int
    ) -> Optional[UserSubscription]:
        current_date = datetime.now()
        stmt = select(UserSubscription).where(
            UserSubscription.user_id == user_id,
            UserSubscription.is_active,
            UserSubscription.expires_at > current_date,
        )
        result = await self.adapter.execute_query_one(stmt)
        return result is not None

    async def get_user_subscriptions(
        self, user_id: int
    ) -> List[Optional[UserSubscription]]:
        stmt = (
            select(UserSubscription)
            .where(
                UserSubscription.user_id == user_id,
            )
            .order_by(UserSubscription.expires_at.desc())
        )
        result = await self.adapter.execute_query(stmt)
        return result

    async def create_user_subscription(
        self, data: CreateUserSubscription
    ) -> UserSubscription:
        result = await self.create(data=data)
        return result

    async def get_active_subscription(
        self, user_id: int
    ) -> Optional[UserSubscription]:
        now = datetime.now()
        stmt = (
            select(UserSubscription)
            .where(
                UserSubscription.user_id == user_id,
                UserSubscription.is_active,
                UserSubscription.starts_at <= now,
                UserSubscription.expires_at >= now,
                UserSubscription.payment_status == PaymentStatus.succeeded,
            )
            .options(joinedload(UserSubscription.plan))
            .limit(1)
        )
        result = await self.adapter.execute_query_one(stmt)
        return result
