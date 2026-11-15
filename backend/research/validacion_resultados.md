# Resultados de la validación del motor

Generado por `research/validar_motor.py` con clima real de NASA POWER (consulta del 15/11/2026). No editar a mano: volver a correr el script.

## 1. Calibración del margen de helada letal de EcoCrop

| Margen (°C) | Viables (cultivos reales) | Siembra en la ventana oficial | Descarta lo que no se siembra | Barbecho donde corresponde |
|---|---|---|---|---|
| 0 | 97 % (33/34) | 100 % (33/33) | 100 % (12/12) | 100 % (3/3) |
| 2.5 ← usado | 97 % (33/34) | 100 % (33/33) | 100 % (12/12) | 100 % (3/3) |
| 5 | 94 % (32/34) | 97 % (31/32) | 100 % (12/12) | 100 % (3/3) |

## 2. Cultivos que de verdad se siembran (margen = 2.5 °C)

| Lugar | Cultivo | Temporada | ¿Viable? | Aptitud | Siembra (motor) | Siembra (oficial) | ¿Coincide? | Fuente |
|---|---|---|---|---|---|---|---|---|
| Iowa (Ames) | Maíz | primavera | ✅ | 0.81 | May | Abr–May | ✅ | USDA NASS 2010, Usual Planting Dates: maíz, 25 abr – 18 may |
| Iowa (Ames) | Soya | primavera | ✅ | 0.64 | May | May–Jun | ✅ | USDA NASS 2010, Usual Planting Dates: soya, 8 may – 2 jun |
| Iowa (Ames) | Avena | primavera | ✅ | 0.54 | May | Abr–May | ✅ | USDA NASS 2010, Usual Planting Dates: avena de primavera, 2 abr – 2 may |
| Dakota del Norte (Jamestown) | Trigo | primavera | ✅ | 0.90 | May | Abr–May | ✅ | USDA NASS 2010, Usual Planting Dates: trigo de primavera, 24 abr – 25 may |
| Dakota del Norte (Jamestown) | Cebada | primavera | ✅ | 0.86 | May | Abr–May | ✅ | USDA NASS 2010, Usual Planting Dates: cebada de primavera, 26 abr – 25 may |
| Dakota del Norte (Jamestown) | Maíz | primavera | ✅ | 0.50 | May | May–May | ✅ | USDA NASS 2010, Usual Planting Dates: maíz, 2 – 28 may |
| Dakota del Norte (Jamestown) | Soya | primavera | ✅ | 0.40 | May | May–Jun | ✅ | USDA NASS 2010, Usual Planting Dates: soya, 14 may – 3 jun |
| Kansas (Salina) | Trigo | otoño | ❌ | 0.00 | — | Sep–Oct | — | USDA NASS 2010, Usual Planting Dates: trigo de invierno, 15 sep – 20 oct |
| Kansas (Salina) | Sorgo | verano | ✅ | 1.00 | Jun | May–Jun | ✅ | USDA NASS 2010, Usual Planting Dates: sorgo, 15 may – 20 jun |
| Kansas (Salina) | Maíz | primavera | ✅ | 1.00 | May | Abr–May | ✅ | USDA NASS 2010, Usual Planting Dates: maíz, 15 abr – 15 may |
| Kansas (Salina) | Soya | primavera | ✅ | 0.88 | May | May–Jun | ✅ | USDA NASS 2010, Usual Planting Dates: soya, 15 may – 20 jun |
| Arizona (Maricopa) | Trigo | invierno | ✅ | 0.66 | Dic | Dic–Dic | ✅ | USDA NASS 2010, Usual Planting Dates: trigo duro e invernal, 1 – 30 dic |
| Arizona (Maricopa) | Cebada | invierno | ✅ | 0.74 | Dic | Dic–Dic | ✅ | USDA NASS 2010, Usual Planting Dates: cebada de otoño, 1 – 30 dic |
| Arizona (Maricopa) | Algodón | primavera | ✅ | 1.00 | Abr – May | Abr–Abr | ✅ | USDA NASS 2010, Usual Planting Dates: algodón, 1 – 30 abr |
| Arizona (Maricopa) | Maíz | primavera | ✅ | 0.88 | Mar – May | Abr–May | ✅ | USDA NASS 2010, Usual Planting Dates: maíz, 1 abr – 15 may |
| California (Fresno) | Algodón | primavera | ✅ | 0.77 | May | Abr–May | ✅ | USDA NASS 2010, Usual Planting Dates: algodón, 10 abr – 5 may |
| California (Fresno) | Trigo | otoño | ✅ | 0.48 | Oct – Nov | Oct–Dic | ✅ | USDA NASS 2010, Usual Planting Dates: trigo invernal, 20 oct – 1 ene |
| California (Fresno) | Maíz | primavera | ✅ | 1.00 | May | Abr–Jul | ✅ | USDA NASS 2010, Usual Planting Dates: maíz, 1 abr – 1 jul |
| Valle de Mexicali (BC) | Trigo | otoño | ✅ | 0.84 | Nov | Nov–Dic | ✅ | SADER BC: trigo otoño-invierno (~38 000 ha, 2022-23) |
| Valle de Mexicali (BC) | Algodón | primavera | ✅ | 1.00 | Abr – May | Mar–Abr | ✅ | SADER BC: algodón primavera-verano |
| San Quintín (BC) | Jitomate | verano | ✅ | 0.87 | Jul | Mar–Jul | ✅ | SADER BC: hortalizas de la zona costa (jitomate) |
| Valle del Yaqui (Son.) | Trigo | otoño | ✅ | 0.95 | Nov | Nov–Dic | ✅ | SADER/Sonora: trigo otoño-invierno |
| Valle del Yaqui (Son.) | Cártamo | invierno | ✅ | 0.97 | Feb | Nov–Ene | ✅ | SADER/Sonora: reconversión OI 2025-26 a cártamo |
| Valle del Yaqui (Son.) | Canola | otoño | ✅ | 1.00 | Nov | Nov–Ene | ✅ | SADER/Sonora: reconversión OI 2025-26 a canola |
| Culiacán (Sin.) | Maíz | otoño | ✅ | 1.00 | Sep – Nov | Nov–Dic | ✅ | CEIEG Sinaloa: OI es el ciclo principal (maíz) |
| Culiacán (Sin.) | Frijol | otoño | ✅ | 1.00 | Nov | Oct–Dic | ✅ | CEIEG Sinaloa: frijol OI |
| Culiacán (Sin.) | Garbanzo | otoño | ✅ | 1.00 | Sep – Nov | Nov–Dic | ✅ | CEIEG Sinaloa: garbanzo OI |
| Bajío (Celaya, Gto.) | Sorgo | primavera | ✅ | 0.81 | Abr | May–Jul | ✅ | SADER Guanajuato: sorgo PV (~128 000 ha en 2025) |
| Bajío (Celaya, Gto.) | Trigo | invierno | ✅ | 1.00 | Feb | Nov–Ene | ✅ | Guanajuato: trigo OI de riego |
| Bajío (Celaya, Gto.) | Cebada | otoño | ✅ | 0.92 | Sep – Nov | Nov–Ene | ✅ | Guanajuato: cebada OI de riego |
| Saskatchewan (Saskatoon) | Trigo | primavera | ✅ | 0.80 | May | May–May | ✅ | Saskatchewan Crop Report (mayo 2026): trigo de primavera |
| Saskatchewan (Saskatoon) | Cebada | primavera | ✅ | 0.85 | May | May–May | ✅ | Saskatchewan Crop Report: cebada |
| Saskatchewan (Saskatoon) | Canola | primavera | ✅ | 0.80 | May | May–May | ✅ | Saskatchewan Crop Report: canola |
| Saskatchewan (Saskatoon) | Chícharo | primavera | ✅ | 1.00 | May | Abr–May | ✅ | Saskatchewan Crop Report: leguminosas (las primeras en sembrarse) |

