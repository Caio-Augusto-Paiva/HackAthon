import type { components } from './tipos.gerado';

type Detalhe = components['schemas']['Detalhe'];
type ErroResposta = components['schemas']['ErroResposta'];

export class ErroApi extends Error {
  constructor(
    public readonly status: number,
    public readonly codigo: string,
    mensagem: string,
    public readonly requisicaoId = '',
    public readonly detalhes: Detalhe[] = [],
  ) {
    super(mensagem);
    this.name = 'ErroApi';
  }
}

function temErroEstruturado(dados: unknown): dados is ErroResposta {
  if (typeof dados !== 'object' || dados === null || !('erro' in dados)) return false;
  const erro = dados.erro;
  return typeof erro === 'object' && erro !== null
    && 'codigo' in erro && typeof erro.codigo === 'string'
    && 'mensagem' in erro && typeof erro.mensagem === 'string'
    && 'requisicao_id' in erro && typeof erro.requisicao_id === 'string';
}

/** Executa uma operação local e preserva o erro público retornado pela API. */
export async function chamar<T>(
  metodo: 'GET' | 'POST' | 'PUT' | 'PATCH', caminho: string, corpo?: unknown,
): Promise<T> {
  let resposta: Response;
  try {
    resposta = await fetch(`/api${caminho}`, {
      method: metodo,
      headers: { Accept: 'application/json', ...(corpo === undefined ? {} : { 'Content-Type': 'application/json' }) },
      body: corpo === undefined ? undefined : JSON.stringify(corpo),
    });
  } catch {
    throw new ErroApi(0, 'sem_conexao', 'Não consegui falar com o sistema. Ele está rodando?');
  }
  let dados: unknown;
  try {
    dados = await resposta.json();
  } catch {
    throw new ErroApi(resposta.status, 'resposta_inesperada',
      'O sistema devolveu uma resposta inesperada. Tente de novo.', resposta.headers.get('X-Requisicao-Id') ?? '');
  }
  if (!resposta.ok) {
    if (temErroEstruturado(dados)) {
      const erro = dados.erro;
      throw new ErroApi(resposta.status, erro.codigo, erro.mensagem, erro.requisicao_id,
        Array.isArray(erro.detalhes) ? erro.detalhes : []);
    }
    throw new ErroApi(resposta.status, 'erro_interno', 'Não foi possível concluir a operação. Tente de novo.');
  }
  return dados as T;
}
