from typing import Annotated, Any, AsyncGenerator

from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from database import get_session
from .repository import (
    MarkCommentRepository,
    CommentReactionRepository,
    CommentStatRepository,
)
from .service import MarkCommentService

DBSession = Annotated[AsyncSession, Depends(get_session)]


async def get_mark_comment_repository(session: DBSession):
    yield MarkCommentRepository(session=session)


async def get_comment_stat_repository(session: DBSession):
    yield CommentStatRepository(session=session)


async def get_comment_reaction_repository(session: DBSession):
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
