from typing import Annotated, List

from fastapi import APIRouter, Depends

from crud.subcription.repository import SubscriptionPlanRepository
from dependencies.crud import get_subscription_plan_repository
from models.subscription.schemas import ReadSubscriptionPlan

router = APIRouter(
    prefix="/subscription",
    tags=["subscription"],
)


@router.get("/", response_model=List[ReadSubscriptionPlan])
async def get_subscription_plans(
    repo: Annotated[
        SubscriptionPlanRepository, Depends(get_subscription_plan_repository)
    ],
):
    result = await repo.get_subscription_plans()
    return result
