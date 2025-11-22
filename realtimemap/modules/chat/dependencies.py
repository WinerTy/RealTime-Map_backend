from typing import Annotated, TYPE_CHECKING

from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from database import get_session
from database.adapter import PgAdapter
from modules.message.dependencies import get_pg_message_repository
from .model import Chat
from .repository import PgChatRepository
from .schemas import CreateChat, UpdateChat
from .service import ChatService

if TYPE_CHECKING:
    from core.common.repository import ChatRepository, MessageRepository

DBSession = Annotated[AsyncSession, Depends(get_session)]


async def get_chat_repository(
    session: DBSession,
) -> "ChatRepository":
    adapter = PgAdapter[Chat, CreateChat, UpdateChat](session, Chat)
    return PgChatRepository(adapter=adapter)


async def get_chat_service(
    chat_repo: Annotated["ChatRepository", Depends(get_chat_repository)],
    message_repo: Annotated["MessageRepository", Depends(get_pg_message_repository)],
) -> ChatService:
    return ChatService(chat_repo, message_repo)
