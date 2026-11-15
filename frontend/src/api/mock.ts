// GENERADO por backend/research/generar_mock.py — no editar a mano.
// Respuesta real de POST /api/v1/analyses?guardar=false del 15/11/2026: NASA POWER + SoilGrids + motor
// de reglas. Parcela y petición = las de la demo en vivo de la presentación (valle de Mexicali, maíz,
// prioridad agua). Para actualizarlo: levanta el backend y corre `python backend/research/generar_mock.py`.
import type { AnalysisResponse, AnalysisSummary } from './types';

export const mockAnalysis: AnalysisResponse = {
  "id": "demo-001",
  "createdAt": "2026-11-15T18:00:00Z",
  "areaHa": 8.37,
  "location": {
    "lat": 32.54999,
    "lon": -115.25005
  },
  "country": "MX",
  "metrics": [
    {
      "id": "soilMoisture",
      "label": "Humedad del suelo",
      "value": 0.14,
      "unit": "0–1",
      "status": "ok",
      "meaning": "No se compara con el histórico: NASA POWER calculó los días recientes con otro modelo (GEOSIT) y la humedad del suelo no es continua con MERRA-2",
      "series": [
        0.466,
        0.463,
        0.461,
        0.452,
        0.45,
        0.45,
        0.45,
        0.451,
        0.453,
        0.453,
        0.454,
        0.462
      ],
      "source": "NASA POWER · 11/08–08/11/2026"
    },
    {
      "id": "rain90d",
      "label": "Lluvia 90 días",
      "value": 48.0,
      "unit": "mm",
      "status": "ok",
      "meaning": "Temporada normalmente seca (lo normal es 23 mm): esa lluvia casi no la aprovecha el cultivo (FAO)",
      "series": [
        13.2,
        7.4,
        10.5,
        2.7,
        1.3,
        0.1,
        3.0,
        8.6,
        11.6,
        3.3,
        7.8,
        11.9
      ],
      "source": "NASA POWER · 11/08–08/11/2026"
    },
    {
      "id": "tempMean",
      "label": "Temperatura media",
      "value": 23.5,
      "unit": "°C",
      "status": "ok",
      "meaning": "0.2 °C bajo lo normal (0.1 desviaciones estándar)",
      "series": [
        13.09,
        15.21,
        18.27,
        23.05,
        26.16,
        31.79,
        35.36,
        35.31,
        31.3,
        25.49,
        18.87,
        13.97
      ],
      "source": "NASA POWER · 11/08–08/11/2026"
    },
    {
      "id": "solarRadiation",
      "label": "Radiación solar",
      "value": 5.9,
      "unit": "kWh/m²/día",
      "status": "ok",
      "meaning": "Alta: buena para cultivos de sol",
      "series": [
        3.59,
        4.67,
        5.91,
        7.36,
        8.16,
        8.38,
        7.66,
        7.1,
        6.14,
        5.18,
        3.86,
        3.2
      ],
      "source": "NASA POWER · 2016-2025"
    }
  ],
  "rotation": [
    {
      "season": "winter",
      "cropId": "pea",
      "score": 66,
      "reasons": [
        "Todo su ciclo (Ene–Mar) cae en su rango óptimo de temperatura (ECOCROP)",
        "Necesita 65 % menos agua que maíz",
        "Leguminosa: fija nitrógeno del aire (estimado)"
      ],
      "waterSavingPct": 65.0,
      "nitrogenDelta": 8.0,
      "risks": [
        "Requiere riego: la lluvia cubre ~0 % de lo que necesita"
      ],
      "plantingWindow": "Dic – Feb",
      "irrigationMm": 316.0
    },
    {
      "season": "spring",
      "cropId": "sorghum",
      "score": 57,
      "reasons": [
        "Tolera las temperaturas de su ciclo (May–Ago)",
        "Es de los 5 cultivos más sembrados en México (FAOSTAT): hay mercado e insumos",
        "Necesita 20 % menos agua que maíz"
      ],
      "waterSavingPct": 20.0,
      "nitrogenDelta": -52.0,
      "risks": [
        "Calor: en jul la temperatura media (~35 °C) pasa su óptimo (35 °C, ECOCROP); el rendimiento puede bajar: siembra temprano o elige una variedad tolerante",
        "Requiere riego: la lluvia cubre ~0 % de lo que necesita"
      ],
      "plantingWindow": "Abr – May",
      "irrigationMm": 908.0
    },
    {
      "season": "autumn",
      "cropId": "pea",
      "score": 65,
      "reasons": [
        "Todo su ciclo (Nov–Ene) cae en su rango óptimo de temperatura (ECOCROP)",
        "Necesita 44 % menos agua que maíz",
        "Leguminosa: fija nitrógeno del aire (estimado)"
      ],
      "waterSavingPct": 44.0,
      "nitrogenDelta": 8.0,
      "risks": [
        "Requiere riego: la lluvia cubre ~0 % de lo que necesita"
      ],
      "plantingWindow": "Nov",
      "irrigationMm": 226.0
    }
  ],
  "impact": [
    {
      "label": "Agua total del cultivo",
      "unit": "mm",
      "current": 1311.0,
      "recommended": 1453.0,
      "betterWhen": "lower"
    },
    {
      "label": "Riego necesario",
      "unit": "mm",
      "current": 1310.0,
      "recommended": 1451.0,
      "betterWhen": "lower"
    },
    {
      "label": "Balance de nitrógeno (estimado)",
      "unit": "kg/ha",
      "current": -94.0,
      "recommended": -36.0,
      "betterWhen": "higher"
    }
  ],
  "soilHealth": {
    "current": 40,
    "recommended": 70
  },
  "climate": [
    {
      "month": "Ene",
      "rain": 13.0,
      "temp": 13.1
    },
    {
      "month": "Feb",
      "rain": 7.0,
      "temp": 15.2
    },
    {
      "month": "Mar",
      "rain": 10.0,
      "temp": 18.3
    },
    {
      "month": "Abr",
      "rain": 3.0,
      "temp": 23.1
    },
    {
      "month": "May",
      "rain": 1.0,
      "temp": 26.2
    },
    {
      "month": "Jun",
      "rain": 0.0,
      "temp": 31.8
    },
    {
      "month": "Jul",
      "rain": 3.0,
      "temp": 35.4
    },
    {
      "month": "Ago",
      "rain": 9.0,
      "temp": 35.3
    },
    {
      "month": "Sep",
      "rain": 12.0,
      "temp": 31.3
    },
    {
      "month": "Oct",
      "rain": 3.0,
      "temp": 25.5
    },
    {
      "month": "Nov",
      "rain": 8.0,
      "temp": 18.9
    },
    {
      "month": "Dic",
      "rain": 12.0,
      "temp": 14.0
    }
  ],
  "uncertainty": {
    "level": "medium",
    "reason": "La lluvia anual varía 27 % entre años (NASA POWER 2016-2025)"
  },
  "soilDetected": null,
  "irrigated": null,
  "strategies": [
    {
      "id": "current",
      "title": "Seguir como hoy",
      "isCurrent": true,
      "isRecommended": false,
      "steps": [
        {
          "season": "winter",
          "cropId": "maize",
          "score": 29,
          "reasons": [
            "Es lo que siembras hoy",
            "Tolera las temperaturas de su ciclo (Feb–Jun)"
          ],
          "waterSavingPct": 0.0,
          "nitrogenDelta": -47.0,
          "risks": [
            "Fuera de su temporada habitual de siembra; confirma las fechas locales",
            "Requiere riego: la lluvia cubre ~0 % de lo que necesita",
            "Misma familia que el cultivo anterior (más riesgo de plagas)"
          ],
          "plantingWindow": "Feb",
          "irrigationMm": 902.0
        },
        {
          "season": "summer",
          "cropId": "fallow",
          "score": 0,
          "reasons": [
            "Ningún ciclo cabe entre la cosecha de maíz (jul) y la siembra que sigue",
            "Deja el rastrojo o siembra una cobertura corta para no dejar el suelo desnudo"
          ],
          "waterSavingPct": 100.0,
          "nitrogenDelta": 0.0,
          "risks": [],
          "plantingWindow": "—",
          "irrigationMm": 0.0
        },
        {
          "season": "autumn",
          "cropId": "maize",
          "score": 23,
          "reasons": [
            "Es lo que siembras hoy",
            "Es la mejor opción disponible para esta temporada"
          ],
          "waterSavingPct": 0.0,
          "nitrogenDelta": -47.0,
          "risks": [
            "Fuera de su temporada habitual de siembra; confirma las fechas locales",
            "Requiere riego: la lluvia cubre ~0 % de lo que necesita",
            "Misma familia que el cultivo anterior (más riesgo de plagas)"
          ],
          "plantingWindow": "Sep – Nov",
          "irrigationMm": 408.0
        }
      ],
      "waterMm": 1311.0,
      "irrigationMm": 1310.0,
      "nitrogenKgHa": -94.0,
      "soilHealth": 40,
      "bareSeasons": 1,
      "why": "Tu cultivo actual en las temporadas en que el clima lo permite; descanso en las demás.",
      "benefits": [
        "Ya conoces el cultivo, tienes el equipo y sabes dónde venderlo"
      ],
      "tradeoffs": [
        "Repite familia botánica: plagas y enfermedades se acumulan",
        "1 temporada(s) sin cultivo: deja rastrojo o una cobertura para evitar erosión",
        "Fuera de su temporada habitual de siembra; confirma las fechas locales",
        "Requiere riego: la lluvia cubre ~0 % de lo que necesita"
      ],
      "evidence": [
        "Maíz, siembra feb (ciclo Feb–Jun): necesita ~902 mm (FAO-56, ET₀ Penman-Monteith) y la lluvia efectiva aporta ~0 mm (NASA POWER)",
        "Maíz, siembra sep – nov (ciclo Oct–Feb): necesita ~409 mm (FAO-56, ET₀ Penman-Monteith) y la lluvia efectiva aporta ~1 mm (NASA POWER)"
      ]
    },
    {
      "id": "water",
      "title": "Ahorrar agua",
      "isCurrent": false,
      "isRecommended": true,
      "steps": [
        {
          "season": "winter",
          "cropId": "pea",
          "score": 66,
          "reasons": [
            "Todo su ciclo (Ene–Mar) cae en su rango óptimo de temperatura (ECOCROP)",
            "Necesita 65 % menos agua que maíz",
            "Leguminosa: fija nitrógeno del aire (estimado)"
          ],
          "waterSavingPct": 65.0,
          "nitrogenDelta": 8.0,
          "risks": [
            "Requiere riego: la lluvia cubre ~0 % de lo que necesita"
          ],
          "plantingWindow": "Dic – Feb",
          "irrigationMm": 316.0
        },
        {
          "season": "spring",
          "cropId": "sorghum",
          "score": 57,
          "reasons": [
            "Tolera las temperaturas de su ciclo (May–Ago)",
            "Es de los 5 cultivos más sembrados en México (FAOSTAT): hay mercado e insumos",
            "Necesita 20 % menos agua que maíz"
          ],
          "waterSavingPct": 20.0,
          "nitrogenDelta": -52.0,
          "risks": [
            "Calor: en jul la temperatura media (~35 °C) pasa su óptimo (35 °C, ECOCROP); el rendimiento puede bajar: siembra temprano o elige una variedad tolerante",
            "Requiere riego: la lluvia cubre ~0 % de lo que necesita"
          ],
          "plantingWindow": "Abr – May",
          "irrigationMm": 908.0
        },
        {
          "season": "autumn",
          "cropId": "pea",
          "score": 65,
          "reasons": [
            "Todo su ciclo (Nov–Ene) cae en su rango óptimo de temperatura (ECOCROP)",
            "Necesita 44 % menos agua que maíz",
            "Leguminosa: fija nitrógeno del aire (estimado)"
          ],
          "waterSavingPct": 44.0,
          "nitrogenDelta": 8.0,
          "risks": [
            "Requiere riego: la lluvia cubre ~0 % de lo que necesita"
          ],
          "plantingWindow": "Nov",
          "irrigationMm": 226.0
        }
      ],
      "waterMm": 1453.0,
      "irrigationMm": 1451.0,
      "nitrogenKgHa": -36.0,
      "soilHealth": 70,
      "bareSeasons": 0,
      "why": "En cada temporada elige lo que menos agua necesita entre lo que el clima permite.",
      "benefits": [
        "Menos riego por ciclo: ~484 mm contra ~655 mm de seguir como hoy",
        "Balance de nitrógeno 58 kg/ha mejor que seguir como hoy (estimado)",
        "Salud del suelo de 40 a 70 / 100 (estimado)",
        "Cada ciclo cambia de familia botánica: corta ciclos de plagas"
      ],
      "tradeoffs": [
        "Usa 142 mm más de agua en total: hay más ciclos de cultivo",
        "Requiere riego: la lluvia cubre ~0 % de lo que necesita",
        "Calor: en jul la temperatura media (~35 °C) pasa su óptimo (35 °C, ECOCROP); el rendimiento puede bajar: siembra temprano o elige una variedad tolerante"
      ],
      "evidence": [
        "Chícharo, siembra dic – feb (ciclo Ene–Mar): necesita ~317 mm (FAO-56, ET₀ Penman-Monteith) y la lluvia efectiva aporta ~1 mm (NASA POWER)",
        "Sorgo, siembra abr – may (ciclo May–Ago): necesita ~908 mm (FAO-56, ET₀ Penman-Monteith) y la lluvia efectiva aporta ~0 mm (NASA POWER)",
        "Chícharo, siembra nov (ciclo Nov–Ene): necesita ~227 mm (FAO-56, ET₀ Penman-Monteith) y la lluvia efectiva aporta ~1 mm (NASA POWER)"
      ]
    },
    {
      "id": "nitrogen",
      "title": "Regenerar el suelo",
      "isCurrent": false,
      "isRecommended": false,
      "steps": [
        {
          "season": "winter",
          "cropId": "pea",
          "score": 70,
          "reasons": [
            "Todo su ciclo (Ene–Mar) cae en su rango óptimo de temperatura (ECOCROP)",
            "Necesita 65 % menos agua que maíz",
            "Leguminosa: fija nitrógeno del aire (estimado)"
          ],
          "waterSavingPct": 65.0,
          "nitrogenDelta": 8.0,
          "risks": [
            "Requiere riego: la lluvia cubre ~0 % de lo que necesita"
          ],
          "plantingWindow": "Dic – Feb",
          "irrigationMm": 316.0
        },
        {
          "season": "spring",
          "cropId": "cotton",
          "score": 55,
          "reasons": [
            "Todo su ciclo (Abr–Oct) cae en su rango óptimo de temperatura (ECOCROP)",
            "Encaja en tu sistema de producción actual (granos y forrajes)",
            "Cambia de familia respecto a chícharo (Fabaceae → Malvaceae): corta el ciclo de plagas"
          ],
          "waterSavingPct": -22.0,
          "nitrogenDelta": -139.0,
          "risks": [
            "Requiere riego: la lluvia cubre ~0 % de lo que necesita"
          ],
          "plantingWindow": "Abr – May",
          "irrigationMm": 1390.0
        },
        {
          "season": "autumn",
          "cropId": "pea",
          "score": 70,
          "reasons": [
            "Todo su ciclo (Nov–Ene) cae en su rango óptimo de temperatura (ECOCROP)",
            "Necesita 44 % menos agua que maíz",
            "Leguminosa: fija nitrógeno del aire (estimado)"
          ],
          "waterSavingPct": 44.0,
          "nitrogenDelta": 8.0,
          "risks": [
            "Requiere riego: la lluvia cubre ~0 % de lo que necesita"
          ],
          "plantingWindow": "Nov",
          "irrigationMm": 226.0
        }
      ],
      "waterMm": 1935.0,
      "irrigationMm": 1932.0,
      "nitrogenKgHa": -123.0,
      "soilHealth": 70,
      "bareSeasons": 0,
      "why": "Da más peso a leguminosas y coberturas, que devuelven nitrógeno y protegen el suelo.",
      "benefits": [
        "Menos riego por ciclo: ~644 mm contra ~655 mm de seguir como hoy",
        "Salud del suelo de 40 a 70 / 100 (estimado)",
        "Cada ciclo cambia de familia botánica: corta ciclos de plagas"
      ],
      "tradeoffs": [
        "Usa 624 mm más de agua en total: hay más ciclos de cultivo",
        "Requiere riego: la lluvia cubre ~0 % de lo que necesita"
      ],
      "evidence": [
        "Chícharo, siembra dic – feb (ciclo Ene–Mar): necesita ~317 mm (FAO-56, ET₀ Penman-Monteith) y la lluvia efectiva aporta ~1 mm (NASA POWER)",
        "Algodón, siembra abr – may (ciclo Abr–Oct): necesita ~1390 mm (FAO-56, ET₀ Penman-Monteith) y la lluvia efectiva aporta ~0 mm (NASA POWER)",
        "Chícharo, siembra nov (ciclo Nov–Ene): necesita ~227 mm (FAO-56, ET₀ Penman-Monteith) y la lluvia efectiva aporta ~1 mm (NASA POWER)"
      ]
    },
    {
      "id": "yield",
      "title": "Más rendimiento",
      "isCurrent": false,
      "isRecommended": false,
      "steps": [
        {
          "season": "winter",
          "cropId": "pea",
          "score": 63,
          "reasons": [
            "Todo su ciclo (Ene–Mar) cae en su rango óptimo de temperatura (ECOCROP)",
            "Necesita 65 % menos agua que maíz",
            "Leguminosa: fija nitrógeno del aire (estimado)"
          ],
          "waterSavingPct": 65.0,
          "nitrogenDelta": 8.0,
          "risks": [
            "Requiere riego: la lluvia cubre ~0 % de lo que necesita"
          ],
          "plantingWindow": "Dic – Feb",
          "irrigationMm": 316.0
        },
        {
          "season": "spring",
          "cropId": "cotton",
          "score": 70,
          "reasons": [
            "Todo su ciclo (Abr–Oct) cae en su rango óptimo de temperatura (ECOCROP)",
            "Cultivo de alto valor productivo",
            "Encaja en tu sistema de producción actual (granos y forrajes)"
          ],
          "waterSavingPct": -22.0,
          "nitrogenDelta": -139.0,
          "risks": [
            "Requiere riego: la lluvia cubre ~0 % de lo que necesita"
          ],
          "plantingWindow": "Abr – May",
          "irrigationMm": 1390.0
        },
        {
          "season": "autumn",
          "cropId": "barley",
          "score": 64,
          "reasons": [
            "Tolera las temperaturas de su ciclo (Nov–Mar)",
            "Es de los 5 cultivos más sembrados en México (FAOSTAT): hay mercado e insumos",
            "Necesita 12 % menos agua que maíz"
          ],
          "waterSavingPct": 12.0,
          "nitrogenDelta": -52.0,
          "risks": [
            "Requiere riego: la lluvia cubre ~0 % de lo que necesita"
          ],
          "plantingWindow": "Nov",
          "irrigationMm": 361.0
        }
      ],
      "waterMm": 2069.0,
      "irrigationMm": 2067.0,
      "nitrogenKgHa": -183.0,
      "soilHealth": 60,
      "bareSeasons": 0,
      "why": "Da más peso a los cultivos de mayor valor productivo que el clima permite.",
      "benefits": [
        "Salud del suelo de 40 a 60 / 100 (estimado)",
        "Cada ciclo cambia de familia botánica: corta ciclos de plagas"
      ],
      "tradeoffs": [
        "Usa 758 mm más de agua en total: hay más ciclos de cultivo",
        "Requiere riego: la lluvia cubre ~0 % de lo que necesita"
      ],
      "evidence": [
        "Chícharo, siembra dic – feb (ciclo Ene–Mar): necesita ~317 mm (FAO-56, ET₀ Penman-Monteith) y la lluvia efectiva aporta ~1 mm (NASA POWER)",
        "Algodón, siembra abr – may (ciclo Abr–Oct): necesita ~1390 mm (FAO-56, ET₀ Penman-Monteith) y la lluvia efectiva aporta ~0 mm (NASA POWER)",
        "Cebada, siembra nov (ciclo Nov–Mar): necesita ~362 mm (FAO-56, ET₀ Penman-Monteith) y la lluvia efectiva aporta ~1 mm (NASA POWER)"
      ]
    }
  ],
  "localChecks": [
    "Confirma las fechas de siembra y las variedades con productores o el extensionista de tu zona.",
    "Revisa que haya semilla e inoculante de chícharo en tu zona antes de sembrarlo.",
    "Pregunta qué plagas y enfermedades son comunes en tu zona para estos cultivos."
  ],
  "climateShift": null
};

export const mockHistory: AnalysisSummary[] = [
  {
    "id": "demo-001",
    "createdAt": "2026-11-15T18:00:00Z",
    "location": {
      "lat": 32.54999,
      "lon": -115.25005
    },
    "areaHa": 8.37,
    "currentCrop": "maize",
    "priority": "water",
    "rotationCrops": [
      "pea",
      "sorghum",
      "pea"
    ]
  },
  {
    "id": "demo-000",
    "createdAt": "2026-11-15T16:30:00Z",
    "location": {
      "lat": 32.51999,
      "lon": -115.35003
    },
    "areaHa": 3.02,
    "currentCrop": "wheat",
    "priority": "nitrogen",
    "rotationCrops": [
      "pea",
      "sorghum",
      "pea"
    ]
  }
];
