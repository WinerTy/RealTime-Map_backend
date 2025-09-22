from decimal import Decimal
from typing import Annotated, Dict, Any, Literal, Union

from pydantic import BaseModel, Field, ConfigDict, model_validator

from .model import SubPlanType


class PremiumSubscriptionPlan(BaseModel):
    plan_type: Annotated[
        Literal[SubPlanType.premium],
        Field(default=SubPlanType.premium, description="Premium subscription plan"),
    ]
    exp_multiplier: Annotated[float, Field(default=1.2, description="Exp multiplier")]


class PremiumPlusSubscriptionPlan(BaseModel):
    plan_type: Annotated[
        Literal[SubPlanType.premium_plus],
        Field(
            default=SubPlanType.premium_plus, description="Premium subscription plan"
        ),
    ]
    exp_multiplier: Annotated[float, Field(default=1.35, description="Exp multiplier")]


class UltraSubscriptionPlan(BaseModel):
    plan_type: Annotated[
        Literal[SubPlanType.ultra],
        Field(default=SubPlanType.ultra, description="Premium subscription plan"),
    ]
    exp_multiplier: Annotated[float, Field(default=1.5, description="Exp multiplier")]
    developers_respect: Annotated[
        bool, Field(default=True, description="Developers respect")
    ]  # TODO убрать из итоговой сборки :)


PlanFeatures = Union[
    PremiumSubscriptionPlan, PremiumPlusSubscriptionPlan, UltraSubscriptionPlan
]


class BaseSubscriptionPlan(BaseModel):
    name: Annotated[
        str, Field(..., max_length=128, description="Name of the subscription plan")
    ]
    price: Annotated[
        Decimal,
        Field(..., decimal_places=10, description="Price of the subscription plan"),
    ]


# SCHEMФ FOR CREATE. update this for same validate
class CreateSubscriptionPlan(BaseSubscriptionPlan):
    features: Annotated[
        Dict[str, Any], Field(default_factory=dict, description="Features dict")
    ]


class ReadSubscriptionPlan(BaseSubscriptionPlan):
    id: Annotated[int, Field(..., description="ID of the subscription plan")]
    plan_type: SubPlanType
    features: Annotated[
        PlanFeatures, Field(..., discriminator="plan_type", description="Features json")
    ]

    model_config = ConfigDict(from_attributes=True)

    @model_validator(mode="before")
    def _inject_plan_type_into_features(cls, data: Any) -> Any:
        """
        Этот валидатор "внедряет" plan_type из корневого объекта
        внутрь словаря features перед его валидацией.
        Это позволяет дискриминатору Union найти нужный тег.
        """
        # Проверяем, что работаем со словарем (или объектом с атрибутами)
        if isinstance(data, dict):
            plan_type = data.get("plan_type")
            features = data.get("features")

            # Если features - это словарь и в нем нет plan_type, добавляем его
            if plan_type and isinstance(features, dict) and "plan_type" not in features:
                features["plan_type"] = plan_type

        # Если data - это ORM-объект (при from_attributes=True)
        elif hasattr(data, "plan_type") and hasattr(data, "features"):
            plan_type = getattr(data, "plan_type")
            features = getattr(data, "features")

            if plan_type and isinstance(features, dict) and "plan_type" not in features:
                # Важно! Не изменяем исходный ORM-объект.
                # Создаем копию словаря и работаем с ней.
                # Pydantic v2 достаточно умен, чтобы обработать это правильно.
                data.features = {**features, "plan_type": plan_type}

        return data


class UpdateSubscriptionPlan(BaseSubscriptionPlan):
    pass
