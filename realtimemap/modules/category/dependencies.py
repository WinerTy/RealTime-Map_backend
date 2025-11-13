from typing import Annotated, TYPE_CHECKING

from fastapi import Depends

from database import get_session
from .repository import CategoryRepository

if TYPE_CHECKING:
    from sqlalchemy.ext.asyncio import AsyncSession


async def get_category_repository(
    session: Annotated["AsyncSession", Depends(get_session)],
):
    yield CategoryRepository(session=session)
