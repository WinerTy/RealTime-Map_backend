from typing import Annotated, TYPE_CHECKING

from fastapi import Depends

from database import get_session
from database.adapter import PgAdapter
from .model import Message
from .repository import PgMessageRepository
from .schemas import CreateMessage, UpdateMessage

if TYPE_CHECKING:
    from sqlalchemy.ext.asyncio import AsyncSession
    from core.common.repository import MessageRepository


async def get_pg_message_repository(
    session: Annotated["AsyncSession", Depends(get_session)],
) -> "MessageRepository":
    adapter = PgAdapter[Message, CreateMessage, UpdateMessage](session, Message)
    return PgMessageRepository(adapter=adapter)
