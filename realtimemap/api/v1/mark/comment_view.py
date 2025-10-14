from typing import Annotated, TYPE_CHECKING, List

from fastapi import APIRouter, Depends

from api.v1.auth.fastapi_users import get_current_user_without_ban
from dependencies.checker import check_mark_exist, check_mark_comment_exist
from dependencies.service import get_mark_comment_service
from errors import (
    RecordNotFoundError,
    UserPermissionError,
    NestingLevelExceededError,
)
from errors.utils import http_error_response_generator
from models.mark_comment.schemas import (
    CreateCommentRequest,
    ReadComment,
    CommentReactionRequest,
)

if TYPE_CHECKING:
    from services.mark_comment.service import MarkCommentService
    from models import User

GENERAL_ERROR_RESPONSES = http_error_response_generator(
    RecordNotFoundError, UserPermissionError
)

SUB_ERROR_RESPONSES = http_error_response_generator(NestingLevelExceededError)

router = APIRouter(
    prefix="/{mark_id}",
    tags=["Mark Comments"],
    dependencies=[Depends(check_mark_exist)],
    responses=GENERAL_ERROR_RESPONSES,
)


@router.post("/comments/", response_model=ReadComment, responses=SUB_ERROR_RESPONSES)
async def create_comment_endpoint(
    mark_id: int,
    service: Annotated["MarkCommentService", Depends(get_mark_comment_service)],
    user: Annotated["User", Depends(get_current_user_without_ban)],
    create_data: CreateCommentRequest,
):
    result = await service.create_comment(
        mark_id=mark_id, create_data=create_data, user=user
    )
    return result


@router.get("/comments/", response_model=List[ReadComment])
async def get_comments(
    mark_id: int,
    service: Annotated["MarkCommentService", Depends(get_mark_comment_service)],
):
    result = await service.get_comments(mark_id=mark_id)
    return result


@router.put("/comments/{comment_id}/", dependencies=[Depends(check_mark_comment_exist)])
async def add_comment_reaction(
    comment_id: int,
    user: Annotated["User", Depends(get_current_user_without_ban)],
    service: Annotated["MarkCommentService", Depends(get_mark_comment_service)],
    data: CommentReactionRequest,
):
    result = await service.create_or_update_comment_reaction(comment_id, data, user)
    return result
