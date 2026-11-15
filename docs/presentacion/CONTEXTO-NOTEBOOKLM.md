# AgroBytes — contexto técnico para preparar preguntas del jurado

> Documento de estudio para el equipo (cargar en NotebookLM). Resume **qué hace** AgroBytes, **cómo funciona por
> dentro**, **de dónde sale cada número**, **qué tan validado está** y **qué preguntas técnicas** puede hacer el
> jurado, con respuestas sugeridas en español y una versión corta en inglés para decir en voz alta.
> Refleja el código de la rama `feature/back-validacion-cientifica` (noviembre de 2026). Si el código y
> `docs/ARQUITECTURA.md` no coinciden, aquí manda el código.

---

## 1. El proyecto en 30 segundos

- **Nombre:** AgroBytes (equipo de la UABC, Facultad de Ingeniería, FIAD).
- **Evento:** NASA Space Apps Challenge, reto **«Field Shift»** (cambio de campo): ayudar a los agricultores a elegir
  rotaciones de cultivos que protejan su suelo y su agua frente a un clima que cambia.
- **Qué es:** un **sistema de apoyo a la decisión (DSS)**. No decide por el agricultor: le da opciones explicadas.
- **Cómo se usa:**
  1. El agricultor **dibuja su parcela** en un mapa.
  2. Elige su **cultivo actual** y su **prioridad**: ahorrar agua, regenerar el suelo (nitrógeno) o más rendimiento.
  3. El backend descarga **10 años de clima de NASA POWER** para ese punto y el **suelo** (textura y pH) de **ISRIC
     SoilGrids**.
  4. Un **motor de reglas agronómicas** (FAO ECOCROP + FAO-56) recomienda una **rotación para las próximas 3
     temporadas** y la compara con «seguir como hoy» y con otras 2–3 estrategias.
  5. Cada opción trae **puntaje 0–100, razones, riesgos, evidencia, agua, riego, balance de nitrógeno (estimado),
     índice de salud del suelo (estimado) e incertidumbre**.
- **Frase clave:** *"NASA data in, rotation options out — for one field, in plain words."*
- **Alcance:** cualquier parcela de **México, Estados Unidos o Canadá**, de **0.1 a 500 hectáreas**.

### Lo que NO es (importante para no exagerar)
- **No es inteligencia artificial ni machine learning.** Es un motor de **reglas transparentes** con fuentes
  científicas. Cada número se puede explicar con una fórmula.
- **No procesa imágenes de satélite.** El fondo del mapa es imagen satelital de Esri, solo como referencia visual.
  Los datos de clima vienen de **NASA POWER**, que es un producto de datos (reanálisis + observaciones), no imágenes.
- **No predice el clima del próximo año.** Usa el clima típico de los últimos 10 años y lo compara con lo que pasó en
  los últimos 90 días. El «¿y si…?» es un escenario hipotético que el usuario mueve a mano.
- **No estima rendimiento (toneladas por hectárea).** No hay una fuente confiable sin un modelo de cultivo calibrado.
- **Nitrógeno y salud del suelo son estimaciones por reglas** y la app las etiqueta así.

---

## 2. Arquitectura (cómo está construido)

```
Navegador / PWA (React)  ──REST JSON──►  Backend (FastAPI, Python)  ──►  PostgreSQL + PostGIS
                                              │
                                              ├──► NASA POWER API (clima)
                                              └──► ISRIC SoilGrids API (suelo)
```

| Pieza | Tecnología | Para qué |
|---|---|---|
| Frontend | React 19, Vite 8, TypeScript 6, Tailwind 4, react-leaflet 5 (mapa), Turf (área), Zustand (estado), TanStack Query (peticiones), Recharts (gráficas), Framer Motion (animaciones), jsPDF (PDF) | Interfaz, mapa, resultados, PWA offline |
| Backend | Python 3.11, FastAPI, Pydantic v2, httpx (asíncrono) | API REST, descarga de NASA POWER y SoilGrids, motor de reglas |
| Base de datos | PostgreSQL 15 + PostGIS 3.3, SQLAlchemy 2, Alembic (migraciones), GeoAlchemy2 | Historial de análisis, catálogo de cultivos, caché de clima, cultivos por país |
| Despliegue | Docker Compose (3 contenedores: db, backend, frontend) | `docker compose up --build`; frontend :3000, API :8000/docs, BD :5432 |

**Equipo y roles:** Mauro (backend, motor de reglas, integración NASA), Daniel (base de datos), Mia (mapa),
Fernando (layout y resultados), Ximena / menaxmn (PWA, cliente API, QA). Presentan Mia y Mauro.

### Endpoints de la API
| Método | Ruta | Qué hace |
|---|---|---|
| GET | `/health` | Estado del backend y la BD |
| POST | `/api/v1/analyses` | Analiza una parcela y guarda el resultado (`?guardar=false` → no lo guarda; lo usan «Comparar» y «¿y si…?») |
| GET | `/api/v1/analyses` | Historial del dispositivo |
| GET / DELETE | `/api/v1/analyses/{id}` | Ver o borrar un análisis |
| GET | `/api/v1/climate?lat=&lon=` | Resumen de NASA POWER de un punto |
| GET | `/api/v1/crops` | Catálogo de 18 cultivos con sus fuentes |
| GET | `/api/v1/soil?lat=&lon=` | Suelo estimado (SoilGrids) |

- La documentación viva está en `/docs` (Swagger generado por FastAPI). En el pitch hay un botón **«API docs ↗»**.
- JSON en camelCase; errores siempre como `{"detail": "mensaje en español"}`.
- Códigos: 422 validación (polígono inválido, fuera de la región o del tamaño) · 404 no existe · 429 límite de
  peticiones · 503 NASA POWER caído sin caché.

### Flujo de un análisis (`POST /api/v1/analyses`)
1. Valida el polígono GeoJSON: anillo cerrado, todos los vértices en México/EE. UU./Canadá, área entre 0.1 y 500 ha.
2. Calcula **centroide y área** (proyección equirectangular local, error < 1 % para parcelas).
3. Detecta el **país** por el centroide (contornos de Natural Earth).
4. Pide el **clima**: primero caché en memoria, luego tabla `climate_cache` en PostgreSQL, y si no hay, NASA POWER
   (serie mensual de 10 años + diaria de 90 días, **en paralelo** con `asyncio.gather`).
5. Pide el **suelo** a SoilGrids si el usuario no lo dio (timeout 10 s; si falla, sigue sin suelo).
6. Corre el **motor de reglas** (función pura, sin internet ni BD).
7. Guarda el análisis (geometría PostGIS + resultado en JSONB) y responde.

