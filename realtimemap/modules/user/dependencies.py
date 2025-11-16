from typing import Annotated, AsyncGenerator, Any

from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from database import get_session
from modules.user_ban.dependencies import get_user_ban_repository
from modules.user_subscription.dependencies import get_user_subscription_repository
from .repository import UserRepository
from .service import UserService

DBSession = Annotated[AsyncSession, Depends(get_session)]


async def get_user_repository(
    session: DBSession,
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
