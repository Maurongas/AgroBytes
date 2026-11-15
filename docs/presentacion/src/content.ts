// TODOS los textos de la presentación. Edita aquí; los componentes no tienen texto fijo.
// - title / subtitle / eyebrow: lo único que se ve en pantalla (poco texto a propósito).
// - script: guion por presentador. Solo aparece en la ventana de notas (tecla S).
// - seconds: duración objetivo (para el cronómetro de las notas). Total ≈ 4 min.
// - builds: cuántas veces la flecha revela algo antes de pasar a la siguiente diapositiva.
// - {{clave}}: se sustituye por un número de mockAnalysis (ver `facts` en data.ts).

export type Speaker = 'Mia' | 'Mauro' | 'Both';
export interface Line { who: Speaker; text: string }
export interface SlideContent {
  id: string;
  title: string;
  subtitle?: string;
  /** Etiqueta pequeña sobre el título (p. ej. «The challenge»). */
  eyebrow?: string;
  /** Frase del gancho (portada). */
  hook?: string;
  seconds: number;
  builds: number;
  script: Line[];
  /** Qué revela cada build, para las notas del orador. */
  buildNotes?: string[];
}

export const deck = {
  name: 'AgroBytes',
  tagline: 'From NASA data to your field.',
  event: 'NASA Space Apps Challenge 2026',
  challenge: 'Field Shift: Adapting Farms with NASA Data',
  presenters: ['Mia', 'Mauro'] as const,
};

/** Integrantes (portada y cierre). Revisa la ortografía de cada nombre. */
export const team = ['Diego Núñez', 'Mauro Arango', 'Ximena Reséndiz', 'Mia Herrera', 'Daniel Hernández', 'Fernando González'];

