# Alcance geográfico: ¿México, Norteamérica, América o el mundo?

> Qué tan ambicioso es hacer la herramienta "para cualquier parte del mundo", cuánto trabajo cuesta cada nivel
> y qué recomendamos para el hackathon. Fecha: 2026-11-14. Ver también `INVESTIGACION-CULTIVOS.md`.

## Resumen

**Lo que ya funciona en todo el mundo:** el clima (NASA POWER), el suelo (SoilGrids), los rangos de cada cultivo
(FAO ECOCROP), el agua del cultivo (FAO-56) y los hemisferios. Si dibujas una parcela en Kenia, la herramienta
responde con datos reales.

**Lo que NO es global todavía:** *qué cultivos* se le ofrecen al usuario (18, de clima templado/subtropical,
elegidos pensando en México) y *cómo se definen las temporadas* (4 estaciones por temperatura, que no sirven en el
trópico ni en climas muy fríos).

**Recomendación:** presentarla como **"global por diseño, calibrada para Norteamérica (México, EE. UU., Canadá)"**.
Es alcanzable en 2–3 semanas y la historia es honesta: funciona en cualquier punto, y fuera de Norteamérica avisa
que la recomendación es orientativa.

## Qué ya es global y qué no

| Pieza | ¿Global? | Notas |
|---|---|---|
| Clima (NASA POWER) | ✅ | Malla 0.5° × 0.625° (~55 km). Temperatura confiable; **la lluvia es el punto débil**, sobre todo en zonas áridas y montaña ([validación en Omán](https://arxiv.org/pdf/2210.16111)). NASA ofrece IMERG (GPM) como alternativa de lluvia ([POWER, precipitación](https://power.larc.nasa.gov/docs/methodology/meteorology/precipitation/)). |
| Suelo (ISRIC SoilGrids) | ✅ con límites | ~250 m, todo el mundo, licencia CC BY 4.0. API en **beta**, sin garantía de disponibilidad, **5 consultas/min** ([FAQ ISRIC](https://docs.isric.org/globaldata/soilgrids/SoilGrids_faqs_02.html)). Sin dato en ciudades y agua. |
| Rangos de cultivos (ECOCROP) | ✅ | ~2 500 especies de todo el mundo; FAO lo descontinuó (~2015) pero los datos siguen disponibles ([OpenCLIM](https://github.com/openclim/ecocrop)). |
| Agua (FAO-56 + Hargreaves) | ✅ | Método estándar mundial; solo necesita Tmax/Tmin y latitud. |
| Hemisferios | ✅ | Las temporadas se invierten si `lat < 0`. |
| **Catálogo de cultivos** | ❌ | 18 cultivos templados. Faltan arroz, caña, yuca, café, plátano, remolacha, girasol, etc. |
| **Relevancia local** | ❌ | Hoy puede recomendar canola en Chiapas o algodón en un lugar donde nadie lo siembra. |
| **Temporadas** | ⚠️ | 4 estaciones por temperatura. En el trópico manda lluvia/secas; en Canadá hay **una** temporada de cultivo al año. |
| **Altitud** | ⚠️ | La celda de POWER promedia el terreno: en los Andes o el Altiplano la temperatura real puede estar varios °C más fría. |
| Idioma y unidades | ⚠️ | Solo español y sistema métrico. |
| Validación agronómica | ❌ | Solo se puede validar región por región (INIFAP, USDA, AAFC, INTA…). |

## Niveles de ambición y esfuerzo

Esfuerzo en **días-persona** (una persona, día completo), estimado para este equipo. Son órdenes de magnitud, no
compromisos.

### Nivel 0 — México (lo que hay hoy) ✅
Clima + suelo + ECOCROP + FAO-56 + 18 cultivos + barbecho + riego + heladas + pH. Ya funciona y está probado
con datos reales en Mexicali, Ensenada, San Quintín, el Bajío, Chiapas, Iowa, Saskatchewan y la Pampa.
**Falta:** validar 3–4 casos con guías de INIFAP (2–3 días).

### Nivel 1 — Norteamérica (MX + EE. UU. + Canadá) ⭐ recomendado · ~10–15 días-persona
| Tarea | Por qué | Esfuerzo |
|---|---|---|
| **Filtro de relevancia por país** con FAOSTAT: tabla país → cultivos con superficie cosechada > 0 | Que no recomiende lo que nadie siembra ahí. FAOSTAT QCL se descarga en bloque sin llave ([bulk QCL](https://bulks-faostat.fao.org/production/Production_Crops_Livestock_E_All_Data_NOFLAG.zip)). | 2–3 |
| País por coordenadas con **PostGIS** + límites de Natural Earth (dominio público) | Ya tenemos PostGIS: `ST_Contains(pais.geom, punto)`. | 1–2 |
| **Temporada de cultivo en climas fríos**: si el invierno es barbecho, la rotación es por año (1 cultivo/año), no por estación | En Canadá y el norte de EE. UU. se siembra una vez al año. | 2–3 |
| Agregar cultivos: remolacha, girasol, trigo duro, alfalfa (perenne, como "pradera") | Cultivos grandes de EE. UU./Canadá. Con `build_crops.py` es agregar renglones. | 1–2 |
| Inglés + unidades imperiales (acres, pulgadas, °F) | Usuarios de EE. UU. | 2–3 (frontend) |
| Validar con calendarios USDA/AAFC; opcional: cultivo real por punto en EE. UU. con CropScape (API sin llave, [ejemplos](https://nassgeodata.gmu.edu/CropScape/devhelp/getexamples.html)) y en Canadá con el [Annual Crop Inventory](https://open.canada.ca/data/en/dataset/ba2645d5-4458-414d-b196-6303ac06c1c9) | Comprobar que lo recomendado se parece a lo que se siembra. | 2–3 |

### Nivel 2 — Toda América · +15–25 días-persona sobre el nivel 1
| Tarea | Por qué | Esfuerzo |
|---|---|---|
| **Temporadas por lluvia** en el trópico (meses con lluvia > ET₀/2 = temporada de lluvias) | Entre los trópicos la temperatura casi no cambia; manda la lluvia. | 4–6 |
| **Corrección por altitud** (−6.5 °C por km entre la altura real, de SRTM, y la de la celda) | Andes, Altiplano, Sierra Madre. | 3–4 |
| Cultivos tropicales: arroz, yuca, caña, cacahuate, camote; perennes (café, cacao, plátano) aparte | No son rotación por temporada; requieren otro tipo de recomendación. | 4–6 |
| Lluvia con IMERG en vez de POWER en zonas tropicales | Mejor precisión de lluvia. | 3–4 |
| Portugués (Brasil) | Mercado agrícola más grande de la región. | 2–3 |

### Nivel 3 — Todo el mundo · ~2–3 meses
Todo lo anterior, más: listas de cultivos por región con **MapSPAM 2020** (46 cultivos a 10 km; requiere
formulario y limita la redistribución, [IFPRI](https://www.landcarbonlab.org/news-updates/crop-distribution-yields-spam-2020-model-map))
o aptitud de **FAO GAEZ v4/v5** (rásteres globales por cultivo, [GAEZ](https://www.fao.org/gaez/gaezv4/en)); climas con
**dos temporadas de lluvia** (África del Este, sur de Asia con monzón); más idiomas; y validación imposible de
cubrir → todo se etiqueta como orientativo.

## Qué conviene decir en el pitch
- "Funciona en cualquier punto del planeta con datos globales de **NASA POWER**, **FAO** e **ISRIC**."
- "Está calibrada y validada para Norteamérica; en otras regiones la recomendación es orientativa y lo
  indicamos en la incertidumbre."
- Evitar: "funciona igual de bien en todo el mundo" o "IA". Son reglas agronómicas transparentes con fuentes.

## Fuentes
- NASA POWER, precipitación: https://power.larc.nasa.gov/docs/methodology/meteorology/precipitation/
- Validación de NASA POWER en Omán (temperatura buena, lluvia mala en zona árida): https://arxiv.org/pdf/2210.16111
- ISRIC SoilGrids, acceso y límite de uso: https://docs.isric.org/globaldata/soilgrids/SoilGrids_faqs_02.html
- FAO ECOCROP (copia pública): https://github.com/openclim/ecocrop
- FAOSTAT QCL (descarga en bloque): https://bulks-faostat.fao.org/production/Production_Crops_Livestock_E_All_Data_NOFLAG.zip
- MapSPAM 2020: https://www.landcarbonlab.org/news-updates/crop-distribution-yields-spam-2020-model-map
- FAO GAEZ: https://www.fao.org/gaez/gaezv4/en
- USDA CropScape: https://nassgeodata.gmu.edu/CropScape/devhelp/getexamples.html
- AAFC Annual Crop Inventory: https://open.canada.ca/data/en/dataset/ba2645d5-4458-414d-b196-6303ac06c1c9
