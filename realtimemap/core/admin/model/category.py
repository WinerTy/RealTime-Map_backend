from starlette_admin import ColorField
from starlette_admin.contrib.sqla import ModelView

from models import Category


class AdminCategory(ModelView):
    label = "Categories"
    fields = [
        Category.id,
        Category.category_name,
        ColorField("color"),
        Category.icon,
        Category.is_active,
    ]
