from typing import Annotated, TYPE_CHECKING

from fastapi import Depends, HTTPException

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
    record_id: int,
    repo: Annotated["MarkCommentRepository", Depends(get_mark_comment_repository)],
):
    is_exist = await repo.exist(record_id)
    if not is_exist:
        raise HTTPException(
            status_code=404, detail=f"Mark comment with id {record_id} not found."
        )
