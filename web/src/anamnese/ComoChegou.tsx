import { useEffect, useState } from 'react';
import { obterComo } from '../api/sessao';
import type { components } from '../api/tipos.gerado';
import { Modal } from '../componentes/Modal';
import estilos from './ComoChegou.module.css';

type Como = components['schemas']['Como'];
type Evidencia = components['schemas']['Evidencia'];
type Entrada = components['schemas']['Entrada'];

const porcento = (cf: number) => `${Math.round(Math.max(0, cf) * 100)}%`;
const legivel = (e: Entrada) => e.nome ?? e.simbolo.replace(/_/g, ' ').replace(/^./, c => c.toUpperCase());
const valorLegivel = (valor: Entrada['valor']) => valor === null ? 'não sei' : valor === true ? 'sim' : valor === false ? 'não' : String(valor);
const origens: Record<Entrada['origem'], string> = { resposta: 'você respondeu', ficha: 'da ficha do animal', importacao: 'importado', regra: 'calculado pelo sistema' };

/** Só o domínio do link, ou o texto da fonte quando não há link. */
function Fonte({ fonte }: { fonte: string | null }) {
  if (!fonte) return null;
  const url = /https:\/\/[^\s;]+/.exec(fonte)?.[0];
  return <p className={estilos.fonte}>Fonte: {url
    ? <a href={url} target="_blank" rel="noreferrer noopener">{new URL(url).hostname.replace(/^www\./, '')}</a>
    : fonte}</p>;
}

function Fato({ entrada }: { entrada: Entrada }) {
  const deducao = entrada.evidencias?.find(e => e.frase);
  return <li className={estilos.fato}>
    <span><strong>{legivel(entrada)}</strong>: {valorLegivel(entrada.valor)} <span className={estilos.origem}>({origens[entrada.origem]})</span></span>
    {deducao && <span className={estilos.deducao}>O sistema concluiu isso porque foi observado: {deducao.frase}.</span>}
  </li>;
}

function Passo({ evidencia, passo }: { evidencia: Evidencia; passo?: Como['combinacao'][number] }) {
  const diminui = evidencia.cf_regra < 0;
  return <li className={estilos.regra}>
    {passo && <div className={estilos.subida}>
      <span className={estilos.trilho} aria-hidden="true">
        <span style={{ width: porcento(Math.min(passo.antes, passo.depois)) }} />
        <span className={estilos.ganho} style={{ left: porcento(Math.min(passo.antes, passo.depois)), width: `calc(${porcento(Math.max(passo.antes, passo.depois))} - ${porcento(Math.min(passo.antes, passo.depois))})` }} />
      </span>
      <span className={estilos.numeros}>{porcento(passo.antes)} → {porcento(passo.depois)}</span>
    </div>}
    <p className={estilos.frase}>{diminui ? 'Isto diminuiu a chance' : 'Porque foi observado'}: {evidencia.frase || evidencia.texto}.</p>
    <ul className={estilos.fatos}>{evidencia.entradas.map((e, i) => <Fato key={`${e.simbolo}-${i}`} entrada={e} />)}</ul>
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
    {dados.evidencias.length > 0 && ' Veja abaixo cada sinal que fez a chance subir.'}</p>;
  return <Modal variante="folha" titulo="Como cheguei aqui?" resumo={resumo} aoFechar={aoFechar}>
    {erro ? <p role="alert">Não consegui carregar a explicação. <button onClick={() => definirTentativa(t => t + 1)}>Tentar novamente</button></p>
      : !dados ? <p role="status">Carregando explicação…</p>
      : dados.evidencias.length ? <>
        <ol className={estilos.lista}>{dados.evidencias.map((e, i) =>
          <Passo key={`${e.regra_id}-${i}`} evidencia={e} passo={dados.combinacao.find(c => c.apos_regra === e.regra_id)} />)}</ol>
        <p className={estilos.nota}>Estas regras ainda são suposições: precisam ser conferidas por um médico-veterinário.</p>
      </>
      : <p>Nenhum sinal informado até agora aponta para esta doença.</p>}
  </Modal>;
}
