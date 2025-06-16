from fastapi import APIRouter, status, Depends
from typing import Annotated, TYPE_CHECKING
from models.mark_comment.schemas import CreateMarkCommentRequest
from api.v1.auth.fastapi_users import current_user
from dependencies.service import get_mark_service
from dependencies.checker import check_mark_exist

if TYPE_CHECKING:
    from services.mark.service import MarkService

router = APIRouter(prefix="/{record_id}", tags=["Mark Comments"])


@router.post(
    "/comment",
    status_code=status.HTTP_201_CREATED,
    dependencies=[Depends(check_mark_exist)],
)
async def create_comment(
    record_id: int,
    user: current_user,
    data: CreateMarkCommentRequest,
    service: Annotated["MarkService", Depends(get_mark_service)],
):
    result = await service.create_comment(user=user, data=data, mark_id=record_id)
    return result
