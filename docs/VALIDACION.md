# Validación del motor de reglas

> Cómo comprobamos que el motor no inventa: lo contrastamos con **calendarios oficiales de siembra** usando **clima
> real de NASA POWER**. Fecha: 2026-11-15. Resultados completos (tablas por caso):
> [`backend/research/validacion_resultados.md`](../backend/research/validacion_resultados.md), generados por
> [`backend/research/validar_motor.py`](../backend/research/validar_motor.py). Fuentes de cada número del motor:
> [`METODOLOGIA.md`](METODOLOGIA.md).

## 1. Qué se validó y qué no

| Sí se validó | Todavía no |
|---|---|
| Las fórmulas (Penman-Monteith, radiación, presión, lluvia efectiva, curva Kc) contra los **ejemplos resueltos de FAO-56** y la Tabla 6 de la FAO (`tests/test_fao56.py`) | Rendimientos reales en parcelas |
| Que el motor considere viable lo que **de verdad se siembra** en 11 regiones (34 casos) y descarte lo que no | Opinión de agricultores y agrónomos (INIFAP, extensionistas) |
| Que la **fecha de siembra** que sugiere coincida con la oficial | Economía (precios, costos) y plagas locales |
| Que proponga **descanso** en inviernos sin agricultura | |
| Cuánto cambian las rotaciones si se mueven los **parámetros de diseño** (sensibilidad) | |

Es una **validación de plausibilidad agroclimática**, no una validación de campo. Se dice así en el pitch.

## 2. Casos de referencia (fuentes oficiales)

| Región | Cultivos y temporada de siembra | Fuente |
|---|---|---|
| Iowa (Ames) | maíz, soya y avena en primavera; invierno sin cultivos; sin algodón | USDA NASS (2010), *Field Crops Usual Planting and Harvesting Dates*, Agricultural Handbook 628 |
| Dakota del Norte (Jamestown) | trigo y cebada de primavera, maíz, soya; invierno sin cultivos; sin algodón | USDA NASS (2010) |
| Kansas (Salina) | trigo de invierno (otoño), sorgo, maíz, soya | USDA NASS (2010) |
| Arizona (Maricopa) | trigo y cebada en diciembre, algodón y maíz en abril | USDA NASS (2010) |
| California (Fresno) | algodón (abr–may), trigo de invierno (oct–dic), maíz | USDA NASS (2010) |
| Valle de Mexicali (BC) | trigo otoño-invierno, algodón primavera-verano | SADER Baja California |
| San Quintín (BC) | jitomate (hortalizas de la zona costa) | SADER Baja California |
| Valle del Yaqui (Son.) | trigo, cártamo y canola en otoño-invierno | SADER / Gobierno de Sonora (reconversión OI 2025-26) |
| Culiacán (Sin.) | maíz, frijol y garbanzo en otoño-invierno (el ciclo principal) | Gobierno de Sinaloa, CEIEG |
| Bajío (Celaya, Gto.) | sorgo primavera-verano; trigo y cebada otoño-invierno | SADER Guanajuato |
| Saskatchewan (Saskatoon) | trigo, cebada, canola y chícharo en mayo; invierno sin cultivos; sin algodón | Saskatchewan Ministry of Agriculture, *Crop Report* (mayo 2026) |

URL del manual del USDA: https://esmis.nal.usda.gov/publication/usual-planting-and-harvesting-dates-us-field-crops/2010-10-29

## 3. Resultados

Con el margen de helada usado (2.5 °C):

| Prueba | Resultado |
|---|---|
| ¿Considera viable lo que de verdad se siembra? | **97 %** (33 de 34) |
| ¿Su fecha de siembra cae en la ventana oficial (± 1 mes)? | **100 %** (33 de 33) |
| ¿Descarta lo que no se siembra por clima? (algodón en Iowa, Dakota del Norte y Saskatchewan, las 4 temporadas) | **100 %** (12 de 12) |
| ¿Propone descanso en inviernos sin agricultura? (Iowa, Dakota del Norte, Saskatchewan) | **100 %** (3 de 3) |

**El caso que falla: el trigo de invierno de Kansas.** Se siembra en otoño y pasa el invierno dormido bajo la nieve
(endurecimiento y vernalización). Un modelo mensual tipo EcoCrop no simula esa dormancia y lo ve como muerto por
helada. Es una limitación conocida del modelo y se declara.

### Calibración del margen de helada letal (EcoCrop)

| Margen | Viables | Fecha correcta | Descarta lo que no se siembra | Descanso correcto |
|---|---|---|---|---|
| 0 °C | 97 % | 100 % | 100 % | 100 % |
| **2.5 °C (usado)** | **97 %** | **100 %** | **100 %** | **100 %** |
| 5 °C (valor de `dismo::ecocrop`) | 94 % | 97 % | 100 % | 100 % |

Con 5 °C el motor descarta el trigo y la cebada de diciembre en Arizona, que sí se siembran. 0 y 2.5 °C empatan; se
eligió 2.5 °C para conservar un margen de seguridad frente a la mínima media mensual. Es un parámetro **calibrado**,
no tomado de un artículo.

### Sensibilidad de los parámetros de diseño

11 lugares × 3 prioridades × 3 pasos de rotación. Se movió un parámetro a la vez: cada peso ×0.5 y ×1.5 (los pesos se
renormalizan para sumar 1) y cada castigo hacia arriba y hacia abajo.

- **En promedio, el 95 % de los pasos de la rotación no cambia.**
- Los más influyentes: el castigo por cambio de sistema (0.85 → 0.95 deja igual el 87 %) y el peso de la temperatura
  a la mitad (87 %). Tiene sentido: deciden si se propone pasar de granos a hortalizas y cuánto pesa el clima.
- Lo menos influyente: el peso del suelo y el castigo por repetir familia (95–100 %).

Conclusión: las recomendaciones dependen sobre todo de los datos (clima, ciclo, agua) y no de los números que
elegimos nosotros.

## 4. Hallazgos durante la validación

La validación encontró dos problemas reales en los datos, que ya están corregidos (detalle en `METODOLOGIA.md` §4):

1. **En el endpoint mensual de NASA POWER, `T2M_MAX` y `T2M_MIN` son extremos del mes, no promedios.** Con los
   extremos, el motor veía heladas letales en mayo en Iowa y descartaba el maíz (la viabilidad bajaba a 41 %). Con la
   media diaria correcta (`T2M ± T2M_RANGE/2`) sube a 97 %.
2. **Desde oct-2026 NASA POWER calcula los días recientes con otro modelo (GEOS-IT)** y la humedad del suelo no es
   continua con el histórico de MERRA-2. Ahora se detecta con `header.sources` y no se compara.

## 5. Cómo reproducirlo

```bash
docker compose up -d                                         # backend y BD
docker compose exec backend pytest -q                        # 148 pruebas (incluye ejemplos de FAO-56)
docker compose exec backend python research/validar_motor.py # ~1 min, escribe research/validacion_resultados.md
python backend/research/generar_mock.py                      # regenera el modo demo con datos reales
```

## 6. Siguiente paso

Validación con personas: revisar 3–4 casos de Baja California con un agrónomo de INIFAP o un extensionista (fechas
de siembra locales, variedades, plagas) y con productores del valle de Mexicali y de la zona costa.
