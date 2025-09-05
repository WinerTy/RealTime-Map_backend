from datetime import datetime
from typing import TYPE_CHECKING

from sqlalchemy import ForeignKey, String, Enum, DateTime, func, Boolean
from sqlalchemy.orm import Mapped, mapped_column, relationship

from models import BaseSqlModel
from models.mixins import IntIdMixin
from enum import Enum as PyEnum

if TYPE_CHECKING:
    from models import User


class BanReason(str, PyEnum):
    abuse = "abuse"
    spam = "spam"
    other = "other"


class UsersBan(BaseSqlModel, IntIdMixin):
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

    # FK
    user_id: Mapped[int] = mapped_column(
        ForeignKey("users.id", ondelete="CASCADE"), nullable=False
    )
    moderator_id: Mapped[int] = mapped_column(
        ForeignKey("users.id", ondelete="CASCADE"), nullable=False
    )

    # RS
    user: Mapped["User"] = relationship(back_populates="bans", foreign_keys=[user_id])
    moderator: Mapped["User"] = relationship(
        back_populates="given_bans", foreign_keys=[moderator_id]
    )
