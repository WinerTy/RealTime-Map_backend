from typing import TYPE_CHECKING

from sqlalchemy import select

from crud import BaseRepository
from models import User, Comment
from models.mark_comment.schemas import (
    CreateComment,
    UpdateComment,
    DeleteComment,
)

if TYPE_CHECKING:
    from sqlalchemy.ext.asyncio import AsyncSession


class MarkCommentRepository(
    BaseRepository[Comment, CreateComment, UpdateComment, DeleteComment]
):
    def __init__(self, session: "AsyncSession"):
        super().__init__(session=session, model=Comment)

    async def create_comment(self, data: CreateComment):
        result = await self.create(data=data)
        return result

    async def get_comment_for_mark(self, mark_id: int):
        stmt = (
            select(self.model)
            .where(self.model.mark_id == mark_id)
            .order_by(self.model.created_at.desc())
        )
        return stmt

    async def update_reaction(self):
        pass

    async def update_comment(self):
        pass
