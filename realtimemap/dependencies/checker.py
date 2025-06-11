from typing import Annotated

from fastapi import Depends

from crud.mark import MarkRepository
from dependencies.crud import get_mark_repository


async def check_mark_exist(
    mark_id: int, repo: Annotated["MarkRepository", Depends(get_mark_repository)]
):
    await repo.get_mark_by_id(mark_id)
