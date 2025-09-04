from typing import Annotated, TYPE_CHECKING, List

from fastapi import APIRouter, status, Depends
from fastapi_cache.decorator import cache
from fastapi_pagination import Page, Params
from fastapi_pagination.ext.sqlalchemy import apaginate

from api.v1.auth.fastapi_users import current_user
from crud.mark_comment import MarkCommentRepository
from dependencies.checker import check_mark_exist, check_mark_comment_exist
from dependencies.crud import get_mark_comment_repository
from dependencies.service import get_mark_service, get_mark_comment_service
from models import Comment
from models.mark_comment.schemas import (
    CreateCommentRequest,
    CreateComment,
    ReadComment,
)
from services.mark_comment.service import MarkCommentService

if TYPE_CHECKING:
    pass

router = APIRouter(
    prefix="/{mark_id}",
    tags=["Mark Comments"],
    dependencies=[Depends(check_mark_exist)],
    responses={
        status.HTTP_404_NOT_FOUND: {
            "description": "Mark not found",
            "content": {
                "application/json": {
                    "schema": {
                        "type": "object",
                        "properties": {
                            "detail": {"type": "string"},
                        },
                    }
                }
            },
        }
    },
)

comment_service = Annotated[MarkCommentService, Depends(get_mark_comment_service)]


@router.post(
    "/comments/",
)
async def create_comment_endpoint(
    mark_id: int,
    service: comment_service,
    user: current_user,
    create_data: CreateCommentRequest,
):
    result = await service.create_comment(
        mark_id=mark_id, create_data=create_data, user=user
    )
    return result


@router.get("/comments/", response_model=List[ReadComment])
async def get_comments(
    mark_id: int,
    service: comment_service,
):
    result = await service.get_comments(mark_id=mark_id)
    return result
