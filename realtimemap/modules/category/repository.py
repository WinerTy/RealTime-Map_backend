from typing import TYPE_CHECKING

from sqlalchemy import select

from core.common.repository.category import CategoryRepository
from .model import Category

if TYPE_CHECKING:
    pass


class PgCategoryRepository(CategoryRepository):

    def get_select_all(self):
        return select(Category).order_by(Category.id.desc())
