import logging
from typing import TYPE_CHECKING, List

from sqlalchemy import select

from crud import BaseRepository
from models import Message
from models.message import CreateMessage, UpdateMessage

if TYPE_CHECKING:
    from sqlalchemy.ext.asyncio import AsyncSession
    from models.message.filters import MessageFilter

logger = logging.getLogger(__name__)


class MessageRepository(BaseRepository[Message, CreateMessage, UpdateMessage]):
    def __init__(self, session: "AsyncSession"):
        super().__init__(model=Message, session=session)

    async def create_message(self, data: CreateMessage) -> Message:
        result = await self.create(data)
        return result

    async def get_chat_messages(
        self, chat_id: int, params: "MessageFilter"
    ) -> List[Message]:
        try:
            stmt = (
                select(self.model)
                .where(self.model.chat_id == chat_id)
                .order_by(self.model.created_at.desc(), self.model.id.desc())
            )
            if params.before:
                stmt = stmt.where(self.model.created_at < params.before)

            stmt = stmt.limit(params.limit)
            result = await self.session.execute(stmt)
            return result.scalars().all()
        except Exception as e:
            logger.error("Error while getting chat messages.", exc_info=e)
            return []
