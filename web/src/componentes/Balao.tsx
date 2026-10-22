import { Boi } from './Boi';
import ajuda from '../assets/ajuda.svg';
import estilos from './Balao.module.css';

export function Balao({ texto, aoPorque }: { texto: string; aoPorque?: () => void }) {
  return <div className={estilos.conjunto}>
    <div className={estilos.boi}><Boi /></div>
    <section className={estilos.balao}>
      <h1 tabIndex={-1} data-pergunta>{texto}</h1>
      {aoPorque && <button type="button" onClick={aoPorque} className={estilos.porque}>
        <img src={ajuda} alt="" width={20} height={20} />Por que estou perguntando isso?
      </button>}
    </section>
  </div>;
}
