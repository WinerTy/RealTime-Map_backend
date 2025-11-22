from abc import ABC, abstractmethod
from typing import List

from modules.subscription.model import SubscriptionPlan
from modules.subscription.schemas import UpdateSubscriptionPlan, CreateSubscriptionPlan
from .base import BaseRepository


class SubscriptionPlanRepository(
    BaseRepository[SubscriptionPlan, CreateSubscriptionPlan, UpdateSubscriptionPlan],
    ABC,
):
    @abstractmethod
    async def get_subscription_plans(self) -> List[SubscriptionPlan]:
        """
        Метод на получение всех доступных платных подписок
        :return:
        """
        raise NotImplementedError
