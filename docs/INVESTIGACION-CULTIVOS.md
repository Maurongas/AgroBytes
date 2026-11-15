# Investigación: cultivos, datos y reglas de recomendación

> Guía para decidir **qué cultivos** maneja la herramienta, **de dónde sale cada número** y **cómo mejorar las
> recomendaciones**. Fecha: 2026-11-14. Complementa `ARQUITECTURA.md` §6 (modelo) y §7 (motor de reglas).

> **Estado (2026-11-14, rama `feature/back-catalogo-v2`):** implementado lo de las secciones 3–5 en el backend:
> catálogo de **18 cultivos** generado por `backend/research/build_crops.py` (16 de la propuesta + canola y papa,
> para Norteamérica), migración `a3f1c2d4e5b6`, riego, barbecho, familia botánica, heladas, pH, agua FAO-56 y suelo
> con SoilGrids (`GET /api/v1/soil`). La temporada pasó de filtro a preferencia y se agregó la regla de sistema de
> producción (granos ↔ hortalizas). Lo que falta en la UI: `FRONTEND-PENDIENTES.md`. Alcance mundial: `ALCANCE-GEOGRAFICO.md`.

> **Actualización (2026-11-15, v2.3):** este documento es el **diagnóstico histórico**. Lo vigente está en
> [`METODOLOGIA.md`](METODOLOGIA.md) (fuente y nivel de respaldo de cada número) y [`VALIDACION.md`](VALIDACION.md)
> (contraste con calendarios oficiales). Cambios respecto a lo que dice abajo: el nitrógeno ya no es "40 % de lo
> fijado" sino fijación (Herridge et al. 2022) − extracción por la cosecha (Ludemann et al. 2024) con el rendimiento
> FAOSTAT del país; la ET₀ es Penman-Monteith (Hargreaves solo como plan B); el Kc sigue la curva de 4 etapas de
> FAO-56; la lluvia efectiva sale de la Tabla 6 de la FAO; la aptitud por temperatura es el modelo EcoCrop sobre
> todo el ciclo; y la rotación es una línea de tiempo sin ciclos encimados.

---

## 1. Diagnóstico: de dónde salieron los 8 cultivos actuales

| Pregunta | Respuesta honesta |
|---|---|
| ¿Quién eligió `maize, wheat, soy, bean, chile, tomato, oat, sorghum`? | Se eligieron a mano al definir la arquitectura (commit `89e4688`); la primera lista tenía `alfalfa` y no tenía soya/chile/tomate. **No hay un criterio documentado** (ni regional ni agronómico). |
| ¿De dónde salen los números de `crops.json`? | Daniel puso `source: "FAO ECOCROP (...)"`. Al compararlo con la base ECOCROP real, **las temperaturas se parecen pero no coinciden**, y `water_need_mm` **no viene de ECOCROP** (ECOCROP da lluvia *anual*, no por ciclo). |
| ¿Y el nitrógeno? | `nitrogen_delta_kg_ha` no tiene fuente. Son valores razonables a ojo. |
| ¿Y las reglas del motor? | Son heurísticas propias (pesos 40/30/15/15, castigo ×0.7 por repetir familia). No vienen de un estudio; hay que presentarlas como **reglas simplificadas**. |

### Comparación `crops.json` vs. ECOCROP (FAO) original

