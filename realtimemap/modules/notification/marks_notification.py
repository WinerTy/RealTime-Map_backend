import logging
from typing import List, Optional, Dict, Set, TYPE_CHECKING

from fastapi import Request
from socketio import AsyncServer

from core.config import conf
from modules import Mark
from modules.geo_service import GeoService, get_geo_service
from modules.mark.filters import MarkFilter
from modules.mark.schemas import MarkRequestParams, ReadMark
from .base import BaseNotificationSocketIO

if TYPE_CHECKING:
    from core.common.repository import MarkRepository


logger = logging.getLogger(__name__)


class MarkNotificationService(BaseNotificationSocketIO):
    def __init__(
        self,
        mark_repo: "MarkRepository",
        sio: AsyncServer,
        geo_service: GeoService = get_geo_service(),
        namespace: str = conf.socket.prefix.marks,
    ):
        super().__init__(sio, namespace)
        self.mark_repo = mark_repo
        self.geo_service = geo_service

    async def notify_mark_action(
        self, mark: Mark, event: str, request: Optional[Request] = None
    ):
        try:
            room_sids = self.get_sids(self.namespace)
            if not room_sids:
                return

            sessions = await self._get_sessions(room_sids)

            targets = await self._filter_connection_in_range(sessions, mark)
            if not targets:
                return

            mark_data = ReadMark.model_validate(
                mark, context={"request": request}
            ).model_dump(mode="json")

            await self._send_notifications(targets, event, mark_data)

        except Exception as e:
            logger.error(e)

    async def _get_sessions(
        self, room_sids: List[str]
    ) -> Dict[str, Optional[MarkRequestParams]]:
        sessions = {}
        for sid in room_sids:
            try:
                params = await self.sio.get_session(sid, self.namespace)
                sessions[sid] = params
            except Exception as e:
                logger.error(e)
                sessions[sid] = None

        return sessions

    async def _filter_connection_in_range(
        self, sessions: Dict[str, Optional[MarkRequestParams]], mark: Mark
    ) -> Set[str]:
        targets = set()

        for sid, params in sessions.items():
            if not params:
                continue

            if not self.geo_service.check_geohash_proximity(coords=params, mark=mark):
                continue

            in_range = await self.mark_repo.check_distance(
                MarkFilter.from_request(params), mark
            )
            if in_range:
                targets.add(sid)

        return targets
