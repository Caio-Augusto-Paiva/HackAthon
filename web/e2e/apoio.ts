import { expect, type Page } from '@playwright/test';
import casosJson from '../../base/casos/casos.json' with { type: 'json' };
import type { EstadoSessao, Modo } from '../src/api/sessao';

type Valor = string | number | boolean | string[] | null;
type Caso = { id: string; ficha: Record<string, Valor>; triagem: Record<string, Valor>; respostas: Record<string, Valor>; esperado: { top1?: string; urgencia?: string } };
export const casos = casosJson as unknown as Caso[];
export function caso(id: string) {
  const encontrado = casos.find(c => c.id === id);
  if (!encontrado) throw new Error(`Caso não encontrado: ${id}`);
  return encontrado;
}
export async function iniciar(page: Page, modo: Modo = 'produtor') {
  await page.goto('/');
  const criada = page.waitForResponse(r => r.url().endsWith('/api/sessoes') && r.request().method() === 'POST');
  await page.getByRole('button', { name: modo === 'produtor' ? 'Iniciar verificação' : 'Iniciar verificação como especialista', exact: true }).click();
  const estado = await (await criada).json() as EstadoSessao;
  await expect(page.getByRole('heading', { level: 1 })).toBeVisible();
  return estado;
}
export async function enviar(page: Page, estado: EstadoSessao, dados: Caso) {
  const tela = estado.proxima;
  if (!tela) throw new Error('O caso não tem uma pergunta aberta.');
  if (tela.tipo === 'tela_triagem') {
    const valor = dados.triagem[tela.tela_id] ?? dados.ficha[tela.tela_id];
    if (valor === undefined || valor === null) await page.getByRole(tela.selecao === 'multipla' ? 'checkbox' : 'radio', { name: 'Não sei', exact: true }).check();
    else if (tela.selecao === 'multipla') {
      const marcadas = Array.isArray(valor) ? tela.campos.filter(c => valor.includes(c.simbolo)) : [];
      if (!marcadas.length) await page.getByRole('checkbox', { name: 'Nenhuma alteração' }).check();
      for (const c of marcadas) await page.getByRole('checkbox', { name: c.rotulo ?? c.simbolo, exact: true }).check();
    } else {
      const c = tela.campos[0];
      if (c.entrada === 'numerico') await page.getByRole('textbox').fill(String(valor));
      else await page.getByRole('radio', { name: c.entrada === 'booleano' ? valor ? 'Sim' : 'Não'
        : c.opcoes!.find(o => o.valor === valor)!.rotulo, exact: true }).check();
    }
  } else {
    const valor = dados.respostas[tela.simbolo] ?? dados.ficha[tela.simbolo];
    if (valor === undefined || valor === null) await page.getByRole('radio', { name: 'Não sei', exact: true }).check();
    else if (tela.entrada === 'numerico') await page.getByRole('textbox').fill(String(valor));
    else await page.getByRole('radio', { name: tela.entrada === 'booleano' ? valor ? 'Sim' : 'Não'
      : tela.opcoes!.find(o => o.valor === valor)!.rotulo, exact: true }).check();
  }
  const recebida = page.waitForResponse(r => r.request().method() === 'POST' && /\/(triagem\/[^/]+|respostas)$/.test(r.url()));
  await page.getByRole('button', { name: 'Responder', exact: true }).click();
  const resposta = await recebida;
  expect(resposta.status()).toBe(200);
  return resposta.json() as Promise<EstadoSessao>;
}
