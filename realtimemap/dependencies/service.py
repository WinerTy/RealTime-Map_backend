from typing import Annotated, TYPE_CHECKING, Any, AsyncGenerator

from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from database.helper import db_helper
from dependencies.crud import (
    get_mark_repository,
    get_category_repository,
    get_mark_comment_repository,
    get_comment_stat_repository,
    get_comment_reaction_repository,
    get_chat_repository,
    get_message_repository,
    get_user_subscription_repository,
    get_subscription_plan_repository,
    get_user_repository,
    get_user_ban_repository,
)
from interfaces import (
    IUserSubscriptionRepository,
    IUserRepository,
    IMarkCommentRepository,
    ICategoryRepository,
    IMarkRepository,
    IMessageRepository,
    IChatRepository,
    ICommentReactionRepository,
    ICommentStatRepository,
    ISubscriptionPlanRepository,
)
from interfaces import IUsersBanRepository
from services.chat.service import ChatService
from services.geo.dependency import get_geo_service
from services.geo.service import GeoService
from services.mark.service import MarkService
from services.mark_comment.service import MarkCommentService
from services.subscription.service import SubscriptionService
from services.user.service import UserService

if TYPE_CHECKING:
    pass

get_session = Annotated[AsyncSession, Depends(db_helper.session_getter)]


async def get_mark_service(
    mark_repo: Annotated["IMarkRepository", Depends(get_mark_repository)],
    category_repo: Annotated["ICategoryRepository", Depends(get_category_repository)],
    mark_comment_repo: Annotated[
        "IMarkCommentRepository", Depends(get_mark_comment_repository)
    ],
    geo_service: Annotated[GeoService, Depends(get_geo_service)],
    session: get_session,
) -> AsyncGenerator[MarkService, Any]:
    yield MarkService(
        session=session,
        mark_repo=mark_repo,
        category_repo=category_repo,
        mark_comment_repo=mark_comment_repo,
        geo_service=geo_service,
    )


async def get_mark_comment_service(
    session: get_session,
    comment_repo: Annotated[
        "IMarkCommentRepository", Depends(get_mark_comment_repository)
    ],
    comment_stat_repo: Annotated[
        "ICommentStatRepository", Depends(get_comment_stat_repository)
    ],
    comment_reaction_repo: Annotated[
        "ICommentReactionRepository", Depends(get_comment_reaction_repository)
    ],
) -> AsyncGenerator[MarkCommentService, Any]:
    yield MarkCommentService(
        session=session,
        comment_repo=comment_repo,
        comment_stat_repo=comment_stat_repo,
        comment_reaction_repo=comment_reaction_repo,
    )


async def get_chat_service(
    session: get_session,
    chat_repo: Annotated["IChatRepository", Depends(get_chat_repository)],
    message_repo: Annotated["IMessageRepository", Depends(get_message_repository)],
) -> AsyncGenerator[ChatService, Any]:
    yield ChatService(session, chat_repo, message_repo)


async def get_subscription_service(
    session: get_session,
    user_subscription_repo: Annotated[
        "IUserSubscriptionRepository", Depends(get_user_subscription_repository)
    ],
    subscription_repo: Annotated[
        "ISubscriptionPlanRepository", Depends(get_subscription_plan_repository)
    ],
) -> AsyncGenerator[SubscriptionService, Any]:
    yield SubscriptionService(session, user_subscription_repo, subscription_repo)


async def get_user_service(
    user_repo: Annotated["IUserRepository", Depends(get_user_repository)],
    user_ban_repo: Annotated["IUsersBanRepository", Depends(get_user_ban_repository)],
    user_subs_repo: Annotated[
        "IUserSubscriptionRepository", Depends(get_user_subscription_repository)
    ],
) -> AsyncGenerator[UserService, Any]:
    yield UserService(user_repo, user_ban_repo, user_subs_repo)
