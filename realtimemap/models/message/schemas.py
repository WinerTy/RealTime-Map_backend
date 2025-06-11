from pydantic import Field, BaseModel


class BaseMessage(BaseModel):
    content: str = Field(
        ..., description="Message content", max_length=256, min_length=1
    )
    recipient_id: int = Field(..., description="Recipient ID")
    owner_id: int = Field(..., description="Owner ID")


class CreateMessage(BaseMessage):
    pass


class UpdateMessage(BaseMessage):
    pass


class ReadMessage(BaseMessage):
    pass


class CreateMessageRequest(BaseModel):
    content: str = Field(
        ..., description="Message content", max_length=256, min_length=1
    )
    recipient_id: int = Field(..., description="Recipient ID")
