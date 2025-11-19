from datetime import datetime
from typing import Annotated, Optional, List

from pydantic import Field, BaseModel, ConfigDict

from modules.mark_comment.schemas.comment_stat.crud import BaseCommentStat
from modules.user.schemas import UserRead


class BaseComment(BaseModel):
    content: Annotated[
        str, Field(..., description="Comment content", min_length=1, max_length=256)
    ]


class BaseReadComment(BaseComment):
    id: Annotated[int, Field(0, ge=0, description="id")]
    owner: UserRead
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)


class CreateComment(BaseComment):
    owner_id: Annotated[int, Field(0, ge=0, description="Owner id")]
    mark_id: Annotated[int, Field(0, ge=0, description="Mark id")]
    parent_id: Annotated[Optional[int], Field(None, description="Parent comment id")]


class UpdateComment(BaseComment):
    owner_id: Annotated[int, Field(0, ge=0, description="Owner id")]
    mark_id: Annotated[int, Field(0, ge=0, description="Mark id")]

    model_config = ConfigDict(from_attributes=True)


class ReadCommentReply(BaseReadComment):
    stats: BaseCommentStat


class ReadComment(BaseReadComment):
    replies: Annotated[
        Optional[List[ReadCommentReply]],
        Field(default_factory=list, description="Replies to comment"),
    ]
    stats: BaseCommentStat
