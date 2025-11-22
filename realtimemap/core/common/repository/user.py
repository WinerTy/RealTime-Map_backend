from abc import ABC, abstractmethod
from typing import List, Optional

from core.common.repository import BaseRepository
from modules.user.model import User
from modules.user.schemas import UserCreate, UserUpdate


class UserRepository(BaseRepository[User, UserCreate, UserUpdate], ABC):

    @abstractmethod
    async def user_is_banned(self, user_id: int) -> bool:
        """
        Проверка забанен ли пользователь
        :param user_id:
        :return: True/False
        """
        raise NotImplementedError()

    @abstractmethod
    async def get_level_up(self, user_id: int) -> int:
        """
        Метод сравнит требования следуйщего уровня для повышения,
        и вернет числовое значение уровня после начисления опыта
        :param user_id:
        :return: числовое значение уровня после начисления всего опыта
        """
        raise NotImplementedError()

    @abstractmethod
    async def get_users_for_leaderboard(self) -> Optional[List[User]]:
        """
        Метод для получения лидеров по уровню
        :return:
        """
        raise NotImplementedError()
