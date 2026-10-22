import { useEffect, useState } from 'react';
import { obterPorque, type Porque } from '../api/sessao';
import { Modal } from '../componentes/Modal';
import estilos from './PorQue.module.css';

type Doenca = Porque['serve_a'][number];

const juntar = (itens: string[]) => itens.length <= 1 ? itens.join('') : `${itens.slice(0, -1).join(', ')} ou ${itens.at(-1)}`;
const maiuscula = (texto: string) => texto.charAt(0).toUpperCase() + texto.slice(1);

/** Uma frase por doença, em linguagem comum: sem ids de regra. */
function Frase({ doenca }: { doenca: Doenca }) {
  const sinais = doenca.sinais ?? [];
  const contra = doenca.sinais_contra ?? [];
  return <li className={estilos.item}>
    <span className={estilos.textos}>
      {sinais.length
        ? <span>Em casos de <strong>{doenca.nome}</strong>, o animal pode apresentar {juntar(sinais)}.</span>
        : !contra.length && <span>A resposta ajuda a confirmar ou afastar <strong>{doenca.nome}</strong>.</span>}
      {contra.length > 0 && <span className={sinais.length ? estilos.contra : undefined}>
        {!sinais.length && <><strong>{doenca.nome}</strong>: </>}{maiuscula(juntar(contra))} torna essa hipótese menos provável.
      </span>}
    </span>
  </li>;
}

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
      : <div className={estilos.corpo}>
        {motivos.map(m => <section key={m.simbolo} className={estilos.secao}>
          {motivos.length > 1 && <h3>{m.pergunta}</h3>}
          {m.serve_a.length
            ? <ul className={estilos.lista}>{m.serve_a.map(d => <Frase key={d.doenca} doenca={d} />)}</ul>
            : <p>Esta resposta não está ligada a nenhuma doença no momento.</p>}
        </section>)}
      </div>}
  </Modal>;
}