### Robustez (preguntas tipo «¿y si se cae NASA?»)
- **Caché en dos niveles:** memoria (rápido) y PostgreSQL (sobrevive reinicios). Clima de largo plazo: 30 días.
  Datos recientes: 1 día. La llave del caché es la **celda de NASA POWER**, así que parcelas vecinas comparten caché.
- Si NASA POWER no responde, se usa el registro guardado **aunque esté vencido**.
- **Plan B:** si llega el clima de largo plazo pero no los datos diarios recientes, «lo reciente» se toma igual a lo
  normal, se avisa en la fuente de las métricas y la **incertidumbre sube un nivel**.
- Cliente NASA: timeout 20 s, 2 reintentos solo ante errores de red o 5xx.
- SoilGrids (API beta, ~5 consultas/min): si falla un punto, no se reintenta en 5 min; dos peticiones simultáneas al
  mismo punto comparten una sola consulta.
- **Límite de 30 análisis por IP por minuto** (429 con `Retry-After`) para cuidar las cuotas de NASA y SoilGrids.
- La primera consulta a un lugar nuevo tarda ~10 s (NASA POWER); después responde en milisegundos.

### Privacidad
- No hay cuentas ni contraseñas. El historial se separa por un **identificador anónimo de dispositivo** (UUID en el
  navegador, header `X-Device-Id`). No es autenticación.
- Se guarda la geometría de la parcela y el resultado; no se piden datos personales al servidor.

### PWA y offline
- `vite-plugin-pwa`: la app se puede **instalar** y abre sin internet.
- Precache de la interfaz; estrategia *NetworkFirst* para `/api/*`; el **último análisis** se guarda en el
  navegador (`localStorage`) para verlo en el campo sin señal.
- Los mosaicos del mapa no se guardan masivamente (términos de uso del proveedor).

### Calidad
- **148 pruebas automáticas con pytest** (motor de reglas, FAO-56, cliente NASA, API, región, suelo, repositorios).
- El motor es una **función pura**: se prueba con climas inventados y siempre da el mismo resultado con la misma
  entrada.
- Script de validación científica: `backend/research/validar_motor.py` (sección 6).

---

## 3. Fuentes de datos

### 3.1 NASA POWER (clima) — la fuente principal
- **Qué es:** *Prediction Of Worldwide Energy Resources*, servicio de NASA Langley. Datos diarios y mensuales de
  meteorología y radiación solar para cualquier punto del planeta, **gratis y sin API key**. Más de 40 años de datos.
- **Origen:** la meteorología viene del reanálisis **MERRA-2** (modelo atmosférico de NASA GMAO que asimila
  observaciones); la radiación solar viene de productos de **CERES**. Nosotros solo consumimos la API.
- **Comunidad `AG`** (agricultura): unidades pensadas para agronomía.
- **Malla:** celdas de **0.5° de latitud × 0.625° de longitud** (~55 km). El backend consulta el **centro de la
  celda** (`snap_to_grid`). Detalle técnico: redondear la longitud a 0.5° cae en otra celda; en Ensenada eso daba un
  clima de tierra adentro ~5 °C más frío en enero. Por eso se usa la malla real de MERRA-2.
- **Endpoints que usamos:**
  - **Mensual**, últimos **10 años completos** (2016–2025): clima típico de cada mes y variabilidad entre años.
  - **Diario**, últimos **90 días** hasta «hoy − 7 días» (los datos diarios llegan con unos días de retraso):
    anomalías recientes.
  - No usamos el endpoint *climatology* porque su periodo es fijo (2001–2025); queremos que el promedio y la
    variabilidad salgan del **mismo** periodo de 10 años.
- **Variables:**

| Variable | Significado | Uso |
|---|---|---|
| `T2M` | Temperatura media a 2 m (°C) | Aptitud del cultivo, métricas |
| `T2M_RANGE` | Rango diario promedio (°C) | Máxima y mínima diarias medias = T2M ± rango/2 |
| `T2M_MAX` / `T2M_MIN` | En el endpoint mensual son los **extremos** del mes, no el promedio | Solo como extremos (trampa técnica conocida) |
| `PRECTOTCORR` | Lluvia corregida (mm/día) | × días del mes = lluvia mensual |
| `GWETROOT` | Humedad del suelo en la zona de raíces (0 seco – 1 saturado) | Métrica de humedad |
| `ALLSKY_SFC_SW_DWN` | Radiación solar en superficie (MJ/m²/día → ÷ 3.6 = kWh/m²/día) | Penman-Monteith, métrica |
| `T2MDEW` | Punto de rocío (°C) | Humedad del aire para Penman-Monteith |
| `WS2M` | Viento a 2 m (m/s) | Penman-Monteith y ajuste de Kc |
| `FROST_DAYS` | Días con helada en el mes | Riesgo de helada medido |
| Altitud de la celda | En la respuesta de POWER | Presión atmosférica en Penman-Monteith |

- `-999` = sin dato (se descarta). En el endpoint mensual el «mes 13» es el promedio anual.

### 3.2 ISRIC SoilGrids v2.0 (suelo)
- Modelo global de suelos a ~**250 m**, licencia CC BY 4.0, sin API key (API en beta).
- Pedimos **arcilla, arena y pH** en 0–5, 5–15 y 15–30 cm y promediamos **0–30 cm** ponderando por grosor.
- Textura simplificada del triángulo USDA a 3 clases: **arcilloso** si arcilla ≥ 35 %; **arenoso** si arena ≥ 65 % y
  arcilla < 15 %; si no, **franco** (*loam*).
- Sin dato en ciudades y cuerpos de agua → el análisis sigue sin suelo. El usuario puede corregirlo a mano.
- Es una **estimación de modelo**: la app recomienda hacer un análisis de suelo de laboratorio.

### 3.3 FAO ECOCROP (rangos de los cultivos)
- Base de datos de la FAO con ~2 500 especies: temperatura óptima y absoluta, temperatura que mata la planta
  (`KTMP`), pH óptimo, textura de suelo, ciclo. FAO descontinuó el portal (~2015); usamos la copia pública
  `EcoCrop_DB.csv` (OpenCLIM).

### 3.4 FAO-56 y manual FAO de riego (agua)
- **FAO-56** (Allen et al., 1998), *Crop evapotranspiration*: el estándar mundial para calcular cuánta agua usa un
  cultivo. Tablas 11 (etapas) y 12 (coeficientes Kc).
- **FAO Training Manual 3** (Brouwer y Heibloem, 1986): ciclo y agua típica por cultivo (Tablas 4 y 5) y **lluvia
  efectiva** (Tabla 6).

### 3.5 FAOSTAT (qué se siembra en cada país y rendimientos)
- Área cosechada promedio **2020–2024** por país. Solo se recomiendan cultivos con **≥ 10 000 ha cosechadas al año**
  en el país (p. ej. en Canadá no se ofrece sorgo, algodón ni cártamo; en México no se ofrece canola).
