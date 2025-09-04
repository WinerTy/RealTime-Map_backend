from typing import Annotated

from fastapi import Depends
from fastapi_users import FastAPIUsers

from dependencies.auth.backend import authentication_backend
from dependencies.auth.manager import get_user_manager
from models import User

fastapi_users = FastAPIUsers[User, int](
    get_user_manager,
    [authentication_backend],
)


current_active_user = fastapi_users.current_user(active=True)
current_active_superuser = fastapi_users.current_user(active=True, superuser=True)


async def get_current_user(user: User = Depends(current_active_user)):
    return user


current_user = Annotated[User, Depends(get_current_user)]
