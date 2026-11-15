# 07 · Fernando: historial, borrar y resultados

Nov 14, 2026 · @Mia

## Qué te toca

Tu Historial y el modo sin conexión ya están. Faltan dos cosas que el contrato v2.1 agregó: **borrar un análisis** y **mostrar el suelo detectado y el riego** en el Diagnóstico.

- Rama: `feature/front-historial-borrar`, creada desde `main` actualizado.
- Archivos tuyos: `src/views/HistoryView.tsx`, `src/views/DiagnosisView.tsx`, `src/lib/offline.ts`.
- **Espera el PR A de menaxmn** (agrega `deleteAnalysis` a `src/api/client.ts`). Mientras tanto puedes empezar por el paso 2, que no lo necesita. No edites `client.ts` tú: si dos personas lo editan se generan conflictos.

## Paso 1 · Borrar un análisis del historial

El backend ya tiene `DELETE /api/v1/analyses/{id}` y el cliente tendrá `deleteAnalysis(id)` cuando se mergee el PR A. Falta el botón.

```bash
cd frontend
git switch main && git pull
git switch -c feature/front-historial-borrar
```

**a) `src/lib/offline.ts`**: agrega esta función justo después de `leerAnalisis`. Quita el análisis de las tres cosas que guarda el archivo: la lista del historial, la copia completa y la "última".

```ts
/** Quita un análisis de lo guardado en el dispositivo (historial, copia completa y "última"). */
export function quitarAnalisis(id: string): void {
  const filas = leerHistorial();
  if (filas) guardarHistorial(filas.filter((f) => f.id !== id));

  const todos = leer<Record<string, AnalysisResponse>>(K_ANALISIS);
  if (todos && id in todos) {
    delete todos[id];
    guardar(K_ANALISIS, todos);
  }

  if (leerUltima()?.analysis.id === id) {
    try {
      localStorage.removeItem(K_ULTIMA);
    } catch {
      /* bloqueado: se ignora */
    }
  }
}
```

**b) `src/views/HistoryView.tsx`**: cambios en cuatro lugares.

(1) Imports: agrega `useQueryClient`, `Trash2` y las dos funciones nuevas:

```tsx
import { useQuery, useQueryClient } from '@tanstack/react-query';
import { Trash2 } from 'lucide-react';
import { listAnalyses, getAnalysis, deleteAnalysis } from '../api/client';
import { guardarAnalisis, guardarHistorial, leerAnalisis, leerHistorial, quitarAnalisis } from '../lib/offline';
```

(2) Dentro de `HistoryView()`, debajo de `const [errorAbrir, ...]`, el estado y la función de borrar. El primer toque pide confirmación (se cancela solo a los 3 s) y el segundo borra:

```tsx
  const qc = useQueryClient();
  const [confirmando, setConfirmando] = useState<string | null>(null);
  const [borrando, setBorrando] = useState<string | null>(null);
  const [avisoBorrar, setAvisoBorrar] = useState<string | null>(null);

  async function borrar(fila: AnalysisSummary) {
    if (confirmando !== fila.id) {
      setConfirmando(fila.id);
      setTimeout(() => setConfirmando((actual) => (actual === fila.id ? null : actual)), 3000);
      return;
    }
    setConfirmando(null);
    setBorrando(fila.id);
    setAvisoBorrar(null);
    try {
      await deleteAnalysis(fila.id);
    } catch {
      setAvisoBorrar('No hay conexión con el servidor: se quitó solo de este dispositivo y puede volver a aparecer al reconectar.');
    } finally {
      quitarAnalisis(fila.id);
      qc.setQueryData(['historial'], (prev: { filas: AnalysisSummary[]; guardado: boolean } | undefined) =>
        prev ? { ...prev, filas: prev.filas.filter((f) => f.id !== fila.id) } : prev,
      );
      setBorrando(null);
    }
  }
```

(3) Debajo del bloque `{errorAbrir && (...)}` agrega el aviso:

```tsx
      {avisoBorrar && (
        <p className="mt-4 rounded-xl bg-sun-100 p-3 text-sm text-ink-900" role="status">{avisoBorrar}</p>
      )}
```

(4) El botón, en las dos vistas. En la tabla de escritorio, dentro del `<td className="px-4 py-3 text-right">` y después del botón *Abrir*:

```tsx
                      <button onClick={() => borrar(f)} disabled={borrando !== null}
                        aria-label={confirmando === f.id ? 'Confirmar borrar análisis' : 'Borrar análisis'}
                        className="ml-2 inline-flex items-center gap-1 rounded-full border border-danger/50 px-3 py-1 text-danger hover:bg-danger/10 disabled:opacity-50">
                        <Trash2 size={14} aria-hidden />
                        {borrando === f.id ? 'Borrando…' : confirmando === f.id ? '¿Borrar?' : 'Borrar'}
                      </button>
```

En las tarjetas del celular, debajo del botón *Abrir resultados*:

```tsx
                <button onClick={() => borrar(f)} disabled={borrando !== null}
                  aria-label={confirmando === f.id ? 'Confirmar borrar análisis' : 'Borrar análisis'}
                  className="mt-2 inline-flex w-full items-center justify-center gap-1 rounded-full border border-danger/50 py-2 text-sm text-danger hover:bg-danger/10 disabled:opacity-50">
                  <Trash2 size={14} aria-hidden />
                  {borrando === f.id ? 'Borrando…' : confirmando === f.id ? '¿Borrar?' : 'Borrar'}
                </button>
```

## Paso 2 · Mostrar riego, tipo de suelo y si hay riego

