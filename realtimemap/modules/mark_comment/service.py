from typing import Optional, List, TYPE_CHECKING

from errors.http2 import NestingLevelExceededError, NotFoundError, ValidationError
from modules.user.model import User
from .model import Comment
from .schemas import (
    CreateComment,
    CreateCommentRequest,
    CommentReactionRequest,
    CreateCommentReaction,
)

if TYPE_CHECKING:
    from core.common.repository import (
        MarkCommentRepository,
        CommentStatRepository,
        CommentReactionRepository,
    )


class MarkCommentService:
    # Явно указывем слоты для экономии памяти
    __slots__ = (
        "comment_repo",
        "comment_stat_repo",
        "comment_reaction_repo",
    )

    def __init__(
        self,
        comment_repo: "MarkCommentRepository",
        comment_stat_repo: "CommentStatRepository",
        comment_reaction_repo: "CommentReactionRepository",
    ):
        self.comment_repo = comment_repo
        self.comment_stat_repo = comment_stat_repo
        self.comment_reaction_repo = comment_reaction_repo

    async def get_comment_by_id(self, comment_id: int) -> Comment:
        result = await self.comment_repo.get_by_id(comment_id)
        if not result:
            raise NotFoundError()
        return result

    async def after_create_comment(self, comment: Comment) -> None:
        pass

    async def create_comment(
        self, create_data: CreateCommentRequest, mark_id: int, user: User
    ):
        if create_data.parent_id:
            parent_comment = await self.comment_repo.get_by_id(create_data.parent_id)
            if not parent_comment:
                raise ValidationError(
                    field="parent_id",
                    user_input=create_data.parent_id,
                    input_type="number",
                )
            if parent_comment.parent_id:
                raise NestingLevelExceededError()
        full_data = CreateComment(
            **create_data.model_dump(), mark_id=mark_id, owner_id=user.id
        )
        result = await self.comment_repo.create(full_data)
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
            result = await self.comment_reaction_repo.create(create_data)
            return result

        if comment_reaction.reaction_type == data.reaction_type:
            result = await self.comment_reaction_repo.delete(comment_reaction.id)
            return result

        result = await self.comment_reaction_repo.update(comment_reaction.id, data)
        return result
