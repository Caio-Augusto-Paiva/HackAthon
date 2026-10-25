import { act, render, screen, waitFor, within } from '@testing-library/react';
import userEvent from '@testing-library/user-event';
import { MemoryRouter, Route, Routes, useLocation } from 'react-router-dom';
import { describe, expect, it, vi } from 'vitest';
import type { EstadoSessao } from '../api/sessao';
import { primeira, segunda, multipla, perguntaDinamica, exemploParecer, exemploPorque, estadoPausado, resposta } from '../teste/cenarios';
import { Anamnese } from './Anamnese';

type Mutacao = { caminho: string; metodo: string; corpo: unknown };
type Controle = { estado: EstadoSessao; mutacoes: Mutacao[] };
function simular(inicial: EstadoSessao, aoEnviar?: (controle: Controle, mutacao: Mutacao) => Promise<Response> | Response) {
  const controle: Controle = { estado: inicial, mutacoes: [] };
  vi.stubGlobal('fetch', vi.fn(async (caminho: string, opcoes: RequestInit) => {
    if (caminho.endsWith('/parecer')) return resposta(exemploParecer);
    if (caminho.includes('/porque/')) return resposta(exemploPorque);
    if (opcoes.method !== 'GET') {
      const mutacao = { caminho, metodo: String(opcoes.method), corpo: JSON.parse(String(opcoes.body)) as unknown };
      controle.mutacoes.push(mutacao);
      if (aoEnviar) return aoEnviar(controle, mutacao);
      controle.estado = segunda;
    }
    return resposta(controle.estado);
  }));
  return controle;
}
function Destino() { return <p>Destino: {useLocation().pathname}</p>; }
function montar() {
  render(<MemoryRouter initialEntries={['/anamnese/ses_0001']}><Routes>
    <Route path="/anamnese/:sessaoId" element={<Anamnese />} />
    <Route path="/parecer/:sessaoId" element={<Destino />} />
  </Routes></MemoryRouter>);
}

