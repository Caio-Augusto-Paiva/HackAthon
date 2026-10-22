import { useEffect, useState } from 'react';
import { obterComo } from '../api/sessao';
import type { components } from '../api/tipos.gerado';
import { Modal } from '../componentes/Modal';
import estilos from './ComoChegou.module.css';

function Evidencias({ itens }: { itens: components['schemas']['Evidencia'][] }) {
  return <ul className={estilos.lista}>{itens.map((e, indice) => <li key={`${e.regra_id}-${indice}`}>
    <strong>{e.regra_id}</strong><p>{e.texto}</p>
    <p>Fonte: {e.fonte ?? 'Não informada'} · {e.status === 'validada' ? 'Validada' : 'Suposição a validar'}</p>
    <ul>{e.entradas.map((entrada, i) => <li key={`${entrada.simbolo}-${i}`}>
      {entrada.simbolo}: {entrada.valor === null ? 'Não sei' : entrada.valor === true ? 'Sim' : entrada.valor === false ? 'Não' : String(entrada.valor)}
      {entrada.evidencias && <Evidencias itens={entrada.evidencias} />}
    </li>)}</ul>
  </li>)}</ul>;
}

export function ComoChegou({ sessaoId, simbolo, aoFechar }: { sessaoId: string; simbolo: string; aoFechar: () => void }) {
  const [dados, definirDados] = useState<components['schemas']['Como']>();
  const [erro, definirErro] = useState(false);
  const [tentativa, definirTentativa] = useState(0);
  useEffect(() => {
    let ativa = true; definirErro(false);
    obterComo(sessaoId, simbolo).then(d => { if (ativa) definirDados(d); }).catch(() => { if (ativa) definirErro(true); });
    return () => { ativa = false; };
  }, [sessaoId, simbolo, tentativa]);
  return <Modal titulo="Como cheguei aqui?" aoFechar={aoFechar}>
    {erro ? <p role="alert">Não consegui carregar as evidências. <button onClick={() => definirTentativa(t => t + 1)}>Tentar novamente</button></p>
      : !dados ? <p role="status">Carregando evidências…</p>
      : <><p><strong>{dados.nome}</strong> · {dados.percentual}% de confiança</p>
        {dados.evidencias.length ? <Evidencias itens={dados.evidencias} /> : <p>Nenhuma regra contribuiu para esta hipótese.</p>}</>}
  </Modal>;
}
