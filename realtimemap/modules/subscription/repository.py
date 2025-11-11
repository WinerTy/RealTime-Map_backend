from typing import TYPE_CHECKING, Sequence

from sqlalchemy import select

from core.common import BaseRepository
from .model import SubscriptionPlan
from .schemas import (
    CreateSubscriptionPlan,
    UpdateSubscriptionPlan,
)

if TYPE_CHECKING:
    from sqlalchemy.ext.asyncio import AsyncSession


class SubscriptionPlanRepository(
    BaseRepository[
        SubscriptionPlan,
        CreateSubscriptionPlan,
        UpdateSubscriptionPlan,
    ]
):
    def __init__(self, session: "AsyncSession"):
        super().__init__(session=session, model=SubscriptionPlan)

    async def get_subscription_plans(self) -> Sequence[SubscriptionPlan]:
        stmt = select(self.model).where(self.model.is_active)
        result = await self.session.execute(stmt)
        return result.scalars().all()
