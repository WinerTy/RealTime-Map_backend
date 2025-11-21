from typing import TYPE_CHECKING

from sqlalchemy import select

from core.common.repository import BaseRepository
from .model import Category
from .schemas import CreateCategory, UpdateCategory

if TYPE_CHECKING:
    pass


class CategoryRepository(BaseRepository[Category, CreateCategory, UpdateCategory]):

    @staticmethod
    def get_select_all():
        return select(Category).order_by(Category.id.desc())
