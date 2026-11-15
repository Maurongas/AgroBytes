"""
validar_motor.py — Contrasta el motor de reglas con lo que de verdad se siembra, con clima REAL de NASA POWER.

Uso (desde backend/, con internet; tarda ~1 min):
    python research/validar_motor.py            # escribe research/validacion_resultados.md

Qué mide
--------
1. Viabilidad (sensibilidad): para cada cultivo que una fuente oficial reporta como sembrado en un lugar y
   temporada, ¿el motor lo considera climáticamente viable (aptitud EcoCrop > 0 en su mejor fecha de siembra)?
2. Fecha de siembra: ¿el mes de siembra que sugiere el motor cae dentro (o a un mes) de la ventana oficial?
3. Especificidad: casos donde un cultivo NO se siembra por clima (algodón al norte de ~37° N, cualquier cultivo
   en el invierno del Medio Oeste o las praderas canadienses): ¿el motor lo descarta?
4. Barbecho: en inviernos sin agricultura, ¿el motor propone descanso?
5. Calibración del margen de helada letal de EcoCrop (KILL_MARGIN_C): se repite todo con 0, 2.5 y 5 °C.
6. Sensibilidad de los parámetros de diseño (pesos y castigos): ¿cuántos pasos de la rotación cambian si cada
   parámetro se mueve ±50 % (pesos) o ±0.15 (castigos)?

Fuentes de lo "real" (ver docs/VALIDACION.md):
- EE. UU.: USDA NASS (2010). Field Crops Usual Planting and Harvesting Dates. Agricultural Handbook 628.
  https://esmis.nal.usda.gov/publication/usual-planting-and-harvesting-dates-us-field-crops/2010-10-29
- México: SADER Baja California (trigo OI y algodón PV en Mexicali; hortalizas en la zona costa), Gobierno de
  Sinaloa CEIEG (OI es el ciclo principal: maíz, frijol, garbanzo), SADER/Gobierno de Sonora (trigo OI y
  reconversión a cártamo y canola en OI 2025-26), SADER Guanajuato (sorgo PV; trigo y cebada OI en el Bajío).
- Canadá: Saskatchewan Ministry of Agriculture, Crop Report semanal (siembra de mayo: trigo, cebada, canola,
  leguminosas).
"""

from __future__ import annotations

import asyncio
import statistics
import sys
from dataclasses import dataclass, field
from datetime import date
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from app.schemas.analysis import AnalysisRequest  # noqa: E402
from app.services import climate as climate_service  # noqa: E402
from app.services import crops as crops_service  # noqa: E402
from app.services import recommender  # noqa: E402

HOY = date(2026, 11, 15)
SALIDA = Path(__file__).resolve().parent / "validacion_resultados.md"
MES = recommender.MONTH_ABBR
NORTE = {"spring": "primavera", "summer": "verano", "autumn": "otoño", "winter": "invierno"}


@dataclass
class Esperado:
    crop: str
    seasons: tuple[str, ...]  # temporadas en que se siembra (cualquiera vale)
    window: tuple[int, int]  # meses oficiales de siembra (inicio, fin)
    source: str


@dataclass
class Sitio:
    name: str
    lat: float
    lon: float
    country: str
    expected: list[Esperado] = field(default_factory=list)
    # (cultivo, temporadas) que NO se siembran ahí por clima; "*" = ningún cultivo (debe salir barbecho)
    not_grown: list[tuple[str, tuple[str, ...], str]] = field(default_factory=list)
    main_crop: str = "maize"
    irrigated: bool = False


