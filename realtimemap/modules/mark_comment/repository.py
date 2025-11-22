from typing import TYPE_CHECKING, List, Optional

from sqlalchemy import select, Select
from sqlalchemy.orm import selectinload

from core.common.repository import (
    MarkCommentRepository,
    CommentStatRepository,
    CommentReactionRepository,
)
from database.adapter import PgAdapter
from .model import Comment, CommentStat, CommentReaction
from .schemas import (
    CreateComment,
    CreateCommentStat,
    UpdateComment,
    UpdateCommentStat,
    CreateCommentReaction,
    UpdateCommentReaction,
)

if TYPE_CHECKING:
    pass


class PgMarkCommentRepository(MarkCommentRepository):

    def __init__(self, adapter: PgAdapter[Comment, CreateComment, UpdateComment]):
        super().__init__(adapter)
        self.adapter = adapter

    async def create_comment(self, data: CreateComment) -> Comment:
        result = await self.create(data=data)
        return result

    @staticmethod
    def _get_load_strategy():
        loads = [
            # load replies with joined data
            selectinload(Comment.replies).options(
                selectinload(Comment.stats),
                selectinload(Comment.owner),
            ),
            # load for main comment
            selectinload(Comment.owner),
            selectinload(Comment.stats),
        ]
        return loads

    def _get_comment_for_mark(self, mark_id: int) -> Select:
        stmt = (
            select(Comment)
            .where(Comment.mark_id == mark_id, Comment.parent_id.is_(None))
            .options(*self._get_load_strategy())
        ).order_by(Comment.created_at.desc())
        return stmt

    async def get_comments(self, mark_id: int) -> List[Comment]:
        stmt = self._get_comment_for_mark(mark_id=mark_id)
        comments = await self.adapter.execute_query(stmt, True)
        return comments

    async def update_reaction(self):
        pass

    async def update_comment(self):
        pass


class PgCommentStatRepository(CommentStatRepository):
    def __init__(
        self, adapter: PgAdapter[CommentStat, CreateCommentStat, UpdateCommentStat]
    ):
        super().__init__(adapter)
        self.adapter = adapter

    async def create_base_stat(self, comment_id: int) -> None:
        data = CreateCommentStat(comment_id=comment_id)
        await self.create(data=data)


class PgCommentReactionRepository(CommentReactionRepository):
    def __init__(
        self,
        adapter: PgAdapter[
            CommentReaction, CreateCommentReaction, UpdateCommentReaction
        ],
    ):
        super().__init__(adapter)
        self.adapter = adapter

    async def get_comment_reaction(
        self, user_id: int, comment_id: int
    ) -> Optional[CommentReaction]:
        stmt = select(CommentReaction).where(
            CommentReaction.user_id == user_id, CommentReaction.comment_id == comment_id
        )
        comment = await self.adapter.execute_query_one(stmt)
        return comment
