import { expect, test } from '@playwright/test';
import { iniciar } from './apoio';

test('dias preserva 12,5, mostra 422 e só avança ao corrigir para 12', async ({ page }) => {
  await page.goto('/');
  await page.screenshot({ animations: 'disabled', path: 'test-results/capturas/01-inicio.png', fullPage: true });
  await iniciar(page);
  const campo = page.getByRole('textbox');
  await campo.fill('12,5');
  const rejeitada = page.waitForResponse(r => r.url().includes('/triagem/') && r.request().method() === 'POST');
  await page.getByRole('button', { name: 'Responder', exact: true }).click();
  const resposta = await rejeitada;
  expect(resposta.status()).toBe(422);
  expect(resposta.request().postDataJSON()).toEqual({ valores: { dias_em_lactacao: '12,5' } });
  await expect(campo).toHaveAttribute('aria-invalid', 'true');
  await expect(campo).toHaveValue('12,5');
  await page.screenshot({ animations: 'disabled', path: 'test-results/capturas/02b-erro.png', fullPage: true });
  await campo.fill('12');
  await page.getByRole('button', { name: 'Responder', exact: true }).click();
  await expect(page.getByText('Pergunta 2 de até 18')).toBeVisible();
});
