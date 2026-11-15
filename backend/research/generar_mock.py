"""
generar_mock.py — Regenera frontend/src/api/mock.ts con respuestas REALES del backend (NASA POWER + motor de reglas).

Así el modo demo (VITE_USE_MOCK=true) y la presentación muestran exactamente lo que el motor calcula, no números
escritos a mano. Volver a correrlo cada vez que cambie el motor o el catálogo.

Uso (con el backend corriendo en localhost:8000; solo usa la biblioteca estándar, corre fuera de Docker):
    python backend/research/generar_mock.py

La parcela principal es la misma que dibuja la presentación (docs/presentacion/src/components/FieldMap.tsx, valle
de Mexicali) con la misma petición que hace su demo en vivo (docs/presentacion/src/live.ts): maíz, prioridad
«ahorrar agua», sin indicar riego. Si cambias esa petición, cámbiala aquí también.
"""

from __future__ import annotations

import json
import urllib.request
from datetime import date
from pathlib import Path

API = "http://localhost:8000/api/v1/analyses?guardar=false"
SALIDA = Path(__file__).resolve().parents[2] / "frontend" / "src" / "api" / "mock.ts"

# FieldMap.tsx: SPOT + OFFSETS (lat, lon)
SPOT = (32.55, -115.25)
OFFSETS = [(0.001221, -0.00176), (0.001346, 0.001449), (-0.000414, 0.001863), (-0.001242, 0.000103),
           (-0.000983, -0.001915)]
PRINCIPAL = {"currentCrop": "maize", "priority": "water"}
# Segundo análisis del historial: trigo en otro punto del valle, con riego y prioridad nitrógeno
SEGUNDO = {"lat": 32.52, "lon": -115.35, "currentCrop": "wheat", "priority": "nitrogen", "irrigated": True}


def anillo(center: tuple[float, float], offsets: list[tuple[float, float]]) -> list[list[float]]:
    pts = [[round(center[1] + dx, 6), round(center[0] + dy, 6)] for dy, dx in offsets]  # GeoJSON: [lon, lat]
    return [*pts, pts[0]]


def analizar(geometry: dict, extra: dict) -> dict:
    body = json.dumps({"geometry": geometry, **extra}).encode()
    req = urllib.request.Request(API, data=body, headers={"Content-Type": "application/json"}, method="POST")
    with urllib.request.urlopen(req, timeout=60) as r:
        return json.loads(r.read())


def main() -> None:
    hoy = date.today()
    principal = analizar({"type": "Polygon", "coordinates": [anillo(SPOT, OFFSETS)]}, PRINCIPAL)
    principal |= {"id": "demo-001", "createdAt": f"{hoy}T18:00:00Z"}
    lat2, lon2 = SEGUNDO["lat"], SEGUNDO["lon"]
    segundo = analizar({"type": "Polygon", "coordinates": [anillo((lat2, lon2), [(o[0] * 0.6, o[1] * 0.6)
                                                                                for o in OFFSETS])]},
                       {k: v for k, v in SEGUNDO.items() if k not in ("lat", "lon")})
    historial = [
        {"id": "demo-001", "createdAt": f"{hoy}T18:00:00Z", "location": principal["location"],
         "areaHa": principal["areaHa"], "currentCrop": PRINCIPAL["currentCrop"], "priority": PRINCIPAL["priority"],
         "rotationCrops": [s["cropId"] for s in principal["rotation"]]},
        {"id": "demo-000", "createdAt": f"{hoy}T16:30:00Z", "location": segundo["location"],
         "areaHa": segundo["areaHa"], "currentCrop": SEGUNDO["currentCrop"], "priority": SEGUNDO["priority"],
         "rotationCrops": [s["cropId"] for s in segundo["rotation"]]},
    ]
    ts = (
        "// GENERADO por backend/research/generar_mock.py — no editar a mano.\n"
        f"// Respuesta real de POST /api/v1/analyses?guardar=false del {hoy:%d/%m/%Y}: NASA POWER + SoilGrids + motor\n"
        "// de reglas. Parcela y petición = las de la demo en vivo de la presentación (valle de Mexicali, maíz,\n"
        "// prioridad agua). Para actualizarlo: levanta el backend y corre `python backend/research/generar_mock.py`.\n"
        "import type { AnalysisResponse, AnalysisSummary } from './types';\n\n"
        f"export const mockAnalysis: AnalysisResponse = {json.dumps(principal, ensure_ascii=False, indent=2)};\n\n"
        f"export const mockHistory: AnalysisSummary[] = {json.dumps(historial, ensure_ascii=False, indent=2)};\n"
    )
    SALIDA.write_text(ts, encoding="utf-8")
    print(f"{SALIDA}: {len(principal['strategies'])} estrategias; rotacion "
          f"{[s['cropId'] for s in principal['rotation']]}")


if __name__ == "__main__":
    main()
