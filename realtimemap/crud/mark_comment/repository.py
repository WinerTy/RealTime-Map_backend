from typing import TYPE_CHECKING

from sqlalchemy import select

from crud import BaseRepository
from models import MarkComment, User
from models.mark_comment.schemas import (
    CreateMarkComment,
    ReadMarkComment,
    UpdateMarkComment,
    CreateMarkCommentRequest,
)

if TYPE_CHECKING:
    from sqlalchemy.ext.asyncio import AsyncSession


class MarkCommentRepository(
    BaseRepository[MarkComment, CreateMarkComment, ReadMarkComment, UpdateMarkComment]
):
    def __init__(self, session: "AsyncSession"):
        super().__init__(session=session, model=MarkComment)

    async def create_comment(
        self, user: User, data: CreateMarkCommentRequest, mark_id: int
    ):
        create_data = CreateMarkComment(
            **data.model_dump(), user_id=user.id, mark_id=mark_id
        )
        result = await self.create(data=create_data)
        return result

    async def get_comment_for_mark(self, mark_id: int):
        stmt = (
            select(self.model)
            .where(self.model.mark_id == mark_id)
            .order_by(self.model.created_at.desc())
        ).join(self.model.user)
        return stmt

    async def update_reaction(self):
        pass

    async def update_comment(self):
        pass
