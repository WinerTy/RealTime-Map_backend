from typing import Any

from errors.base import RealTimeMapError


class NestingLevelExceededError(RealTimeMapError):
    def __init__(self, detail: str = "Nesting level exceeded"):
        super().__init__(detail)


class MessageSendingError(RealTimeMapError):
    def __init__(self, detail: str = "Message sending failed"):
        super().__init__(detail)


class HaveActiveSubscriptionError(RealTimeMapError):
    def __init__(self, detail: str = "You already have an active subscription"):
        super().__init__(detail)


class TimeOutError(RealTimeMapError):
    def __init__(self, detail: str = "The time for renewal has disappeared"):
        super().__init__(detail)


class UserPermissionError(RealTimeMapError):
    def __init__(self, detail: str = "Permission denied"):
        super().__init__(detail)


class NotFoundError(RealTimeMapError):
    def __init__(self, detail: str = "Record not found"):
        super().__init__(detail)


class IntegrityError(RealTimeMapError):
    def __init__(self, detail: str = "Record already exists"):
        super().__init__(detail)


class AuthenticationError(RealTimeMapError):
    def __init__(self, detail: str = "Authentication failed"):
        super().__init__(detail)


class ValidationError(RealTimeMapError):
    def __init__(
        self,
        field: str,
        user_input: Any,
        input_type: str,
        detail: str = "Validation failed",
    ):
        error_obj = [
            {
                "loc": ["body", field],
                "msg": detail,
                "input": user_input,
                "type": input_type,
            }
        ]
        super().__init__(error_obj)
