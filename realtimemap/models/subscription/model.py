from datetime import datetime, timedelta
from decimal import Decimal
from enum import Enum as PyEnum
from typing import Optional, Dict, Any, List, TYPE_CHECKING

from sqlalchemy import String, DECIMAL, Boolean, Enum, Integer
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm import Mapped, mapped_column, relationship

from models import BaseSqlModel
from models.mixins import TimeMarkMixin, IntIdMixin

if TYPE_CHECKING:
    from models.user_subscription.model import UserSubscription


class SubPlanType(str, PyEnum):
    premium = "premium"
    premium_plus = "premium Plus"
    ultra = "ultra"


class SubscriptionPlan(BaseSqlModel, IntIdMixin, TimeMarkMixin):
    # Main fields
    name: Mapped[str] = mapped_column(String(length=128), nullable=False)
    price: Mapped[Decimal] = mapped_column(
        DECIMAL(precision=10, scale=2), nullable=False
    )
    duration_days: Mapped[int] = mapped_column(Integer, nullable=False)
    plan_type: Mapped[str] = mapped_column(
        Enum(SubPlanType, name="plan_type_enum"),
        nullable=False,
        default=SubPlanType.premium.value,
        server_default=SubPlanType.premium.value,
        index=True,
    )

    # Field for sub bonuses example: exp_bonus_multiplier: 1.2, day_limit_for_create_mark: 10 and etc
    features: Mapped[Optional[Dict[str, Any]]] = mapped_column(
        JSONB, nullable=True, default=dict
    )

    # MetaFields
    is_active: Mapped[bool] = mapped_column(Boolean, nullable=False, default=True)

    # RS
    user_subscriptions: Mapped[List["UserSubscription"]] = relationship(
        back_populates="plan"
    )

    def calculate_expires_at(self) -> datetime:
        expires_at = datetime.now() + timedelta(days=self.duration_days)
        return expires_at
