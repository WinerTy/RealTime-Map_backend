from typing import TYPE_CHECKING

from fastapi import Request

if TYPE_CHECKING:
    from integrations.payment.yookassa import YookassaClient


async def get_yookassa_client(request: Request) -> "YookassaClient":
    return request.app.state.yookassa_client
