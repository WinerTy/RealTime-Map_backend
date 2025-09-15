from typing import Optional, Dict

from fastapi import status

from .client import ClientError


class UserPermissionError(ClientError):
    def __init__(
        self,
        status_code: int = status.HTTP_403_FORBIDDEN,
        detail: str = "Permission denied",
        headers: Optional[Dict[str, str]] = None,
    ):
        super().__init__(status_code=status_code, detail=detail, headers=headers)
