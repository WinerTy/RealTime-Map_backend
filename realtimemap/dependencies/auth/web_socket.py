from typing import Annotated
from fastapi import Depends, WebSocket, status, WebSocketException

from .strategy import get_database_strategy
from fastapi_users.authentication.strategy import DatabaseStrategy

from .manager import get_user_manager
from auth.user_manager import UserManager

from models.user.schemas import UserRead


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
