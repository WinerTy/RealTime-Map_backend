from abc import ABC, abstractmethod

from core.common.repository import BaseRepository
from modules.mark_comment.model import CommentStat
from modules.mark_comment.schemas import CreateCommentStat, UpdateCommentStat


class CommentStatRepository(
    BaseRepository[CommentStat, CreateCommentStat, UpdateCommentStat], ABC
):

    @abstractmethod
    async def create_base_stat(self, comment_id: int) -> None:
        raise NotImplementedError
