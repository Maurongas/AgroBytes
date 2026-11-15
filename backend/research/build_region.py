"""
build_region.py — Genera el contorno de la región de trabajo (México, EE. UU. y Canadá).

Uso (desde backend/):
    python research/build_region.py     # descarga Natural Earth 1:50m (3 MB) la primera vez a research/.cache/

Fuente: Natural Earth, Admin 0 – Countries, escala 1:50m (dominio público).
        https://www.naturalearthdata.com/downloads/50m-cultural-vectors/50m-admin-0-countries-2/

Para que el archivo sea pequeño (también lo carga el navegador):
  - solo el anillo exterior de cada polígono (sin huecos);
  - se quitan las islas de menos de 2 000 km² (casi todas en el Ártico; ninguna es zona agrícola relevante);
  - se simplifica con Douglas-Peucker a 0.02° (~2 km) y se redondea a 3 decimales (~100 m).
El error de ~2 km en la costa se compensa con una tolerancia de 0.05° (~5 km) al validar (services/region.py).

Escribe el MISMO archivo en dos lugares (backend y frontend):
  backend/app/data/region.json  y  frontend/src/data/region.json
"""

from __future__ import annotations

import json
import math
import sys
import urllib.request
from pathlib import Path

AQUI = Path(__file__).parent
CACHE = AQUI / ".cache" / "ne_50m_admin_0_countries.geojson"
URL = ("https://raw.githubusercontent.com/nvkelso/natural-earth-vector/master/geojson/"
       "ne_50m_admin_0_countries.geojson")
SALIDAS = [AQUI.parent / "app" / "data" / "region.json",
           AQUI.parent.parent / "frontend" / "src" / "data" / "region.json"]

PAISES = {"MX": "México", "US": "Estados Unidos", "CA": "Canadá"}
MIN_ISLA_KM2 = 2000
TOLERANCIA_GRADOS = 0.02
DECIMALES = 3


def descargar() -> None:
    if CACHE.exists():
        return
    CACHE.parent.mkdir(parents=True, exist_ok=True)
    print(f"Descargando {URL} …")
    urllib.request.urlretrieve(URL, CACHE)


def area_km2(anillo: list[list[float]]) -> float:
    """Área aproximada (proyección equirectangular local + fórmula de Gauss)."""
    lat0 = sum(p[1] for p in anillo) / len(anillo)
    k = 111.32  # km por grado
    xy = [(p[0] * k * math.cos(math.radians(lat0)), p[1] * k) for p in anillo]
    return abs(sum(a[0] * b[1] - b[0] * a[1] for a, b in zip(xy, xy[1:] + xy[:1]))) / 2


def douglas_peucker(puntos: list[list[float]], tol: float) -> list[list[float]]:
    """Versión iterativa (los anillos de Canadá tienen miles de puntos)."""
    if len(puntos) < 3:
        return puntos
    conservar = [False] * len(puntos)
    conservar[0] = conservar[-1] = True
    pila = [(0, len(puntos) - 1)]
    while pila:
        i, j = pila.pop()
        (ax, ay), (bx, by) = puntos[i][:2], puntos[j][:2]
        dx, dy = bx - ax, by - ay
        largo = math.hypot(dx, dy)
        mejor, k_mejor = 0.0, -1
        for k in range(i + 1, j):
            px, py = puntos[k][:2]
            d = abs(dy * (px - ax) - dx * (py - ay)) / largo if largo else math.hypot(px - ax, py - ay)
            if d > mejor:
                mejor, k_mejor = d, k
        if mejor > tol:
            conservar[k_mejor] = True
            pila += [(i, k_mejor), (k_mejor, j)]
    return [p for p, c in zip(puntos, conservar) if c]


def main() -> None:
    descargar()
    datos = json.loads(CACHE.read_text(encoding="utf-8"))
    paises: dict[str, dict] = {}
    for f in datos["features"]:
        codigo = f["properties"]["ISO_A2"]
        if codigo not in PAISES:
            continue
        g = f["geometry"]
        poligonos = g["coordinates"] if g["type"] == "MultiPolygon" else [g["coordinates"]]
        anillos = []
        for poligono in poligonos:
            exterior = poligono[0]
            if area_km2(exterior) < MIN_ISLA_KM2:
                continue
            simple = douglas_peucker(exterior, TOLERANCIA_GRADOS)
            if len(simple) >= 4:
                anillos.append([[round(lon, DECIMALES), round(lat, DECIMALES)] for lon, lat in simple])
        paises[codigo] = {"name": PAISES[codigo], "rings": anillos}
    faltan = set(PAISES) - set(paises)
    if faltan:
        sys.exit(f"No se encontraron en Natural Earth: {faltan}")

    salida = {
        "source": "Natural Earth 1:50m Admin 0 – Countries (dominio público), simplificado a ~2 km "
                  "(research/build_region.py)",
        "countries": paises,
    }
    texto = json.dumps(salida, ensure_ascii=False, separators=(",", ":"))
    for ruta in SALIDAS:
        ruta.parent.mkdir(parents=True, exist_ok=True)
        ruta.write_text(texto + "\n", encoding="utf-8")
        print(f"{ruta}: {len(texto) / 1024:.0f} KB")
    for codigo, p in paises.items():
        print(f"  {codigo}: {len(p['rings'])} polígonos, {sum(len(r) for r in p['rings'])} vértices")


if __name__ == "__main__":
    main()