- Las coberturas (veza) no se filtran porque se incorporan al suelo y no aparecen en estadísticas de cosecha.
- El rendimiento del país se usa para el balance de nitrógeno.

### 3.6 Natural Earth (fronteras)
- Contornos 1:50m de dominio público, simplificados a ~2 km; tolerancia de 0.05° (~5 km) para no rechazar parcelas
  en la costa.

### El catálogo: 18 cultivos
Maíz, sorgo, trigo, cebada, avena · frijol, soya, garbanzo, chícharo · veza (abono verde / cobertura) · canola,
cártamo · algodón · jitomate, chile, papa, cebolla, calabaza. Cubren cereales, leguminosas de verano e invierno,
oleaginosas, industriales y hortalizas en las 4 temporadas. Lo genera un script (`build_crops.py`) desde ECOCROP +
tablas FAO, con el campo `source` que cita cada fuente; **no se edita a mano**.

---

## 4. El motor de reglas, paso a paso

Archivo: `backend/app/services/recommender.py`. Es una **función pura**: recibe clima, catálogo, petición y fecha;
devuelve el resultado. No consulta internet ni la hora.

### 4.1 Temporadas
- 4 temporadas de 3 meses: primavera (mar–may), verano (jun–ago), otoño (sep–nov), invierno (dic–feb).
  En el hemisferio sur se invierten (si latitud < 0).
- La rotación es una **línea de tiempo de 12 meses** (las 4 temporadas que siguen a la actual) con **3 pasos**:
  cada cultivo se siembra **después de cosechar el anterior**, en la primera temporada que todavía permite sembrar,
  y su cosecha tiene que dejar lugar a los pasos que faltan. Una temporada que el cultivo anterior todavía ocupa no
  se muestra. Así no hay ciclos encimados: en Mexicali salen 2 ciclos al año (trigo OI → algodón/sorgo PV); en Iowa
  uno (maíz may–sep, invierno en descanso), como en la realidad.

### 4.2 Simulación del ciclo de cada cultivo (día por día)
Para cada cultivo y temporada se prueban **6 fechas de siembra** (día 1 y 16 de cada mes de la temporada) y se
recorre el ciclo completo día por día (el ciclo puede pasar a la siguiente temporada):
1. **Aptitud por temperatura (modelo EcoCrop, Hijmans et al. 2001):** para cada mes del ciclo (con ≥ 10 días),
   vale 1 si la temperatura media está en el rango óptimo y baja en línea recta hasta 0 en los límites absolutos.
   **Manda el peor mes** del ciclo.
2. **Helada letal:** si en algún mes la mínima diaria media menos **2.5 °C** es ≤ la temperatura que mata al
   cultivo (`KTMP` de ECOCROP, o 0 °C si no hay dato), el cultivo queda descartado en esa fecha. El margen de 2.5 °C
   está **calibrado** (sección 6); el paquete original `dismo::ecocrop` usa 5 °C.
3. Gana la fecha con **mejor aptitud**. Si varias empatan, todas forman la **ventana de siembra** que muestra la
   app (p. ej. «Abr – May») y los números (agua, cosecha) son los de la fecha **a la mitad de la ventana**: neutral,
   sin escoger la fecha que más le conviene a una estrategia.
4. **Agua del ciclo (FAO-56):** `ETc = Σ Kc(día) × ET₀(mes)` con la curva de Kc de **4 etapas** (inicial,
   desarrollo, media, final; Tablas 11 y 12) y Kc ajustado al viento y la humedad del lugar (ec. 62 y 65: un clima
   seco y ventoso hace que el cultivo transpire más que en las tablas).
5. **ET₀ (evapotranspiración de referencia):** **FAO Penman-Monteith** (FAO-56 ec. 6) con temperatura, punto de
   rocío, viento, radiación y altitud de NASA POWER. Si falta algún dato, **Hargreaves** (ec. 52, solo temperatura y
   latitud).
6. **Lluvia efectiva:** la parte de la lluvia mensual que aprovecha el cultivo (FAO Tabla 6; con ≤ 10 mm/mes es 0).
7. **Riego necesario** = `max(0, agua del ciclo − lluvia efectiva del ciclo)`.
8. **Riesgo de helada:** ≥ 1 día con helada esperado en el ciclo (promedio de 10 años de `FROST_DAYS`).
   **Riesgo de calor:** la temperatura **media** de algún mes del ciclo pasa el óptimo de ECOCROP (la misma escala
   que usa EcoCrop; comparar la máxima diaria contra ECOCROP mezclaría escalas).

### 4.3 Puntaje 0–100 de cada cultivo que tolera el clima

| Factor | Cálculo (0 a 1) | Peso |
|---|---|---|
| Temperatura | Aptitud EcoCrop del ciclo | 0.40 |
| Agua | De temporal: `min(1, lluvia efectiva / agua necesaria)` · De riego: `1 − riego / máximo riego de las opciones` | 0.30 |
| Suelo | Textura (1 si la tolera, 0.5 si no) × pH (1 si está en el óptimo ± 0.5, 0.6 si no) | 0.15 |
| Prioridad | Agua: `1 − agua / máxima agua` · Nitrógeno: leguminosa 1, cobertura 0.7, otros 0 · Rendimiento: cereales, hortalizas, oleaginosas, industriales 1; otros 0.5 | 0.15 |

`puntaje = round(100 × Σ peso × factor)` y luego multiplicadores:
- **× 0.7** si es de la **misma familia botánica** que el cultivo anterior (comparten plagas y enfermedades; p. ej.
  chile → jitomate, ambos Solanáceas).
- **× 0.9** si está fuera de su temporada habitual (es preferencia, no filtro: en climas fríos el trigo va en verano).
- **× 0.85** si cambia de sistema de producción respecto al cultivo actual (granos ↔ hortalizas: otro equipo, mano
  de obra y mercado).
- Nunca se repite el mismo cultivo dos temporadas seguidas. Empate → el que necesita menos agua.
- **Barbecho (descanso):** si ningún cultivo tolera el clima de la temporada, o ninguno cabe entre la cosecha
  anterior y lo que sigue, el paso es «descanso» con puntaje 0 y la razón lo dice (p. ej. invierno en Iowa o
  Saskatchewan).

**Importante:** los pesos (40/30/15/15) y los castigos (0.7, 0.9, 0.85) son **parámetros de diseño propios**, no
vienen de un estudio. Por eso se midió su efecto con un análisis de sensibilidad (sección 6).

### 4.4 Estrategias
- **«Seguir como hoy»:** el cultivo actual cada vez que cabe en la línea de tiempo y el clima lo permite; descanso
  donde no (monocultivo).
- Una rotación por cada prioridad (**agua**, **nitrógeno**, **rendimiento**): el mismo algoritmo, solo cambia el
  factor de prioridad. Si dos dan los mismos cultivos se fusionan («Ahorrar agua · Regenerar el suelo»).
