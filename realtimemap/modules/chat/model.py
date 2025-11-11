from typing import TYPE_CHECKING, List

from sqlalchemy import Column, Integer, ForeignKey, Table
from sqlalchemy.orm import relationship, Mapped

from modules import BaseSqlModel
from modules.mixins import TimeMarkMixin, IntIdMixin

if TYPE_CHECKING:
    from modules.user.model import User
    from modules.message.model import Message


chat_participants_table = Table(
    "chat_participants",
    BaseSqlModel.metadata,
    Column("user_id", Integer, ForeignKey("users.id"), primary_key=True),
    Column("chat_id", Integer, ForeignKey("chats.id"), primary_key=True),
)


class Chat(BaseSqlModel, IntIdMixin, TimeMarkMixin):
    participants: Mapped[List["User"]] = relationship(
        secondary=chat_participants_table, back_populates="chats"
    )

    # Связь с сообщениями в этом чате
    messages: Mapped[List["Message"]] = relationship(back_populates="chat")
