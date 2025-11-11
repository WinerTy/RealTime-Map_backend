from typing import Annotated, TYPE_CHECKING

from fastapi import Depends
from fastapi_users.authentication.strategy import DatabaseStrategy

from core.config import conf
from .access_token import get_access_token_db

if TYPE_CHECKING:
    from modules import AccessToken
    from fastapi_users.authentication.strategy.db import AccessTokenDatabase


async def get_database_strategy(
    access_tokens_db: Annotated[
        "AccessTokenDatabase[AccessToken]",
        Depends(get_access_token_db),
    ],
) -> DatabaseStrategy:
    yield DatabaseStrategy(
        database=access_tokens_db,
        lifetime_seconds=conf.api.v1.auth.token_lifetime_seconds,
    )
