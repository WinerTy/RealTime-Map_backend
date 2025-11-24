"""
Фикстуры для тестирования репозиториев с адаптерами
"""

import pytest
from sqlalchemy.ext.asyncio import AsyncSession

from database.adapter import PgAdapter
from modules import (
    Category,
    Level,
    ExpAction,
    UserExpHistory,
    SubscriptionPlan,
)
from modules.category.schemas import CreateCategory, UpdateCategory
from modules.gamefication.schemas import CreateUserExpHistory, UpdateUserExpHistory


@pytest.fixture
def category_adapter(db_session: AsyncSession) -> PgAdapter[Category, CreateCategory, UpdateCategory]:
    """Адаптер для работы с категориями"""
    return PgAdapter(session=db_session, model=Category)


@pytest.fixture
def level_adapter(db_session: AsyncSession) -> PgAdapter[Level, None, None]:
    """Адаптер для работы с уровнями"""
    return PgAdapter(session=db_session, model=Level)


@pytest.fixture
def exp_action_adapter(db_session: AsyncSession) -> PgAdapter[ExpAction, None, None]:
    """Адаптер для работы с действиями опыта"""
    return PgAdapter(session=db_session, model=ExpAction)


@pytest.fixture
def user_exp_history_adapter(
    db_session: AsyncSession,
) -> PgAdapter[UserExpHistory, CreateUserExpHistory, UpdateUserExpHistory]:
    """Адаптер для работы с историей опыта пользователей"""
    return PgAdapter(session=db_session, model=UserExpHistory)


@pytest.fixture
def subscription_plan_adapter(db_session: AsyncSession) -> PgAdapter[SubscriptionPlan, None, None]:
    """Адаптер для работы с планами подписок"""
    return PgAdapter(session=db_session, model=SubscriptionPlan)
