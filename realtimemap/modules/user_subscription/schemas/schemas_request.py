from typing import Annotated

from pydantic import BaseModel, Field


class CreateSubscriptionRequest(BaseModel):
    plan_id: Annotated[int, Field(..., ge=0, description="Plan id")]
