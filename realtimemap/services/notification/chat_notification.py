from typing import TYPE_CHECKING

from core.config import conf
from services.notification.base import BaseNotificationSocketIO

if TYPE_CHECKING:
    from socketio import AsyncServer


class ChatNotificationService(BaseNotificationSocketIO):
    def __init__(self, sio: "AsyncServer", namespace: str = conf.socket.prefix.chat):
        super().__init__(sio, namespace)
