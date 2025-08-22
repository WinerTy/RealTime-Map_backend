from typing import Annotated, TYPE_CHECKING

from fastapi import APIRouter, status, Depends
from fastapi_cache.decorator import cache
from fastapi_pagination import Page, Params
from fastapi_pagination.ext.sqlalchemy import apaginate

from api.v1.auth.fastapi_users import current_user
from dependencies.checker import check_mark_exist, check_mark_comment_exist
from dependencies.service import get_mark_service
from models.mark_comment.schemas import (
    CreateMarkCommentRequest,
    ReadMarkComment,
    UpdateMarkCommentReaction,
)

if TYPE_CHECKING:
    pass

router = APIRouter(prefix="/{record_id}", tags=["Mark Comments"])


@router.post(
    "/comment",
    status_code=201,
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


@router.get(
    "/comment",
    status_code=status.HTTP_200_OK,
    dependencies=[Depends(check_mark_exist)],
    response_model=Page[ReadMarkComment],
)
@cache(expire=3600, namespace="comments_list")
async def get_comments(
    record_id: int,
    service: Annotated["MarkService", Depends(get_mark_service)],
    params: Params = Depends(),
):
    comments = await service.get_comments(mark_id=record_id)
    return await apaginate(service.session, comments)


@router.patch(
    "/comment",
    status_code=status.HTTP_200_OK,
    dependencies=[Depends(check_mark_comment_exist)],
)
async def update_comment(
    record_id: int,
    service: Annotated["MarkService", Depends(get_mark_service)],
):
    pass


@router.patch("/comment/reaction", dependencies=[Depends(check_mark_comment_exist)])
async def reaction_comment(
    record_id: int,
    user: current_user,
    reaction: UpdateMarkCommentReaction,
    service: Annotated["MarkService", Depends(get_mark_service)],
):
    pass
