from typing import Annotated, TYPE_CHECKING

from fastapi import Depends

from dependencies.crud import get_mark_repository, get_mark_comment_repository
from exceptions import RecordNotFoundError

if TYPE_CHECKING:
    from crud.mark import MarkRepository
    from crud.mark_comment import MarkCommentRepository


async def check_mark_exist(
    mark_id: int, repo: Annotated["MarkRepository", Depends(get_mark_repository)]
):
    is_exist = await repo.exist(mark_id)
    if not is_exist:
        raise RecordNotFoundError()


async def check_mark_comment_exist(
    comment_id: int,
    repo: Annotated["MarkCommentRepository", Depends(get_mark_comment_repository)],
):
    is_exist = await repo.exist(comment_id)
    if not is_exist:
        raise RecordNotFoundError()
