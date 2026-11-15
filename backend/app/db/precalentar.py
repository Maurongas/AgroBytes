"""Pre-calienta la caché de clima (tabla climate_cache) con los lugares de la demo.

Uso, con `docker compose up` corriendo:
    docker compose exec backend python -m app.db.precalentar
Así el primer análisis de cada lugar no espera a NASA POWER durante la presentación.
"""

import asyncio
import time

from app.db.database import SessionLocal
from app.services import climate as climate_service
from app.services.nasa_power import NasaUnavailableError

LUGARES = {
    "Ensenada": (31.86, -116.60),
    "Valle de Guadalupe": (32.08, -116.62),
    "Tijuana": (32.51, -117.04),
    "Mexicali": (32.66, -115.47),
    "Culiacán": (24.80, -107.39),
}


async def main() -> None:
    with SessionLocal() as db:
        for nombre, (lat, lon) in LUGARES.items():
            inicio = time.perf_counter()
            try:
                await climate_service.get_climate(lat, lon, db=db)
                print(f"OK     {nombre:<20} {time.perf_counter() - inicio:5.1f} s")
            except NasaUnavailableError as exc:
                print(f"FALLÓ  {nombre:<20} {exc}")


if __name__ == "__main__":
    asyncio.run(main())
