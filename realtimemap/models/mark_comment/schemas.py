from datetime import datetime
from typing import Optional

from pydantic import BaseModel, Field

from models.user.schemas import UserRead


class BaseMarkComment(BaseModel):
    content: str = Field(..., description="Mark content", min_length=1, max_length=256)


class CreateMarkComment(BaseMarkComment):
    mark_id: int = Field(..., description="Mark id", ge=0)
    user_id: int = Field(..., description="User id", ge=0)


class UpdateMarkCommentReaction(BaseModel):
    likes: int = Field(..., description="Likes", ge=0)
    dislikes: int = Field(..., description="Dislikes", ge=0)


class UpdateMarkComment(BaseMarkComment, UpdateMarkCommentReaction):
    pass


class ReadMarkComment(BaseMarkComment):
    mark_id: int = Field(..., description="Mark id", ge=0)
    likes: int = Field(..., description="Likes", ge=0)
    dislikes: int = Field(..., description="Dislikes", ge=0)
    created_at: datetime = Field(..., description="Creation date in ISO format")
    user: Optional[UserRead] = None


class CreateMarkCommentRequest(BaseMarkComment):
    pass
