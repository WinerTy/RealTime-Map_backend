import logging
from typing import AsyncGenerator, TYPE_CHECKING, Generator

from .helper import db_helper

if TYPE_CHECKING:
    from sqlalchemy.ext.asyncio import AsyncSession
    from sqlalchemy.orm import Session

logger = logging.getLogger(__name__)


async def get_session() -> AsyncGenerator["AsyncSession", None]:
    async with db_helper.session_factory() as session:
        try:
            yield session
            await session.commit()
        except Exception:
            await session.rollback()
            raise


def get_sync_session() -> Generator["Session", None]:
    with db_helper.sync_session_factory() as session:
        try:
            yield session
            session.commit()
        except Exception as e:
            session.rollback()
            logger.error("Error while getting session", e)
            raise
