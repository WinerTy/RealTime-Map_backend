from typing import Protocol, Optional, List

from interfaces import IBaseRepository
from models import Category
from models.category.schemas import CreateCategory, UpdateCategory, ReadCategory


class ICategoryRepository(
    IBaseRepository[Category, CreateCategory, UpdateCategory], Protocol
):

    async def get_all(self) -> List[ReadCategory]: ...

    def get_select_all(self): ...

    async def create_category(self, data: CreateCategory) -> Optional[Category]: ...