USDA = "USDA NASS 2010, Usual Planting Dates"
SITIOS = [
    Sitio("Iowa (Ames)", 42.03, -93.62, "US", [
        Esperado("maize", ("spring",), (4, 5), f"{USDA}: maíz, 25 abr – 18 may"),
        Esperado("soy", ("spring", "summer"), (5, 6), f"{USDA}: soya, 8 may – 2 jun"),
        Esperado("oat", ("spring",), (4, 5), f"{USDA}: avena de primavera, 2 abr – 2 may"),
    ], [("*", ("winter",), "Sin cultivos en invierno (USDA: siembras de abr a jun)"),
        ("cotton", ("spring", "summer", "autumn", "winter"), "USDA: algodón solo al sur de ~36° N")],
        main_crop="maize"),
    Sitio("Dakota del Norte (Jamestown)", 46.90, -98.70, "US", [
        Esperado("wheat", ("spring",), (4, 5), f"{USDA}: trigo de primavera, 24 abr – 25 may"),
        Esperado("barley", ("spring",), (4, 5), f"{USDA}: cebada de primavera, 26 abr – 25 may"),
        Esperado("maize", ("spring",), (5, 5), f"{USDA}: maíz, 2 – 28 may"),
        Esperado("soy", ("spring",), (5, 6), f"{USDA}: soya, 14 may – 3 jun"),
    ], [("*", ("winter",), "Sin cultivos en invierno"),
        ("cotton", ("spring", "summer", "autumn", "winter"), "USDA: algodón solo al sur de ~36° N")],
        main_crop="wheat"),
    Sitio("Kansas (Salina)", 38.84, -97.61, "US", [
        Esperado("wheat", ("autumn",), (9, 10), f"{USDA}: trigo de invierno, 15 sep – 20 oct"),
        Esperado("sorghum", ("spring", "summer"), (5, 6), f"{USDA}: sorgo, 15 may – 20 jun"),
        Esperado("maize", ("spring",), (4, 5), f"{USDA}: maíz, 15 abr – 15 may"),
        Esperado("soy", ("spring", "summer"), (5, 6), f"{USDA}: soya, 15 may – 20 jun"),
    ], main_crop="wheat"),
    Sitio("Arizona (Maricopa)", 33.07, -111.97, "US", [
        Esperado("wheat", ("winter",), (12, 12), f"{USDA}: trigo duro e invernal, 1 – 30 dic"),
        Esperado("barley", ("winter",), (12, 12), f"{USDA}: cebada de otoño, 1 – 30 dic"),
        Esperado("cotton", ("spring",), (4, 4), f"{USDA}: algodón, 1 – 30 abr"),
        Esperado("maize", ("spring",), (4, 5), f"{USDA}: maíz, 1 abr – 15 may"),
    ], main_crop="cotton", irrigated=True),
    Sitio("California (Fresno)", 36.75, -119.77, "US", [
        Esperado("cotton", ("spring",), (4, 5), f"{USDA}: algodón, 10 abr – 5 may"),
        Esperado("wheat", ("autumn", "winter"), (10, 12), f"{USDA}: trigo invernal, 20 oct – 1 ene"),
        Esperado("maize", ("spring", "summer"), (4, 7), f"{USDA}: maíz, 1 abr – 1 jul"),
    ], main_crop="cotton", irrigated=True),
    Sitio("Valle de Mexicali (BC)", 32.55, -115.35, "MX", [
        Esperado("wheat", ("autumn", "winter"), (11, 12), "SADER BC: trigo otoño-invierno (~38 000 ha, 2022-23)"),
        Esperado("cotton", ("spring",), (3, 4), "SADER BC: algodón primavera-verano"),
    ], main_crop="wheat", irrigated=True),
    Sitio("San Quintín (BC)", 30.55, -115.95, "MX", [
        Esperado("tomato", ("spring", "summer"), (3, 7), "SADER BC: hortalizas de la zona costa (jitomate)"),
    ], main_crop="tomato", irrigated=True),
    Sitio("Valle del Yaqui (Son.)", 27.37, -109.93, "MX", [
        Esperado("wheat", ("autumn", "winter"), (11, 12), "SADER/Sonora: trigo otoño-invierno"),
        Esperado("safflower", ("autumn", "winter"), (11, 1), "SADER/Sonora: reconversión OI 2025-26 a cártamo"),
        Esperado("canola", ("autumn", "winter"), (11, 1), "SADER/Sonora: reconversión OI 2025-26 a canola"),
    ], main_crop="wheat", irrigated=True),
    Sitio("Culiacán (Sin.)", 24.80, -107.40, "MX", [
        Esperado("maize", ("autumn", "winter"), (11, 12), "CEIEG Sinaloa: OI es el ciclo principal (maíz)"),
        Esperado("bean", ("autumn", "winter"), (10, 12), "CEIEG Sinaloa: frijol OI"),
        Esperado("chickpea", ("autumn", "winter"), (11, 12), "CEIEG Sinaloa: garbanzo OI"),
    ], main_crop="maize", irrigated=True),
    Sitio("Bajío (Celaya, Gto.)", 20.52, -100.81, "MX", [
        Esperado("sorghum", ("spring", "summer"), (5, 7), "SADER Guanajuato: sorgo PV (~128 000 ha en 2025)"),
        Esperado("wheat", ("autumn", "winter"), (11, 1), "Guanajuato: trigo OI de riego"),
        Esperado("barley", ("autumn", "winter"), (11, 1), "Guanajuato: cebada OI de riego"),
    ], main_crop="sorghum", irrigated=True),
    Sitio("Saskatchewan (Saskatoon)", 52.13, -106.67, "CA", [
        Esperado("wheat", ("spring",), (5, 5), "Saskatchewan Crop Report (mayo 2026): trigo de primavera"),
        Esperado("barley", ("spring",), (5, 5), "Saskatchewan Crop Report: cebada"),
        Esperado("canola", ("spring",), (5, 5), "Saskatchewan Crop Report: canola"),
        Esperado("pea", ("spring",), (4, 5), "Saskatchewan Crop Report: leguminosas (las primeras en sembrarse)"),
    ], [("*", ("winter",), "Sin cultivos en invierno"),
        ("cotton", ("spring", "summer", "autumn", "winter"), "Sin algodón en las praderas canadienses")],
        main_crop="wheat"),
]


