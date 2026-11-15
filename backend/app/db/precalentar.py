"""Pre-calienta las cachés de clima (BD y memoria) y suelo con los lugares de la demo.

Uso, con `docker compose up` corriendo:
    docker compose exec backend python -m app.db.precalentar
Así el primer análisis de cada lugar no espera a NASA POWER ni SoilGrids durante la presentación.
"""

import asyncio
import time

import httpx

API = "http://localhost:8000"  # dentro del contenedor del backend, el propio uvicorn
LADO = 0.0005  # ~55 m → parcela de ~1 ha (dentro del límite 0.1–500 ha)

LUGARES = {
    "Ensenada": (31.86, -116.60),
    "Valle de Guadalupe": (32.08, -116.62),
    "Tijuana": (32.51, -117.04),
    "Mexicali": (32.66, -115.47),
    "Culiacán": (24.80, -107.39),
}


def parcela(lat: float, lon: float) -> dict:
    a, b, c, d = lon - LADO, lat - LADO, lon + LADO, lat + LADO
    return {"type": "Polygon", "coordinates": [[[a, b], [c, b], [c, d], [a, d], [a, b]]]}


async def main() -> None:
    async with httpx.AsyncClient(base_url=API, timeout=90) as client:
        for nombre, (lat, lon) in LUGARES.items():
            inicio = time.perf_counter()
            r = await client.post("/api/v1/analyses", params={"guardar": "false"},
                                  headers={"X-Device-Id": "precalentar-demo"},
                                  json={"geometry": parcela(lat, lon), "currentCrop": "maize", "priority": "water"})
            estado = "OK   " if r.status_code == 200 else f"{r.status_code}  "
            print(f"{estado} {nombre:<20} {time.perf_counter() - inicio:5.1f} s")


if __name__ == "__main__":
    asyncio.run(main())
