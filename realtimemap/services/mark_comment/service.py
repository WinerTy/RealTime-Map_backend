from sqlalchemy.ext.asyncio import AsyncSession

from crud.mark_comment import MarkCommentRepository
from exceptions import RecordNotFoundError, NestingLevelExceededError
from models import Comment, User
from models.mark_comment.schemas import (
    CreateComment,
    CreateCommentRequest,
)
from services.base import BaseService


class MarkCommentService(BaseService):
    def __init__(self, session: AsyncSession, comment_repo: MarkCommentRepository):
        super().__init__(session)
        self.comment_repo = comment_repo

    async def get_comment_by_id(self, comment_id: int) -> Comment:
        result = await self.comment_repo.get_by_id(comment_id)
        if not result:
            raise RecordNotFoundError()
        return result

    async def create_comment(
        self, create_data: CreateCommentRequest, mark_id: int, user: User
    ):
        # TODO need check
        if create_data.parent_id:
            parent_comment = await self.comment_repo.get_by_id(create_data.parent_id)
            if not parent_comment:
                raise RecordNotFoundError()
            if parent_comment.parent_id:
                raise NestingLevelExceededError()
        full_data = CreateComment(
            **create_data.model_dump(), mark_id=mark_id, owner_id=user.id
        )
        result = await self.comment_repo.create_comment(full_data)
        return result
