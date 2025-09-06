from datetime import datetime
from typing import Optional, List, Annotated

from pydantic import BaseModel, Field, ConfigDict

from models.user.schemas import UserRead


class BaseComment(BaseModel):
    content: Annotated[
        str, Field(..., description="Comment content", min_length=1, max_length=256)
    ]


class CreateComment(BaseComment):
    owner_id: Annotated[int, Field(0, ge=0, description="Owner id")]
    mark_id: Annotated[int, Field(0, ge=0, description="Mark id")]
    parent_id: Annotated[Optional[int], Field(None, description="Parent comment id")]


class UpdateComment(BaseComment):
    owner_id: Annotated[int, Field(0, ge=0, description="Owner id")]
    mark_id: Annotated[int, Field(0, ge=0, description="Mark id")]

    model_config = ConfigDict(from_attributes=True)


class BaseCommentStat(BaseModel):
    likes_count: Annotated[int, Field(0, description="Likes count", ge=0)]
    dislikes_count: Annotated[int, Field(0, description="Dislikes count", ge=0)]
    total_replies: Annotated[int, Field(0, ge=0)]

    model_config = ConfigDict(from_attributes=True)


class BaseReadComment(BaseComment):
    id: Annotated[int, Field(0, ge=0, description="id")]
    owner: UserRead
    created_at: datetime
    stats: BaseCommentStat


class ReadCommentReply(BaseReadComment):
    pass


class ReadComment(BaseReadComment):
    replies: Annotated[
        Optional[List[ReadCommentReply]],
        Field(default_factory=list, description="Replies to comment"),
    ]


class CreateCommentRequest(BaseComment):
    parent_id: Annotated[
        Optional[int], Field(None, description="Parent comment id", ge=0)
    ]


class CreateCommentStat(BaseModel):
    comment_id: Annotated[int, Field(..., description="Comment id", ge=0)]


class ReadCommentStat(BaseCommentStat):
    pass


class UpdateCommentStat(CreateComment, BaseCommentStat):
    pass
