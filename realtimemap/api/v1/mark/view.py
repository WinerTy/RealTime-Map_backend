import logging
from typing import Annotated, List, Optional

from fastapi import (
    APIRouter,
    Depends,
    Form,
    BackgroundTasks,
    Request,
    Response,
    WebSocket,
)

from api.v1.auth.fastapi_users import current_active_user
from core.app.socket import sio
from crud.mark import MarkRepository
from database.helper import db_helper
from dependencies.service import get_mark_service
from models import User, Mark
from models.mark.schemas import (
    CreateMarkRequest,
    ReadMark,
    MarkRequestParams,
    action_type,
)
from services.mark.service import MarkService

router = APIRouter(prefix="/marks", tags=["Marks"])

logger = logging.getLogger(__name__)


async def notify_mark_action(mark: Mark, action: action_type):
    try:
        async with db_helper.session_factory() as session:
            repo = MarkRepository(session)
            connections = sio.manager.rooms.get("/marks", {})
            if not connections:
                return
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
                            data=mark.id,
                            namespace="/marks",
                        )
    except Exception as e:
        print(e)


@router.get("/", response_model=List[ReadMark], status_code=200)
async def get_marks(
    # request: Request, mb for generate full url
    service: Annotated["MarkService", Depends(get_mark_service)],
    params: MarkRequestParams = Depends(),
):
    """
    Endpoint for getting all marks in radius, filtered by params.
    """
    result = await service.get_marks(params)
    return result


@router.post("/", response_model=ReadMark, status_code=201)
async def create_mark_point(
    background: BackgroundTasks,
    mark: Annotated[CreateMarkRequest, Form(media_type="multipart/form-data")],
    user: Annotated["User", Depends(current_active_user)],
    service: Annotated["MarkService", Depends(get_mark_service)],
    request: Request,
):
    """
    Protected endpoint for create mark.
    """
    instance = await service.create_mark(mark, user)
    background.add_task(
        notify_mark_action,
        mark=instance,
        action="create",
    )
    return instance


@router.get("/{mark_id}/", response_model=ReadMark, status_code=200)
# @cache(expire=3600)
async def get_mark(
    mark_id: int,
    service: Annotated["MarkService", Depends(get_mark_service)],
):
    result = await service.get_mark_by_id(mark_id)
    return result


@router.delete("/{mark_id}", status_code=204)
async def delete_mark(
    mark_id: int,
    background: BackgroundTasks,
    user: Annotated["User", Depends(current_active_user)],
    service: Annotated["MarkService", Depends(get_mark_service)],
):
    instance = await service.mark_repo.delete_mark(mark_id, user)
    return Response(status_code=204)


@router.websocket("/")
async def mark_websocket_endpoint(
    websocket: WebSocket,
    service: Annotated["MarkService", Depends(get_mark_service)],
):
    await service.manager.connect(websocket)

    while True:
        params = await websocket.receive_json()
        await service.manager.set_params(
            websocket=websocket, params=MarkRequestParams(**params)
        )
