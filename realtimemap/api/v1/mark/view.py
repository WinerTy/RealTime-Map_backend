import logging
from typing import Annotated, List, Optional

from fastapi import (
    APIRouter,
    Depends,
    Form,
    BackgroundTasks,
    Request,
    Response,
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


def get_sids(namespace: str = "/") -> List[Optional[str]]:
    try:
        connections = sio.manager.rooms.get(namespace, {})
        if not connections:
            return []
        result = []
        for room_sid in connections:
            if room_sid:
                result.append(room_sid)
        return result
    except Exception:
        return []


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


@router.get("/", response_model=List[ReadMark], status_code=200)
async def get_marks(
    request: Request,
    service: Annotated["MarkService", Depends(get_mark_service)],
    params: MarkRequestParams = Depends(),
):
    """
    Endpoint for getting all marks in radius, filtered by params.
    """
    result = await service.get_marks(params)
    return [
        ReadMark.model_validate(mark, context={"request": request}) for mark in result
    ]


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
        action="marks_created",
    )
    return ReadMark.model_validate(instance, context={"request": request})


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
    background.add_task(
        notify_mark_action,
        mark=instance,
        action="marks_deleted",
    )
    return Response(status_code=204)
