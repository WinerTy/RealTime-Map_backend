from typing import Annotated, TYPE_CHECKING, Any, AsyncGenerator

from fastapi import Depends

from database.helper import db_helper
from modules.gamefication.repository import (
    NewLevelRepository,
    LevelRepository,
    NewUserExpHistoryRepository,
    UserExpHistoryRepository,
    ExpActionRepository,
    NewExpActionRepository,
)
from modules.gamefication.service import GameFicationService
from modules.user.dependencies import get_user_repository
from modules.user_subscription.dependencies import get_user_subscription_repository
from modules.user_subscription.repository import UserSubscriptionRepository

if TYPE_CHECKING:
    from sqlalchemy.ext.asyncio import AsyncSession


async def get_level_repository(
    session: Annotated["AsyncSession", Depends(db_helper.session_getter)],
) -> AsyncGenerator[LevelRepository, Any]:
    yield NewLevelRepository(session)


async def get_user_exp_history_repository(
    session: Annotated["AsyncSession", Depends(db_helper.session_getter)],
) -> AsyncGenerator[UserExpHistoryRepository, Any]:
    yield NewUserExpHistoryRepository(session)


async def get_exp_action_repository(
    session: Annotated["AsyncSession", Depends(db_helper.session_getter)],
) -> AsyncGenerator[ExpActionRepository, Any]:
    yield NewExpActionRepository(session)


async def get_game_fication_service(
    history_repo: Annotated[
        "UserExpHistoryRepository", Depends(get_user_exp_history_repository)
    ],
    action_repo: Annotated["ExpActionRepository", Depends(get_exp_action_repository)],
    level_repo: Annotated["LevelRepository", Depends(get_level_repository)],
    user_repo: Annotated["UserRepository", Depends(get_user_repository)],
    user_subs_repo: Annotated[
        "UserSubscriptionRepository", Depends(get_user_subscription_repository)
    ],
) -> GameFicationService:
    return GameFicationService(
        history_repo, action_repo, level_repo, user_repo, user_subs_repo
    )
