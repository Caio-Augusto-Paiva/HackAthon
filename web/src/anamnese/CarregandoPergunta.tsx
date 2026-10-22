import { Boi } from '../componentes/Boi';
import estilos from './CarregandoPergunta.module.css';

export function CarregandoPergunta() {
  return <main className={`${estilos.pagina} fundoComBrilho`} aria-busy="true">
    <p role="status" className="somenteLeitor">Carregando verificação…</p>
    <div className={estilos.conjunto} aria-hidden="true"><Boi /><div className={estilos.balao}><span /><span /></div></div>
    <div className={estilos.opcoes} aria-hidden="true"><span /><span /><span /></div>
  </main>;
}
