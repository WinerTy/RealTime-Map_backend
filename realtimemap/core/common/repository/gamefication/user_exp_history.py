from abc import ABC, abstractmethod
from typing import Optional

from core.common.repository import BaseRepository
from modules.gamefication.model import UserExpHistory
from modules.gamefication.schemas import CreateUserExpHistory, UpdateUserExpHistory


class UserExpHistoryRepository(
    BaseRepository[UserExpHistory, CreateUserExpHistory, UpdateUserExpHistory], ABC
):

    @abstractmethod
    async def get_user_daily_limit_by_action(
        self, user_id: int, action_id: int
    ) -> Optional[int]:
        """
        Метод на получение дневных лимитов события
        :param user_id:
        :param action_id:
        :return:
        """
        raise NotImplementedError

    @abstractmethod
    async def check_if_user_alredy_granted(self, user_id: int, action_id: int) -> bool:
        """
        Метод для проверки начисления опыта. Например для неповторяющих событий
        :param user_id:
        :param action_id:
        :return:
        """
        raise NotImplementedError
