// TODOS los textos de la presentación. Edita aquí; los componentes no tienen texto fijo.
// - title / subtitle: lo único que se ve en pantalla (poco texto a propósito).
// - script: guion por presentador. Solo aparece en la ventana de notas (tecla S).
// - seconds: duración objetivo (para el cronómetro de las notas).
// - builds: cuántas veces la flecha revela algo antes de pasar a la siguiente diapositiva.
// - {{clave}}: se sustituye por un número de mockAnalysis (ver `facts` en data.ts).

export type Speaker = 'Mia' | 'Mauro' | 'Both';
export interface Line { who: Speaker; text: string }
export interface SlideContent {
  id: string;
  title: string;
  subtitle?: string;
  seconds: number;
  builds: number;
  script: Line[];
  /** Qué revela cada build, para las notas del orador. */
  buildNotes?: string[];
}

export const deck = {
  name: 'Field Shift',
  tagline: 'From NASA data to your field.',
  challenge: 'NASA Space Apps 2026 · Field Shift: Adapting Farms with NASA Data',
  presenters: ['Mia', 'Mauro'] as const,
};

export const ui = {
  estimated: 'estimated',
  recommended: 'Recommended',
  today: 'Today',
  withRotation: 'With rotation',
  why: 'Why',
  evidence: 'Evidence',
  benefits: 'Benefits',
  risks: 'Risks',
  flipHint: 'Hover or tap a card',
  score: 'score',
  soilDetected: 'Soil detected',
  yourField: 'Your field',
  currentCrop: 'What you grow today',
  priority: 'What matters most',
  priorities: { water: 'Save water', nitrogen: 'Rebuild soil', yield: 'Max yield' },
  analyze: 'Analyze with NASA data',
  scanMessages: ['Asking NASA POWER…', 'Reading soil moisture…', 'Computing water balance…', 'Comparing rotations…'],
  rain: 'Rain',
  temperature: 'Temperature',
  simulated: 'prototype preview · preset scenarios',
  rainUnit: 'mm',
  tempUnit: '°C',
  bareSoil: 'bare soil',
  uncertainty: 'Uncertainty',
  checkLocally: 'Check locally',
  supports: 'Supports the farmer. Never replaces them.',
  demo: 'Try the demo',
  // TODO: URL real de la demo y su QR (imagen en docs/presentacion/public/, p. ej. 'qr.svg').
  // Mientras estén vacíos, la diapositiva final no muestra el bloque del QR.
  demoUrl: '',
  qrImage: '',
  thanks: 'Thank you',
  sampleField: 'sample field · Ensenada, Baja California',
  soilHealth: 'Soil health',
  irrigation: 'irrigation',
  irrigation3: 'Irrigation · 3 seasons',
  frost: 'Frost',
  heat: 'Heat',
  planSaved: 'Plan saved',
  keysHint: '→ / Space next · ← back · S notes · F fullscreen · T theme',
};

/** Textos de la ventana de notas del orador (tecla S). */
export const notesUi = {
  title: 'Speaker notes',
  connected: 'synced',
  waiting: 'waiting for the deck… (open it and press S)',
  total: 'Total',
  slide: 'Slide',
  pace: 'vs plan',
  both: 'Both',
  now: 'Now',
  next: 'Next',
  nextBuild: 'Next click',
  end: 'End',
  prev: 'Back',
  advance: 'Next',
  reset: 'Reset timer (R)',
  help: '→ / Space next · ← back · R reset timer · the timer starts on the first advance',
};

export const features = [
  { id: 'calendar', title: 'Calendar', line: 'See when your field sits bare' },
  { id: 'alerts', title: 'Alerts', line: 'Frost · heat · drought · rain' },
  { id: 'offline', title: 'Offline', line: 'Works out in the field' },
  { id: 'pdf', title: 'PDF', line: 'Share with your agronomist' },
] as const;

export const problems = [
  { id: 'heat', label: 'Hotter' },
  { id: 'rain', label: 'Unpredictable rain' },
  { id: 'soil', label: 'Tired soil' },
] as const;

export const nasaYears = { value: 40, suffix: '+ years', line: 'of NASA climate data', lock: 'for scientists only', gap: 'Gap' };

export const steps = [
  { id: 'draw', label: 'Draw' },
  { id: 'choose', label: 'Choose' },
  { id: 'decide', label: 'Decide' },
] as const;

