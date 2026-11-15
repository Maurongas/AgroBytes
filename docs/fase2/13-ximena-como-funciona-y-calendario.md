# 13 · Ximena: "Cómo funciona", suelo descubierto y README para el jurado

Nov 14, 2026 · Mauro

> **Fase 2.** Empieza cuando termines lo del doc 08. Necesitas el **PR 2 de menaxmn** (`lib/glosario.ts` y
> `components/Termino.tsx`). El calendario funciona desde ya con los datos de ejemplo.

## Por qué

El reto pide tres cosas que nadie tiene todavía, y las tres caen en lo tuyo (navegación, Calendario y docs):

1. **Explicar los términos** y cómo se diferencian los datos de NASA de una medición en campo.
2. **Mostrar cuándo la parcela queda descubierta** ("times when fields are typically bare").
3. **Dejar claro qué hace y qué no hace la herramienta**: los datos, el método y los límites. Esto es lo que el
   jurado revisa cuando pregunta "¿y esto de dónde sale?".

## Orden de toda la fase 2 (es el mismo en los 5 documentos)

| # | Quién | Qué | Rama | Espera a |
| --- | --- | --- | --- | --- |
| 1 | Mauro | Contrato v2.2: tipos + datos de ejemplo | `feature/contrato-v22` | nada |
| 2 | menaxmn | Glosario y componente `Termino` | `feature/front-glosario` | nada |
| 3 | Mauro | Motor de estrategias + escenario climático | `feature/back-estrategias` | 1 |
| 4 | Fernando | Estrategias en Resultados | `feature/front-estrategias` | 1 y 2 |
| 5 | **tú** | **Vista "Cómo funciona" + suelo descubierto** | `feature/front-como-funciona` | 2 |
| 6 | Daniel | Calor, "Antes de decidir" y pre-calentar | `feature/back-calor-confirmar` | 3 |
| 7 | Mía | "¿Y si cambia el clima?" | `feature/front-que-pasa-si` | 1 |
| 8 | Mauro + menaxmn | Publicar | `chore/deploy` | todo |

## Cómo debe verse

- Solo tokens de `src/index.css`, tarjetas `rounded-card border border-line bg-surface-raised p-5 shadow-card`,
  títulos `font-display`, íconos `lucide-react`. Nada de colores `#…` nuevos.
- "Cómo funciona" se lee como una **guía corta**, no como un manual: secciones con títulos claros, frases
  cortas, una tabla y el glosario al final. En el celular todo en una columna.

```bash
cd frontend
git switch main && git pull
git switch -c feature/front-como-funciona
```

---

## Paso 1 · Suelo descubierto en el Calendario

### a) `src/lib/calendario.ts`: agrega al final

```ts
import type { RotationStep, Season } from '../api/types';

// Meses de cada temporada en el hemisferio norte (la app trabaja en México, EE. UU. y Canadá). 0 = enero.
export const MESES_TEMPORADA: Record<Season, number[]> = {
  spring: [2, 3, 4], summer: [5, 6, 7], autumn: [8, 9, 10], winter: [11, 0, 1],
};

export type Cobertura = 'cultivo' | 'descubierto' | 'fuera';

/** Para cada mes: con cultivo, descubierto (descanso) o fuera del plan (la temporada actual). */
export function coberturaPorMes(pasos: RotationStep[]): Cobertura[] {
  const meses: Cobertura[] = Array(12).fill('fuera');
  for (const p of pasos) {
    for (const m of MESES_TEMPORADA[p.season]) meses[m] = p.cropId === 'fallow' ? 'descubierto' : 'cultivo';
  }
  return meses;
}
```

(El `import type` va arriba del archivo, junto a los demás.)

### b) `src/views/CalendarView.tsx`

Imports:

```tsx
import { MESES, mesesDeVentana, coberturaPorMes, type Cobertura } from '../lib/calendario';
import Termino from '../components/Termino';
```

Arriba del componente:

```tsx
const BARRA: Record<Cobertura, string> = {
  cultivo: 'bg-leaf-300',
  descubierto: 'bg-clay-300',
  fuera: 'bg-line-soft',
};
```

Dentro del componente, después de `colMes`:

