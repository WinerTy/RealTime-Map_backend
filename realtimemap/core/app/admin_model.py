from fastapi_amis_admin.admin import admin

from models import Category
from models.category.schemas import CreateCategory

from fastapi_amis_admin.amis.components import Form
from fastapi_amis_admin.crud import BaseApiOut
from pydantic import BaseModel
from starlette.requests import Request

from typing import Any
from models.user.schemas import UserLogin


class AdminCategory(admin.ModelAdmin):
    page_schema = "Category"

    model = Category

    list_per_page_max = 100

    schema_create = CreateCategory


class UserLoginFormAdmin(admin.FormAdmin):
    page_schema = "UserLoginForm"
    # Configure form information, can be omitted
    form = Form(
        title="This is a test login form",
        submitText="Login",
    )

    # Create a form data model
    class schema(UserLogin):
        pass

    # Handle form submission data
    async def handle(
        self, request: Request, data: BaseModel, **kwargs
    ) -> BaseApiOut[Any]:
        if data.username == "amisadmin" and data.password == "amisadmin":
            return BaseApiOut(msg="Login successful!", data={"token": "xxxxxxx"})
        return BaseApiOut(status=-1, msg="Username or password error!")
