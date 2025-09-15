from contextlib import asynccontextmanager
from typing import Any, Optional

from socketio import AsyncNamespace

from crud.chat.repository import ChatRepository
from crud.message.repository import MessageRepository
from database.helper import db_helper
from dependencies.auth.web_socket import socket_current_user
from services.chat.service import ChatService


@asynccontextmanager
async def get_chat_service():
    async with db_helper.session_factory() as session:
        message_repo = MessageRepository(session)
        chat_repo = ChatRepository(session)
        yield ChatService(session, chat_repo, message_repo)


class ChatNamespace(AsyncNamespace):
    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)

    async def on_connect(self, sid, _, auth):
        user = await socket_current_user(self.get_token(auth))
        if not user:
            raise ConnectionRefusedError("Authentication required")

        async with get_chat_service() as chat_service:
            chats_ids = await chat_service.get_user_chats_ids(user.id)
            for chat_id in chats_ids:
                await self.enter_room(sid, room=str(chat_id))

    async def on_message(self, sid, data):
        pass

    @staticmethod
    def get_token(auth: Any) -> Optional[str]:
        if auth is None:
            raise ConnectionRefusedError("Authentication required")
        token = auth.get("token", None)
        return token if token else None
