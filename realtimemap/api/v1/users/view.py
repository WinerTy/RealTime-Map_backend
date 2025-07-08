from typing import Annotated

from fastapi import APIRouter, Request, Form, Depends
from fastapi_cache.decorator import cache
from fastapi_limiter.depends import RateLimiter
from starlette.responses import Response

from api.v1.auth.fastapi_users import current_user
from crud.user.repository import UserRepository
from dependencies.crud import get_user_repository
from models.user.schemas import UserRead, UserUpdate

router = APIRouter(prefix="/user", tags=["user"])


@router.get(
    "/me",
    response_model=UserRead,
)
@cache(expire=3600, namespace="user")
async def me(user: current_user, request: Request):
    return UserRead.model_validate(user, context={"request": request})


@router.patch(
    "/me",
    response_model=UserRead,
    dependencies=[Depends(RateLimiter(times=2, minutes=5))],
)
async def update_me(
    user: current_user,
    update_data: Annotated[UserUpdate, Form(media_type="multipart/form-data")],
    repo: Annotated[UserRepository, Depends(get_user_repository)],
    request: Request,
):
    result = await repo.update_user(user, update_data)
    return UserRead.model_validate(result, context={"request": request})


@router.delete("/me", status_code=204, response_class=Response)
async def delete_me(
    user: current_user, repo: Annotated[UserRepository, Depends(get_user_repository)]
):
    return await repo.delete_user(user)
