from typing import TYPE_CHECKING

from models.chat.schemas import ReadChat
from services.base import BaseService

if TYPE_CHECKING:
    from crud.chat.repository import ChatRepository
    from sqlalchemy.ext.asyncio import AsyncSession
    from models import User


class ChatService(BaseService):
    def __init__(self, session: "AsyncSession", chat_repo: "ChatRepository"):
        super().__init__(session)
        self.chat_repo = chat_repo

    async def get_chats_for_user(self, user: "User"):
        crud_result = await self.chat_repo.get_user_chats_with_details(user.id)
        result = []

        for chat, user, message in crud_result:
            result.append(
                ReadChat(
                    id=chat.id,
                    created_at=chat.created_at,
                    other_participant=user,
                    last_message=message,
                )
            )
        return result
