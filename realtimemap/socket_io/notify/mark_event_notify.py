from typing import Optional

from starlette.requests import Request

from core.app.socket import sio
from crud.mark import MarkRepository
from database.helper import db_helper
from models import Mark
from models.mark.schemas import action_type, MarkRequestParams, ReadMark
from socket_io.utils import get_sids


# Разбить на функции
async def notify_mark_action(
    mark: Mark, action: action_type, request: Optional[Request] = None
):
    try:
        async with db_helper.session_factory() as session:
            repo = MarkRepository(session)
            connections = get_sids(namespace="/marks")
            for room_name in connections:
                if room_name:
                    params: Optional[MarkRequestParams] = await sio.get_session(
                        room_name, "/marks"
                    )
                    if not params:
                        continue
                    in_range = await repo.check_distance(params, mark)
                    if in_range:
                        await sio.emit(
                            action,
                            to=room_name,
                            data=ReadMark.model_validate(
                                mark,
                                context={
                                    "request": request,
                                },
                            ).model_dump(mode="json"),
                            namespace="/marks",
                        )
    except Exception as e:
        print(e)
