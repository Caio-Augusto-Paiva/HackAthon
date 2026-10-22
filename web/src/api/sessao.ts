import type { components, operations } from './tipos.gerado';
import { chamar } from './cliente';

export type EstadoSessao = components['schemas']['EstadoSessao'];
export type Modo = EstadoSessao['modo'];
export type Tela = NonNullable<EstadoSessao['proxima']>;
export type Parecer = components['schemas']['Parecer'];
export type Porque = components['schemas']['PorQue'];
export const caminhoSessao = (id: string) => `/sessoes/${encodeURIComponent(id)}`;
export const obterSessao = (id: string) => chamar<EstadoSessao>('GET', caminhoSessao(id));
export const obterParecer = (id: string) => chamar<Parecer>('GET', `${caminhoSessao(id)}/parecer`);
export const obterComo = (id: string, simbolo: string) => chamar<components['schemas']['Como']>('GET', `${caminhoSessao(id)}/como/${encodeURIComponent(simbolo)}`);
export const obterPorque = (id: string, simbolo: string) => chamar<Porque>('GET', `${caminhoSessao(id)}/porque/${encodeURIComponent(simbolo)}`);
export const agirBandeira = (id: string, acao: components['schemas']['AcaoBandeira']['acao']) =>
  chamar<EstadoSessao>('POST', `${caminhoSessao(id)}/acoes/bandeira`, { acao });

export function responder(id: string, tela: Tela, corpo: unknown, corrigir = false) {
  const sufixo = tela.tipo === 'tela_triagem' ? `/triagem/${encodeURIComponent(tela.tela_id)}`
    : `/respostas${corrigir ? `/${encodeURIComponent(tela.simbolo)}` : ''}`;
  return chamar<EstadoSessao>(corrigir ? 'PUT' : 'POST', `${caminhoSessao(id)}${sufixo}`, corpo);
}
type AnimalCriado = operations['criar_animal']['responses'][201]['content']['application/json'];

/** Cria um animal fictício anônimo e inicia uma consulta na base ativa. */
export async function iniciarVerificacao(modo: Modo): Promise<EstadoSessao> {
  const aleatorio = crypto.getRandomValues(new Uint32Array(1))[0].toString(36).slice(0, 4).padStart(4, '0');
  const animal = await chamar<AnimalCriado>('POST', '/animais', {
    brinco: `ANON-${Date.now().toString(36)}${aleatorio}`,
    nome: 'Animal da verificação', ficha: {},
  });
  return chamar<EstadoSessao>('POST', '/sessoes', { animal_id: animal.id, modo });
}
