import logging
from typing import List, TYPE_CHECKING

from fastapi import (
    APIRouter,
    Depends,
    Form,
    BackgroundTasks,
    Request,
    Response,
)

from api.v1.auth.fastapi_users import Annotated, get_current_user_without_ban
from dependencies.notification import (
    get_mark_notification_service,
)
from dependencies.service import get_mark_service
from models.mark.schemas import (
    CreateMarkRequest,
    ReadMark,
    MarkRequestParams,
    DetailMark,
    UpdateMarkRequest,
    ActionType,
)
from models.mark.schemas.schemas import allowed_duration
from services.mark.service import MarkService
from services.notification import MarkNotificationService

if TYPE_CHECKING:
    from models import User


router = APIRouter(prefix="/marks", tags=["Marks"])

logger = logging.getLogger(__name__)

mark_service = Annotated[MarkService, Depends(get_mark_service)]

mark_notification_service = Annotated[
    MarkNotificationService, Depends(get_mark_notification_service)
]


@router.get("/", response_model=List[ReadMark], status_code=200)
async def get_marks(
    request: Request,
    service: mark_service,
    params: MarkRequestParams = Depends(),
):
    """
    Endpoint for getting all marks in radius, filtered by params.
    """
    result = await service.get_marks(params)
    return [
        ReadMark.model_validate(mark, context={"request": request}) for mark in result
    ]


@router.post(
    "/",
    response_model=ReadMark,
    status_code=201,
)
async def create_mark_point(
    background: BackgroundTasks,
    mark: Annotated[CreateMarkRequest, Form(media_type="multipart/form-data")],
    user: Annotated["User", Depends(get_current_user_without_ban)],
    service: mark_service,
    request: Request,
    notification: mark_notification_service,
):
    """
    Protected endpoint for create mark.
    """
    instance = await service.create_mark(mark, user)
    background.add_task(
        notification.notify_mark_action,
        mark=instance,
        event=ActionType.CREATE.value,
        request=request,
    )
    return ReadMark.model_validate(instance, context={"request": request})


@router.get("/{mark_id}/", response_model=DetailMark, status_code=200)
# @cache(expire=3600) TODO Fix
async def get_mark(mark_id: int, service: mark_service, request: Request):
    result = await service.get_mark_by_id(mark_id)
    return DetailMark.model_validate(result, context={"request": request})


@router.delete(
    "/{mark_id}/",
    status_code=204,
)
async def delete_mark(
    mark_id: int,
    background: BackgroundTasks,
    user: Annotated["User", Depends(get_current_user_without_ban)],
    service: mark_service,
    request: Request,
    notification: mark_notification_service,
):
    instance = await service.delete_mark(mark_id, user)
    background.add_task(
        notification.notify_mark_action,
        mark=instance,
        event=ActionType.DELETE.value,
        request=request,
    )
    return Response(status_code=204)


@router.patch(
    "/{mark_id}",
    response_model=ReadMark,
    status_code=200,
)
async def update_mark(
    mark_id: int,
    mark: Annotated[UpdateMarkRequest, Form(media_type="multipart/form-data")],
    service: mark_service,
    user: Annotated["User", Depends(get_current_user_without_ban)],
    request: Request,
    background: BackgroundTasks,
    notification: mark_notification_service,
):
    result = await service.update_mark(mark_id, mark, user)
    background.add_task(
        notification.notify_mark_action,
        mark=result,
        event=ActionType.UPDATE.value,
        request=request,
    )
    return ReadMark.model_validate(result, context={"request": request})


@router.get("/allowed-duration/", response_model=List[int], status_code=200)
async def get_allowed_duration():
    return allowed_duration


#
# def generate_random_point_in_radius(
#     center_lat: float, center_lon: float, radius: float
# ):
#     # Более точный вариант для небольших радиусов, использующий смещение в метрах # Переводим радиус в метры
#     distance = random.uniform(0, radius)
#     angle = random.uniform(0, 2 * math.pi)
#
#     delta_x = distance * math.cos(angle)
#     delta_y = distance * math.sin(angle)
#
#     new_lat = center_lat + (delta_y / 111139.0)
#     new_lon = center_lon + (delta_x / (111139.0 * math.cos(math.radians(center_lat))))
#
#     return new_lat, new_lon
#
#
# def generate_random_mark_time_data() -> Tuple[datetime, int]:
#     duration = random.choice(allowed_duration)
#     if random.random() < 0.7:
#         start_at = datetime.now() + timedelta(days=random.randint(-2, 3))
#     else:
#         start_at = datetime.now() + timedelta(days=random.randint(5, 7))
#     return start_at, duration
#
#
# """
# Задача: Создать тестовые метки в n количестве в радиусе от переданных координат.
# Для облегчения создания тестовых данных
#
# Задачи:
# 1. Получить ids Польователей и Категорий для рандомной выборки для тестовой метки. ГОТОВО
# 2. Сделать функцию для генерации даты. 70% активных в настоящее время и 30% для активности в будущем ГОТОВО
# 3. Функция для генерации рандомных координат в диапазоне пользователя
# 4. Создать тестовые данные
# """
#
#
# @router.post("/test/")
# async def create_test_marks(
#     data: CreateTestMarkRequest,
#     service: mark_service,
#     db: Annotated[AsyncSession, Depends(db_helper.session_getter)],
# ):
#
#     point = service.geo_service.create_point(data)
#
#     return data
