"""Cliente de NASA POWER y cálculos de climate.py, sin internet (httpx.MockTransport simula a la NASA)."""

import asyncio
from datetime import date, timedelta

import httpx
import pytest

from app.services import climate as climate_service
from app.services import nasa_power
from app.services.nasa_power import NasaUnavailableError


def respuesta(parameter: dict) -> dict:
    return {"properties": {"parameter": parameter}, "header": {"fill_value": -999.0}}


def correr(handler, coro_factory):
    """Ejecuta una corrutina con un cliente httpx que responde con `handler` en vez de ir a internet."""
    async def run():
        async with httpx.AsyncClient(transport=httpx.MockTransport(handler)) as client:
            return await coro_factory(client)
    return asyncio.run(run())


@pytest.fixture
def sin_espera(monkeypatch):
    """Los reintentos esperan 0.5 s y 1 s; en pruebas no esperamos."""
    async def no_sleep(_seconds):
        return None
    monkeypatch.setattr(nasa_power.asyncio, "sleep", no_sleep)


def test_parse_descarta_los_menos_999():
    serie = nasa_power.parse_response(respuesta({"T2M": {"202401": 15.0, "202402": -999.0}}))
    assert serie == {"T2M": {"202401": 15.0}}


def test_parse_respuesta_sin_datos_falla():
    with pytest.raises(NasaUnavailableError):
        nasa_power.parse_response({"messages": ["error"]})


def test_reintenta_si_nasa_falla_y_luego_responde(sin_espera):
    llamadas = []

    def handler(request: httpx.Request) -> httpx.Response:
        llamadas.append(request)
        if len(llamadas) == 1:
            return httpx.Response(503)
        return httpx.Response(200, json=respuesta({"T2M": {"20261101": 20.0}}))

    dia = date(2026, 11, 1)
    serie = correr(handler, lambda c: nasa_power.fetch_daily(31.5, -116.5, dia, dia, c))
    assert serie["T2M"]["20261101"] == 20.0
    assert len(llamadas) == 2
    q = llamadas[0].url.params
    assert q["community"] == "AG" and q["start"] == "20261101" and "GWETROOT" in q["parameters"]


def test_se_rinde_despues_de_los_reintentos(sin_espera):
    llamadas = []

    def handler(request):
        llamadas.append(request)
        return httpx.Response(500)

    with pytest.raises(NasaUnavailableError):
        correr(handler, lambda c: nasa_power.fetch_monthly(31.5, -116.5, 2016, 2025, c))
    assert len(llamadas) == nasa_power.RETRIES + 1


def test_error_4xx_no_se_reintenta():
    llamadas = []

    def handler(request):
        llamadas.append(request)
        return httpx.Response(422, json={"detail": "bad"})

    with pytest.raises(NasaUnavailableError):
        correr(handler, lambda c: nasa_power.fetch_monthly(31.5, -116.5, 2016, 2025, c))
    assert len(llamadas) == 1


# ---------------------------------------------------------------- climate.py (cálculos)


def serie_mensual(rain_by_year: dict[int, float]) -> dict:
    """Lluvia constante por año (mm/día) y el resto de variables fijas."""
    params: dict = {p: {} for p in nasa_power.PARAMETERS}
    for year, rain in rain_by_year.items():
        for m in range(1, 13):
            k = f"{year}{m:02d}"
            params["T2M"][k] = 10.0 + m
            params["T2M_MAX"][k] = 20.0 + m
            params["T2M_MIN"][k] = 0.0 + m
            params["PRECTOTCORR"][k] = rain
            params["GWETROOT"][k] = 0.4
            params["ALLSKY_SFC_SW_DWN"][k] = 18.0  # MJ/m²/día
        params["T2M"][f"{year}13"] = 99.0  # promedio anual de POWER: se ignora
    return params


def test_resumen_convierte_unidades_y_calcula_variabilidad():
    s = climate_service.build_summary(serie_mensual({2024: 1.0, 2025: 2.0}), 31.5, -116.5, 2024, 2025)
    enero = s.monthly[0]
    assert enero.temp_c == 11.0  # el "mes 13" no se mezcla
    assert enero.rain_mm == pytest.approx((31 * 1 + 31 * 2) / 2)  # mm/día × días del mes
    assert s.monthly[1].rain_mm == pytest.approx((29 * 1 + 28 * 2) / 2)  # 2024 es bisiesto
    assert enero.solar_radiation == pytest.approx(5.0)  # 18 MJ ÷ 3.6 = 5 kWh
    assert s.rain_annual_mm == pytest.approx((366 + 365 * 2) / 2, abs=0.1)
    assert s.rain_cv_pct > 40
    assert s.period == "2024-2025"


def test_resumen_con_meses_faltantes_falla():
    serie = serie_mensual({2025: 1.0})
    del serie["T2M"]["202503"]
    with pytest.raises(NasaUnavailableError):
        climate_service.build_summary(serie, 31.5, -116.5, 2025, 2025)


def test_reciente_compara_contra_lo_normal():
    mensual = serie_mensual({2024: 1.0, 2025: 1.0})
    s = climate_service.build_summary(mensual, 31.5, -116.5, 2024, 2025)
    inicio, fin = date(2026, 1, 1), date(2026, 3, 31)  # 90 días
    diaria: dict = {"PRECTOTCORR": {}, "T2M": {}, "GWETROOT": {}}
    d = inicio
    while d <= fin:
        k = d.strftime("%Y%m%d")
        diaria["PRECTOTCORR"][k] = 0.5  # la mitad de lo normal
        diaria["T2M"][k] = 15.0
        diaria["GWETROOT"][k] = 0.2
        d += timedelta(days=1)
    r = climate_service.build_recent(diaria, mensual, s, inicio, fin)
    assert r.rain_90d_mm == pytest.approx(45.0)
    assert r.rain_90d_normal_mm == pytest.approx(90.0)
    assert r.temp_30d_c == 15.0
    assert r.temp_30d_normal_c == pytest.approx(13.0)  # marzo = 10 + 3
    assert r.soil_moisture_30d == 0.2


def test_malla_y_periodo():
    assert climate_service.snap_to_grid(31.86, -116.6) == (32.0, -116.875)
    assert climate_service.snap_to_grid(-33.44, -70.66) == (-33.5, -70.625)
    assert climate_service.snap_to_grid(0.1, 179.9) == (0.0, -180.0)
    assert climate_service.climate_period(date(2026, 11, 14)) == (2016, 2025)


def test_cache_evita_volver_a_llamar_a_nasa(monkeypatch):
    llamadas = []

    async def falso_monthly(lat, lon, start, end, client=None):
        llamadas.append((lat, lon))
        return serie_mensual({y: 1.0 for y in range(start, end + 1)})

    monkeypatch.setattr(nasa_power, "fetch_monthly", falso_monthly)
    hoy = date(2026, 11, 14)
    asyncio.run(climate_service.get_climate_summary(31.86, -116.6, today=hoy))
    asyncio.run(climate_service.get_climate_summary(31.9, -116.7, today=hoy))  # misma celda
    assert llamadas == [(32.0, -116.875)]
