from interfaces import IUserRepository


class UserService:
    def __init__(self, user_repo: "IUserRepository"):
        self.user_repo = user_repo

    async def is_ban(self, user_id: int) -> bool:
        return await self.user_repo.user_is_banned(user_id)
