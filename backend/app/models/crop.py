from sqlalchemy import Float, Integer, String
from sqlalchemy.dialects.postgresql import ARRAY
from sqlalchemy.orm import Mapped, mapped_column

from app.db.database import Base


class Crop(Base):
    __tablename__ = "crops"

    id: Mapped[str] = mapped_column(String(50), primary_key=True)
    name: Mapped[str] = mapped_column(String(100), nullable=False)
    family: Mapped[str] = mapped_column(String(30), nullable=False)
    temp_opt_min: Mapped[float] = mapped_column(Float, nullable=False)
    temp_opt_max: Mapped[float] = mapped_column(Float, nullable=False)
    temp_abs_min: Mapped[float] = mapped_column(Float, nullable=False)
    temp_abs_max: Mapped[float] = mapped_column(Float, nullable=False)
    water_need_mm: Mapped[float] = mapped_column(Float, nullable=False)
    cycle_days: Mapped[int] = mapped_column(Integer, nullable=False)
    seasons: Mapped[list[str]] = mapped_column(ARRAY(String), nullable=False)
    soils: Mapped[list[str]] = mapped_column(ARRAY(String), nullable=False)
    nitrogen_delta_kg_ha: Mapped[float] = mapped_column(Float, nullable=False)
    source: Mapped[str] = mapped_column(String(150), nullable=False)