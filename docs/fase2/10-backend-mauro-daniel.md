# 10 · Backend (Mauro + Daniel): estrategias, escenarios y publicar

Nov 14, 2026 · Mauro

> **Fase 2.** Empieza cuando termines lo del doc 06. Esta fase cubre lo que el reto de NASA pide y todavía no
> tenemos. Los otros cuatro documentos (11–14) dependen del **PR 1** de este documento: hazlo primero.

## Por qué existe esta fase

El reto "Field Shift" pide, casi literalmente:

> *Compare at least three rotation strategies, including the existing rotation. For each strategy, explain why it
> was suggested, what evidence supports it, what benefits it may offer, where information gaps exist, and any
> risks that would need local review.*

Hoy devolvemos **una** rotación recomendada y la comparamos contra el cultivo actual. Con esta fase:

| El reto pide | Quién lo resuelve |
| --- | --- |
| Comparar 3 o más estrategias, incluida la actual | Mauro (backend, PR 1 y 2) → Fernando (pantalla) |
| Por qué, evidencia, beneficios y riesgos de cada una | Mauro (textos) → Fernando |
| Qué revisar con expertos locales | Daniel (backend) → Fernando |
| Estrés por calor y heladas | Daniel (backend) + Alertas, que ya existen |
| Periodos con el suelo descubierto | Ximena (Calendario) |
| Explicar términos, de dónde salen los datos y sus límites | menaxmn (glosario) + Ximena ("Cómo funciona") |
| Sliders de escenario (lluvia y temperatura) | Mauro (backend) → Mía ("¿Y si…?") |
| Que el jurado lo pueda abrir en un celular | Mauro (backend) + menaxmn (frontend): publicar |

## Orden de toda la fase 2 (es el mismo en los 5 documentos)

| # | Quién | Qué | Rama | Espera a |
| --- | --- | --- | --- | --- |
| 1 | Mauro | **Contrato v2.2**: tipos + datos de ejemplo | `feature/contrato-v22` | nada (**primero**, ~1 h) |
| 2 | menaxmn | Glosario y componente `Termino` | `feature/front-glosario` | nada |
| 3 | Mauro | Motor de estrategias + escenario climático | `feature/back-estrategias` | 1 |
| 4 | Fernando | Estrategias en Resultados | `feature/front-estrategias` | 1 y 2 |
| 5 | Ximena | Vista "Cómo funciona" + suelo descubierto | `feature/front-como-funciona` | 2 |
| 6 | Daniel | Calor, "Antes de decidir" y pre-calentar | `feature/back-calor-confirmar` | 3 |
| 7 | Mía | "¿Y si cambia el clima?" | `feature/front-que-pasa-si` | 1 (con datos reales: 3) |
| 8 | Mauro + menaxmn | Publicar backend y frontend | `chore/deploy` | todo lo anterior |

**Truco para no bloquear a nadie:** el PR 1 solo agrega los campos nuevos al contrato y los llena en
`mock.ts`. El frontend trabaja con datos de ejemplo mientras el backend hace la lógica de verdad en el PR 3.

---

## Mauro · Antes de la fase 2: correcciones al doc 06 (plan B de NASA)

El código del doc 06 funciona, pero corrígele esto en tu rama `feature/back-resiliencia`:

1. **Usa `return_exceptions=True` en el `gather`.** Así, si falla lo diario, la descarga mensual no se repite y
   no esperas el doble cuando NASA está lento:

   ```python
           if recent is None:
               long_res, daily_res = await asyncio.gather(
                   _long_term(client, lat_g, lon_g, today, db),
                   nasa_power.fetch_daily(lat_g, lon_g, start, end, client=client),
                   return_exceptions=True,
               )
               if isinstance(long_res, BaseException):
                   raise long_res  # sin largo plazo no hay plan B → la API responde 503
               summary, monthly = long_res
               try:
                   if isinstance(daily_res, BaseException):
                       raise daily_res
                   recent = build_recent(daily_res, monthly, summary, start, end)
                   _recent_cache.set((lat_g, lon_g, end), recent)
               except NasaUnavailableError:
                   log.warning("Sin datos diarios de NASA para (%s, %s): se usa lo normal como reciente", lat_g, lon_g)
                   recent = recent_from_normals(monthly, summary, start, end)
   ```

2. **No digas que son datos medidos cuando no lo son.** Agrega `estimated: bool = False` al final de
   `RecentClimate`, y `estimated=True` en el `return` de `recent_from_normals`. En `recommender.py`:
   - en `metrics_for`, si `r.estimated` es verdadero, usa `recent_src = f"Promedio NASA POWER {s.period} (sin datos recientes)"`;
   - en `uncertainty_for`, si `data.recent.estimated` es verdadero, sube un nivel (`i = min(2, i + 1)`) y agrega
     `"; no llegaron los datos de los últimos 90 días y se usó el promedio"` a `reason`.

