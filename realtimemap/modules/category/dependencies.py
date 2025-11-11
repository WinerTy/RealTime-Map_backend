from typing import Annotated

from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from database.helper import db_helper
from .repository import CategoryRepository

get_session = Annotated[AsyncSession, Depends(db_helper.session_getter)]


async def get_category_repository(session: get_session):
    yield CategoryRepository(session=session)
