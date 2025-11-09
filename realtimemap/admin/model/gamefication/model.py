from starlette_admin import TextAreaField, IntegerField
from starlette_admin.contrib.sqla import ModelView

from models import Level, ExpAction


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
    pass
