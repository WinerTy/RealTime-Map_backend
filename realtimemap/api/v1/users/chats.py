from typing import Annotated, TYPE_CHECKING, List

from fastapi import APIRouter, Depends

from api.v1.auth.fastapi_users import get_current_user_without_ban
from dependencies.service import get_chat_service
from models import User
from models.chat.schemas import ReadChat
from services.chat.service import ChatService

if TYPE_CHECKING:
    pass

router = APIRouter(
    prefix="/chats",
    tags=["chats"],
)

current_user = Annotated[User, Depends(get_current_user_without_ban)]
chat_service = Annotated[ChatService, Depends(get_chat_service)]


@router.get("/", response_model=List[ReadChat])
async def get_chats(
    user: current_user,
    service: chat_service,
):
    result = await service.get_chats_for_user(user)
    return result


@router.post("/{chat_id}/")
async def send_message(chat_id: int, user: current_user):
    pass
