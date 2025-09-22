from typing import Annotated, TYPE_CHECKING

from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from crud.category.repository import CategoryRepository
from crud.chat.repository import ChatRepository
from crud.mark import MarkRepository
from crud.mark_comment.repository import (
    MarkCommentRepository,
    CommentStatRepository,
    CommentReactionRepository,
)
from crud.message.repository import MessageRepository
from crud.request_log.repository import RequestLogRepository
from crud.subcription.repository import SubscriptionPlanRepository
from crud.user.repository import UserRepository
from crud.user_ban.repository import UsersBanRepository
from database.helper import db_helper
from services.geo.dependency import get_geo_service
from services.geo.service import GeoService

if TYPE_CHECKING:
    pass


get_session = Annotated[AsyncSession, Depends(db_helper.session_getter)]


async def get_mark_repository(
    session: get_session, geo_service: Annotated[GeoService, Depends(get_geo_service)]
) -> MarkRepository:
    yield MarkRepository(session=session, geo_service=geo_service)


async def get_category_repository(session: get_session) -> CategoryRepository:
    yield CategoryRepository(session=session)


async def get_request_log_repository(session: get_session) -> RequestLogRepository:
    yield RequestLogRepository(session=session)


async def get_mark_comment_repository(session: get_session) -> MarkCommentRepository:
    yield MarkCommentRepository(session=session)


async def get_user_repository(session: get_session) -> UserRepository:
    yield UserRepository(session=session)


async def get_comment_stat_repository(session: get_session) -> CommentStatRepository:
    yield CommentStatRepository(session=session)


async def get_comment_reaction_repository(
    session: get_session,
) -> CommentReactionRepository:
    yield CommentReactionRepository(session=session)


async def get_user_ban_repository(session: get_session) -> UsersBanRepository:
    yield UsersBanRepository(session=session)


async def get_chat_repository(session: get_session) -> ChatRepository:
    yield ChatRepository(session=session)


async def get_message_repository(session: get_session) -> MessageRepository:
    yield MessageRepository(session=session)


async def get_subscription_plan_repository(
    session: get_session,
) -> SubscriptionPlanRepository:
    yield SubscriptionPlanRepository(session=session)
