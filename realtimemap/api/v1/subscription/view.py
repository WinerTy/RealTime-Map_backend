from typing import Annotated, List, TYPE_CHECKING

from fastapi import APIRouter, Depends, Request
from starlette.responses import RedirectResponse

from api.v1.auth.fastapi_users import get_current_user_without_ban
from crud.subcription.repository import SubscriptionPlanRepository
from dependencies.crud import get_subscription_plan_repository
from dependencies.payment import get_yookassa_client
from dependencies.service import get_subscription_service
from integrations.payment.yookassa import YookassaClient
from models.subscription.schemas import ReadSubscriptionPlan
from models.user_subscription.schemas import CreateSubscriptionRequest
from services.subscription.service import SubscriptionService

if TYPE_CHECKING:
    from models import User

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


@router.post("/")
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
