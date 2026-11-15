import { ResponsiveContainer, ComposedChart, Bar, Line, XAxis, YAxis, CartesianGrid } from 'recharts';
import { MONTHS_EN } from '../i18n';

export interface ClimatePoint { month: string; rain: number; temp: number }

/**
 * Misma gráfica que «Clima de la parcela» en frontend/src/views/DiagnosisView.tsx
 * (barras de lluvia #1F8FD6 + línea de temperatura #F08A24). Meses en inglés por posición.
 */
export default function ClimateChart({ data, rainMax, tempRange }: { data: ClimatePoint[]; rainMax?: number; tempRange?: [number, number] }) {
  const rows = data.map((d, i) => ({ ...d, month: MONTHS_EN[i] ?? d.month }));
  return (
    <ResponsiveContainer width="100%" height="100%">
      <ComposedChart data={rows} margin={{ top: 8, right: 8, bottom: 0, left: 8 }}>
        <CartesianGrid stroke="var(--color-line-soft)" vertical={false} />
        <XAxis dataKey="month" tickLine={false} axisLine={false} tick={{ fill: 'var(--color-ink-500)', fontSize: 14 }} />
        <YAxis yAxisId="l" tickLine={false} axisLine={false} unit=" mm" domain={[0, rainMax ?? 'auto']}
          tick={{ fill: 'var(--color-ink-500)', fontSize: 13 }} width={64} />
        <YAxis yAxisId="r" orientation="right" tickLine={false} axisLine={false} unit="°" domain={tempRange ?? ['auto', 'auto']}
          tick={{ fill: 'var(--color-ink-500)', fontSize: 13 }} width={44} />
        <Bar yAxisId="l" dataKey="rain" fill="#1F8FD6" radius={[6, 6, 0, 0]} animationDuration={500} />
        <Line yAxisId="r" dataKey="temp" stroke="#F08A24" strokeWidth={3} dot={false} animationDuration={500} />
      </ComposedChart>
    </ResponsiveContainer>
  );
}
