from typing import TYPE_CHECKING

from sqlalchemy import String, ForeignKey, Boolean
from sqlalchemy.orm import Mapped, mapped_column, relationship

from modules import BaseSqlModel
from modules.mixins import IntIdMixin, TimeMarkMixin

if TYPE_CHECKING:
    from modules.chat.model import Chat


class Message(BaseSqlModel, IntIdMixin, TimeMarkMixin):
    # FK
    sender_id: Mapped[int] = mapped_column(ForeignKey("users.id"), nullable=False)
    chat_id: Mapped[int] = mapped_column(ForeignKey("chats.id"), nullable=False)
    # attrs
    is_read: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False)
    content: Mapped[str] = mapped_column(String(256), nullable=False)
    # RS
    chat: Mapped["Chat"] = relationship(back_populates="messages")
