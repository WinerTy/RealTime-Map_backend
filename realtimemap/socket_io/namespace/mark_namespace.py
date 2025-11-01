import logging
from typing import Any, Optional

from socketio import AsyncNamespace

from crud.mark import MarkRepository
from database.helper import db_helper
from models.mark.filters import MarkFilter
from models.mark.schemas import MarkRequestParams, ReadMark
from services.geo.service import GeoService

logger = logging.getLogger(__name__)


# TODO СДЕЛАТЬ РУМЫ ПО ГЕОХЭШУ ДЛЯ СОКРАЩЕНИЯ ЧИСЛА ЗАПРОСОВ
class MarksNamespace(AsyncNamespace):
    def __init__(self, namespace=None):
        super().__init__(namespace)
        self.geo_service = GeoService()

    @staticmethod
    async def on_connect(sid, environ, auth):
        pass

    @staticmethod
    async def on_disconnect(sid):
        pass

    async def on_marks_message(self, sid, data):
        params = self._validate_params(data)
        await self.save_session(sid, params)
        if params:
            async with db_helper.session_factory() as session:
                repo = MarkRepository(session)
                result = await repo.get_marks(params)
                result = [
                    ReadMark.model_validate(mark).model_dump(mode="json")
                    for mark in result
                ]
                await self.emit("marks_get", data=result, to=sid)

    async def on_message(self, sid, data):
        pass

    def _validate_params(self, data: Any) -> Optional[MarkFilter]:
        try:
            req = MarkRequestParams(**data)
            filters = MarkFilter.from_request(req, self.geo_service)
            return filters
        except Exception as e:
            logger.error(f"Error on validate params in socker.io: {e}")
            return None
