import { expect, test } from '@playwright/test';
import { caso, enviar, iniciar } from './apoio';

test('C-MAS-02: especialista responde à temperatura retal técnica', async ({ page }) => {
  let estado = await iniciar(page, 'veterinario');
  estado = await enviar(page, estado, caso('C-MAS-02'));
  expect(estado.proxima?.tipo).toBe('tela_triagem');
  if (estado.proxima?.tipo !== 'tela_triagem') throw new Error('Esperava triagem técnica.');
  expect(estado.proxima.campos[0].simbolo).toBe('temperatura_retal');
  await expect(page.getByRole('textbox')).toBeVisible();
  estado = await enviar(page, estado, caso('C-MAS-02'));
  expect(estado.progresso.triagem_respondidas).toBe(2);
});
