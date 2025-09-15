from typing import Annotated, TYPE_CHECKING, List

from fastapi import APIRouter, Depends, BackgroundTasks

from api.v1.auth.fastapi_users import get_current_user_without_ban
from core.app.socket import sio
from core.config import conf
from dependencies.checker import check_message_exist
from dependencies.service import get_chat_service
from models import User
from models.chat.schemas import ReadChat
from models.message.schemas import CreateMessageRequest, UpdateMessageRequest
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


@router.post(
    "/message/",
)
async def send_message(
    user: current_user,
    service: chat_service,
    message: CreateMessageRequest,
    background: BackgroundTasks,
):
    result = await service.send_message(user=user, message=message)
    background.add_task(
        sio.emit,
        event="new_message",
        room=str(result.chat_id),
        data=result.content,
        namespace=conf.socket.prefix.chat,
    )
    return result


@router.patch("/message/{message_id}", dependencies=[Depends(check_message_exist)])
async def update_message(
    message_id: int,
    user: current_user,
    service: chat_service,
    message: UpdateMessageRequest,
):
    message = await service.update_message(message_id, message, user)
    return message


@router.delete("/message/{message_id}", dependencies=[Depends(check_message_exist)])
async def delete_message(
    message_id: int,
    user: current_user,
    service: chat_service,
):
    message = await service.delete_message(message_id, user)
    return message