3. **En la prueba, sustituye las dos descargas.** `fetch_monthly` con `serie_mensual(...)` de
   `test_nasa_power.py` y `fetch_daily` con una función que lance `NasaUnavailableError`. Si solo sustituyes la
   diaria, la prueba sale a internet. Revisa también que `recent.estimated is True`.

---

## Mauro · PR 1 · Contrato v2.2 (`feature/contrato-v22`)

Solo tipos y datos de ejemplo. El backend todavía devuelve listas vacías. Así Fernando, Ximena y Mía empiezan
hoy mismo.

```bash
git switch main && git pull
git switch -c feature/contrato-v22
```

### a) `backend/app/schemas/analysis.py`

Debajo de `CountryCode`:

```python
StrategyId = Literal["current", "water", "nitrogen", "yield"]
```

Debajo de la clase `Soil`:

```python
class ClimateShift(CamelModel):
    """Escenario hipotético «¿y si…?»: modifica el clima histórico antes de recomendar. Solo con guardar=false."""

    rain_pct: float = Field(default=0, ge=-60, le=60, description="% de cambio en la lluvia de cada mes")
    temp_c: float = Field(default=0, ge=-3, le=5, description="°C que se suman a la temperatura de cada mes")
```

En `AnalysisRequest`, después de `irrigated`:

```python
    climate_shift: ClimateShift | None = Field(
        default=None, description="Escenario climático hipotético (solo con guardar=false; si no, 422)")
```

Debajo de `class Uncertainty`:

```python
class Strategy(CamelModel):
    """Una forma de usar la parcela las próximas 3 temporadas. `current` = seguir como hoy."""

    id: StrategyId
    title: str = Field(examples=["Ahorrar agua"])
    is_current: bool
    is_recommended: bool = Field(description="La de la prioridad elegida: sus pasos son los mismos que `rotation`")
    steps: list[RotationStep] = Field(min_length=3, max_length=3)
    water_mm: float = Field(description="Agua total de los cultivos (FAO-56)")
    irrigation_mm: float = Field(description="Parte del agua que la lluvia no cubre")
    nitrogen_kg_ha: float = Field(description="Balance de nitrógeno ESTIMADO por reglas")
    soil_health: int = Field(ge=0, le=100, description="Índice ESTIMADO por reglas")
    bare_seasons: int = Field(ge=0, le=3, description="Temporadas con el suelo sin cultivo")
    why: str
    benefits: list[str]
    tradeoffs: list[str] = Field(description="Riesgos y costos a revisar")
    evidence: list[str] = Field(description="Datos que respaldan la estrategia, con su fuente")
```

En `AnalysisResponse`, al final:

```python
    strategies: list[Strategy] = Field(
        default_factory=list, description="Seguir como hoy + una rotación por prioridad. [] en análisis viejos")
    local_checks: list[str] = Field(
        default_factory=list, description="Qué confirmar con productores o un agrónomo de la zona")
    climate_shift: ClimateShift | None = None
```

### b) `backend/app/api/v1/analyses.py`

En `create_analysis`, justo después del comentario `# 1. Geometría…` y antes de `ring = …`:

```python
    if req.climate_shift is not None and guardar:
        raise HTTPException(status.HTTP_422_UNPROCESSABLE_CONTENT,
                            detail="Los escenarios hipotéticos solo se calculan sin guardar (guardar=false)")
```

Y en `body`, después de `"irrigated": req.irrigated,`:

```python
        "strategies": [s.model_dump(mode="json") for s in result.strategies],
        "local_checks": list(result.local_checks),
        "climate_shift": req.climate_shift.model_dump(mode="json") if req.climate_shift else None,
```

En `recommender.py`, agrega los dos campos a `RecommendationResult` (al final, con valor por defecto, para que
nada se rompa todavía). Cambia `from dataclasses import dataclass` por `from dataclasses import dataclass, field`:

```python
    strategies: list[Strategy] = field(default_factory=list)
    local_checks: list[str] = field(default_factory=list)
```

y agrega `Strategy` al `import` de `app.schemas.analysis`.

### c) `frontend/src/api/types.ts` (espejo exacto)

Después de `Uncertainty`:

```ts
export type StrategyId = 'current' | Priority;

// Escenario hipotético «¿y si…?» (solo con previewAnalysis / guardar=false)
export interface ClimateShift {
  rainPct: number; // −60 a 60: % de cambio en la lluvia de cada mes
  tempC: number;   // −3 a 5: °C que se suman a cada mes
}

// Una forma de usar la parcela las próximas 3 temporadas. 'current' = seguir como hoy.
export interface Strategy {
  id: StrategyId;
  title: string;            // «Ahorrar agua»; si dos coinciden: «Ahorrar agua · Regenerar el suelo»
  isCurrent: boolean;
  isRecommended: boolean;   // la de la prioridad elegida (= rotation)
  steps: RotationStep[];    // 3 pasos
  waterMm: number;
  irrigationMm: number;
  nitrogenKgHa: number;     // ESTIMADO por reglas
  soilHealth: number;       // 0-100, ESTIMADO por reglas
  bareSeasons: number;      // temporadas con el suelo sin cultivo
  why: string;
  benefits: string[];
  tradeoffs: string[];      // riesgos y costos a revisar
  evidence: string[];       // datos que la respaldan, con su fuente
}
```

