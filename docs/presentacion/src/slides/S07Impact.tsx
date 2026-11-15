import { motion } from 'framer-motion';
import { ArrowRight } from 'lucide-react';
import GaugeSoilHealth from '@app/components/GaugeSoilHealth';
import { slide, ui } from '../content';
import { analysis, impactEn } from '../data';
import PitchImpactBar from '../components/PitchImpactBar';
import { EASE, Estimated, Title } from '../components/ui';
import type { SlideProps } from './types';

const T = slide('impact');

export default function S07Impact(_: SlideProps) {
  return (
    <div className="absolute inset-0 flex flex-col bg-canvas px-24 py-20">
      <Title>{T.title}</Title>
      <div className="mt-14 grid flex-1 grid-cols-5 gap-10">
        <motion.section className="col-span-2 flex flex-col rounded-panel border border-line bg-surface-raised p-8 shadow-card"
          initial={{ opacity: 0, x: -30 }} animate={{ opacity: 1, x: 0 }} transition={{ duration: 0.6, ease: EASE }}>
          <p className="flex items-center gap-3 text-2xl font-medium">{ui.soilHealth} <Estimated className="text-leaf-700" /></p>
          {/* Gauges reales de la app (GaugeSoilHealth) */}
          <div className="flex flex-1 items-center justify-between gap-2">
            <div className="flex-1 text-center [&_svg]:mx-auto [&_svg]:max-w-[240px]">
              <GaugeSoilHealth value={analysis.soilHealth.current} />
              <p className="mt-2 text-lg text-ink-500">{ui.today}</p>
            </div>
            <motion.span initial={{ opacity: 0, x: -10 }} animate={{ opacity: 1, x: 0 }} transition={{ delay: 1 }}>
              <ArrowRight size={40} className="text-leaf-600" />
            </motion.span>
            <motion.div className="flex-1 text-center [&_svg]:mx-auto [&_svg]:max-w-[240px]" initial={{ opacity: 0 }} animate={{ opacity: 1 }} transition={{ delay: 0.8 }}>
              <GaugeSoilHealth value={analysis.soilHealth.recommended} />
              <p className="mt-2 text-lg font-medium text-leaf-700">{ui.withRotation}</p>
            </motion.div>
          </div>
        </motion.section>

        <section className="col-span-3 flex flex-col justify-center gap-9 rounded-panel border border-line bg-surface-raised p-10 shadow-card">
          {impactEn.map((it, i) => (
            <PitchImpactBar key={it.label} item={it} estimated={it.estimated} delay={0.3 + i * 0.35} />
          ))}
        </section>
      </div>
    </div>
  );
}
