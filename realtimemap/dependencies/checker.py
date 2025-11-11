from typing import Annotated, TYPE_CHECKING

from fastapi import Depends

from errors.http2 import NotFoundError
from modules.chat.dependencies import get_chat_repository
from modules.mark.dependencies import get_mark_repository
from modules.mark_comment.dependencies import get_mark_comment_repository
from modules.message.dependencies import get_message_repository
from modules.message.repository import MessageRepository

if TYPE_CHECKING:
    from modules.mark.repository import MarkRepository
    from modules.mark_comment.repository import MarkCommentRepository
    from modules.chat.repository import ChatRepository


async def check_mark_exist(
    mark_id: int, repo: Annotated["MarkRepository", Depends(get_mark_repository)]
) -> None:
    is_exist = await repo.exist(mark_id)
    if not is_exist:
        raise NotFoundError()


async def check_mark_comment_exist(
    comment_id: int,
    repo: Annotated["MarkCommentRepository", Depends(get_mark_comment_repository)],
) -> None:
    is_exist = await repo.exist(comment_id)
    if not is_exist:
        raise NotFoundError()


async def check_chat_exist(
    chat_id: int,
    repo: Annotated["ChatRepository", Depends(get_chat_repository)],
) -> None:
    is_exist = await repo.exist(chat_id)
    if not is_exist:
        raise NotFoundError()


async def check_message_exist(
    message_id: int,
    repo: Annotated["MessageRepository", Depends(get_message_repository)],
):
    is_exist = await repo.exist(message_id)
    if not is_exist:
        raise NotFoundError()
