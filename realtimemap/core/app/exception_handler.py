from typing import TYPE_CHECKING

from fastapi import status
from fastapi.responses import ORJSONResponse

from errors import RealTimeMapIntegrityError
from errors.http2 import GateWayError

if TYPE_CHECKING:
    from fastapi import FastAPI, Request


def register_exception_handler(app: "FastAPI"):
    @app.exception_handler(RealTimeMapIntegrityError)
    async def integrity_error_handler(_: "Request", exc: RealTimeMapIntegrityError):
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