/** Logos de la universidad (archivos en docs/presentacion/public/). */
export const school = {
  line: 'Universidad Autónoma de Baja California · Facultad de Ingeniería, Arquitectura y Diseño',
  logos: [
    { src: 'uabc.png', alt: 'UABC' },
    { src: 'fiad.png', alt: 'FIAD' },
  ],
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
  simulated: 'offline preview · preset scenarios',
  liveWhatIf: 'live · recalculated by the API',
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
  soilHealth: 'Soil health',
  irrigation: 'irrigation',
  irrigation3: 'Irrigation · 3 seasons',
  frost: 'Frost',
  heat: 'Heat',
  planSaved: 'Plan saved',
  live: 'LIVE · NASA POWER API',
  apiDocs: 'API docs',
  sampleData: 'offline · sample data',
  team: 'Team',
  sampleField: 'Sample field',
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

export const nasaYears = {
  value: 40, suffix: '+ years', line: 'of NASA climate data', lock: 'for scientists only', gap: 'Gap',
  insight: 'Our idea: NASA data → rotation options for one field, in plain words.',
};

/** Diagrama «How we built it» (diapositiva 3). */
export const pipeline = {
  inputs: [
    { id: 'field', title: 'Your field', line: 'Drawn on the map + your priorities' },
    { id: 'nasa', title: 'NASA POWER', line: '10 years · rain, heat, sun, soil moisture' },
    { id: 'soil', title: 'ISRIC SoilGrids', line: 'Soil texture & pH for that point' },
    { id: 'crops', title: 'Crop library', line: '18 crops · FAO ECOCROP ranges' },
  ],
  engine: { title: 'Rules engine', line: 'FAO-56 water balance · climate fit · rotation rules' },
  output: { title: 'Rotation options', line: 'Current + 3 strategies, each with its reasons' },
  stack: ['React', 'Leaflet', 'FastAPI', 'PostgreSQL', 'Docker'],
  note: 'No black box: every number traces back to its source.',
} as const;

/** Pestañas del prototipo (diapositiva 4). */
export const panes = {
  draw: { tab: 'Draw', title: 'Draw your field' },
  nasa: { tab: 'NASA data', title: 'NASA data for your field', subtitle: '10 years of NASA POWER for this exact point' },
  compare: { tab: 'Options', title: 'Options, not one answer' },
  whatif: { tab: 'What if?', title: 'What if next year is drier?' },
  field: { tab: 'In the field', title: 'Built for the field' },
} as const;
export type PaneId = keyof typeof panes;

/** Cada paso de la diapositiva 4 → qué pestaña se ve y en qué sub-paso. */
export const prototypeSteps: { pane: PaneId; step: number }[] = [
  { pane: 'draw', step: 2 },    // dibuja la parcela + suelo detectado
  { pane: 'draw', step: 3 },    // panel: cultivo + prioridad
  { pane: 'nasa', step: 0 },    // escaneo → tarjetas NASA
  { pane: 'compare', step: 4 }, // 4 estrategias
  { pane: 'compare', step: 5 }, // voltea la recomendada
  { pane: 'whatif', step: 1 },  // sliders a −20 % / +1.5 °C
  { pane: 'field', step: 0 },   // calendario · alertas · offline · PDF
];
/** Sub-paso que se muestra si alguien hace clic en una pestaña a mano. */
export const paneFinalStep: Record<PaneId, number> = { draw: 3, nasa: 0, compare: 4, whatif: 1, field: 0 };

/** Columna «How we keep it honest» (diapositiva 5). {{clave}} = número del mock. */
export const validation = {
  title: 'How we keep it honest',
  items: [
    { id: 'nasa', text: 'Real NASA POWER data · 10 years for this exact point' },
    { id: 'fao', text: 'Water use with FAO-56, the FAO standard method' },
    { id: 'sources', text: 'Crop ranges from FAO ECOCROP · soil from ISRIC SoilGrids' },
    { id: 'uncertainty', text: 'Uncertainty: {{uncertainty}} — plus {{checks}} things to check locally' },
    { id: 'next', text: 'Next: validate with local farmers and agronomists' },
  ],
} as const;

// Guion en inglés SENCILLO (no es nuestra lengua materna): frases cortas, palabras fáciles, números y términos
// técnicos sin cambiar. Es una guía, no para recitar: el título de cada diapositiva es la pista. Ver SPEECH.md.
export const slides: SlideContent[] = [
  {
    id: 'cover', title: 'AgroBytes', subtitle: 'From NASA data to your field.', seconds: 20, builds: 1,
    hook: 'Every season is a bet.',
    buildNotes: ['Parcel draws itself → “Every season is a bet.”'],
    script: [{ who: 'Mia', text: 'Hi! We are AgroBytes, from UABC. [→] Every season, a farmer makes a bet. What to plant? When? Is there enough water? The climate is changing, and the old rules don’t work anymore.' }],
  },
  {
    id: 'challenge', eyebrow: '01 · The challenge', title: 'The climate changed. The tools didn’t.', seconds: 35, builds: 2,
    buildNotes: ['“40+ years of NASA climate data” counter', 'Lock breaks → “Gap” + our idea'],
    script: [{ who: 'Mauro', text: 'Our challenge is Field Shift: help farmers choose crop rotations that protect their soil and their water. First, we looked at the problems: more heat, rain you can’t predict, and tired soil. [→] Then we looked at the data. NASA has more than 40 years of climate data, for almost any place on Earth. [→] But this data is made for scientists, not for farmers. That is the gap. So our idea is simple: NASA data in, rotation options out — for one field, in plain words.' }],
  },
  {
    id: 'build', eyebrow: '02 · How we built it', title: 'Open data in. Clear options out.', seconds: 35, builds: 0,
    script: [{ who: 'Mia', text: 'This is how we built it. One: the farmer draws the field on a map. Two: we get 10 years of climate from NASA POWER, and the soil — texture and pH — from ISRIC SoilGrids. Three: we use a library of 18 crops with FAO ranges. Then our rules engine uses the FAO-56 water balance. It is not a black box: every number has a source. The result: your current rotation, plus 3 other options.' }],
  },
  {
    id: 'prototype', eyebrow: '03 · The solution', title: 'Live, on real NASA data', seconds: 85, builds: prototypeSteps.length - 1,
    buildNotes: ['Panel: what you grow + what matters most', 'NASA data: REAL request to the API (see the log)', 'Four strategies side by side', 'Flip the recommended card', 'What if? → −20 % rain · +1.5 °C, recalculated by the API', 'In the field: calendar · alerts · offline · PDF'],
    script: [
      { who: 'Mauro', text: 'This is not a video. This is the real app, connected to our API right now. First, we draw the field. The app measures it — {{area}} hectares — and finds the soil: {{soil}}. [→] Then we choose the crop we grow today, and what matters most. Here: save water. [→] Now the app calls our API. Look at the top: this is a real request to NASA POWER and SoilGrids. Every number has a simple meaning, like “dry soil”. [→] And here are the options: our current rotation, and 3 strategies. [→] Each card says why, the evidence, the benefits and the risks.' },
      { who: 'Mia', text: '[→] Now: what if next year is drier? We move the sliders: 20% less rain, 1.5 degrees hotter. The API calculates the plan again, live. Look at the irrigation: this field needs more water. [→] The app also shows when the field has no crop, gives frost and heat alerts, works offline, and makes a PDF for the agronomist.' },
    ],
  },
  {
    id: 'impact', eyebrow: '04 · Impact & validation', title: 'See the impact. Know how sure it is.', seconds: 35, builds: 1,
    buildNotes: ['“How we keep it honest” checklist'],
    script: [{ who: 'Mauro', text: 'So, what is the impact? For this field, the recommended rotation needs {{waterPct}}% {{waterWord}} irrigation per crop cycle. Its nitrogen balance is about {{nitroGain}} kilos per hectare {{nitroWord}} than today. And soil health goes from {{soilNow}} to {{soilNew}}. These are estimates, and we say it clearly. [→] How do we keep it honest? Real NASA data. The FAO-56 method. Published crop ranges. And we show the uncertainty, plus what to check locally. Our next step: test it with real farmers and agronomists.' }],
  },
  {
    id: 'close', title: 'AgroBytes', subtitle: 'Supports the farmer. Never replaces them.', seconds: 20, builds: 0,
    script: [
      { who: 'Mia', text: 'AgroBytes does not replace the farmer. It helps the farmer decide, with NASA science — for any field in North America.' },
      { who: 'Mauro', text: 'From NASA data… to your field.' },
      { who: 'Both', text: 'We are AgroBytes. Thank you!' },
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
