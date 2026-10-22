import { render, screen, within } from '@testing-library/react';
import userEvent from '@testing-library/user-event';
import { MemoryRouter, Route, Routes } from 'react-router-dom';
import { describe, expect, it, vi } from 'vitest';
import { exemploComo, exemploParecer, resposta, segunda } from '../teste/cenarios';
import { Parecer } from './Parecer';

function montar(parecer = exemploParecer) {
  const fetch = vi.fn(async (caminho: string, opcoes: RequestInit) => resposta(opcoes.method === 'POST' ? segunda : caminho.includes('/como/') ? exemploComo : parecer));
  vi.stubGlobal('fetch', fetch);
  render(<MemoryRouter initialEntries={['/parecer/ses_0001']}><Routes><Route path="/parecer/:sessaoId" element={<Parecer />} />
    <Route path="/anamnese/:sessaoId" element={<h1>Pergunta retomada</h1>} />
    <Route path="/" element={<h1>Início da verificação</h1>} /></Routes></MemoryRouter>);
  return fetch;
}

describe('parecer do sistema', () => {
  it('apresenta oito doenças ordenadas, nos blocos da API e com gravidade textual', async () => {
    montar();
    const tabela = await screen.findByRole('table', { name: 'Hipóteses e confiança do sistema' });
    const linhas = within(tabela).getAllByRole('row').filter(l => l.querySelector('td'));
    expect(linhas).toHaveLength(8);
    expect(linhas.map(l => within(l).getByRole('meter').getAttribute('aria-valuenow'))).toEqual(['87', '32', '15', '5', '0', '0', '0', '0']);
    for (const bloco of exemploParecer.blocos) expect(tabela).toHaveTextContent(bloco.titulo);
    expect(linhas[0]).toHaveTextContent('Alta'); expect(linhas[1]).toHaveTextContent('Média'); expect(linhas[4]).toHaveTextContent('Baixa');
    expect(screen.getByRole('status')).toHaveTextContent(exemploParecer.urgencia.texto);
  });
  it.each(['chamar_agora', 'observar', 'sem_problema'] as const)('identifica a urgência %s com texto da API', async nivel => {
    montar({ ...exemploParecer, urgencia: { ...exemploParecer.urgencia, nivel, texto: `Orientação ${nivel}` } });
    await screen.findByText(`Orientação ${nivel}`);
    expect(screen.getByRole('status')).toHaveAttribute('data-nivel', nivel);
    expect(screen.getByRole('status')).toHaveTextContent(`Orientação ${nivel}`);
  });
  it('consulta as evidências da primeira doença e mostra regras e fonte', async () => {
    const fetch = montar();
    await userEvent.click(await screen.findByRole('button', { name: 'Como cheguei aqui?' }));
    const dialogo = await screen.findByRole('dialog');
    expect(await within(dialogo).findByText('R-MAS-01')).toBeInTheDocument();
    expect(dialogo).toHaveTextContent('F1');
    expect(dialogo).toHaveTextContent('Suposição a validar');
    expect(dialogo).toHaveTextContent('leite_alterado');
    expect(fetch).toHaveBeenCalledWith('/api/sessoes/ses_0001/como/hipocalcemia', expect.objectContaining({ method: 'GET' }));
  });
  it('avisa que o parecer é parcial e permite nova verificação', async () => {
    montar({ ...exemploParecer, final: false });
    expect(await screen.findByText('Parecer parcial')).toBeInTheDocument();
    await userEvent.click(screen.getByRole('link', { name: 'Nova verificação' }));
    expect(await screen.findByRole('heading', { name: 'Início da verificação' })).toBeInTheDocument();
  });
  it('reabre por continuar o parecer encerrado voluntariamente', async () => {
    montar({ ...exemploParecer, motivo_parada: null });
    const fetch = vi.mocked(globalThis.fetch);
    await userEvent.click(await screen.findByRole('button', { name: 'Continuar respondendo' }));
    expect(await screen.findByRole('heading', { name: 'Pergunta retomada' })).toBeInTheDocument();
    expect(fetch).toHaveBeenCalledWith('/api/sessoes/ses_0001/acoes/bandeira', expect.objectContaining({ method: 'POST', body: JSON.stringify({ acao: 'continuar' }) }));
  });
  it('não promete reabrir uma sessão encerrada por parada automática', async () => {
    montar();
    await screen.findByRole('table');
    expect(screen.queryByRole('button', { name: 'Continuar respondendo' })).not.toBeInTheDocument();
  });
});
