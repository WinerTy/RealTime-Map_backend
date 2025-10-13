from typing import TYPE_CHECKING

from crud import BaseRepository
from models import RequestLog
from models.request_log.schemas import (
    CreateRequestLog,
    UpdateRequestLog,
)

if TYPE_CHECKING:
    from sqlalchemy.ext.asyncio import AsyncSession


class RequestLogRepository(
    BaseRepository[RequestLog, CreateRequestLog, UpdateRequestLog]
):
    def __init__(self, session: "AsyncSession"):
        super().__init__(model=RequestLog, session=session)
