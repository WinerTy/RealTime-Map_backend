from typing import TYPE_CHECKING

from crud import BaseRepository
from models import Message
from models.message import CreateMessage, ReadMessage, UpdateMessage

if TYPE_CHECKING:
    from sqlalchemy.ext.asyncio import AsyncSession


class MessageRepository(
    BaseRepository[Message, CreateMessage, ReadMessage, UpdateMessage]
):
    def __init__(self, session: "AsyncSession"):
        super().__init__(model=Message, session=session)

    async def create_message(self, data: CreateMessage):
        result = await self.create(data)
        return result
