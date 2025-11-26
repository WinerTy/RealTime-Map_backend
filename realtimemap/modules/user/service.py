import asyncio
from typing import TYPE_CHECKING, Optional, List

from errors.http2 import AuthenticationError
from modules.user_ban.schemas import ReadUsersBan
from .schemas import (
    UserRead,
    UserRequestParams,
    UserRelationShip,
    ReadUserSubscription,
    UserGamefication,
    UserUpdate,
)
from ..gamefication.schemas.level.crud import LevelRead

if TYPE_CHECKING:
    from modules import User
    from fastapi import Request
    from core.common.repository import (
        UserRepository,
        LevelRepository,
        UsersBanRepository,
        UserSubscriptionRepository,
    )


class UserService:
    def __init__(
        self,
        user_repo: "UserRepository",
        user_ban_repo: "UsersBanRepository",
        user_subs_repo: "UserSubscriptionRepository",
        level_repo: "LevelRepository",
    ):
        self.user_repo = user_repo
        self.user_ban_repo = user_ban_repo
        self.user_subs_repo = user_subs_repo
        self.level_repo = level_repo

    async def is_ban(self, user_id: int) -> bool:
        return await self.user_repo.user_is_banned(user_id)

    async def _load_subscriptions(
        self, user_id: int, request: "Request"
    ) -> List[ReadUserSubscription]:
        user_subs = await self.user_subs_repo.get_user_subscriptions(user_id)
        return (
            [
                ReadUserSubscription.model_validate(sub, context={"request": request})
                for sub in user_subs
            ]
            if user_subs
            else []
        )

    async def _load_bans(self, user_id: int, request: "Request") -> List[ReadUsersBan]:
        user_bans = await self.user_ban_repo.get_user_bans(user_id)
        return (
            [
                ReadUsersBan.model_validate(ban, context={"request": request})
                for ban in user_bans
            ]
            if user_bans
            else []
        )

    async def _load_gamefication(self, user: "User") -> Optional[UserGamefication]:
        next_level = None
        raw_level = await self.level_repo.get_next_level(user.level)
        if raw_level:
            next_level = LevelRead.model_validate(raw_level)
        return UserGamefication(
            current_level=user.level,
            current_exp=user.current_exp,
            next_level=next_level,
        )

    async def get_included_user_info(
        self, request: "Request", user: "User", params: UserRequestParams
    ) -> UserRead:
        if not user:
            raise AuthenticationError()

        user_response = UserRead.model_validate(user, context={"request": request})

        if not params.include:
            return user_response

        # Параллельная загрузка
        tasks = []
        include_mapping = {}

        if UserRelationShip.SUBSCRIPTION in params.include:
            tasks.append(self._load_subscriptions(user.id, request))
            include_mapping[len(tasks) - 1] = "subscriptions"

        if UserRelationShip.BANS in params.include:
            tasks.append(self._load_bans(user.id, request))
            include_mapping[len(tasks) - 1] = "bans"

        if UserRelationShip.GAMEFICATION in params.include:
            tasks.append(self._load_gamefication(user))
            include_mapping[len(tasks) - 1] = "gamefication"

        if tasks:
            results = await asyncio.gather(*tasks)
            for idx, result in enumerate(results):
                field_name = include_mapping[idx]
                if result:
                    setattr(user_response, field_name, result)

        return user_response

    async def get_leaderboard(self, request: "Request"):
        leaders = await self.user_repo.get_users_for_leaderboard()
        users = [
            UserRead.model_validate(leader, context={"request": request})
            for leader in leaders
        ]
        return users

    async def update_user(self, user_id: int, update_data: UserUpdate) -> "User":
        user = await self.user_repo.update(user_id, update_data)
        return user

    async def delete_user(self, user_id: int) -> None:
        await self.user_repo.delete(user_id)
