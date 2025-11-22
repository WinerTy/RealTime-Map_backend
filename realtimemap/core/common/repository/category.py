from abc import abstractmethod, ABC

from sqlalchemy import Select

from core.common.repository.base import BaseRepository
from modules.category.model import Category
from modules.category.schemas import CreateCategory, UpdateCategory


class CategoryRepository(BaseRepository[Category, CreateCategory, UpdateCategory], ABC):
    """
    Абстрактный класс(интерфейс) для репозитория Категорий
    """

    @abstractmethod
    def get_select_all(self) -> Select[Category]:
        raise NotImplementedError
