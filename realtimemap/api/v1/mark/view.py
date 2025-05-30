from typing import Annotated, List

from fastapi import APIRouter, Depends, Form, WebSocketDisconnect, WebSocket
from pydantic import BaseModel, Field
from starlette.requests import Request
from starlette.responses import Response

from api.v1.auth.fastapi_users import current_active_user
from crud.mark import MarkRepository
from dependencies.crud import get_mark_repository
from dependencies.service import get_mark_service
from models import User
from models.mark.schemas import CreateMarkRequest, ReadMark
from services.mark.service import MarkService
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
    service: Annotated["MarkService", Depends(get_mark_service)],
    request: Request,
):
    """
    Protected endpoint for create mark.
    """
    instance = await service.service_create_mark(mark, user)
    end_at = instance.end_at
    data = instance.__dict__
    data["end_at"] = end_at
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
    end_at = result.end_at
    result = result.__dict__
    result["end_at"] = end_at
    result.pop("geom")
    return ReadMark.model_validate(result, context={"request": request})


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
            result = await service.mark_repo.get_marks(**actual_coords.model_dump())
            result_json = [
                mark.model_dump(
                    context={"request": websocket}, exclude=["start_at", "end_at"]
                )
                for mark in result
            ]
            await marks_websocket.broadcast_json(websocket, result_json)
        except WebSocketDisconnect:
            await marks_websocket.disconnect(websocket)
