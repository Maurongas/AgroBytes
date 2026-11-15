"""device_id en analyses (historial por dispositivo)

Cada análisis guarda el dispositivo anónimo que lo creó (header X-Device-Id). Los análisis viejos quedan con
NULL. El historial y el borrado se filtran por este campo (ver ARQUITECTURA §5.3).

Revision ID: b7d2e9f4a1c3
Revises: a3f1c2d4e5b6
Create Date: 2026-11-14 20:00:00.000000

"""
from typing import Sequence, Union

import sqlalchemy as sa
from alembic import op

revision: str = "b7d2e9f4a1c3"
down_revision: Union[str, Sequence[str], None] = "a3f1c2d4e5b6"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column("analyses", sa.Column("device_id", sa.String(length=64), nullable=True))
    op.create_index("ix_analyses_device_id", "analyses", ["device_id"])


def downgrade() -> None:
    op.drop_index("ix_analyses_device_id", table_name="analyses")
    op.drop_column("analyses", "device_id")
