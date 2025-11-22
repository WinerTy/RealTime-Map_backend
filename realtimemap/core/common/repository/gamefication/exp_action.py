from abc import ABC, abstractmethod
from typing import Optional

from core.common.repository import BaseRepository
from modules.gamefication.model import ExpAction


class ExpActionRepository(BaseRepository[ExpAction, None, None], ABC):

    @abstractmethod
    async def get_action_by_type(self, action_type: str) -> Optional[ExpAction]:
        """
        Метод получения объекта конфига
        :param action_type:
        :return:
        """
        raise NotImplementedError
