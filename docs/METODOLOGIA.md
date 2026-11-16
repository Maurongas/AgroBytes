# Metodología: de dónde sale cada número

> Inventario completo de los datos y reglas del sistema, con su fuente y qué tan respaldado está cada uno.
> Fecha: 2026-11-15 (arquitectura v2.3). Complementa [`ARQUITECTURA.md`](ARQUITECTURA.md) §6–§8 (cómo se implementa)
> y [`VALIDACION.md`](VALIDACION.md) (cómo se comprobó contra la realidad).

## Cómo leer este documento

Cada número cae en una de cuatro categorías. La regla es **no presentar nunca uno de nivel 🔴 como si fuera 🟢**.

| Nivel | Significa | Cómo se presenta |
|---|---|---|
| 🟢 **Dato oficial / método publicado** | Sale tal cual de una base de datos oficial o de una ecuación publicada y verificada | "Según NASA POWER / FAO-56 / FAOSTAT…" |
| 🟡 **Publicado con aproximación** | Método publicado, pero con una simplificación nuestra documentada (p. ej. usar la fila de un cultivo parecido) | Se dice la aproximación |
| 🟠 **Calibrado** | Parámetro elegido para que el motor coincida con calendarios oficiales de siembra (no viene de un artículo) | "Calibrado contra USDA/SADER" |
| 🔴 **Diseño propio** | Regla o peso nuestro, sin estudio que lo respalde. Su efecto se midió con análisis de sensibilidad | "Estimado" / "parámetro de diseño" |

---

## 1. Datos de entrada

| Dato | Fuente | Nivel | Notas |
|---|---|---|---|
| Temperatura media, rango diario, extremos, lluvia, humedad del suelo, radiación, punto de rocío, viento, días con helada, altitud | **NASA POWER** (comunidad AG), API mensual 10 años + diaria 90 días | 🟢 | Reanálisis MERRA-2 (y GEOS-IT en los días más recientes), celda de ~55 km. No es una estación en la parcela. |
| Rangos de temperatura (óptimo y absoluto), temperatura letal (KTMP), pH óptimo, textura, familia botánica | **FAO ECOCROP** (copia pública `EcoCrop_DB.csv`, OpenCLIM) | 🟢 | Rangos de expertos por especie, no por variedad. FAO descontinuó el portal (~2015). |
| Duración del ciclo y agua típica por ciclo | **FAO Irrigation Water Management, Training Manual 3**, cap. 2, Tablas 4 y 5 (punto medio) | 🟡 | Garbanzo, veza, canola, cártamo y calabaza no están: se usa el cultivo FAO más parecido o ECOCROP (`build_crops.py` dice cuál). El agua típica solo se usa si no hay Kc. |
| Coeficientes de cultivo Kc ini / mid / end, altura | **FAO-56**, Tabla 12 | 🟢/🟡 | Punto medio cuando la tabla da un rango; Kc ini del grupo del cultivo. Veza no está: se usa chícharo. |
| Duración de las 4 etapas del ciclo | **FAO-56**, Tabla 11 (fila indicada en `build_crops.py`) | 🟡 | Garbanzo, veza y canola no tienen fila: se usa la de chícharo o cártamo. |
| Suelo de la parcela (arcilla, arena, pH, 0–30 cm) | **ISRIC SoilGrids v2.0** | 🟢 | Modelo global de ~250 m: la app pide confirmar con análisis de laboratorio. API beta: a veces no responde y el análisis sigue sin suelo. |
| Qué se siembra en cada país (área cosechada) y rendimiento (producción / área) | **FAOSTAT QCL**, promedio 2020–2024 | 🟢 | |
| N que sale con la cosecha (kg N por tonelada) | **Ludemann et al. 2024**, *Earth System Science Data* 16:525, suplemento, Tabla S3 | 🟢 | Es la base que usa FAOSTAT para sus balances de nutrientes. Excepción documentada: algodón (abajo). |
| N fijado por leguminosas de grano | Modelo de **Herridge et al. 2022** (*Plant and Soil*), coeficientes de Ludemann et al. 2024, Tabla S2 | 🟢 | Depende del rendimiento del país. |
| N de la veza como abono verde | **Kebede 2021**, *Frontiers in Sustainable Food Systems* 5:767998, Tabla 1 (107–131 → 119 kg/ha) | 🟢 | Se incorpora al suelo: no se cosecha. |
| N del algodón | **Univ. of Missouri Extension G4256** (35–40 lb N por paca de 480 lb de fibra → ~30 kg N/t de algodón con semilla) | 🟡 | La Tabla S3 dice 56 kg N/t, imposible para algodón con semilla (implicaría 5.6 % de N). Se usa Missouri y se documenta la discrepancia. |
| Fronteras de países | **Natural Earth** 1:50m | 🟢 | |

