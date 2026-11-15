import type { ComponentType } from 'react';
import { slides } from '../content';
import type { SlideProps } from './types';
import S01Cover from './S01Cover';
import S02Challenge from './S02Challenge';
import S03Build from './S03Build';
import S04Prototype from './S04Prototype';
import S05Impact from './S05Impact';
import S06Close from './S06Close';

/** id de content.ts → componente. El orden lo decide `slides` en content.ts. */
const BY_ID: Record<string, ComponentType<SlideProps>> = {
  cover: S01Cover, challenge: S02Challenge, build: S03Build, prototype: S04Prototype, impact: S05Impact, close: S06Close,
};

export const SLIDE_COMPONENTS: ComponentType<SlideProps>[] = slides.map((s) => {
  const C = BY_ID[s.id];
  if (!C) throw new Error(`No hay componente para la diapositiva "${s.id}"`);
  return C;
});
