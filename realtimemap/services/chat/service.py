from typing import TYPE_CHECKING, List

from errors.http2 import UserPermissionError
from models.chat.schemas import ReadChat
from models.message.schemas import (
    CreateMessageRequest,
    CreateMessage,
    UpdateMessageRequest,
    MessageFilter,
)
from models.message.schemas import MessageParamsRequest
from services.base import BaseService

if TYPE_CHECKING:
    from interfaces import IMessageRepository, IChatRepository
    from sqlalchemy.ext.asyncio import AsyncSession
    from models import User, Message


class ChatService(BaseService):
    def __init__(
        self,
        session: "AsyncSession",
        chat_repo: "IChatRepository",
        message_repo: "IMessageRepository",
    ):
        super().__init__(session)
        self.chat_repo = chat_repo
        self.message_repo = message_repo

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

    async def get_user_chats_ids(self, user_id: int) -> List[int]:
        return await self.chat_repo.get_user_chats_ids(user_id)

    async def check_user_in_chat(self, chat_id: int, user_id: int) -> None:
        in_chat = await self.chat_repo.check_user_in_chat(chat_id, user_id)
        if not in_chat:
            raise UserPermissionError()

    async def get_chat_message_history(
        self, chat_id: int, user: "User", params: "MessageParamsRequest"
    ) -> List["Message"]:
        await self.check_user_in_chat(chat_id, user.id)
        filters = MessageFilter.from_request(params)
        messages = await self.message_repo.get_chat_messages(chat_id, filters)
        return messages

    async def send_message(self, user: "User", message: CreateMessageRequest):
        is_new, chat = await self.chat_repo.find_or_create_private_chat(
            user1_id=user.id, user2_id=message.recipient_id
        )
        await self._before_send_message(chat.id, user_id=user.id)
        valid_message = self._prepare_message(chat.id, user, message)
        result = await self.message_repo.create_message(valid_message)
        await self._after_send_message()
        return result

    @staticmethod
    def _prepare_message(
        chat_id: int,
        user: "User",
        message: CreateMessageRequest,
    ) -> CreateMessage:
        return CreateMessage(
            chat_id=chat_id,
            sender_id=user.id,
            content=message.content,
        )

    async def _before_send_message(self, chat_id: int, user_id: int):
        user_in_chat: bool = await self.chat_repo.check_user_in_chat(chat_id, user_id)
        if not user_in_chat:
            raise UserPermissionError()

    async def _after_send_message(self):
        pass

    async def update_message(
        self, message_id: int, message: UpdateMessageRequest, user: "User"
    ):
        instance = await self.message_repo.get_by_id(message_id)
        if instance.sender_id != user.id:
            raise UserPermissionError()

        instance = await self.message_repo.update(message_id, message)
        return instance

    async def delete_message(self, message_id: int, user: "User"):
        instance = await self.message_repo.get_by_id(message_id)
        if instance.sender_id != user.id:
            raise UserPermissionError()
        instance = await self.message_repo.delete(message_id)
        return instance
