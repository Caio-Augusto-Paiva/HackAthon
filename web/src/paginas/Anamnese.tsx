import { useEffect, useRef, useState } from 'react';
import { Link, useLocation, useNavigate, useParams } from 'react-router-dom';
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
import { CarregandoPergunta } from '../anamnese/CarregandoPergunta';
import { ControleModo, ConfirmacaoEspecialista } from '../anamnese/ControleModo';
import { useTrocaModo } from '../anamnese/useTrocaModo';
import { corrigirTelaEmOutroModo } from '../anamnese/corrigirTelaEmOutroModo';
import { paraCorpoPergunta, paraCorpoTriagem, passoAtual, type Escolha } from '../anamnese/mapearResposta';
import estilos from './Anamnese.module.css';

type RespostaAnterior = { estado: EstadoSessao; escolha: Escolha };
export function Anamnese() {
  const { sessaoId = '' } = useParams();
  const navegar = useNavigate();
  const local = useLocation();
  const anuncioRota: unknown = local.state?.anuncioModo;
  const [estado, definirEstado] = useState<EstadoSessao>();
  const [erro, definirErro] = useState<string>();
  const [erroCorrecao, definirErroCorrecao] = useState<string>();
  const [enviando, definirEnviando] = useState(false);
  const [tentativa, definirTentativa] = useState(0);
  const [porqueAberto, definirPorque] = useState(false);
  const [historico, definirHistorico] = useState<RespostaAnterior[]>([]);
  const [indiceCorrecao, definirCorrecao] = useState<number>();
  const trava = useRef(false);
  const troca = useTrocaModo({ sessaoId, modo: estado?.modo, trava, definirEnviando,
    aoAtualizar: atualizado => { definirEstado(atualizado); definirCorrecao(undefined); definirPorque(false); definirErro(undefined); definirErroCorrecao(undefined); } });
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
  useEffect(() => {
    if (!troca.confirmando) document.querySelector<HTMLElement>('[data-pergunta]')?.focus();
  }, [chave, estado?.modo, troca.confirmando]);
  async function enviar(escolha: Escolha) {
    if (!tela || !estado || trava.current) return;
    trava.current = true; definirEnviando(true); definirErro(undefined); definirErroCorrecao(undefined);
    try {
      const resposta = tela.tipo === 'pergunta' ? paraCorpoPergunta(tela, escolha) : undefined;
      const corpo = tela.tipo === 'tela_triagem' ? paraCorpoTriagem(tela, escolha)
        : anterior ? { valor: resposta?.valor, ...(resposta?.nao_sei ? { nao_sei: true } : {}) } : resposta;
      const gravarHistorico = () => definirHistorico(h => anterior ? h.map((item, indice) => indice === indiceCorrecao
        ? { estado: anterior.estado, escolha } : item) : [...h, { estado, escolha }]);
      const outraVersao = tela.tipo === 'tela_triagem' && anterior?.estado.modo !== estado.modo
        ? [estado, ...historico.map(h => h.estado)].find(e => e.modo === estado.modo
          && e.proxima?.tipo === 'tela_triagem' && e.proxima.tela_id === tela.tela_id)?.proxima : undefined;
      const campos = (t: typeof tela) => t.tipo === 'tela_triagem' ? t.campos.map(c => c.simbolo).sort().join('|') : t.simbolo;
      if (anterior && outraVersao && campos(outraVersao) !== campos(tela)) {
        const resultado = await corrigirTelaEmOutroModo(sessaoId, tela, corpo, anterior.estado.modo, estado.modo);
        if (resultado.gravada) { gravarHistorico(); definirCorrecao(undefined); }
        if (resultado.estado) {
          definirEstado(resultado.estado);
          if (resultado.estado.modo !== estado.modo) troca.anunciarModo(resultado.estado.modo);
        }
        if (resultado.erro instanceof ErroApi && resultado.erro.status !== 409) definirErro(resultado.erro.message);
        else if (resultado.erro) definirErroCorrecao(resultado.erro instanceof ErroApi
          ? 'A sessão foi atualizada. Confira a resposta antes de corrigir novamente.' : resultado.erro.message);
        return;
      }
      const atualizado = await responder(sessaoId, tela, corpo, anterior !== undefined);
      gravarHistorico();
      definirCorrecao(undefined); definirEstado(atualizado);
    } catch (e) {
      if (e instanceof ErroApi && e.status === 409) {
        try { definirEstado(await obterSessao(sessaoId)); definirCorrecao(undefined); }
        catch (falha) { definirErro(falha instanceof Error ? falha.message : 'Não consegui atualizar a verificação.'); }
      } else definirErro(e instanceof Error ? e.message : 'Não consegui enviar a resposta. Tente novamente.');
    } finally { trava.current = false; definirEnviando(false); }
  }
  if (!estado) return erro ? <main className={estilos.espera}><h1>Não consegui abrir a verificação</h1><p role="alert">{erro}</p>
    <Botao onClick={() => definirTentativa(t => t + 1)}>Tentar novamente</Botao><Link to="/">Voltar ao início</Link></main> : <CarregandoPergunta />;
  const passo = passoAtual(visivel!.progresso);
  const limite = estado.progresso.limite_dinamico;
  const total = limite === null || limite === undefined ? undefined : estado.progresso.triagem_total + limite;
  const propriedades = { inicial: anterior?.escolha, erro, carregando: enviando, aoEnviar: enviar, aoEditar: () => definirErro(undefined),
    aoVoltar: historico.length && indiceCorrecao !== 0 ? () => definirCorrecao(indiceCorrecao === undefined ? historico.length - 1 : indiceCorrecao - 1) : undefined };
  return <div className={`${estilos.pagina} fundoComBrilho`}><main className={estilos.principal}>
    <header className={estilos.cabecalho}><Link to="/">Anamnese Bovina</Link>
      <ControleModo modo={estado.modo} enviando={enviando} aoMudar={troca.solicitar} />
      <span className={estilos.contador}>{total === undefined ? `Pergunta ${passo}` : `Pergunta ${passo} de até ${total}`}</span></header>
    {troca.erro && <p role="alert" className={estilos.erroModo}>{troca.erro}</p>}
    {erroCorrecao && <p role="alert" className={estilos.erroModo}>{erroCorrecao}</p>}
    {(troca.anuncio || typeof anuncioRota === 'string') && <p role="status" className="somenteLeitor">{troca.anuncio || String(anuncioRota)}</p>}
    {total !== undefined && <BarraProgresso atual={passo - 1} total={total} />}
    <div className={estilos.dialogo} key={`${estado.modo}-${chave}-${indiceCorrecao ?? 'atual'}`}>
      {tela ? <><Balao texto={tela.tipo === 'tela_triagem' ? tela.titulo : tela.texto} aoPorque={() => definirPorque(true)} />
        <div className={estilos.resposta} key={`${chave}-${indiceCorrecao ?? 'atual'}`}>
          {anterior && <p className={estilos.correcao}>Corrigindo resposta anterior. <button onClick={() => { definirCorrecao(undefined); definirErro(undefined); }}>Retomar pergunta atual</button></p>}
          {tela.tipo === 'tela_triagem' ? <TelaTriagem tela={tela} {...propriedades} /> : <PerguntaDinamica pergunta={tela} {...propriedades} />}
          {!anterior && <Link className={estilos.verAnalise} to={`/parecer/${encodeURIComponent(sessaoId)}`} aria-disabled={enviando}
            onClick={e => { if (enviando) e.preventDefault(); }}>Ver análise agora</Link>}
        </div>
        {porqueAberto && <PorQue sessaoId={sessaoId} simbolos={tela.tipo === 'tela_triagem' ? tela.campos.map(c => c.simbolo) : [tela.simbolo]} aoFechar={() => definirPorque(false)} />}
      </> : <p role="status">{estado.alerta?.pausa ? estado.alerta.texto : 'Abrindo parecer…'}</p>}
    </div>
  </main>{passo > 1 && <BarraHipoteses sessaoId={sessaoId} revisao={estado.revisao} />}
    {estado.alerta?.pausa && !troca.confirmando && <AlertaBandeira alerta={estado.alerta} sessaoId={sessaoId} aoAtualizar={definirEstado}
      erroExterno={troca.erro} complemento={<ControleModo modo={estado.modo} enviando={enviando} aoMudar={troca.solicitar} />} />}
    {troca.confirmando && <ConfirmacaoEspecialista enviando={enviando} aoConfirmar={troca.confirmar} aoFechar={troca.fechar} />}
  </div>;
}
