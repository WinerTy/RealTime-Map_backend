import asyncio

import pytest
from sqlalchemy import select, literal_column


async def debug_func(x, y):
    await asyncio.sleep(1)
    return x + y


# TODO временный тест по готовности убрать
@pytest.mark.asyncio
@pytest.mark.parametrize("x, y, res", [(1, 2, 3), (5, 5, 10), (10, 0, 10)])
async def test_func(x, y, res):
    result = await debug_func(x, y)
    assert result == res


# TODO временный тест по готовности убрать
@pytest.mark.asyncio
@pytest.mark.parametrize("x", [1, 2, 3, 4])
async def test_db_session(x, db_session):
    base = "hello world"
    db_string = f"{base} {x}"
    stmt = select(literal_column(f"'{db_string}'"))
    result = await db_session.execute(stmt)
    result = result.scalars().all()
    assert result == [db_string]
