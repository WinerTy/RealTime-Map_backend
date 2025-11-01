from typing import Annotated

from pydantic import BaseModel, Field

from models.mark_comment.model import CommentReactionType


class BaseCommentReaction(BaseModel):
    reaction_type: CommentReactionType


class CreateCommentReaction(BaseCommentReaction):
    user_id: Annotated[int, Field(..., description="Owner id", ge=1)]
    comment_id: Annotated[int, Field(..., description="Comment id", ge=1)]


class UpdateCommentReaction(BaseCommentReaction):
    pass


class ReadCommentReaction(BaseModel):
    pass
