import type { ComponentType } from 'react';
import { slides } from '../content';
import type { SlideProps } from './types';
import S01Hook from './S01Hook';
import S02Problem from './S02Problem';
import S03Meet from './S03Meet';
import S04Draw from './S04Draw';
import S05Nasa from './S05Nasa';
import S06Compare from './S06Compare';
import S07Impact from './S07Impact';
import S08WhatIf from './S08WhatIf';
import S09Field from './S09Field';
import S10Close from './S10Close';

/** id de content.ts → componente. El orden lo decide `slides` en content.ts. */
const BY_ID: Record<string, ComponentType<SlideProps>> = {
  hook: S01Hook, problem: S02Problem, meet: S03Meet, draw: S04Draw, nasa: S05Nasa,
  compare: S06Compare, impact: S07Impact, whatif: S08WhatIf, field: S09Field, close: S10Close,
};

export const SLIDE_COMPONENTS: ComponentType<SlideProps>[] = slides.map((s) => {
  const C = BY_ID[s.id];
  if (!C) throw new Error(`No hay componente para la diapositiva "${s.id}"`);
  return C;
});
