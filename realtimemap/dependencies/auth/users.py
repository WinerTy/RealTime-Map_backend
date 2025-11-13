from typing import (
    TYPE_CHECKING,
    Annotated,
)

from fastapi import Depends

from database import get_session
from modules import User

if TYPE_CHECKING:
    from sqlalchemy.ext.asyncio import AsyncSession


async def get_users_db(
    session: Annotated[
        "AsyncSession",
        Depends(get_session),
    ],
):
    yield User.get_db(session=session)
