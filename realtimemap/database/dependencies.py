from typing import AsyncGenerator, TYPE_CHECKING

from .helper import db_helper

if TYPE_CHECKING:
    from sqlalchemy.ext.asyncio import AsyncSession


async def get_session() -> AsyncGenerator["AsyncSession", None]:
    async with db_helper.session_factory() as session:
        try:
            yield session
            await session.commit()
        except Exception:
            await session.rollback()
            raise
