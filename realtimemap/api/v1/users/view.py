from functools import partial
from typing import Annotated, TYPE_CHECKING

from fastapi import APIRouter, Request, Form, Depends
from fastapi_cache.decorator import cache
from fastapi_limiter.depends import RateLimiter
from starlette.responses import Response

from api.v1.auth.fastapi_users import get_current_user_without_ban, get_user_with_sub
from dependencies.crud import get_user_repository
from dependencies.service import get_user_service
from models.subscription.model import SubPlanType
from models.user.schemas import UserRead, UserUpdate
from services.user.service import UserService

if TYPE_CHECKING:
    from models import User
    from crud.user.repository import UserRepository

get_user_with_sub_ultra = partial(get_user_with_sub, sub_type=SubPlanType.ultra)

router = APIRouter(tags=["user"])


# TODO Убрать sub/ ban эндпоинты и переписать все в 1 метод с возможныстью управления состоянием ответа
@router.get(
    "/me",
    response_model=UserRead,
)
@cache(expire=3600, namespace="user")
async def me(
    user: Annotated["User", Depends(get_current_user_without_ban)], request: Request
):
    return UserRead.model_validate(user, context={"request": request})


@router.patch(
    "/me",
    response_model=UserRead,
    dependencies=[Depends(RateLimiter(times=2, minutes=5))],
)
async def update_me(
    user: Annotated["User", Depends(get_current_user_without_ban)],
    update_data: Annotated[UserUpdate, Form(media_type="multipart/form-data")],
    repo: Annotated["UserRepository", Depends(get_user_repository)],
    request: Request,
):
    result = await repo.update_user(user, update_data)
    return UserRead.model_validate(result, context={"request": request})


@router.delete("/me", status_code=204, response_class=Response)
async def delete_me(
    user: Annotated["User", Depends(get_current_user_without_ban)],
    repo: Annotated["UserRepository", Depends(get_user_repository)],
):
    await repo.delete_user(user)
    return Response(status_code=204)


@router.get("/me/subscriptions")
async def get_my_subscriptions(
    user: Annotated["User", Depends(get_current_user_without_ban)],
):
    return user.subscriptions


@router.get("/me/ban")
async def test_proto(
    user: Annotated["User", Depends(get_current_user_without_ban)],
    service: Annotated["UserService", Depends(get_user_service)],
):
    result = await service.is_ban(user.id)
    return result
