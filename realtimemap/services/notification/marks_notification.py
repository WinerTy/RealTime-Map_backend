from typing import List, Optional, Dict, Set

from socketio import AsyncServer

from crud.mark import MarkRepository
from models import Mark
from models.mark.schemas import MarkRequestParams, action_type, ReadMark
from services.geo.service import GeoService
import logging
from fastapi import Request

from .base import BaseNotificationSocketIO

logger = logging.getLogger(__name__)


class MarkNotificationService(BaseNotificationSocketIO):
    def __init__(
        self, mark_repo: MarkRepository, sio: AsyncServer, geo_service: GeoService
    ):
        super().__init__(sio)
        self.mark_repo = mark_repo
        self.geo_service = geo_service
        self.namespace: str = "/marks"

    async def notify_mark_action(
        self, mark: Mark, action: action_type, request: Optional[Request] = None
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

            await self._send_notifications(targets, action, mark_data)

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
            print(params)
            print(mark)
            if not self.geo_service.check_geohash_proximity(coords=params, mark=mark):
                continue

            in_range = await self.mark_repo.check_distance(params, mark)
            if in_range:
                targets.add(sid)

        return targets

    async def _send_notifications(
        self, targets: Set[str], action: action_type, mark_data: dict
    ) -> None:
        for sid in targets:
            try:
                await self.sio.emit(
                    action,
                    to=sid,
                    namespace=self.namespace,
                    data=mark_data,
                )
            except Exception as e:
                logger.error(e)
