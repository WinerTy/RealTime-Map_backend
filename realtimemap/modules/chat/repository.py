from typing import List, Tuple, Union

from sqlalchemy import select, func, Select, and_
from sqlalchemy.orm import aliased

from core.common.repository import ChatRepository
from database.adapter import PgAdapter
from modules.message.model import Message
from modules.user.model import User
from .model import Chat
from .schemas import CreateChat, UpdateChat


class PgChatRepository(ChatRepository):
    def __init__(self, adapter: PgAdapter[Chat, CreateChat, UpdateChat]):
        super().__init__(adapter)
        self.adapter = adapter

    async def get_user_chats_with_details(
        self, current_user_id: int
    ) -> List[Tuple[Chat, User, Message]]:
        other_participant = aliased(User)

        last_message_subq = (
            select(Message.chat_id, func.max(Message.id).label("max_message_id"))
            .group_by(Message.chat_id)
            .subquery("last_message_subq")
        )

        stmt = (
            select(self.model, other_participant, Message)
            .join(self.model.participants.and_(User.id == current_user_id))
            .join(self.model.participants.of_type(other_participant))
            .where(other_participant.id != current_user_id)
            .join(last_message_subq, self.model.id == last_message_subq.c.chat_id)
            .join(Message, Message.id == last_message_subq.c.max_message_id)
            .order_by(Message.created_at.desc())
        )

        result = await self.session.execute(stmt)
        return result.unique().all()

    async def get_user_chats_ids(self, user_id: int) -> List[int]:
        stmt = select(Chat.id).join(Chat.participants).where(User.id == user_id)
        result = await self.session.execute(stmt)
        return result.scalars().all()

    async def check_user_in_chat(
        self, chat_id: int, user_id: int, get_stmt: bool = False
    ) -> Union[bool, "Select"]:
        stmt = select(Chat.id).where(
            Chat.id == chat_id,
            Chat.participants.any(User.id == user_id),
        )
        if get_stmt:
            return stmt
        result = await self.adapter.execute_scalar(stmt)
        return result is not None

    async def find_or_create_private_chat(
        self, user1_id: int, user2_id: int
    ) -> Tuple[bool, Chat]:
        if user1_id > user2_id:
            user1_id, user2_id = user2_id, user1_id

        stmt = (
            select(Chat)
            .join(Chat.participants)
            .group_by(Chat.id)
            .having(
                and_(
                    func.count(User.id) == 2,
                    func.array_agg(User.id.op("ORDER BY")(User.id))
                    == [user1_id, user2_id],
                )
            )
        )

        existing_chat = await self.adapter.execute_query_one(stmt)

        if existing_chat:
            return False, existing_chat
        user1_stmt = select(User).where(User.id == user1_id)
        user2_stmt = select(User).where(User.id == user2_id)
        user1 = await self.adapter.execute_query_one(user1_stmt)
        user2 = await self.adapter.execute_query_one(user2_stmt)

        if not user1 or not user2:
            raise ValueError("user1_id/user2_id is invalid")

        new_chat = Chat(participants=[user1, user2])
        self.session.add(new_chat)
        await self.session.flush()
        await self.session.refresh(new_chat)
        return True, new_chat
