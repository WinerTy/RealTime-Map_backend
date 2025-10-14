from jinja2 import Environment, FileSystemLoader
from sqlalchemy import Select
from sqlalchemy.orm import joinedload, selectinload
from starlette.requests import Request

from core.admin.fields import JsonField
from core.config import conf
from models import SubscriptionPlan, UserSubscription
from .base import BaseModelAdmin

env = Environment(loader=FileSystemLoader(conf.template_dir))


class AdminSubscriptionPlan(BaseModelAdmin):
    fields = [
        SubscriptionPlan.id,
        SubscriptionPlan.name,
        SubscriptionPlan.price,
        SubscriptionPlan.plan_type,
        SubscriptionPlan.duration_days,
        JsonField("features"),
        SubscriptionPlan.is_active,
        SubscriptionPlan.created_at,
        SubscriptionPlan.updated_at,
    ]
    exclude_fields_from_list = [SubscriptionPlan.features]
    exclude_fields_from_create = [
        SubscriptionPlan.created_at,
        SubscriptionPlan.updated_at,
    ]
    detail_template = "view/subscription_plan_detail.html"

    def get_details_query(self, request: Request) -> Select:
        stmt = super().get_details_query(request)
        stmt = stmt.options(selectinload(SubscriptionPlan.user_subscriptions))
        return stmt


class AdminUserSubscription(BaseModelAdmin):
    fields = [
        UserSubscription.id,
        UserSubscription.user_id,
        UserSubscription.user,
        UserSubscription.plan,
        UserSubscription.payment_status,
        UserSubscription.payment_provider_id,
    ]

    exclude_fields_from_create = [
        UserSubscription.payment_provider_id,
        UserSubscription.payment_status,
    ]

    def get_list_query(self, request: Request) -> Select:
        stmt = super().get_list_query(request)
        stmt = stmt.options(
            joinedload(UserSubscription.user),
            joinedload(UserSubscription.plan),
        )
        return stmt

    # TODO Create payment
    async def after_create(self, request: Request, obj: UserSubscription) -> None:
        pass
