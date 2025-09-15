from typing import Dict, Optional

from fastapi import HTTPException


class MessageSendingError(HTTPException):
    def __init__(
        self,
        status_code: int = 400,
        detail: str = "",
        headers: Optional[Dict[str, str]] = None,
    ) -> None:
        super().__init__(status_code, detail, headers)
