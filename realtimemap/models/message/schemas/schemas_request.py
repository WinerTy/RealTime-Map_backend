from typing import Annotated

from pydantic import BaseModel, Field


class CreateMessageRequest(BaseModel):
    recipient_id: Annotated[int, Field(..., description="Recipient ID", ge=0)]
    content: Annotated[str, Field(..., description="Message content")]


class UpdateMessageRequest(BaseModel):
    content: Annotated[str, Field(..., description="Message content")]
