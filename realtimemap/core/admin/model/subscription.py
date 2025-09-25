from models import SubscriptionPlan
from .base import BaseModelAdmin


class AdminSubscriptionPlan(BaseModelAdmin):
    fields = [
        SubscriptionPlan.id,
        SubscriptionPlan.name,
        SubscriptionPlan.price,
        SubscriptionPlan.plan_type,
        SubscriptionPlan.features,
        SubscriptionPlan.is_active,
    ]
