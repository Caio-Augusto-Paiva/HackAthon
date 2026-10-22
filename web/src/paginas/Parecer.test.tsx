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
  it('mostra até quanto a confiança pode chegar quando o potencial supera o percentual', async () => {
    montar();
    const tabela = await screen.findByRole('table', { name: 'Hipóteses e confiança do sistema' });
    const linhas = within(tabela).getAllByRole('row').filter(l => l.querySelector('td'));
    const comPotencial = exemploParecer.blocos.flatMap(b => b.itens).filter(i => i.potencial > i.percentual);
    expect(comPotencial.length).toBeGreaterThan(0);
    expect(within(tabela).getAllByText(/pode chegar a \d+%/)).toHaveLength(comPotencial.length);
    expect(linhas[0]).not.toHaveTextContent('pode chegar a');
    expect(linhas[1]).toHaveTextContent(`pode chegar a ${exemploParecer.blocos[1].itens[0].potencial}%`);
  });
  it('avisa e oferece continuar quando nenhuma doença foi confirmada', async () => {
    const zerado = { ...exemploParecer, final: true, blocos: exemploParecer.blocos.map(b => ({ ...b, itens: b.itens.map(i => ({ ...i, percentual: 0, potencial: 60 })) })) };
    montar(zerado);
    const aviso = await screen.findByText('Nenhuma doença foi confirmada com as respostas dadas. Responda mais perguntas para o sistema calcular as chances.');
    expect(aviso.closest('[role="status"]')).not.toBeNull();
    await userEvent.click(within(aviso.closest('[role="status"]') as HTMLElement).getByRole('link', { name: 'Continuar respondendo' }));
    expect(await screen.findByRole('heading', { name: 'Pergunta retomada' })).toBeInTheDocument();
  });
  it('não mostra o aviso de nada confirmado quando alguma doença tem percentual', async () => {
    montar();
    await screen.findByRole('table', { name: 'Hipóteses e confiança do sistema' });
    expect(screen.queryByText(/Nenhuma doença foi confirmada/)).toBeNull();
  });
  it.each(['chamar_agora', 'observar', 'sem_problema'] as const)('avisa que não substitui o laudo, mesmo com urgência %s', async nivel => {
    montar({ ...exemploParecer, urgencia: { ...exemploParecer.urgencia, nivel } });
    const aviso = await screen.findByRole('note', { name: 'Este parecer não é um laudo' });
    expect(aviso).toHaveTextContent('Esta análise não substitui um laudo médico e é importante procurar um médico-veterinário');
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
    expect(dialogo).toHaveTextContent('Leite alterado');
    expect(within(dialogo).getByText('0% → 70%')).toBeInTheDocument();
    expect(within(dialogo).getByText('70% → 88%')).toBeInTheDocument();
    expect(within(dialogo).getByRole('button', { name: 'Expandir painel' })).toBeInTheDocument();
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
  it('oferece troca no parecer parcial e navega à mesma anamnese após confirmar', async () => {
    const fetch = montar({ ...exemploParecer, final: false });
    fetch.mockImplementation(async (caminho, opcoes) => resposta(opcoes.method === 'PATCH'
      ? { ...segunda, modo: 'veterinario' } : caminho.includes('/como/') ? exemploComo : { ...exemploParecer, final: false }));
    await userEvent.click(await screen.findByRole('button', { name: 'Mudar para modo especialista' }));
    const dialogo = await screen.findByRole('dialog');
    await userEvent.click(within(dialogo).getByRole('button', { name: 'Confirmar troca' }));
    expect(await screen.findByRole('heading', { name: 'Pergunta retomada' })).toBeInTheDocument();
    expect(fetch).toHaveBeenCalledWith('/api/sessoes/ses_0001', expect.objectContaining({ method: 'PATCH', body: JSON.stringify({ modo: 'veterinario' }) }));
  });
  it('mantém o parecer parcial e informa falha sem trocar o modo quando o PATCH falha', async () => {
    const fetch = montar({ ...exemploParecer, final: false, modo: 'veterinario' });
    fetch.mockImplementation(async (_caminho, opcoes) => opcoes.method === 'PATCH'
      ? resposta({ erro: { codigo: 'erro_interno', mensagem: 'Falha técnica', requisicao_id: 'rq_troca' } }, 500)
      : resposta({ ...exemploParecer, final: false, modo: 'veterinario' }));
    await userEvent.click(await screen.findByRole('button', { name: 'Mudar para modo produtor' }));
    expect(await screen.findByRole('alert')).toHaveTextContent('Não consegui trocar o modo. Tente novamente.');
    expect(screen.getByRole('table')).toBeInTheDocument();
    expect(screen.getByRole('button', { name: 'Mudar para modo produtor' })).toBeEnabled();
  });
});
