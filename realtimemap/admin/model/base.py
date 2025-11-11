from typing import TYPE_CHECKING

from starlette.requests import Request
from starlette_admin.contrib.sqla import ModelView

if TYPE_CHECKING:
    from modules import User


class BaseModelAdmin(ModelView):
    @staticmethod
    def get_current_user(request: Request) -> "User":
        user = request.state.user
        return user