```tsx
  const hoy = analysis.strategies?.find((s) => s.isCurrent);
  const filasSuelo = [
    { titulo: 'Con la rotación', meses: coberturaPorMes(analysis.rotation) },
    ...(hoy ? [{ titulo: 'Si sigues como hoy', meses: coberturaPorMes(hoy.steps) }] : []),
  ];
  const descubiertos = filasSuelo[filasSuelo.length - 1].meses
    .map((c, i) => (c === 'descubierto' ? MESES[i] : null)).filter(Boolean);
```

En la cuadrícula, **entre** las filas de cultivos y la fila de "Lluvia (mm)":

```tsx
            <div className="col-span-full mt-2 border-t border-line-soft pt-2 text-left text-xs font-semibold uppercase tracking-widest text-ink-500">
              <Termino id="barbecho">Suelo cubierto</Termino>
            </div>
            {filasSuelo.map((fila) => (
              <div key={fila.titulo} className="contents">
                <span className="pr-2 text-left text-sm text-ink-700">{fila.titulo}</span>
                {fila.meses.map((c, i) => (
                  <span key={MESES[i]} className={`flex h-7 items-center px-0.5 ${colMes(i)}`}>
                    <span className={`h-2 w-full rounded-full ${BARRA[c]}`}
                      aria-label={`${MESES[i]}: ${c === 'cultivo' ? 'con cultivo' : c === 'descubierto' ? 'suelo descubierto' : 'fuera del plan'}`} />
                  </span>
                ))}
              </div>
            ))}
```

Debajo del recuadro, antes de la nota final, una leyenda y el aviso:

```tsx
      <div className="mt-3 flex flex-wrap gap-4 text-xs text-ink-500">
        <span className="flex items-center gap-1.5"><span className="h-2 w-5 rounded-full bg-leaf-300" />Con cultivo</span>
        <span className="flex items-center gap-1.5"><span className="h-2 w-5 rounded-full bg-clay-300" />Suelo descubierto</span>
        <span className="flex items-center gap-1.5"><span className="h-2 w-5 rounded-full bg-line-soft" />Temporada actual (fuera del plan)</span>
      </div>
      {descubiertos.length > 0 && (
        <p className="mt-3 rounded-xl bg-clay-100 p-3 text-sm text-ink-900">
          Si sigues como hoy, tu parcela queda sin cultivo en <strong>{descubiertos.join(', ')}</strong>.
          El suelo desnudo se erosiona: deja el rastrojo o siembra una cobertura.
        </p>
      )}
```

Con los datos de ejemplo debe salir: con la rotación, todo verde salvo la primavera; si sigues como hoy, el
invierno (Dic, Ene, Feb) en barro y el aviso.

---

## Paso 2 · La vista "Cómo funciona"

### a) Registrar la vista (3 archivos compartidos: avisa en el grupo antes)

1. `src/store/useStore.ts` (de Mía): agrega `'method'` al tipo `ViewId`. **Solo esa palabra.**
2. `src/App.tsx`: `const MethodView = lazy(() => import('./views/MethodView'));` y `method: MethodView,` en `VIEWS`.
3. `src/components/nav/navItems.ts` (tuyo): importa `BookOpen` de `lucide-react` y agrega al final de `NAV_ITEMS`:
   `{ id: 'method', label: 'Cómo funciona', icon: BookOpen },`. Sin `needsAnalysis`: se puede leer sin analizar.
   En el celular aparece solo dentro de "Más".

### b) `src/views/MethodView.tsx` (nuevo)

