from decimal import Decimal

import pytest_asyncio
from sqlalchemy.ext.asyncio import AsyncSession

from modules.gamefication.model import Level, ExpAction
from modules.subscription.model import SubscriptionPlan, SubPlanType
from modules.user.model import User


@pytest_asyncio.fixture
async def test_user(db_session: AsyncSession) -> User:
    """Создает тестового пользователя"""
    user = User(
        email="test@example.com",
        username="testuser",
        hashed_password="hashed_password",
        is_active=True,
        is_superuser=False,
        is_verified=False,
        level=1,
        current_exp=0,
        total_exp=0,
    )
    db_session.add(user)
    await db_session.flush()
    await db_session.refresh(user)
    return user


@pytest_asyncio.fixture
async def test_subscription_plan(db_session: AsyncSession) -> SubscriptionPlan:
    """Создает тестовый план подписки"""
    plan = SubscriptionPlan(
        name="Premium Plan",
        price=Decimal("9.99"),
        duration_days=30,
        plan_type=SubPlanType.premium,
        features={"exp_multiplier": 1.2},
        is_active=True,
    )
    db_session.add(plan)
    await db_session.flush()
    await db_session.refresh(plan)
    return plan


@pytest_asyncio.fixture
async def test_subscription_plans(db_session: AsyncSession) -> list[SubscriptionPlan]:
    """Создает несколько тестовых планов подписки"""
    plans = [
        SubscriptionPlan(
            name="Premium Plan",
            price=Decimal("9.99"),
            duration_days=30,
            plan_type=SubPlanType.premium,
            features={"exp_multiplier": 1.2},
            is_active=True,
        ),
        SubscriptionPlan(
            name="Premium Plus Plan",
            price=Decimal("19.99"),
            duration_days=30,
            plan_type=SubPlanType.premium_plus,
            features={"exp_multiplier": 1.35},
            is_active=True,
        ),
        SubscriptionPlan(
            name="Ultra Plan",
            price=Decimal("29.99"),
            duration_days=30,
            plan_type=SubPlanType.ultra,
            features={"exp_multiplier": 1.5, "developers_respect": True},
            is_active=True,
        ),
        SubscriptionPlan(
            name="Inactive Plan",
            price=Decimal("5.99"),
            duration_days=30,
            plan_type=SubPlanType.premium,
            features={"exp_multiplier": 1.1},
            is_active=False,
        ),
    ]
    for plan in plans:
        db_session.add(plan)
    await db_session.flush()
    for plan in plans:
        await db_session.refresh(plan)
    return plans


@pytest_asyncio.fixture
async def test_level(db_session: AsyncSession) -> Level:
    """Создает тестовый уровень"""
    level = Level(
        level=1,
        required_exp=100,
        description="First level",
        is_active=True,
    )
    db_session.add(level)
    await db_session.flush()
    await db_session.refresh(level)
    return level


@pytest_asyncio.fixture
async def test_levels(db_session: AsyncSession) -> list[Level]:
    """Создает несколько тестовых уровней"""
    levels = [
        Level(level=1, required_exp=0, description="Level 1", is_active=True),
        Level(level=2, required_exp=100, description="Level 2", is_active=True),
        Level(level=3, required_exp=250, description="Level 3", is_active=True),
        Level(level=4, required_exp=500, description="Level 4", is_active=True),
        Level(level=5, required_exp=1000, description="Level 5", is_active=True),
        Level(level=6, required_exp=2000, description="Level 6", is_active=False),
    ]
    for level in levels:
        db_session.add(level)
    await db_session.flush()
    for level in levels:
        await db_session.refresh(level)
    return levels


@pytest_asyncio.fixture
async def test_exp_action(db_session: AsyncSession) -> ExpAction:
    """Создает тестовое действие для опыта"""
    action = ExpAction(
        action_type="create_mark",
        base_exp=10,
        name="Create Mark",
        description="Experience for creating a mark",
        is_active=True,
        is_repeatable=True,
        max_per_day=10,
    )
    db_session.add(action)
    await db_session.flush()
    await db_session.refresh(action)
    return action


@pytest_asyncio.fixture
async def test_exp_actions(db_session: AsyncSession) -> list[ExpAction]:
    """Создает несколько тестовых действий для опыта"""
    actions = [
        ExpAction(
            action_type="create_mark",
            base_exp=10,
            name="Create Mark",
            description="Experience for creating a mark",
            is_active=True,
            is_repeatable=True,
            max_per_day=10,
        ),
        ExpAction(
            action_type="create_comment",
            base_exp=5,
            name="Create Comment",
            description="Experience for creating a comment",
            is_active=True,
            is_repeatable=True,
            max_per_day=20,
        ),
        ExpAction(
            action_type="verify_email",
            base_exp=50,
            name="Verify Email",
            description="Experience for verifying email",
            is_active=True,
            is_repeatable=False,
            max_per_day=1,
        ),
        ExpAction(
            action_type="inactive_action",
            base_exp=100,
            name="Inactive Action",
            description="This action is inactive",
            is_active=False,
            is_repeatable=False,
            max_per_day=1,
        ),
    ]
    for action in actions:
        db_session.add(action)
    await db_session.flush()
    for action in actions:
        await db_session.refresh(action)
    return actions
