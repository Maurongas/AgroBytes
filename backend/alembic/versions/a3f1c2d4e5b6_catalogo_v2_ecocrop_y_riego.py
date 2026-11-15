"""catalogo v2 (ECOCROP/FAO) y riego en analyses

Agrega a crops: scientific_name, botanical_family, frost_kill_c, ph_min, ph_max, kc_mid y amplía source.
Agrega a analyses: irrigated. Los datos del catálogo los vuelve a sembrar app/db/seed.py.

Revision ID: a3f1c2d4e5b6
Revises: 7c4987b08e73
Create Date: 2026-11-14 18:00:00.000000

"""
from typing import Sequence, Union

import sqlalchemy as sa
from alembic import op

revision: str = "a3f1c2d4e5b6"
down_revision: Union[str, Sequence[str], None] = "7c4987b08e73"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column("crops", sa.Column("scientific_name", sa.String(length=100), nullable=False, server_default=""))
    op.add_column("crops", sa.Column("botanical_family", sa.String(length=50), nullable=False, server_default=""))
    op.add_column("crops", sa.Column("frost_kill_c", sa.Float(), nullable=True))
    op.add_column("crops", sa.Column("ph_min", sa.Float(), nullable=True))
    op.add_column("crops", sa.Column("ph_max", sa.Float(), nullable=True))
    op.add_column("crops", sa.Column("kc_mid", sa.Float(), nullable=True))
    op.alter_column("crops", "source", type_=sa.String(length=300), existing_nullable=False)
    op.add_column("analyses", sa.Column("irrigated", sa.Boolean(), nullable=True))


def downgrade() -> None:
    op.drop_column("analyses", "irrigated")
    op.alter_column("crops", "source", type_=sa.String(length=150), existing_nullable=False)
    for col in ("kc_mid", "ph_max", "ph_min", "frost_kill_c", "botanical_family", "scientific_name"):
        op.drop_column("crops", col)
