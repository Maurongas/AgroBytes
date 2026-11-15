from datetime import datetime

from sqlalchemy import DateTime, Float, Integer, String, UniqueConstraint, func
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm import Mapped, mapped_column

from app.db.database import Base


class ClimateCache(Base):
    __tablename__ = "climate_cache"
    __table_args__ = (
        UniqueConstraint(
            "lat_grid", "lon_grid", "period", name="uq_climate_cache_grid_period"
        ),
    )

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    lat_grid: Mapped[float] = mapped_column(Float, nullable=False)
    lon_grid: Mapped[float] = mapped_column(Float, nullable=False)
    period: Mapped[str] = mapped_column(String(30), nullable=False)
    payload: Mapped[dict] = mapped_column(JSONB, nullable=False)
    fetched_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), nullable=False
    )