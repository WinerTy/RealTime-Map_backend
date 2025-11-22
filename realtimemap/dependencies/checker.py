from typing import Annotated, TYPE_CHECKING

from fastapi import Depends

from errors.http2 import NotFoundError
from modules.chat.dependencies import get_chat_repository
from modules.mark.dependencies import get_pg_mark_repository
from modules.mark_comment.dependencies import get_mark_comment_repository
from modules.message.dependencies import get_pg_message_repository
from modules.message.repository import PgMessageRepository

if TYPE_CHECKING:
    from modules.mark.repository import PgMarkRepository
    from modules.mark_comment.repository import PgMarkCommentRepository
    from modules.chat.repository import PgChatRepository


async def check_mark_exist(
    mark_id: int, repo: Annotated["PgMarkRepository", Depends(get_pg_mark_repository)]
) -> None:
    is_exist = await repo.exist(mark_id)
    if not is_exist:
        raise NotFoundError()


async def check_mark_comment_exist(
    comment_id: int,
    repo: Annotated["PgMarkCommentRepository", Depends(get_mark_comment_repository)],
) -> None:
    is_exist = await repo.exist(comment_id)
    if not is_exist:
        raise NotFoundError()


async def check_chat_exist(
    chat_id: int,
    repo: Annotated["PgChatRepository", Depends(get_chat_repository)],
) -> None:
    is_exist = await repo.exist(chat_id)
    if not is_exist:
        raise NotFoundError()


async def check_message_exist(
    message_id: int,
    repo: Annotated["PgMessageRepository", Depends(get_pg_message_repository)],
):
    is_exist = await repo.exist(message_id)
    if not is_exist:
        raise NotFoundError()
