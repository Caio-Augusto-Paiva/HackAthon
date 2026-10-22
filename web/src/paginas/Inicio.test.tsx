import { render, screen } from '@testing-library/react';
import userEvent from '@testing-library/user-event';
import { MemoryRouter, Route, Routes, useLocation } from 'react-router-dom';
import { describe, expect, it, vi } from 'vitest';
import exemploSessao from '../../../contratos/exemplos/criar_sessao.json';
import { Inicio } from './Inicio';

function Destino() { return <p>Destino: {useLocation().pathname}</p>; }
function montar() {
  render(<MemoryRouter><Routes><Route path="/" element={<Inicio />} />
    <Route path="/anamnese/:sessaoId" element={<Destino />} /></Routes></MemoryRouter>);
}
function simularCriacao() {
  const chamadas: { caminho: string; corpo: unknown }[] = [];
  vi.stubGlobal('fetch', vi.fn(async (entrada: string, opcoes: RequestInit) => {
    chamadas.push({ caminho: entrada, corpo: JSON.parse(String(opcoes.body)) as unknown });
    const dados = entrada === '/api/animais' ? { id: 'an_novo' } : exemploSessao.resposta;
    return new Response(JSON.stringify(dados), { status: 201 });
  }));
  return chamadas;
}

describe('início da verificação', () => {
  it('cria animal fictício e sessão no modo produtor e abre a anamnese', async () => {
    const chamadas = simularCriacao();
    montar();
    await userEvent.click(screen.getByRole('button', { name: 'Iniciar verificação' }));
    expect(await screen.findByText('Destino: /anamnese/ses_0001')).toBeInTheDocument();
    expect(chamadas[0]).toMatchObject({ caminho: '/api/animais', corpo: { nome: 'Animal da verificação', ficha: {} } });
    expect(chamadas[1]).toEqual({ caminho: '/api/sessoes', corpo: { animal_id: 'an_novo', modo: 'produtor' } });
  });

  it('envia veterinario ao iniciar como especialista e associa o aviso ao botão', async () => {
    const chamadas = simularCriacao();
    montar();
    const botao = screen.getByRole('button', { name: 'Iniciar verificação como especialista' });
    expect(botao).toHaveAccessibleDescription(/No modo especialista as perguntas têm complexidade maior/);
    await userEvent.click(botao);
    await screen.findByText('Destino: /anamnese/ses_0001');
    expect(chamadas[1].corpo).toMatchObject({ modo: 'veterinario' });
  });

  it('explica base ausente e permite tentar novamente', async () => {
    vi.stubGlobal('fetch', vi.fn().mockResolvedValue(new Response(JSON.stringify({ erro: {
      codigo: 'conflito', mensagem: 'Nenhuma base ativa.', requisicao_id: 'rq_base',
    } }), { status: 409 })));
    montar();
    await userEvent.click(screen.getByRole('button', { name: 'Iniciar verificação' }));
    expect(await screen.findByRole('alert')).toHaveTextContent('Nenhuma base ativa. Peça para ativar uma versão.');
    simularCriacao();
    await userEvent.click(screen.getByRole('button', { name: 'Tentar de novo' }));
    expect(await screen.findByText('Destino: /anamnese/ses_0001')).toBeInTheDocument();
  });

  it('mostra erro amigável quando a API está fora do ar', async () => {
    vi.stubGlobal('fetch', vi.fn().mockRejectedValue(new TypeError('Failed to fetch')));
    montar();
    await userEvent.click(screen.getByRole('button', { name: 'Iniciar verificação' }));
    expect(await screen.findByRole('alert')).toHaveTextContent('Não consegui falar com o sistema. Ele está rodando?');
    expect(screen.getByRole('button', { name: 'Tentar de novo' })).toBeEnabled();
  });
});
