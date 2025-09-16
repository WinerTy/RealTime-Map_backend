from typing import TYPE_CHECKING, List, Optional

from sqlalchemy import select

from crud import BaseRepository
from models import Category
from models.category.schemas import CreateCategory, ReadCategory, UpdateCategory

if TYPE_CHECKING:
    from sqlalchemy.ext.asyncio import AsyncSession


class CategoryRepository(
    BaseRepository[Category, CreateCategory, ReadCategory, UpdateCategory]
):
    def __init__(self, session: "AsyncSession"):
        super().__init__(session=session, model=Category)

    async def get_all(self) -> List[ReadCategory]:
        stmt = select(self.model)
        result = await self.session.execute(stmt)
        return result.scalars().all()

    def get_select_all(self):
        return select(self.model).order_by(self.model.id.desc())

    async def create_category(self, data: CreateCategory) -> Optional[Category]:
        result = await self.create(data)
        return result
