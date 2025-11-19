from typing import Annotated, TYPE_CHECKING

from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from database import get_session
from .repository import UserRepository

if TYPE_CHECKING:
    pass

DBSession = Annotated[AsyncSession, Depends(get_session)]


async def get_user_repository(
    session: DBSession,
):
    yield UserRepository(session=session)
