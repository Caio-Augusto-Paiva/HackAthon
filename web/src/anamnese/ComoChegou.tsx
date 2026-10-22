import { useEffect, useState } from 'react';
import { obterComo } from '../api/sessao';
import type { components } from '../api/tipos.gerado';
import { Modal } from '../componentes/Modal';
import estilos from './ComoChegou.module.css';

type Como = components['schemas']['Como'];
type Evidencia = components['schemas']['Evidencia'];
type Entrada = components['schemas']['Entrada'];

const porcento = (cf: number) => `${Math.round(Math.max(0, cf) * 100)}%`;
const legivel = (simbolo: string) => simbolo.replace(/_/g, ' ').replace(/^./, c => c.toUpperCase());
const valorLegivel = (valor: Entrada['valor']) => valor === null ? 'Não sei' : valor === true ? 'Sim' : valor === false ? 'Não' : String(valor);
const origens: Record<Entrada['origem'], string> = { resposta: 'você respondeu', ficha: 'da ficha do animal', importacao: 'importado', regra: 'deduzido' };

/** "R-X: SE a ENTÃO b" vira { se: a, entao: b }; texto fora do padrão fica inteiro. */
function frase(evidencia: Evidencia) {
  const texto = evidencia.texto.replace(new RegExp(`^${evidencia.regra_id}:\\s*`), '');
  const partes = /^SE\s+(.+?)\s+ENTÃO\s+(.+)$/.exec(texto);
  return partes ? { se: partes[1], entao: partes[2] } : { texto };
}

/** Separa o link da referência (mostrado pelo domínio) do restante da nota de fonte. */
function Fonte({ fonte }: { fonte: string | null }) {
  if (!fonte) return <p className={estilos.fonte}>Fonte não informada</p>;
  const url = /https:\/\/[^\s;]+/.exec(fonte)?.[0];
  if (!url) return <p className={estilos.fonte}>Fonte: {fonte}</p>;
  const resto = fonte.replace(url, '').replace(/^[^:]*:\s*;?\s*/, '').replace(/^;\s*/, '').trim();
  return <p className={estilos.fonte}>Fonte: <a href={url} target="_blank" rel="noreferrer noopener">{new URL(url).hostname.replace(/^www\./, '')}</a>
    {resto && <span className={estilos.nota}> · {resto}</span>}</p>;
}

function Fatos({ entradas }: { entradas: Entrada[] }) {
  return <ul className={estilos.fatos}>{entradas.map((e, i) => <li key={`${e.simbolo}-${i}`}>
    <span className={estilos.fato}><span>{legivel(e.simbolo)}</span><strong>{valorLegivel(e.valor)}</strong>
      <span className={estilos.origem}>{origens[e.origem]}</span></span>
    {e.evidencias?.length ? <details className={estilos.deducao}><summary>Como isso foi deduzido</summary>
      <ol className={estilos.aninhadas}>{e.evidencias.map((ev, j) => <Regra key={`${ev.regra_id}-${j}`} evidencia={ev} />)}</ol>
    </details> : null}
  </li>)}</ul>;
}

function Regra({ evidencia, passo }: { evidencia: Evidencia; passo?: Como['combinacao'][number] }) {
  const f = frase(evidencia);
  return <li className={estilos.regra}>
    <div className={estilos.topo}>
      <strong className={estilos.id}>{evidencia.regra_id}</strong>
      <span className={estilos.status} data-status={evidencia.status}>{evidencia.status === 'validada' ? 'Validada' : 'Suposição a validar'}</span>
      {passo && <span className={estilos.subida}><span className={estilos.trilho} aria-hidden="true">
        <span style={{ width: porcento(passo.antes) }} /><span className={estilos.ganho} style={{ left: porcento(passo.antes), width: `calc(${porcento(passo.depois)} - ${porcento(passo.antes)})` }} />
      </span><span>{porcento(passo.antes)} → {porcento(passo.depois)}</span></span>}
    </div>
    {'texto' in f ? <p className={estilos.frase}>{f.texto}</p>
      : <p className={estilos.frase}><span className={estilos.palavra}>Se</span> {f.se} <span className={estilos.palavra}>então</span> {f.entao}</p>}
    <Fatos entradas={evidencia.entradas} />
    <Fonte fonte={evidencia.fonte} />
  </li>;
}

export function ComoChegou({ sessaoId, simbolo, aoFechar }: { sessaoId: string; simbolo: string; aoFechar: () => void }) {
  const [dados, definirDados] = useState<Como>();
  const [erro, definirErro] = useState(false);
  const [tentativa, definirTentativa] = useState(0);
  useEffect(() => {
    let ativa = true; definirErro(false);
    obterComo(sessaoId, simbolo).then(d => { if (ativa) definirDados(d); }).catch(() => { if (ativa) definirErro(true); });
    return () => { ativa = false; };
  }, [sessaoId, simbolo, tentativa]);
  const resumo = dados && <p className={estilos.resumo}><strong>{dados.nome}</strong> · {dados.percentual}% de confiança.
    {dados.evidencias.length > 0 && ' Cada regra abaixo disparou e aumentou a confiança.'}</p>;
  return <Modal variante="folha" titulo="Como cheguei aqui?" resumo={resumo} aoFechar={aoFechar}>
    {erro ? <p role="alert">Não consegui carregar as evidências. <button onClick={() => definirTentativa(t => t + 1)}>Tentar novamente</button></p>
      : !dados ? <p role="status">Carregando evidências…</p>
      : dados.evidencias.length ? <ol className={estilos.lista}>{dados.evidencias.map((e, i) =>
        <Regra key={`${e.regra_id}-${i}`} evidencia={e} passo={dados.combinacao.find(c => c.apos_regra === e.regra_id)} />)}</ol>
      : <p>Nenhuma regra contribuiu para esta hipótese.</p>}
  </Modal>;
}
