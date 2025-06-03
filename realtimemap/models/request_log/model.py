from sqlalchemy import Integer, String
from sqlalchemy.orm import Mapped, mapped_column

from models import BaseSqlModel
from models.mixins import IntIdMixin, CreateMixin


class RequestLog(BaseSqlModel, IntIdMixin, CreateMixin):
    user_id: Mapped[int] = mapped_column(Integer, nullable=True)
    method: Mapped[str] = mapped_column(String(32))
    endpoint: Mapped[str] = mapped_column(String(128))
    params: Mapped[str] = mapped_column(String(256), nullable=True)
    headers: Mapped[str] = mapped_column(String(256), nullable=True)
    ip: Mapped[str] = mapped_column(String(256), nullable=False)
    agent: Mapped[str] = mapped_column(String(256), nullable=True)
