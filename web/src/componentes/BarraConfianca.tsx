import type { CSSProperties } from 'react';
import estilos from './BarraConfianca.module.css';

export function BarraConfianca({ percentual, rotulo }: { percentual: number; rotulo: string }) {
  const estilo = { '--percentual': `${percentual}%` } as CSSProperties;
  return <div role="meter" aria-label={rotulo} aria-valuemin={0} aria-valuemax={100}
    aria-valuenow={percentual} aria-valuetext={`${percentual}% de confiança`} className={estilos.trilho}>
    <span className={estilos.preenchimento} style={estilo} />
  </div>;
}