## 3. Lo que NO se siembra por clima

| Lugar | Cultivo | Temporada | ¿Lo descarta? | Fuente |
|---|---|---|---|---|
| Iowa (Ames) | Algodón | primavera | ✅ | USDA: algodón solo al sur de ~36° N |
| Iowa (Ames) | Algodón | verano | ✅ | USDA: algodón solo al sur de ~36° N |
| Iowa (Ames) | Algodón | otoño | ✅ | USDA: algodón solo al sur de ~36° N |
| Iowa (Ames) | Algodón | invierno | ✅ | USDA: algodón solo al sur de ~36° N |
| Dakota del Norte (Jamestown) | Algodón | primavera | ✅ | USDA: algodón solo al sur de ~36° N |
| Dakota del Norte (Jamestown) | Algodón | verano | ✅ | USDA: algodón solo al sur de ~36° N |
| Dakota del Norte (Jamestown) | Algodón | otoño | ✅ | USDA: algodón solo al sur de ~36° N |
| Dakota del Norte (Jamestown) | Algodón | invierno | ✅ | USDA: algodón solo al sur de ~36° N |
| Saskatchewan (Saskatoon) | Algodón | primavera | ✅ | Sin algodón en las praderas canadienses |
| Saskatchewan (Saskatoon) | Algodón | verano | ✅ | Sin algodón en las praderas canadienses |
| Saskatchewan (Saskatoon) | Algodón | otoño | ✅ | Sin algodón en las praderas canadienses |
| Saskatchewan (Saskatoon) | Algodón | invierno | ✅ | Sin algodón en las praderas canadienses |

## 4. Barbecho en inviernos sin agricultura

| Lugar | Temporada | ¿Propone barbecho? | Cultivos que aún ve viables | Fuente |
|---|---|---|---|---|
| Iowa (Ames) | invierno | ✅ | — | Sin cultivos en invierno (USDA: siembras de abr a jun) |
| Dakota del Norte (Jamestown) | invierno | ✅ | — | Sin cultivos en invierno |
| Saskatchewan (Saskatoon) | invierno | ✅ | — | Sin cultivos en invierno |

## 5. Sensibilidad de los parámetros de diseño

Rotaciones comparadas: 11 lugares × 3 prioridades × 3 temporadas. Se mueve un parámetro a la vez (los pesos se renormalizan para sumar 1).

| Parámetro | Cambio | Pasos de la rotación que NO cambian |
|---|---|---|
| `W_TEMP` | ×0.5 | 87 % |
| `W_TEMP` | ×1.5 | 98 % |
| `W_WATER` | ×0.5 | 96 % |
| `W_WATER` | ×1.5 | 94 % |
| `W_SOIL` | ×0.5 | 99 % |
| `W_SOIL` | ×1.5 | 96 % |
| `W_PRIORITY` | ×0.5 | 96 % |
| `W_PRIORITY` | ×1.5 | 91 % |
| `SAME_FAMILY_PENALTY` | 0.70 → 0.55 | 100 % |
| `SAME_FAMILY_PENALTY` | 0.70 → 0.85 | 98 % |
| `OUT_OF_SEASON_PENALTY` | 0.90 → 0.85 | 98 % |
| `OUT_OF_SEASON_PENALTY` | 0.90 → 0.95 | 91 % |
| `SYSTEM_CHANGE_PENALTY` | 0.85 → 0.75 | 98 % |
| `SYSTEM_CHANGE_PENALTY` | 0.85 → 0.95 | 87 % |

Promedio: **95 %** de los pasos se mantienen.
