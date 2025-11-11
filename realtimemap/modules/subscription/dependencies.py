from typing import AsyncGenerator, Annotated, Any

from fastapi import Depends

from database.helper import db_helper
from modules.user_subscription.dependencies import get_user_subscription_repository
from .repository import SubscriptionPlanRepository
from .service import SubscriptionService


async def get_subscription_plan_repository(
    session: Annotated["AsyncSession", Depends(db_helper.session_getter)],
):
    yield SubscriptionPlanRepository(session=session)


async def get_subscription_service(
    user_subscription_repo: Annotated[
        "IUserSubscriptionRepository", Depends(get_user_subscription_repository)
    ],
    subscription_repo: Annotated[
        "ISubscriptionPlanRepository", Depends(get_subscription_plan_repository)
    ],
) -> AsyncGenerator[SubscriptionService, Any]:
    yield SubscriptionService(user_subscription_repo, subscription_repo)
