import type { ButtonHTMLAttributes } from 'react';
import estilos from './Botao.module.css';

type Propriedades = ButtonHTMLAttributes<HTMLButtonElement> & {
  variante?: 'primario' | 'secundario';
  carregando?: boolean;
};

export function Botao({ variante = 'primario', carregando = false, disabled, children,
  className = '', type = 'button', ...outras }: Propriedades) {
  return <button {...outras} type={type} className={`${estilos.botao} ${estilos[variante]} ${className}`}
    disabled={disabled || carregando} aria-busy={carregando || undefined}>
    {children}{carregando && <span className="somenteLeitor">, enviando</span>}
  </button>;
}
