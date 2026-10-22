import { render, screen, waitFor, within } from '@testing-library/react';
import userEvent from '@testing-library/user-event';
import { MemoryRouter, Route, Routes, useLocation } from 'react-router-dom';
import { describe, expect, it, vi } from 'vitest';
import { estadoPausado, segunda, resposta, exemploParecer } from '../teste/cenarios';
import { Anamnese } from '../paginas/Anamnese';

function montar(acoes = estadoPausado.alerta!.acoes) {
  const fetch = vi.fn(async (caminho: string, opcoes: RequestInit) => caminho.endsWith('/parecer') ? resposta(exemploParecer) : resposta(opcoes.method === 'POST'
    ? JSON.parse(String(opcoes.body)).acao === 'continuar' ? segunda : { ...estadoPausado, fase: 'encerrada', alerta: { ...estadoPausado.alerta, pausa: false } }
    : { ...estadoPausado, alerta: { ...estadoPausado.alerta, acoes } }));
  vi.stubGlobal('fetch', fetch);
  function Destino() { return <p>{useLocation().pathname}</p>; }
  render(<MemoryRouter initialEntries={['/anamnese/ses_0001']}><Routes><Route path="/anamnese/:sessaoId" element={<Anamnese />} />
    <Route path="/parecer/:sessaoId" element={<Destino />} /></Routes></MemoryRouter>);
  return fetch;
}

describe('interrupção por bandeira vermelha', () => {
  it('protege o foco, ignora Esc e o clique no fundo', async () => {
    montar();
    const dialogo = await screen.findByRole('alertdialog');
    const primeiro = within(dialogo).getByRole('button', { name: 'Ver parecer' });
    await waitFor(() => expect(primeiro).toHaveFocus());
    await userEvent.tab({ shift: true });
    expect(within(dialogo).getByRole('button', { name: 'Mudar para modo especialista' })).toHaveFocus();
    await userEvent.tab(); expect(primeiro).toHaveFocus();
    await userEvent.keyboard('{Escape}');
    await userEvent.click(dialogo.parentElement!);
    expect(dialogo).toBeInTheDocument();
    expect(dialogo).toHaveTextContent(estadoPausado.alerta!.texto);
  });
  it('envia ver_parecer e abre o parecer', async () => {
    const fetch = montar();
    await userEvent.click(await screen.findByRole('button', { name: 'Ver parecer' }));
    expect(await screen.findByText('/parecer/ses_0001')).toBeInTheDocument();
    expect(fetch).toHaveBeenCalledWith('/api/sessoes/ses_0001/acoes/bandeira', expect.objectContaining({ method: 'POST', body: JSON.stringify({ acao: 'ver_parecer' }) }));
  });
  it('envia continuar e retorna à pergunta da API', async () => {
    montar();
    await userEvent.click(await screen.findByRole('button', { name: 'Continuar respondendo' }));
    expect(await screen.findByRole('heading', { name: 'Como estão as orelhas e as pontas dos membros?' })).toBeInTheDocument();
    await waitFor(() => expect(screen.queryByRole('alertdialog')).not.toBeInTheDocument());
  });
  it('mostra apenas as ações autorizadas', async () => {
    montar(['ver_parecer']);
    await screen.findByRole('alertdialog');
    expect(screen.queryByRole('button', { name: 'Continuar respondendo' })).not.toBeInTheDocument();
  });
});