## 2. Cálculos del motor

| Cálculo | Método | Nivel | Detalle |
|---|---|---|---|
| ET₀ (demanda de agua de la atmósfera) | **FAO Penman-Monteith**, FAO-56 ec. 6 (con ec. 7, 8, 11–14, 21–25, 37–40, 43) | 🟢 | Verificado contra el **ejemplo 17 de FAO-56** (5.72 mm/día) en `tests/test_fao56.py`. Plan B: Hargreaves (ec. 52) si faltan datos. |
| Máxima / mínima diaria promedio | `T2M ± T2M_RANGE / 2` de NASA POWER | 🟢 | Verificado contra los datos diarios de POWER (ver "Errores corregidos"). |
| Agua del cultivo (ETc) | `Σ Kc(día) × ET₀(mes)` con la curva de 4 etapas, FAO-56 ec. 66 | 🟢 | Kc mid y Kc end ajustados al viento y a la humedad mínima del lugar, FAO-56 ec. 62 y 65. |
| Lluvia que aprovecha el cultivo | FAO Training Manual 3, cap. 3, **Tabla 6** (interpolación lineal) | 🟢 | Arriba de 250 mm/mes se mantiene la pendiente de la tabla (0.8): extrapolación nuestra. |
| Riego necesario | `max(0, ETc − lluvia efectiva)` | 🟢 | |
| Aptitud por temperatura | Modelo **EcoCrop** (Hijmans et al. 2001; función `ecocrop` del paquete `dismo`): trapecio de ECOCROP aplicado a cada mes del ciclo, manda el peor | 🟢 | Un mes cuenta si el ciclo pasa ahí ≥ 10 días (🔴, detalle de implementación). |
| Helada letal | EcoCrop: mes letal si `mínima diaria media − margen ≤ KTMP` | 🟠 | `dismo` usa 5 °C; con 34 casos reales, **2.5 °C** acierta más sin perder especificidad (`VALIDACION.md`). |
| Mejor fecha de siembra | Se prueban los días 1 y 16 de cada mes de la temporada (como EcoCrop prueba cada mes de inicio) | 🟢/🔴 | Si empatan, la ventana es todo el rango y los números salen de la fecha a la mitad (neutral). |
| Rotación sin ciclos encimados | Línea de tiempo de 12 meses: cada cultivo se siembra después de cosechar el anterior | 🟢 | Restricción física, no un supuesto. |
| Riesgo de helada | ≥ 1 día con helada esperado en el ciclo (`FROST_DAYS` de NASA POWER, promedio de 10 años) | 🟢 | Umbral de 1 día = "al menos una helada en un año típico". |
| Riesgo de calor | Temperatura media de algún mes del ciclo > óptimo de ECOCROP | 🟢 | Misma escala que EcoCrop (media mensual). |
| Balance de nitrógeno | Fijación (Herridge) − extracción (Ludemann × rendimiento FAOSTAT del país) | 🟢 como método, 🟡 como número | Es un **balance parcial**: no incluye pérdidas, fertilización, residuos ni mineralización. Sirve para comparar rotaciones, no para fertilizar. Por eso dice "estimado". |
| Lluvia de 90 días contra lo normal | Categorías del **India Meteorological Department**: normal ±19 %, deficiente −20 a −59 %, muy deficiente ≤ −60 % | 🟢 | Si lo normal es ≤ 10 mm/mes no se compara: la lluvia efectiva es 0 (FAO Tabla 6). |
| Temperatura de 30 días contra lo normal | Anomalía en desviaciones estándar de esos meses entre los 10 años: ≥ 1 atención, ≥ 2 crítico | 🟢 (estadística estándar) | Sin desviación de referencia no se alerta. |
| Humedad del suelo contra lo normal | Percentil frente a las mismas fechas de los 10 años, categorías del **U.S. Drought Monitor** (Svoboda et al. 2002): ≤ 20 D1, ≤ 10 D2 o peor | 🟢 | No se compara si NASA calculó los días recientes con otro modelo (GEOS-IT; ver "Errores corregidos"). |
| Incertidumbre | Coeficiente de variación de la lluvia anual: < 20 % baja, 20–30 % media, > 30 % alta (**Abdul Talib et al. 2024**, *Heliyon* 10:e30324, Tabla 2) | 🟢 | Sube un nivel si no llegaron los datos recientes. |
| Qué se recomienda en cada país | Cultivos con ≥ 10 000 ha cosechadas al año en el país (FAOSTAT) | 🟢 dato · 🔴 umbral | El umbral de 10 000 ha es nuestro. |