export const slides: SlideContent[] = [
  {
    id: 'hook', title: 'Every season is a bet.', seconds: 20, builds: 0,
    script: [{ who: 'Mia', text: 'Every season, a farmer makes a bet. What to plant, when to plant it, and whether there will be enough water. For generations, that bet was made on memory and instinct. But the climate our grandparents knew… is not the one we farm in today.' }],
  },
  {
    id: 'problem', title: 'The climate changed. The tools didn’t.', seconds: 25, builds: 2,
    buildNotes: ['“40+ years of NASA climate data” counter', 'Lock breaks → “Gap”'],
    script: [{ who: 'Mauro', text: 'Temperatures are shifting, rain is harder to predict, and soil is wearing out. [→] At the same time, NASA has decades of climate data for almost every point on Earth. [→] The problem? It’s built for scientists, not for farmers. We wanted to close that gap.' }],
  },
  {
    id: 'meet', title: 'Field Shift', subtitle: 'From NASA data to your field.', seconds: 20, builds: 0,
    script: [{ who: 'Mia', text: 'This is Field Shift. It turns NASA data into a crop-rotation plan for your own field — in three simple steps, in under a minute.' }],
  },
  {
    id: 'draw', title: 'Draw your field', seconds: 30, builds: 3,
    buildNotes: ['Cursor draws the parcel → {{area}} ha', 'Soil detected chip ({{soil}})', 'Panel: Maize + Save water'],
    script: [{ who: 'Mauro', text: 'Step one: [→] draw your field on the map. That’s it. Field Shift measures the area, [→] detects your soil automatically and knows your local climate. [→] Step two: tell us what you grow today. Step three: what matters most to you — saving water, rebuilding your soil, or maximizing yield.' }],
  },
  {
    id: 'nasa', title: 'NASA data for your field', subtitle: '10 years of NASA POWER for this exact point', seconds: 25, builds: 0,
    script: [{ who: 'Mia', text: 'Then we ask NASA. Ten years of climate for your exact location: soil moisture, rainfall, temperature and sunlight. And every number comes with a plain meaning — not “zero point two one”, but “a bit dry for corn”.' }],
  },
  {
    id: 'compare', title: 'Options, not one answer', seconds: 35, builds: 5,
    buildNotes: ['Keep as today', 'Save water (recommended)', 'Regenerate soil', 'Boost yield', 'Flip the recommended card: Why · Evidence · Benefits · Risks'],
    script: [{ who: 'Mauro', text: 'Here’s the heart of it. We don’t give you one answer — we give you options. [→] Your current rotation, [→] side by side with strategies to save water, [→] regenerate the soil, [→] or boost yield. [→] And each one tells you why it was suggested, the evidence behind it, the benefits… and the risks.' }],
  },
  {
    id: 'impact', title: 'See the impact before you plant', seconds: 20, builds: 0,
    script: [{ who: 'Mia', text: 'And you see the impact before planting a single seed. In this example field: {{waterPct}}% less water, {{nitroGain}} more kilos of nitrogen per hectare back in the soil, and a soil-health score that climbs from {{soilNow}} to {{soilNew}}.' }],
  },
  {
    id: 'whatif', title: 'What if next year is drier?', seconds: 20, builds: 1,
    buildNotes: ['Sliders glide to −20% rain · +1.5 °C (or move them by hand)'],
    script: [{ who: 'Mauro', text: 'But what if next year is drier? Just move a slider. [→] Twenty percent less rain, one and a half degrees hotter — and the plan adapts instantly. Farmers can test the future before it arrives.' }],
  },
  {
    id: 'field', title: 'Built for the field', seconds: 20, builds: 0,
    script: [{ who: 'Mia', text: 'Field Shift shows when your field sits bare, warns you about frost and heat, works offline out in the field, and exports a plan to share with your agronomist. And it’s honest: it tells you how sure it is, and what to double-check locally.' }],
  },
  {
    id: 'close', title: 'Field Shift', subtitle: 'Supports the farmer. Never replaces them.', seconds: 25, builds: 0,
    script: [
      { who: 'Mauro', text: 'Field Shift doesn’t replace the farmer’s judgment. It backs it up with NASA science — for any field in North America, today.' },
      { who: 'Mia', text: 'From NASA’s data… to your field.' },
      { who: 'Both', text: 'This is Field Shift. Thank you.' },
    ],
  },
];

/** Escenario que el build de «What if?» aplica solo (lo que dice el guion). */
export const whatIfTarget = { rainPct: -20, tempC: 1.5 };

/** Contenido de una diapositiva por su id (así reordenar `slides` no rompe nada). */
export const slide = (id: string): SlideContent => {
  const s = slides.find((x) => x.id === id);
  if (!s) throw new Error(`Slide "${id}" no está en content.ts`);
  return s;
};
