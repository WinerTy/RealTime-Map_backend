from typing import Protocol, List

from interfaces import IBaseRepository
from models import SubscriptionPlan
from models.subscription.schemas import CreateSubscriptionPlan, UpdateSubscriptionPlan


class ISubscriptionPlanRepository(
    IBaseRepository[SubscriptionPlan, CreateSubscriptionPlan, UpdateSubscriptionPlan],
    Protocol,
):
    async def get_subscription_plans(self) -> List[SubscriptionPlan]: ...