- La recomendada es la de la prioridad que eligió el usuario.
- Cada estrategia trae: agua total, riego, nitrógeno, salud del suelo, temporadas sin cultivo, beneficios, riesgos y
  **evidencia** (p. ej. «Chícharo, siembra dic – feb (ciclo Dic–Feb): necesita ~316 mm (FAO-56, ET₀
  Penman-Monteith) y la lluvia efectiva aporta ~0 mm (NASA POWER)»).
- **`localChecks`:** 1–5 cosas que confirmar con productores o un agrónomo (análisis de suelo, fechas locales,
  plagas de la zona, plan si falla la lluvia…).

### 4.5 Impacto (comparación «hoy» vs. «recomendado»)
- **Agua total del cultivo** = Σ ETc de los ciclos (menor = mejor).
- **Riego necesario** = Σ riego (menor = mejor).
- **Balance de nitrógeno (estimado)** = Σ balances parciales de cada cultivo (sección 4.6). Negativo = la rotación
  saca más nitrógeno del que repone y hay que fertilizar.
- El barbecho no consume agua ni nitrógeno.
- Ojo: si «seguir como hoy» deja temporadas sin cultivo y la rotación tiene más ciclos, la recomendada puede usar
  **más** agua total. Es real: hay más ciclos de cultivo (y más producción y suelo cubierto). Por eso la estrategia
  también dice el **riego por ciclo** (comparación justa) y el pitch cita esa cifra, con «less» o «more» según el
  signo real (en la demo de Mexicali: ~484 contra ~655 mm por ciclo).

### 4.6 Nitrógeno (estimado)
- **Balance parcial = N fijado del aire − N que sale con la cosecha** (kg N/ha por ciclo).
- **N que sale con la cosecha:** coeficiente kg N por tonelada (Ludemann et al. 2024, *Earth System Science Data*,
  la base que usa FAOSTAT para sus balances de nutrientes) × **rendimiento real del país** (FAOSTAT).
- **N fijado por leguminosas de grano:** modelo de **Herridge et al. 2022** (*Plant and Soil*), que depende del
  rendimiento, del índice de cosecha y de la fracción de N que viene del aire.
- **Veza como abono verde:** no se cosecha, todo lo fijado se queda: **119 kg N/ha** (punto medio de 107–131,
  Kebede 2021).
- No incluye pérdidas por lixiviación, fertilización, residuos ni mineralización. Sirve para **comparar
  rotaciones**, no como recomendación de fertilización. Por eso se etiqueta «estimado».

### 4.7 Salud del suelo (índice estimado 0–100)
- Parte de 50 (40 si el usuario dice que su materia orgánica es baja, 60 si es alta) **+10 por cada leguminosa**,
  **+8 por cada cobertura**, **−10 por cada par de cultivos seguidos de la misma familia**; acotado a 0–100.
- Es una **regla propia e ilustrativa**: va en la dirección que reporta la literatura (más diversidad y leguminosas
  → mejor suelo) pero los puntos no vienen de un estudio. Se presenta como índice comparativo, no como medición.

### 4.8 Métricas NASA de la parcela (las 4 tarjetas)

| Métrica | Valor | Cuándo alerta |
|---|---|---|
| Humedad del suelo (raíces) | `GWETROOT` medio de los últimos 30 días: **percentil** frente a las mismas fechas de los 10 años | Categorías del U.S. Drought Monitor: percentil ≤ 20 (D1) → atención; ≤ 10 (D2 o peor) → crítico. Si NASA calculó los días recientes con otro modelo (GEOS-IT), **no se compara** y la tarjeta lo explica |
| Lluvia 90 días | Lluvia de los últimos 90 días vs. lo normal para esas fechas | Categorías del Servicio Meteorológico de la India (IMD): −20 a −59 % deficiente (atención); ≤ −60 % muy deficiente (crítico). Si lo normal es ≤ 30 mm se marca «temporada normalmente seca» |
| Temperatura media | Últimos 30 días vs. lo normal | Desviación de ±1 σ → atención; ±2 σ → crítico |
| Radiación solar | Promedio anual (kWh/m²/día) | Informativa |

Cada tarjeta trae un **significado en palabras simples** («Seca: más seca que en 8 de los últimos 10 años en estas
fechas») y la serie de 12 meses.

**Hallazgo técnico (buena respuesta para el jurado):** desde octubre de 2026 NASA POWER calcula los días recientes
con **GEOS-IT** en vez de **MERRA-2** (lo dice el encabezado `sources` de la respuesta). La temperatura y la lluvia
siguen continuas, pero la humedad del suelo salta: en Mexicali pasa de ~0.45 a 0.14 y en Iowa de ~0.45 a 0.70 de un
mes a otro. Compararla contra el histórico daría alarmas falsas, así que el backend lo detecta y no la compara.

### 4.9 Incertidumbre
- Según el **coeficiente de variación (CV) de la lluvia anual** de los 10 años: **< 20 % baja, 20–30 % media,
  > 30 % alta** (umbrales de Abdul Talib et al. 2024, *Heliyon*, Tabla 2).
- Sube un nivel si no llegaron los datos recientes (plan B) y se marca si es un escenario hipotético.

### 4.10 Escenario «¿y si…?» (`climateShift`)
- El usuario mueve dos sliders: lluvia de **−60 % a +60 %** y temperatura de **−3 a +5 °C**.
- Se multiplica la lluvia de cada mes y se suman los °C a la media, máxima, mínima y punto de rocío (humedad relativa
  casi constante, lo habitual en escenarios de calentamiento). Se vuelve a correr todo el motor.
- **Nunca se guarda en el historial** (solo funciona con `guardar=false`): un escenario inventado no debe parecer un
  análisis real.
- Es un análisis de sensibilidad, **no** una proyección de un modelo climático (no usamos CMIP6).

### 4.11 Otras funciones del frontend
- Calendario de siembra, alertas de heladas/calor/sequía/lluvia por mes (reglas simples sobre el clima mensual
  histórico; **no es pronóstico**), comparación de escenarios, historial, exportar el plan en **PDF** para el
  agrónomo, modo claro/oscuro, búsqueda de lugar y «Mi ubicación».

---

## 5. Números para tener a la mano

