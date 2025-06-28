from typing import Any, Optional

import socketio
from socketio import AsyncNamespace

from crud.mark import MarkRepository
from database.helper import db_helper
from models.mark.schemas import MarkRequestParams, ReadMark

sio = socketio.AsyncServer(
    async_mode="asgi",
    cors_allowed_origins=[],
    client_manager=socketio.AsyncManager(),
)
sio_app = socketio.ASGIApp(socketio_server=sio)


class MarksNamespace(AsyncNamespace):
    async def on_connect(self, sid, environ, auth):
        print(f"Клиент подключился к marks_ws: {sid}")

    async def on_disconnect(self, sid):
        pass

    async def on_message(self, sid, data):
        params = self._validate_params(data)
        await self.save_session(sid, params)
        if params:
            async with db_helper.session_factory() as session:
                repo = MarkRepository(session)
                result = await repo.get_marks(params)
                result = [
                    ReadMark(end_at=mark.end_at, **mark.__dict__).model_dump(
                        mode="json"
                    )
                    for mark in result
                ]
                await self.emit("get_marks", data=result, to=sid)

    @staticmethod
    def _validate_params(data: Any) -> Optional[MarkRequestParams]:
        try:
            valid_params = MarkRequestParams(**data)
            return valid_params
        except Exception:
            return None


sio.register_namespace(MarksNamespace("/marks"))
