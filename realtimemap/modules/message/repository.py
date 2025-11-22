import logging
from typing import TYPE_CHECKING, List

from sqlalchemy import select

from core.common.repository import MessageRepository
from database.adapter import PgAdapter
from . import UpdateMessage
from .model import Message
from .schemas import CreateMessage

if TYPE_CHECKING:
    from modules.message.filters import MessageFilter

logger = logging.getLogger(__name__)


class PgMessageRepository(MessageRepository):
    def __init__(self, adapter: PgAdapter[Message, CreateMessage, UpdateMessage]):
        super().__init__(adapter)
        self.adapter = adapter

    async def create_message(self, data: CreateMessage) -> Message:
        result = await self.create(data)
        return result

    async def get_chat_messages(
        self, chat_id: int, params: "MessageFilter"
    ) -> List[Message]:
        try:
            stmt = (
                select(Message)
                .where(Message.chat_id == chat_id)
                .order_by(Message.created_at.desc(), Message.id.desc())
            )
            if params.before:
                stmt = stmt.where(Message.created_at < params.before)

            stmt = stmt.limit(params.limit)
            result = await self.adapter.execute_query(stmt)
            return result
        except Exception as e:
            logger.error("Error while getting chat messages.", exc_info=e)
            return []
