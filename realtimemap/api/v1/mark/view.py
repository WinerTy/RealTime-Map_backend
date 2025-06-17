import logging
from typing import Annotated, List

from fastapi import APIRouter, Depends, Form, WebSocket, BackgroundTasks
from starlette.requests import Request
from starlette.responses import Response

from api.v1.auth.fastapi_users import current_active_user
from crud.mark import MarkRepository
from dependencies.crud import get_mark_repository
from dependencies.service import get_mark_service
from models import User
from models.mark.schemas import (
    CreateMarkRequest,
    ReadMark,
    MarkRequestParams,
)
from services.mark.service import MarkService
from websocket.mark_socket import marks_websocket

router = APIRouter(prefix="/marks", tags=["Marks"])

logger = logging.getLogger(__name__)


@router.get("/", response_model=List[ReadMark], status_code=200)
async def get_marks(
    request: Request,
    repo: Annotated["MarkRepository", Depends(get_mark_repository)],
    params: MarkRequestParams = Depends(),
):
    result = await repo.get_marks(params)
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
    instance = await service.service_create_mark(mark, user)
    # background.add_task(
    #     ws_manager.broadcast_json, ReadMark(**data).model_dump(mode="json")
    # )
    return instance


@router.get("/{mark_id}/", response_model=ReadMark, status_code=200)
# @cache(expire=3600) # TODO FIX
async def get_mark(
    mark_id: int,
    repo: Annotated["MarkRepository", Depends(get_mark_repository)],
):
    result = await repo.get_by_id(mark_id)
    return result


@router.delete("/{mark_id}", status_code=204)
async def delete_mark(
    mark_id: int,
    user: Annotated["User", Depends(current_active_user)],
    service: Annotated["MarkService", Depends(get_mark_service)],
):
    await service.mark_repo.delete_mark(mark_id, user)

    return Response(status_code=204)


# FIX, Context, serialize datetime field
@router.websocket("/")
async def websocket_endpoint(
    websocket: WebSocket, service: Annotated["MarkService", Depends(get_mark_service)]
):
    await marks_websocket.connect(websocket)

    while True:
        try:
            cords = await websocket.receive_json()
            await marks_websocket.update_coordinates(websocket, cords)
            actual_coords = marks_websocket.get_user_cords(websocket)
            result = await service.mark_repo.get_marks(
                MarkRequestParams(**actual_coords.model_dump())
            )
            result_json = [mark.model_dump(mode="json") for mark in result]
            await marks_websocket.broadcast_json(websocket, result_json)
        except Exception as e:
            await websocket.send_json({"message": "Disconnected", "error": str(e)})
            await marks_websocket.disconnect(websocket)
