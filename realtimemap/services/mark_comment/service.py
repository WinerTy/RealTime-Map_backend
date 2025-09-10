from typing import Optional, List

from sqlalchemy.ext.asyncio import AsyncSession

from crud.mark_comment import MarkCommentRepository
from crud.mark_comment.repository import (
    CommentStatRepository,
    CommentReactionRepository,
)
from exceptions import RecordNotFoundError, NestingLevelExceededError
from models import Comment, User
from models.mark_comment.schemas import (
    CreateComment,
    CreateCommentRequest,
    CommentReactionRequest,
    CreateCommentReaction,
)
from services.base import BaseService


class MarkCommentService(BaseService):
    def __init__(
        self,
        session: AsyncSession,
        comment_repo: MarkCommentRepository,
        comment_stat_repo: CommentStatRepository,
        comment_reaction_repo: CommentReactionRepository,
    ):
        super().__init__(session)
        self.comment_repo = comment_repo
        self.comment_stat_repo = comment_stat_repo
        self.comment_reaction_repo = comment_reaction_repo

    async def get_comment_by_id(self, comment_id: int) -> Comment:
        result = await self.comment_repo.get_by_id(comment_id)
        if not result:
            raise RecordNotFoundError()
        return result

    async def after_create_comment(self, comment: Comment) -> None:
        pass

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
        await self.after_create_comment(result)
        return result

    async def get_comments(self, mark_id: int) -> Optional[List[Comment]]:
        comments = await self.comment_repo.get_comments(mark_id=mark_id)
        return comments

    # TODO Optimization ORM use this on_conflict_do_update
    async def create_or_update_comment_reaction(
        self, comment_id: int, data: CommentReactionRequest, user: User
    ):
        comment_reaction = await self.comment_reaction_repo.get_comment_reaction(
            user.id, comment_id
        )
        if not comment_reaction:
            create_data = CreateCommentReaction(
                comment_id=comment_id, user_id=user.id, **data.model_dump()
            )
            result = await self.comment_reaction_repo.create_comment_reaction(
                create_data
            )
            return result

        if comment_reaction.reaction_type == data.reaction_type:
            result = await self.comment_reaction_repo.delete_comment_reaction(
                comment_reaction.id
            )
            return result

        result = await self.comment_reaction_repo.update_comment_reaction(
            comment_reaction.id, data
        )
        return result
