import { jsPDF } from 'jspdf';
import autoTable from 'jspdf-autotable';
import type { AnalysisResponse, Priority } from '../api/types';
import { cropName, seasonLabel } from './crops';
import { formatoFecha, priorityLabel } from './etiquetas';
import { tr } from './i18n';

const VERDE: [number, number, number] = [63, 125, 74];
const estado = (s: 'ok' | 'warn' | 'danger') =>
  ({ ok: tr('Bien', 'Good'), warn: tr('Atención', 'Caution'), danger: tr('Crítico', 'Critical') })[s];
const incertidumbre = (l: 'low' | 'medium' | 'high') =>
  ({ low: tr('baja', 'low'), medium: tr('media', 'medium'), high: tr('alta', 'high') })[l];

type DocConTabla = jsPDF & { lastAutoTable: { finalY: number } };
const finalY = (d: jsPDF) => (d as DocConTabla).lastAutoTable.finalY;

interface Extra {
  crop: string | null;
  priority: Priority | null;
}

// OJO: las fuentes estándar de PDF solo traen caracteres latinos (acentos y ñ sí). No uses flechas, emojis ni símbolos raros.
export function exportarPlanPdf(a: AnalysisResponse, { crop, priority }: Extra): void {
  const doc = new jsPDF({ unit: 'mm', format: 'a4' });
  const ancho = doc.internal.pageSize.getWidth();
  let y = 18;

  const titulo = (texto: string) => {
    if (y > 255) { doc.addPage(); y = 18; }
    doc.setFont('helvetica', 'bold');
    doc.setFontSize(13);
    doc.setTextColor(...VERDE);
    doc.text(texto, 14, y);
    y += 4;
  };
  const parrafo = (texto: string) => {
    doc.setFont('helvetica', 'normal');
    doc.setFontSize(10);
    doc.setTextColor(60);
    const lineas = doc.splitTextToSize(texto, ancho - 28);
    doc.text(lineas, 14, y + 4);
    y += lineas.length * 5 + 6;
  };
  const tabla = (head: string[], body: string[][]) => {
    autoTable(doc, {
      startY: y,
      head: [head],
      body,
      styles: { font: 'helvetica', fontSize: 9, cellPadding: 2 },
      headStyles: { fillColor: VERDE },
      margin: { left: 14, right: 14, bottom: 20 }, // deja espacio para el pie de página
    });
    y = finalY(doc) + 10;
  };

  // Encabezado
  doc.setFont('helvetica', 'bold');
  doc.setFontSize(20);
  doc.setTextColor(...VERDE);
  doc.text(tr('AgroBytes - Plan de rotación', 'AgroBytes - Crop rotation plan'), 14, y);
  y += 8;
  doc.setFont('helvetica', 'normal');
  doc.setFontSize(10);
  doc.setTextColor(60);
  const datos = [
    `${tr('Fecha del análisis', 'Analysis date')}: ${formatoFecha(a.createdAt)}`,
    `${tr('Ubicación', 'Location')}: ${a.location.lat.toFixed(4)}, ${a.location.lon.toFixed(4)}  ·  ${tr('Superficie', 'Area')}: ${a.areaHa.toFixed(1)} ha`,
    crop ? `${tr('Cultivo actual', 'Current crop')}: ${cropName(crop)}` : '',
    priority ? `${tr('Prioridad', 'Priority')}: ${priorityLabel(priority)}` : '',
  ].filter(Boolean);
  for (const linea of datos) { doc.text(linea, 14, y); y += 5; }
  y += 5;

  // Rotación
  titulo(tr('Rotación recomendada', 'Recommended rotation'));
  tabla(
    [tr('Temporada', 'Season'), tr('Cultivo', 'Crop'), tr('Siembra', 'Planting'), tr('Puntaje', 'Score'),
      tr('Ahorro de agua', 'Water saving'), tr('Riego (mm)', 'Irrigation (mm)'), tr('Nitrógeno (estimado)', 'Nitrogen (estimated)')],
    a.rotation.map((r) => [
      seasonLabel(r.season), cropName(r.cropId), r.plantingWindow, `${r.score} / 100`,
      `${r.waterSavingPct} %`, String(r.irrigationMm), `${r.nitrogenDelta > 0 ? '+' : ''}${r.nitrogenDelta} kg/ha`,
    ]),
  );
  tabla(
    [tr('Cultivo', 'Crop'), tr('Por qué se recomienda', 'Why it is recommended'), tr('Riesgos', 'Risks')],
    a.rotation.map((r) => [
      cropName(r.cropId),
      r.reasons.map((x) => `- ${x}`).join('\n'),
      r.risks.length ? r.risks.map((x) => `- ${x}`).join('\n') : tr('Sin riesgos registrados', 'No risks recorded'),
    ]),
  );

  // Estrategias (análisis v2.2 en adelante)
  if (a.strategies?.length) {
    titulo(tr('Estrategias comparadas', 'Strategies compared'));
    tabla(
      [tr('Estrategia', 'Strategy'), tr('Cultivos por temporada', 'Crops by season'), tr('Riego (mm)', 'Irrigation (mm)'),
        tr('Nitrógeno (kg/ha, est.)', 'Nitrogen (kg/ha, est.)'), tr('Suelo (/100, est.)', 'Soil (/100, est.)')],
      a.strategies.map((s) => [
        s.isRecommended ? `${s.title} (${tr('recomendada', 'recommended')})` : s.title,
        s.steps.map((p) => `${seasonLabel(p.season)}: ${cropName(p.cropId)}`).join('\n'),
        String(s.irrigationMm), String(s.nitrogenKgHa), String(s.soilHealth),
      ]),
    );
  }

  // Métricas NASA
  titulo(tr('Datos de la NASA para la parcela', 'NASA data for the field'));
  tabla(
    [tr('Métrica', 'Metric'), tr('Valor', 'Value'), tr('Estado', 'Status'), tr('Significado', 'Meaning')],
    a.metrics.map((m) => [m.label, `${m.value} ${m.unit}`, estado(m.status), `${m.meaning} (${m.source})`]),
  );

  // Impacto y suelo
  titulo(tr('Impacto estimado', 'Estimated impact'));
  tabla(
    [tr('Indicador', 'Indicator'), tr('Actual', 'Current'), tr('Con la rotación', 'With the rotation')],
    a.impact.map((i) => [i.label, `${i.current} ${i.unit}`, `${i.recommended} ${i.unit}`]),
  );
  parrafo(tr(
    `Salud del suelo (estimada por reglas): ${a.soilHealth.current} / 100 ahora, ${a.soilHealth.recommended} / 100 con la rotación.`,
    `Soil health (rule-based estimate): ${a.soilHealth.current} / 100 now, ${a.soilHealth.recommended} / 100 with the rotation.`,
  ));

  // Incertidumbre
  titulo(tr('Incertidumbre', 'Uncertainty'));
  parrafo(tr(`Nivel ${incertidumbre(a.uncertainty.level)}.`, `Level: ${incertidumbre(a.uncertainty.level)}.`) + ` ${a.uncertainty.reason}.`);

  if (a.localChecks?.length) {
    titulo(tr('Antes de decidir, confirma', 'Before deciding, confirm'));
    parrafo(a.localChecks.map((c) => `- ${c}`).join('\n'));
  }
  titulo(tr('Tú decides', 'You decide'));
  parrafo(tr(
    'Este plan es una guía para explorar opciones con datos de NASA POWER y reglas agronómicas. No reemplaza tu experiencia ni la de un agrónomo de tu zona.',
    'This plan is a guide to explore options with NASA POWER data and agronomic rules. It does not replace your experience or that of a local agronomist.',
  ));

  // Pie de cada página
  const paginas = doc.getNumberOfPages();
  for (let i = 1; i <= paginas; i++) {
    doc.setPage(i);
    doc.setFont('helvetica', 'normal');
    doc.setFontSize(8);
    doc.setTextColor(120);
    const nota = doc.splitTextToSize(tr(
      'Clima: NASA POWER. Recomendación por reglas agronómicas; el nitrógeno y la salud del suelo son estimaciones.',
      'Climate: NASA POWER. Rule-based agronomic recommendation; nitrogen and soil health are estimates.',
    ), ancho - 60);
    doc.text(nota, 14, 284);
    doc.text(tr(`Página ${i} de ${paginas}`, `Page ${i} of ${paginas}`), ancho - 14, 284, { align: 'right' });
  }

  doc.save(tr(`plan-rotacion-${a.id}.pdf`, `rotation-plan-${a.id}.pdf`));
}
