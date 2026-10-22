import { act, render, screen, waitFor, within } from '@testing-library/react';
import userEvent from '@testing-library/user-event';
import { MemoryRouter, Route, Routes, useLocation } from 'react-router-dom';
import { describe, expect, it, vi } from 'vitest';
import type { EstadoSessao } from '../api/sessao';
import { primeira, segunda, multipla, perguntaDinamica, exemploParecer, exemploPorque, resposta } from '../teste/cenarios';
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

  it('abre o porquê com o motivo, as doenças e as regras retornadas', async () => {
    simular(primeira);
    montar();
    await userEvent.click(await screen.findByRole('button', { name: 'Por que estou perguntando isso?' }));
    const dialogo = await screen.findByRole('dialog');
    expect(await within(dialogo).findByText(exemploPorque.motivo)).toBeInTheDocument();
    expect(dialogo).toHaveTextContent('Mastite clínica');
    expect(dialogo).toHaveTextContent('R-MAS-03');
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
});
