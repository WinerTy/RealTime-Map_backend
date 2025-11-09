import asyncio
from typing import AsyncGenerator

import pytest
import pytest_asyncio
from httpx import ASGITransport, AsyncClient
from sqlalchemy import text, NullPool
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine

from core.config import conf
from database.helper import db_helper
from dependencies.crud import get_session
from main import app
from models import BaseSqlModel


@pytest.fixture(scope="session")
def event_loop_policy():
    return asyncio.get_event_loop_policy()


@pytest.fixture(scope="function")
def event_loop(event_loop_policy):
    loop = event_loop_policy.new_event_loop()
    yield loop
    loop.close()


@pytest_asyncio.fixture(scope="session")
async def test_engine():
    engine = create_async_engine(
        str(conf.db.url),
        poolclass=NullPool,  # Важно для тестов!
        echo=False,
    )
    yield engine
    await engine.dispose()


@pytest_asyncio.fixture(scope="session")
async def test_session_factory(test_engine):
    return async_sessionmaker(
        bind=test_engine,
        class_=AsyncSession,
        expire_on_commit=False,
        autoflush=False,
        autocommit=False,
    )


@pytest_asyncio.fixture(scope="function")
async def db_session(test_session_factory):
    async with test_session_factory() as session:
        async with session.begin():
            yield session
            await session.rollback()


@pytest_asyncio.fixture(scope="function")
async def override_get_session(test_session_factory):
    async def _get_test_session() -> AsyncGenerator[AsyncSession, None]:
        async with test_session_factory() as session:
            async with session.begin():
                yield session
                await session.rollback()

    return _get_test_session


# Проверка готовности к тестированию
@pytest.fixture(scope="session", autouse=True)
def check_conf():
    """
    Проверка готовнисти тестирования
    :return:
    """
    assert conf.mode.lower() == "test"


# Проврека расширения для postgresql (Без него тесты не имеют значения)
@pytest.fixture(scope="session", autouse=True)
async def db_extension():
    """
    Проверка установленного расширения
    :return:
    """
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
    """
    Подготовка БД
    :return:
    """
    BaseSqlModel.metadata.drop_all(bind=db_helper.sync_engine)
    BaseSqlModel.metadata.create_all(bind=db_helper.sync_engine)


@pytest_asyncio.fixture(scope="function")
async def client():
    """HTTP клиент для тестирования endpoints"""

    app.dependency_overrides[get_session] = override_get_session
    # app.dependency_overrides[db_helper.session_getter] = override_get_session

    transport = ASGITransport(app=app)

    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        yield ac
