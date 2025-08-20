from typing import Any, Optional

from socketio import AsyncNamespace

from crud.mark import MarkRepository
from database.helper import db_helper
from models.mark.schemas import MarkRequestParams, ReadMark


class MarksNamespace(AsyncNamespace):
    async def on_connect(self, sid, environ, auth):
        print(auth)

    async def on_disconnect(self, sid):
        print(sid, "disconnect")

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

    @staticmethod
    def _validate_params(data: Any) -> Optional[MarkRequestParams]:
        try:
            valid_params = MarkRequestParams(**data)
            return valid_params
        except Exception:
            return None
