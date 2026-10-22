import { describe, expect, it, vi } from 'vitest';
import { chamar, ErroApi } from './cliente';

describe('cliente HTTP', () => {
  it('preserva o código, a mensagem e o identificador de uma resposta de erro', async () => {
    vi.stubGlobal('fetch', vi.fn().mockResolvedValue(new Response(JSON.stringify({ erro: {
      codigo: 'resposta_invalida', mensagem: 'Use só números inteiros.',
      requisicao_id: 'rq_teste', detalhes: null,
    } }), { status: 422 })));
    await expect(chamar('POST', '/sessoes/ses_1/respostas', { valor: '12,5' })).rejects.toMatchObject({
      status: 422, codigo: 'resposta_invalida', requisicaoId: 'rq_teste',
      message: 'Use só números inteiros.', detalhes: [],
    });
  });

  it('transforma falha de rede em erro recuperável sem_conexao', async () => {
    vi.stubGlobal('fetch', vi.fn().mockRejectedValue(new TypeError('Failed to fetch')));
    const erro = await chamar('GET', '/saude').catch((e: unknown) => e);
    expect(erro).toBeInstanceOf(ErroApi);
    expect(erro).toMatchObject({ status: 0, codigo: 'sem_conexao' });
  });

  it('devolve o JSON da resposta e consulta o prefixo local /api', async () => {
    const fetch = vi.fn().mockResolvedValue(new Response(JSON.stringify({ status: 'ok' })));
    vi.stubGlobal('fetch', fetch);
    const resultado = await chamar<{ status: string }>('GET', '/saude');
    expect(resultado).toEqual({ status: 'ok' });
    expect(fetch.mock.calls[0][0]).toBe('/api/saude');
  });
});
