from typing import Optional, Dict

from fastapi import status

from errors.base import BaseRealTimeMapException


class HttpIntegrityError(BaseRealTimeMapException):
    def __init__(
        self,
        status_code: int = status.HTTP_400_BAD_REQUEST,
        detail=None,
        headers: Optional[Dict[str, str]] = None,
    ):
        self.detail = {"detail": "Record already exists."}
        super().__init__(status_code=status_code, detail=detail, headers=headers)
