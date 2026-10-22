import type { CSSProperties } from 'react';
import estilos from './BarraProgresso.module.css';

export function BarraProgresso({ atual, total }: { atual: number; total: number }) {
  const estilo = { '--percentual': `${total > 0 ? Math.min(100, atual / total * 100) : 0}%` } as CSSProperties;
  return <div className={estilos.trilho} role="progressbar" aria-label="Progresso da verificação"
    aria-valuemin={0} aria-valuemax={total} aria-valuenow={atual}>
    <span style={estilo} />
  </div>;
}
