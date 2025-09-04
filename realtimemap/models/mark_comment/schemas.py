from datetime import datetime
from typing import Optional, List

from pydantic import BaseModel, Field, field_validator, field_serializer

from models.user.schemas import UserRead


class BaseComment(BaseModel):
    content: str = Field(..., description="Mark content", min_length=1, max_length=256)


class CreateComment(BaseComment):
    owner_id: int
    mark_id: int
    parent_id: Optional[int] = None


class UpdateComment(BaseComment):
    owner_id: int
    mark_id: int

    class Config:
        from_attributes = True


class CommentStats(BaseModel):
    likes_count: int
    dislikes_count: int
    total_replies: int

    class Config:
        from_attributes = True


class BaseReadComment(BaseComment):
    id: int
    owner: UserRead
    created_at: datetime
    stats: CommentStats


class ReadCommentReply(BaseReadComment):
    pass


class ReadComment(BaseReadComment):
    replies: Optional[List[ReadCommentReply]] = []


class CreateCommentRequest(BaseComment):
    parent_id: Optional[int] = Field(None, description="Parent comment id", ge=0)
