from typing import Any, Optional

from socketio import AsyncNamespace
from socketio.exceptions import ConnectionRefusedError

from dependencies.auth.web_socket import socket_current_user


class ChatNamespace(AsyncNamespace):
    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)

    async def on_connect(self, sid, environ, auth):
        user = await socket_current_user(self.get_token(auth))
        if not user:
            raise ConnectionRefusedError("Authentication required")

    @staticmethod
    def get_token(auth: Any) -> Optional[str]:
        token = auth.get("token", None)
        return token
