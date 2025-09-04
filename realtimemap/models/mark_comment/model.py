from datetime import datetime
from typing import TYPE_CHECKING, Optional

from sqlalchemy import (
    ForeignKey,
    String,
    Integer,
    Boolean,
    UniqueConstraint,
    DateTime,
    func,
    Index,
)
from sqlalchemy.orm import mapped_column, Mapped, relationship

from models import BaseSqlModel
from models.mixins import IntIdMixin, TimeMarkMixin

if TYPE_CHECKING:
    from models.mark.model import Mark
    from models.user.model import User


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
    #
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        print("Вызов init")


class CommentReaction(BaseSqlModel, IntIdMixin, TimeMarkMixin):
    # FK
    user_id: Mapped[int] = mapped_column(
        ForeignKey("users.id", ondelete="CASCADE"), nullable=False
    )
    comment_id: Mapped[int] = mapped_column(
        ForeignKey("comments.id", ondelete="CASCADE"), nullable=False
    )
    # cols
    is_like: Mapped[bool] = mapped_column(Boolean, default=False)

    # RS
    #
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
    #
    __table_args__ = (
        Index("ix_comment_stats_likes", "likes_count"),
        Index("ix_comment_stats_activity", "last_activity"),
    )
