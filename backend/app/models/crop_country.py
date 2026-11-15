from sqlalchemy import Float, ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column

from app.db.database import Base


class CropCountry(Base):
    """Superficie cosechada de cada cultivo del catálogo en cada país (FAOSTAT). Se llena con app/db/seed.py
    desde app/data/crop_countries.json (que genera research/build_crop_countries.py). Ver ARQUITECTURA §6."""

    __tablename__ = "crop_countries"

    crop_id: Mapped[str] = mapped_column(String(50), ForeignKey("crops.id", ondelete="CASCADE"), primary_key=True)
    # ISO 3166-1 alfa-2: MX | US | CA
    country_code: Mapped[str] = mapped_column(String(2), primary_key=True)
    # Promedio anual del periodo (ha); 0 = no se siembra en ese país
    harvested_area_ha: Mapped[float] = mapped_column(Float, nullable=False)
    period: Mapped[str] = mapped_column(String(20), nullable=False)
    source: Mapped[str] = mapped_column(String(200), nullable=False)
