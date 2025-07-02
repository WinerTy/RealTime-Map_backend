from typing import TYPE_CHECKING

from fastapi import Request
from fastapi_users_db_sqlalchemy import SQLAlchemyBaseUserTable
from fastapi_users_db_sqlalchemy.access_token import (
    SQLAlchemyAccessTokenDatabase,
    SQLAlchemyBaseAccessTokenTable,
)
from jinja2 import Template
from sqlalchemy import String, Integer, ForeignKey, event
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy_file import ImageField

from auth.user_database import MySQLAlchemyUserDatabase
from models import BaseSqlModel, Mark
from models.mixins import IntIdMixin

if TYPE_CHECKING:
    from sqlalchemy.ext.asyncio import AsyncSession


class User(BaseSqlModel, IntIdMixin, SQLAlchemyBaseUserTable[int]):
    __tablename__ = "users"
    phone: Mapped[str] = mapped_column(
        String(32), unique=True, nullable=True, index=True
    )
    username: Mapped[str] = mapped_column(
        String(32), unique=True, nullable=False, index=True
    )

    avatar: Mapped[ImageField] = mapped_column(
        ImageField(upload_storage="users"), nullable=True
    )
    marks: Mapped["Mark"] = relationship(
        "Mark",
        back_populates="owner",
    )

    @classmethod
    def get_db(cls, session: "AsyncSession"):
        return MySQLAlchemyUserDatabase(session, cls)

    def __str__(self):
        return self.username

    async def __admin_repr__(self, request: Request):
        return self.username

    async def __admin_select2_repr__(self, request: Request) -> str:
        temp = Template("""<span>{{email}}</span>""", autoescape=True)
        return temp.render(email=self.email)


class AccessToken(BaseSqlModel, SQLAlchemyBaseAccessTokenTable[int]):
    user_id: Mapped[int] = mapped_column(
        Integer,
        ForeignKey("users.id", ondelete="cascade"),
        nullable=False,
    )

    @classmethod
    def get_db(cls, session: "AsyncSession"):
        return SQLAlchemyAccessTokenDatabase(session, cls)


@event.listens_for(User, "before_insert")
def before_insert_listener(mapper, connection, target):
    print("before_insert")
    print("-" * 50)
    print(target.username)
