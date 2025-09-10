from typing import Annotated

from pydantic import BaseModel, Field, ConfigDict


class BaseCommentStat(BaseModel):
    likes_count: Annotated[int, Field(0, description="Likes count", ge=0)]
    dislikes_count: Annotated[int, Field(0, description="Dislikes count", ge=0)]
    total_replies: Annotated[int, Field(0, ge=0)]

    model_config = ConfigDict(from_attributes=True)


class CreateCommentStat(BaseModel):
    comment_id: Annotated[int, Field(..., description="Comment id", ge=1)]


class ReadCommentStat(BaseCommentStat):
    pass


class UpdateCommentStat(BaseCommentStat):
    pass
