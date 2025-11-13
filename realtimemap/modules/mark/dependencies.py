from typing import TYPE_CHECKING, Annotated, Any, AsyncGenerator

from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from database import get_session
from modules.category.dependencies import get_category_repository
from modules.geo_service import get_geo_service
from modules.mark_comment.dependencies import get_mark_comment_repository
from .repository import MarkRepository
from .service import MarkService

if TYPE_CHECKING:
    from modules.geo_service import GeoService

DBSession = Annotated[AsyncSession, Depends(get_session)]


async def get_mark_repository(
    session: DBSession,
    geo_service: Annotated["GeoService", Depends(get_geo_service)],
):
    yield MarkRepository(session=session, geo_service=geo_service)


async def get_mark_service(
    mark_repo: Annotated["IMarkRepository", Depends(get_mark_repository)],
    category_repo: Annotated["ICategoryRepository", Depends(get_category_repository)],
    mark_comment_repo: Annotated[
        "IMarkCommentRepository", Depends(get_mark_comment_repository)
    ],
    geo_service: Annotated["GeoService", Depends(get_geo_service)],
) -> AsyncGenerator[MarkService, Any]:
    yield MarkService(
        mark_repo=mark_repo,
        category_repo=category_repo,
        mark_comment_repo=mark_comment_repo,
        geo_service=geo_service,
    )
