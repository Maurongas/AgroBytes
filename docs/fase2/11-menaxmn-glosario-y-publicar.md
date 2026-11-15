# 11 · menaxmn: glosario y publicar el frontend

Nov 14, 2026 · Mauro

> **Fase 2.** Empieza cuando termines lo del doc 05 (PR A y PR B). Tu primera tarea **no depende de nadie**
> y Fernando y Ximena la van a usar: hazla primero.

## Por qué

El reto pide *"explicar términos científicos como evapotranspiración, anomalías de humedad del suelo o riesgo de
helada"* y que la herramienta sea entendible *"para agricultores con poca experiencia técnica"*. Además, el
jurado tiene que poder abrir la app en su celular, y eso exige publicarla con HTTPS.

## Orden de toda la fase 2 (es el mismo en los 5 documentos)

| # | Quién | Qué | Rama | Espera a |
| --- | --- | --- | --- | --- |
| 1 | Mauro | Contrato v2.2: tipos + datos de ejemplo | `feature/contrato-v22` | nada |
| 2 | **tú** | **Glosario y componente `Termino`** | `feature/front-glosario` | nada |
| 3 | Mauro | Motor de estrategias + escenario climático | `feature/back-estrategias` | 1 |
| 4 | Fernando | Estrategias en Resultados | `feature/front-estrategias` | 1 y 2 |
| 5 | Ximena | Vista "Cómo funciona" + suelo descubierto | `feature/front-como-funciona` | 2 |
| 6 | Daniel | Calor, "Antes de decidir" y pre-calentar | `feature/back-calor-confirmar` | 3 |
| 7 | Mía | "¿Y si cambia el clima?" | `feature/front-que-pasa-si` | 1 |
| 8 | Mauro + **tú** | Publicar backend y frontend | `chore/deploy` | todo |

## Cómo debe verse (vale para todo el equipo)

Lo nuevo tiene que parecer que siempre estuvo ahí:

- **Solo tokens de `src/index.css`** (`leaf`, `sky`, `clay`, `sun`, `ink`, `line`, `surface-*`). Nada de colores
  `#…` nuevos: así el modo oscuro funciona solo.
- Tarjetas: `rounded-card border border-line bg-surface-raised p-5 shadow-card`. Títulos: `font-display`.
  Chips y botones: `rounded-full`. Íconos de `lucide-react` a 14–18 px.
- Animaciones discretas, como las que ya hay (framer-motion, 0.2–0.3 s). Nada que rebote.
- Palabras sencillas. Todo lo estimado lleva "(estimado)". Nunca "IA", "ML" ni "satélite".

---

## PR 2 · Glosario y `Termino` (`feature/front-glosario`)

Un ícono pequeño de información (ⓘ) junto a una palabra técnica. Al tocarlo aparece una explicación de una o dos
frases. Es un solo componente reutilizable: Fernando lo pone en las tarjetas de NASA y Ximena arma el glosario
completo en "Cómo funciona".

```bash
cd frontend
git switch main && git pull
git switch -c feature/front-glosario
```

### a) `src/lib/glosario.ts` (nuevo)

