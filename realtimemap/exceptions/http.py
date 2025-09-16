from typing import Dict, Optional

from fastapi import status

from .base import BaseRealTimeMapException


class RecordNotFoundError(BaseRealTimeMapException):
    def __init__(
        self,
        status_code: int = status.HTTP_404_NOT_FOUND,
        detail: str = "Record not found",
        headers: Optional[Dict[str, str]] = None,
    ) -> None:
        super().__init__(status_code=status_code, detail=detail, headers=headers)


class NestingLevelExceededError(BaseRealTimeMapException):
    def __init__(
        self,
        status_code: int = status.HTTP_400_BAD_REQUEST,
        detail: str = "Nesting level exceeded",
        headers: Optional[Dict[str, str]] = None,
    ):
        super().__init__(status_code=status_code, detail=detail, headers=headers)
