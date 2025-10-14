import logging
from typing import TYPE_CHECKING

from fastapi import HTTPException

from errors import RecordNotFoundError
from errors.users import HaveActiveSubscriptionException
from integrations.payment.yookassa.exception import GatewayException
from models.user_subscription.schemas import CreateUserSubscription
from services.base import BaseService

if TYPE_CHECKING:
    from sqlalchemy.ext.asyncio import AsyncSession
    from interfaces import IUserSubscriptionRepository, ISubscriptionPlanRepository
    from models import User
    from integrations.payment.yookassa import YookassaClient

logger = logging.getLogger(__name__)


class SubscriptionService(BaseService):
    def __init__(
        self,
        session: "AsyncSession",
        user_subscription_repo: "IUserSubscriptionRepository",
        subscription_repo: "ISubscriptionPlanRepository",
    ):
        self.user_subscription_repo = user_subscription_repo
        self.subscription_repo = subscription_repo
        super().__init__(session)

    async def check_active_subscription(self, user_id: int) -> bool:
        have_active_subscription = (
            await self.user_subscription_repo.check_active_subscription(user_id)
        )
        if have_active_subscription:
            from errors.users import HaveActiveSubscriptionException

            raise HaveActiveSubscriptionException()

    async def create_subscription_offer(
        self,
        plan_id: int,
        user: "User",
        payment_client: "YookassaClient",
        redirect_url: str,
    ) -> str:
        try:
            await self.check_active_subscription(user.id)
            subscription_info = await self.subscription_repo.get_by_id(plan_id)
            if subscription_info is None:
                raise RecordNotFoundError()
            try:
                payment = payment_client.create_payment(
                    subscription_info.price,
                    redirect_url,
                    f"Offer for {subscription_info.plan_type} subscription!",
                    metadata={
                        "plan_id": plan_id,
                        "user_id": user.id,
                    },
                )
            except Exception:
                raise GatewayException()

            await self.user_subscription_repo.create(
                CreateUserSubscription(
                    user_id=user.id,
                    plan_id=plan_id,
                    expires_at=subscription_info.calculate_expires_at(),
                    payment_provider_id=payment.id,
                    is_active=False,
                )
            )
            return payment.confirmation["confirmation_url"]

        except RecordNotFoundError:
            raise
        except GatewayException:
            raise
        except HaveActiveSubscriptionException:
            raise
        except Exception as e:
            logger.error("Failed to create subscription offer", e)
            raise HTTPException(status_code=500, detail=str(e))
