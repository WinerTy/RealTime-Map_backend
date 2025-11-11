from typing import Protocol, List, Tuple, TYPE_CHECKING, Union

from interfaces import IBaseRepository
from modules import Message, Chat, User
from modules.chat.schemas import UpdateChat, CreateChat
from modules.message import CreateMessage, UpdateMessage

if TYPE_CHECKING:
    from sqlalchemy import Select
    from modules.message.filters import MessageFilter


class IMessageRepository(
    IBaseRepository[Message, CreateMessage, UpdateMessage], Protocol
):

    async def create_message(self, data: CreateMessage) -> Message: ...

    async def get_chat_messages(
        self, chat_id: int, params: "MessageFilter"
    ) -> List[Message]: ...


class IChatRepository(IBaseRepository[Chat, CreateChat, UpdateChat], Protocol):

    async def get_user_chats_with_details(
        self, current_user_id: int
    ) -> List[Tuple[Chat, User, Message]]: ...

    async def get_user_chats_ids(self, user_id: int) -> List[int]: ...

    async def check_user_in_chat(
        self, chat_id: int, user_id: int, get_stmt: bool = False
    ) -> Union[bool, "Select"]: ...

    async def find_or_create_private_chat(
        self, user1_id: int, user2_id: int
    ) -> Tuple[bool, Chat]: ...
