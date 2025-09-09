from datetime import datetime
from enum import Enum as PyEnum
from typing import TYPE_CHECKING, Optional

from sqlalchemy import ForeignKey, String, Enum, DateTime, func, Boolean
from sqlalchemy.orm import Mapped, mapped_column, relationship

from models import BaseSqlModel
from models.mixins import IntIdMixin

if TYPE_CHECKING:
    from models import User


class BanReason(str, PyEnum):
    abuse = "abuse"
    spam = "spam"
    other = "other"


# TODO ADD INDEX
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

    unbanned_at: Mapped[Optional[datetime]] = mapped_column(DateTime, nullable=True)
    unbanned_by: Mapped[Optional[int]] = mapped_column(
        ForeignKey("users.id", ondelete="SET NULL"), nullable=True
    )
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
