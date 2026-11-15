"""
build_crop_countries.py — Qué tanto se siembra cada cultivo del catálogo en cada país (México, EE. UU., Canadá).

Uso (desde backend/):
    python research/build_crop_countries.py   # descarga FAOSTAT QCL (Américas, 3.6 MB) la primera vez a .cache/

Fuente: FAOSTAT, dominio "Crops and livestock products" (QCL), elemento 5312 "Area harvested" (ha).
        Descarga en bloque: https://bulks-faostat.fao.org/production/Production_Crops_Livestock_E_Americas.zip
        Licencia CC BY 4.0 (FAO). Se usa el PROMEDIO de los últimos 5 años con dato, para suavizar años malos
        (p. ej. la sequía de 2023 en México, cuando el frijol bajó a la mitad).

        También: elemento 5510 "Production" (t) → rendimiento real del país = producción / área.

Cómo se usa (services/recommender.py, ver ARQUITECTURA §7):
  - Un cultivo solo se RECOMIENDA en un país si ahí se cosechan ≥ 10 000 ha al año (si no, nadie lo siembra ni
    tiene a quién venderlo). El cultivo actual del usuario no se filtra.
  - Excepción: los cultivos de cobertura (veza) no aparecen en estadísticas de COSECHA porque se incorporan al
    suelo; no se filtran.
  - Balance de nitrógeno por cultivo y país (research/nitrogen.py): N fijado (Herridge et al. 2022, con el
    rendimiento de grano del país) − N que sale con la cosecha (Ludemann et al. 2024 × producción del país).

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

import nitrogen

AQUI = Path(__file__).parent
CACHE = AQUI / ".cache" / "Production_Crops_Livestock_E_Americas.zip"
URL = "https://bulks-faostat.fao.org/production/Production_Crops_Livestock_E_Americas.zip"
CSV = "Production_Crops_Livestock_E_Americas_NOFLAG.csv"
SALIDA = AQUI.parent / "app" / "data" / "crop_countries.json"

PAISES = {"Mexico": "MX", "United States of America": "US", "Canada": "CA"}
ELEMENTO_AREA_COSECHADA = "5312"
ELEMENTO_PRODUCCION = "5510"
ANIOS = 5
ROLES_LEGUMINOSA = {"bean", "soy", "chickpea", "pea"}
# Para la fijación se usa el rendimiento de GRANO SECO (así está calibrado el modelo de Herridge)
GRANO_SECO = {"bean": "176", "soy": "236", "chickpea": "191", "pea": "187"}

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


def leer_series() -> dict[tuple[str, str, str], dict[int, float]]:
    """(país, código de producto, elemento) → {año: valor}, solo para los productos y elementos que usamos."""
    codigos = {cod for cods in PRODUCTOS.values() for cod in cods}
    elementos = {ELEMENTO_AREA_COSECHADA, ELEMENTO_PRODUCCION}
    series: dict[tuple[str, str, str], dict[int, float]] = {}
    with zipfile.ZipFile(CACHE) as z, z.open(CSV) as f:
        lector = csv.DictReader(io.TextIOWrapper(f, encoding="latin-1"))
        columnas_anio = [c for c in lector.fieldnames or [] if re.fullmatch(r"Y\d{4}", c)]
        for fila in lector:
            pais = PAISES.get(fila["Area"])
            if not pais or fila["Item Code"] not in codigos or fila["Element Code"] not in elementos:
                continue
            serie = series.setdefault((pais, fila["Item Code"], fila["Element Code"]), {})
            for col in columnas_anio:
                if fila[col]:
                    serie[int(col[1:])] = float(fila[col])
    return series


def promedio(serie: dict[int, float], anios: list[int]) -> float:
    valores = [serie[a] for a in anios if a in serie]
    return sum(valores) / len(valores) if valores else 0.0


def main() -> None:
    descargar()
    series = leer_series()
    ultimo = max(a for (_, _, e), s in series.items() if e == ELEMENTO_AREA_COSECHADA for a in s)
    anios = list(range(ultimo - ANIOS + 1, ultimo + 1))

    def media(pais: str, codigo: str, elemento: str) -> float:
        return promedio(series.get((pais, codigo, elemento), {}), anios)

    paises: dict[str, dict[str, float]] = {}
    rendimientos: dict[str, dict[str, float]] = {}
    nitrogeno: dict[str, dict[str, float]] = {}
    for codigo_pais in PAISES.values():
        areas, rinde, n = {}, {}, {}
        for cultivo, codigos in PRODUCTOS.items():
            area = sum(media(codigo_pais, c, ELEMENTO_AREA_COSECHADA) for c in codigos)
            produccion = {c: media(codigo_pais, c, ELEMENTO_PRODUCCION) for c in codigos}
            areas[cultivo] = round(area)
            if area <= 0 or sum(produccion.values()) <= 0:
                continue  # sin datos en el país: el catálogo trae un valor por defecto
            rinde[cultivo] = round(sum(produccion.values()) / area, 2)
            grano = None
            if cultivo in GRANO_SECO:
                cod = GRANO_SECO[cultivo]
                area_seco = media(codigo_pais, cod, ELEMENTO_AREA_COSECHADA)
                grano = media(codigo_pais, cod, ELEMENTO_PRODUCCION) / area_seco if area_seco > 0 else None
            rol = "cover" if cultivo == "vetch" else ("legume" if cultivo in ROLES_LEGUMINOSA else "other")
            n[cultivo] = round(nitrogen.balance_kg_ha(cultivo, rol, grano, nitrogen.removal_kg_ha(produccion, area)))
        paises[codigo_pais] = dict(sorted(areas.items(), key=lambda kv: -kv[1]))
        rendimientos[codigo_pais] = rinde
        nitrogeno[codigo_pais] = n

    salida = {
        "source": f"FAOSTAT QCL, área cosechada (ha) y producción (t), promedio {anios[0]}–{anios[-1]} (CC BY 4.0)",
        "period": f"{anios[0]}-{anios[-1]}",
        "countries": paises,
        "yields_t_ha": rendimientos,
        "nitrogen_source": ("Balance parcial de N (kg/ha por ciclo) = fijación (Herridge et al. 2022) − extracción "
                            "por cosecha (Ludemann et al. 2024, ESSD 16:525) con el rendimiento FAOSTAT del país"),
        "nitrogen_kg_ha": nitrogeno,
    }
    SALIDA.write_text(json.dumps(salida, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(f"{SALIDA} ({salida['source']})")
    for codigo, areas in paises.items():
        print(f"  {codigo}: " + ", ".join(f"{c} {a:,.0f} ha / {rendimientos[codigo].get(c, 0)} t/ha / "
                                         f"N {nitrogeno[codigo].get(c, '—')}" for c, a in areas.items()))


if __name__ == "__main__":
    main()
