from typing import Annotated, TYPE_CHECKING

from fastapi import Depends

from database.helper import db_helper
from modules.message.dependencies import get_message_repository
from .repository import ChatRepository
from .service import ChatService

if TYPE_CHECKING:
    from sqlalchemy.ext.asyncio import AsyncSession


async def get_chat_repository(
    session: Annotated["AsyncSession", Depends(db_helper.session_getter)],
):
    yield ChatRepository(session=session)


async def get_chat_service(
    chat_repo: Annotated["IChatRepository", Depends(get_chat_repository)],
    message_repo: Annotated["IMessageRepository", Depends(get_message_repository)],
) -> ChatService:
    yield ChatService(chat_repo, message_repo)
