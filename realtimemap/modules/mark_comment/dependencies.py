from typing import Annotated, TYPE_CHECKING

from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from database import get_session
from database.adapter import PgAdapter
from .model import Comment, CommentStat, CommentReaction
from .repository import (
    PgMarkCommentRepository,
    PgCommentReactionRepository,
    PgCommentStatRepository,
)
from .schemas import (
    CreateComment,
    UpdateComment,
    UpdateCommentStat,
    CreateCommentStat,
    CreateCommentReaction,
    UpdateCommentReaction,
)
from .service import MarkCommentService

if TYPE_CHECKING:
    from core.common.repository import (
        MarkCommentRepository,
        CommentStatRepository,
        CommentReactionRepository,
    )

DBSession = Annotated[AsyncSession, Depends(get_session)]


async def get_mark_comment_repository(session: DBSession) -> "MarkCommentRepository":
    adapter = PgAdapter[Comment, CreateComment, UpdateComment](session, Comment)
    return PgMarkCommentRepository(adapter=adapter)


async def get_comment_stat_repository(session: DBSession) -> "CommentStatRepository":
    adapter = PgAdapter[CommentStat, CreateCommentStat, UpdateCommentStat](
        session, Comment
    )
    return PgCommentStatRepository(adapter=adapter)


async def get_comment_reaction_repository(
    session: DBSession,
) -> "CommentReactionRepository":
    adapter = PgAdapter[CommentReaction, CreateCommentReaction, UpdateCommentReaction](
        session, Comment
    )
    return PgCommentReactionRepository(adapter=adapter)


async def get_mark_comment_service(
    comment_repo: Annotated[
        "MarkCommentRepository", Depends(get_mark_comment_repository)
    ],
    comment_stat_repo: Annotated[
        "CommentStatRepository", Depends(get_comment_stat_repository)
    ],
    comment_reaction_repo: Annotated[
        "CommentReactionRepository", Depends(get_comment_reaction_repository)
    ],
) -> "MarkCommentService":
    return MarkCommentService(
        comment_repo=comment_repo,
        comment_stat_repo=comment_stat_repo,
        comment_reaction_repo=comment_reaction_repo,
    )