```tsx
import { Check, X } from 'lucide-react';
import { GLOSARIO } from '../lib/glosario';

const FUENTES = [
  { nombre: 'NASA POWER', que: 'Temperatura media, máxima y mínima; lluvia; humedad del suelo en la zona de raíces; radiación solar.',
    detalle: 'Promedio de los últimos 10 años (mes a mes) y los últimos 90 días. Cada dato cubre una zona de ~50 × 60 km.' },
  { nombre: 'ISRIC SoilGrids', que: 'Textura (arcilla, arena) y pH del suelo, de 0 a 30 cm.',
    detalle: 'Modelo global de ~250 m. Orienta si no conoces tu suelo; no reemplaza un análisis de laboratorio.' },
  { nombre: 'FAO ECOCROP', que: 'Rango de temperatura, tolerancia a helada y pH de cada cultivo.',
    detalle: 'Ficha agronómica de los 18 cultivos del catálogo.' },
  { nombre: 'FAO-56', que: 'Cuánta agua necesita cada cultivo según el clima (evapotranspiración).',
    detalle: 'Método estándar de la FAO, calculado con las temperaturas de NASA POWER.' },
  { nombre: 'FAOSTAT', que: 'Qué cultivos se siembran en México, EE. UU. y Canadá.',
    detalle: 'Solo recomendamos cultivos que tienen mercado e insumos en tu país.' },
];

const PASOS = [
  'Dibujas tu parcela y nos dices qué siembras, qué te importa más y si tienes riego.',
  'Pedimos a NASA POWER el clima de los últimos 10 años y de los últimos 90 días para ese lugar.',
  'Para cada una de las próximas 3 temporadas calificamos los 18 cultivos: 40 % temperatura, 30 % agua, 15 % suelo y 15 % tu prioridad.',
  'Restamos puntos si un cultivo repite familia (plagas), si está fuera de su temporada o si cambia tu sistema de producción.',
  'Armamos una rotación por cada prioridad y la comparamos contra seguir como hoy.',
];

function Seccion({ titulo, children }: { titulo: string; children: React.ReactNode }) {
  return (
    <section className="rounded-card border border-line bg-surface-raised p-5 shadow-card">
      <h2 className="font-display text-xl font-semibold">{titulo}</h2>
      <div className="mt-3 text-sm leading-relaxed text-ink-700">{children}</div>
    </section>
  );
}

export default function MethodView() {
  return (
    <div className="h-full overflow-auto p-6">
      <div className="mx-auto max-w-3xl space-y-5">
        <header>
          <h1 className="font-display text-3xl font-semibold">Cómo funciona</h1>
          <p className="mt-1 text-sm text-ink-500">De dónde salen los datos, cómo elegimos cada cultivo y qué no puede hacer esta herramienta.</p>
        </header>

        <Seccion titulo="Qué hace y qué no">
          <ul className="space-y-2">
            {['Te ayuda a comparar rotaciones con datos de clima de tu zona.',
              'Explica por qué sugiere cada cultivo y qué riesgos tiene.'].map((t) => (
              <li key={t} className="flex gap-2"><Check size={16} className="mt-0.5 shrink-0 text-leaf-700" aria-hidden />{t}</li>
            ))}
            {['No es un pronóstico del clima ni garantiza cosechas.',
              'No reemplaza tu experiencia ni la de un agrónomo de tu zona: tú decides.'].map((t) => (
              <li key={t} className="flex gap-2"><X size={16} className="mt-0.5 shrink-0 text-clay-700" aria-hidden />{t}</li>
            ))}
          </ul>
        </Seccion>

        <Seccion titulo="Cómo elegimos cada cultivo">
          <ol className="list-decimal space-y-1.5 pl-5">{PASOS.map((p) => <li key={p}>{p}</li>)}</ol>
          <p className="mt-3">Son <strong>reglas agronómicas</strong> públicas y explicables, no una caja negra: cada número del resultado se puede rastrear hasta su dato.</p>
        </Seccion>

        <Seccion titulo="De dónde salen los datos">
          <div className="-mx-1 overflow-x-auto">
            <table className="w-full min-w-[520px] text-left">
              <thead className="text-xs uppercase tracking-widest text-ink-500">
                <tr><th className="px-1 py-2">Fuente</th><th className="px-1 py-2">Qué nos da</th><th className="px-1 py-2">Hay que saber</th></tr>
              </thead>
              <tbody>
                {FUENTES.map((f) => (
                  <tr key={f.nombre} className="border-t border-line-soft align-top">
                    <td className="px-1 py-2 font-medium text-ink-900">{f.nombre}</td>
                    <td className="px-1 py-2">{f.que}</td>
                    <td className="px-1 py-2 text-ink-500">{f.detalle}</td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        </Seccion>

        <Seccion titulo="Datos de NASA contra medir en tu parcela">
          <p>NASA POWER combina observaciones y modelos para dar el clima de <strong>toda una zona</strong> de unos 50 km, día por día y en cualquier parte del mundo. Es ideal para ver patrones de años, pero no ve lo que pasa dentro de tu parcela: una ladera, un bajo que se encharca o tu pozo.</p>
          <p className="mt-2">Una estación o un sensor en tu terreno mide <strong>exactamente ahí</strong>, pero casi nunca tiene 10 años de historia. Lo mejor es combinar los dos: usa estos resultados como punto de partida y ajústalos con lo que tú observas cada temporada.</p>
        </Seccion>

        <Seccion titulo="Límites que debes conocer">
          <ul className="list-disc space-y-1.5 pl-5">
            <li>El nitrógeno y la salud del suelo son <strong>estimaciones por reglas</strong>, no mediciones.</li>
            <li>El clima es el promedio de 10 años: un año puede ser muy distinto, sobre todo si la incertidumbre es alta.</li>
            <li>No consideramos precios, plagas locales ni disponibilidad de semilla: confírmalos en tu zona.</li>
            <li>Funciona en México, Estados Unidos y Canadá, con 18 cultivos.</li>
          </ul>
        </Seccion>

        <Seccion titulo="Glosario">
          <dl className="grid gap-4 sm:grid-cols-2">
            {Object.values(GLOSARIO).map((t) => (
              <div key={t.termino}>
                <dt className="font-medium text-ink-900">{t.termino}</dt>
                <dd className="mt-0.5 text-ink-700">{t.corto}</dd>
              </div>
            ))}
          </dl>
        </Seccion>
      </div>
    </div>
  );
}
```

