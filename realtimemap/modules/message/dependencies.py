from typing import Annotated, TYPE_CHECKING

from fastapi import Depends

from database.helper import db_helper
from .repository import MessageRepository

if TYPE_CHECKING:
    from sqlalchemy.ext.asyncio import AsyncSession


async def get_message_repository(
    session: Annotated["AsyncSession", Depends(db_helper.session_getter)],
):
    yield MessageRepository(session=session)
