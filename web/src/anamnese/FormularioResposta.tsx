import { useState } from 'react';
import type { components } from '../api/tipos.gerado';
import { Botao } from '../componentes/Botao';
import { CampoNumerico } from '../componentes/CampoNumerico';
import { OpcaoResposta } from '../componentes/OpcaoResposta';
import type { Escolha } from './mapearResposta';
import estilos from './FormularioResposta.module.css';

export type PropriedadesFormulario = {
  inicial?: Escolha; erro?: string; carregando: boolean; aoEnviar: (escolha: Escolha) => void;
  aoEditar: () => void; aoVoltar?: () => void;
};
type Propriedades = PropriedadesFormulario & {
  campos: components['schemas']['Campo'][]; multipla: boolean; permiteNaoSei: boolean;
};

export function FormularioResposta({ campos, multipla, permiteNaoSei, inicial, erro, carregando, aoEnviar, aoEditar, aoVoltar }: Propriedades) {
  const [escolha, definirEscolha] = useState<Escolha>(inicial ?? { tipo: 'vazia' });
  const escolher = (nova: Escolha) => { definirEscolha(nova); aoEditar(); };
  const valor = (simbolo: string) => escolha.tipo === 'valores' ? escolha.valores[simbolo] : undefined;
  const atualizar = (simbolo: string, conteudo: string | boolean) => escolher({ tipo: 'valores',
    valores: { ...(escolha.tipo === 'valores' ? escolha.valores : {}), [simbolo]: conteudo } });
  const valida = escolha.tipo === 'nao_sei' || escolha.tipo === 'nenhuma'
    || (escolha.tipo === 'multipla' && escolha.simbolos.length > 0)
    || (escolha.tipo === 'valores' && campos.every(c => c.entrada === 'numerico'
      ? typeof valor(c.simbolo) === 'string' && /^[0-9]{1,6}([.,][0-9]{1,3})?$/.test(String(valor(c.simbolo)))
      : valor(c.simbolo) !== undefined));
  return <form className={estilos.formulario} onSubmit={e => { e.preventDefault(); if (valida && !carregando) aoEnviar(escolha); }}>
    <fieldset disabled={carregando}>
      <legend className="somenteLeitor">Sua resposta</legend>
      {multipla && <p className={estilos.instrucao}>Pode marcar mais de uma opção.</p>}
      {campos.map(c => multipla
        ? <OpcaoResposta key={c.simbolo} tipo="multipla" name="resposta" value={c.simbolo}
          checked={escolha.tipo === 'multipla' && escolha.simbolos.includes(c.simbolo)} onChange={marcada => {
            const anteriores = escolha.tipo === 'multipla' ? escolha.simbolos : [];
            const simbolos = marcada ? [...anteriores, c.simbolo] : anteriores.filter(s => s !== c.simbolo);
            escolher(simbolos.length ? { tipo: 'multipla', simbolos } : { tipo: 'vazia' });
          }}>{c.rotulo ?? c.simbolo}</OpcaoResposta>
        : c.entrada === 'numerico' ? <CampoNumerico key={c.simbolo} rotulo={c.rotulo ?? c.simbolo}
          unidade={c.unidade} min={c.min} max={c.max} valor={String(valor(c.simbolo) ?? '')}
          onChange={v => atualizar(c.simbolo, v)} erro={erro} disabled={carregando} />
        : <div className={estilos.opcoes} key={c.simbolo}>
          {campos.length > 1 && <p>{c.rotulo ?? c.simbolo}</p>}
          {(c.entrada === 'booleano' ? [{ valor: true, rotulo: 'Sim' }, { valor: false, rotulo: 'Não' }] : c.opcoes ?? []).map(o =>
            <OpcaoResposta key={String(o.valor)} tipo="unica" name={c.simbolo} value={String(o.valor)}
              checked={valor(c.simbolo) === o.valor} onChange={() => atualizar(c.simbolo, o.valor)}>{o.rotulo}</OpcaoResposta>)}
        </div>)}
      {multipla && <OpcaoResposta tipo="multipla" name="resposta" value="nenhuma" checked={escolha.tipo === 'nenhuma'}
        onChange={marcada => escolher({ tipo: marcada ? 'nenhuma' : 'vazia' })}>Nenhuma alteração</OpcaoResposta>}
      {permiteNaoSei && <OpcaoResposta tipo={multipla ? 'multipla' : 'unica'} name="desconhecido" value="nao_sei"
        checked={escolha.tipo === 'nao_sei'} onChange={marcada => escolher({ tipo: marcada ? 'nao_sei' : 'vazia' })}>Não sei</OpcaoResposta>}
    </fieldset>
    {erro && !campos.some(c => c.entrada === 'numerico') && <p role="alert" className={estilos.erro}>{erro}</p>}
    <div className={estilos.acoes}>
      <Botao variante="secundario" disabled={!aoVoltar || carregando} onClick={aoVoltar}>Voltar</Botao>
      <Botao type="submit" disabled={!valida} carregando={carregando}>Responder</Botao>
    </div>
  </form>;
}
