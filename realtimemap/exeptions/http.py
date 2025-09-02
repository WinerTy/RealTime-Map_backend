from typing import Dict, Optional

from fastapi import HTTPException, status


class RecordNotFoundError(HTTPException):
    def __init__(
        self,
        status_code: int = status.HTTP_404_NOT_FOUND,
        detail: str = "Record not found",
        headers: Optional[Dict[str, str]] = None,
    ) -> None:
        super().__init__(status_code=status_code, detail=detail, headers=headers)


class UserPermissionError(HTTPException):
    def __init__(
        self,
        status_code: int = status.HTTP_401_UNAUTHORIZED,
        detail: str = "Permission denied",
        headers: Optional[Dict[str, str]] = None,
    ):
        super().__init__(status_code=status_code, detail=detail, headers=headers)


class ClientError(HTTPException):
    status_code: int = status.HTTP_400_BAD_REQUEST


class TimeOutError(ClientError):
    def __init__(
        self,
        detail: str = "Timeout expired",
        headers: Optional[Dict[str, str]] = None,
    ):
        super().__init__(
            detail=detail, status_code=status.HTTP_400_BAD_REQUEST, headers=headers
        )
