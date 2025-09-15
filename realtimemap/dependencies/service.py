from typing import Annotated, TYPE_CHECKING

from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from crud.chat.repository import ChatRepository
from crud.mark_comment.repository import CommentReactionRepository
from crud.message.repository import MessageRepository
from database.helper import db_helper
from dependencies.crud import (
    get_mark_repository,
    get_category_repository,
    get_mark_comment_repository,
    get_comment_stat_repository,
    get_comment_reaction_repository,
    get_chat_repository,
    get_message_repository,
)
from dependencies.websocket import get_mark_websocket_manager
from services.chat.service import ChatService
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
    comment_reaction_repo: Annotated[
        "CommentReactionRepository", Depends(get_comment_reaction_repository)
    ],
) -> MarkCommentService:
    yield MarkCommentService(
        session=session,
        comment_repo=comment_repo,
        comment_stat_repo=comment_stat_repo,
        comment_reaction_repo=comment_reaction_repo,
    )


async def get_chat_service(
    session: get_session,
    chat_repo: Annotated["ChatRepository", Depends(get_chat_repository)],
    message_repo: Annotated["MessageRepository", Depends(get_message_repository)],
) -> ChatService:
    yield ChatService(session, chat_repo, message_repo)
