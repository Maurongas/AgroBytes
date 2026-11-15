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


def test_parse_guarda_la_altitud_de_la_celda():
    payload = {**respuesta({"T2M": {"202401": 15.0}}),
               "geometry": {"type": "Point", "coordinates": [-115.0, 32.5, 42.36]}}
    serie = nasa_power.parse_response(payload)
    assert serie[nasa_power.ELEVATION_KEY] == {"m": 42.36}


def test_diario_pide_solo_lo_necesario():
    pedidos = []

    def handler(request: httpx.Request) -> httpx.Response:
        pedidos.append(request.url.params["parameters"])
        return httpx.Response(200, json=respuesta({"T2M": {"20260101": 15.0}}))

    correr(handler, lambda c: nasa_power.fetch_daily(31.5, -116.5, date(2026, 1, 1), date(2026, 1, 2), c))
    assert pedidos == [",".join(nasa_power.DAILY_PARAMETERS)]


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
            params["T2M_RANGE"][k] = 10.0  # rango diario promedio → máx. diaria = T2M + 5, mín. = T2M − 5
            params["T2MDEW"][k] = 2.0 + m
            params["WS2M"][k] = 2.0
            params["FROST_DAYS"][k] = 3.0 if m in (12, 1, 2) else 0.0
        params["T2M"][f"{year}13"] = 99.0  # promedio anual de POWER: se ignora
    params[nasa_power.ELEVATION_KEY] = {"m": 120.0}
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


def test_maxima_y_minima_diarias_salen_del_rango_no_de_los_extremos():
    """En el endpoint mensual de POWER, T2M_MAX/T2M_MIN son los extremos del mes (mayo 2024 en Iowa: 28.96 y
    5.63 °C, cuando las diarias promediaron 23.6 y 11.1 °C). La media diaria sale de T2M ± T2M_RANGE/2."""
    s = climate_service.build_summary(serie_mensual({2024: 1.0, 2025: 2.0}), 31.5, -116.5, 2024, 2025)
    enero = s.monthly[0]  # T2M 11, extremos 21 y 1, rango diario 10
    assert (enero.temp_max_c, enero.temp_min_c) == (16.0, 6.0)
    assert (enero.temp_max_abs_c, enero.temp_min_abs_c) == (21.0, 1.0)


def test_resumen_trae_rocio_viento_heladas_y_altitud():
    s = climate_service.build_summary(serie_mensual({2024: 1.0, 2025: 2.0}), 31.5, -116.5, 2024, 2025)
    enero = s.monthly[0]
    assert (enero.dewpoint_c, enero.wind_ms, enero.frost_days) == (3.0, 2.0, 3.0)
    assert s.monthly[5].frost_days == 0.0
    assert s.elevation_m == 120.0


def test_resumen_sin_variables_nuevas_las_deja_en_none():
    serie = serie_mensual({2024: 1.0, 2025: 1.0})
    for p in nasa_power.OPTIONAL_PARAMETERS:
        serie[p] = {}
    s = climate_service.build_summary(serie, 31.5, -116.5, 2024, 2025)
    assert s.monthly[0].dewpoint_c is None and s.monthly[0].wind_ms is None and s.monthly[0].frost_days is None
    assert not climate_service.has_all_parameters(serie)


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
    # Variabilidad normal entre años: en la serie de prueba los dos años son idénticos → desviación 0
    assert r.soil_moisture_30d_normal == pytest.approx(0.4)
    assert r.temp_30d_sd_c == 0.0
    assert r.soil_moisture_30d_percentile is None  # con menos de 5 años no se calcula percentil
    assert r.recent_model_change is None  # la serie de prueba no dice de qué modelo viene


def test_percentil_de_la_humedad_frente_a_10_anios():
    mensual = serie_mensual({y: 1.0 for y in range(2016, 2026)})
    for i, y in enumerate(range(2016, 2026)):  # marzo de cada año: 0.30, 0.31, … 0.39
        mensual["GWETROOT"][f"{y}03"] = 0.30 + i / 100
    dias = [date(2026, 3, d) for d in range(1, 31)]
    assert climate_service.window_percentile(mensual, "GWETROOT", 2016, 2025, dias, 0.25) == 0.0
    assert climate_service.window_percentile(mensual, "GWETROOT", 2016, 2025, dias, 0.345) == 50.0
    assert climate_service.window_percentile(mensual, "GWETROOT", 2016, 2025, dias, 0.50) == 100.0


