from datetime import datetime
from typing import Annotated

from pydantic import Field, BaseModel, ConfigDict


class BaseMessage(BaseModel):
    content: Annotated[str, Field(..., description="Message content")]
    sender_id: Annotated[int, Field(..., description="Owner ID")]


class CreateMessage(BaseMessage):
    chat_id: Annotated[int, Field(description="Chat ID")]


class UpdateMessage(BaseMessage):
    pass


class ReadMessage(BaseMessage):
    id: Annotated[int, Field(ge=0)]
    created_at: Annotated[datetime, Field(..., description="Creation time")]

    model_config = ConfigDict(from_attributes=True)
