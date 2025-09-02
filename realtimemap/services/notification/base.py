import logging
from typing import List, Optional

from socketio import AsyncServer

logger = logging.getLogger(__name__)


class BaseNotificationSocketIO:
    def __init__(self, sio: AsyncServer):
        self.sio = sio

    def get_sids(self, namespace: str = "/") -> List[Optional[str]]:
        try:
            connections = self.sio.manager.rooms.get(namespace, {})
            if not connections:
                return []
            result = []
            for room_sid in connections:
                if room_sid:
                    result.append(room_sid)
            return result
        except Exception as e:
            logger.error(e)
            return []