```ts
// Glosario de términos para agricultores. Frases cortas y sin jerga.
// Lo usan <Termino id="…"> (ícono ⓘ) y la vista "Cómo funciona".
export const GLOSARIO = {
  'nasa-power': {
    termino: 'NASA POWER',
    corto: 'Servicio gratuito de la NASA con clima diario y mensual de todo el mundo (temperatura, lluvia, humedad del suelo, sol). Cada dato cubre una zona de unos 50 km, no un punto exacto.',
  },
  'humedad-suelo': {
    termino: 'Humedad del suelo (zona de raíces)',
    corto: 'Qué tan mojada está la tierra donde viven las raíces: 0 es totalmente seca y 1 saturada. Debajo de 0.3 las plantas empiezan a sufrir.',
  },
  anomalia: {
    termino: 'Anomalía',
    corto: 'La diferencia entre lo que pasó estos días y lo normal para las mismas fechas en los últimos 10 años. "−35 %" de lluvia significa que llovió un tercio menos de lo normal.',
  },
  evapotranspiracion: {
    termino: 'Evapotranspiración',
    corto: 'El agua que se va de la parcela: la que se evapora del suelo más la que las plantas "sudan". Con calor, sol y viento sube. Con ella calculamos cuánta agua necesita cada cultivo.',
  },
  radiacion: {
    termino: 'Radiación solar',
    corto: 'La energía del sol que llega al suelo. Más radiación ayuda a los cultivos de sol (maíz, sorgo), pero también seca más rápido la tierra.',
  },
  helada: {
    termino: 'Riesgo de helada',
    corto: 'Cuando las temperaturas mínimas se acercan a la que daña al cultivo. Cada cultivo aguanta distinto: el trigo resiste mucho más que el frijol.',
  },
  calor: {
    termino: 'Estrés por calor',
    corto: 'Cuando las máximas pasan el rango cómodo del cultivo: la planta cierra sus poros, crece menos y puede perder flores o granos.',
  },
  rotacion: {
    termino: 'Rotación de cultivos',
    corto: 'Cambiar de cultivo en cada temporada en lugar de sembrar siempre lo mismo. Corta el ciclo de plagas, cuida el suelo y reparte el uso del agua.',
  },
  leguminosa: {
    termino: 'Leguminosa',
    corto: 'Plantas como el frijol, la soya o el garbanzo, que junto con bacterias de sus raíces toman nitrógeno del aire y lo dejan en el suelo.',
  },
  cobertura: {
    termino: 'Cultivo de cobertura',
    corto: 'Un cultivo que se siembra sobre todo para proteger el suelo (avena, veza): evita que el viento y la lluvia se lleven la tierra y le agrega materia orgánica.',
  },
  barbecho: {
    termino: 'Descanso (barbecho)',
    corto: 'Una temporada sin cultivo. Si el suelo queda desnudo se erosiona: conviene dejar el rastrojo o una cobertura.',
  },
  temporal: {
    termino: 'Temporal',
    corto: 'Parcela sin riego, que depende solo de la lluvia.',
  },
  incertidumbre: {
    termino: 'Incertidumbre',
    corto: 'Qué tan seguros podemos estar del resultado. Es alta cuando la lluvia cambia mucho de un año a otro: en ese caso confirma con productores de tu zona.',
  },
  puntaje: {
    termino: 'Puntaje (0–100)',
    corto: 'Qué tan bien encaja un cultivo en esa temporada: 40 % temperatura, 30 % agua, 15 % suelo y 15 % tu prioridad. Baja si repite familia o cambia tu sistema de producción.',
  },
  estimado: {
    termino: 'Estimado por reglas',
    corto: 'Un número calculado con reglas agronómicas generales, no medido en tu parcela. Sirve para comparar opciones, no como valor exacto.',
  },
} as const;

export type TerminoId = keyof typeof GLOSARIO;
```

### b) `src/components/Termino.tsx` (nuevo)

```tsx
import { useEffect, useId, useRef, useState, type ReactNode } from 'react';
import { Info } from 'lucide-react';
import { GLOSARIO, type TerminoId } from '../lib/glosario';

interface Props {
  id: TerminoId;
  children?: ReactNode; // la palabra junto a la que va el ícono (opcional)
  claro?: boolean;      // true sobre fondos oscuros (las tarjetas de NASA)
}

/** Palabra + ícono ⓘ que abre una explicación corta. Se cierra con Escape o tocando fuera. */
export default function Termino({ id, children, claro = false }: Props) {
  const [abierto, setAbierto] = useState(false);
  const caja = useRef<HTMLSpanElement>(null);
  const panelId = useId();
  const t = GLOSARIO[id];

  useEffect(() => {
    if (!abierto) return;
    const alTocar = (e: PointerEvent) => {
      if (!caja.current?.contains(e.target as Node)) setAbierto(false);
    };
    const alTeclear = (e: KeyboardEvent) => {
      if (e.key === 'Escape') setAbierto(false);
    };
    document.addEventListener('pointerdown', alTocar);
    document.addEventListener('keydown', alTeclear);
    return () => {
      document.removeEventListener('pointerdown', alTocar);
      document.removeEventListener('keydown', alTeclear);
    };
  }, [abierto]);

  return (
    <span ref={caja} className="relative inline-flex items-center gap-1">
      {children}
      <button type="button" onClick={() => setAbierto((v) => !v)} aria-expanded={abierto} aria-controls={panelId}
        aria-label={`Qué significa: ${t.termino}`}
        className={`-m-1.5 inline-flex items-center justify-center rounded-full p-1.5 transition-colors focus-visible:outline-2 focus-visible:outline-leaf-600 ${
          claro ? 'text-paper/60 hover:text-paper' : 'text-ink-400 hover:text-leaf-700'}`}>
        <Info size={14} aria-hidden />
      </button>
      {abierto && (
        <span id={panelId} role="note"
          className="absolute left-0 top-full z-30 mt-2 block w-64 max-w-[80vw] rounded-2xl border border-line bg-surface-raised p-3 text-left text-xs font-normal normal-case leading-relaxed tracking-normal text-ink-700 shadow-lift">
          <strong className="mb-1 block font-display text-sm text-ink-900">{t.termino}</strong>
          {t.corto}
        </span>
      )}
    </span>
  );
}
```

