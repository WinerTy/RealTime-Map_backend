from typing import TYPE_CHECKING, List

from sqlalchemy import select

from crud import BaseRepository
from models import SubscriptionPlan
from models.subscription.schemas import (
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

    async def get_subscription_plans(self) -> List[SubscriptionPlan]:
        stmt = select(self.model).where(self.model.is_active)
        result = await self.session.execute(stmt)
        return result.scalars().all()
