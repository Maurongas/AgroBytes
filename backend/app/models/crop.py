from sqlalchemy import Float, Integer, String
from sqlalchemy.dialects.postgresql import ARRAY
from sqlalchemy.orm import Mapped, mapped_column

from app.db.database import Base


class Crop(Base):
    """Catálogo de cultivos. Se llena con app/db/seed.py desde app/data/crops.json
    (que genera research/build_crops.py a partir de FAO ECOCROP + tablas FAO)."""

    __tablename__ = "crops"

    id: Mapped[str] = mapped_column(String(50), primary_key=True)
    name: Mapped[str] = mapped_column(String(100), nullable=False)
    scientific_name: Mapped[str] = mapped_column(String(100), nullable=False, default="")
    # Rol en la rotación: cereal | legume | cover | vegetable | oilseed | industrial
    family: Mapped[str] = mapped_column(String(30), nullable=False)
    # Familia botánica (Poaceae, Fabaceae, Solanaceae…): la que importa para plagas y enfermedades
    botanical_family: Mapped[str] = mapped_column(String(50), nullable=False, default="")
    temp_opt_min: Mapped[float] = mapped_column(Float, nullable=False)
    temp_opt_max: Mapped[float] = mapped_column(Float, nullable=False)
    temp_abs_min: Mapped[float] = mapped_column(Float, nullable=False)
    temp_abs_max: Mapped[float] = mapped_column(Float, nullable=False)
    frost_kill_c: Mapped[float | None] = mapped_column(Float, nullable=True)
    ph_min: Mapped[float | None] = mapped_column(Float, nullable=True)
    ph_max: Mapped[float | None] = mapped_column(Float, nullable=True)
    water_need_mm: Mapped[float] = mapped_column(Float, nullable=False)
    # Curva de coeficiente de cultivo de FAO-56 (Tablas 11 y 12): Kc inicial, medio y final, altura y fracción
    # del ciclo de cada etapa (inicial, desarrollo, media, final)
    kc_ini: Mapped[float | None] = mapped_column(Float, nullable=True)
    kc_mid: Mapped[float | None] = mapped_column(Float, nullable=True)
    kc_end: Mapped[float | None] = mapped_column(Float, nullable=True)
    crop_height_m: Mapped[float | None] = mapped_column(Float, nullable=True)
    kc_stages: Mapped[list[float] | None] = mapped_column(ARRAY(Float), nullable=True)
    cycle_days: Mapped[int] = mapped_column(Integer, nullable=False)
    seasons: Mapped[list[str]] = mapped_column(ARRAY(String), nullable=False)
    soils: Mapped[list[str]] = mapped_column(ARRAY(String), nullable=False)
    nitrogen_delta_kg_ha: Mapped[float] = mapped_column(Float, nullable=False)
    source: Mapped[str] = mapped_column(String(300), nullable=False)
