import enum
from typing import TYPE_CHECKING

from geoalchemy2 import Geometry
from sqlalchemy import ForeignKey, String, Index, Enum
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .base import BaseSqlModel
from .mixins import IntIdMixin, TimeMarkMixin

if TYPE_CHECKING:
    from .user import User


class TypeMark(str, enum.Enum):
    game = "Игры"
    other = "Другое"


class Mark(BaseSqlModel, IntIdMixin, TimeMarkMixin):
    mark_name: Mapped[str] = mapped_column(String(128), nullable=False)
    geom: Mapped[Geometry] = mapped_column(
        Geometry(geometry_type="POINT", srid=4326), nullable=False
    )
    photo: Mapped[str] = mapped_column(String(256), nullable=True)
    owner_id: Mapped[int] = mapped_column(
        ForeignKey("users.id", ondelete="CASCADE"), nullable=False
    )
    owner: Mapped["User"] = relationship(
        "User",
        foreign_keys=[owner_id],
    )
    type_mark: Mapped[str] = mapped_column(
        Enum(TypeMark),
        nullable=False,
        default=TypeMark.other,
        server_default=TypeMark.other.value,
    )
    additional_info: Mapped[str] = mapped_column(String(256), nullable=True)

    __table_args__ = (Index("idx_locations_geom", geom, postgresql_using="gist"),)