def test_dias_recientes_de_otro_modelo_se_marcan():
    mensual = serie_mensual({2024: 1.0, 2025: 1.0})
    s = climate_service.build_summary(mensual, 31.5, -116.5, 2024, 2025)
    inicio, fin = date(2026, 1, 1), date(2026, 3, 31)
    diaria: dict = {"PRECTOTCORR": {}, "T2M": {}, "GWETROOT": {}, nasa_power.SOURCES_KEY: {"GEOSIT": 1.0}}
    d = inicio
    while d <= fin:
        k = d.strftime("%Y%m%d")
        diaria["PRECTOTCORR"][k], diaria["T2M"][k], diaria["GWETROOT"][k] = 1.0, 13.0, 0.4
        d += timedelta(days=1)
    assert climate_service.build_recent(diaria, mensual, s, inicio, fin).recent_model_change == "GEOSIT"


def test_parse_guarda_los_modelos_de_origen():
    payload = {**respuesta({"T2M": {"20261001": 20.0}}), "header": {"fill_value": -999.0, "sources": ["GEOSIT"]}}
    assert nasa_power.parse_response(payload)[nasa_power.SOURCES_KEY] == {"GEOSIT": 1.0}


def test_variabilidad_mensual_entre_anios():
    mensual = serie_mensual({2024: 1.0, 2025: 1.0})
    mensual["T2M"]["202401"], mensual["T2M"]["202501"] = 10.0, 14.0
    spread = climate_service.monthly_spread(mensual, "T2M", 2024, 2025)
    assert spread[1][0] == pytest.approx(12.0)
    assert spread[1][1] == pytest.approx(2.828, abs=0.01)  # desviación estándar muestral de (10, 14)


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


# ---------------------------------------------------------------- caché en la tabla climate_cache (repo falso)


class SesionFalsa:
    def rollback(self):
        pass


@pytest.fixture
def tabla_falsa(monkeypatch):
    """Reemplaza repositories.climate_cache por un dict {(lat_g, lon_g, period): payload}."""
    from types import SimpleNamespace

    from app.repositories import climate_cache as cache_repo

    tabla: dict = {}
    vencidos: set = set()

    def get_valid(db, lat_g, lon_g, period, max_days=None):
        key = (lat_g, lon_g, period)
        if key not in tabla or (key in vencidos and (max_days or 0) < 3650):
            return None
        return SimpleNamespace(payload=tabla[key])

    def upsert(db, lat_g, lon_g, period, payload):
        tabla[(lat_g, lon_g, period)] = payload
        vencidos.discard((lat_g, lon_g, period))

    monkeypatch.setattr(cache_repo, "get_valid", get_valid)
    monkeypatch.setattr(cache_repo, "upsert", upsert)
    return SimpleNamespace(tabla=tabla, vencidos=vencidos)


def test_cache_de_bd_sobrevive_reinicio(monkeypatch, tabla_falsa):
    llamadas = []

    async def falso_monthly(lat, lon, start, end, client=None):
        llamadas.append((lat, lon))
        return serie_mensual({y: 1.0 for y in range(start, end + 1)})

    monkeypatch.setattr(nasa_power, "fetch_monthly", falso_monthly)
    hoy, db = date(2026, 11, 14), SesionFalsa()
    primero = asyncio.run(climate_service.get_climate_summary(31.86, -116.6, today=hoy, db=db))
    # Se guarda con la malla de POWER (0.5° × 0.625°), no con la de 0.5° × 0.5°
    assert list(tabla_falsa.tabla) == [(32.0, -116.875, "2016-2025")]

    climate_service._long_term_cache.clear()  # simula reiniciar el backend
    segundo = asyncio.run(climate_service.get_climate_summary(31.86, -116.6, today=hoy, db=db))
    assert llamadas == [(32.0, -116.875)]  # la segunda vez salió de la tabla
    assert segundo == primero


def test_nasa_caida_usa_cache_vencida(monkeypatch, tabla_falsa):
    async def bien(lat, lon, start, end, client=None):
        return serie_mensual({y: 1.0 for y in range(start, end + 1)})

    async def caida(*args, **kwargs):
        raise NasaUnavailableError("caído")

    hoy, db = date(2026, 11, 14), SesionFalsa()
    monkeypatch.setattr(nasa_power, "fetch_monthly", bien)
    guardado = asyncio.run(climate_service.get_climate_summary(31.86, -116.6, today=hoy, db=db))

    climate_service._long_term_cache.clear()
    tabla_falsa.vencidos.add((32.0, -116.875, "2016-2025"))
    monkeypatch.setattr(nasa_power, "fetch_monthly", caida)
    assert asyncio.run(climate_service.get_climate_summary(31.86, -116.6, today=hoy, db=db)) == guardado

    # Sin nada guardado, NASA caída sí es un error
    with pytest.raises(NasaUnavailableError):
        asyncio.run(climate_service.get_climate_summary(10.0, 10.0, today=hoy, db=db))