| Dato | Valor |
|---|---|
| Años de clima por análisis | 10 años completos (2016–2025) + últimos 90 días |
| Historial disponible en NASA POWER | más de 40 años |
| Resolución del clima | celda de 0.5° × 0.625° (~55 km) |
| Resolución del suelo | ~250 m (SoilGrids), capa 0–30 cm |
| Cultivos en el catálogo | 18 |
| Rotación | 3 pasos en una línea de tiempo de 12 meses, sin ciclos encimados |
| Estrategias comparadas | «Seguir como hoy» + hasta 3 (agua, nitrógeno, rendimiento) |
| Tamaño de parcela | 0.1 a 500 ha |
| Países | México, EE. UU., Canadá |
| Filtro por país | ≥ 10 000 ha cosechadas al año (FAOSTAT 2020–2024) |
| Pesos del puntaje | temperatura 40 %, agua 30 %, suelo 15 %, prioridad 15 % |
| Castigos | misma familia × 0.7 · fuera de temporada × 0.9 · cambio de sistema × 0.85 |
| Margen de helada letal | 2.5 °C (calibrado) |
| Fechas de siembra probadas | 6 por temporada (día 1 y 16 de cada mes) |
| Pruebas automáticas | 148 (pytest), incluido Penman-Monteith contra el ejemplo 17 de FAO-56 |
| Validación | 34 casos reales en 11 regiones (sección 6) |
| Primera consulta de un lugar | ~10 s; después milisegundos (caché) |
| Límite de uso | 30 análisis por IP por minuto |
| Demo del pitch | parcela en el valle de Mexicali (~8.4 ha, suelo franco, pH ~8). Los números del pitch salen **en vivo**: decir los de la pantalla |

---

## 6. Validación científica (cómo sabemos que no inventa)

Script `backend/research/validar_motor.py`, con **clima real de NASA POWER**, compara lo que dice el motor contra
calendarios oficiales de siembra:

- **Fuentes de referencia:** USDA NASS *Usual Planting and Harvesting Dates* (2010) para Iowa, Dakota del Norte,
  Kansas, Arizona y California; SADER Baja California (valle de Mexicali, San Quintín); SADER/Sonora (valle del
  Yaqui); CEIEG Sinaloa (Culiacán); SADER Guanajuato (Bajío); *Saskatchewan Crop Report* (Canadá).
- **34 combinaciones lugar–cultivo–temporada que de verdad se siembran** en **11 regiones**.

Resultados con el margen de helada usado (2.5 °C):

| Prueba | Resultado |
|---|---|
| ¿Considera viable lo que de verdad se siembra? | **97 %** (33 de 34) |
| ¿La ventana de siembra del motor coincide con la oficial? | **100 %** (33 de 33) |
| ¿Descarta lo que no se siembra por clima? (algodón en Iowa, Dakota del Norte, Saskatchewan) | **100 %** (12 de 12) |
| ¿Propone barbecho en inviernos sin agricultura? (Iowa, Dakota del Norte, Saskatchewan) | **100 %** (3 de 3) |

- **El caso que falla:** el **trigo de invierno de Kansas**. Ese trigo se siembra en otoño y pasa el invierno
  dormido bajo la nieve (endurecimiento y vernalización); un modelo mensual tipo EcoCrop no simula la dormancia, así
  que lo ve como muerto por helada. Es una limitación conocida y honesta.
- **Calibración del margen de helada:** con 0 °C y 2.5 °C acierta 97 %; con 5 °C (el valor de `dismo`) baja a 94 %
  porque descarta el trigo de diciembre en Arizona. Se eligió 2.5 °C.
- **Análisis de sensibilidad de los parámetros de diseño:** 11 lugares × 3 prioridades × 3 temporadas; se movió cada
  peso ×0.5 y ×1.5 y cada castigo hacia arriba y hacia abajo. **En promedio, el 95 % de los pasos de la rotación no
  cambian.** Lo más sensible es el castigo por cambio de sistema (0.85 → 0.95 deja igual el 87 %) y el peso de la
  temperatura a la mitad (87 %), lo cual tiene sentido: deciden si se propone pasar de granos a hortalizas y cuánto
  pesa el clima.
- **Errores que la validación encontró y ya se corrigieron** (detalle en `docs/METODOLOGIA.md` §4 y
  `docs/VALIDACION.md`):
  1. En el endpoint mensual de NASA POWER, `T2M_MAX`/`T2M_MIN` son **extremos** del mes, no promedios. Con ellos el
     motor veía heladas en mayo en Iowa y descartaba el maíz (viabilidad 41 %). Con `T2M ± T2M_RANGE/2` sube a 97 %.
  2. Desde oct-2026 los días recientes de POWER vienen de **GEOS-IT** y la humedad del suelo no es continua con
     MERRA-2: se detecta con `header.sources` y no se compara.
  3. **Ciclos encimados:** los ciclos duran 95–188 días, no 3 meses; ahora la rotación es una línea de tiempo.
  4. Se quitaron constantes sin fuente (lluvia efectiva fija de 80 %, base de 40 kg N/ha, umbrales de lluvia
     −10/−30 %, CV 15/30 %, etc.) y se reemplazaron por FAO, IMD, U.S. Drought Monitor y Abdul Talib 2024.
  5. El modo demo (`mock.ts`) ya no tiene números escritos a mano: lo genera `research/generar_mock.py` con una
     respuesta real del backend.
- **Cómo reproducirlo:** `docker compose exec backend pytest -q` (148 pruebas) y
  `docker compose exec backend python research/validar_motor.py` (~1 min).
- **Lo que falta validar:** probar con **agricultores y agrónomos reales** (INIFAP, extensionistas). Es nuestro
  siguiente paso y lo decimos en el pitch.

---

## 7. Limitaciones (decirlas antes de que las pregunten)

1. **Resolución del clima ~55 km:** no capta microclimas, valles ni efectos de altitud dentro de la celda. Por eso el
   límite de 500 ha y la recomendación de confirmar localmente.
2. **La lluvia es lo más débil de NASA POWER**, sobre todo en zonas áridas y de montaña. La temperatura es mucho más
   confiable. Alternativa futura: lluvia de GPM IMERG.
3. **Temporadas por temperatura:** sirven para clima templado/subtropical. En el trópico manda la época de lluvias;
   en Canadá en realidad hay una sola temporada de cultivo (el motor lo resuelve con barbecho en invierno).
4. **Suelo de un modelo global de 250 m**, no un análisis de laboratorio.
5. **Pesos y castigos propios**, medidos con sensibilidad pero no calibrados con datos de rendimiento.
6. **Nitrógeno y salud del suelo son estimaciones** (balance parcial y regla ilustrativa).
7. **Sin rendimiento ni economía** (precios, costos, mercado).
8. **Sin plagas ni enfermedades locales** (solo la regla de familia botánica).
9. **Cultivos perennes** (alfalfa, frutales) fuera del catálogo: no encajan en una rotación por temporada.
10. **No es pronóstico:** clima típico de 10 años + anomalía reciente; el «¿y si…?» es hipotético.
11. **Validación agronómica en campo pendiente.**
12. **Cambio de modelo en NASA POWER (GEOS-IT desde oct-2026):** la humedad del suelo reciente no es comparable con
    el histórico de MERRA-2; mientras dure, esa tarjeta no alerta (y lo explica).
