"""Suelo por coordenadas (ISRIC SoilGrids), sin internet."""

import asyncio

import httpx
import pytest

from app.services import soil


def capa(nombre: str, valores: list[float | None]) -> dict:
    etiquetas = ["0-5cm", "5-15cm", "15-30cm"]
    return {"name": nombre, "depths": [{"label": e, "values": {"mean": v}} for e, v in zip(etiquetas, valores)]}


def test_textura_simplificada():
    assert soil.texture_class(40, 30) == "clay"
    assert soil.texture_class(8, 80) == "sandy"
    assert soil.texture_class(19, 58) == "loam"  # franco-arenoso → "loam"


def test_parse_soilgrids_mexicali():
    payload = {"properties": {"layers": [capa("clay", [401, 397, 397]), capa("sand", [295, 291, 291]),
                                         capa("phh2o", [79, 79, 79])]}}
    s = soil.parse(payload)
    assert s.texture == "clay" and s.ph == 7.9 and s.clay_pct == pytest.approx(39.8, abs=0.2)


def test_soilgrids_sin_dato_o_caido_da_none():
    urbano = {"properties": {"layers": [capa("clay", [None] * 3), capa("sand", [None] * 3)]}}
    assert soil.parse(urbano) is None

    def caido(request):
        return httpx.Response(503)

    async def run():
        async with httpx.AsyncClient(transport=httpx.MockTransport(caido)) as c:
            return await soil.get_soil(10.123, 20.456, client=c)

    assert asyncio.run(run()) is None


def test_soilgrids_caido_no_se_reintenta_enseguida():
    llamadas = []

    def caido(request):
        llamadas.append(request)
        return httpx.Response(503)

    async def run():
        async with httpx.AsyncClient(transport=httpx.MockTransport(caido)) as c:
            await soil.get_soil(10.123, 20.456, client=c)
            return await soil.get_soil(10.124, 20.457, client=c)  # mismo punto (~1 km)

    assert asyncio.run(run()) is None
    assert len(llamadas) == 1  # el segundo análisis no vuelve a esperar el timeout


def test_dos_analisis_simultaneos_hacen_una_sola_consulta():
    """«Comparar escenarios» lanza dos análisis a la vez sobre la misma parcela."""
    llamadas = []
    payload = {"properties": {"layers": [capa("clay", [400] * 3), capa("sand", [300] * 3), capa("phh2o", [78] * 3)]}}

    async def lento(request):
        llamadas.append(request)
        await asyncio.sleep(0.05)
        return httpx.Response(200, json=payload)

    async def run():
        async with httpx.AsyncClient(transport=httpx.MockTransport(lento)) as c:
            return await asyncio.gather(soil.get_soil(32.52, -115.35, client=c),
                                        soil.get_soil(32.521, -115.351, client=c))

    a, b = asyncio.run(run())
    assert a == b and a.texture == "clay"
    assert len(llamadas) == 1
    assert soil._inflight == {}
