from typing import Dict, Optional

from exceptions.base import BaseRealTimeMapException


# TODO Maybe Rename
class GatewayException(BaseRealTimeMapException):
    def __init__(
        self,
        status_code: int = 502,
        detail: str = "Gateway Error",
        headers: Optional[Dict[str, str]] = None,
    ):
        super().__init__(status_code=status_code, detail=detail, headers=headers)