En `AnalysisRequest`: `climateShift?: ClimateShift;`.
En `AnalysisResponse`, al final:

```ts
  strategies?: Strategy[];  // [] o ausente en análisis guardados antes de la v2.2
  localChecks?: string[];   // qué confirmar con productores o un agrónomo de la zona
  climateShift?: ClimateShift | null;
```

### d) `frontend/src/api/mock.ts`

Cambia el `import` a `import type { AnalysisResponse, AnalysisSummary, RotationStep } from './types';`. Saca la
rotación actual a una constante para reutilizarla (`rotation: ROTACION_AGUA,` dentro de `mockAnalysis`) y agrega
esto **antes** de `mockAnalysis`:

```ts
const ROTACION_AGUA: RotationStep[] = [ /* ← mueve aquí los 3 pasos que hoy están en mockAnalysis.rotation */ ];

const p = (season: RotationStep['season'], cropId: string, score: number, irrigationMm: number,
  nitrogenDelta: number, reasons: string[], risks: string[] = []): RotationStep => ({
  season, cropId, score, irrigationMm, nitrogenDelta, reasons, risks,
  waterSavingPct: 0, plantingWindow: cropId === 'fallow' ? '—' : 'Según temporada',
});
```

Y en `mockAnalysis`, después de `irrigated: false,`:

```ts
  strategies: [
    { id: 'current', title: 'Seguir como hoy', isCurrent: true, isRecommended: false,
      steps: [
        p('autumn', 'maize', 58, 260, -30, ['Es lo que siembras hoy'], ['Misma familia que el cultivo anterior (más riesgo de plagas)']),
        p('winter', 'fallow', 0, 0, 0, ['El maíz no tolera el invierno de este lugar', 'Hoy la parcela queda sin cultivo en esta temporada']),
        p('summer', 'maize', 55, 260, -30, ['Es lo que siembras hoy'], ['Requiere riego: la lluvia cubre ~10 % de lo que necesita']),
      ],
      waterMm: 640, irrigationMm: 520, nitrogenKgHa: 38, soilHealth: 52, bareSeasons: 1,
      why: 'Tu cultivo actual en las temporadas en que el clima lo permite; descanso en las demás.',
      benefits: ['Ya conoces el cultivo, tienes el equipo y sabes dónde venderlo'],
      tradeoffs: ['Repite familia botánica: plagas y enfermedades se acumulan', '1 temporada sin cultivo: deja rastrojo o una cobertura para evitar erosión'],
      evidence: ['Maíz, verano: necesita ~420 mm y la lluvia aporta ~6 mm (FAO-56 con clima de NASA POWER)'] },
    { id: 'water', title: 'Ahorrar agua', isCurrent: false, isRecommended: true, steps: ROTACION_AGUA,
      waterMm: 470, irrigationMm: 340, nitrogenKgHa: 71, soilHealth: 74, bareSeasons: 0,
      why: 'En cada temporada elige lo que menos agua necesita entre lo que el clima permite.',
      benefits: ['180 mm menos de riego que seguir como hoy', '+33 kg/ha de nitrógeno en el suelo (estimado)', 'Salud del suelo de 52 a 74 / 100 (estimado)'],
      tradeoffs: ['Sensible a heladas tempranas', 'Requiere control de maleza temprano'],
      evidence: ['Frijol, otoño: necesita ~300 mm y la lluvia aporta ~60 mm (FAO-56 con clima de NASA POWER)', 'Sorgo, verano: necesita ~420 mm y la lluvia aporta ~6 mm (FAO-56 con clima de NASA POWER)'] },
    { id: 'nitrogen', title: 'Regenerar el suelo', isCurrent: false, isRecommended: false,
      steps: [
        p('autumn', 'chickpea', 82, 150, 40, ['Leguminosa: fija nitrógeno en el suelo (estimado)']),
        p('winter', 'vetch', 80, 40, 60, ['Cultivo de cobertura: protege el suelo de la erosión']),
        p('summer', 'sorghum', 70, 200, -12, ['Resiste calor y sequía'], ['Requiere riego: la lluvia cubre ~15 % de lo que necesita']),
      ],
      waterMm: 520, irrigationMm: 390, nitrogenKgHa: 112, soilHealth: 86, bareSeasons: 0,
      why: 'Da más peso a leguminosas y coberturas, que devuelven nitrógeno y protegen el suelo.',
      benefits: ['130 mm menos de riego que seguir como hoy', '+74 kg/ha de nitrógeno en el suelo (estimado)', 'Salud del suelo de 52 a 86 / 100 (estimado)'],
      tradeoffs: ['El garbanzo y la veza tienen menos mercado que el maíz en la zona'],
      evidence: ['Garbanzo, otoño: necesita ~280 mm y la lluvia aporta ~60 mm (FAO-56 con clima de NASA POWER)'] },
    { id: 'yield', title: 'Más rendimiento', isCurrent: false, isRecommended: false,
      steps: [
        p('autumn', 'bean', 88, 120, 45, ['Es de los 5 cultivos más sembrados en México (FAOSTAT): hay mercado e insumos']),
        p('winter', 'wheat', 81, 90, -20, ['La temperatura de invierno (14 °C) está en su rango óptimo']),
        p('summer', 'maize', 76, 270, -30, ['Cultivo de alto valor productivo'], ['Requiere riego: la lluvia cubre ~10 % de lo que necesita']),
      ],
      waterMm: 610, irrigationMm: 480, nitrogenKgHa: 58, soilHealth: 66, bareSeasons: 0,
      why: 'Da más peso a los cultivos de mayor valor productivo que el clima permite.',
      benefits: ['40 mm menos de riego que seguir como hoy', '+20 kg/ha de nitrógeno en el suelo (estimado)'],
      tradeoffs: ['Usa casi la misma agua que hoy: depende del riego en verano'],
      evidence: ['Trigo, invierno: necesita ~250 mm y la lluvia aporta ~150 mm (FAO-56 con clima de NASA POWER)'] },
  ],
  localChecks: [
    'Confirma las fechas de siembra con productores o el extensionista de tu zona.',
    'Haz un análisis de suelo: la textura y el pH vienen de un modelo global de unos 250 m, no de tu parcela.',
    'Revisa que haya semilla e inoculante de frijol en tu zona antes de sembrarlo.',
    'La lluvia varía mucho entre años: ten un plan por si el temporal falla.',
  ],
  climateShift: null,
```

