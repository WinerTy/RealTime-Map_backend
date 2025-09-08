from typing import Annotated

from fastapi import Depends, status
from fastapi_users import FastAPIUsers

from crud.user.repository import UserRepository
from dependencies.auth.backend import authentication_backend
from dependencies.auth.manager import get_user_manager
from dependencies.crud import get_user_repository
from exceptions import UserPermissionError
from models import User

fastapi_users = FastAPIUsers[User, int](
    get_user_manager,
    [authentication_backend],
)


current_active_user = fastapi_users.current_user(active=True)
current_active_superuser = fastapi_users.current_user(active=True, superuser=True)


async def get_current_user(
    user_repo: Annotated[UserRepository, Depends(get_user_repository)],
    user: User = Depends(current_active_user),
):
    user_ban = await user_repo.user_is_banned(user.id)
    if user_ban:
        raise UserPermissionError(
            detail="You are banned at this time.", status_code=status.HTTP_403_FORBIDDEN
        )
    return user


current_user = Annotated[User, Depends(get_current_user)]
