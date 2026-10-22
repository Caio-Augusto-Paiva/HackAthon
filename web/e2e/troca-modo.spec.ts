import { expect, test } from '@playwright/test';
import AxeBuilder from '@axe-core/playwright';
import { caso, enviar, iniciar } from './apoio';
import type { EstadoSessao } from '../src/api/sessao';

test('troca produtor por especialista, corrige resposta anterior e produz um único parecer com os sinais dos dois modos', async ({ page, request }) => {
  const dados = caso('C-MAS-01');
  let estado = await iniciar(page);
  for (let n = 0; n < 5; n++) estado = await enviar(page, estado, dados);
  const sessaoId = estado.sessao_id;
  await page.getByRole('button', { name: 'Mudar para modo especialista' }).click();
  const modal = page.getByRole('dialog', { name: 'Mudar para modo especialista?' });
  await expect(modal).toBeVisible();
  expect((await new AxeBuilder({ page }).withTags(['wcag2a', 'wcag2aa', 'wcag21aa']).analyze()).violations).toEqual([]);
  const alterada = page.waitForResponse(r => r.request().method() === 'PATCH');
  await modal.getByRole('button', { name: 'Confirmar troca' }).click();
  const resposta = await alterada;
  expect(resposta.request().postDataJSON()).toEqual({ modo: 'veterinario' });
  estado = await resposta.json() as EstadoSessao;
  expect(estado.sessao_id).toBe(sessaoId);
  expect(estado.proxima?.tipo === 'tela_triagem' && estado.proxima.campos[0].simbolo).toBe('temperatura_retal');
  await expect(page.getByText('Modo especialista ativado.')).toBeAttached();
  await expect(page.getByRole('heading', { level: 1 })).toBeFocused();
  // As cinco respostas continuam corrigíveis: volte até dias sem recriar a sessão.
  for (let n = 0; n < 5; n++) await page.getByRole('button', { name: 'Voltar', exact: true }).click();
  await page.getByRole('textbox').fill('91');
  const corrigida = page.waitForResponse(r => r.request().method() === 'PUT');
  await page.getByRole('button', { name: 'Responder', exact: true }).click();
  expect((await corrigida).status()).toBe(200);
  // A tela térmica tem símbolos diferentes: o fato do produtor também continua corrigível.
  async function corrigirTermicaAnterior(voltas: number) {
    for (let n = 0; n < voltas; n++) await page.getByRole('button', { name: 'Voltar', exact: true }).click();
    await page.getByRole('radio', { name: 'normal', exact: true }).check();
    const put = page.waitForResponse(r => r.request().method() === 'PUT');
    await page.getByRole('button', { name: 'Responder', exact: true }).click();
    expect((await put).status()).toBe(200);
    await expect(page.getByText('Modo especialista', { exact: true })).toBeVisible();
    await expect(page.getByRole('button', { name: 'Mudar para modo produtor' })).toBeEnabled();
  }
  await corrigirTermicaAnterior(4);
  const dadosVet = { ...dados, triagem: { ...dados.triagem, estado_termico: 38.5 }, respostas: { cmt_reagente: true } };
  estado = await enviar(page, estado, dadosVet);
  await corrigirTermicaAnterior(5);
  for (let n = 0; n < 30 && estado.proxima; n++) estado = await enviar(page, estado, dadosVet);
  await expect(page).toHaveURL(`/parecer/${sessaoId}`);
  const parecer = await (await request.get(`/api/sessoes/${sessaoId}/parecer`)).json();
  expect(parecer.sessao_id).toBe(sessaoId); expect(parecer.modo).toBe('veterinario'); expect(parecer.final).toBe(true);
  expect(parecer.blocos[0].itens[0].doenca).toBe('mastite');
  expect(parecer.blocos[0].itens[0].percentual).toBeGreaterThanOrEqual(75);
  const como = await (await request.get(`/api/sessoes/${sessaoId}/como/mastite`)).json();
  expect(JSON.stringify(como)).toContain('leite_alterado');
  expect(JSON.stringify(como)).toContain('ubere_inflamado');
  expect((await new AxeBuilder({ page }).withTags(['wcag2a', 'wcag2aa', 'wcag21aa']).analyze()).violations).toEqual([]);
  await page.screenshot({ animations: 'disabled', path: 'test-results/troca-modo/parecer-unico.png', fullPage: true });
});

test('troca pela pausa sem perder a bandeira e permite voltar ao produtor', async ({ page, request }) => {
  let estado = await iniciar(page);
  for (let n = 0; n < 3; n++) estado = await enviar(page, estado, caso('C-HIP-01'));
  const alerta = page.getByRole('alertdialog'); await expect(alerta).toBeVisible();
  await alerta.getByRole('button', { name: 'Mudar para modo especialista' }).click();
  await expect(page.getByRole('alertdialog')).toHaveCount(0);
  await page.getByRole('dialog').getByRole('button', { name: 'Confirmar troca' }).click();
  await expect(page.getByRole('textbox')).toBeVisible();
  await expect(page.getByText('Modo especialista', { exact: true })).toBeVisible();
  const parecer = await (await request.get(`/api/sessoes/${estado.sessao_id}/parecer`)).json();
  expect(parecer.urgencia.nivel).toBe('chamar_agora');
  expect(parecer.blocos[0].itens[0].doenca).toBe('hipocalcemia');
  expect((await new AxeBuilder({ page }).withTags(['wcag2a', 'wcag2aa', 'wcag21aa']).analyze()).violations).toEqual([]);
  await page.screenshot({ animations: 'disabled', path: 'test-results/troca-modo/especialista.png', fullPage: true });
  await page.getByRole('button', { name: 'Mudar para modo produtor' }).click();
  await expect(page.getByRole('alertdialog')).toBeVisible();
  await expect(page.getByRole('dialog')).toHaveCount(0);
});

test('parecer parcial troca de modo na mesma sessão e anuncia a chegada à anamnese', async ({ page }) => {
  const estado = await iniciar(page);
  await page.goto(`/parecer/${estado.sessao_id}`);
  await page.getByRole('button', { name: 'Mudar para modo especialista' }).click();
  await page.getByRole('dialog').getByRole('button', { name: 'Confirmar troca' }).click();
  await expect(page).toHaveURL(`/anamnese/${estado.sessao_id}`);
  await expect(page.getByText('Modo especialista ativado.')).toBeAttached();
  await expect(page.getByRole('textbox')).toBeVisible();
  expect((await new AxeBuilder({ page }).withTags(['wcag2a', 'wcag2aa', 'wcag21aa']).analyze()).violations).toEqual([]);
});
