from pydantic import BaseModel

from models.mark_comment.model import CommentReactionType


class CommentReactionRequest(BaseModel):
    reaction_type: CommentReactionType
