from decimal import Decimal
from typing import Annotated, Dict, Any, Literal, Union

from pydantic import BaseModel, Field, ConfigDict, model_validator

from models.subscription.model import SubPlanType


class PremiumSubscriptionPlan(BaseModel):
    """
    Class for Premium Subscription Plan
    """

    plan_type: Annotated[
        Literal[SubPlanType.premium],
        Field(default=SubPlanType.premium, description="Premium subscription plan"),
    ]
    exp_multiplier: Annotated[float, Field(default=1.2, description="Exp multiplier")]


class PremiumPlusSubscriptionPlan(BaseModel):
    """
    Class for Premium+ Subscription Plan
    """

    plan_type: Annotated[
        Literal[SubPlanType.premium_plus],
        Field(
            default=SubPlanType.premium_plus, description="Premium subscription plan"
        ),
    ]
    exp_multiplier: Annotated[float, Field(default=1.35, description="Exp multiplier")]


class UltraSubscriptionPlan(BaseModel):
    """
    Class for Ultra Subscription Plan
    """

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
        if isinstance(data, dict):
            plan_type = data.get("plan_type")
            features = data.get("features")

            if plan_type and isinstance(features, dict) and "plan_type" not in features:
                features["plan_type"] = plan_type

        elif hasattr(data, "plan_type") and hasattr(data, "features"):
            plan_type = getattr(data, "plan_type")
            features = getattr(data, "features")

            if plan_type and isinstance(features, dict) and "plan_type" not in features:
                data.features = {**features, "plan_type": plan_type}

        return data


class UpdateSubscriptionPlan(BaseSubscriptionPlan):
    pass
