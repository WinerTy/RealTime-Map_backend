from typing import Annotated

from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from database import get_session
from modules.message.dependencies import get_message_repository
from .repository import ChatRepository
from .service import ChatService

DBSession = Annotated[AsyncSession, Depends(get_session)]


async def get_chat_repository(
    session: DBSession,
):
    yield ChatRepository(session=session)


async def get_chat_service(
    chat_repo: Annotated["IChatRepository", Depends(get_chat_repository)],
    message_repo: Annotated["IMessageRepository", Depends(get_message_repository)],
) -> ChatService:
    yield ChatService(chat_repo, message_repo)
