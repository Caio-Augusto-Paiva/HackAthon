import { expect, it, vi } from 'vitest';
import { corrigirTelaEmOutroModo } from './corrigirTelaEmOutroModo';
import { segunda, resposta } from '../teste/cenarios';
import type { Tela } from '../api/sessao';

const tela = segunda.proxima as Tela;
const vet = { ...segunda, modo: 'veterinario' };
const falha = (status: number) => resposta({ erro: { codigo: status === 409 ? 'conflito' : 'resposta_invalida', mensagem: 'Falha da operação', requisicao_id: 'rq_correcao' } }, status);
it('restaura o modo escolhido mesmo se o PUT falhar, sem declarar resposta gravada', async () => {
  const fetch = vi.fn().mockResolvedValueOnce(resposta(segunda)).mockResolvedValueOnce(falha(422)).mockResolvedValueOnce(resposta(vet));
  vi.stubGlobal('fetch', fetch);
  const resultado = await corrigirTelaEmOutroModo('s', tela, {}, 'produtor', 'veterinario');
  expect(resultado.gravada).toBe(false); expect(resultado.estado?.modo).toBe('veterinario');
  expect(resultado.erro).toMatchObject({ status: 422 });
  expect(fetch.mock.calls.map(c => c[1].method)).toEqual(['PATCH', 'PUT', 'PATCH']);
});
it('informa o modo real e a gravação confirmada se a restauração falhar', async () => {
  const fetch = vi.fn().mockResolvedValueOnce(resposta(segunda)).mockResolvedValueOnce(resposta(segunda))
    .mockResolvedValueOnce(falha(500)).mockResolvedValueOnce(resposta(segunda));
  vi.stubGlobal('fetch', fetch);
  const resultado = await corrigirTelaEmOutroModo('s', tela, {}, 'produtor', 'veterinario');
  expect(resultado.gravada).toBe(true); expect(resultado.estado?.modo).toBe('produtor');
  expect(resultado.erro?.message).toContain('Não consegui retornar ao modo especialista');
  expect(fetch.mock.calls.map(c => c[1].method)).toEqual(['PATCH', 'PUT', 'PATCH', 'GET']);
});
it('relê um conflito na primeira troca sem enviar PUT nem repetir PATCH', async () => {
  const fetch = vi.fn().mockResolvedValueOnce(falha(409)).mockResolvedValueOnce(resposta(vet));
  vi.stubGlobal('fetch', fetch);
  const resultado = await corrigirTelaEmOutroModo('s', tela, {}, 'produtor', 'veterinario');
  expect(resultado.gravada).toBe(false); expect(resultado.estado?.modo).toBe('veterinario');
  expect(resultado.erro).toMatchObject({ status: 409 });
  expect(fetch.mock.calls.map(c => c[1].method)).toEqual(['PATCH', 'GET']);
});
it('reconcilia conflito na restauração pelo GET, sem repetir a correção', async () => {
  const fetch = vi.fn().mockResolvedValueOnce(resposta(segunda)).mockResolvedValueOnce(resposta(segunda))
    .mockResolvedValueOnce(falha(409)).mockResolvedValueOnce(resposta(vet));
  vi.stubGlobal('fetch', fetch);
  const resultado = await corrigirTelaEmOutroModo('s', tela, {}, 'produtor', 'veterinario');
  expect(resultado.gravada).toBe(true); expect(resultado.estado?.modo).toBe('veterinario'); expect(resultado.erro).toBeUndefined();
  expect(fetch.mock.calls.map(c => c[1].method)).toEqual(['PATCH', 'PUT', 'PATCH', 'GET']);
});