### e) `docs/ARQUITECTURA.md`

En §5 agrega `climateShift` al request y `strategies`, `localChecks` y `climateShift` a la respuesta (con una
línea de explicación cada uno), y sube la versión a **v2.2**. En §7 (motor) agrega un párrafo: "Estrategias:
`current` + una rotación por prioridad; las idénticas se fusionan".

### Probar y mandar

```bash
docker compose exec backend pytest -q      # todo debe seguir verde
cd frontend && npm run build               # o: docker compose exec frontend npm run build
git add backend/app/schemas/analysis.py backend/app/api/v1/analyses.py backend/app/services/recommender.py \
        frontend/src/api/types.ts frontend/src/api/mock.ts docs/ARQUITECTURA.md
git commit -m "feat: contrato v2.2 (estrategias, qué confirmar y escenario climático)"
git push -u origin feature/contrato-v22
```

Avisa en el grupo **en cuanto Mía lo mergee**: Fernando, Ximena y Mía empiezan con eso.

---

## Mauro · PR 3 · Motor de estrategias y escenario (`feature/back-estrategias`)

Todo esto va en `backend/app/services/recommender.py`. La idea es reutilizar lo que ya existe:
`recommend()` ya arma una rotación para **una** prioridad; la corremos para las tres y agregamos "seguir como hoy".

### a) Constantes y escenario

Arriba, junto a los demás imports: `import dataclasses`. Agrega `ClimateShift`, `Priority`, `Strategy` al import
de `app.schemas.analysis`. Después de `TOP_CROPS_IN_COUNTRY`:

```python
PRIORITIES: tuple[Priority, ...] = ("water", "nitrogen", "yield")
STRATEGY_TITLE = {"current": "Seguir como hoy", "water": "Ahorrar agua", "nitrogen": "Regenerar el suelo",
                  "yield": "Más rendimiento"}
STRATEGY_WHY = {
    "current": "Tu cultivo actual en las temporadas en que el clima lo permite; descanso en las demás.",
    "water": "En cada temporada elige lo que menos agua necesita entre lo que el clima permite.",
    "nitrogen": "Da más peso a leguminosas y coberturas, que devuelven nitrógeno y protegen el suelo.",
    "yield": "Da más peso a los cultivos de mayor valor productivo que el clima permite.",
}
```

Junto a `uncertainty_for`:

```python
def apply_shift(data: ClimateData, shift: ClimateShift | None) -> ClimateData:
    """Escenario «¿y si…?»: cambia la lluvia (%) y suma °C al clima histórico de cada mes. No toca el original.
    Lo reciente (90 días) no se toca: el escenario es sobre las temporadas típicas."""
    if shift is None or (shift.rain_pct == 0 and shift.temp_c == 0):
        return data
    f, d = 1 + shift.rain_pct / 100, shift.temp_c
    s = data.summary
    monthly = [p.model_copy(update={"temp_c": p.temp_c + d, "temp_max_c": p.temp_max_c + d,
                                    "temp_min_c": p.temp_min_c + d, "rain_mm": p.rain_mm * f}) for p in s.monthly]
    summary = s.model_copy(update={"monthly": monthly, "temp_mean_c": s.temp_mean_c + d,
                                   "rain_annual_mm": s.rain_annual_mm * f})
    return dataclasses.replace(data, summary=summary)
```

### b) Sacar el ciclo de `recommend()` a una función

Corta el `for sc in seasons:` que hoy está dentro de `recommend()` y pégalo como función, sin cambiar su lógica:

