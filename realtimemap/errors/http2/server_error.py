from errors.base import RealTimeMapError


class GateWayError(RealTimeMapError):
    def __init__(
        self, detail: str = "The service is temporarily unavailable. Try again later."
    ):
        super().__init__(detail)
