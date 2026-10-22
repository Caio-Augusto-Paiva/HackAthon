import { expect, test, type Page } from '@playwright/test';
import AxeBuilder from '@axe-core/playwright';
import { caso, enviar, iniciar } from './apoio';

async function auditar(page: Page, nome: string, largura: number) {
  await page.evaluate(() => document.fonts.ready);
  const resultado = await new AxeBuilder({ page }).withTags(['wcag2a', 'wcag2aa', 'wcag21aa']).analyze();
  expect(resultado.violations, `${nome}: ${JSON.stringify(resultado.violations.map(v => ({ id: v.id, alvos: v.nodes.map(n => n.target) })))}`).toEqual([]);
  expect(await page.evaluate(() => document.documentElement.scrollWidth <= innerWidth), `${nome}: rolagem horizontal`).toBe(true);
  for (const barra of await page.getByRole('meter').all()) expect((await barra.boundingBox())?.height, `${nome}: barra visível`).toBeGreaterThanOrEqual(10);
  await page.screenshot({ animations: 'disabled', path: `test-results/qualidade/${largura}-${nome}.png`, fullPage: true });
}

for (const largura of [375, 768, 1024, 1440]) test(`seis telas acessíveis, locais e sem overflow em ${largura}px`, async ({ page }) => {
  await page.setViewportSize({ width: largura, height: 900 });
  const externas: string[] = [];
  page.on('request', r => { if (!/^http:\/\/(127\.0\.0\.1|localhost):8000\//.test(r.url())) externas.push(r.url()); });
  await page.goto('/'); await auditar(page, '01-inicio', largura);
  let estado = await iniciar(page); await auditar(page, '02-pergunta', largura);
  const dados = caso('C-HIP-01');
  estado = await enviar(page, estado, dados);
  await expect(page.getByRole('meter')).toHaveCount(4);
  await auditar(page, '03-lateral', largura);
  estado = await enviar(page, estado, dados);
  await expect(page.getByRole('checkbox').first()).toBeVisible();
  await auditar(page, '04-multipla', largura);
  estado = await enviar(page, estado, dados);
  await expect(page.getByRole('alertdialog')).toBeVisible();
  await auditar(page, '05-alerta', largura);
  await page.keyboard.press('Escape'); await expect(page.getByRole('alertdialog')).toBeVisible();
  await page.getByRole('button', { name: 'Ver parecer', exact: true }).click();
  await expect(page.getByRole('table')).toBeVisible(); await auditar(page, '06-parecer', largura);
  await page.getByRole('button', { name: 'Como cheguei aqui?' }).click();
  await expect(page.getByRole('dialog')).toBeVisible();
  await expect(page.getByRole('dialog').getByText('R-HIP-01', { exact: true })).toBeVisible();
  expect(externas).toEqual([]);
});
