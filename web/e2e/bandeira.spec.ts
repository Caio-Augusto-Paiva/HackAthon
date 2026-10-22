import { expect, test } from '@playwright/test';
import { caso, enviar, iniciar } from './apoio';

test('decúbito interrompe a consulta e permite ver o parecer urgente', async ({ page }) => {
  const dados = { ...caso('C-MAS-01'), triagem: { ...caso('C-MAS-01').triagem, atitude_locomocao: ['decubito'] } };
  let estado = await iniciar(page);
  await page.screenshot({ path: 'test-results/capturas/02-pergunta.png', fullPage: true });
  while (estado.proxima && estado.proxima.tipo === 'tela_triagem' && estado.proxima.tela_id !== 'atitude_locomocao') {
    estado = await enviar(page, estado, dados);
    if (estado.progresso.triagem_respondidas === 1) await page.screenshot({ path: 'test-results/capturas/03-lateral.png', fullPage: true });
  }
  await expect(page.getByRole('checkbox').first()).toBeVisible();
  await page.screenshot({ path: 'test-results/capturas/04-multipla.png', fullPage: true });
  estado = await enviar(page, estado, dados);
  expect(estado.alerta?.pausa).toBe(true);
  await expect(page.getByRole('alertdialog')).toBeVisible();
  await page.screenshot({ path: 'test-results/capturas/05-alerta.png', fullPage: true });
  await page.getByRole('button', { name: 'Ver parecer', exact: true }).click();
  await expect(page).toHaveURL(/\/parecer\//);
  await expect(page.locator('[data-nivel="chamar_agora"]')).toBeVisible();
});
