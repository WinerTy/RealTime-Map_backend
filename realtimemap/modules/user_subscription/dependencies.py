from typing import TYPE_CHECKING, Annotated

from fastapi import Depends

from database.helper import db_helper
from modules.user_subscription.repository import UserSubscriptionRepository

if TYPE_CHECKING:
    from sqlalchemy.ext.asyncio import AsyncSession


async def get_user_subscription_repository(
    session: Annotated["AsyncSession", Depends(db_helper.session_getter)],
):
    yield UserSubscriptionRepository(session=session)
