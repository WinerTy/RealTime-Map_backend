from typing import TYPE_CHECKING, List, Tuple

from sqlalchemy import func, select
from sqlalchemy.orm import aliased

from crud import BaseRepository
from models import User, Message
from models.chat.model import Chat
from models.chat.schemas import CreateChat, ReadChat, UpdateChat

if TYPE_CHECKING:
    from sqlalchemy.ext.asyncio import AsyncSession


class ChatRepository(BaseRepository[Chat, CreateChat, ReadChat, UpdateChat]):
    def __init__(self, session: "AsyncSession"):
        super().__init__(session=session, model=Chat)

    async def get_user_chats_with_details(
        self, current_user_id: int
    ) -> List[Tuple[Chat, User, Message]]:
        OtherParticipant = aliased(User)

        last_message_subq = (
            select(Message.chat_id, func.max(Message.id).label("max_message_id"))
            .group_by(Message.chat_id)
            .subquery("last_message_subq")
        )

        stmt = (
            select(Chat, OtherParticipant, Message)
            .join(Chat.participants.and_(User.id == current_user_id))
            .join(Chat.participants.of_type(OtherParticipant))
            .where(OtherParticipant.id != current_user_id)
            .join(last_message_subq, Chat.id == last_message_subq.c.chat_id)
            .join(Message, Message.id == last_message_subq.c.max_message_id)
            .order_by(Message.created_at.desc())
        )

        result = await self.session.execute(stmt)
        return result.unique().all()