Temperaturas en °C (óptimo / absoluto). ECOCROP extraído de la copia pública `EcoCrop_DB.csv`
([OpenCLIM/ecocrop](https://github.com/openclim/ecocrop)); FAO descontinuó el portal original en ~2015.

| Cultivo | ECOCROP óptimo | Nuestro óptimo | ECOCROP absoluto | Nuestro absoluto | Diferencia importante |
|---|---|---|---|---|---|
| Maíz | 18–33 | 18–30 | 10–47 | 10–40 | máximos recortados |
| Trigo | 15–23 | 15–23 | 5–27 | 4–32 | máx. absoluto inflado (+5) |
| Soya | 20–33 | 20–30 | 10–38 | 10–38 | ok |
| Frijol | 16–25 | 16–27 | 7–32 | 10–35 | rango desplazado |
| Chile | 17–30 | 18–28 | 8–35 | 10–36 | ok aprox. |
| Jitomate | 20–27 | 18–27 | 7–35 | — | (en ECOCROP como *Lycopersicon esculentum*) |
| Avena | **16–20** | **12–22** | 5–30 | 2–30 | óptimo mucho más ancho → por eso la avena gana casi siempre en invierno |
| Sorgo | 22–35 | 22–34 | 8–40 | 12–42 | ok aprox. |

**Agua por ciclo** (FAO, *Irrigation Water Management*, cap. 2, [Tabla 5](https://www.fao.org/4/s2022e/s2022e02.htm)), mm por ciclo completo:

| Cultivo | FAO (rango) | Nuestro `water_need_mm` |
|---|---|---|
| Maíz | 500–800 | 550 |
| Trigo / avena / cebada | 450–650 | 450 / 350 (avena por debajo del rango FAO) |
| Frijol | 300–500 | 380 |
| Soya | 450–700 | 500 |
| Chile (pimiento) | 600–900 | 600 |
| Jitomate | 400–800 | 650 |
| Sorgo | 450–650 | 400 (por debajo del rango FAO) |

**Conclusión:** el catálogo hay que **rehacerlo con una fuente por campo** (sección 4). Los valores actuales
funcionan para una demo, pero no se pueden defender ante un jurado ni ante un agricultor.

---

## 2. Por qué la recomendación sale casi igual en todos lados

Medido el 2026-11-14 con NASA POWER real en 5 lugares (Ensenada, Chiapas, Bajío, Iowa, Pampa):

1. **Invierno solo tiene 2 opciones** (avena, trigo) y la avena tiene un rango óptimo inflado y la menor
   necesidad de agua → gana casi siempre.
2. **Encadenamiento**: avena (cereal) → castiga cereales en primavera → gana frijol (leguminosa) → castiga
   leguminosas en verano → gana sorgo. Resultado típico: **avena → frijol → sorgo**.
3. **La lluvia domina en zonas secas**: en el norte de México la lluvia no cubre a nadie, así que gana quien
   gasta menos agua. Pero en Baja California (clima desértico) **la mayor parte de la agricultura es de riego** → el factor lluvia
   está midiendo algo que al agricultor no le importa.
4. **Bug**: si ningún cultivo tolera la temperatura (invierno en Iowa) recomienda uno igual (chile en invierno).
   Debería recomendar **barbecho / descanso**.
5. **Familias mal definidas**: `family` mezcla uso (`vegetable`) con botánica. Chile y jitomate son ambos
   **Solanáceas** y comparten plagas/enfermedades, pero el motor los trata como distintos... o como iguales a
   cualquier "vegetable". La regla de rotación debe usar la **familia botánica**.

---

## 3. Qué cultivos conviene tener (propuesta)

Criterios: (a) que se siembren de verdad en México/Baja California, (b) que cubran **todas las temporadas**,
sobre todo invierno, (c) que haya **leguminosas de invierno** para romper el ciclo, (d) datos disponibles en
ECOCROP y FAO.

Lo que se siembra en Baja California (SIAP/SADER):
- **Trigo y alfalfa** predominan en el estado ([SIAP, Panorama de la frontera agrícola BC 2023](https://www.gob.mx/cms/uploads/attachment/file/807680/Panorama_FA_2023_BCN.pdf)).
- Valle de Mexicali: **trigo** en otoño-invierno (~38 000 ha en 2022-23,
  [SADER](https://www.gob.mx/agricultura/bajacalifornia/es/articulos/alcanzo-superficie-triguera-cumplimiento-del-97-con-la-siembra-de-37-mil-935-hectareas)),
  **algodón** en primavera-verano ([SADER](https://www.gob.mx/agricultura/bajacalifornia/articulos/aumenta-la-superficie-sembrada-del-ciclo-primavera-verano-2023-en-mexicali)).
- Alfalfa: cultivo perenne más grande de BC, 41 146 ha ([INEGI, Censo Agropecuario 2022](https://www.inegi.org.mx/contenidos/saladeprensa/boletines/2023/CA_Def/CA_Def2022_BC.pdf)).
- Zona costa (Ensenada / San Quintín): hortalizas (jitomate, chile, fresa, pepino), ~21 000 ha
  ([SADER](https://www.gob.mx/agricultura/bajacalifornia/articulos/reporta-agricultura-el-establecimiento-de-20-975-hectareas-en-la-zona-costa-de-bc)).

### Catálogo propuesto (16 cultivos)

Valores de ECOCROP (`EcoCrop_DB.csv`). Agua y ciclo: FAO Tablas 4 y 5. "Helada" = temperatura que mata la
planta joven (`KTMP` de ECOCROP; NA = no reportado).

| id | Nombre | Familia botánica | Rol en rotación | Temporada típica (norte) | T. óptima | T. absoluta | Helada | Agua FAO (mm) | Ciclo FAO (días) |
|---|---|---|---|---|---|---|---|---|---|
| `wheat` | Trigo | Poaceae | cereal | otoño-invierno | 15–23 | 5–27 | 0 | 450–650 | 120–150 |
| `barley` | Cebada | Poaceae | cereal | otoño-invierno | 15–20 | 2–40 | 0 | 450–650 | 120–150 |
| `oat` | Avena | Poaceae | cereal / forraje | otoño-invierno | 16–20 | 5–30 | −1 | 450–650 | 120–150 |
| `maize` | Maíz | Poaceae | cereal | primavera-verano | 18–33 | 10–47 | NA | 500–800 | 125–180 |
| `sorghum` | Sorgo | Poaceae | cereal | primavera-verano | 22–35 | 8–40 | NA | 450–650 | 120–130 |
| `chickpea` | Garbanzo | Fabaceae | **leguminosa de invierno** | otoño-invierno | 15–29 | 7–35 | 0 | 350–500* | 90–180† |
| `vetch` | Veza (abono verde) | Fabaceae | **cobertura de invierno** | otoño-invierno | 14–23 | 3–28 | −1 | — | 80–170† |
| `pea` | Chícharo | Fabaceae | leguminosa de invierno | otoño-invierno | 10–24 | 4–30 | 0 | 350–500 | 90–100 |
| `bean` | Frijol | Fabaceae | leguminosa | primavera-verano | 16–25 | 7–32 | NA | 300–500 | 95–110 |
| `soy` | Soya | Fabaceae | leguminosa | primavera-verano | 20–33 | 10–38 | NA | 450–700 | 135–150 |
| `cotton` | Algodón | Malvaceae | industrial | primavera-verano | 22–36 | 15–42 | NA | 700–1300 | 180–195 |
| `safflower` | Cártamo | Asteraceae | oleaginosa (tolera sequía) | otoño-invierno | 20–32 | 5–45 | −2 | — | 120–245† |
| `onion` | Cebolla | Amaryllidaceae | hortaliza | otoño-invierno | 12–25 | 4–30 | NA | 350–550 | 150–210 |
| `tomato` | Jitomate | **Solanaceae** | hortaliza | primavera-verano | 20–27 | 7–35 | NA | 400–800 | 135–180 |
| `chile` | Chile | **Solanaceae** | hortaliza | primavera-verano | 17–30 | 8–35 | NA | 600–900 | 120–210 |
| `squash` | Calabaza | Cucurbitaceae | hortaliza | primavera-verano | 17–30 | 6–40 | NA | — | 95–120 |

\* FAO no lista garbanzo; se usa el rango de chícharo/legumbres. † Ciclo de ECOCROP (FAO no lo lista).
"—" = no está en la tabla FAO; calcularlo con el método Kc (sección 5.4).

**Alfalfa**: es perenne (3–4 años), no entra en una rotación por temporada. Si se quiere, se ofrece como
"pradera de varios años" en una versión posterior.

Con esto, el invierno pasa de 2 opciones a **8** (trigo, cebada, avena, garbanzo, veza, chícharo, cártamo,
cebolla) y hay leguminosas en ambas temporadas, así que la cadena avena → frijol → sorgo deja de ser forzada.

---

## 4. De dónde debe salir cada campo del catálogo

| Campo | Fuente recomendada | Cómo obtenerlo |
|---|---|---|
| `temp_opt_min/max`, `temp_abs_min/max` | FAO ECOCROP (`TOPMN, TOPMX, TMIN, TMAX`) | `EcoCrop_DB.csv` de OpenCLIM; buscar por nombre científico |
| `frost_kill_c` (nuevo) | ECOCROP `KTMP` | mismo CSV |
| `ph_min/max` (nuevo, opcional) | ECOCROP `PHOPMN, PHOPMX` | mismo CSV |
| `family` | **Familia botánica** (ECOCROP `FAMNAME`) | Poaceae, Fabaceae, Solanaceae… |
| `role` (nuevo) | Propio, documentado | cereal / leguminosa / cobertura / hortaliza / industrial |
| `cycle_days` | FAO Tabla 4 (punto medio) | [fao.org/4/s2022e/s2022e02.htm](https://www.fao.org/4/s2022e/s2022e02.htm) |
| `water_need_mm` | FAO Tabla 5 (punto medio) — o mejor, Kc × ET₀ (5.4) | misma página |
| `kc_mid` (nuevo, opcional) | FAO-56 Tabla 12 | [fao.org/4/x0490e/x0490e0b.htm](https://www.fao.org/4/x0490e/x0490e0b.htm) |
| `seasons` | Ciclos SIAP (otoño-invierno / primavera-verano) + calendario FAO | [FAO Crop Calendar](https://cropcalendar.apps.fao.org/) |
| `soils` | ECOCROP `TEXT` (light / medium / heavy → sandy / loam / clay) | mismo CSV |
| `nitrogen_delta_kg_ha` | Literatura de fijación biológica (ver abajo) | marcar siempre como **estimado** |
| `source` | Texto con **todas** las fuentes usadas por ese cultivo | p. ej. `"ECOCROP; FAO IWM T4-T5"` |

**Nitrógeno fijado por leguminosas** (por temporada; varía muchísimo con suelo y manejo):
frijol 16–72 kg N/ha (fija poco), garbanzo 21–104, soya ~90–95 (EE. UU.), veza común 107–131
([Kebede 2021, *Frontiers in Sustainable Food Systems*, Tabla 1](https://www.frontiersin.org/articles/10.3389/fsufs.2021.767998/pdf)).
Ojo: si se **cosecha el grano**, buena parte de ese N sale con la cosecha; el aporte neto al suelo es menor.
Las coberturas (veza) que se incorporan al suelo son las que más aportan.

---

## 5. Mejoras al motor de reglas (en orden de impacto)

### 5.1 Preguntar si la parcela tiene riego ⭐ (lo que más mejora la utilidad)
En BC la mayor parte es de riego. Con riego, la lluvia no debe pesar 30 %; lo que importa es **cuánta agua de riego
hará falta** (ya lo calculamos en "Riego necesario"). Propuesta: campo `irrigation: boolean` en el request;
con riego, el factor agua pasa a "eficiencia de agua" (menos riego = mejor) y la lluvia solo informa.

### 5.2 Barbecho cuando nada tolera el clima
Si ningún cultivo tiene `temp_f > 0` en una temporada → paso de rotación `cropId: "fallow"` ("Descanso /
barbecho") con su razón ("Invierno demasiado frío: −5 °C de media"). Requiere agregar `fallow` al frontend.

### 5.3 Regla de familia botánica + heladas
- Castigar repetir **familia botánica** (Solanaceae → Solanaceae es lo peor: jitomate después de chile).
- **Heladas**: NASA POWER tiene `T2M_MIN` (mínima mensual) y `FROST_DAYS`. Si la mínima de la temporada
  baja de `frost_kill_c` del cultivo → descartarlo o marcar riesgo alto. Más preciso que la media.

### 5.4 Agua según el clima del lugar (método FAO-56)
Hoy `water_need_mm` es fijo. FAO-56 calcula **ETc = Kc × ET₀**: el mismo maíz necesita mucha más agua en
Mexicali que en Ensenada. ET₀ se puede estimar con **Hargreaves** usando `T2M_MAX`, `T2M_MIN` de NASA POWER
(ya los descargamos) y la radiación extraterrestre (fórmula por latitud), o con Penman-Monteith usando además
`RH2M`, `WS2M` y `ALLSKY_SFC_SW_DWN` (verificado: POWER los da en la comunidad AG).

### 5.5 Suelo automático con SoilGrids (ISRIC)
API gratuita sin llave que da arcilla, arena y pH por punto:
`https://rest.isric.org/soilgrids/v2.0/properties/query?lon=..&lat=..&property=clay&property=sand&property=phh2o&depth=0-5cm&value=mean`
(valores ×10: `clay=401` → 40.1 %, `phh2o=79` → pH 7.9). Probado: Mexicali → arcilloso pH 7.9; Valle de
Guadalupe → franco-arenoso pH 6.9; en zonas urbanas devuelve `null` (usar lo que elija el usuario).
Así el usuario no tiene que saber su textura de suelo, y se puede usar el pH contra `ph_min/max`.

### 5.6 Trópico
Cerca del ecuador las "estaciones" por temperatura casi no existen; lo que manda es **lluvia vs. secas**.
A futuro: en latitudes < ~23° definir temporadas por lluvia (meses con lluvia > ET₀/2).

---

## 6. Plan sugerido

| # | Tarea | Quién | Esfuerzo |
|---|---|---|---|
| 1 | Script que genere `crops.json` desde `EcoCrop_DB.csv` + tablas FAO, con `source` por cultivo | Backend | ✅ |
| 2 | Ampliar catálogo (18 cultivos) + migración + `lib/crops.ts` | Backend/DBA | ✅ (selector en UI: pendiente) |
| 3 | Barbecho + regla de familia botánica + heladas con `T2M_MIN` | Backend | ✅ |
| 4 | Pregunta de riego (contrato §5 + `QuickPanel`) | Backend ✅ + Mapa | UI pendiente |
| 5 | Suelo automático con SoilGrids | Backend ✅ + Mapa | UI pendiente |
| 6 | Agua con Kc × ET₀ (Hargreaves) | Backend | ✅ |
| 7 | Validar 3–4 casos con un agrónomo / guías INIFAP de BC (fechas de siembra locales) | Equipo | pendiente |

## 7. Cómo presentarlo (honestidad)

- Es una herramienta de **orientación** (screening), no una prescripción agronómica.
- Clima: **NASA POWER** (real). Rangos de cultivos: **FAO ECOCROP** y **FAO** (manual de riego, FAO-56).
  Suelo (si se agrega): **ISRIC SoilGrids**. Nitrógeno y salud del suelo: **estimaciones por reglas**.
- Las reglas son simplificadas y conviene validarlas con INIFAP o un agrónomo local.

## Fuentes
- FAO ECOCROP (copia pública): https://github.com/openclim/ecocrop · portal FAO: https://www.fao.org/land-water/resources/tools/databases/ecocrop/en
- FAO, *Irrigation Water Management: Training Manual 3*, cap. 2 (Tablas 4 y 5): https://www.fao.org/4/s2022e/s2022e02.htm
- FAO-56, *Crop evapotranspiration*, Tabla 12 (Kc): https://www.fao.org/4/x0490e/x0490e0b.htm
- FAO Crop Calendar: https://cropcalendar.apps.fao.org/
- Kebede (2021), fijación biológica de N: https://www.frontiersin.org/articles/10.3389/fsufs.2021.767998/pdf
- ISRIC SoilGrids v2.0 API: https://rest.isric.org/soilgrids/v2.0/docs
- SIAP / SADER / INEGI (Baja California): enlaces en la sección 3.
- Rotación por familias (extensión universitaria): https://uthort.tennessee.edu/wp-content/uploads/sites/228/2024/01/W235-E-rotation.pdf
