from typing import Dict, Optional

from exceptions.base import BaseRealTimeMapException


class MessageSendingError(BaseRealTimeMapException):
    def __init__(
        self,
        status_code: int = 400,
        detail: str = "Error sending message",
        headers: Optional[Dict[str, str]] = None,
    ) -> None:
        super().__init__(status_code, detail, headers)
