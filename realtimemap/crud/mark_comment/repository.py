from typing import TYPE_CHECKING

from sqlalchemy import select, Select
from sqlalchemy.orm import selectinload

from crud import BaseRepository
from models import User, Comment
from models.mark_comment.schemas import (
    CreateComment,
    UpdateComment,
    ReadComment,
)

if TYPE_CHECKING:
    from sqlalchemy.ext.asyncio import AsyncSession


class MarkCommentRepository(
    BaseRepository[Comment, CreateComment, ReadComment, UpdateComment]
):
    def __init__(self, session: "AsyncSession"):
        super().__init__(session=session, model=Comment)

    async def create_comment(self, data: CreateComment):
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

    def get_comment_for_mark(self, mark_id: int) -> Select:
        stmt = (
            select(self.model)
            .where(self.model.mark_id == mark_id, self.model.parent_id.is_(None))
            .options(*self._get_load_strategy())
        ).order_by(self.model.created_at.desc())
        return stmt

    async def get_comments(self, mark_id: int):
        stmt = self.get_comment_for_mark(mark_id=mark_id)
        result = await self.session.execute(stmt)
        comments = result.scalars().unique().all()
        return comments

    async def update_reaction(self):
        pass

    async def update_comment(self):
        pass