## 3. Parámetros de diseño (🔴 sin estudio: se presentan como tales)

| Parámetro | Valor | Por qué existe | Sensibilidad (`VALIDACION.md`) |
|---|---|---|---|
| Pesos del puntaje | temperatura 0.40 · agua 0.30 · suelo 0.15 · prioridad 0.15 | Ordenar candidatos que ya son viables | ±50 % en cada peso: 86–99 % de los pasos no cambian |
| Misma familia botánica seguida | × 0.7 | Plagas y enfermedades compartidas (la dirección sí está respaldada por guías de extensión; el número no) | 97–100 % |
| No repetir un cultivo en la rotación | Excluido si hay otra opción (nunca el inmediato anterior) | Mismo motivo que la regla de familia: repetir la especie en 12 meses acumula sus plagas y enfermedades. Es filtro, no número | — |
| Fuera de su temporada habitual | × 0.9 | La temporada es preferencia, no filtro | 90–98 % |
| Cambio de sistema (granos ↔ hortalizas) | × 0.85 | Otro equipo, mano de obra y mercado | 85–97 % (el más influyente) |
| Suelo fuera de lo que tolera | textura × 0.5 · pH × 0.6 | Castigo, no descarte | — |
| Tolerancia de pH | óptimo de ECOCROP ± 0.5 | ECOCROP da el óptimo, no el absoluto | — |
| Factor de prioridad "rendimiento" | cereales, hortalizas, oleaginosas e industriales 1; otros 0.5 | No hay datos de precio ni de rendimiento por variedad | — |
| Índice de salud del suelo | 50 ± 10 por materia orgánica, +10 por leguminosa, +8 por cobertura, −10 por repetir familia | Va en la dirección que reporta la literatura (diversidad y leguminosas → mejor suelo), pero los puntos son nuestros | — |
| Umbral de 10 000 ha por país | | Que haya mercado e insumos | — |

## 4. Errores corregidos en esta revisión (2026-11-15)

1. **`T2M_MAX` y `T2M_MIN` mensuales son extremos, no promedios.** En el endpoint mensual de NASA POWER son la
   máxima más alta y la mínima más baja del mes. El código los trataba como "promedio de la máxima diaria". Eso
   inflaba la ET₀ de Hargreaves (raíz de un rango de temperatura casi el doble) y hacía ver heladas donde no las
   hay. Verificado con datos diarios de mayo de 2024 en Iowa: extremos de 28.96 / 5.63 °C contra diarias promedio
   de 23.6 / 11.1 °C. Ahora se usa `T2M ± T2M_RANGE/2` (23.8 / 11.3 °C).
2. **Cambio de modelo en los datos recientes de NASA POWER.** Desde octubre de 2026 los días recientes vienen de
   GEOS-IT en lugar de MERRA-2 (`header.sources`). La humedad del suelo salta de un mes a otro (Mexicali 0.45 → 0.14,
   Iowa 0.45 → 0.70); temperatura y lluvia siguen continuas. Ahora se detecta y no se compara.
3. **Ciclos encimados.** La rotación suponía un cultivo de 3 meses por temporada, pero los ciclos reales duran de 95
   a 188 días: dos pasos seguidos se encimaban en la misma parcela. Ahora es una línea de tiempo.
4. **Constantes sin fuente que se quitaron:** Kc promedio = 80 % del Kc medio, lluvia efectiva = 80 % fija,
   "40 % del N fijado queda en el suelo", base de 40 kg N/ha, márgenes de helada (2 °C) y calor (4 °C), umbrales de
   humedad del suelo 0.3 / 0.5, umbrales de lluvia −10 / −30 %, CV 15 / 30 %, y "suelo seco sube la incertidumbre".