El backend ya devuelve `irrigationMm` en cada paso de la rotación, y `soilDetected` e `irrigated` en el análisis (los tipos ya están en `api/types.ts` y `api/mock.ts` ya trae datos de ejemplo). Nadie los muestra todavía. No necesitas el PR A para este paso.

**a) `src/lib/etiquetas.ts`**: agrega al final, y cambia la primera línea para importar el tipo:

```ts
import type { Priority, SoilTexture } from '../api/types';
```

```ts
export const TEXTURA_LABEL: Record<SoilTexture, string> = {
  sandy: 'Arenoso',
  loam: 'Franco',
  clay: 'Arcilloso',
};
```

**b) `src/views/DiagnosisView.tsx`**: cuatro cambios. Importa la etiqueta junto a la de prioridad:

```tsx
import { PRIORITY_LABEL, TEXTURA_LABEL } from '../lib/etiquetas';
```

1. **Chip de riego** en el encabezado, justo después del chip de `priority`:

```tsx
        {analysis.irrigated != null && (
          <span className="rounded-full bg-sky-50 px-3 py-1 text-xs text-sky-700">
            {analysis.irrigated ? 'Con riego' : 'Temporal (sin riego)'}
          </span>
        )}
```

2. **Riego estimado por temporada**: en el panel de cada paso, cambia `grid grid-cols-2 gap-3 text-sm` por `grid grid-cols-2 gap-3 text-sm sm:grid-cols-3` y agrega esta tarjeta después de la de "Nitrógeno (estimado)":

```tsx
                      <div className="rounded-xl bg-surface-raised/70 p-3">
                        <p className="text-xs text-ink-500">Riego estimado</p>
                        <p className="font-display text-xl font-semibold text-sky-700">
                          {step.irrigationMm > 0 ? `${step.irrigationMm} mm` : 'No necesita'}
                        </p>
                      </div>
```

3. **Tarjeta de suelo** en la columna "Impacto comparado", justo después de la tarjeta de "Salud del suelo":

```tsx
          {analysis.soilDetected && (
            <div className="rounded-card border border-line bg-surface-raised p-5 shadow-card">
              <p className="text-sm font-medium">Suelo de la parcela</p>
              <p className="mt-1 font-display text-xl font-semibold">{TEXTURA_LABEL[analysis.soilDetected.texture]}</p>
              <p className="mt-1 text-sm text-ink-700">
                Arcilla {Math.round(analysis.soilDetected.clayPct)} % · Arena {Math.round(analysis.soilDetected.sandPct)} %
                {analysis.soilDetected.ph != null && ` · pH ${analysis.soilDetected.ph.toFixed(1)}`}
              </p>
              <p className="mt-2 text-xs text-ink-500">
                {analysis.soilDetected.source}. Es una estimación global de unos 250 m, no una muestra de tu parcela.
              </p>
            </div>
          )}
```

4. **Sin dato de suelo**: si `soilDetected` es `null` (SoilGrids no respondió) no se muestra nada; está bien. No inventes un valor por defecto.

**c) Opcional, `src/lib/pdf.ts`**: abre el archivo, busca la tabla de la rotación (la llamada a `tabla([...], [...])`) y agrega una columna "Riego (mm)" con `String(r.irrigationMm)`. Respeta el mismo estilo del archivo; si no ves cómo, déjalo y menciónalo en el PR.

## Cómo probar y mandar el PR

```bash
npm run build
npm run dev   # o docker compose up, http://localhost:3000
```

Con datos de ejemplo (`VITE_USE_MOCK=true`, el valor por defecto):

1. Analiza una parcela. En *Diagnóstico* ves el chip "Temporal (sin riego)", la tarjeta "Riego estimado" en cada temporada (120, 60 y 410 mm en el ejemplo) y la tarjeta "Suelo de la parcela" con textura Franco y pH 6.9.
2. Abre *Historial*, toca **Borrar** en una fila: cambia a "¿Borrar?"; espera 3 s y vuelve a "Borrar". Tócalo dos veces seguidas: la fila desaparece sin recargar.
3. Recarga la página: la fila vuelve a aparecer, y es normal: en modo de ejemplo `listAnalyses` siempre devuelve las mismas filas; por eso la prueba real del borrado es el paso 5.
4. Revisa el celular (DevTools → vista móvil) y el modo oscuro: los botones rojos deben leerse bien.
5. **Con el backend real** (`docker compose up`, `VITE_USE_MOCK=false` y `VITE_API_URL=http://localhost:8000` en `frontend/.env`, reinicia `npm run dev`): crea dos análisis, bórralos desde el Historial y confirma que al recargar ya no aparecen. En DevTools → *Network* el `DELETE` debe responder `204`.
6. Sin conexión: con el historial abierto, marca *Offline* en DevTools → *Network*, borra una fila. Debe salir el aviso amarillo y la fila desaparecer del dispositivo.

```bash
git status   # solo deben aparecer HistoryView, DiagnosisView, offline.ts y etiquetas.ts (y pdf.ts si lo hiciste)
git add src/views/HistoryView.tsx src/views/DiagnosisView.tsx src/lib/offline.ts src/lib/etiquetas.ts
git commit -m "feat: borrar análisis del historial y mostrar suelo y riego en resultados"
git push -u origin feature/front-historial-borrar
```

Abre el PR hacia `main` y menciona a Mía para que lo revise. Si no ves la función `deleteAnalysis` en `client.ts` es que el PR A de menaxmn aún no está en `main`: haz `git pull` antes de abrir la rama.
