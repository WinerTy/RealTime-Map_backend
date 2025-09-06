from datetime import datetime
from typing import Optional, List, Annotated

from pydantic import BaseModel, Field

from models.user.schemas import UserRead


class BaseComment(BaseModel):
    content: str = Field(..., description="Mark content", min_length=1, max_length=256)


class CreateComment(BaseComment):
    owner_id: Annotated[int, Field(0, ge=0, description="Owner id")]
    mark_id: Annotated[int, Field(0, ge=0, description="Mark id")]
    parent_id: Annotated[Optional[int], Field(..., description="Parent comment id")]


class UpdateComment(BaseComment):
    owner_id: Annotated[int, Field(0, ge=0, description="Owner id")]
    mark_id: Annotated[int, Field(0, ge=0, description="Mark id")]

    class Config:
        from_attributes = True


class BaseCommentStats(BaseModel):
    likes_count: Annotated[int, Field(default=0, description="Likes count", ge=0)]
    dislikes_count: Annotated[int, Field(default=0, description="Dislikes count", ge=0)]
    total_replies: Annotated[int, Field(0, ge=0)]

    class Config:
        from_attributes = True


class BaseReadComment(BaseComment):
    id: Annotated[int, Field(default=0, ge=0, description="id")]
    owner: UserRead
    created_at: datetime
    stats: BaseCommentStats


class ReadCommentReply(BaseReadComment):
    pass


class ReadComment(BaseReadComment):
    replies: Annotated[
        Optional[List[ReadCommentReply]],
        Field(list(), description="Replies to comment"),
    ]


class CreateCommentRequest(BaseComment):
    parent_id: Annotated[
        Optional[int], Field(None, description="Parent comment id", ge=0)
    ]


class CreateCommentStat(BaseCommentStats):
    comment_id: Annotated[int, Field(..., description="Comment id", ge=0)]