El área para tocar es de ~26 px gracias a `p-1.5 -m-1.5`. Ocupa poco, pero se puede tocar con el pulgar.

### c) Pruébalo

Para probarlo, ponlo temporalmente en `AccountView` (`<Termino id="evapotranspiracion">Evapotranspiración</Termino>`),
revisa claro/oscuro y celular (390 px: el globo no debe salirse de la pantalla) y **quítalo antes del PR**.

```bash
npm run build
git add src/lib/glosario.ts src/components/Termino.tsx
git commit -m "feat: glosario de términos y componente Termino"
git push -u origin feature/front-glosario
```

Avisa a Fernando y a Ximena en cuanto se mergee.

---

## Extra · Que un error no deje la pantalla en blanco (`feature/front-error-boundary`)

Si una vista falla con datos reales (por ejemplo, un campo que llega distinto), hoy React deja la pantalla en
blanco. En la demo eso es lo peor que puede pasar. Crea `src/components/ErrorBoundary.tsx`:

```tsx
import { Component, type ReactNode } from 'react';

interface State { error: Error | null }

/** Si una vista se rompe, muestra un aviso con salida en lugar de una pantalla en blanco. */
export default class ErrorBoundary extends Component<{ children: ReactNode }, State> {
  state: State = { error: null };

  static getDerivedStateFromError(error: Error): State {
    return { error };
  }

  componentDidCatch(error: Error) {
    console.error('Vista con error:', error);
  }

  render() {
    if (!this.state.error) return this.props.children;
    return (
      <div className="flex h-full flex-col items-center justify-center gap-3 p-6 text-center">
        <h1 className="font-display text-2xl font-semibold">Algo salió mal en esta pantalla</h1>
        <p className="max-w-sm text-sm text-ink-500">Tus datos siguen guardados. Vuelve al mapa e inténtalo de nuevo.</p>
        <button onClick={() => { this.setState({ error: null }); location.reload(); }}
          className="rounded-full bg-leaf-600 px-5 py-2 text-sm font-medium text-paper hover:bg-leaf-700">
          Volver a cargar
        </button>
      </div>
    );
  }
}
```

En `src/App.tsx`, envuelve el `<Suspense>` con `<ErrorBoundary key={view}>…</ErrorBoundary>`. El `key` hace que
al cambiar de vista el error se limpie solo. Avisa a Mía, porque `App.tsx` es compartido.

---

## PR 8 · Publicar el frontend (con Mauro)

Cuando Mauro te pase la URL del backend (`https://…`):

1. Crea el sitio en Netlify, Vercel o Cloudflare Pages conectado al repo:
   - **Directorio base:** `frontend` · **Comando:** `npm run build` · **Carpeta publicada:** `dist`
   - **Variables:** `VITE_API_URL=https://<backend>` y `VITE_USE_MOCK=false`
2. Es una SPA: configura que toda ruta desconocida sirva `index.html`. En Netlify es `frontend/public/_redirects`
   con la línea `/*  /index.html  200`. En Vercel, un `frontend/vercel.json` con un *rewrite* a `/index.html`.
3. Pásale a Mauro el dominio final para que lo ponga en `CORS_ORIGINS`.
4. **En el celular**, con la URL pública:
   - [ ] Abre, instala ("Agregar a pantalla de inicio") y abre desde el ícono: ventana propia, sin barra.
   - [ ] Analiza Ensenada; en DevTools remoto (`chrome://inspect`) las peticiones llevan `X-Device-Id`.
   - [ ] Modo avión: la app abre y muestra el último análisis.
5. Corre **Lighthouse** (DevTools → Lighthouse → móvil) en la URL publicada. Meta: PWA instalable, Accesibilidad ≥ 90,
   Buenas prácticas ≥ 90. Arregla lo que sea de tus archivos y abre issues para lo de los demás. Adjunta la
   captura al PR.

```bash
git add frontend/public/_redirects   # o frontend/vercel.json
git commit -m "chore: publicar frontend (SPA + variables de producción)"
```

## Cómo saber que terminaste

- [ ] `Termino` funciona con mouse, dedo y teclado (Tab → Enter abre, Escape cierra), en claro y oscuro.
- [ ] Una vista que falla muestra "Algo salió mal…" en lugar de pantalla en blanco.
- [ ] La app publicada abre en un celular, se instala y funciona en modo avión.
