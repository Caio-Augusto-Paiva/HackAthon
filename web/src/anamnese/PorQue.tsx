import { useEffect, useState } from 'react';
import { obterPorque, type Porque } from '../api/sessao';
import { Modal } from '../componentes/Modal';

export function PorQue({ sessaoId, simbolos, aoFechar }: { sessaoId: string; simbolos: string[]; aoFechar: () => void }) {
  const [motivos, definirMotivos] = useState<Porque[]>();
  const [erro, definirErro] = useState(false);
  const [tentativa, definirTentativa] = useState(0);
  const chave = simbolos.join('|');
  useEffect(() => {
    let ativa = true;
    definirErro(false);
    Promise.all(chave.split('|').map(s => obterPorque(sessaoId, s))).then(m => { if (ativa) definirMotivos(m); })
      .catch(() => { if (ativa) definirErro(true); });
    return () => { ativa = false; };
  }, [sessaoId, chave, tentativa]);
  return <Modal titulo="Por que estou perguntando isso?" aoFechar={aoFechar}>
    {erro ? <p role="alert">Não consegui carregar a explicação. <button onClick={() => definirTentativa(t => t + 1)}>Tentar novamente</button></p>
      : !motivos ? <p role="status">Carregando explicação…</p>
      : motivos.map(m => <section key={m.simbolo}><p>{m.motivo}</p>
        {m.serve_a.length ? <ul>{m.serve_a.map(d => <li key={d.doenca}><strong>{d.nome}</strong> — {d.regras.join(', ')}</li>)}</ul>
          : <p>Sem doenças associadas a esta pergunta.</p>}</section>)}
  </Modal>;
}