```python
def build_rotation(candidates: list[CropParams], seasons: list[SeasonClimate], req: AnalysisRequest,
                   current: CropParams, soil: SoilInput, uncertainty: Uncertainty, country_name: str | None,
                   popular: set[str]) -> tuple[list[RotationStep], list[CropParams | None]]:
    """Rotación de 3 temporadas para la prioridad de `req` (el ciclo que antes vivía dentro de recommend)."""
    irrigated = bool(req.irrigated)
    rotation: list[RotationStep] = []
    chosen: list[CropParams | None] = []
    previous = current
    for sc in seasons:
        # ↓↓↓ aquí va EXACTAMENTE el cuerpo del for que tenías (choose, fallow_step, RotationStep…)
        ...
    return rotation, chosen


def current_steps(current: CropParams, candidates: list[CropParams], seasons: list[SeasonClimate],
                  req: AnalysisRequest, soil: SoilInput, uncertainty: Uncertainty) -> list[RotationStep]:
    """Pasos de «Seguir como hoy»: el mismo cultivo en cada temporada que lo tolera (monocultivo)."""
    steps: list[RotationStep] = []
    for sc in seasons:
        label = SEASON_LABEL[sc.season]
        if not tolerates(current, sc):
            steps.append(RotationStep(
                season=sc.season, crop_id=FALLOW_ID, score=0, water_saving_pct=0, nitrogen_delta=0, risks=[],
                reasons=[f"El {current.name.lower()} no tolera el {label} de este lugar",
                         "Hoy la parcela queda sin cultivo en esta temporada"],
                planting_window="—", irrigation_mm=0))
            continue
        c = evaluate(current, sc, req, current, season_context([*candidates, current], sc), soil, current)
        steps.append(RotationStep(
            season=sc.season, crop_id=current.id, score=c.score,
            reasons=["Es lo que siembras hoy", *reasons_for(c, sc, current, current, req)[:2]],
            water_saving_pct=0, nitrogen_delta=current.nitrogen_delta_kg_ha,
            risks=risks_for(c, sc, uncertainty.level == "high", not c.in_season, bool(req.irrigated), soil),
            planting_window=planting_window(sc.months), irrigation_mm=round(c.irrigation_mm)))
    return steps
```

### c) Describir cada estrategia y fusionar las repetidas

```python
def describe(sid: str, steps: list[RotationStep], seq: list[CropParams | None], seasons: list[SeasonClimate],
             base: tuple[float, float, float, int], organic_matter: str | None, priority: Priority) -> Strategy:
    """Números y textos de una estrategia. `base` = (agua, riego, nitrógeno, suelo) de «Seguir como hoy»."""
    water, irrigation, nitrogen = impact(seq, seasons)
    soil_h = soil_health_index(seq, organic_matter)
    bare = sum(c is None for c in seq)
    b_water, b_irr, b_n, b_soil = base
    benefits: list[str] = []
    tradeoffs: list[str] = []
    if sid == "current":
        benefits.append("Ya conoces el cultivo, tienes el equipo y sabes dónde venderlo")
    else:
        if irrigation < b_irr:
            benefits.append(f"{b_irr - irrigation:.0f} mm menos de riego que seguir como hoy")
        if nitrogen > b_n:
            benefits.append(f"{nitrogen - b_n:+.0f} kg/ha de nitrógeno en el suelo (estimado)")
        if soil_h > b_soil:
            benefits.append(f"Salud del suelo de {b_soil} a {soil_h} / 100 (estimado)")
        if water > b_water:
            tradeoffs.append(f"Usa {water - b_water:.0f} mm más de agua en total: hay más temporadas con cultivo")
    families = [family_of(c) for c in seq if c is not None]
    if len(families) >= 2 and len(set(families)) == len(families):
        benefits.append("Cada temporada cambia de familia botánica: corta ciclos de plagas")
    elif len(set(families)) < len(families):
        tradeoffs.append("Repite familia botánica: plagas y enfermedades se acumulan")
    if bare:
        tradeoffs.append(f"{bare} temporada(s) sin cultivo: deja rastrojo o una cobertura para evitar erosión")
    for risk in (r for s in steps for r in s.risks):
        if risk not in tradeoffs and len(tradeoffs) < 4:
            tradeoffs.append(risk)
    evidence = [
        f"{c.name}, {SEASON_LABEL[sc.season]}: necesita ~{water_need(c, sc):.0f} mm y la lluvia aporta "
        f"~{cycle_rain(c, sc):.0f} mm (FAO-56 con clima de NASA POWER)"
        for c, sc in zip(seq, seasons) if c is not None
    ]
    return Strategy(
        id=sid, title=STRATEGY_TITLE[sid], is_current=sid == "current", is_recommended=sid == priority,
        steps=steps, water_mm=water, irrigation_mm=irrigation, nitrogen_kg_ha=nitrogen, soil_health=soil_h,
        bare_seasons=bare, why=STRATEGY_WHY[sid],
        benefits=benefits or ["Resultados parecidos a seguir como hoy"], tradeoffs=tradeoffs, evidence=evidence,
    )


def merge_duplicates(strategies: list[Strategy]) -> list[Strategy]:
    """Si dos prioridades dan los mismos cultivos, se muestran como una sola («Ahorrar agua · Regenerar el suelo»)."""
    out: list[Strategy] = []
    for s in strategies:
        twin = next((o for o in out if [x.crop_id for x in o.steps] == [x.crop_id for x in s.steps]), None)
        if twin is None:
            out.append(s)
        else:
            twin.title = f"{twin.title} · {s.title}"
            twin.is_recommended = twin.is_recommended or s.is_recommended
    return out
```

