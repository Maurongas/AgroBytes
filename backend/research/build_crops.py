"""
build_crops.py — Genera app/data/crops.json a partir de fuentes citables.

Uso (desde backend/):
    python research/build_crops.py            # descarga EcoCrop_DB.csv (1.6 MB) la primera vez a research/.cache/

De dónde sale cada campo (ver docs/INVESTIGACION-CULTIVOS.md §4):
  - temp_opt_*/temp_abs_*, frost_kill_c, ph_*, botanical_family, soils  → FAO ECOCROP (columnas TOPMN, TOPMX,
    TMIN, TMAX, KTMP, PHOPMN, PHOPMX, FAMNAME, TEXTR = textura tolerada). Copia pública: github.com/openclim/ecocrop
  - water_need_mm, cycle_days → FAO Irrigation Water Management, Training Manual 3, cap. 2, Tablas 4 y 5
    (punto medio del rango). Si FAO no lista el cultivo, se usa ECOCROP (GMIN/GMAX) o el cultivo FAO más parecido.
  - kc_ini, kc_mid, kc_end, crop_height_m → FAO-56 Tabla 12 (punto medio cuando la tabla da un rango; Kc ini del
    grupo del cultivo). kc_stages → FAO-56 Tabla 11: duración de las etapas inicial / desarrollo / media / final
    de la fila indicada, como fracción del ciclo. Con esto el motor arma la curva Kc de FAO-56 día por día.
  - nitrogen_delta_kg_ha (ESTIMADO, por ciclo): balance parcial de N = fijación − extracción por la cosecha
    (research/nitrogen.py: Ludemann et al. 2024 + Herridge et al. 2022) con el rendimiento FAOSTAT de México
    (o de EE. UU./Canadá si México no lo reporta). El motor usa el valor del PAÍS de la parcela
    (crop_countries.json); este es solo el valor por defecto. Correr antes research/build_crop_countries.py.
  - family (rol en la rotación) y seasons (temporadas de siembra en clima templado del norte): criterio propio,
    basado en los ciclos SIAP otoño-invierno / primavera-verano. La temporada es preferencia, no filtro.
"""

from __future__ import annotations

import csv
import json
import sys
import urllib.request
from pathlib import Path

AQUI = Path(__file__).parent
CACHE = AQUI / ".cache" / "EcoCrop_DB.csv"
SALIDA = AQUI.parent / "app" / "data" / "crops.json"
PAISES_JSON = AQUI.parent / "app" / "data" / "crop_countries.json"
URL = "https://raw.githubusercontent.com/openclim/ecocrop/main/EcoCrop_DB.csv"

OI = ["autumn", "winter"]  # otoño-invierno
PV = ["spring", "summer"]  # primavera-verano

# id, nombre, nombre científico (ECOCROP), rol, temporadas, agua FAO (min, max) mm, ciclo FAO (min, max) días
CULTIVOS = [
    ("maize", "Maíz", "Zea mays", "cereal", PV, (500, 800), (125, 180)),
    ("sorghum", "Sorgo", "Sorghum bicolor", "cereal", PV, (450, 650), (120, 130)),
    ("wheat", "Trigo", "Triticum aestivum", "cereal", OI, (450, 650), (120, 150)),
    ("barley", "Cebada", "Hordeum vulgare", "cereal", OI, (450, 650), (120, 150)),
    ("oat", "Avena", "Avena sativa", "cereal", OI, (450, 650), (120, 150)),
    ("bean", "Frijol", "Phaseolus vulgaris", "legume", PV, (300, 500), (95, 110)),
    ("soy", "Soya", "Glycine max", "legume", PV, (450, 700), (135, 150)),
    ("chickpea", "Garbanzo", "Cicer arietinum", "legume", OI, (350, 500), None),
    ("pea", "Chícharo", "Pisum sativum", "legume", OI, (350, 500), (90, 100)),
    ("vetch", "Veza (abono verde)", "Vicia sativa ssp. sativa", "cover", OI, (350, 500), None),
    ("canola", "Canola", "Brassica napus", "oilseed", OI, (450, 650), None),
    ("safflower", "Cártamo", "Carthamus tinctorius", "oilseed", OI, (600, 1000), None),
    ("cotton", "Algodón", "Gossypium hirsutum", "industrial", PV, (700, 1300), (180, 195)),
    ("tomato", "Jitomate", "Lycopersicon esculentum", "vegetable", PV, (400, 800), (135, 180)),
    ("chile", "Chile", "Capsicum annuum", "vegetable", PV, (600, 900), (120, 210)),
    ("potato", "Papa", "Solanum tuberosum", "vegetable", ["spring", "summer", "autumn"], (500, 700), (105, 145)),
    ("onion", "Cebolla", "Allium cepa", "vegetable", OI, (350, 550), (150, 210)),
    ("squash", "Calabaza", "Cucurbita pepo", "vegetable", PV, (400, 600), (95, 120)),
]
# Agua sin dato FAO: chickpea/vetch = rango de chícharo; canola = cereales de invierno; cártamo = girasol;
# calabaza = melón (FAO Tabla 5).