def test_registro_viejo_sin_variables_nuevas_se_vuelve_a_pedir(monkeypatch, tabla_falsa):
    """Un registro guardado antes de pedir rocío/viento/heladas no sirve para Penman-Monteith: si NASA responde,
    se descarga de nuevo; si NASA está caída, se usa igual (mejor un dato viejo que un 503)."""
    viejo = serie_mensual({y: 1.0 for y in range(2016, 2026)})
    for p in nasa_power.OPTIONAL_PARAMETERS:
        viejo[p] = {}
    resumen_viejo = climate_service.build_summary(viejo, 32.0, -116.875, 2016, 2025)
    tabla_falsa.tabla[(32.0, -116.875, "2016-2025")] = {"summary": resumen_viejo.model_dump(mode="json"),
                                                        "monthly": viejo}
    llamadas = []

    async def bien(lat, lon, start, end, client=None):
        llamadas.append((lat, lon))
        return serie_mensual({y: 1.0 for y in range(start, end + 1)})

    hoy, db = date(2026, 11, 14), SesionFalsa()
    monkeypatch.setattr(nasa_power, "fetch_monthly", bien)
    nuevo = asyncio.run(climate_service.get_climate_summary(31.86, -116.6, today=hoy, db=db))
    assert llamadas == [(32.0, -116.875)] and nuevo.monthly[0].dewpoint_c is not None

    async def caida(*args, **kwargs):
        raise NasaUnavailableError("caído")

    climate_service._long_term_cache.clear()
    tabla_falsa.tabla[(32.0, -116.875, "2016-2025")] = {"summary": resumen_viejo.model_dump(mode="json"),
                                                        "monthly": viejo}
    monkeypatch.setattr(nasa_power, "fetch_monthly", caida)
    assert asyncio.run(climate_service.get_climate_summary(31.86, -116.6, today=hoy, db=db)) == resumen_viejo


def test_bd_caida_no_tumba_el_clima(monkeypatch):
    from sqlalchemy.exc import OperationalError

    from app.repositories import climate_cache as cache_repo

    def explota(*args, **kwargs):
        raise OperationalError("SELECT", {}, Exception("sin conexión"))

    async def bien(lat, lon, start, end, client=None):
        return serie_mensual({y: 1.0 for y in range(start, end + 1)})

    monkeypatch.setattr(cache_repo, "get_valid", explota)
    monkeypatch.setattr(cache_repo, "upsert", explota)
    monkeypatch.setattr(nasa_power, "fetch_monthly", bien)
    s = asyncio.run(climate_service.get_climate_summary(31.86, -116.6, today=date(2026, 11, 14), db=SesionFalsa()))
    assert s.period == "2016-2025"


# ---------------------------------------------------------------- plan B: NASA no da los datos diarios


def test_sin_datos_diarios_usa_lo_normal_como_reciente(monkeypatch):
    llamadas = []

    async def falso_monthly(lat, lon, start, end, client=None):
        llamadas.append("mensual")
        return serie_mensual({y: 1.0 for y in range(start, end + 1)})

    async def daily_caido(lat, lon, start, end, client=None):
        raise NasaUnavailableError("NASA POWER no disponible")

    monkeypatch.setattr(nasa_power, "fetch_monthly", falso_monthly)
    monkeypatch.setattr(nasa_power, "fetch_daily", daily_caido)
    datos = asyncio.run(climate_service.get_climate(31.86, -116.6, today=date(2026, 11, 14)))
    r = datos.recent
    assert r.estimated is True  # el motor lo etiqueta como promedio, no como dato medido
    assert r.rain_90d_mm == r.rain_90d_normal_mm == pytest.approx(90.0)  # 1 mm/día × 90 días
    assert r.temp_30d_c == r.temp_30d_normal_c
    assert r.soil_moisture_30d == 0.4
    assert climate_service._recent_cache.get((32.0, -116.875, r.end)) is None  # el plan B no se guarda
    assert llamadas == ["mensual"]  # si falla lo diario, la serie mensual no se vuelve a descargar


def test_sin_datos_diarios_ni_largo_plazo_sigue_fallando(monkeypatch):
    async def caido(lat, lon, start, end, client=None):
        raise NasaUnavailableError("NASA POWER no disponible")

    monkeypatch.setattr(nasa_power, "fetch_monthly", caido)
    monkeypatch.setattr(nasa_power, "fetch_daily", caido)
    with pytest.raises(NasaUnavailableError):
        asyncio.run(climate_service.get_climate(31.86, -116.6, today=date(2026, 11, 14)))