### d) El nuevo `recommend()`

Reemplaza desde `seasons = [...]` hasta el `return` por:

```python
    data = apply_shift(data, req.climate_shift)
    if req.climate_shift is not None:
        uncertainty = uncertainty.model_copy(update={"reason": uncertainty.reason + (
            f"; escenario hipotético: lluvia {req.climate_shift.rain_pct:+.0f} %, "
            f"temperatura {req.climate_shift.temp_c:+.1f} °C")})
    seasons = [season_climate(s, data) for s in next_seasons(today, data.summary.lat)]
    organic_matter = req.soil.organic_matter if req.soil else None

    # 1. «Seguir como hoy»: el cultivo actual donde puede crecer, descanso en las demás temporadas
    baseline: list[CropParams | None] = [current if tolerates(current, sc) else None for sc in seasons]
    base_numbers = (*impact(baseline, seasons), soil_health_index(baseline, organic_matter))
    # 2. Una rotación por prioridad (priority_factor cambia el puntaje). La elegida va primero.
    order = [req.priority, *[p for p in PRIORITIES if p != req.priority]]
    built = {p: build_rotation(candidates, seasons, req.model_copy(update={"priority": p}), current, soil,
                               uncertainty, country_name, popular) for p in order}
    rotation, chosen = built[req.priority]
    strategies = merge_duplicates([
        describe("current", current_steps(current, candidates, seasons, req, soil, uncertainty), baseline,
                 seasons, base_numbers, organic_matter, req.priority),
        *[describe(p, steps, seq, seasons, base_numbers, organic_matter, req.priority)
          for p, (steps, seq) in built.items()],
    ])
    water_cur, irr_cur, n_cur, _ = base_numbers
    water_rec, irr_rec, n_rec = impact(chosen, seasons)

    return RecommendationResult(
        metrics=metrics_for(data, current),
        rotation=rotation,
        impact=[ ... igual que hoy ... ],
        soil_health=SoilHealth(current=base_numbers[3], recommended=soil_health_index(chosen, organic_matter)),
        climate=[ ... igual que hoy ... ],
        uncertainty=uncertainty,
        strategies=strategies,
    )
```

`metrics_for` recibe el clima del escenario y por eso marca valores modificados. Es correcto: en un escenario
todo lo que se muestra es hipotético, y la razón de la incertidumbre lo dice.

### e) Pruebas (`backend/tests/test_recommender.py`)

```python
def test_estrategias_incluyen_la_actual_y_al_menos_tres(climate, catalog):
    r = recommender.recommend(climate, catalog, req(), NOV)
    assert r.strategies[0].is_current and r.strategies[0].id == "current"
    assert len(r.strategies) >= 3, "el reto pide comparar al menos 3, incluida la actual"
    recomendada = next(s for s in r.strategies if s.is_recommended)
    assert [p.crop_id for p in recomendada.steps] == [p.crop_id for p in r.rotation]
    assert all(len(s.steps) == 3 and s.why and s.evidence is not None for s in r.strategies)


def test_estrategias_repetidas_se_fusionan(climate, catalog):
    r = recommender.recommend(climate, catalog, req(), NOV)
    rotaciones = [tuple(p.crop_id for p in s.steps) for s in r.strategies]
    assert len(rotaciones) == len(set(rotaciones))


def test_escenario_mas_caliente_y_seco_cambia_el_clima(climate, catalog):
    # arriba del archivo: from app.schemas.analysis import AnalysisRequest, ClimateShift
    base = recommender.recommend(climate, catalog, req(), NOV)
    escenario = req().model_copy(update={"climate_shift": ClimateShift(rain_pct=-40, temp_c=3)})
    seco = recommender.recommend(climate, catalog, escenario, NOV)
    assert seco.climate[6].temp > base.climate[6].temp
    assert seco.climate[0].rain < base.climate[0].rain
    assert "escenario hipotético" in seco.uncertainty.reason
```

En `test_api.py`:

```python
def test_escenario_con_guardar_da_422(monkeypatch, catalog):
    falsear(monkeypatch, catalog)
    r = client.post("/api/v1/analyses", json={**BODY, "climateShift": {"rainPct": -20, "tempC": 1}})
    assert r.status_code == 422


def test_escenario_sin_guardar_responde_estrategias(monkeypatch, catalog):
    falsear(monkeypatch, catalog)
    r = client.post("/api/v1/analyses?guardar=false", json={**BODY, "climateShift": {"rainPct": -20, "tempC": 1}})
    assert r.status_code == 200
    assert len(r.json()["strategies"]) >= 3 and r.json()["climateShift"]["rainPct"] == -20
```

