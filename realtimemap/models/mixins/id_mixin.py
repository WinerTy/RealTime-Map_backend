from sqlalchemy import Integer
from sqlalchemy.orm import Mapped, mapped_column


class IntIdMixin:
    """
    Mixin class to add an 'id' integer primary key column to a SQLAlchemy model
    """

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
