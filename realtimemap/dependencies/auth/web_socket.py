import contextlib
from typing import Annotated, Optional

from fastapi import Depends, WebSocket, status, WebSocketException
from fastapi_users.authentication.strategy import DatabaseStrategy

from auth.user_manager import UserManager
from database.helper import db_helper
from models import User
from models.user.schemas import UserRead
from utils.dependency_resolver import resolve_dependency
from .access_token import get_access_token_db
from .manager import get_user_manager
from .strategy import get_database_strategy
from .users import get_users_db


async def websocket_auth(
    websocket: WebSocket,
    strategy: Annotated["DatabaseStrategy", Depends(get_database_strategy)],
    manager: Annotated["UserManager", Depends(get_user_manager)],
) -> UserRead:
    token = websocket.headers.get("token")

    if not token:
        raise WebSocketException(
            code=status.WS_1008_POLICY_VIOLATION,
            reason="Token is required",
        )

    user = await strategy.read_token(token, user_manager=manager)
    if not user:
        raise WebSocketException(
            code=status.WS_1008_POLICY_VIOLATION,
        )
    return UserRead(**user.__dict__)


async def socket_current_user(token: str) -> Optional[User]:
    async with contextlib.AsyncExitStack() as stack:
        # Инициализация всех зависимостей
        session = await stack.enter_async_context(
            resolve_dependency(db_helper.session_getter)
        )
        access_token_db = await stack.enter_async_context(
            resolve_dependency(get_access_token_db, session)
        )
        strategy = await stack.enter_async_context(
            resolve_dependency(get_database_strategy, access_token_db)
        )
        users_db = await stack.enter_async_context(
            resolve_dependency(get_users_db, session)
        )
        user_manager = await stack.enter_async_context(
            resolve_dependency(get_user_manager, users_db)
        )

        user = await strategy.read_token(token, user_manager=user_manager)
        return user