> Si TypeScript pide el tipo de `children`, usa `import type { ReactNode } from 'react';`.

---

## Paso 3 · Docs y README para el jurado

1. **README**: además de lo del doc 08, agrega una sección **"Cómo cumple el reto"**, con esta tabla corta
   (ajústala a lo que de verdad quede mergeado):

   | El reto pide | AgroBytes |
   | --- | --- |
   | Datos de observación de la Tierra de NASA | NASA POWER: 10 años de clima + últimos 90 días |
   | Suelo local, cultivos y prioridades | SoilGrids, FAO ECOCROP/FAOSTAT, prioridad y riego |
   | Comparar ≥ 3 estrategias, incluida la actual | "Seguir como hoy" + 3 rotaciones, con por qué, beneficios, riesgos y evidencia |
   | Riesgos y vacíos de información | Incertidumbre, heladas, calor y "Antes de decidir, confirma" |
   | Periodos con el suelo descubierto | Calendario: suelo cubierto mes a mes |
   | Escenarios de clima | "¿Y si cambia el clima?": sliders de lluvia y temperatura |
   | Diseño para agricultores | Español sencillo, glosario, PWA que funciona sin internet |
   | Apoyo, no reemplazo | Aviso "Tú decides" en Resultados y en el PDF |

2. Capturas nuevas para `docs/img/`: tarjetas de estrategias (escritorio), calendario con suelo descubierto y
   "Cómo funciona" en el celular.
3. `docs/contexto/frontend-layout.md`: agrega `views/MethodView.tsx` y `components/Termino.tsx`.
4. Recuerda la regla: nada de "IA", "ML" ni "satélite" donde no aplica.

---

## Paso 4 · QA de lo nuevo (después de que se mergeen Fernando y Mía)

Misma rutina del doc 08 (390 px y 1280 px, claro y oscuro, Tab), ahora en:

- [ ] Tarjetas de estrategias: se deslizan en el celular sin scroll horizontal de la página; la elegida se nota.
- [ ] Cada ⓘ abre, cierra con Escape y no queda tapada por la barra inferior ni por el mapa.
- [ ] "Cómo funciona": la tabla se desliza sola en 390 px; el glosario se lee bien en oscuro.
- [ ] Calendario: las tres barras se distinguen también en modo oscuro (si `clay-300` no contrasta, avisa).
- [ ] "¿Y si cambia el clima?" (Mía): sliders usables con el pulgar y con flechas del teclado.

Los arreglos de clases van en un PR aparte, `fix: …`, como en el doc 08.

## Cómo mandar el PR

```bash
npm run build
git add src/lib/calendario.ts src/views/CalendarView.tsx src/views/MethodView.tsx \
        src/components/nav/navItems.ts src/App.tsx src/store/useStore.ts
git commit -m "feat: vista Cómo funciona y suelo descubierto en el calendario"
git push -u origin feature/front-como-funciona
```

El README y los docs van en otro PR (`docs: README con cumplimiento del reto`), cuando todo esté mergeado.
