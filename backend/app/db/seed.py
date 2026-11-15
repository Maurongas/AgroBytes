"""Siembra idempotente del catálogo de cultivos desde app/data/crops.json."""

import json
from pathlib import Path

from sqlalchemy.dialects.postgresql import insert
from sqlalchemy.orm import Session

from app.db.database import SessionLocal
from app.models.crop import Crop

DATA_PATH = Path(__file__).resolve().parent.parent / "data" / "crops.json"


def seed_crops(db: Session) -> int:
    crops_data = json.loads(DATA_PATH.read_text(encoding="utf-8"))
    for item in crops_data:
        stmt = insert(Crop).values(**item)
        update_cols = {k: stmt.excluded[k] for k in item if k != "id"}
        stmt = stmt.on_conflict_do_update(index_elements=["id"], set_=update_cols)
        db.execute(stmt)
    db.commit()
    return len(crops_data)


def main() -> None:
    with SessionLocal() as db:
        count = seed_crops(db)
        print(f"Catálogo sembrado: {count} cultivos actualizados/insertados.")


if __name__ == "__main__":
    main()