from fastapi_amis_admin.admin import admin

from models import Category
from models.category.schemas import CreateCategory


class AdminCategory(admin.ModelAdmin):
    page_schema = "Category"

    model = Category

    list_per_page_max = 100

    schema_create = CreateCategory
