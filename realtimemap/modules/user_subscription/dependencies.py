from typing import TYPE_CHECKING, Annotated

from fastapi import Depends

from database import get_session
from modules.user_subscription.repository import UserSubscriptionRepository

if TYPE_CHECKING:
    from sqlalchemy.ext.asyncio import AsyncSession


async def get_user_subscription_repository(
    session: Annotated["AsyncSession", Depends(get_session)],
):
    yield UserSubscriptionRepository(session=session)
