import logging
from typing import TYPE_CHECKING

from core.config import conf
from models import Message
from models.message import ReadMessage
from services.notification.base import BaseNotificationSocketIO

if TYPE_CHECKING:
    from socketio import AsyncServer

logger = logging.getLogger(__name__)


class ChatNotificationService(BaseNotificationSocketIO):
    def __init__(self, sio: "AsyncServer", namespace: str = conf.socket.prefix.chat):
        super().__init__(sio, namespace)

    async def notify_action_in_chat(self, event: str, message: Message) -> None:
        try:
            if not message:
                return

            serialized_data = ReadMessage.model_validate(message).model_dump(
                mode="json"
            )

            await self.sio.emit(
                event=event,
                data=serialized_data,
                room=str(message.chat_id),
                namespace=self.namespace,
            )
        except Exception as e:
            logger.error("Chat notification failed", exc_info=e)
