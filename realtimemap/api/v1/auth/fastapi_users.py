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

current_user = Annotated[User, Depends(current_active_user)]
