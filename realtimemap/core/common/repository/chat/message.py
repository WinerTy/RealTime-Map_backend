from abc import ABC, abstractmethod
from typing import List, TYPE_CHECKING

from core.common.repository import BaseRepository
from modules.message import CreateMessage, UpdateMessage, Message

if TYPE_CHECKING:
    from modules.message.filters import MessageFilter


class MessageRepository(BaseRepository[Message, CreateMessage, UpdateMessage], ABC):

    @abstractmethod
    async def get_chat_messages(
        self, chat_id: int, params: "MessageFilter"
    ) -> List[Message]:
        """
        Метод на получение сообщений в определенном чате
        :param chat_id:
        :param params:
        :return:
        """
        raise NotImplementedError
