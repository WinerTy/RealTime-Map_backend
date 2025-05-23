from crud.mark import MarkRepository
from dependencies.session import get_session


async def get_mark_repository(session: get_session) -> MarkRepository:
    yield MarkRepository(session)
