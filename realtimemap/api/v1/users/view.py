from typing import Annotated, TYPE_CHECKING, List

from fastapi import APIRouter, Request, Form, Depends, Query
from fastapi_limiter.depends import RateLimiter
from starlette.responses import Response

from api.v1.auth.fastapi_users import get_current_user_without_ban, get_current_user
from modules.user.dependencies import get_user_repository
from modules.user.schemas import UserRead, UserUpdate, UserRequestParams
from modules.user.service import UserService
from modules.user.service_depenencies import get_user_service

if TYPE_CHECKING:
    from modules import User
    from modules.user.repository import UserRepository


router = APIRouter(tags=["user"])


@router.get(
    "/me",
    response_model=UserRead,
)
# @cache(expire=3600, namespace="user")
async def me(
    request: Request,
    user: Annotated["User", Depends(get_current_user)],
    params: Annotated[UserRequestParams, Query()],
    service: Annotated["UserService", Depends(get_user_service)],
):
    result = await service.get_included_user_info(request, user, params)
    return result


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


@router.get("/leaderboard", response_model=List[UserRead])
async def get_leaderboard(
    request: Request, service: Annotated["UserService", Depends(get_user_service)]
):
    leaders = await service.get_leaderboard(request)
    return leaders
