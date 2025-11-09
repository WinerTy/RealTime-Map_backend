import pytest
import pytest_asyncio
from sqlalchemy import text

from core.config import conf
from database.helper import db_helper
from models import BaseSqlModel


@pytest.fixture(scope="session")
def event_loop():
    """Создаем event loop для всей сессии тестов"""
    import asyncio

    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()


# Проверка готовности к тестированию
@pytest.fixture(scope="session", autouse=True)
def check_conf():
    assert conf.mode.lower() == "test"


# Проврека расширения для postgresql (Без него тесты не имеют значения)
@pytest.fixture(scope="session", autouse=True)
async def db_extension():
    async with db_helper.session_factory() as session:
        try:
            stmt = text(
                "SELECT EXISTS(SELECT 1 FROM pg_extension WHERE extname = 'postgis')"
            )
            result = await session.execute(stmt)
            postgis_extension = result.scalar_one()
            if not postgis_extension:
                pytest.fail("postgis extension not found")
        finally:
            await db_helper.dispose()


@pytest.fixture(scope="session", autouse=True)
def setup_db():
    BaseSqlModel.metadata.drop_all(bind=db_helper.sync_engine)
    BaseSqlModel.metadata.create_all(bind=db_helper.sync_engine)


@pytest_asyncio.fixture(scope="function")
async def db_session():
    async with db_helper.session_factory() as session:
        yield session
    await db_helper.dispose()
