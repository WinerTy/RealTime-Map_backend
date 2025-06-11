from typing import TYPE_CHECKING

from sqlalchemy import ForeignKey, String, Integer
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
