from typing import TYPE_CHECKING, List, Optional

from sqlalchemy import select, Select
from sqlalchemy.orm import selectinload

from core.common import BaseRepository
from .model import Comment, CommentStat, CommentReaction
from .schemas import (
    CreateComment,
    UpdateComment,
    CreateCommentStat,
    UpdateCommentStat,
    CreateCommentReaction,
    UpdateCommentReaction,
)

if TYPE_CHECKING:
    from sqlalchemy.ext.asyncio import AsyncSession


class MarkCommentRepository(BaseRepository[Comment, CreateComment, UpdateComment]):
    def __init__(self, session: "AsyncSession"):
        super().__init__(session=session, model=Comment)

    async def create_comment(self, data: CreateComment) -> Comment:
        result = await self.create(data=data)
        return result

    def _get_load_strategy(self):
        loads = [
            # load replies with joined data
            selectinload(self.model.replies).options(
                selectinload(Comment.stats),
                selectinload(Comment.owner),
            ),
            # load for main comment
            selectinload(self.model.owner),
            selectinload(self.model.stats),
        ]
        return loads

    def _get_comment_for_mark(self, mark_id: int) -> Select:
        stmt = (
            select(self.model)
            .where(self.model.mark_id == mark_id, self.model.parent_id.is_(None))
            .options(*self._get_load_strategy())
        ).order_by(self.model.created_at.desc())
        return stmt

    async def get_comments(self, mark_id: int) -> List[Comment]:
        stmt = self._get_comment_for_mark(mark_id=mark_id)
        result = await self.session.execute(stmt)
        comments = result.scalars().unique().all()
        return comments

    async def update_reaction(self):
        pass

    async def update_comment(self):
        pass


class CommentStatRepository(
    BaseRepository[CommentStat, CreateCommentStat, UpdateCommentStat]
):
    def __init__(self, session: "AsyncSession"):
        super().__init__(session=session, model=CommentStat)

    async def create_base_stat(self, comment_id: int) -> None:
        data = CreateCommentStat(comment_id=comment_id)
        await self.create(data=data)


class CommentReactionRepository(
    BaseRepository[
        CommentReaction,
        CreateCommentReaction,
        UpdateCommentReaction,
    ]
):
    def __init__(self, session: "AsyncSession"):
        super().__init__(session=session, model=CommentReaction)

    async def create_comment_reaction(
        self, data: CreateCommentReaction
    ) -> CommentReaction:
        result = await self.create(data=data)
        return result

    async def get_comment_reaction(
        self, user_id: int, comment_id: int
    ) -> Optional[CommentReaction]:
        stmt = select(self.model).where(
            self.model.user_id == user_id, self.model.comment_id == comment_id
        )
        result = await self.session.execute(stmt)
        comment = result.scalar_one_or_none()
        return comment

    async def update_comment_reaction(
        self, comment_reaction_id: int, data: UpdateCommentReaction
    ):
        result = await self.update(comment_reaction_id, data)
        return result

    async def delete_comment_reaction(self, comment_reaction_id: int):
        result = await self.delete(comment_reaction_id)
        return result
