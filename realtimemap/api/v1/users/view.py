from typing import Annotated

from fastapi import APIRouter, Request, Form
from fastapi_cache.decorator import cache

from api.v1.auth.fastapi_users import current_user
from models.user.schemas import UserRead, UserUpdate

router = APIRouter(prefix="/user", tags=["user"])


@router.get("/me", response_model=UserRead)
@cache(expire=3600, namespace="user")
async def me(user: current_user, request: Request):
    return UserRead.model_validate(user, context={"request": request})


@router.patch("/me", response_model=UserRead)
async def update_me(
    user: current_user,
    update_data: Annotated[UserUpdate, Form(media_type="multipart/form-data")],
):
    pass
