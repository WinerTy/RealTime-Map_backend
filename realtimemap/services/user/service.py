from interfaces import IUserRepository, IUsersBanRepository, IUserSubscriptionRepository


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
