from typing import TYPE_CHECKING, Annotated, Optional

from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from database import get_session
from database.adapter import PgAdapter
from modules.category.dependencies import get_pg_category_repository
from modules.geo_service import get_geo_service
from modules.mark_comment.dependencies import get_mark_comment_repository
from .model import Mark
from .repository import PgMarkRepository
from .schemas import CreateMark, UpdateMark
from .service import MarkService

if TYPE_CHECKING:
    from modules.geo_service import GeoService
    from core.common.repository import (
        MarkRepository,
        CategoryRepository,
        MarkCommentRepository,
    )

DBSession = Annotated[AsyncSession, Depends(get_session)]


async def get_pg_mark_repository(
    session: DBSession,
    geo_service: Annotated[Optional["GeoService"], Depends(get_geo_service)],
) -> "MarkRepository":
    adapter = PgAdapter[Mark, CreateMark, UpdateMark](session, Mark)
    return PgMarkRepository(adapter=adapter, geo_service=geo_service)


async def get_mark_service(
    mark_repo: Annotated["MarkRepository", Depends(get_pg_mark_repository)],
    category_repo: Annotated["CategoryRepository", Depends(get_pg_category_repository)],
    mark_comment_repo: Annotated[
        "MarkCommentRepository", Depends(get_mark_comment_repository)
    ],
    geo_service: Annotated["GeoService", Depends(get_geo_service)],
) -> "MarkService":
    return MarkService(
        mark_repo=mark_repo,
        category_repo=category_repo,
        mark_comment_repo=mark_comment_repo,
        geo_service=geo_service,
    )
