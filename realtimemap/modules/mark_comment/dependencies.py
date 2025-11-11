from typing import TYPE_CHECKING, Annotated, Any, AsyncGenerator

from fastapi import Depends

from database.helper import db_helper
from .repository import (
    MarkCommentRepository,
    CommentReactionRepository,
    CommentStatRepository,
)
from .service import MarkCommentService

if TYPE_CHECKING:
    from sqlalchemy.ext.asyncio import AsyncSession


async def get_mark_comment_repository(
    session: Annotated["AsyncSession", Depends(db_helper.session_getter)],
):
    yield MarkCommentRepository(session=session)


async def get_comment_stat_repository(
    session: Annotated["AsyncSession", Depends(db_helper.session_getter)],
):
    yield CommentStatRepository(session=session)


async def get_comment_reaction_repository(
    session: Annotated["AsyncSession", Depends(db_helper.session_getter)],
):
    yield CommentReactionRepository(session=session)


async def get_mark_comment_service(
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
        comment_repo=comment_repo,
        comment_stat_repo=comment_stat_repo,
        comment_reaction_repo=comment_reaction_repo,
    )
