from sqlalchemy import ForeignKey, Integer
from sqlalchemy.orm import Mapped, mapped_column

from modules import BaseSqlModel
from modules.mixins import IntIdMixin, TimeMarkMixin


class UserMetric(BaseSqlModel, IntIdMixin, TimeMarkMixin):
    user_id: Mapped[int] = mapped_column(
        ForeignKey("users.id", ondelete="SET NULL"),
        nullable=True,
        unique=True,
        index=True,
    )
    # Метрики меток
    total_marks: Mapped[int] = mapped_column(
        Integer, nullable=False, default=0, server_default="0"
    )
    active_marks: Mapped[int] = mapped_column(
        Integer, nullable=False, default=0, server_default="0"
    )
    ended_marks: Mapped[int] = mapped_column(
        Integer, nullable=False, default=0, server_default="0"
    )
    # Соц метрики
