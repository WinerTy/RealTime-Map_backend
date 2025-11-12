from starlette_admin import TextAreaField, IntegerField
from starlette_admin.contrib.sqla import ModelView

from modules import Level, ExpAction, UserExpHistory


class AdminLevel(ModelView):
    fields = [
        IntegerField("level", help_text="Level number"),
        Level.required_exp,
        TextAreaField("description", label="description"),
        Level.is_active,
    ]


# TODO Валидация на проверку является ли action_type словосочетанием
class AdminExpAction(ModelView):
    fields = [
        ExpAction.action_type,
        ExpAction.base_exp,
        ExpAction.name,
        TextAreaField("description", label="description"),
        ExpAction.is_active,
        ExpAction.is_repeatable,
        ExpAction.max_per_day,
    ]


class AdmiUserExpHistory(ModelView):
    fields = [
        UserExpHistory.user,
        UserExpHistory.action,
        UserExpHistory.source_id,
        UserExpHistory.base_exp,
        UserExpHistory.exp_before,
        UserExpHistory.total_exp,
        UserExpHistory.level_before,
        UserExpHistory.level_after,
    ]