```bash
docker compose exec backend pytest -q
git add backend/app/services/recommender.py backend/tests/test_recommender.py backend/tests/test_api.py
git commit -m "feat: estrategias de rotación comparadas y escenario climático hipotético"
```

---

## Daniel · PR 6 · Calor, "Antes de decidir" y pre-calentar (`feature/back-calor-confirmar`)

**Espera a que el PR 3 de Mauro esté en `main`**: tocas el mismo archivo (`recommender.py`). Haz `git pull`
antes de crear la rama.

### 1 · Estrés por calor en cada paso

Hoy solo avisamos de heladas. NASA POWER ya nos da la máxima de cada mes (`temp_max_c`).

En `recommender.py`:

1. Constante, junto a `FROST_MARGIN_C`: `HEAT_MARGIN_C = 4  # máxima media 4 °C sobre el óptimo del cultivo → riesgo`.
2. En `SeasonClimate`, debajo de `temp_min_c`: `temp_max_c: float = -99.0  # promedio de la máxima diaria (calor)`.
3. En `season_climate(...)`, dentro del `return SeasonClimate(...)`:
   `temp_max_c=sum(p.temp_max_c for p in points) / 3,`
4. En `Candidate`, debajo de `frost_risk`: `heat_risk: bool = False`.
5. En `evaluate(...)`, dentro del `return Candidate(...)`, junto a `frost_risk=...`:
   `heat_risk=sc.temp_max_c > crop.temp_opt_max + HEAT_MARGIN_C,`
6. En `risks_for(...)`, justo después del bloque de helada:

```python
    if c.heat_risk:
        risks.append(f"Estrés por calor: máximas de ~{sc.temp_max_c:.0f} °C (su óptimo llega a "
                     f"{c.crop.temp_opt_max:.0f} °C); siembra temprano o riega en horas frescas")
```

Las estrategias de Mauro toman los riesgos de cada paso, así que el calor aparece solo en "A considerar".

### 2 · "Antes de decidir, confirma" (`local_checks`)

El reto insiste en que la herramienta **no reemplaza** al agricultor ni al agrónomo. Esta lista dice qué revisar.
Agrega en `recommender.py`, antes de `recommend()`:

```python
def local_checks_for(chosen: list[CropParams | None], current: CropParams, req: AnalysisRequest,
                     detected_soil: DetectedSoil | None, uncertainty: Uncertainty,
                     seasons: list[SeasonClimate]) -> list[str]:
    """Qué confirmar con productores o un agrónomo de la zona antes de cambiar la rotación (máx. 5)."""
    checks = ["Confirma las fechas de siembra con productores o el extensionista de tu zona."]
    if (req.soil is None or req.soil.ph is None) and detected_soil is not None:
        checks.append("Haz un análisis de suelo: la textura y el pH vienen de un modelo global de unos 250 m, "
                      "no de tu parcela.")
    crops = [c for c in chosen if c is not None]
    for c in crops:
        if c.family == "legume":
            checks.append(f"Revisa que haya semilla e inoculante de {c.name.lower()} en tu zona antes de sembrarlo.")
            break
    if any(changes_system(c, current) for c in crops):
        checks.append("Algún cultivo cambia tu sistema de producción: confirma que tienes equipo, mano de obra "
                      "y comprador.")
    if uncertainty.level == "high" and not req.irrigated:
        checks.append("La lluvia varía mucho entre años: ten un plan por si el temporal falla.")
    if any(c is None for c in chosen):
        empty = next(SEASON_LABEL[sc.season] for c, sc in zip(chosen, seasons) if c is None)
        checks.append(f"Planea cómo cubrir el suelo en {empty} (rastrojo o una cobertura).")
    checks.append("Pregunta qué plagas y enfermedades son comunes en tu zona para estos cultivos.")
    return checks[:5]
```

Y en el `return RecommendationResult(...)` de `recommend()`, agrega:

```python
        local_checks=local_checks_for(chosen, current, req, detected_soil, uncertainty, seasons),
```

### 3 · Pre-calentar desde el servidor (corrige el doc 06)

Tu script del doc 06 corre en **otro proceso**, así que solo llena la tabla `climate_cache`. Los 90 días
recientes y el suelo de SoilGrids viven en la memoria del servidor (uvicorn) y siguen fríos. Por eso la
verificación de "menos de 3 s" va a fallar. Arreglo: que el script pida un análisis **al servidor que ya está
corriendo**. Reemplaza `main()` en `backend/app/db/precalentar.py`:

