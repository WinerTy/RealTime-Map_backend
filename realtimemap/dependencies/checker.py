from typing import Annotated

from fastapi import Depends, HTTPException

from crud.mark import MarkRepository
from dependencies.crud import get_mark_repository


async def check_mark_exist(
    record_id: int, repo: Annotated["MarkRepository", Depends(get_mark_repository)]
):
    is_exist = await repo.exist(record_id)
    if not is_exist:
        raise HTTPException(
            status_code=404, detail=f"Mark with id {record_id} not found."
        )
