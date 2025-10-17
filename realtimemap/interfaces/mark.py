from typing import Protocol, TYPE_CHECKING, List, Optional, Tuple, Sequence

from interfaces import IBaseRepository
from models import Mark, Comment, CommentReaction, CommentStat
from models.mark.schemas import (
    CreateMark,
    UpdateMark,
    MarkFilter,
    MarkRequestParams,
)
from models.mark_comment.schemas import (
    UpdateComment,
    CreateComment,
    CreateCommentReaction,
    UpdateCommentReaction,
    UpdateCommentStat,
    CreateCommentStat,
)

if TYPE_CHECKING:
    pass


class IMarkRepository(IBaseRepository[Mark, CreateMark, UpdateMark], Protocol):

    async def get_marks(self, filters: MarkFilter) -> List[Mark]: ...

    async def create_mark(self, mark: CreateMark) -> Mark: ...

    async def get_mark_by_id(self, mark_id: int) -> Optional[Mark]: ...

    async def check_distance(
        self, current_location: MarkRequestParams, mark: Mark, radius: int = 500
    ) -> bool: ...

    async def update_mark(self, mark_id: int, update_data: UpdateMark) -> Mark: ...

    async def delete_mark(self, mark_id: int) -> Mark: ...

    async def get_ids_for_test(self) -> Tuple[Sequence[int], Sequence[int]]: ...


class IMarkCommentRepository(
    IBaseRepository[Comment, CreateComment, UpdateComment], Protocol
):

    async def create_comment(self, data: CreateComment) -> Comment: ...

    async def get_comments(self, mark_id: int) -> List[Comment]: ...


class ICommentStatRepository(
    IBaseRepository[CommentStat, CreateCommentStat, UpdateCommentStat],
    Protocol,
):
    async def create_base_stat(self, comment_id: int) -> None: ...


class ICommentReactionRepository(
    IBaseRepository[CommentReaction, CreateCommentReaction, UpdateCommentReaction],
    Protocol,
):
    async def create_comment_reaction(
        self, data: CreateCommentReaction
    ) -> CommentReaction: ...

    async def get_comment_reaction(
        self, user_id: int, comment_id: int
    ) -> Optional[CommentReaction]: ...

    async def update_comment_reaction(
        self, comment_reaction_id: int, data: UpdateCommentReaction
    ) -> CommentReaction: ...

    async def delete_comment_reaction(
        self, comment_reaction_id: int
    ) -> CommentReaction: ...
