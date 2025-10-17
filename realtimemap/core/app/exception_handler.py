from typing import TYPE_CHECKING

from fastapi import status
from fastapi.responses import ORJSONResponse

from errors import UserPermissionError
from errors.http2 import (
    GateWayError,
    IntegrityError,
    NestingLevelExceededError,
    NotFoundError,
    TimeOutError,
)

if TYPE_CHECKING:
    from fastapi import FastAPI, Request


def register_exception_handler(app: "FastAPI"):
    @app.exception_handler(IntegrityError)
    async def integrity_error_handler(_: "Request", exc: IntegrityError):
        return ORJSONResponse(
            status_code=status.HTTP_400_BAD_REQUEST,
            content=exc.detail,
        )

    @app.exception_handler(GateWayError)
    async def gateway_error_handler(_: "Request", exc: GateWayError):
        return ORJSONResponse(
            status_code=status.HTTP_502_BAD_GATEWAY,
            content=exc.detail,
        )

    @app.exception_handler(NestingLevelExceededError)
    async def nesting_error_handler(_: "Request", exc: NestingLevelExceededError):
        return ORJSONResponse(
            status_code=status.HTTP_400_BAD_REQUEST,
            content=exc.detail,
        )

    @app.exception_handler(NotFoundError)
    async def not_found_error_handler(_: "Request", exc: NotFoundError):
        return ORJSONResponse(
            status_code=status.HTTP_404_NOT_FOUND,
            content=exc.detail,
        )

    @app.exception_handler(TimeOutError)
    async def timeout_error_handler(_: "Request", exc: TimeOutError):
        return ORJSONResponse(
            status_code=status.HTTP_400_BAD_REQUEST,
            content=exc.detail,
        )

    @app.exception_handler(UserPermissionError)
    async def user_permission_error_handler(_: "Request", exc: UserPermissionError):
        return ORJSONResponse(
            status_code=status.HTTP_403_FORBIDDEN,
            content=exc.detail,
        )
