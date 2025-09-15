from typing import Annotated

from fastapi import Depends

from core.app.socket import sio
from crud.mark import MarkRepository
from dependencies.crud import get_mark_repository
from services.geo.dependency import get_geo_service
from services.geo.service import GeoService
from services.notification import MarkNotificationService, ChatNotificationService


async def get_mark_notification_service(
    mark_repo: Annotated[MarkRepository, Depends(get_mark_repository)],
    geo_service: Annotated[GeoService, Depends(get_geo_service)],
) -> MarkNotificationService:
    yield MarkNotificationService(mark_repo=mark_repo, geo_service=geo_service, sio=sio)


async def get_chat_notification_service() -> ChatNotificationService:
    yield ChatNotificationService(sio=sio)
