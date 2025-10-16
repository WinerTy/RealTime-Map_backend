from datetime import datetime
from typing import Annotated, Optional

from fastapi import Depends
from fastapi_users import FastAPIUsers
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from crud.user_ban.repository import UsersBanRepository
from database.helper import db_helper
from dependencies.auth.backend import authentication_backend
from dependencies.auth.manager import get_user_manager
from dependencies.crud import get_user_ban_repository
from errors import UserPermissionError
from models import User, UserSubscription, SubscriptionPlan
from models.subscription.model import SubPlanType

fastapi_users = FastAPIUsers[User, int](
    get_user_manager,
    [authentication_backend],
)


current_active_user = fastapi_users.current_user(active=True)
current_active_superuser = fastapi_users.current_user(active=True, superuser=True)


async def get_current_user_without_ban(
    user_ban_repo: Annotated[UsersBanRepository, Depends(get_user_ban_repository)],
    user: User = Depends(current_active_user),
):
    user_ban = await user_ban_repo.check_active_user_ban(user.id)
    if user_ban:
        raise UserPermissionError(detail="You are banned at this time.")
    return user


async def get_current_user(user: User = Depends(current_active_user)):
    return user


current_user = Annotated[User, Depends(get_current_user_without_ban)]


async def get_user_with_sub(
    session: Annotated["AsyncSession", Depends(db_helper.session_factory)],
    user: Annotated[User, Depends(current_active_user)],
    sub_type: Optional[SubPlanType] = None,
):

    now = datetime.now()

    stmt = (
        select(UserSubscription)
        .join(SubscriptionPlan)
        .where(
            UserSubscription.user_id == user.id,
            UserSubscription.is_active,
            UserSubscription.expires_at > now,
        )
    )
    if sub_type:
        stmt = stmt.where(SubscriptionPlan.plan_type == sub_type)

    result = await session.execute(stmt)
    active_sub = result.scalar_one_or_none()

    if not active_sub:
        raise UserPermissionError(detail="You dont have permission to do that.")

    return user
