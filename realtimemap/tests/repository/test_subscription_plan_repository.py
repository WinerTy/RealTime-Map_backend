from decimal import Decimal

import pytest
from sqlalchemy.ext.asyncio import AsyncSession

from modules.subscription.model import SubscriptionPlan, SubPlanType
from modules.subscription.repository import SubscriptionPlanRepository
from modules.subscription.schemas import CreateSubscriptionPlan, UpdateSubscriptionPlan
from .fixtures import test_subscription_plan, test_subscription_plans


class TestSubscriptionPlanRepository:
    """Тесты для SubscriptionPlanRepository"""

    @pytest.mark.asyncio
    async def test_create_subscription_plan(self, db_session: AsyncSession):
        """Тест создания плана подписки"""
        repo = SubscriptionPlanRepository(session=db_session)

        plan_data = CreateSubscriptionPlan(
            name="Test Plan",
            price=Decimal("15.99"),
            duration_days=30,
            plan_type=SubPlanType.premium,
            features={"exp_multiplier": 1.2},
        )

        created_plan = await repo.create(plan_data)

        assert created_plan.id is not None
        assert created_plan.name == "Test Plan"
        assert created_plan.price == Decimal("15.99")
        assert created_plan.duration_days == 30
        assert created_plan.plan_type == SubPlanType.premium
        assert created_plan.is_active is True

    @pytest.mark.asyncio
    async def test_get_by_id(self, db_session: AsyncSession, test_subscription_plan):
        """Тест получения плана подписки по ID"""
        repo = SubscriptionPlanRepository(session=db_session)

        plan = await repo.get_by_id(test_subscription_plan.id)

        assert plan is not None
        assert plan.id == test_subscription_plan.id
        assert plan.name == test_subscription_plan.name

    @pytest.mark.asyncio
    async def test_get_by_id_not_found(self, db_session: AsyncSession):
        """Тест получения несуществующего плана подписки"""
        repo = SubscriptionPlanRepository(session=db_session)

        plan = await repo.get_by_id(99999)

        assert plan is None

    @pytest.mark.asyncio
    async def test_get_subscription_plans_with_inactive(
        self, db_session: AsyncSession, test_subscription_plans
    ):
        """Тест получения планов подписки (активные и неактивные)"""
        repo = SubscriptionPlanRepository(session=db_session)

        # Получаем только активные
        active_plans = await repo.get_subscription_plans()
        assert len(active_plans) == 3

    @pytest.mark.asyncio
    async def test_get_subscription_plans_active_only(
        self, db_session: AsyncSession, test_subscription_plans
    ):
        """Тест получения только активных планов подписки"""
        repo = SubscriptionPlanRepository(session=db_session)

        active_plans = await repo.get_subscription_plans()

        assert len(active_plans) == 3
        assert all(plan.is_active for plan in active_plans)
        assert all(isinstance(plan, SubscriptionPlan) for plan in active_plans)

    @pytest.mark.asyncio
    async def test_update_subscription_plan(
        self, db_session: AsyncSession, test_subscription_plan
    ):
        """Тест обновления плана подписки"""
        repo = SubscriptionPlanRepository(session=db_session)

        update_data = UpdateSubscriptionPlan(
            name="Updated Plan",
            price=Decimal("25.99"),
        )

        updated_plan = await repo.update(test_subscription_plan.id, update_data)

        assert updated_plan is not None
        assert updated_plan.name == "Updated Plan"
        assert updated_plan.price == Decimal("25.99")
        assert updated_plan.id == test_subscription_plan.id

    @pytest.mark.asyncio
    async def test_delete_subscription_plan(
        self, db_session: AsyncSession, test_subscription_plan
    ):
        """Тест удаления плана подписки"""
        repo = SubscriptionPlanRepository(session=db_session)

        result = await repo.delete(test_subscription_plan.id)

        assert result is not None
        assert result.id == test_subscription_plan.id

        deleted_plan = await repo.get_by_id(test_subscription_plan.id)
        assert deleted_plan is None

    @pytest.mark.asyncio
    async def test_delete_non_existent_plan(self, db_session: AsyncSession):
        """Тест удаления несуществующего плана"""
        repo = SubscriptionPlanRepository(session=db_session)

        result = await repo.delete(99999)

        assert result is None

    @pytest.mark.asyncio
    async def test_get_subscription_plans_empty(self, db_session: AsyncSession):
        """Тест получения активных планов когда их нет"""
        repo = SubscriptionPlanRepository(session=db_session)

        plans = await repo.get_subscription_plans()

        assert len(plans) == 0

    @pytest.mark.asyncio
    async def test_create_plan_with_different_types(self, db_session: AsyncSession):
        """Тест создания планов с разными типами"""
        repo = SubscriptionPlanRepository(session=db_session)

        # Premium
        premium_plan = await repo.create(
            CreateSubscriptionPlan(
                name="Premium",
                price=Decimal("9.99"),
                duration_days=30,
                plan_type=SubPlanType.premium,
                features={"exp_multiplier": 1.2},
            )
        )

        # Premium Plus
        premium_plus_plan = await repo.create(
            CreateSubscriptionPlan(
                name="Premium Plus",
                price=Decimal("19.99"),
                duration_days=30,
                plan_type=SubPlanType.premium_plus,
                features={"exp_multiplier": 1.35},
            )
        )

        # Ultra
        ultra_plan = await repo.create(
            CreateSubscriptionPlan(
                name="Ultra",
                price=Decimal("29.99"),
                duration_days=30,
                plan_type=SubPlanType.ultra,
                features={"exp_multiplier": 1.5, "developers_respect": True},
            )
        )

        assert premium_plan.plan_type == SubPlanType.premium
        assert premium_plus_plan.plan_type == SubPlanType.premium_plus
        assert ultra_plan.plan_type == SubPlanType.ultra

        # Проверяем что все три плана созданы и активны
        active_plans = await repo.get_subscription_plans()
        assert len(active_plans) == 3
