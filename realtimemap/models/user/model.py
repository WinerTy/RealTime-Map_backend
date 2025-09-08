from typing import TYPE_CHECKING, List

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
from models import BaseSqlModel
from models.mixins import IntIdMixin

if TYPE_CHECKING:
    from sqlalchemy.ext.asyncio import AsyncSession
    from models.user_ban.model import UsersBan
    from models.mark.model import Mark
    from models.mark_comment.model import Comment


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

    # RS
    marks: Mapped["Mark"] = relationship(
        "Mark",
        back_populates="owner",
    )
    comments: Mapped[List["Comment"]] = relationship(back_populates="owner")
    bans: Mapped[List["UsersBan"]] = relationship(
        back_populates="user",
        cascade="all, delete-orphan",
        foreign_keys="UsersBan.user_id",
        lazy="joined",
    )
    given_bans: Mapped[List["UsersBan"]] = relationship(
        back_populates="moderator", foreign_keys="UsersBan.moderator_id"
    )

    @classmethod
    def get_db(cls, session: "AsyncSession"):
        return MySQLAlchemyUserDatabase(session, cls)

    def __str__(self):
        return self.username

    async def __admin_repr__(self, _: Request):
        return self.username

    async def __admin_select2_repr__(self, _: Request) -> str:
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


# For Testing sync events in async projects
@event.listens_for(User, "before_insert")
def before_insert_listener(mapper, connection, target: User):
    print("before_insert")
    print("-" * 50)
    print(target.username)
