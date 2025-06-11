from sqlalchemy import String, ForeignKey, Boolean
from sqlalchemy.orm import Mapped, mapped_column

from models import BaseSqlModel
from models.mixins import IntIdMixin, TimeMarkMixin


class Message(BaseSqlModel, IntIdMixin, TimeMarkMixin):
    sender_id: Mapped[int] = mapped_column(ForeignKey("users.id"), nullable=False)
    recipient_id: Mapped[int] = mapped_column(ForeignKey("users.id"), nullable=False)
    content: Mapped[str] = mapped_column(String(256), nullable=False)
    is_read: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False)
