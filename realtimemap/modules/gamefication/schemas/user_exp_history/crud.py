from decimal import Decimal
from typing import Annotated, Optional

from pydantic import BaseModel, Field


class BaseUserExpHistory(BaseModel):
    user_id: Annotated[int, Field(..., description="The id of the user")]
    action_id: Annotated[int, Field(..., description="The id of the action")]
    is_revoked: Annotated[
        Optional[bool], Field(False, description="The id of the user")
    ]
    base_exp: Annotated[int, Field(..., description="Base exp")]
    multiplier: Annotated[Decimal, Field(..., description="Multiplier")]
    total_exp: Annotated[int, Field(..., description="Total exp")]
    source_type: Annotated[Optional[str], Field(None, description="Total exp")]
    source_id: Annotated[Optional[int], Field(None, description="Source record id")]
    level_before: Annotated[int, Field(..., description="Level before")]
    level_after: Annotated[int, Field(..., description="Level after")]
    exp_before: Annotated[int, Field(..., description="Exp before")]
    subscription_plan_id: Annotated[
        Optional[int], Field(None, description="Subscription plan")
    ]


class CreateUserExpHistory(BaseUserExpHistory):
    pass


class UpdateUserExpHistory(BaseUserExpHistory):
    revoked_reason: Optional[str] = Field(None, description="Revoked reason")
