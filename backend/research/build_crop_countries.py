"""
build_crop_countries.py — Qué tanto se siembra cada cultivo del catálogo en cada país (México, EE. UU., Canadá).

Uso (desde backend/):
    python research/build_crop_countries.py   # descarga FAOSTAT QCL (Américas, 3.6 MB) la primera vez a .cache/

Fuente: FAOSTAT, dominio "Crops and livestock products" (QCL), elemento 5312 "Area harvested" (ha).
        Descarga en bloque: https://bulks-faostat.fao.org/production/Production_Crops_Livestock_E_Americas.zip
        Licencia CC BY 4.0 (FAO). Se usa el PROMEDIO de los últimos 5 años con dato, para suavizar años malos
        (p. ej. la sequía de 2023 en México, cuando el frijol bajó a la mitad).

Cómo se usa (services/recommender.py, ver ARQUITECTURA §7):
  - Un cultivo solo se RECOMIENDA en un país si ahí se cosechan ≥ 10 000 ha al año (si no, nadie lo siembra ni
    tiene a quién venderlo). El cultivo actual del usuario no se filtra.
  - Excepción: los cultivos de cobertura (veza) no aparecen en estadísticas de COSECHA porque se incorporan al
    suelo; no se filtran.

Salida: app/data/crop_countries.json  (lo siembra app/db/seed.py en la tabla crop_countries).
"""

from __future__ import annotations

import csv
import io
import json
import re
import urllib.request
import zipfile
from pathlib import Path

AQUI = Path(__file__).parent
CACHE = AQUI / ".cache" / "Production_Crops_Livestock_E_Americas.zip"
URL = "https://bulks-faostat.fao.org/production/Production_Crops_Livestock_E_Americas.zip"
CSV = "Production_Crops_Livestock_E_Americas_NOFLAG.csv"
SALIDA = AQUI.parent / "app" / "data" / "crop_countries.json"

PAISES = {"Mexico": "MX", "United States of America": "US", "Canada": "CA"}
ELEMENTO_AREA_COSECHADA = "5312"
ANIOS = 5

# id del catálogo → códigos de producto FAOSTAT (se suman). Seco + verde cuando FAOSTAT los separa.
PRODUCTOS = {
    "maize": ["56"],  # Maize (corn)
    "sorghum": ["83"],  # Sorghum
    "wheat": ["15"],  # Wheat
    "barley": ["44"],  # Barley
    "oat": ["75"],  # Oats
    "bean": ["176"],  # Beans, dry
    "soy": ["236"],  # Soya beans
    "chickpea": ["191"],  # Chick peas, dry
    "pea": ["187", "417"],  # Peas, dry + Peas, green
    "vetch": ["205"],  # Vetches (solo grano; como abono verde no se cosecha)
    "canola": ["270"],  # Rape or colza seed
    "safflower": ["280"],  # Safflower seed
    "cotton": ["328"],  # Seed cotton, unginned
    "tomato": ["388"],  # Tomatoes
    "chile": ["401", "689"],  # Chillies and peppers, green + dry
    "potato": ["116"],  # Potatoes
    "onion": ["403", "402"],  # Onions and shallots, dry + green
    "squash": ["394"],  # Pumpkins, squash and gourds
}


def descargar() -> None:
    if CACHE.exists():
        return
    CACHE.parent.mkdir(parents=True, exist_ok=True)
    print(f"Descargando {URL} …")
    urllib.request.urlretrieve(URL, CACHE)


def main() -> None:
    descargar()
    codigo_a_cultivo = {cod: cultivo for cultivo, cods in PRODUCTOS.items() for cod in cods}
    # (país, cultivo) → {año: ha}
    series: dict[tuple[str, str], dict[int, float]] = {}
    with zipfile.ZipFile(CACHE) as z, z.open(CSV) as f:
        lector = csv.DictReader(io.TextIOWrapper(f, encoding="latin-1"))
        columnas_anio = [c for c in lector.fieldnames or [] if re.fullmatch(r"Y\d{4}", c)]
        for fila in lector:
            pais = PAISES.get(fila["Area"])
            cultivo = codigo_a_cultivo.get(fila["Item Code"])
            if not pais or not cultivo or fila["Element Code"] != ELEMENTO_AREA_COSECHADA:
                continue
            serie = series.setdefault((pais, cultivo), {})
            for col in columnas_anio:
                if fila[col]:
                    anio = int(col[1:])
                    serie[anio] = serie.get(anio, 0.0) + float(fila[col])

    ultimo = max(a for s in series.values() for a in s)
    anios = list(range(ultimo - ANIOS + 1, ultimo + 1))
    paises: dict[str, dict[str, float]] = {}
    for codigo in PAISES.values():
        areas = {}
        for cultivo in PRODUCTOS:
            serie = series.get((codigo, cultivo), {})
            valores = [serie[a] for a in anios if a in serie]
            areas[cultivo] = round(sum(valores) / len(valores)) if valores else 0
        paises[codigo] = dict(sorted(areas.items(), key=lambda kv: -kv[1]))

    salida = {
        "source": f"FAOSTAT QCL, área cosechada (ha), promedio {anios[0]}–{anios[-1]} (CC BY 4.0)",
        "period": f"{anios[0]}-{anios[-1]}",
        "countries": paises,
    }
    SALIDA.write_text(json.dumps(salida, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(f"{SALIDA} ({salida['source']})")
    for codigo, areas in paises.items():
        print(f"  {codigo}: " + ", ".join(f"{c} {a:,.0f}" for c, a in areas.items()))


if __name__ == "__main__":
    main()
