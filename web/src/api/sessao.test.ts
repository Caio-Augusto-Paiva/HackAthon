import { expect, it, vi } from 'vitest';
import { trocarModo } from './sessao';
import { segunda, resposta } from '../teste/cenarios';

it('troca o modo por PATCH na mesma sessão, com id codificado e corpo da API', async () => {
  const atualizado = { ...segunda, modo: 'veterinario' };
  const fetch = vi.fn().mockResolvedValue(resposta(atualizado));
  vi.stubGlobal('fetch', fetch);
  await expect(trocarModo('sessao/1', 'veterinario')).resolves.toEqual(atualizado);
  expect(fetch).toHaveBeenCalledWith('/api/sessoes/sessao%2F1', expect.objectContaining({
    method: 'PATCH', body: JSON.stringify({ modo: 'veterinario' }),
  }));
});
