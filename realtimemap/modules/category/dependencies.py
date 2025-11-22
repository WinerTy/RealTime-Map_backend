from typing import Annotated, TYPE_CHECKING, AsyncGenerator

from fastapi import Depends

from core.common.repository.category import CategoryRepository
from database import get_session
from database.adapter import PgAdapter
from .model import Category
from .repository import PgCategoryRepository
from .schemas import CreateCategory, UpdateCategory

if TYPE_CHECKING:
    from sqlalchemy.ext.asyncio import AsyncSession


async def get_pg_category_repository(
    session: Annotated["AsyncSession", Depends(get_session)],
) -> AsyncGenerator[CategoryRepository, None]:
    pg_adapter = PgAdapter[Category, CreateCategory, UpdateCategory](session, Category)
    yield PgCategoryRepository(pg_adapter)