```python
import httpx

API = "http://localhost:8000"  # dentro del contenedor del backend, el propio uvicorn
LADO = 0.0005  # ~55 m → parcela de ~1 ha (dentro del límite 0.1–500 ha)


def parcela(lat: float, lon: float) -> dict:
    a, b, c, d = lon - LADO, lat - LADO, lon + LADO, lat + LADO
    return {"type": "Polygon", "coordinates": [[[a, b], [c, b], [c, d], [a, d], [a, b]]]}


async def main() -> None:
    async with httpx.AsyncClient(base_url=API, timeout=90) as client:
        for nombre, (lat, lon) in LUGARES.items():
            inicio = time.perf_counter()
            r = await client.post("/api/v1/analyses", params={"guardar": "false"},
                                  headers={"X-Device-Id": "precalentar-demo"},
                                  json={"geometry": parcela(lat, lon), "currentCrop": "maize", "priority": "water"})
            estado = "OK   " if r.status_code == 200 else f"{r.status_code}  "
            print(f"{estado} {nombre:<20} {time.perf_counter() - inicio:5.1f} s")
```

(Borra los imports que ya no uses: `SessionLocal`, `climate_service`, `NasaUnavailableError`.) Córrelo dos veces:
la segunda debe tardar menos de 1 s por lugar. **Importante:** uvicorn corre con `--reload`; si alguien guarda un
`.py` del backend, el servidor se reinicia y se pierde lo calentado. El día de la demo, corre el script al final,
cuando ya nadie toque código.

### 4 · Pruebas

```python
def test_calor_aparece_como_riesgo():
    calido = make_climate()
    calido = calido.__class__(summary=calido.summary.model_copy(update={"monthly": [
        p.model_copy(update={"temp_max_c": 44}) for p in calido.summary.monthly]}), recent=calido.recent)
    maiz = crop("maize", "cereal", (18, 32), (10, 46), 600, ["spring", "summer"], -30)
    frijol = crop("bean", "legume", (16, 28), (8, 45), 350, ["spring", "summer"], 40)
    r = recommender.recommend(calido, [maiz, frijol], req(), NOV)
    assert any("calor" in risk for step in r.rotation for risk in step.risks)


def test_siempre_hay_algo_que_confirmar(climate, catalog):
    r = recommender.recommend(climate, catalog, req(), NOV)
    assert 1 <= len(r.local_checks) <= 5
    assert any("siembra" in c for c in r.local_checks)
```

```bash
docker compose exec backend pytest -q
git add backend/app/services/recommender.py backend/app/db/precalentar.py backend/tests/test_recommender.py
git commit -m "feat: riesgo por calor, lista de qué confirmar y pre-calentado vía la API"
```

---

## Mauro · PR 8 · Publicar el backend (`chore/deploy`)

Para que el jurado (y la PWA en el celular) funcionen, la app necesita una dirección con **HTTPS**. Plan
sugerido (revisa los precios y límites actuales en la web de cada servicio):

| Pieza | Dónde | Notas |
| --- | --- | --- |
| Base de datos | Render Postgres, Neon o Supabase | Tiene que permitir `CREATE EXTENSION postgis` |
| Backend | Render (Web Service con Docker) o Railway | Usa `backend/Dockerfile` |
| Frontend | Netlify, Vercel o Cloudflare Pages (lo hace menaxmn) | Es un sitio estático (`npm run build` → `dist/`) |

Pasos para el backend:

1. **Comando de arranque sin `--reload`** (en producción no queremos que se reinicie solo). En el servicio
   configura el *start command*:
   `sh -c "alembic upgrade head && python -m app.db.seed && uvicorn app.main:app --host 0.0.0.0 --port ${PORT:-8000}"`
2. **Variables de entorno:** `DATABASE_URL` (la que te da el proveedor, con el prefijo
   `postgresql+psycopg://`), `CORS_ORIGINS=https://<dominio-del-frontend>`, `REQUIRE_DEVICE_ID=true`,
   `RATE_LIMIT_ANALYSES_PER_MIN=30`.
3. Prueba `https://<tu-backend>/health` → `{"status":"ok","db":"ok"}` y `/docs`.
4. Pásale la URL a menaxmn para su `VITE_API_URL`.
5. **Plan gratis = se duerme.** Muchos planes gratuitos apagan el servidor si nadie lo usa y tarda ~1 min en
   despertar. Antes de presentar: abre `/health`, corre el pre-calentado de Daniel contra la URL pública
   (cambia `API`) y deja la app abierta.

Documenta las URLs y las variables en `docs/GUIA-INICIO.md` (sección "Versión publicada"). **Nunca subas
contraseñas al repo.**

## Cómo saber que el backend de la fase 2 está listo

- [ ] `POST /api/v1/analyses` en Ensenada devuelve `strategies` con 3 o 4 elementos, el primero `current`.
- [ ] La estrategia con `isRecommended: true` tiene los mismos cultivos que `rotation`.
- [ ] `localChecks` trae entre 1 y 5 frases.
- [ ] En Mexicali (32.66, −115.47) aparece "Estrés por calor" en algún riesgo de verano.
- [ ] `?guardar=false` con `climateShift: {rainPct: -40, tempC: 3}` responde 200 y cambia cultivos o riego;
      sin `guardar=false` responde 422.
- [ ] `pytest` en verde en CI.
- [ ] `https://<backend>/health` responde desde el celular.
