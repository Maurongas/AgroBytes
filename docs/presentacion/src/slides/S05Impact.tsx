import { AnimatePresence, motion } from 'framer-motion';
import { ArrowRight, BadgeCheck, Droplets, FlaskConical, Gauge, ShieldCheck, Users, type LucideIcon } from 'lucide-react';
import GaugeSoilHealth from '@app/components/GaugeSoilHealth';
import { slide, ui, validation } from '../content';
import { analysis, fill, impactEn } from '../data';
import PitchImpactBar from '../components/PitchImpactBar';
import { EASE, Estimated, Title } from '../components/ui';
import type { SlideProps } from './types';

const T = slide('impact');
const ICON: Record<(typeof validation.items)[number]['id'], { icon: LucideIcon; tone: string }> = {
  nasa: { icon: BadgeCheck, tone: 'text-nasa-mark' },
  fao: { icon: Droplets, tone: 'text-sky-500' },
  sources: { icon: FlaskConical, tone: 'text-clay-500' },
  uncertainty: { icon: Gauge, tone: 'text-sun-700' },
  next: { icon: Users, tone: 'text-leaf-600' },
};

export default function S05Impact({ step, preview }: SlideProps) {
  const d = preview ? 0 : 1;
  const honest = step >= 1;
  return (
    <div className="absolute inset-0 flex flex-col bg-canvas px-20 py-16">
      <Title eyebrow={T.eyebrow}>{T.title}</Title>

      <div className="mt-10 grid flex-1 grid-cols-12 gap-8">
        {/* Impacto: gauges reales de la app + barras */}
        <motion.section className="col-span-7 flex flex-col gap-6 rounded-panel border border-line bg-surface-raised p-8 shadow-card"
          initial={{ opacity: 0, x: -30 }} animate={{ opacity: 1, x: 0 }} transition={{ duration: 0.6 * d, ease: EASE }}>
          <div className="flex items-center gap-6">
            <div className="w-[170px] text-center [&_svg]:mx-auto [&_svg]:max-w-[170px]">
              <GaugeSoilHealth value={analysis.soilHealth.current} />
              <p className="mt-1 text-base text-ink-500">{ui.today}</p>
            </div>
            <motion.span initial={{ opacity: 0, x: -10 }} animate={{ opacity: 1, x: 0 }} transition={{ delay: 0.9 * d }}>
              <ArrowRight size={36} className="text-leaf-600" />
            </motion.span>
            <motion.div className="w-[170px] text-center [&_svg]:mx-auto [&_svg]:max-w-[170px]" initial={{ opacity: 0 }} animate={{ opacity: 1 }} transition={{ delay: 0.7 * d }}>
              <GaugeSoilHealth value={analysis.soilHealth.recommended} />
              <p className="mt-1 text-base font-medium text-leaf-700">{ui.withRotation}</p>
            </motion.div>
            <p className="ml-auto flex flex-col items-end gap-2 text-2xl font-medium">{ui.soilHealth} <Estimated className="text-leaf-700" /></p>
          </div>
          <div className="flex flex-1 flex-col justify-around gap-4">
            {impactEn.map((it, i) => (
              <PitchImpactBar key={it.label} item={it} estimated={it.estimated} delay={(0.3 + i * 0.3) * d} />
            ))}
          </div>
        </motion.section>

        {/* Validación */}
        <section className="relative col-span-5 flex flex-col">
          <div className="absolute inset-0 rounded-panel border-2 border-dashed border-line-soft" />
          <AnimatePresence>
            {honest && (
              <motion.div key="honest" className="relative flex h-full flex-col rounded-panel bg-orbit p-8 text-paper shadow-lift"
                initial={{ opacity: 0, y: 30, scale: 0.97 }} animate={{ opacity: 1, y: 0, scale: 1 }} exit={{ opacity: 0, y: 20 }}
                transition={{ duration: 0.55 * d, ease: EASE }}>
                <p className="flex items-center gap-3 font-display text-3xl font-semibold"><ShieldCheck size={32} className="text-leaf-300" /> {validation.title}</p>
                <ul className="mt-6 flex flex-1 flex-col justify-between gap-3">
                  {validation.items.map((v, i) => {
                    const { icon: Icon, tone } = ICON[v.id];
                    return (
                      <motion.li key={v.id} className={`flex items-center gap-4 rounded-2xl px-4 py-3 text-xl leading-snug ${v.id === 'next' ? 'border border-dashed border-paper/30' : 'bg-paper/[0.07]'}`}
                        initial={{ opacity: 0, x: 24 }} animate={{ opacity: 1, x: 0 }} transition={{ delay: (0.3 + i * 0.2) * d, duration: 0.45, ease: EASE }}>
                        <span className="flex h-11 w-11 shrink-0 items-center justify-center rounded-xl bg-paper"><Icon size={24} className={tone} /></span>
                        {fill(v.text)}
                      </motion.li>
                    );
                  })}
                </ul>
                <motion.p className="mt-5 text-center text-lg text-paper/70" initial={{ opacity: 0 }} animate={{ opacity: 1 }} transition={{ delay: 1.5 * d }}>
                  {ui.supports}
                </motion.p>
              </motion.div>
            )}
          </AnimatePresence>
        </section>
      </div>
    </div>
  );
}
