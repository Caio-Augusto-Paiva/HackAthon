import { useEffect, useState } from 'react';
import { obterParecer, type Parecer } from '../api/sessao';
import { BarraConfianca } from '../componentes/BarraConfianca';
import estilos from './BarraHipoteses.module.css';

export function BarraHipoteses({ sessaoId, revisao }: { sessaoId: string; revisao: number }) {
  const [parecer, definirParecer] = useState<Parecer>();
  const [erro, definirErro] = useState(false);
  const [tentativa, definirTentativa] = useState(0);
  useEffect(() => {
    let ativa = true;
    definirErro(false);
    definirParecer(undefined);
    obterParecer(sessaoId).then(p => { if (ativa) definirParecer(p); }).catch(() => { if (ativa) definirErro(true); });
    return () => { ativa = false; };
  }, [sessaoId, revisao, tentativa]);
  const itens = parecer?.blocos.flatMap(b => b.itens).sort((a, b) => b.percentual - a.percentual).slice(0, 4);
  return <aside className={estilos.lateral} aria-label="Hipóteses do sistema">
    <h2>O que estou pensando</h2><p>A cada resposta, as hipóteses vão ficando mais claras.</p>
    {erro ? <div role="alert">Não consegui atualizar as hipóteses. <button onClick={() => definirTentativa(t => t + 1)}>Tentar novamente</button></div>
      : !itens ? <p role="status">Atualizando hipóteses…</p>
      : <ul>{itens.map(i => <li key={i.doenca}><div><strong>{i.nome}</strong><span>{i.percentual}%</span></div>
        <BarraConfianca percentual={i.percentual} rotulo={i.nome} /></li>)}</ul>}
    <p className={estilos.nota}>A porcentagem é a confiança do sistema, não uma probabilidade.</p>
  </aside>;
}
