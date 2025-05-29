from fastapi import APIRouter

from dependencies.auth.backend import authentication_backend
from models.user.schemas import UserRead, UserCreate
from .fastapi_users import fastapi_users

router = APIRouter(
    prefix="/auth",
    tags=["Auth"],
)


router.include_router(
    router=fastapi_users.get_auth_router(
        authentication_backend,
    )
)
router.include_router(
    router=fastapi_users.get_register_router(
        UserRead,
        UserCreate,
    ),
)
