from fastapi import APIRouter, Request

from api.v1.auth.fastapi_users import current_user
from models.user.schemas import UserRead

router = APIRouter(prefix="/user", tags=["user"])


@router.get("/", response_model=UserRead)
async def me(user: current_user, request: Request):
    return UserRead.model_validate(user, context={"request": request})
