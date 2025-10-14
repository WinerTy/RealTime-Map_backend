from typing import Optional, Dict

from fastapi import status

from errors.base import BaseRealTimeMapException


class TimeOutError(BaseRealTimeMapException):
    def __init__(
        self,
        detail: str = "Timeout expired",
        headers: Optional[Dict[str, str]] = None,
    ):
        super().__init__(
            detail=detail, status_code=status.HTTP_400_BAD_REQUEST, headers=headers
        )
