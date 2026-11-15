"""crea analyses crops climate_cache y elimina historial_consultas

Revision ID: 7c4987b08e73
Revises: 
Create Date: 2026-11-14 14:00:00.000000

"""
from typing import Sequence, Union

from alembic import op
import geoalchemy2
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision: str = "7c4987b08e73"
down_revision: Union[str, Sequence[str], None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.execute("CREATE EXTENSION IF NOT EXISTS postgis")

    op.create_table(
        "analyses",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column(
            "created_at",
            sa.DateTime(timezone=True),
            server_default=sa.text("now()"),
            nullable=False,
        ),
        sa.Column(
            "geom",
            geoalchemy2.types.Geography(
                geometry_type="POLYGON",
                srid=4326,
                spatial_index=False,
                from_text="ST_GeogFromText",
                name="geography",
            ),
            nullable=False,
        ),
        sa.Column("lat", sa.Float(), nullable=False),
        sa.Column("lon", sa.Float(), nullable=False),
        sa.Column("area_ha", sa.Float(), nullable=False),
        sa.Column("current_crop", sa.String(length=50), nullable=False),
        sa.Column("priority", sa.String(length=20), nullable=False),
        sa.Column("soil", postgresql.JSONB(astext_type=sa.Text()), nullable=True),
        sa.Column(
            "climate_summary",
            postgresql.JSONB(astext_type=sa.Text()),
            nullable=False,
        ),
        sa.Column(
            "result", postgresql.JSONB(astext_type=sa.Text()), nullable=False
        ),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(
        "idx_analyses_geom",
        "analyses",
        ["geom"],
        unique=False,
        postgresql_using="gist",
    )
    op.create_index(op.f("ix_analyses_id"), "analyses", ["id"], unique=False)

    op.create_table(
        "climate_cache",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("lat_grid", sa.Float(), nullable=False),
        sa.Column("lon_grid", sa.Float(), nullable=False),
        sa.Column("period", sa.String(length=30), nullable=False),
        sa.Column(
            "payload", postgresql.JSONB(astext_type=sa.Text()), nullable=False
        ),
        sa.Column(
            "fetched_at",
            sa.DateTime(timezone=True),
            server_default=sa.text("now()"),
            nullable=False,
        ),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint(
            "lat_grid", "lon_grid", "period", name="uq_climate_cache_grid_period"
        ),
    )
    op.create_index(
        op.f("ix_climate_cache_id"), "climate_cache", ["id"], unique=False
    )

    op.create_table(
        "crops",
        sa.Column("id", sa.String(length=50), nullable=False),
        sa.Column("name", sa.String(length=100), nullable=False),
        sa.Column("family", sa.String(length=30), nullable=False),
        sa.Column("temp_opt_min", sa.Float(), nullable=False),
        sa.Column("temp_opt_max", sa.Float(), nullable=False),
        sa.Column("temp_abs_min", sa.Float(), nullable=False),
        sa.Column("temp_abs_max", sa.Float(), nullable=False),
        sa.Column("water_need_mm", sa.Float(), nullable=False),
        sa.Column("cycle_days", sa.Integer(), nullable=False),
        sa.Column("seasons", postgresql.ARRAY(sa.String()), nullable=False),
        sa.Column("soils", postgresql.ARRAY(sa.String()), nullable=False),
        sa.Column("nitrogen_delta_kg_ha", sa.Float(), nullable=False),
        sa.Column("source", sa.String(length=150), nullable=False),
        sa.PrimaryKeyConstraint("id"),
    )

    op.execute("DROP TABLE IF EXISTS historial_consultas")


def downgrade() -> None:
    op.drop_table("crops")
    op.drop_index(op.f("ix_climate_cache_id"), table_name="climate_cache")
    op.drop_table("climate_cache")
    op.drop_index(op.f("ix_analyses_id"), table_name="analyses")
    op.drop_index("idx_analyses_geom", table_name="analyses", postgresql_using="gist")
    op.drop_table("analyses")