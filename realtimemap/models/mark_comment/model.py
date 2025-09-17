import logging
from datetime import datetime
from enum import Enum as PyEnum
from typing import TYPE_CHECKING, Optional, List

from sqlalchemy import (
    ForeignKey,
    String,
    Integer,
    Boolean,
    UniqueConstraint,
    DateTime,
    func,
    Index,
    event,
    Connection,
    Enum,
)
from sqlalchemy.dialects.postgresql import insert
from sqlalchemy.orm import mapped_column, Mapped, relationship, Session

from models import BaseSqlModel
from models.mixins import IntIdMixin, TimeMarkMixin

if TYPE_CHECKING:
    from models.mark.model import Mark
    from models.user.model import User
    from fastapi import Request


class CommentReactionType(str, PyEnum):
    like = "like"
    dislike = "dislike"


logger = logging.getLogger(__name__)


class MarkComment(BaseSqlModel, IntIdMixin, TimeMarkMixin):
    mark_id: Mapped[int] = mapped_column(
        ForeignKey("marks.id", ondelete="CASCADE"), nullable=False
    )
    user_id: Mapped[int] = mapped_column(
        ForeignKey("users.id", ondelete="CASCADE"), nullable=False
    )
    content: Mapped[str] = mapped_column(String(256), nullable=False)

    likes: Mapped[int] = mapped_column(Integer, nullable=False, default=0)
    dislikes: Mapped[int] = mapped_column(Integer, nullable=False, default=0)

    user: Mapped["User"] = relationship(
        "User",
        foreign_keys=[user_id],
    )
    mark: Mapped["Mark"] = relationship(
        "Mark",
        foreign_keys=[mark_id],
    )


class Comment(BaseSqlModel, IntIdMixin, TimeMarkMixin):
    content: Mapped[str] = mapped_column(String(256), nullable=False)

    is_deleted: Mapped[bool] = mapped_column(Boolean, default=False)

    # FK
    owner_id: Mapped[int] = mapped_column(
        ForeignKey("users.id", ondelete="CASCADE"), nullable=False
    )
    mark_id: Mapped[int] = mapped_column(
        ForeignKey("marks.id", ondelete="CASCADE"), nullable=False
    )
    parent_id: Mapped[Optional[int]] = mapped_column(
        ForeignKey("comments.id", ondelete="CASCADE"), nullable=True
    )

    # RS
    parent: Mapped["Comment"] = relationship(
        remote_side="Comment.id",
        back_populates="replies",
    )
    replies: Mapped[List["Comment"]] = relationship(back_populates="parent")
    mark: Mapped["Mark"] = relationship(
        back_populates="comments", foreign_keys=[mark_id]
    )
    owner: Mapped["User"] = relationship(back_populates="comments")
    stats: Mapped["CommentStat"] = relationship(back_populates="comment")
    reactions: Mapped[List["CommentReaction"]] = relationship(
        back_populates="comment", foreign_keys="CommentReaction.comment_id"
    )

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    async def __admin_repr__(self, _: "Request"):
        return f"Comment №{self.id}: {self.content[:25]}"


class CommentReaction(BaseSqlModel, IntIdMixin, TimeMarkMixin):
    # FK
    user_id: Mapped[int] = mapped_column(
        ForeignKey("users.id", ondelete="CASCADE"), nullable=False
    )
    comment_id: Mapped[int] = mapped_column(
        ForeignKey("comments.id", ondelete="CASCADE"), nullable=False
    )
    # cols
    reaction_type: Mapped[str] = mapped_column(
        Enum(CommentReactionType, name="comment_reaction_type"),
        nullable=False,
        server_default=CommentReactionType.like.value,
        default=CommentReactionType.like,
    )

    # RS
    user: Mapped["User"] = relationship(
        back_populates="reactions", foreign_keys=[user_id]
    )
    comment: Mapped["Comment"] = relationship(
        back_populates="reactions", foreign_keys=[comment_id]
    )

    __table_args__ = (
        UniqueConstraint("user_id", "comment_id", name="uq_user_comment_reaction"),
    )


class CommentStat(BaseSqlModel, IntIdMixin):
    # FK
    comment_id: Mapped[int] = mapped_column(
        ForeignKey("comments.id", ondelete="CASCADE"), nullable=False
    )

    # cols
    likes_count: Mapped[int] = mapped_column(Integer, nullable=False, default=0)
    dislikes_count: Mapped[int] = mapped_column(Integer, nullable=False, default=0)
    total_replies: Mapped[int] = mapped_column(Integer, nullable=False, default=0)
    last_activity: Mapped[datetime] = mapped_column(DateTime, server_default=func.now())

    # RS
    comment: Mapped["Comment"] = relationship(back_populates="stats")

    __table_args__ = (
        Index("ix_comment_stats_likes", "likes_count"),
        Index("ix_comment_stats_activity", "last_activity"),
    )

    async def __admin_repr__(self, _: "Request"):
        return f"Likes: {self.likes_count}. Dislikes: {self.dislikes_count}"


@event.listens_for(Comment, "after_insert")
def create_base_stats(mapper, connection: Connection, target: Comment):
    logger.info("Create base stats")
    connection.execute(
        insert(CommentStat).values(
            comment_id=target.id,
        )
    )


# TODO ивент для автоматического обновления статистики
@event.listens_for(Session, "before_flush")
def update_comment_stats(session: Session, flush_context, instances):
    pass
