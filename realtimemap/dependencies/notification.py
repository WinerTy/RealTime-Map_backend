from typing import Annotated, Any, AsyncGenerator, TYPE_CHECKING

from fastapi import Depends

from core.app.socket import sio
from modules.geo_service import GeoService, get_geo_service
from modules.mark.dependencies import get_pg_mark_repository
from modules.notification import MarkNotificationService, ChatNotificationService

if TYPE_CHECKING:
    from core.common.repository import MarkRepository


def get_mark_notification_service(
    mark_repo: Annotated["MarkRepository", Depends(get_pg_mark_repository)],
    geo_service: Annotated[GeoService, Depends(get_geo_service)],
) -> MarkNotificationService:
    return MarkNotificationService(
        mark_repo=mark_repo, geo_service=geo_service, sio=sio
    )


async def get_chat_notification_service() -> (
    AsyncGenerator[ChatNotificationService, Any]
):
    yield ChatNotificationService(sio=sio)
