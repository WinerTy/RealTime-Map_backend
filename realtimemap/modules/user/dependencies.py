from typing import Annotated, TYPE_CHECKING, AsyncGenerator, Any

from fastapi import Depends

from database.helper import db_helper
from modules.user_ban.dependencies import get_user_ban_repository
from modules.user_subscription.dependencies import get_user_subscription_repository
from .repository import UserRepository
from .service import UserService

if TYPE_CHECKING:
    from sqlalchemy.ext.asyncio import AsyncSession


async def get_user_repository(
    session: Annotated["AsyncSession", Depends(db_helper.session_getter)],
):
    yield UserRepository(session=session)


async def get_user_service(
    user_repo: Annotated["IUserRepository", Depends(get_user_repository)],
    user_ban_repo: Annotated["IUsersBanRepository", Depends(get_user_ban_repository)],
    user_subs_repo: Annotated[
        "IUserSubscriptionRepository", Depends(get_user_subscription_repository)
    ],
) -> AsyncGenerator[UserService, Any]:
    yield UserService(user_repo, user_ban_repo, user_subs_repo)
