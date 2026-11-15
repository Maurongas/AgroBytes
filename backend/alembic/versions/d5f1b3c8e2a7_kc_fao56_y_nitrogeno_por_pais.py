"""curva Kc de FAO-56 en crops y rendimiento + balance de N por país en crop_countries

Agrega a crops: kc_ini, kc_end, crop_height_m, kc_stages (FAO-56 Tablas 11 y 12).
Agrega a crop_countries: yield_t_ha, nitrogen_kg_ha (FAOSTAT + Ludemann et al. 2024 + Herridge et al. 2022).
Los datos los vuelve a sembrar app/db/seed.py.

Revision ID: d5f1b3c8e2a7
Revises: c4e8a2f7b913
Create Date: 2026-11-15 12:00:00.000000

"""
from typing import Sequence, Union

import sqlalchemy as sa
from alembic import op
from sqlalchemy.dialects import postgresql

revision: str = "d5f1b3c8e2a7"
down_revision: Union[str, Sequence[str], None] = "c4e8a2f7b913"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column("crops", sa.Column("kc_ini", sa.Float(), nullable=True))
    op.add_column("crops", sa.Column("kc_end", sa.Float(), nullable=True))
    op.add_column("crops", sa.Column("crop_height_m", sa.Float(), nullable=True))
    op.add_column("crops", sa.Column("kc_stages", postgresql.ARRAY(sa.Float()), nullable=True))
    op.add_column("crop_countries", sa.Column("yield_t_ha", sa.Float(), nullable=True))
    op.add_column("crop_countries", sa.Column("nitrogen_kg_ha", sa.Float(), nullable=True))


def downgrade() -> None:
    op.drop_column("crop_countries", "nitrogen_kg_ha")
    op.drop_column("crop_countries", "yield_t_ha")
    for col in ("kc_stages", "crop_height_m", "kc_end", "kc_ini"):
        op.drop_column("crops", col)