# FAO-56: Kc ini, Kc mid, Kc end, altura (m) — Tabla 12 —; etapas (ini, des, media, final) en días — Tabla 11 —
# y la fila usada. Kc ini = valor del grupo de la Tabla 12 (cereales 0.3, leguminosas 0.4, oleaginosas y fibras
# 0.35, solanáceas 0.6, raíces y tubérculos 0.5, hortalizas pequeñas 0.7, cucurbitáceas 0.5).
KC = {
    "maize": (0.30, 1.20, 0.35, 2.0, (30, 40, 50, 30), "maíz grano, abril, España/California"),
    "sorghum": (0.30, 1.05, 0.55, 1.5, (20, 35, 40, 30), "sorgo, may/jun, EE. UU."),
    "wheat": (0.30, 1.15, 0.325, 1.0, (20, 50, 60, 30), "cebada/avena/trigo, dic, desierto de California"),
    "barley": (0.30, 1.15, 0.25, 1.0, (20, 50, 60, 30), "cebada/avena/trigo, dic, desierto de California"),
    "oat": (0.30, 1.15, 0.25, 1.0, (20, 50, 60, 30), "cebada/avena/trigo, dic, desierto de California"),
    "bean": (0.40, 1.15, 0.35, 0.4, (20, 30, 40, 20), "frijol seco, may/jun, clima continental"),
    "soy": (0.40, 1.15, 0.50, 0.75, (20, 35, 60, 25), "soya, mayo, centro de EE. UU."),
    "chickpea": (0.40, 1.00, 0.35, 0.4, (20, 30, 35, 15), "sin fila propia: chícharo, mar/abr, Mediterráneo"),
    "pea": (0.40, 1.15, 0.30, 0.5, (20, 30, 35, 15), "chícharo, mar/abr, Mediterráneo"),
    "vetch": (0.40, 1.15, 0.30, 0.5, (20, 30, 35, 15), "sin fila propia (ni en Tabla 12): se usa chícharo"),
    "canola": (0.35, 1.075, 0.35, 0.6, (20, 35, 45, 25), "sin fila propia en Tabla 11: cártamo, abril, California"),
    "safflower": (0.35, 1.075, 0.25, 0.8, (20, 35, 45, 25), "cártamo, abril, California"),
    "cotton": (0.35, 1.175, 0.60, 1.35, (30, 50, 60, 55), "algodón, mar-may, Egipto/Pakistán/California"),
    "tomato": (0.60, 1.15, 0.80, 0.6, (30, 40, 45, 30), "jitomate, abr/may, Mediterráneo"),
    "chile": (0.60, 1.05, 0.90, 0.7, (25, 35, 40, 20), "pimiento, abr/jun, Europa y Mediterráneo"),
    "potato": (0.50, 1.15, 0.75, 0.6, (25, 30, 45, 30), "papa, mayo, clima continental"),
    "onion": (0.70, 1.05, 0.75, 0.4, (15, 25, 70, 40), "cebolla seca, abril, Mediterráneo"),
    "squash": (0.50, 0.95, 0.75, 0.3, (25, 35, 25, 15), "calabacita, abr/dic, Mediterráneo/zona árida"),
}

