from typing import TYPE_CHECKING, Sequence

from sqlalchemy import select

from core.common.repository import SubscriptionPlanRepository
from database.adapter import PgAdapter
from .model import SubscriptionPlan
from .schemas import UpdateSubscriptionPlan, CreateSubscriptionPlan

if TYPE_CHECKING:
    pass


class PgSubscriptionPlanRepository(SubscriptionPlanRepository):
    def __init__(
        self,
        adapter: PgAdapter[
            SubscriptionPlan, CreateSubscriptionPlan, UpdateSubscriptionPlan
        ],
    ):
        super().__init__(adapter)
        self.adapter = adapter

    async def get_subscription_plans(self) -> Sequence[SubscriptionPlan]:
        stmt = select(SubscriptionPlan).where(SubscriptionPlan.is_active)
        result = await self.adapter.execute_query(stmt)
        return result
