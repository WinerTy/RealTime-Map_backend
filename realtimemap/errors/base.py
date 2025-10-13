from typing import Dict, Optional, TYPE_CHECKING

from fastapi import HTTPException

from errors.schemas import HTTPErrorDetail

if TYPE_CHECKING:
    from pydantic import BaseModel


class BaseRealTimeMapException(HTTPException):
    response_model: "BaseModel" = HTTPErrorDetail

    def __init__(
        self,
        status_code: int,
        detail: str = None,
        headers: Optional[Dict[str, str]] = None,
    ):
        super().__init__(status_code=status_code, detail=detail, headers=headers)
