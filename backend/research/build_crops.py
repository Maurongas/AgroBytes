"""
build_crops.py — Genera app/data/crops.json a partir de fuentes citables.

Uso (desde backend/):
    python research/build_crops.py            # descarga EcoCrop_DB.csv (1.6 MB) la primera vez a research/.cache/

De dónde sale cada campo (ver docs/INVESTIGACION-CULTIVOS.md §4):
  - temp_opt_*/temp_abs_*, frost_kill_c, ph_*, botanical_family, soils  → FAO ECOCROP (columnas TOPMN, TOPMX,
    TMIN, TMAX, KTMP, PHOPMN, PHOPMX, FAMNAME, TEXTR = textura tolerada). Copia pública: github.com/openclim/ecocrop
  - water_need_mm, cycle_days → FAO Irrigation Water Management, Training Manual 3, cap. 2, Tablas 4 y 5
    (punto medio del rango). Si FAO no lista el cultivo, se usa ECOCROP (GMIN/GMAX) o el cultivo FAO más parecido.
  - kc_mid → FAO-56 Tabla 12.
  - nitrogen_delta_kg_ha (ESTIMADO, por temporada):
      leguminosas de grano = 40 % del N fijado (el resto sale con el grano); cobertura incorporada = 100 %.
      Fijación: Kebede 2021 (Front. Sustain. Food Syst., Tabla 1). No leguminosas = − extracción en la cosecha
      (kg N/t, tabla de Manitoba Agriculture) × rendimiento típico supuesto. Donde no hay fuente: "N aprox.".
  - family (rol en la rotación) y seasons (temporadas de siembra en clima templado del norte): criterio propio,
    basado en los ciclos SIAP otoño-invierno / primavera-verano.
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
URL = "https://raw.githubusercontent.com/openclim/ecocrop/main/EcoCrop_DB.csv"

OI = ["autumn", "winter"]  # otoño-invierno
PV = ["spring", "summer"]  # primavera-verano

# id, nombre, nombre científico (ECOCROP), rol, temporadas, agua FAO (min, max) mm, ciclo FAO (min, max) días,
# kc_mid FAO-56, N (kg/ha, estimado), nota de la fuente del N
CULTIVOS = [
    ("maize", "Maíz", "Zea mays", "cereal", PV, (500, 800), (125, 180), 1.20, -104, "N: 17.4 kg/t × 6 t"),
    ("sorghum", "Sorgo", "Sorghum bicolor", "cereal", PV, (450, 650), (120, 130), 1.05, -87, "N: 17.4 kg/t (maíz) × 5 t"),
    ("wheat", "Trigo", "Triticum aestivum", "cereal", OI, (450, 650), (120, 150), 1.15, -105, "N: 21 kg/t × 5 t"),
    ("barley", "Cebada", "Hordeum vulgare", "cereal", OI, (450, 650), (120, 150), 1.15, -81, "N: 20.3 kg/t × 4 t"),
    ("oat", "Avena", "Avena sativa", "cereal", OI, (450, 650), (120, 150), 1.15, -55, "N: 18.3 kg/t × 3 t"),
    ("bean", "Frijol", "Phaseolus vulgaris", "legume", PV, (300, 500), (95, 110), 1.15, 18, "N: 40 % de 16–72 fijado"),
    ("soy", "Soya", "Glycine max", "legume", PV, (450, 700), (135, 150), 1.15, 37, "N: 40 % de 90–95 fijado"),
    ("chickpea", "Garbanzo", "Cicer arietinum", "legume", OI, (350, 500), None, 1.00, 25, "N: 40 % de 21–104 fijado"),
    ("pea", "Chícharo", "Pisum sativum", "legume", OI, (350, 500), (90, 100), 1.15, 15, "N: 40 % de 30–40 fijado"),
    ("vetch", "Veza (abono verde)", "Vicia sativa ssp. sativa", "cover", OI, (350, 500), None, 1.00, 119,
     "N: 107–131 fijado, se incorpora"),
    ("canola", "Canola", "Brassica napus", "oilseed", OI, (450, 650), None, 1.10, -77, "N: 38.7 kg/t × 2 t"),
    ("safflower", "Cártamo", "Carthamus tinctorius", "oilseed", OI, (600, 1000), None, 1.10, -50, "N aprox."),
    ("cotton", "Algodón", "Gossypium hirsutum", "industrial", PV, (700, 1300), (180, 195), 1.18, -60, "N aprox."),
    ("tomato", "Jitomate", "Lycopersicon esculentum", "vegetable", PV, (400, 800), (135, 180), 1.15, -90, "N aprox."),
    ("chile", "Chile", "Capsicum annuum", "vegetable", PV, (600, 900), (120, 210), 1.05, -70, "N aprox."),
    ("potato", "Papa", "Solanum tuberosum", "vegetable", ["spring", "summer", "autumn"], (500, 700), (105, 145), 1.15,
     -80, "N aprox."),
    ("onion", "Cebolla", "Allium cepa", "vegetable", OI, (350, 550), (150, 210), 1.05, -50, "N aprox."),
    ("squash", "Calabaza", "Cucurbita pepo", "vegetable", PV, (400, 600), (95, 120), 1.00, -40, "N aprox."),
]
# Agua sin dato FAO: chickpea/vetch = rango de chícharo; canola = cereales de invierno; cártamo = girasol;
# calabaza = melón (FAO Tabla 5).

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


def main() -> None:
    descargar()
    filas = {f["ScientificName"]: f for f in csv.DictReader(CACHE.open(encoding="latin-1"))}
    catalogo = []
    for (id_, nombre, cientifico, rol, temporadas, agua, ciclo, kc, n, nota_n) in CULTIVOS:
        f = filas.get(cientifico)
        if f is None:
            sys.exit(f"No está en ECOCROP: {cientifico}")
        if ciclo is None:  # FAO no lo lista → ECOCROP, acotado al rango típico de un cultivo anual
            ciclo = (int(num(f["GMIN"])), min(int(num(f["GMAX"])), 180))
        familia = f["FAMNAME"].split(":")[-1]
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
            "kc_mid": kc,
            "cycle_days": round(sum(ciclo) / 2),
            "seasons": temporadas,
            "soils": suelos(f),
            "nitrogen_delta_kg_ha": float(n),
            "source": f"FAO ECOCROP ({cientifico}); FAO IWM T4-T5; FAO-56 T12; {nota_n}",
        })
    SALIDA.write_text(json.dumps(catalogo, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(f"{len(catalogo)} cultivos -> {SALIDA}")


if __name__ == "__main__":
    main()
