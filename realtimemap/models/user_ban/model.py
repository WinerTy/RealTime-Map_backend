from datetime import datetime

from sqlalchemy import ForeignKey, String, Enum, DateTime, func, Boolean
from sqlalchemy.orm import Mapped, mapped_column

from models import BaseSqlModel
from models.mixins import IntIdMixin
from enum import Enum as PyEnum


class BanReason(str, PyEnum):
    abuse = "abuse"
    spam = "spam"
    other = "other"


class UsersBan(BaseSqlModel, IntIdMixin):
    user_id: Mapped[int] = mapped_column(
        ForeignKey("users.id", ondelete="CASCADE"), nullable=False
    )
    moderator_id: Mapped[int] = mapped_column(
        ForeignKey("users.id", ondelete="CASCADE"), nullable=False
    )
    reason: Mapped[str] = mapped_column(
        Enum(BanReason, name="ban_reason"),
        nullable=False,
        default=BanReason.abuse,
        server_default=BanReason.abuse.value,
    )
    reason_text: Mapped[str] = mapped_column(String(length=128), nullable=True)

    banned_at: Mapped[datetime] = mapped_column(
        DateTime, nullable=False, server_default=func.now()
    )
    banned_until: Mapped[datetime] = mapped_column(DateTime, nullable=True)
    is_permanent: Mapped[bool] = mapped_column(Boolean, default=False)
