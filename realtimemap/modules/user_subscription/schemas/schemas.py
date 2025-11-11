from datetime import datetime
from typing import Annotated, Optional

from pydantic import BaseModel, Field, ConfigDict

from modules.user_subscription.model import PaymentStatus


class BaseUserSubscription(BaseModel):
    payment_provider_id: Annotated[
        Optional[str], Field(None, description="Payment provider id")
    ]


class CreateUserSubscription(BaseUserSubscription):
    user_id: Annotated[int, Field(..., ge=0, description="User id")]
    plan_id: Annotated[int, Field(..., ge=0, description="Plan id")]
    expires_at: Annotated[datetime, Field(..., description="Expiration date")]
    is_active: Annotated[bool, Field(True, description="Is active")]
    payment_status: Annotated[
        PaymentStatus,
        Field(PaymentStatus.waiting_for_capture, description="Payment status"),
    ]


class UpdateUserSubscription(BaseUserSubscription):
    pass


class ReadUserSubscription(BaseUserSubscription):
    starts_at: Annotated[datetime, Field(..., description="Start date")]
    expires_at: Annotated[datetime, Field(..., description="Expires date")]

    model_config = ConfigDict(from_attributes=True)
