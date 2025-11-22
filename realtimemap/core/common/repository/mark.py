from abc import abstractmethod, ABC
from typing import TYPE_CHECKING, List

from modules.mark.model import Mark
from modules.mark.schemas import CreateMark, UpdateMark
from .base import BaseRepository

if TYPE_CHECKING:
    from modules.mark.filters import MarkFilter


class MarkRepository(BaseRepository[Mark, CreateMark, UpdateMark], ABC):

    @abstractmethod
    async def get_marks(self, filters: "MarkFilter") -> List[Mark]:
        raise NotImplementedError

    @abstractmethod
    async def create_mark(self, mark: CreateMark) -> Mark:
        raise NotImplementedError

    @abstractmethod
    async def delete_mark(self, mark_id: int) -> Mark:
        raise NotImplementedError

    @abstractmethod
    async def check_distance(self, filters: "MarkFilter", mark: Mark) -> bool:
        """
        Метод проверки дистанции
        :param filters:
        :param mark:
        :return:
        """
        raise NotImplementedError

    @abstractmethod
    async def update_mark(self, mark_id: int, update_data: UpdateMark) -> Mark:
        raise NotImplementedError
