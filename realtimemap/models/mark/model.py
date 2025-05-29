from typing import TYPE_CHECKING

from geoalchemy2 import Geometry
from geoalchemy2.functions import ST_Y, ST_X
from sqlalchemy import ForeignKey, String, Index
from sqlalchemy.orm import Mapped, mapped_column, relationship

from models.base import BaseSqlModel
from models.mixins import IntIdMixin, TimeMarkMixin

if TYPE_CHECKING:
    from models.user.model import User
    from models.category.model import Category


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
    category_id: Mapped[int] = mapped_column(
        ForeignKey("categories.id", ondelete="CASCADE"), nullable=False
    )
    category: Mapped["Category"] = relationship(
        "Category",
        foreign_keys=[category_id],
    )
    additional_info: Mapped[str] = mapped_column(String(256), nullable=True)

    __table_args__ = (Index("idx_locations_geom", geom, postgresql_using="gist"),)

    @property
    def latitude(self) -> float:
        return ST_Y(self.geom)

    @property
    def longitude(self) -> float:
        return ST_X(self.geom)

    def __str__(self):
        return f"{self.mark_name}: {self.id}"
