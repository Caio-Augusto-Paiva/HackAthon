import { useEffect, useRef, useState, type CSSProperties } from 'react';
import { Link, useNavigate, useParams } from 'react-router-dom';
import { agirBandeira, obterParecer, obterSessao, type Parecer as DadosParecer } from '../api/sessao';
import { ErroApi } from '../api/cliente';
import { Botao } from '../componentes/Botao';
import { Boi } from '../componentes/Boi';
import { BarraConfianca } from '../componentes/BarraConfianca';
import { Contador } from '../componentes/Contador';
import { ComoChegou } from '../anamnese/ComoChegou';
import { ControleModo, ConfirmacaoEspecialista } from '../anamnese/ControleModo';
import { useTrocaModo } from '../anamnese/useTrocaModo';
import alerta from '../assets/alerta-parecer.svg';
import estilos from './Parecer.module.css';

const gravidades = { alta: 'Alta', media: 'Média', baixa: 'Baixa' };
const urgencias = { chamar_agora: 'Chamar agora', observar: 'Observar de perto', sem_problema: 'Sem problema identificado' };
const listaPt = new Intl.ListFormat('pt-BR', { type: 'conjunction' });
export function Parecer() {
  const { sessaoId = '' } = useParams();
  const navegar = useNavigate();
  const [dados, definirDados] = useState<DadosParecer>();
  const [erro, definirErro] = useState<string>();
  const [tentativa, definirTentativa] = useState(0);
  const [comoAberto, definirComo] = useState(false);
  const [retomando, definirRetomando] = useState(false);
  const trava = useRef(false);
  const troca = useTrocaModo({ sessaoId, modo: dados?.modo, trava, definirEnviando: definirRetomando,
    aoAtualizar: atualizado => navegar(`/anamnese/${encodeURIComponent(atualizado.sessao_id)}`, { state: { anuncioModo: `Modo ${atualizado.modo === 'produtor' ? 'produtor' : 'especialista'} ativado.` } }) });
  async function retomar() {
    if (trava.current) return;
    trava.current = true; definirRetomando(true); definirErro(undefined);
    try {
      const estado = await agirBandeira(sessaoId, 'continuar').catch(e => {
        if (e instanceof ErroApi && e.status === 409) return obterSessao(sessaoId);
        throw e;
      });
      if (estado.fase === 'encerrada' && !estado.alerta?.pausa) {
        definirDados(await obterParecer(sessaoId));
        definirErro('O sistema concluiu a consulta e não tem outra pergunta disponível.');
      } else navegar(`/anamnese/${encodeURIComponent(sessaoId)}`);
    } catch (e) { definirErro(e instanceof Error ? e.message : 'Não consegui retomar as perguntas. Tente novamente.'); }
    finally { trava.current = false; definirRetomando(false); }
  }
  useEffect(() => {
    let ativa = true; definirErro(undefined);
    obterParecer(sessaoId).then(p => { if (ativa) definirDados(p); })
      .catch(e => { if (ativa) definirErro(e instanceof Error ? e.message : 'Não consegui carregar o parecer.'); });
    return () => { ativa = false; };
  }, [sessaoId, tentativa]);
  useEffect(() => { if (dados) document.querySelector<HTMLElement>('h1')?.focus(); }, [dados]);
  if (!dados) return <main className={estilos.espera}>{erro ? <><h1>Não consegui abrir o parecer</h1><p role="alert">{erro}</p>
    <Botao onClick={() => definirTentativa(t => t + 1)}>Tentar novamente</Botao><Link to="/">Voltar ao início</Link></> : <p role="status">Carregando parecer…</p>}</main>;
  const blocos = dados.blocos.map(b => ({ ...b, itens: [...b.itens].sort((a, b) => b.percentual - a.percentual) }));
  const primeira = blocos.flatMap(b => b.itens)[0];
  const nenhumaConfirmada = blocos.every(b => b.itens.every(i => i.percentual === 0));
  const nomes = new Map(blocos.flatMap(b => b.itens).map(i => [i.doenca, i.nome]));
  const tratar = blocos.flatMap(b => b.itens).filter(i => i.percentual > 20 && /^https:\/\//i.test(i.tratamento?.url ?? ''));
  let posicao = 0;
  return <div className={estilos.pagina}>
    <header className={estilos.cabecalho}><Link to="/">Anamnese Bovina</Link><span>Modo {dados.modo === 'produtor' ? 'produtor' : 'especialista'}</span>
      <span>{dados.final ? 'Verificação concluída' : 'Verificação em andamento'}</span></header>
    <main className={estilos.conteudo}>
      <div className={estilos.titulo}><Boi tamanho={96} /><div><h1 tabIndex={-1}>Pronto! Este é o meu parecer</h1><p>Doenças em ordem decrescente de confiança</p></div></div>
      {!dados.final && <p className={estilos.parcial}>Parecer parcial</p>}
      <section role="status" data-nivel={dados.urgencia.nivel} className={estilos.urgencia}>
        <img src={alerta} width={30} height={30} alt="" /><div><h2>{urgencias[dados.urgencia.nivel]}</h2><p>{dados.urgencia.texto}</p></div>
      </section>
      {nenhumaConfirmada && <section role="status" className={estilos.nadaFechou}>
        <p>Nenhuma doença foi confirmada com as respostas dadas. Responda mais perguntas para o sistema calcular as chances.</p>
      </section>}
      <aside role="note" aria-labelledby="titulo-laudo" className={estilos.laudo}>
        <h2 id="titulo-laudo">Este parecer não é um laudo</h2>
        <p>Esta análise não substitui um laudo médico e é importante procurar um médico-veterinário para melhor entendimento e segurança.</p>
      </aside>
      <div className={estilos.quadro}><table className={estilos.tabela}>
        <caption className="somenteLeitor">Hipóteses e confiança do sistema</caption>
        <thead className="somenteLeitor"><tr><th>Ordem</th><th>Doença</th><th>Gravidade</th><th>Confiança</th></tr></thead>
        {blocos.map(bloco => <tbody key={bloco.id}><tr className={estilos.bloco}><th colSpan={4} scope="rowgroup">{bloco.titulo}</th></tr>
          {bloco.itens.length ? bloco.itens.map(item => { const ordem = posicao; return <tr key={item.doenca} className={estilos.linha} style={{ '--ordem': ordem } as CSSProperties}>
            <td className={estilos.posicao}>{++posicao}º</td><th scope="row" className={estilos.doenca}>{item.nome}</th>
            <td><span className={estilos.gravidade} data-gravidade={item.gravidade}><span className={estilos.prefixo}>Gravidade </span>{gravidades[item.gravidade]}</span></td>
            <td><div className={estilos.confianca}><BarraConfianca percentual={item.percentual} rotulo={item.nome} atraso={200 + ordem * 70} /><strong><Contador valor={item.percentual} atraso={200 + ordem * 70} /></strong></div>
              {item.potencial > item.percentual && <small className={estilos.potencial}>pode chegar a {item.potencial}%</small>}</td>
          </tr>; }) : <tr><td colSpan={4} className={estilos.vazio}>Nenhuma hipótese neste grupo.</td></tr>}
        </tbody>)}
      </table><p className={estilos.aviso}>{dados.aviso}</p>
      {dados.inconclusivas.length > 0 && <p className={estilos.aviso}>Hipóteses inconclusivas: {listaPt.format(dados.inconclusivas.map(id => nomes.get(id) ?? id))}.</p>}
      {dados.sinais_nao_verificados?.length ? <p className={estilos.aviso}>Sinais graves ainda não verificados: {listaPt.format(dados.sinais_nao_verificados)}.</p> : null}
      </div>
      {dados.final && tratar.length > 0 && <section aria-labelledby="titulo-tratar" className={estilos.tratar}>
        <h2 id="titulo-tratar">Como tratar</h2>
        <p>Informação geral de fonte pública. O tratamento deve ser indicado por um médico-veterinário.</p>
        <div className={estilos.tratarLinks}>{tratar.map(i => <a key={i.doenca} href={i.tratamento!.url} target="_blank" rel="noopener noreferrer">
          <span>Como tratar {i.nome}</span><span className={estilos.tratarFonte}>{i.tratamento!.titulo}</span></a>)}</div>
      </section>}
      <div className={estilos.acoes}><Link className={estilos.nova} to="/">Nova verificação</Link><Link className={estilos.privacidade} to="/privacidade">Política de privacidade</Link>
        <Botao variante="secundario" disabled={!primeira} onClick={() => definirComo(true)}>Como cheguei aqui?</Botao>
        {!dados.final && <Link className={estilos.continuar} to={`/anamnese/${encodeURIComponent(sessaoId)}`}>Continuar respondendo</Link>}
        {!dados.final && <ControleModo modo={dados.modo} mostrarModo={false} enviando={retomando} aoMudar={troca.solicitar} />}
        {dados.final && dados.motivo_parada === null && <Botao variante="secundario" carregando={retomando} onClick={retomar}>Continuar respondendo</Botao>}
      </div>
      {erro && <p role="alert" className={estilos.erro}>{erro}</p>}
      {troca.erro && <p role="alert" className={estilos.erro}>{troca.erro}</p>}
      {troca.confirmando && <ConfirmacaoEspecialista enviando={retomando} aoConfirmar={troca.confirmar} aoFechar={troca.fechar} />}
      {comoAberto && primeira && <ComoChegou sessaoId={sessaoId} simbolo={primeira.doenca} aoFechar={() => definirComo(false)} />}
    </main>
  </div>;
}
