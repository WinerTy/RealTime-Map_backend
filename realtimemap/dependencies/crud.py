from typing import Annotated

from fastapi import Depends

from crud.category.repository import CategoryRepository
from crud.mark import MarkRepository
from crud.mark_comment.repository import MarkCommentRepository, CommentStatRepository
from crud.request_log.repository import RequestLogRepository
from crud.user.repository import UserRepository

from dependencies.session import get_session
from services.geo.dependency import get_geo_service
from services.geo.service import GeoService


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
