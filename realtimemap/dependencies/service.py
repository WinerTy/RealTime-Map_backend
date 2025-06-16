from typing import Annotated

from fastapi import Depends

from crud.category import CategoryRepository
from crud.mark import MarkRepository
from crud.mark_comment.repository import MarkCommentRepository
from dependencies.crud import (
    get_mark_repository,
    get_category_repository,
    get_mark_comment_repository,
)
from dependencies.session import get_session
from services.mark.service import MarkService


async def get_mark_service(
    mark_repo: Annotated["MarkRepository", Depends(get_mark_repository)],
    category_repo: Annotated["CategoryRepository", Depends(get_category_repository)],
    mark_comment_repo: Annotated[
        "MarkCommentRepository", Depends(get_mark_comment_repository)
    ],
    session: get_session,
):
    yield MarkService(
        session=session,
        mark_repo=mark_repo,
        category_repo=category_repo,
        mark_comment_repo=mark_comment_repo,
    )
