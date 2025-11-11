import logging
from typing import List, Optional, Set

from socketio import AsyncServer

logger = logging.getLogger(__name__)


class BaseNotificationSocketIO:
    def __init__(self, sio: AsyncServer, namespace: str):
        self.sio = sio
        self.namespace = namespace

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

    async def _send_notifications(
        self, targets: Set[str], event: str, data: dict, *, room: Optional[str] = None
    ) -> None:
        for sid in targets:
            try:
                await self.sio.emit(
                    event, to=sid, namespace=self.namespace, data=data, room=room
                )
            except Exception as e:
                logger.error(e)