13. **Cereales de invierno que pasan el invierno dormidos** (trigo de Kansas): EcoCrop mensual no modela la
    dormancia/vernalización; el motor los descarta donde el invierno es muy frío.

---

## 8. Preguntas técnicas probables y respuestas sugeridas

Formato: pregunta en inglés (como la haría el jurado) · respuesta en español para entenderla · **Say:** respuesta
corta en inglés sencillo para decirla.

### A. Datos y NASA

**1. Which NASA data do you use exactly?**
NASA POWER, comunidad agricultura: temperatura media, rango diario, lluvia corregida, humedad del suelo en raíces,
radiación solar, punto de rocío, viento y días con helada. Serie mensual de 10 años y diaria de 90 días.
**Say:** *"We use NASA POWER: temperature, rain, root-zone soil moisture, solar radiation, dew point, wind and frost
days. Ten years of monthly data and the last 90 days of daily data."*

**2. Why NASA POWER and not weather stations?**
Cubre cualquier punto del planeta, es gratis, sin llave, consistente en el tiempo y con variables agrícolas listas.
Las estaciones son escasas en zonas rurales y cada país tiene su formato.
**Say:** *"Stations are rare in rural areas. NASA POWER covers every field, for free, with the same format
everywhere."*

**3. NASA POWER has ~55 km resolution. Is that enough for an 8-hectare field?**
Para clima regional sí: la temperatura y la estación de lluvias cambian poco en esa escala en terreno plano. No capta
microclimas ni altitud; por eso el suelo viene de un dato a 250 m, limitamos a 500 ha y pedimos confirmar con
productores locales. Es una herramienta de orientación.
**Say:** *"Climate changes slowly over distance, so it works for planning. For local details, the soil comes from a
250-meter model, and the app tells the farmer what to check locally."*

**4. Is this satellite data?**
NASA POWER combina el reanálisis MERRA-2 (modelo + observaciones, incluidas de satélite) y radiación solar de
CERES. Nosotros no procesamos imágenes de satélite; consumimos la API de POWER. El mapa de fondo es imagen de Esri.
**Say:** *"We don't process satellite images. We use NASA POWER, which combines NASA's MERRA-2 reanalysis and
satellite-based solar data."*

**5. Why 10 years and not the 30-year climate normal?**
Diez años reflejan mejor el clima actual (ya con calentamiento) y usamos el mismo periodo para el promedio y para la
variabilidad. La normal de 30 años de la OMM es más estable pero incluye un clima que ya cambió. Es un
compromiso consciente.
**Say:** *"The climate is changing, so the last 10 years are closer to today's reality. We use the same period for
the average and the variability."*

**6. How accurate is NASA POWER rainfall?**
Es su punto débil, sobre todo en desierto y montaña (estudios de validación lo muestran). La temperatura es buena.
Por eso medimos la incertidumbre con la variabilidad de la lluvia y la mostramos. A futuro: GPM IMERG.
**Say:** *"Rain is the weakest variable, especially in dry areas. That's why we show uncertainty, and IMERG is a next
step."*

**7. What happens if NASA POWER is down during the demo?**
Caché en memoria y en PostgreSQL; si NASA falla se usa el registro guardado aunque esté vencido; si faltan los datos
recientes, plan B con aviso y más incertidumbre. La presentación además arranca con datos de ejemplo si el backend no
responde.
**Say:** *"We cache every location in the database. If NASA is down, we use the saved data and tell the user."*

**8. Is the soil data from NASA?**
No. Es de ISRIC SoilGrids (modelo global de suelos). Lo decimos así en la app.
**Say:** *"No, soil comes from ISRIC SoilGrids, and we label it clearly."*

### B. Algoritmo y ciencia

**9. Is this AI or machine learning?**
No. Es un motor de reglas basado en FAO ECOCROP y FAO-56. No hay datos etiquetados de resultados de rotaciones para
entrenar un modelo confiable, y un agricultor necesita entender **por qué**. Cada número se explica.
**Say:** *"No. It's a transparent rules engine with FAO science. Every number has a source, so the farmer can
understand why."*

**10. How do you decide which crop is recommended?**
Para cada temporada simulamos el ciclo de cada cultivo día por día, descartamos los que el clima no permite y
puntuamos el resto: temperatura 40 %, agua 30 %, suelo 15 %, prioridad del usuario 15 %, con castigos por repetir
familia, salirse de temporada o cambiar de sistema.
**Say:** *"For each season we simulate every crop day by day, remove the ones the climate doesn't allow, and score the
rest on temperature, water, soil and the farmer's priority."*

**11. Where do the weights 40/30/15/15 come from?**
Son parámetros de diseño propios, no de un estudio. Por eso hicimos un análisis de sensibilidad: al moverlos ±50 %,
el 95 % de la rotación no cambia (el más influyente, el castigo por cambio de sistema, deja igual el 87 %). Se pueden calibrar con agrónomos.
**Say:** *"They are our design choices. We tested them: changing each one by 50 percent keeps 95 percent of the
rotation the same."*

**12. How do you calculate crop water needs?**
FAO-56: evapotranspiración de referencia con Penman-Monteith (temperatura, rocío, viento, radiación y altitud de NASA
POWER) × coeficiente de cultivo Kc con su curva de 4 etapas, ajustado al viento y la humedad del lugar, día por día
durante el ciclo. Menos la lluvia efectiva (FAO) = riego.
**Say:** *"We use FAO-56, the world standard: Penman-Monteith with NASA data, times the crop coefficient, day by day.
Minus the effective rain gives the irrigation."*

**13. What is effective rain?**
La parte de la lluvia que realmente aprovecha el cultivo; el resto escurre o se evapora. Usamos la tabla 6 del manual
de riego de la FAO; con menos de 10 mm al mes es cero.
**Say:** *"It's the part of the rain the crop can really use. We use the FAO table."*

**14. Penman-Monteith vs. Hargreaves?**
Penman-Monteith es el método de referencia de la FAO y es el que usamos cuando NASA da rocío, viento y radiación
(normalmente siempre). Hargreaves (solo temperatura) es el respaldo.
**Say:** *"Penman-Monteith is the FAO reference method; Hargreaves is only a backup."*

**15. How do you handle frost?**
Dos niveles: el modelo EcoCrop descarta un cultivo si la mínima media de algún mes del ciclo está a menos de 2.5 °C
de la temperatura que lo mata (calibrado con calendarios reales), y marcamos riesgo si NASA POWER registra en
promedio al menos un día de helada durante el ciclo.
**Say:** *"We remove crops that frost would kill, and we warn if NASA data shows frost days during the cycle."*