5. **El modo demo mostraba números escritos a mano.** `frontend/src/api/mock.ts` ahora lo genera
   `backend/research/generar_mock.py` con una respuesta real del backend.

## 5. Limitaciones (decirlas siempre)

- Clima de una celda de ~55 km, no de la parcela. La lluvia es lo menos confiable de NASA POWER en zonas áridas.
- ECOCROP da rangos por especie, no por variedad. Un modelo mensual tipo EcoCrop no simula la latencia invernal de
  los cereales de invierno (trigo de Kansas: el motor lo descarta).
- Sin rendimiento ni economía (precios, costos), sin plagas locales (solo la regla de familia botánica).
- Sin balance de agua del suelo: el riego compara ETc contra la lluvia efectiva **del ciclo** y no cuenta el agua
  que el suelo ya guarda al sembrar. En zonas de temporal con suelos profundos (p. ej. el Medio Oeste de EE. UU.)
  sobrestima el riego; por eso el aviso dice «Puede requerir riego» y lo aclara.
- Pesos y castigos propios: medidos con sensibilidad, no calibrados con rendimientos.
- Validación con agricultores y agrónomos (INIFAP, extensionistas): **pendiente**. Ver `VALIDACION.md`.

## 6. Referencias

- Abdul Talib, S. A. et al. (2024). Irregularity and time series trend analysis of rainfall in Johor, Malaysia.
  *Heliyon* 10(9): e30324. https://doi.org/10.1016/j.heliyon.2024.e30324 (Tabla 2: clasificación del CV de la lluvia).
- Allen, R. G., Pereira, L. S., Raes, D. y Smith, M. (1998). *Crop evapotranspiration*. FAO Irrigation and Drainage
  Paper 56. https://www.fao.org/4/x0490e/x0490e00.htm (Tablas 11–12: https://www.fao.org/4/x0490e/x0490e0b.htm).
- Brouwer, C. y Heibloem, M. (1986). *Irrigation Water Management: Irrigation Water Needs*. FAO Training Manual 3.
  Cap. 2 (Tablas 4–5): https://www.fao.org/4/s2022e/s2022e02.htm · Cap. 3 (Tabla 6): https://www.fao.org/4/s2022e/s2022e03.htm
- FAO ECOCROP, copia pública: https://github.com/openclim/ecocrop
- FAOSTAT, Crops and livestock products (QCL), CC BY 4.0: https://www.fao.org/faostat/
- Herridge, D. F. et al. (2022). Global estimates of nitrogen fixation in grain legumes. *Plant and Soil*
  (coeficientes en Ludemann et al. 2024, suplemento Tabla S2).
- Hijmans, R. J. et al. (2001). DIVA-GIS (modelo EcoCrop). Implementación de referencia: función `ecocrop` del paquete
  R `dismo`, https://github.com/rspatial/dismo/blob/master/R/ecocrop.R
- India Meteorological Department: categorías de lluvia (normal ±19 %, deficiente −20 a −59 %, muy deficiente ≤ −60 %).
- ISRIC SoilGrids v2.0: https://rest.isric.org/soilgrids/v2.0/docs
- Kebede, E. (2021). Contribution, utilization, and improvement of legumes-driven biological nitrogen fixation in
  agricultural systems. *Frontiers in Sustainable Food Systems* 5: 767998.
- Ludemann, C. I. et al. (2024). A global FAOSTAT reference database of cropland nutrient budgets and nutrient use
  efficiency (1961–2020). *Earth System Science Data* 16: 525–541. https://doi.org/10.5194/essd-16-525-2024
- NASA POWER API: https://power.larc.nasa.gov/docs/services/api/
- Ramirez-Villegas, J., Jarvis, A. y Läderach, P. (2013). Empirical approaches for assessing impacts of climate change
  on agriculture: the EcoCrop model and a case study with grain sorghum. *Agricultural and Forest Meteorology* 170: 67–78.
- Svoboda, M. et al. (2002). The Drought Monitor. *Bulletin of the American Meteorological Society* 83(8): 1181–1190.
- University of Missouri Extension, G4256: Cotton fertility (N en el algodón con semilla).
  https://extension.missouri.edu/publications/g4256
