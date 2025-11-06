from typing import TYPE_CHECKING, List

from fastapi import Request
from fastapi_users_db_sqlalchemy import SQLAlchemyBaseUserTable
from fastapi_users_db_sqlalchemy.access_token import (
    SQLAlchemyAccessTokenDatabase,
    SQLAlchemyBaseAccessTokenTable,
)
from jinja2 import Template
from sqlalchemy import String, Integer, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy_file import ImageField

from auth.user_database import MySQLAlchemyUserDatabase
from models import BaseSqlModel
from models.mixins import IntIdMixin

if TYPE_CHECKING:
    from sqlalchemy.ext.asyncio import AsyncSession
    from models.user_ban.model import UsersBan
    from models.mark.model import Mark
    from models.mark_comment.model import Comment, CommentReaction
    from models.message.model import Chat
    from models.user_subscription.model import UserSubscription


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
        "UsersBan",
        back_populates="user",
        foreign_keys="UsersBan.user_id",
        cascade="all, delete-orphan",
        lazy="noload",
    )
    issued_bans: Mapped[List["UsersBan"]] = relationship(
        "UsersBan",
        back_populates="moderator",
        foreign_keys="UsersBan.moderator_id",
        cascade="all, delete-orphan",
        lazy="selectin",
    )
    chats: Mapped[List["Chat"]] = relationship(
        secondary="chat_participants", back_populates="participants"
    )
    reactions: Mapped[List["CommentReaction"]] = relationship(
        back_populates="user", foreign_keys="CommentReaction.user_id"
    )
    subscriptions: Mapped[List["UserSubscription"]] = relationship(
        "UserSubscription",
        back_populates="user",
        cascade="all, delete-orphan",
        lazy="noload",
    )

    @classmethod
    def get_db(cls, session: "AsyncSession"):
        return MySQLAlchemyUserDatabase(session, cls)

    def __str__(self):
        return self.username

    async def __admin_repr__(self, _: Request) -> str:
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