**16. What is "fallow" and why would you recommend it?**
Descanso. Si ningún cultivo del catálogo tolera la temporada (invierno en Iowa o Saskatchewan), la app lo dice en vez
de forzar un cultivo, y sugiere dejar rastrojo o cobertura para evitar erosión.
**Say:** *"If no crop can grow, we say so honestly and suggest keeping the soil covered."*

**17. How do you estimate nitrogen?**
Balance parcial por cultivo: nitrógeno que fijan las leguminosas (modelo de Herridge 2022) menos el que sale con la
cosecha (coeficientes de Ludemann 2024, los de FAOSTAT) usando el rendimiento real del país. La veza como abono verde
aporta ~119 kg/ha. No incluye pérdidas ni fertilizante: es para comparar opciones.
**Say:** *"It's an estimate: nitrogen fixed by legumes minus nitrogen removed by the harvest, with FAOSTAT yields. We
label it as an estimate."*

**18. How is the soil health index calculated?**
Regla propia e ilustrativa: parte de 50, suma por leguminosas y coberturas, resta por repetir familia. Va en la
dirección de la literatura, pero no es una medición. Lo etiquetamos como estimado.
**Say:** *"It's a simple, transparent index: legumes and cover crops add points, repeating plant families removes
points. It's an estimate, and we say so."*

**19. Why avoid the same botanical family in a row?**
Cultivos de la misma familia comparten plagas y enfermedades (chile y jitomate son Solanáceas). Es la regla básica de
rotación de las guías de extensión universitaria.
**Say:** *"Same family means same pests and diseases. Changing family breaks the cycle."*

**20. How do you measure uncertainty?**
Con la variabilidad de la lluvia anual en 10 años (coeficiente de variación): menos de 20 % baja, 20–30 % media, más
de 30 % alta (Abdul Talib 2024). Sube si faltan datos recientes.
**Say:** *"We measure how much the yearly rain changes between years. More variation means more uncertainty."*

**21. How does the "what if" work? Is it a climate projection?**
No es una proyección de un modelo climático. Cambia la lluvia y la temperatura del clima histórico según los sliders y
vuelve a correr todo el motor en el backend. Es un análisis de sensibilidad para planear escenarios secos o
calientes. No se guarda en el historial.
**Say:** *"It's a scenario, not a forecast. We change rain and temperature and the API recalculates the whole plan."*

**22. Why does the recommended rotation sometimes use more water?**
Porque «seguir como hoy» puede dejar temporadas sin cultivo y la rotación las llena: más ciclos, más producción y
suelo cubierto. Por eso mostramos también el riego y la comparación por estrategia.
**Say:** *"Because the rotation grows more seasons. More crops, more soil cover, so more total water."*

**23. How do you validate the recommendations?**
34 casos reales en 11 regiones de EE. UU., México y Canadá contra calendarios oficiales (USDA, SADER, Saskatchewan):
97 % viables, 100 % de ventanas de siembra correctas, 100 % de descarte de lo que no se siembra y 100 % de barbecho
donde corresponde. Falta probar con agricultores.
**Say:** *"We tested 34 real crops in 11 regions against official planting calendars: 97 percent correct. Next: test
with real farmers."*

**24. What case fails?**
El trigo de invierno de Kansas: pasa el invierno dormido bajo la nieve y nuestro modelo mensual no simula la
dormancia.
**Say:** *"Winter wheat in Kansas: it survives winter dormant under snow, and our monthly model doesn't simulate
that."*

**25. Why only 18 crops?**
Son los más importantes de Norteamérica que cubren todas las temporadas, con leguminosas de invierno y verano, y con
datos completos en ECOCROP y FAO. El catálogo se genera con un script; agregar cultivos es agregar renglones.
**Say:** *"They are the main crops of North America for every season. The catalog is generated by a script, so adding
crops is easy."*

**26. How do you know a crop is relevant in that country?**
FAOSTAT: solo recomendamos cultivos con al menos 10 000 hectáreas cosechadas al año en el país.
**Say:** *"We use FAOSTAT: we only recommend crops that are really grown in that country."*

### C. Ingeniería

**27. What is your tech stack?**
React 19 + Vite + TypeScript con Leaflet para el mapa; FastAPI en Python; PostgreSQL con PostGIS; todo en Docker.
**Say:** *"React and TypeScript in the front, FastAPI in Python in the back, PostgreSQL with PostGIS, all in Docker."*

**28. Why FastAPI / Python?**
Asíncrono (descargas de NASA y SoilGrids en paralelo), validación automática con Pydantic, documentación Swagger
automática y el ecosistema científico de Python.
**Say:** *"It's async, it validates every request, and it generates the API docs automatically."*

**29. Why PostGIS?**
Guardamos la geometría de cada parcela con índice espacial; permite consultas por ubicación y crecer a análisis por
región.
**Say:** *"We store every field as a real geometry, ready for spatial queries."*

**30. How does it scale? What about API limits?**
El clima se guarda por celda de NASA (~55 km): muchas parcelas comparten una sola consulta. El motor es una función
pura y rápida. Hay límite de 30 análisis por IP por minuto para cuidar las cuotas externas. Para crecer: varios
workers y un caché compartido (p. ej. Redis).
**Say:** *"We cache climate per NASA grid cell, so many fields share one request. The engine is fast and
stateless."*

**31. How do you test it?**
148 pruebas con pytest (incluido Penman-Monteith contra el ejemplo 17 de FAO-56): motor de reglas con climas inventados, fórmulas FAO-56, cliente de NASA, API y región. Más el
script de validación con datos reales.
**Say:** *"We have 148 automated tests, plus a validation script with real NASA data."*

**32. Does it work offline?**
Sí, es una PWA instalable: la interfaz y el último análisis funcionan sin internet. Un análisis nuevo sí necesita
conexión porque pide datos a NASA.
**Say:** *"Yes, it's an installable web app. The last analysis works without internet in the field."*

**33. What about user data and privacy?**
No hay cuentas. El historial se separa con un identificador anónimo del dispositivo. No pedimos datos personales.
**Say:** *"No accounts. Each device has an anonymous ID. We don't ask for personal data."*

**34. Is it live or mocked in the demo?**
En vivo: la presentación llama a nuestra API (`POST /api/v1/analyses`) y se ve la petición real (método, estado,
milisegundos). Si el backend fallara, cambia a datos de ejemplo y lo dice en pantalla.
**Say:** *"It's live. You can see the real request at the top, and open the API docs."*

### D. Alcance, impacto y siguiente paso

**35. Does it work outside North America?**
Los datos (NASA, SoilGrids, ECOCROP, FAO-56) son globales, pero el catálogo, el filtro por país y las temporadas están
calibrados para México, EE. UU. y Canadá. Para el trópico hacen falta temporadas por lluvia y cultivos tropicales.
**Say:** *"The data is global, but we calibrated it for North America. The tropics need rain-based seasons; that's
future work."*

