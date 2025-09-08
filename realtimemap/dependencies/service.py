from typing import Annotated, TYPE_CHECKING

from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from database.helper import db_helper
from dependencies.crud import (
    get_mark_repository,
    get_category_repository,
    get_mark_comment_repository,
    get_comment_stat_repository,
)
from dependencies.websocket import get_mark_websocket_manager
from services.mark.service import MarkService
from services.mark_comment.service import MarkCommentService

if TYPE_CHECKING:
    from crud.category import CategoryRepository
    from crud.mark import MarkRepository

    from websocket.mark_socket import MarkManager
    from crud.mark_comment.repository import (
        MarkCommentRepository,
        CommentStatRepository,
    )

get_session = Annotated[AsyncSession, Depends(db_helper.session_getter)]


async def get_mark_service(
    mark_repo: Annotated["MarkRepository", Depends(get_mark_repository)],
    category_repo: Annotated["CategoryRepository", Depends(get_category_repository)],
    mark_comment_repo: Annotated[
        "MarkCommentRepository", Depends(get_mark_comment_repository)
    ],
    manager: Annotated["MarkManager", Depends(get_mark_websocket_manager)],
    session: get_session,
):
    yield MarkService(
        session=session,
        mark_repo=mark_repo,
        category_repo=category_repo,
        mark_comment_repo=mark_comment_repo,
        manager=manager,
    )


async def get_mark_comment_service(
    session: get_session,
    comment_repo: Annotated[
        "MarkCommentRepository", Depends(get_mark_comment_repository)
    ],
    comment_stat_repo: Annotated[
        "CommentStatRepository", Depends(get_comment_stat_repository)
    ],
) -> MarkCommentService:
    yield MarkCommentService(
        session=session, comment_repo=comment_repo, comment_stat_repo=comment_stat_repo
    )
