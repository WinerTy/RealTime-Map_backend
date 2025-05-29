from typing import Optional

from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column

from models.base import BaseSqlModel
from models.mixins import IntIdMixin


class Category(BaseSqlModel, IntIdMixin):
    __tablename__ = "categories"
    category_name: Mapped[str] = mapped_column(String(64), nullable=False, unique=True)
    color: Mapped[Optional[str]] = mapped_column(String(32), nullable=True)

    icon: Mapped[str] = mapped_column(String(128), nullable=True)

    # Meta Fields
    is_active: Mapped[bool] = mapped_column(default=True, nullable=False)