**36. Who is the user?**
Pequeños y medianos productores y, sobre todo, **extensionistas y agrónomos** que asesoran a muchos productores; por
eso el PDF.
**Say:** *"Farmers, and especially agronomists and extension workers who help many farmers."*

**37. How is this different from FAO CROPWAT or AquaCrop?**
CROPWAT calcula necesidades de agua pero pide capturar el clima y el cultivo a mano. AquaCrop simula rendimiento y
requiere calibración experta. Nosotros automatizamos los datos desde el mapa y damos opciones de rotación explicadas en
lenguaje simple.
**Say:** *"Those tools are for experts and need manual data. We get the data from a map click and explain rotation
options in plain words."*

**38. What's your next step?**
Validar con agricultores y agrónomos (INIFAP, extensionistas), mejorar la lluvia con IMERG, temporadas por lluvia
para el trópico, más cultivos, inglés y unidades imperiales.
**Say:** *"Test with real farmers and agronomists, better rain data with IMERG, and more crops and regions."*

### E. Preguntas difíciles (para no ponerse nerviosos)

**39. "Your soil health number goes from 30 to 60. Isn't that made up?"**
Es un índice comparativo con reglas simples y públicas; no es una medición y la app lo etiqueta como estimado. Sirve
para ver qué rotación favorece más el suelo.
**Say:** *"It's an estimate, not a measurement, and we label it. It compares options with simple, public rules."*

**40. "Would you trust this to make a real decision?"**
Para orientar y comparar opciones, sí; para decidir solo, no. Por eso trae incertidumbre y una lista de lo que hay que
confirmar localmente. AgroBytes no reemplaza al agricultor ni al agrónomo.
**Say:** *"It helps the decision; it doesn't replace the farmer or the agronomist. That's why we show uncertainty and
what to check locally."*

**41. "What if the farmer's soil is different from SoilGrids?"**
El usuario puede corregir textura, pH y materia orgánica; lo que capture manda sobre SoilGrids.
**Say:** *"The farmer can change it. Their data always wins."*

**42. "Why not predict yield?"**
Sin un modelo de cultivo calibrado localmente sería un número inventado. Preferimos no mostrarlo.
**Say:** *"Without a calibrated crop model, a yield number would be invented. We prefer to be honest."*

**43. Si no sabes una respuesta**
Decir: *"Good question. We don't model that yet; it's in our next steps."* o *"I'm not sure; my teammate can
answer."* Nunca inventar números.

---

## 9. Glosario rápido

| Término | Qué significa |
|---|---|
| **DSS** | Sistema de apoyo a la decisión: da opciones explicadas, no decide |
| **NASA POWER** | Servicio de NASA con datos de clima y radiación por punto, gratis |
| **MERRA-2** | Reanálisis atmosférico de NASA (modelo + observaciones) del que sale la meteorología de POWER |
| **Reanálisis** | Reconstrucción del clima pasado combinando un modelo con observaciones |
| **GWETROOT** | Humedad del suelo en la zona de raíces, de 0 (seco) a 1 (saturado) |
| **PRECTOTCORR** | Lluvia total corregida de NASA POWER |
| **ET₀** | Evapotranspiración de referencia: agua que pierde un pasto de referencia por clima |
| **ETc** | Evapotranspiración del cultivo = Kc × ET₀ |
| **Kc** | Coeficiente de cultivo (FAO-56): cuánto más o menos agua usa un cultivo que el pasto de referencia, según su etapa |
| **Penman-Monteith** | Método de referencia de la FAO para ET₀ (temperatura, humedad, viento, radiación) |
| **Hargreaves** | Método simple de ET₀ solo con temperatura (respaldo) |
| **Lluvia efectiva** | La parte de la lluvia que aprovecha el cultivo |
| **FAO ECOCROP** | Base de la FAO con los rangos de clima y suelo de cada cultivo |
| **EcoCrop (modelo)** | Modelo de aptitud de Hijmans et al. (2001) que usa esos rangos mes por mes |
| **KTMP** | Temperatura que mata la planta según ECOCROP |
| **Barbecho (fallow)** | Temporada de descanso, sin cultivo |
| **Abono verde / cobertura** | Cultivo (veza) que se incorpora al suelo en vez de cosecharse |
| **Leguminosa** | Familia Fabaceae (frijol, soya, garbanzo, chícharo, veza): fija nitrógeno del aire |
| **Familia botánica** | Grupo de plantas emparentadas que comparten plagas (Poaceae, Fabaceae, Solanaceae…) |
| **Balance parcial de N** | Nitrógeno fijado − nitrógeno que sale con la cosecha |
| **CV** | Coeficiente de variación: desviación estándar / promedio |
| **Desviación estándar (σ)** | Cuánto se aleja normalmente un valor del promedio entre años |
| **SoilGrids** | Modelo global de suelos de ISRIC a 250 m |
| **FAOSTAT** | Estadísticas agrícolas de la FAO por país |
| **PostGIS** | Extensión de PostgreSQL para datos geográficos |
| **PWA** | Aplicación web instalable que funciona sin internet |
| **Temporal / riego** | Parcela que depende de la lluvia / que se riega |

---

## 10. Referencias principales

- NASA POWER — API y metodología: https://power.larc.nasa.gov/docs/
- Allen, R. G. et al. (1998). *Crop evapotranspiration*, FAO Irrigation and Drainage Paper 56.
  https://www.fao.org/4/x0490e/x0490e00.htm
- Brouwer, C. y Heibloem, M. (1986). *Irrigation Water Management: Irrigation Water Needs*, FAO Training Manual 3.
  https://www.fao.org/4/s2022e/s2022e00.htm
- FAO ECOCROP (copia pública): https://github.com/openclim/ecocrop
- Hijmans, R. J. et al. (2001). Modelo EcoCrop (implementado en el paquete `dismo` de R).
- ISRIC SoilGrids v2.0: https://rest.isric.org/soilgrids/v2.0/docs
- FAOSTAT (producción y área cosechada): https://www.fao.org/faostat/
- Ludemann, C. I. et al. (2024). Global FAOSTAT reference database of cropland nutrient budgets. *Earth System
  Science Data* 16, 525–541. https://doi.org/10.5194/essd-16-525-2024
- Herridge, D. F. et al. (2022). Global estimates of nitrogen fixation in grain legumes. *Plant and Soil*.
- Kebede, E. (2021). Fijación biológica de nitrógeno. *Frontiers in Sustainable Food Systems* 5:767998.
- Abdul Talib et al. (2024). Umbrales de CV de la lluvia. *Heliyon* 10:e30324.
- USDA NASS (2010). *Field Crops Usual Planting and Harvesting Dates*.
- Natural Earth (fronteras, dominio público): https://www.naturalearthdata.com/
