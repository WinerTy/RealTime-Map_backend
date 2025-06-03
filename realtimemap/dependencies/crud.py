from crud.category.repository import CategoryRepository
from crud.mark import MarkRepository
from crud.request_log.repository import RequestLogRepository
from dependencies.session import get_session


async def get_mark_repository(session: get_session) -> MarkRepository:
    yield MarkRepository(session=session)


async def get_category_repository(session: get_session) -> CategoryRepository:
    yield CategoryRepository(session=session)


async def get_request_log_repository(session: get_session) -> RequestLogRepository:
    yield RequestLogRepository(session=session)
