import { Component, type ReactNode } from 'react';

/** Si una diapositiva falla (p. ej. cambió un componente de la app), se muestra un aviso y el deck sigue navegable. */
export default class SlideBoundary extends Component<{ children: ReactNode; title: string }, { error: Error | null }> {
  state: { error: Error | null } = { error: null };
  static getDerivedStateFromError(error: Error) { return { error }; }
  componentDidCatch(error: Error) { console.error(`[pitch] "${this.props.title}" failed:`, error); }
  render() {
    if (!this.state.error) return this.props.children;
    return (
      <div className="absolute inset-0 flex flex-col items-center justify-center gap-4 bg-canvas p-20 text-center">
        <p className="font-display text-6xl font-semibold">{this.props.title}</p>
        <p className="font-mono text-base text-danger">{this.state.error.message}</p>
      </div>
    );
  }
}