def mes_cerca(window_engine: tuple[int, int], oficial: tuple[int, int]) -> bool:
    """¿Algún mes de la ventana del motor está dentro de la oficial o a un mes de distancia (circular)?"""
    def meses(a: int, b: int) -> set[int]:
        out, m = {a}, a
        while m != b:
            m = m % 12 + 1
            out.add(m)
        return out
    oficiales = meses(*oficial)
    cerca = oficiales | {(m - 2) % 12 + 1 for m in oficiales} | {m % 12 + 1 for m in oficiales}
    return bool(meses(*window_engine) & cerca)


def season_climates(clima: climate_service.ClimateData) -> dict[str, recommender.SeasonClimate]:
    return {s: recommender.season_climate(s, clima) for s in recommender.SEASON_ORDER}


def evaluar(climas: dict, catalogo: dict) -> dict:
    """Viabilidad, fechas, especificidad y barbecho con los parámetros actuales del motor."""
    filas, viab, fecha, espec, barb = [], [], [], [], []
    for sitio in SITIOS:
        scs = season_climates(climas[sitio.name])
        for e in sitio.expected:
            mejores = [(s, recommender.cycle_for(catalogo[e.crop], scs[s])) for s in e.seasons]
            s, cyc = max(mejores, key=lambda x: x[1].temp_f)
            ok = cyc.temp_f > 0
            en_fecha = ok and mes_cerca(cyc.window, e.window)
            viab.append(ok)
            if ok:
                fecha.append(en_fecha)
            filas.append((sitio.name, catalogo[e.crop].name, NORTE[s], ok, cyc.temp_f,
                          recommender.planting_window(cyc) if ok else "—",
                          f"{MES[e.window[0] - 1]}–{MES[e.window[1] - 1]}", en_fecha, e.source))
        for crop_id, seasons, fuente in sitio.not_grown:
            ids = list(catalogo) if crop_id == "*" else [crop_id]
            for s in seasons:
                viables = [i for i in ids if recommender.cycle_for(catalogo[i], scs[s]).temp_f > 0]
                if crop_id == "*":
                    barb.append((sitio.name, NORTE[s], not viables, viables, fuente))
                else:
                    espec.append((sitio.name, catalogo[crop_id].name, NORTE[s], not viables, fuente))
    return {"filas": filas, "viab": viab, "fecha": fecha, "espec": espec, "barb": barb}


