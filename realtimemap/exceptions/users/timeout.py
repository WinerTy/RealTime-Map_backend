from typing import Optional, Dict
from fastapi import status
from .client import ClientError


class TimeOutError(ClientError):
    def __init__(
        self,
        detail: str = "Timeout expired",
        headers: Optional[Dict[str, str]] = None,
    ):
        super().__init__(
            detail=detail, status_code=status.HTTP_400_BAD_REQUEST, headers=headers
        )
