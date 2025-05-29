from typing import Annotated, List

from fastapi import APIRouter, Depends, Form, WebSocketDisconnect, WebSocket
from pydantic import BaseModel, Field
from starlette.requests import Request

from api.v1.auth.fastapi_users import current_active_user
from crud.mark import MarkRepository
from dependencies.crud import get_mark_repository
from models import User
from models.mark.schemas import CreateMarkRequest, ReadMark
from websocket.mark_socket import marks_websocket

router = APIRouter(prefix="/marks", tags=["Marks"])


class MarkParams(BaseModel):
    latitude: float = Field(..., ge=-180, le=180, examples=["75.445675"])
    longitude: float = Field(..., ge=-90, le=90, examples=["63.201907"])
    radius: int = Field(500, description="Search radius in meters.")
    srid: int = Field(4326, description="SRID")


@router.get("/", response_model=List[ReadMark])
async def get_marks(
    request: Request,
    repo: Annotated["MarkRepository", Depends(get_mark_repository)],
    params: MarkParams = Depends(),
):
    result = await repo.get_marks(**params.model_dump())
    return [
        ReadMark.model_validate(mark, context={"request": request}) for mark in result
    ]


@router.post("/", response_model=ReadMark)
async def create_mark_point(
    mark: Annotated[CreateMarkRequest, Form(media_type="multipart/form-data")],
    user: Annotated["User", Depends(current_active_user)],
    repo: Annotated["MarkRepository", Depends(get_mark_repository)],
    request: Request,
):
    """
    Protected endpoint for create mark.
    """
    instance = await repo.create_mark(mark, user)
    data = instance.__dict__
    data.pop("geom")  # FIX THIS
    return ReadMark.model_validate(data, context={"request": request})


@router.get(
    "/{mark_id}/",
)
async def get_mark(
    mark_id: int,
    repo: Annotated["MarkRepository", Depends(get_mark_repository)],
    request: Request,
):
    result = await repo.get_mark_by_id(mark_id)
    result = result.__dict__
    result.pop("geom")
    return ReadMark.model_validate(result, context={"request": request})


@router.delete("/{mark_id}")
async def delete_mark(
    mark_id: int,
    user: Annotated["User", Depends(current_active_user)],
):
    pass


@router.websocket("/")
async def websocket_endpoint(
    websocket: WebSocket,
    repo: Annotated["MarkRepository", Depends(get_mark_repository)],
):
    await marks_websocket.connect(websocket)

    while True:
        try:
            cords = await websocket.receive_json()
            await marks_websocket.update_coordinates(websocket, cords)
            actual_coords = marks_websocket.get_user_cords(websocket)
            result = await repo.get_marks(**actual_coords.model_dump())
            result_json = [
                mark.model_dump(context={"request": websocket}) for mark in result
            ]
            await marks_websocket.broadcast_json(websocket, result_json)
        except WebSocketDisconnect:
            await marks_websocket.disconnect(websocket)