FAMILIAS = {  # ECOCROP usa nombres antiguos de familia
    "Gramineae": "Poaceae", "Leguminosae": "Fabaceae", "Cruciferae": "Brassicaceae", "Compositae": "Asteraceae",
    "Alliaceae": "Amaryllidaceae", "Umbelliferae": "Apiaceae",
}
TEXTURAS = {"light": "sandy", "medium": "loam", "heavy": "clay"}


def num(valor: str) -> float | None:
    try:
        return float(valor)
    except (TypeError, ValueError):
        return None


def descargar() -> None:
    if CACHE.exists():
        return
    CACHE.parent.mkdir(parents=True, exist_ok=True)
    print(f"Descargando {URL} ...")
    urllib.request.urlretrieve(URL, CACHE)


def suelos(fila: dict) -> list[str]:
    texto = fila["TEXTR"] or fila["TEXT"]  # textura tolerada (la óptima es demasiado estricta)
    encontrados = [s for clave, s in TEXTURAS.items() if clave in texto]
    return encontrados or ["sandy", "loam", "clay"]


def nitrogeno_por_defecto() -> dict[str, tuple[float, str]]:
    """{cultivo: (balance de N, país del rendimiento)}: México primero; si no lo reporta, EE. UU. o Canadá."""
    try:
        datos = json.loads(PAISES_JSON.read_text(encoding="utf-8"))["nitrogen_kg_ha"]
    except (FileNotFoundError, KeyError):
        sys.exit("Falta crop_countries.json con nitrogen_kg_ha: corre antes research/build_crop_countries.py")
    out: dict[str, tuple[float, str]] = {}
    for pais in ("MX", "US", "CA"):
        for cultivo, n in datos.get(pais, {}).items():
            out.setdefault(cultivo, (float(n), pais))
    return out


def main() -> None:
    descargar()
    filas = {f["ScientificName"]: f for f in csv.DictReader(CACHE.open(encoding="latin-1"))}
    n_defecto = nitrogeno_por_defecto()
    catalogo = []
    for (id_, nombre, cientifico, rol, temporadas, agua, ciclo) in CULTIVOS:
        f = filas.get(cientifico)
        if f is None:
            sys.exit(f"No está en ECOCROP: {cientifico}")
        if ciclo is None:  # FAO no lo lista → ECOCROP, acotado al rango típico de un cultivo anual
            ciclo = (int(num(f["GMIN"])), min(int(num(f["GMAX"])), 180))
        familia = f["FAMNAME"].split(":")[-1]
        kc_ini, kc_mid, kc_end, altura, etapas, _fila = KC[id_]
        n, pais_n = n_defecto.get(id_, (0.0, "—"))
        catalogo.append({
            "id": id_,
            "name": nombre,
            "scientific_name": cientifico.split(" ssp.")[0],
            "family": rol,
            "botanical_family": FAMILIAS.get(familia, familia),
            "temp_opt_min": num(f["TOPMN"]),
            "temp_opt_max": num(f["TOPMX"]),
            "temp_abs_min": num(f["TMIN"]),
            "temp_abs_max": num(f["TMAX"]),
            "frost_kill_c": num(f["KTMP"]),
            "ph_min": num(f["PHOPMN"]),
            "ph_max": num(f["PHOPMX"]),
            "water_need_mm": float(sum(agua) / 2),
            "kc_ini": kc_ini,
            "kc_mid": kc_mid,
            "kc_end": kc_end,
            "crop_height_m": altura,
            "kc_stages": [round(e / sum(etapas), 3) for e in etapas],
            "cycle_days": round(sum(ciclo) / 2),
            "seasons": temporadas,
            "soils": suelos(f),
            "nitrogen_delta_kg_ha": n,
            "source": (f"FAO ECOCROP ({cientifico}); FAO IWM T4-T5; FAO-56 T11-T12; "
                       f"N: Ludemann 2024 + Herridge 2022, rendimiento FAOSTAT {pais_n}"),
        })
    SALIDA.write_text(json.dumps(catalogo, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(f"{len(catalogo)} cultivos -> {SALIDA}")


if __name__ == "__main__":
    main()
