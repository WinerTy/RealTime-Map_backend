from typing import (
    TYPE_CHECKING,
    Annotated,
    AsyncGenerator,
)

from fastapi import Depends

from database import get_session
from modules import AccessToken

if TYPE_CHECKING:
    from sqlalchemy.ext.asyncio import AsyncSession

    from fastapi_users_db_sqlalchemy.access_token import (
        SQLAlchemyAccessTokenDatabase,
    )


async def get_access_token_db(
    session: Annotated[
        "AsyncSession",
        Depends(get_session),
    ],
) -> AsyncGenerator["SQLAlchemyAccessTokenDatabase"]:
    yield AccessToken.get_db(session=session)
