import { expect, test } from '@playwright/test';
import { caso, enviar, iniciar } from './apoio';

test('C-MAS-01: produtor completa a consulta e vê o parecer da API', async ({ page, request }) => {
  const dados = caso('C-MAS-01');
  let estado = await iniciar(page);
  for (let n = 0; n < 25 && estado.proxima; n++) estado = await enviar(page, estado, dados);
  await expect(page).toHaveURL(/\/parecer\//);
  const parecer = await (await request.get(`/api/sessoes/${estado.sessao_id}/parecer`)).json();
  expect(parecer.blocos[0].itens[0].doenca).toBe(dados.esperado.top1);
  expect(parecer.urgencia.nivel).toBe(dados.esperado.urgencia);
  await expect(page.getByRole('table')).toBeVisible();
  await expect(page.getByRole('meter')).toHaveCount(8);
  await page.screenshot({ animations: 'disabled', path: 'test-results/capturas/06-parecer.png', fullPage: true });
});
