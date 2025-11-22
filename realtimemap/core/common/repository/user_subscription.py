from abc import ABC, abstractmethod
from typing import Optional, List

from core.common.repository import BaseRepository
from modules.user_subscription.model import UserSubscription
from modules.user_subscription.schemas import (
    UpdateUserSubscription,
    CreateUserSubscription,
)


class UserSubscriptionRepository(
    BaseRepository[UserSubscription, CreateUserSubscription, UpdateUserSubscription],
    ABC,
):

    @abstractmethod
    async def check_active_subscription(
        self, user_id: int
    ) -> Optional[UserSubscription]:
        """
        Проверяет активную подписку, при ее наличии вернет запись о ней
        :param user_id: id пользователя
        :return: None если подписки нет, UserSubscription если есть
        """
        raise NotImplementedError

    @abstractmethod
    async def get_user_subscriptions(
        self, user_id: int
    ) -> List[Optional[UserSubscription]]:
        """
        Метод для получения истории подписок пользователя
        :param user_id:
        :return:
        """
        raise NotImplementedError

    @abstractmethod
    async def get_active_subscriptions(
        self, user_id: int
    ) -> Optional[UserSubscription]:
        """
        Получает текущую активную подписку
        :param user_id:
        :return:
        """
        raise NotImplementedError
