import type { ReactNode } from 'react';
import check from '../assets/check.svg';
import estilos from './OpcaoResposta.module.css';

type Propriedades = {
  tipo: 'unica' | 'multipla'; name: string; value: string; checked: boolean;
  onChange: (marcado: boolean) => void; children: ReactNode; disabled?: boolean;
};

export function OpcaoResposta({ tipo, name, value, checked, onChange, children, disabled }: Propriedades) {
  return <label className={`${estilos.opcao} ${checked ? estilos.selecionada : ''} ${disabled ? estilos.desabilitada : ''}`}>
    <input type={tipo === 'multipla' ? 'checkbox' : 'radio'} name={name} value={value}
      checked={checked} disabled={disabled} onChange={e => onChange(e.currentTarget.checked)} />
    <span aria-hidden="true" className={`${estilos.marcador} ${tipo === 'unica' ? estilos.circular : ''}`}>
      {checked && <img src={check} alt="" width={16} height={16} />}
    </span>
    <span>{children}</span>
  </label>;
}
