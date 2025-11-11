from typing import TYPE_CHECKING

from errors.http2 import AuthenticationError
from interfaces import IUserRepository, IUsersBanRepository, IUserSubscriptionRepository
from modules.user_ban.schemas import ReadUsersBan
from .schemas import UserRead, UserRequestParams, UserRelationShip, ReadUserSubscription

if TYPE_CHECKING:
    from modules import User
    from fastapi import Request


class UserService:
    def __init__(
        self,
        user_repo: "IUserRepository",
        user_ban_repo: "IUsersBanRepository",
        user_subs_repo: "IUserSubscriptionRepository",
    ):
        self.user_repo = user_repo
        self.user_ban_repo = user_ban_repo
        self.user_subs_repo = user_subs_repo

    async def is_ban(self, user_id: int) -> bool:
        return await self.user_repo.user_is_banned(user_id)

    async def get_included_user_info(
        self, request: "Request", user: "User", params: UserRequestParams
    ) -> UserRead:
        if not user:
            raise AuthenticationError()
        user_response = UserRead.model_validate(user, context={"request": request})

        if not params.include:
            return user_response

        if UserRelationShip.SUBSCRIPTION in params.include:
            user_subs = await self.user_subs_repo.get_user_subscriptions(user.id)
            if user_subs:
                user_response.subscriptions = [
                    ReadUserSubscription.model_validate(
                        sub, context={"request": request}
                    )
                    for sub in user_subs
                ]
        if UserRelationShip.BANS in params.include:
            user_bans = await self.user_ban_repo.get_user_bans(user.id)
            if user_bans:
                user_response.bans = [
                    ReadUsersBan.model_validate(ban, context={"request": request})
                    for ban in user_bans
                ]

        return user_response
