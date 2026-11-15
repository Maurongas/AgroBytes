"""Siembra idempotente del catálogo de cultivos (app/data/crops.json) y de la superficie cosechada por país
(app/data/crop_countries.json)."""

import json
from pathlib import Path

from sqlalchemy import select
from sqlalchemy.dialects.postgresql import insert
from sqlalchemy.orm import Session

from app.db.database import SessionLocal
from app.models.crop import Crop
from app.models.crop_country import CropCountry

DATA_PATH = Path(__file__).resolve().parent.parent / "data" / "crops.json"
COUNTRIES_PATH = DATA_PATH.with_name("crop_countries.json")


def seed_crops(db: Session) -> int:
    crops_data = json.loads(DATA_PATH.read_text(encoding="utf-8"))
    for item in crops_data:
        stmt = insert(Crop).values(**item)
        update_cols = {k: stmt.excluded[k] for k in item if k != "id"}
        stmt = stmt.on_conflict_do_update(index_elements=["id"], set_=update_cols)
        db.execute(stmt)
    db.commit()
    return len(crops_data)


def seed_crop_countries(db: Session) -> int:
    """Necesita los cultivos ya sembrados (llave foránea). Ignora cultivos que no estén en el catálogo."""
    data = json.loads(COUNTRIES_PATH.read_text(encoding="utf-8"))
    known = set(db.scalars(select(Crop.id)))
    yields = data.get("yields_t_ha", {})
    nitrogen = data.get("nitrogen_kg_ha", {})
    count = 0
    for country, areas in data["countries"].items():
        for crop_id, area in areas.items():
            if crop_id not in known:
                continue
            values = {"crop_id": crop_id, "country_code": country, "harvested_area_ha": area,
                      "yield_t_ha": yields.get(country, {}).get(crop_id),
                      "nitrogen_kg_ha": nitrogen.get(country, {}).get(crop_id),
                      "period": data["period"], "source": data["source"][:200]}
            stmt = insert(CropCountry).values(**values)
            stmt = stmt.on_conflict_do_update(
                index_elements=["crop_id", "country_code"],
                set_={k: stmt.excluded[k] for k in
                      ("harvested_area_ha", "yield_t_ha", "nitrogen_kg_ha", "period", "source")},
            )
            db.execute(stmt)
            count += 1
    db.commit()
    return count


def main() -> None:
    with SessionLocal() as db:
        count = seed_crops(db)
        print(f"Catálogo sembrado: {count} cultivos actualizados/insertados.")
        count = seed_crop_countries(db)
        print(f"Superficie por país sembrada: {count} filas (FAOSTAT).")


if __name__ == "__main__":
    main()