from typing import Protocol, Optional

from interfaces import IBaseRepository
from models import User, UsersBan, UserSubscription
from models.user.schemas import UserCreate, UserUpdate
from models.user_ban.schemas import UsersBanCreate, UsersBanUpdate
from models.user_subscription.schemas import (
    CreateUserSubscription,
    UpdateUserSubscription,
)


class IUserRepository(IBaseRepository[User, UserCreate, UserUpdate], Protocol):
    async def update_user(self, user: "User", update_data: UserUpdate) -> User: ...

    async def delete_user(self, user: "User") -> "User": ...

    async def user_is_banned(self, user_id: int) -> bool:
        """
        Check if the user is banned.

        Args:
            user_id (int): The id of the user.

        Returns:
            bool: Whether the user is banned.
        """
        ...


class IUsersBanRepository(
    IBaseRepository[UsersBan, UsersBanCreate, UsersBanUpdate], Protocol
):

    async def check_active_user_ban(self, user_id: int) -> bool: ...

    async def ban_user(self, data: UsersBanCreate) -> UsersBan: ...

    async def unban_user(self, user_id: int, data: UsersBanUpdate) -> UsersBan: ...


class IUserSubscriptionRepository(
    IBaseRepository[UserSubscription, CreateUserSubscription, UpdateUserSubscription],
    Protocol,
):
    async def check_active_subscription(
        self, user_id: int
    ) -> Optional[UserSubscription]: ...

    async def create_user_subscription(self, data: CreateUserSubscription): ...
