from decimal import Decimal

import pytest
from pydantic import ValidationError
from sqlalchemy.ext.asyncio import AsyncSession

from crud.subcription.repository import SubscriptionPlanRepository
from models.subscription.model import SubPlanType
from models.subscription.schemas import CreateSubscriptionPlan


class TestSubscriptionPlanRepository:

    @pytest.mark.asyncio
    @pytest.mark.parametrize(
        "plan_data, expected_error, match_error",
        [
            pytest.param(
                {
                    "name": "Test Plan premium",
                    "features": {"testing_limit": 30},
                    "duration_days": 30,
                    "price": 300,
                    "plan_type": SubPlanType.premium,
                },
                None,
                None,
                id="valid_data_premium",
            ),
            pytest.param(
                {
                    "name": "Test Plan Ultra",
                    "features": {"testing_limit": 30},
                    "duration_days": 30,
                    "price": 300,
                    "plan_type": SubPlanType.ultra,
                },
                None,
                None,
                id="valid_data_ultra",
            ),
            pytest.param(
                {
                    "features": {"testing_limit": 30},
                    "duration_days": 30,
                    "price": Decimal(300),
                    "plan_type": SubPlanType.ultra,
                },
                ValidationError,
                None,
                id="name_empty",
            ),
        ],
    )
    async def test_create_plan(
        self, db_session: AsyncSession, plan_data, expected_error, match_error
    ):
        repo = SubscriptionPlanRepository(db_session)
        if expected_error is None:
            plan_schema = CreateSubscriptionPlan(**plan_data)
            result = await repo.create_subscription_plan(plan_schema)

            assert result.id is not None
            assert result.name == plan_data["name"]
            assert result.plan_type == plan_data["plan_type"]
            assert result.duration_days == plan_data["duration_days"]
            assert result.price == plan_data["price"]
            assert type(result.features) is dict

        else:
            with pytest.raises(expected_error, match=match_error):
                plan_schema = CreateSubscriptionPlan(**plan_data)
                await repo.create_subscription_plan(plan_schema)