def pct(xs: list[bool]) -> str:
    return f"{100 * sum(xs) / len(xs):.0f} % ({sum(xs)}/{len(xs)})" if xs else "—"


# ---------------------------------------------------------------- sensibilidad de los parámetros de diseño

PESOS = ("W_TEMP", "W_WATER", "W_SOIL", "W_PRIORITY")
CASTIGOS = {"SAME_FAMILY_PENALTY": 0.15, "OUT_OF_SEASON_PENALTY": 0.05, "SYSTEM_CHANGE_PENALTY": 0.10}


def rotaciones(climas: dict, catalogo_lista: list, areas: dict) -> list[str]:
    """Cultivo de cada paso de la rotación para cada sitio × prioridad (con la fecha HOY fija)."""
    out = []
    for sitio in SITIOS:
        for prioridad in recommender.PRIORITIES:
            req = AnalysisRequest.model_validate({
                "geometry": {"type": "Polygon", "coordinates": [[[sitio.lon - .01, sitio.lat - .01],
                                                                 [sitio.lon + .01, sitio.lat - .01],
                                                                 [sitio.lon + .01, sitio.lat + .01],
                                                                 [sitio.lon - .01, sitio.lat - .01]]]},
                "currentCrop": sitio.main_crop, "priority": prioridad, "irrigated": sitio.irrigated})
            r = recommender.recommend(climas[sitio.name], catalogo_lista, req, HOY,
                                      country_areas=areas.get(sitio.country))
            out.extend(f"{sitio.name}|{prioridad}|{i}|{p.crop_id}" for i, p in enumerate(r.rotation))
    return out


def sensibilidad(climas: dict, catalogo_lista: list, areas: dict) -> list[tuple[str, str, float]]:
    base = rotaciones(climas, catalogo_lista, areas)
    originales = {k: getattr(recommender, k) for k in (*PESOS, *CASTIGOS)}
    resultados = []

    def comparar(etiqueta: str, valor: str) -> None:
        nuevo = rotaciones(climas, catalogo_lista, areas)
        iguales = sum(a == b for a, b in zip(base, nuevo)) / len(base)
        resultados.append((etiqueta, valor, iguales))

    for peso in PESOS:
        for factor in (0.5, 1.5):
            cambiados = {k: originales[k] * (factor if k == peso else 1) for k in PESOS}
            total = sum(cambiados.values())
            for k, v in cambiados.items():
                setattr(recommender, k, v / total)  # se renormaliza para que sumen 1
            comparar(peso, f"×{factor}")
            for k in PESOS:
                setattr(recommender, k, originales[k])
    for castigo, delta in CASTIGOS.items():
        for signo in (-1, 1):
            setattr(recommender, castigo, min(1.0, originales[castigo] + signo * delta))
            comparar(castigo, f"{originales[castigo]:.2f} → {getattr(recommender, castigo):.2f}")
            setattr(recommender, castigo, originales[castigo])
    return resultados


# ---------------------------------------------------------------- principal


async def descargar() -> dict:
    climas = {}
    for sitio in SITIOS:
        print(f"NASA POWER: {sitio.name} …", flush=True)
        climas[sitio.name] = await climate_service.get_climate(sitio.lat, sitio.lon, today=HOY)
    return climas


