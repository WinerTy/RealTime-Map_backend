from crud.category.repository import CategoryRepository
from crud.mark import MarkRepository
from dependencies.session import get_session


async def get_mark_repository(session: get_session) -> MarkRepository:
    yield MarkRepository(session=session)


async def get_category_repository(session: get_session) -> CategoryRepository:
    yield CategoryRepository(session=session)
