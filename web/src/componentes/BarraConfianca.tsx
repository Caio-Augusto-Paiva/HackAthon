import type { CSSProperties } from 'react';
import estilos from './BarraConfianca.module.css';

/** `atraso` (ms) escalona a entrada quando várias barras aparecem juntas. */
export function BarraConfianca({ percentual, rotulo, atraso = 0 }: { percentual: number; rotulo: string; atraso?: number }) {
  const estilo = { '--fracao': Math.max(0, Math.min(100, percentual)) / 100, '--atraso': `${atraso}ms` } as CSSProperties;
  return <div role="meter" aria-label={rotulo} aria-valuemin={0} aria-valuemax={100}
    aria-valuenow={percentual} aria-valuetext={`${percentual}% de confiança`} className={estilos.trilho}>
    <span className={estilos.preenchimento} style={estilo} />
  </div>;
}