describe('diálogo da anamnese', () => {
  it('envia todos os campos booleanos da seleção múltipla', async () => {
    const controle = simular(multipla);
    montar();
    await userEvent.click(await screen.findByRole('checkbox', { name: 'Abatida' }));
    await userEvent.click(screen.getByRole('button', { name: 'Responder' }));
    await waitFor(() => expect(controle.mutacoes).toHaveLength(1));
    expect(controle.mutacoes[0].corpo).toEqual({ valores: { apatia: true, claudicacao: false, decubito: false } });
  });

  it('exige uma escolha explícita e envia todos false para Nenhuma alteração', async () => {
    const controle = simular(multipla);
    montar();
    expect(await screen.findByRole('button', { name: 'Responder' })).toBeDisabled();
    await userEvent.click(screen.getByRole('checkbox', { name: 'Nenhuma alteração' }));
    await userEvent.click(screen.getByRole('button', { name: 'Responder' }));
    await waitFor(() => expect(controle.mutacoes).toHaveLength(1));
    expect(controle.mutacoes[0].corpo).toEqual({ valores: { apatia: false, claudicacao: false, decubito: false } });
  });

  it('envia desconhecimento sem tratar sinais como ausentes', async () => {
    const controle = simular(multipla);
    montar();
    await userEvent.click(await screen.findByRole('checkbox', { name: 'Não sei' }));
    await userEvent.click(screen.getByRole('button', { name: 'Responder' }));
    await waitFor(() => expect(controle.mutacoes).toHaveLength(1));
    expect(controle.mutacoes[0].corpo).toEqual({ nao_sei: true });
  });

  it('envia o número como string e mantém a pergunta com o erro 422 no campo', async () => {
    const controle = simular(primeira, () => resposta({ erro: { codigo: 'resposta_invalida',
      mensagem: 'Use só números inteiros: sem vírgula, ponto, sinal ou letras.', requisicao_id: 'rq_numero' } }, 422));
    montar();
    const campo = await screen.findByRole('textbox', { name: 'Número de dias desde o parto' });
    await userEvent.type(campo, '12,5');
    await userEvent.click(screen.getByRole('button', { name: 'Responder' }));
    await waitFor(() => expect(campo).toHaveAttribute('aria-invalid', 'true'));
    expect(campo).toHaveValue('12,5');
    expect(campo).toHaveAccessibleDescription('Use só números inteiros: sem vírgula, ponto, sinal ou letras.');
    expect(screen.getByRole('button', { name: 'Responder' })).toBeEnabled();
    expect(controle.mutacoes[0].corpo).toEqual({ valores: { dias_em_lactacao: '12,5' } });
  });

  it('mostra a lateral a partir da segunda pergunta com os quatro maiores percentuais da API', async () => {
    simular(primeira);
    montar();
    await userEvent.type(await screen.findByRole('textbox'), '12');
    expect(screen.queryByRole('complementary')).not.toBeInTheDocument();
    await userEvent.click(screen.getByRole('button', { name: 'Responder' }));
    const lateral = await screen.findByRole('complementary');
    await waitFor(() => expect(within(lateral).getAllByRole('meter')).toHaveLength(4));
    expect(within(lateral).getAllByRole('meter').map(m => m.getAttribute('aria-valuenow'))).toEqual(['87', '32', '15', '5']);
    expect(lateral).toHaveTextContent('A porcentagem é a confiança do sistema, não uma probabilidade.');
    expect(screen.getByText('Pergunta 2 de até 18')).toBeInTheDocument();
  });

  it('abre o porquê com as doenças em frases simples, sem a legenda da triagem', async () => {
    simular(primeira);
    montar();
    await userEvent.click(await screen.findByRole('button', { name: 'Por que estou perguntando isso?' }));
    const dialogo = await screen.findByRole('dialog');
    expect(await within(dialogo).findByText(/Em casos de/)).toBeInTheDocument();
    expect(dialogo).not.toHaveTextContent(exemploPorque.motivo);
    expect(dialogo).toHaveTextContent('Em casos de Mastite clínica, o animal pode apresentar grumos na caneca.');
    expect(dialogo).not.toHaveTextContent('R-MAS-03');
  });

  it('no porquê, separa o sinal que afasta a doença e cai num texto simples sem sinais', async () => {
    const porque = { ...exemploPorque, serve_a: [
      { ...exemploPorque.serve_a[0], nome: 'Hipocalcemia', sinais: ['hipotermia'], sinais_contra: ['febre'] },
      { ...exemploPorque.serve_a[0], doenca: 'tpb', nome: 'Tristeza parasitária', sinais: [], sinais_contra: [] },
    ] };
    simular(primeira);
    vi.mocked(globalThis.fetch).mockImplementation(async (caminho: RequestInfo | URL) =>
      resposta(String(caminho).includes('/porque/') ? porque : String(caminho).endsWith('/parecer') ? exemploParecer : primeira));
    montar();
    await userEvent.click(await screen.findByRole('button', { name: 'Por que estou perguntando isso?' }));
    const dialogo = await screen.findByRole('dialog');
    expect(await within(dialogo).findByText(/Em casos de/)).toBeInTheDocument();
    expect(dialogo).toHaveTextContent('Em casos de Hipocalcemia, o animal pode apresentar hipotermia.');
    expect(dialogo).toHaveTextContent('Febre torna essa hipótese menos provável.');
    expect(dialogo).toHaveTextContent('A resposta ajuda a confirmar ou afastar Tristeza parasitária.');
  });

  it('impede dois POSTs durante um duplo clique', async () => {
    let concluir!: (valor: Response) => void;
    const controle = simular(primeira, () => new Promise(resolve => { concluir = resolve; }));
    montar();
    await userEvent.type(await screen.findByRole('textbox'), '12');
    await userEvent.dblClick(screen.getByRole('button', { name: 'Responder' }));
    expect(controle.mutacoes).toHaveLength(1);
    expect(screen.getByRole('button', { name: /Responder/ })).toBeDisabled();
    await act(async () => concluir(resposta(segunda)));
  });

  it('relê o estado depois de 409, sem repetir a mutação nem mostrar mensagem técnica', async () => {
    const controle = simular(primeira, c => {
      c.estado = segunda;
      return resposta({ erro: { codigo: 'ja_respondida', mensagem: 'Revisão alterada por outra requisição.', requisicao_id: 'rq_409' } }, 409);
    });
    montar();
    await userEvent.type(await screen.findByRole('textbox'), '12');
    await userEvent.click(screen.getByRole('button', { name: 'Responder' }));
    expect(await screen.findByRole('heading', { name: 'Como estão as orelhas e as pontas dos membros?' })).toBeInTheDocument();
    expect(controle.mutacoes).toHaveLength(1);
    expect(screen.queryByText('Revisão alterada por outra requisição.')).not.toBeInTheDocument();
  });

  it('envia booleano de uma pergunta dinâmica, sem CF', async () => {
    const controle = simular(perguntaDinamica);
    montar();
    await userEvent.click(await screen.findByRole('radio', { name: 'Sim' }));
    await userEvent.click(screen.getByRole('button', { name: 'Responder' }));
    await waitFor(() => expect(controle.mutacoes).toHaveLength(1));
    expect(controle.mutacoes[0]).toMatchObject({ caminho: '/api/sessoes/ses_0001/respostas',
      corpo: { simbolo: 'teste_caneca_positivo', valor: true } });
  });

  it('abre o parecer quando a API encerra a sessão sem pausa', async () => {
    simular({ ...segunda, fase: 'encerrada', proxima: null });
    montar();
    expect(await screen.findByText('Destino: /parecer/ses_0001')).toBeInTheDocument();
  });

  it('permite voltar e corrigir uma tela por PUT sem reenviar resposta nova', async () => {
    const controle = simular(primeira);
    montar();
    await userEvent.type(await screen.findByRole('textbox'), '12');
    await userEvent.click(screen.getByRole('button', { name: 'Responder' }));
    await userEvent.click(await screen.findByRole('button', { name: 'Voltar' }));
    const campo = await screen.findByRole('textbox');
    expect(campo).toHaveValue('12');
    await userEvent.clear(campo);
    await userEvent.type(campo, '13');
    await userEvent.click(screen.getByRole('button', { name: 'Responder' }));
    await waitFor(() => expect(controle.mutacoes).toHaveLength(2));
    expect(controle.mutacoes[1]).toEqual({ caminho: '/api/sessoes/ses_0001/triagem/dias_em_lactacao',
      metodo: 'PUT', corpo: { valores: { dias_em_lactacao: '13' } } });
  });
  it('corrige pergunta dinâmica com o símbolo só na rota, conforme o contrato', async () => {
    const controle = simular(perguntaDinamica);
    montar();
    await userEvent.click(await screen.findByRole('radio', { name: 'Sim' }));
    await userEvent.click(screen.getByRole('button', { name: 'Responder' }));
    await userEvent.click(await screen.findByRole('button', { name: 'Voltar' }));
    await userEvent.click(await screen.findByRole('radio', { name: 'Não' }));
    await userEvent.click(screen.getByRole('button', { name: 'Responder' }));
    await waitFor(() => expect(controle.mutacoes).toHaveLength(2));
    expect(controle.mutacoes[1]).toEqual({ caminho: '/api/sessoes/ses_0001/respostas/teste_caneca_positivo', metodo: 'PUT', corpo: { valor: false } });
  });
  it('conserva as respostas posteriores no histórico ao corrigir uma resposta antiga', async () => {
    simular(primeira, controle => {
      controle.estado = controle.mutacoes.length === 1 ? segunda : multipla;
      return resposta(controle.estado);
    });
    montar();
    await userEvent.type(await screen.findByRole('textbox'), '12');
    await userEvent.click(screen.getByRole('button', { name: 'Responder' }));
    await userEvent.click((await screen.findAllByRole('radio'))[0]);
    await userEvent.click(screen.getByRole('button', { name: 'Responder' }));
    await screen.findByRole('checkbox', { name: 'Abatida' });
    await userEvent.click(screen.getByRole('button', { name: 'Voltar' }));
    await screen.findByRole('radio', { name: 'Não sei' });
    await userEvent.click(screen.getByRole('button', { name: 'Voltar' }));
    const dias = await screen.findByRole('textbox');
    await userEvent.clear(dias); await userEvent.type(dias, '13');
    await userEvent.click(screen.getByRole('button', { name: 'Responder' }));
    await screen.findByRole('checkbox', { name: 'Abatida' });
    await userEvent.click(screen.getByRole('button', { name: 'Voltar' }));
    expect(await screen.findByRole('heading', { name: 'Como estão as orelhas e as pontas dos membros?' })).toBeInTheDocument();
  });
});

