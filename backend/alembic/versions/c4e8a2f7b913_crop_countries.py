"""tabla crop_countries (cultivos que se siembran en cada país, FAOSTAT)

Superficie cosechada promedio de cada cultivo del catálogo en México, EE. UU. y Canadá. El motor solo recomienda
cultivos con ≥ 10 000 ha en el país de la parcela (ver ARQUITECTURA §6 y §7).

Revision ID: c4e8a2f7b913
Revises: b7d2e9f4a1c3
Create Date: 2026-11-14 22:00:00.000000

"""
from typing import Sequence, Union

import sqlalchemy as sa
from alembic import op

revision: str = "c4e8a2f7b913"
down_revision: Union[str, Sequence[str], None] = "b7d2e9f4a1c3"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        "crop_countries",
        sa.Column("crop_id", sa.String(length=50), sa.ForeignKey("crops.id", ondelete="CASCADE"), nullable=False),
        sa.Column("country_code", sa.String(length=2), nullable=False),
        sa.Column("harvested_area_ha", sa.Float(), nullable=False),
        sa.Column("period", sa.String(length=20), nullable=False),
        sa.Column("source", sa.String(length=200), nullable=False),
        sa.PrimaryKeyConstraint("crop_id", "country_code"),
    )


def downgrade() -> None:
    op.drop_table("crop_countries")
