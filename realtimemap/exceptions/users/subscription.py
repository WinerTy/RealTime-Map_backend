from typing import Dict, Optional

from fastapi import status

from exceptions.base import BaseRealTimeMapException


class HaveActiveSubscriptionException(BaseRealTimeMapException):
    def __init__(
        self,
        status_code: int = status.HTTP_400_BAD_REQUEST,
        detail: str = "You already have an active subscription",
        headers: Optional[Dict[str, str]] = None,
    ):
        super().__init__(status_code=status_code, detail=detail, headers=headers)