const especialista: EstadoSessao = { ...segunda, modo: 'veterinario', revisao: 2,
  progresso: { ...segunda.progresso, limite_dinamico: 25 } };
async function pedirEspecialista() {
  await userEvent.click(await screen.findByRole('button', { name: 'Mudar para modo especialista' }));
  return screen.findByRole('dialog', { name: 'Mudar para modo especialista?' });
}
describe('troca de modo sem reiniciar a anamnese', () => {
  it.each([false, true])('corrige o fato térmico original e retorna ao especialista (temperatura respondida: %s)', async temperaturaRespondida => {
    const termicaVet: EstadoSessao = { ...especialista, proxima: { tipo: 'tela_triagem', tela_id: 'estado_termico',
      titulo: 'Informe a temperatura retal', selecao: 'unica', permite_nao_sei: true,
      campos: [{ simbolo: 'temperatura_retal', entrada: 'numerico', rotulo: 'Temperatura retal', unidade: '°C', min: 30, max: 45, opcoes: null }] } };
    let termicaFeita = false;
    const controle = simular(segunda, (c, m) => {
      if (m.metodo === 'PATCH') c.estado = (m.corpo as { modo: string }).modo === 'produtor' ? multipla
        : termicaFeita ? { ...multipla, modo: 'veterinario' } : termicaVet;
      else if (m.metodo === 'POST' && c.estado.modo === 'veterinario') { termicaFeita = true; c.estado = { ...multipla, modo: 'veterinario' }; }
      else if (m.metodo === 'PUT' && c.estado.modo === 'veterinario') return resposta({ erro: {
        codigo: termicaFeita ? 'resposta_invalida' : 'nao_respondida', mensagem: 'Símbolo de outro modo.', requisicao_id: 'rq_termica' } }, termicaFeita ? 422 : 409);
      else c.estado = multipla;
      return resposta(c.estado);
    }); montar();
    await userEvent.click(await screen.findByRole('radio', { name: 'Frias' }));
    await userEvent.click(screen.getByRole('button', { name: 'Responder' }));
    const dialogo = await pedirEspecialista();
    await userEvent.click(within(dialogo).getByRole('button', { name: 'Confirmar troca' }));
    if (temperaturaRespondida) {
      await userEvent.type(await screen.findByRole('textbox'), '38.5');
      await userEvent.click(screen.getByRole('button', { name: 'Responder' }));
    }
    await userEvent.click(await screen.findByRole('button', { name: 'Voltar' }));
    if (temperaturaRespondida) await userEvent.click(screen.getByRole('button', { name: 'Voltar' }));
    await userEvent.click(await screen.findByRole('radio', { name: 'Normais' }));
    const anteriores = controle.mutacoes.length;
    await userEvent.click(screen.getByRole('button', { name: 'Responder' }));
    await waitFor(() => expect(controle.mutacoes.slice(anteriores).map(m => m.metodo)).toEqual(['PATCH', 'PUT', 'PATCH']));
    expect(controle.mutacoes[anteriores].corpo).toEqual({ modo: 'produtor' });
    expect(controle.mutacoes[anteriores + 1].corpo).toEqual({ valores: { extremidades: 'normal' } });
    expect(controle.mutacoes[anteriores + 2].corpo).toEqual({ modo: 'veterinario' });
    expect(screen.getByText('Modo especialista', { exact: true })).toBeInTheDocument();
    expect(screen.getByRole('button', { name: 'Voltar' })).toBeEnabled();
  });
  it('descarta só o rascunho do campo que mudou de modo e não envia símbolos de outra tela', async () => {
    const termicaVet: EstadoSessao = { ...especialista, proxima: { tipo: 'tela_triagem', tela_id: 'estado_termico',
      titulo: 'Informe a temperatura retal', selecao: 'unica', permite_nao_sei: true,
      campos: [{ simbolo: 'temperatura_retal', entrada: 'numerico', rotulo: 'Temperatura retal', unidade: '°C', min: 30, max: 45, opcoes: null }] } };
    const controle = simular(termicaVet, c => { c.estado = segunda; return resposta(c.estado); }); montar();
    await userEvent.type(await screen.findByRole('textbox'), '38.5');
    await userEvent.click(screen.getByRole('button', { name: 'Mudar para modo produtor' }));
    await userEvent.click(await screen.findByRole('radio', { name: 'Normais' }));
    await userEvent.click(screen.getByRole('button', { name: 'Responder' }));
    await waitFor(() => expect(controle.mutacoes).toHaveLength(2));
    expect(controle.mutacoes[1].corpo).toEqual({ valores: { extremidades: 'normal' } });
  });
  it('confirma o aviso, faz PATCH e atualiza modo, progresso, foco e anúncio', async () => {
    const controle = simular(segunda, c => { c.estado = especialista; return resposta(c.estado); });
    montar();
    const dialogo = await pedirEspecialista();
    expect(dialogo).toHaveTextContent('No modo especialista as perguntas têm complexidade maior');
    expect(controle.mutacoes).toHaveLength(0);
    await userEvent.click(within(dialogo).getByRole('button', { name: 'Confirmar troca' }));
    expect(await screen.findByText('Modo especialista', { exact: true })).toBeInTheDocument();
    expect(screen.getByText('Pergunta 2 de até 31')).toBeInTheDocument();
    expect(screen.getByText('Modo especialista ativado.')).toHaveAttribute('role', 'status');
    expect(screen.getByRole('heading', { level: 1 })).toHaveFocus();
    expect(controle.mutacoes).toEqual([{ caminho: '/api/sessoes/ses_0001', metodo: 'PATCH', corpo: { modo: 'veterinario' } }]);
  });
  it('cancela a confirmação sem alterar a sessão', async () => {
    const controle = simular(segunda); montar();
    const dialogo = await pedirEspecialista();
    await userEvent.click(within(dialogo).getByRole('button', { name: 'Fechar' }));
    expect(controle.mutacoes).toHaveLength(0);
    expect(screen.getByText('Modo produtor', { exact: true })).toBeInTheDocument();
  });
  it('volta ao produtor diretamente, sem confirmação', async () => {
    const controle = simular(especialista, c => { c.estado = segunda; return resposta(c.estado); }); montar();
    await userEvent.click(await screen.findByRole('button', { name: 'Mudar para modo produtor' }));
    expect(await screen.findByText('Modo produtor ativado.')).toBeInTheDocument();
    expect(screen.queryByRole('dialog')).not.toBeInTheDocument();
    expect(controle.mutacoes[0].corpo).toEqual({ modo: 'produtor' });
  });
  it('bloqueia resposta e duplo clique enquanto o PATCH está em andamento', async () => {
    let concluir!: (valor: Response) => void;
    const controle = simular(especialista, () => new Promise(resolve => { concluir = resolve; })); montar();
    await userEvent.click((await screen.findAllByRole('radio'))[0]);
    await userEvent.dblClick(screen.getByRole('button', { name: 'Mudar para modo produtor' }));
    await userEvent.click(screen.getByRole('button', { name: /Responder/ }));
    expect(controle.mutacoes).toHaveLength(1);
    expect(screen.getByRole('button', { name: /Responder/ })).toBeDisabled();
    await act(async () => concluir(resposta(segunda)));
  });
  it('não permite trocar de modo durante o envio de uma resposta', async () => {
    let concluir!: (valor: Response) => void;
    const controle = simular(primeira, () => new Promise(resolve => { concluir = resolve; })); montar();
    await userEvent.type(await screen.findByRole('textbox'), '12');
    await userEvent.click(screen.getByRole('button', { name: 'Responder' }));
    const mudar = screen.getByRole('button', { name: 'Mudar para modo especialista' });
    expect(mudar).toBeDisabled(); await userEvent.click(mudar);
    expect(controle.mutacoes).toHaveLength(1); expect(screen.queryByRole('dialog')).not.toBeInTheDocument();
    await act(async () => concluir(resposta(segunda)));
  });
  it('relê a sessão no 409 sem repetir o PATCH', async () => {
    const controle = simular(especialista, c => {
      c.estado = segunda;
      return resposta({ erro: { codigo: 'conflito', mensagem: 'Conflito de revisão.', requisicao_id: 'rq_modo' } }, 409);
    }); montar();
    await userEvent.click(await screen.findByRole('button', { name: 'Mudar para modo produtor' }));
    expect(await screen.findByText('Modo produtor', { exact: true })).toBeInTheDocument();
    expect(controle.mutacoes).toHaveLength(1);
    expect(screen.queryByText('Conflito de revisão.')).not.toBeInTheDocument();
  });
  it.each([404, 422, 500])('mantém o modo e informa falha recuperável no erro %s', async status => {
    simular(especialista, () => resposta({ erro: { codigo: 'erro', mensagem: 'Detalhe do servidor', requisicao_id: 'rq_erro' } }, status)); montar();
    await userEvent.click(await screen.findByRole('button', { name: 'Mudar para modo produtor' }));
    expect(await screen.findByRole('alert')).toHaveTextContent('Não consegui trocar o modo. Tente novamente.');
    expect(screen.getByText('Modo especialista', { exact: true })).toBeInTheDocument();
    expect(screen.getByRole('button', { name: 'Mudar para modo produtor' })).toBeEnabled();
  });
  it('conserva o histórico e corrige por PUT a resposta dada antes da troca, sem reenviá-la', async () => {
    const controle = simular(primeira, (c, m) => {
      c.estado = m.metodo === 'POST' ? segunda : especialista;
      return resposta(c.estado);
    }); montar();
    await userEvent.type(await screen.findByRole('textbox'), '12');
    await userEvent.click(screen.getByRole('button', { name: 'Responder' }));
    const dialogo = await pedirEspecialista();
    await userEvent.click(within(dialogo).getByRole('button', { name: 'Confirmar troca' }));
    await screen.findByText('Modo especialista', { exact: true });
    expect(controle.mutacoes.map(m => m.metodo)).toEqual(['POST', 'PATCH']);
    await userEvent.click(screen.getByRole('button', { name: 'Voltar' }));
    const campo = await screen.findByRole('textbox'); expect(campo).toHaveValue('12');
    await userEvent.clear(campo); await userEvent.type(campo, '13');
    await userEvent.click(screen.getByRole('button', { name: 'Responder' }));
    await waitFor(() => expect(controle.mutacoes).toHaveLength(3));
    expect(controle.mutacoes[2]).toMatchObject({ metodo: 'PUT', corpo: { valores: { dias_em_lactacao: '13' } } });
    expect(screen.getByText('Modo especialista', { exact: true })).toBeInTheDocument();
  });
  it('oferece a troca dentro da pausa e remove o alerta quando o PATCH retorna sem pausa', async () => {
    const controle = simular(estadoPausado, c => { c.estado = especialista; return resposta(c.estado); }); montar();
    const alerta = await screen.findByRole('alertdialog');
    await userEvent.click(within(alerta).getByRole('button', { name: 'Mudar para modo especialista' }));
    const confirmacao = await screen.findByRole('dialog', { name: 'Mudar para modo especialista?' });
    expect(screen.queryByRole('alertdialog')).not.toBeInTheDocument();
    await userEvent.click(within(confirmacao).getByRole('button', { name: 'Confirmar troca' }));
    await screen.findByText('Modo especialista', { exact: true });
    expect(screen.queryByRole('alertdialog')).not.toBeInTheDocument();
    expect(controle.mutacoes).toHaveLength(1);
  });
  it('vai à análise da pergunta atual sem encerrar a verificação (ida e volta)', async () => {
    const controle = simular(perguntaDinamica);
    montar();
    await userEvent.click(await screen.findByRole('link', { name: 'Ver análise agora' }));
    expect(await screen.findByText('Destino: /parecer/ses_0001')).toBeInTheDocument();
    expect(controle.mutacoes).toEqual([]);  // nada é gravado: a sessão segue aberta na mesma pergunta
  });
  it('no modo especialista conta as perguntas sem prometer um total', async () => {
    simular({ ...perguntaDinamica, modo: 'veterinario', progresso: { ...perguntaDinamica.progresso, limite_dinamico: null } });
    montar();
    expect(await screen.findByText(/^Pergunta \d+$/)).toBeInTheDocument();
    expect(screen.queryByText(/de até/)).toBeNull();
  });
});
