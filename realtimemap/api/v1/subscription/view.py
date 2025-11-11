from typing import Annotated, List, TYPE_CHECKING

from fastapi import APIRouter, Depends, Request
from fastapi.responses import RedirectResponse

from api.v1.auth.fastapi_users import get_current_user_without_ban
from dependencies.payment import get_yookassa_client
from integrations.payment.yookassa import YookassaClient
from modules.subscription.dependencies import (
    get_subscription_plan_repository,
    get_subscription_service,
)
from modules.subscription.repository import SubscriptionPlanRepository
from modules.subscription.schemas import ReadSubscriptionPlan
from modules.subscription.service import SubscriptionService
from modules.user_subscription.schemas import CreateSubscriptionRequest

if TYPE_CHECKING:
    from modules import User


router = APIRouter(
    prefix="/subscription",
    tags=["subscription"],
)

get_sub_repo = Annotated[
    SubscriptionPlanRepository, Depends(get_subscription_plan_repository)
]


@router.get("/", response_model=List[ReadSubscriptionPlan])
async def get_subscription_plans(repo: get_sub_repo):
    result = await repo.get_subscription_plans()
    return result


@router.post(
    "/",
    response_class=RedirectResponse,
    status_code=307,
)
async def purchase_subscription(
    data: CreateSubscriptionRequest,
    user: Annotated["User", Depends(get_current_user_without_ban)],
    service: Annotated["SubscriptionService", Depends(get_subscription_service)],
    payment_client: Annotated["YookassaClient", Depends(get_yookassa_client)],
    request: Request,
):
    redirect_url = await service.create_subscription_offer(
        data.plan_id, user, payment_client, str(request.url)
    )
    return RedirectResponse(url=redirect_url)
