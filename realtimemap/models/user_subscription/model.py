from datetime import datetime
from enum import Enum as PyEnum
from typing import TYPE_CHECKING, Optional

from sqlalchemy import ForeignKey, DateTime, func, Boolean, String, Enum
from sqlalchemy.orm import Mapped, mapped_column, relationship

from models import BaseSqlModel
from models.mixins import IntIdMixin, TimeMarkMixin

if TYPE_CHECKING:
    from models import User, SubscriptionPlan


class PaymentStatus(str, PyEnum):
    succeeded = "succeeded"
    waiting_for_capture = "waiting_for_capture"
    canceled = "canceled"


class UserSubscription(BaseSqlModel, IntIdMixin, TimeMarkMixin):
    # FK
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
    plan_id: Mapped[int] = mapped_column(ForeignKey("subscription_plans.id"))

    starts_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), nullable=False, server_default=func.now()
    )
    expires_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), nullable=False, index=True
    )
    is_active: Mapped[bool] = mapped_column(
        Boolean, nullable=False, default=True, index=True
    )
    payment_provider_id: Mapped[Optional[str]] = mapped_column(
        String(length=128), nullable=True
    )
    payment_status: Mapped[str] = mapped_column(
        Enum(PaymentStatus, name="payment_status_type"),
        nullable=True,
        default=PaymentStatus.waiting_for_capture.value,
        server_default=PaymentStatus.waiting_for_capture.value,
        index=True,
    )
    # RS
    user: Mapped["User"] = relationship("User", back_populates="subscriptions")
    plan: Mapped["SubscriptionPlan"] = relationship(
        back_populates="user_subscriptions", lazy="joined"
    )
