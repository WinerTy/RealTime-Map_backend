from typing import TYPE_CHECKING, List, Tuple

from sqlalchemy import func, select, and_
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
            select(self.model, OtherParticipant, Message)
            .join(self.model.participants.and_(User.id == current_user_id))
            .join(self.model.participants.of_type(OtherParticipant))
            .where(OtherParticipant.id != current_user_id)
            .join(last_message_subq, self.model.id == last_message_subq.c.chat_id)
            .join(Message, Message.id == last_message_subq.c.max_message_id)
            .order_by(Message.created_at.desc())
        )

        result = await self.session.execute(stmt)
        return result.unique().all()

    async def get_user_chats_ids(self, user_id: int) -> List[int]:
        stmt = (
            select(self.model.id)
            .join(self.model.participants)
            .where(User.id == user_id)
        )
        result = await self.session.execute(stmt)
        return result.all()

    async def check_user_in_chat(self, chat_id: int, user_id: int) -> bool:
        stmt = select(self.model.id).where(
            self.model.id == chat_id,
            self.model.participants.any(User.id == user_id),
        )
        result = await self.session.scalar(stmt)
        return result is not None

    async def find_or_create_private_chat(
        self, user1_id: int, user2_id: int
    ) -> Tuple[bool, Chat]:
        if user1_id > user2_id:
            user1_id, user2_id = user2_id, user1_id

        stmt = (
            select(self.model)
            .join(self.model.participants)
            .group_by(self.model.id)
            .having(
                and_(
                    func.count(User.id) == 2,
                    func.array_agg(User.id.op("ORDER BY")(User.id))
                    == [user1_id, user2_id],
                )
            )
        )

        result = await self.session.execute(stmt)
        existing_chat = result.scalar_one_or_none()

        if existing_chat:
            return False, existing_chat

        user1 = await self.session.get(User, user1_id)
        user2 = await self.session.get(User, user2_id)

        if not user1 or not user2:
            raise ValueError("user1_id/user2_id is invalid")

        new_chat = Chat(participants=[user1, user2])
        self.session.add(new_chat)
        await self.session.flush()
        await self.session.refresh(new_chat)
        return True, new_chat
