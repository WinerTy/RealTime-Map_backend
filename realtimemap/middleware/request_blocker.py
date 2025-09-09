from typing import List

from fastapi.responses import ORJSONResponse
from starlette.middleware.base import (
    BaseHTTPMiddleware,
    DispatchFunction,
    RequestResponseEndpoint,
)
from starlette.requests import Request
from starlette.responses import Response
from starlette.types import ASGIApp


class RequestBlockerMiddleware(BaseHTTPMiddleware):
    def __init__(self, app: ASGIApp, dispatch: DispatchFunction | None = None):
        super().__init__(app, dispatch)
        self.blocked_resources: List[str] = [".php", ".env"]

    async def dispatch(
        self, request: Request, call_next: RequestResponseEndpoint
    ) -> Response:
        path = request.url.path.lower()
        for resource in self.blocked_resources:
            if resource in path:
                return ORJSONResponse(
                    status_code=403, content={"detail": "Blocked resource"}
                )

        return await call_next(request)
