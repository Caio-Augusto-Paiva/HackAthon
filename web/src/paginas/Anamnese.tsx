import { useEffect, useRef, useState } from 'react';
import { Link, useNavigate, useParams } from 'react-router-dom';
import { ErroApi } from '../api/cliente';
import { obterSessao, responder, type EstadoSessao } from '../api/sessao';
import { BarraProgresso } from '../componentes/BarraProgresso';
import { Balao } from '../componentes/Balao';
import { Botao } from '../componentes/Botao';
import { TelaTriagem } from '../anamnese/TelaTriagem';
import { PerguntaDinamica } from '../anamnese/PerguntaDinamica';
import { BarraHipoteses } from '../anamnese/BarraHipoteses';
import { PorQue } from '../anamnese/PorQue';
import { AlertaBandeira } from '../anamnese/AlertaBandeira';
import { paraCorpoPergunta, paraCorpoTriagem, passoAtual, type Escolha } from '../anamnese/mapearResposta';
import estilos from './Anamnese.module.css';

type RespostaAnterior = { estado: EstadoSessao; escolha: Escolha };
export function Anamnese() {
  const { sessaoId = '' } = useParams();
  const navegar = useNavigate();
  const [estado, definirEstado] = useState<EstadoSessao>();
  const [erro, definirErro] = useState<string>();
  const [enviando, definirEnviando] = useState(false);
  const [tentativa, definirTentativa] = useState(0);
  const [porqueAberto, definirPorque] = useState(false);
  const [historico, definirHistorico] = useState<RespostaAnterior[]>([]);
  const [indiceCorrecao, definirCorrecao] = useState<number>();
  const trava = useRef(false);
  useEffect(() => {
    let ativa = true;
    definirErro(undefined);
    obterSessao(sessaoId).then(e => { if (ativa) definirEstado(e); })
      .catch(e => { if (ativa) definirErro(e instanceof Error ? e.message : 'Não consegui abrir a verificação.'); });
    return () => { ativa = false; };
  }, [sessaoId, tentativa]);
  useEffect(() => {
    if (estado?.fase === 'encerrada' && !estado.alerta?.pausa) navegar(`/parecer/${encodeURIComponent(sessaoId)}`, { replace: true });
  }, [estado, navegar, sessaoId]);
  const anterior = indiceCorrecao === undefined ? undefined : historico[indiceCorrecao];
  const visivel = anterior?.estado ?? estado;
  const tela = visivel?.proxima;
  const chave = tela?.tipo === 'tela_triagem' ? tela.tela_id : tela?.simbolo;
  useEffect(() => { document.querySelector<HTMLElement>('[data-pergunta]')?.focus(); }, [chave]);
  async function enviar(escolha: Escolha) {
    if (!tela || !estado || trava.current) return;
    trava.current = true; definirEnviando(true); definirErro(undefined);
    try {
      const corpo = tela.tipo === 'tela_triagem' ? paraCorpoTriagem(tela, escolha) : paraCorpoPergunta(tela, escolha);
      const atualizado = await responder(sessaoId, tela, corpo, anterior !== undefined);
      definirHistorico(h => anterior ? h.slice(0, indiceCorrecao).concat({ estado: anterior.estado, escolha }) : [...h, { estado, escolha }]);
      definirCorrecao(undefined); definirEstado(atualizado);
    } catch (e) {
      if (e instanceof ErroApi && e.status === 409) {
        try { definirEstado(await obterSessao(sessaoId)); definirHistorico([]); definirCorrecao(undefined); }
        catch (falha) { definirErro(falha instanceof Error ? falha.message : 'Não consegui atualizar a verificação.'); }
      } else definirErro(e instanceof Error ? e.message : 'Não consegui enviar a resposta. Tente novamente.');
    } finally { trava.current = false; definirEnviando(false); }
  }
  if (!estado) return <main className={estilos.espera}>{erro ? <><h1>Não consegui abrir a verificação</h1><p role="alert">{erro}</p>
    <Botao onClick={() => definirTentativa(t => t + 1)}>Tentar novamente</Botao><Link to="/">Voltar ao início</Link></> : <p role="status">Carregando verificação…</p>}</main>;
  const passo = passoAtual(visivel!.progresso);
  const total = estado.progresso.triagem_total + estado.progresso.limite_dinamico;
  const propriedades = { inicial: anterior?.escolha, erro, carregando: enviando, aoEnviar: enviar, aoEditar: () => definirErro(undefined),
    aoVoltar: historico.length && indiceCorrecao !== 0 ? () => definirCorrecao(indiceCorrecao === undefined ? historico.length - 1 : indiceCorrecao - 1) : undefined };
  return <div className={`${estilos.pagina} fundoComBrilho`}><main className={estilos.principal}>
    <header className={estilos.cabecalho}><Link to="/">Anamnese Bovina</Link><span className={estilos.modo}>Modo {estado.modo === 'produtor' ? 'produtor' : 'especialista'}</span>
      <span className={estilos.contador}>Pergunta {passo} de até {total}</span></header>
    <BarraProgresso atual={passo - 1} total={total} />
    <div className={estilos.dialogo}>
      {tela ? <><Balao texto={tela.tipo === 'tela_triagem' ? tela.titulo : tela.texto} aoPorque={() => definirPorque(true)} />
        <div className={estilos.resposta} key={`${chave}-${indiceCorrecao ?? 'atual'}`}>
          {anterior && <p className={estilos.correcao}>Corrigindo resposta anterior. <button onClick={() => { definirCorrecao(undefined); definirErro(undefined); }}>Retomar pergunta atual</button></p>}
          {tela.tipo === 'tela_triagem' ? <TelaTriagem tela={tela} {...propriedades} /> : <PerguntaDinamica pergunta={tela} {...propriedades} />}
        </div>
        {porqueAberto && <PorQue sessaoId={sessaoId} simbolos={tela.tipo === 'tela_triagem' ? tela.campos.map(c => c.simbolo) : [tela.simbolo]} aoFechar={() => definirPorque(false)} />}
      </> : <p role="status">{estado.alerta?.pausa ? estado.alerta.texto : 'Abrindo parecer…'}</p>}
    </div>
  </main>{passo > 1 && <BarraHipoteses sessaoId={sessaoId} revisao={estado.revisao} />}
    {estado.alerta?.pausa && <AlertaBandeira alerta={estado.alerta} sessaoId={sessaoId} aoAtualizar={definirEstado} />}
  </div>;
}
