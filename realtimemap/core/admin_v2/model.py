import contextlib
import uuid
from typing import Optional

from fastadmin import register, SqlAlchemyModelAdmin

from database.helper import db_helper
from dependencies.auth.manager import get_user_manager
from dependencies.auth.users import get_users_db
from models import User
from models.user.schemas import UserLogin

get_users_db_context = contextlib.asynccontextmanager(get_users_db)
get_user_manager_context = contextlib.asynccontextmanager(get_user_manager)


@register(User, sqlalchemy_sessionmaker=db_helper.session_factory)
class UserAdmin(SqlAlchemyModelAdmin):
    print("Регистрация класса")
    exclude = ("hash_password",)
    list_display = ("id", "username", "is_superuser", "is_active")
    list_display_links = ("id", "username")
    list_filter = ("id", "username", "is_superuser", "is_active")
    search_fields = ("username",)

    @staticmethod
    async def authenticate_user(session, user_credentials: UserLogin) -> Optional[User]:
        async with get_users_db_context(session=session) as users_db:
            async with get_user_manager_context(users_db=users_db) as user_manager:
                user = await user_manager.authenticate(credentials=user_credentials)
                return user if user else None

    async def authenticate(
        self, username: str, password: str
    ) -> uuid.UUID | int | None:
        session_maker = self.get_sessionmaker()
        async with session_maker() as session:
            print(type(session))
            user = await self.authenticate_user(
                session, UserLogin(username=username, password=password)
            )
            if not user:
                return None
            return user
