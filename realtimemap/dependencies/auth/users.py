from typing import (
    TYPE_CHECKING,
    Annotated,
)

from fastapi import Depends

from database.helper import db_helper
from models import User

if TYPE_CHECKING:
    from sqlalchemy.ext.asyncio import AsyncSession


async def get_users_db(
    session: Annotated[
        "AsyncSession",
        Depends(db_helper.session_getter),
    ],
):
    yield User.get_db(session=session)
