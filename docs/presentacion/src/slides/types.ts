export interface SlideProps {
  /** Paso interno (0 = recién entrada; llega hasta `builds` de content.ts) */
  step: number;
  /** true en la miniatura de la ventana de notas: mostrar el estado final, sin esperas */
  preview?: boolean;
}
