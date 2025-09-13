from datetime import datetime
from typing import Annotated

from pydantic import BaseModel, Field, ConfigDict

from models.message import ReadMessage
from models.user.schemas import UserRead


class BaseChat(BaseModel):
    pass


class CreateChat(BaseChat):
    pass


class UpdateChat(BaseChat):
    pass


class ReadChat(BaseChat):
    id: Annotated[int, Field(ge=0, description="Chat ID")]
    created_at: Annotated[datetime, Field(..., description="Creation time")]
    other_participant: UserRead
    last_message: ReadMessage

    model_config = ConfigDict(from_attributes=True)
