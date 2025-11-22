from abc import ABC, abstractmethod
from typing import Optional

from core.common.repository import BaseRepository
from modules.mark_comment.model import CommentReaction
from modules.mark_comment.schemas import CreateCommentReaction, UpdateCommentReaction


class CommentReactionRepository(
    BaseRepository[CommentReaction, CreateCommentReaction, UpdateCommentReaction], ABC
):

    @abstractmethod
    async def get_comment_reaction(
        self, user_id: int, comment_id: int
    ) -> Optional[CommentReaction]:
        raise NotImplementedError
