from typing import Optional, Dict

from .client import ClientError
from fastapi import status


class UserPermissionError(ClientError):
    def __init__(
        self,
        status_code: int = status.HTTP_401_UNAUTHORIZED,
        detail: str = "Permission denied",
        headers: Optional[Dict[str, str]] = None,
    ):
        super().__init__(status_code=status_code, detail=detail, headers=headers)
