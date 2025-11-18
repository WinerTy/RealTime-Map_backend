from typing import TYPE_CHECKING

from errors.http2 import AuthenticationError
from interfaces import IUserRepository, IUsersBanRepository, IUserSubscriptionRepository
from modules.user_ban.schemas import ReadUsersBan
from .schemas import (
    UserRead,
    UserRequestParams,
    UserRelationShip,
    ReadUserSubscription,
    UserGamefication,
)
from ..gamefication.schemas.level.crud import LevelRead

if TYPE_CHECKING:
    from modules import User
    from fastapi import Request
    from modules.gamefication.repository import LevelRepository


class UserService:
    def __init__(
        self,
        user_repo: "IUserRepository",
        user_ban_repo: "IUsersBanRepository",
        user_subs_repo: "IUserSubscriptionRepository",
        level_repo: "LevelRepository",
    ):
        self.user_repo = user_repo
        self.user_ban_repo = user_ban_repo
        self.user_subs_repo = user_subs_repo
        self.level_repo = level_repo

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

        if UserRelationShip.GAMEFICATION in params.include:
            raw_level = await self.level_repo.get_next_level(user.level)
            level = LevelRead.model_validate(raw_level)
            user_response.gamefication = UserGamefication(
                current_level=user.level,
                current_exp=user.current_exp,
                next_level=level,
            )
        return user_response

    async def get_leaderboard(self, request: "Request"):
        leaders = await self.user_repo.get_users_for_leaderboard()
        users = [
            UserRead.model_validate(leader, context={"request": request})
            for leader in leaders
        ]
        return users
