from typing import Annotated

from fastapi import Depends

from crud.category import CategoryRepository
from crud.mark import MarkRepository
from dependencies.crud import get_mark_repository, get_category_repository
from dependencies.session import get_session
from services.mark.service import MarkService


async def get_mark_service(
    mark_repo: Annotated["MarkRepository", Depends(get_mark_repository)],
    category_repo: Annotated["CategoryRepository", Depends(get_category_repository)],
    session: get_session,
):
    yield MarkService(session=session, mark_repo=mark_repo, category_repo=category_repo)
