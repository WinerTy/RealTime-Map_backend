from abc import ABC, abstractmethod
from typing import Tuple, List, Union, TYPE_CHECKING

from core.common.repository import BaseRepository
from modules.chat.model import Chat
from modules.chat.schemas import UpdateChat, CreateChat
from modules.message.model import Message
from modules.user.model import User

if TYPE_CHECKING:
    from sqlalchemy import Select


class ChatRepository(BaseRepository[Chat, CreateChat, UpdateChat], ABC):

    @abstractmethod
    async def get_user_chats_with_details(
        self, user_id: int
    ) -> List[Tuple[Chat, User, Message]]:
        """
        Метод возвращает чаты текущего пользователя с последним сообщением в данном чате
        :param user_id:
        :return:
        """
        raise NotImplementedError

    @abstractmethod
    async def check_user_in_chat(
        self, chat_id: int, user_id: int, get_stmt: bool = False
    ) -> Union[bool, "Select"]:
        """
        Метод проверяет есть ли пользователь в чате, дополнительно может вернуть select
        :param chat_id:
        :param user_id:
        :param get_stmt:
        :return:
        """
        raise NotImplementedError

    @abstractmethod
    async def find_or_create_private_chat(
        self, user1_id: int, user2_id: int
    ) -> Tuple[bool, Chat]:
        """
        Метод проверяет есть ли пользователь в чате с другим пользователем,
        если нет то создаст чат с ним
        :param user1_id:
        :param user2_id:
        :return:
        """
        raise NotImplementedError

    @abstractmethod
    async def get_user_chats_ids(self, user_id: int) -> List[int]:
        """
        Возвращает список id чатов пользователя
        :param user_id:
        :return:
        """
        raise NotImplementedError
