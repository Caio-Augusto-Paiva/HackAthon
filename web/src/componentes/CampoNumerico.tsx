import { useId } from 'react';
import estilos from './CampoNumerico.module.css';

type Propriedades = {
  rotulo: string; unidade?: string | null; min?: number | null; max?: number | null;
  casas?: number; valor: string; onChange: (valor: string) => void; erro?: string;
  disabled?: boolean;
};

export function CampoNumerico({ rotulo, unidade, min, max, casas, valor, onChange, erro, disabled }: Propriedades) {
  const id = useId();
  const ajuda = min != null && max != null ? `Digite apenas números, de ${min} a ${max}.` : 'Digite apenas números.';
  return <div className={estilos.campo}>
    <label htmlFor={id}>{rotulo}</label>
    <div className={`${estilos.caixa} ${erro ? estilos.invalido : ''}`}>
      <input id={id} type="text" inputMode={casas === 0 ? 'numeric' : 'decimal'} value={valor}
        disabled={disabled} autoComplete="off" maxLength={16} aria-invalid={Boolean(erro)}
        aria-describedby={`${id}-ajuda`} onChange={e => {
          const texto = e.currentTarget.value;
          if (/^[0-9.,]*$/.test(texto)) onChange(texto);
        }} />
      {unidade && <span className={estilos.unidade}>{unidade}</span>}
    </div>
    <p id={`${id}-ajuda`} className={erro ? estilos.erro : estilos.ajuda} role={erro ? 'alert' : undefined}>
      {erro || ajuda}
    </p>
  </div>;
}