def main() -> None:
    climas = asyncio.run(descargar())
    catalogo_lista = crops_service.load_catalog_file()
    catalogo = {c.id: c for c in catalogo_lista}
    areas = {p: crops_service.load_country_areas(p) for p in ("MX", "US", "CA")}

    margen_original = recommender.KILL_MARGIN_C
    calibracion = []
    for margen in (0.0, 2.5, 5.0):  # 5 = dismo::ecocrop
        recommender.KILL_MARGIN_C = margen
        r = evaluar(climas, catalogo)
        calibracion.append((margen, r))
    recommender.KILL_MARGIN_C = margen_original
    final = next(r for m, r in calibracion if m == margen_original)
    sens = sensibilidad(climas, catalogo_lista, areas)

    lineas = [
        "# Resultados de la validación del motor",
        "",
        f"Generado por `research/validar_motor.py` con clima real de NASA POWER (consulta del {HOY:%d/%m/%Y}). "
        "No editar a mano: volver a correr el script.",
        "",
        "## 1. Calibración del margen de helada letal de EcoCrop",
        "",
        "| Margen (°C) | Viables (cultivos reales) | Siembra en la ventana oficial | Descarta lo que no se siembra "
        "| Barbecho donde corresponde |",
        "|---|---|---|---|---|",
    ]
    for margen, r in calibracion:
        lineas.append(f"| {margen:g}{' ← usado' if margen == margen_original else ''} | {pct(r['viab'])} | "
                      f"{pct(r['fecha'])} | {pct([e[3] for e in r['espec']])} | {pct([b[2] for b in r['barb']])} |")
    lineas += [
        "",
        f"## 2. Cultivos que de verdad se siembran (margen = {margen_original:g} °C)",
        "",
        "| Lugar | Cultivo | Temporada | ¿Viable? | Aptitud | Siembra (motor) | Siembra (oficial) | ¿Coincide? | Fuente |",
        "|---|---|---|---|---|---|---|---|---|",
    ]
    for (lugar, cultivo, temp, ok, apt, ventana, oficial, en_fecha, fuente) in final["filas"]:
        lineas.append(f"| {lugar} | {cultivo} | {temp} | {'✅' if ok else '❌'} | {apt:.2f} | {ventana} | {oficial} | "
                      f"{'✅' if en_fecha else ('—' if not ok else '⚠️')} | {fuente} |")
    lineas += ["", "## 3. Lo que NO se siembra por clima", "",
               "| Lugar | Cultivo | Temporada | ¿Lo descarta? | Fuente |", "|---|---|---|---|---|"]
    for (lugar, cultivo, temp, ok, fuente) in final["espec"]:
        lineas.append(f"| {lugar} | {cultivo} | {temp} | {'✅' if ok else '❌'} | {fuente} |")
    lineas += ["", "## 4. Barbecho en inviernos sin agricultura", "",
               "| Lugar | Temporada | ¿Propone barbecho? | Cultivos que aún ve viables | Fuente |",
               "|---|---|---|---|---|"]
    for (lugar, temp, ok, viables, fuente) in final["barb"]:
        lineas.append(f"| {lugar} | {temp} | {'✅' if ok else '❌'} | {', '.join(viables) or '—'} | {fuente} |")
    lineas += ["", "## 5. Sensibilidad de los parámetros de diseño", "",
               f"Rotaciones comparadas: {len(SITIOS)} lugares × 3 prioridades × 3 temporadas. "
               "Se mueve un parámetro a la vez (los pesos se renormalizan para sumar 1).", "",
               "| Parámetro | Cambio | Pasos de la rotación que NO cambian |", "|---|---|---|"]
    for etiqueta, valor, iguales in sens:
        lineas.append(f"| `{etiqueta}` | {valor} | {iguales * 100:.0f} % |")
    lineas.append(f"\nPromedio: **{statistics.mean(i for _, _, i in sens) * 100:.0f} %** de los pasos se mantienen.")
    SALIDA.write_text("\n".join(lineas) + "\n", encoding="utf-8")
    print("\n".join(lineas))


if __name__ == "__main__":
    main()
