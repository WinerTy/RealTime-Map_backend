from typing import Annotated, AsyncGenerator, Any, TYPE_CHECKING

from fastapi import Depends

from modules.gamefication.dependencies import get_level_repository
from modules.user_ban.dependencies import get_user_ban_repository
from modules.user_subscription.dependencies import get_user_subscription_repository
from .dependencies import get_user_repository
from .service import UserService

if TYPE_CHECKING:
    from modules.gamefication.repository import LevelRepository


async def get_user_service(
    user_repo: Annotated["IUserRepository", Depends(get_user_repository)],
    user_ban_repo: Annotated["IUsersBanRepository", Depends(get_user_ban_repository)],
    user_subs_repo: Annotated[
        "IUserSubscriptionRepository", Depends(get_user_subscription_repository)
    ],
    level_repo: Annotated["LevelRepository", Depends(get_level_repository)],
) -> AsyncGenerator[UserService, Any]:
    yield UserService(user_repo, user_ban_repo, user_subs_repo, level_repo)
