from datetime import datetime
from typing import Optional

from pydantic import BaseModel, Field, field_validator

from models.user.schemas import UserRead


class CreateComment(BaseModel):
    content: str
    owner_id: int
    mark_id: int
    parent_id: Optional[int] = None


class UpdateComment(BaseModel):
    content: str
    owner_id: int
    mark_id: int


class DeleteComment(BaseModel):
    content: str
    owner_id: int
    mark_id: int


class CreateCommentRequest(BaseModel):
    content: str = Field(..., description="Mark content", min_length=1, max_length=256)
    parent_id: Optional[int] = Field(None, description="Parent Mark id", ge=0)
