"""Add ImageField field

Revision ID: 683f255a906b
Revises: ac302ae9839b
Create Date: 2025-06-06 15:27:22.563773

"""

from typing import Sequence, Union

import sqlalchemy as sa
import sqlalchemy_file
from alembic import op

# revision identifiers, used by Alembic.
revision: str = "683f255a906b"
down_revision: Union[str, None] = "ac302ae9839b"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    # ### commands auto generated by Alembic - please adjust! ###
    # op.drop_table('spatial_ref_sys')
    op.add_column(
        "marks", sa.Column("photo", sqlalchemy_file.types.ImageField(), nullable=True)
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    """Downgrade schema."""
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column("marks", "photo")
    op.create_table(
        "spatial_ref_sys",
        sa.Column("srid", sa.INTEGER(), autoincrement=False, nullable=False),
        sa.Column(
            "auth_name", sa.VARCHAR(length=256), autoincrement=False, nullable=True
        ),
        sa.Column("auth_srid", sa.INTEGER(), autoincrement=False, nullable=True),
        sa.Column(
            "srtext", sa.VARCHAR(length=2048), autoincrement=False, nullable=True
        ),
        sa.Column(
            "proj4text", sa.VARCHAR(length=2048), autoincrement=False, nullable=True
        ),
        sa.CheckConstraint(
            "srid > 0 AND srid <= 998999", name="spatial_ref_sys_srid_check"
        ),
        sa.PrimaryKeyConstraint("srid", name="spatial_ref_sys_pkey"),
    )
    # ### end Alembic commands ###
