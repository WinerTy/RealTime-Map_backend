from abc import ABC, abstractmethod
from typing import List

from core.common.repository import BaseRepository
from modules.mark_comment.model import Comment
from modules.mark_comment.schemas import CreateComment, UpdateComment


class MarkCommentRepository(BaseRepository[Comment, CreateComment, UpdateComment], ABC):

    @abstractmethod
    async def get_comments(self, mark_id: int) -> List[Comment]:
        raise NotImplementedError

    @abstractmethod
    async def update_reaction(self):
        raise NotImplementedError

    @abstractmethod
    async def update_comment(self):
        raise NotImplementedError
