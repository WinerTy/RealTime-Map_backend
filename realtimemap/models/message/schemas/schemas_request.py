from datetime import datetime
from typing import Annotated, Optional

from pydantic import BaseModel, Field


class CreateMessageRequest(BaseModel):
    recipient_id: Annotated[int, Field(..., description="Recipient ID", ge=0)]
    content: Annotated[str, Field(..., description="Message content")]


class UpdateMessageRequest(BaseModel):
    content: Annotated[str, Field(..., description="Message content")]


class MessageParamsRequest(BaseModel):
    before: Annotated[Optional[datetime], Field(None, description="Before date")]
    limit: Annotated[Optional[int], Field(50, description="count max messages")]
