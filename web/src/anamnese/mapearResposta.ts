import type { components } from '../api/tipos.gerado';

export type Escolha = { tipo: 'vazia' | 'nenhuma' | 'nao_sei' }
  | { tipo: 'multipla'; simbolos: string[] }
  | { tipo: 'valores'; valores: Record<string, string | boolean> };
export type TelaTriagem = components['schemas']['TelaTriagem'];
export type PerguntaDinamica = components['schemas']['PerguntaDinamica'];
// O OpenAPI marca o valor padrão como obrigatório; o corpo de entrada pode omiti-lo.
type CorpoEntrada<T extends { nao_sei: boolean }> = Omit<T, 'nao_sei'> & Partial<Pick<T, 'nao_sei'>>;

export function paraCorpoTriagem(tela: TelaTriagem, escolha: Escolha): CorpoEntrada<components['schemas']['RespostaTriagem']> {
  if (escolha.tipo === 'nao_sei') return { nao_sei: true };
  if (tela.selecao === 'multipla' && (escolha.tipo === 'multipla' || escolha.tipo === 'nenhuma')) {
    return { valores: Object.fromEntries(tela.campos.map(c => [c.simbolo,
      escolha.tipo === 'multipla' && escolha.simbolos.includes(c.simbolo)])) };
  }
  if (escolha.tipo === 'valores') return { valores: escolha.valores };
  throw new Error('Escolha uma resposta antes de enviar.');
}

export function paraCorpoPergunta(pergunta: PerguntaDinamica, escolha: Escolha): CorpoEntrada<components['schemas']['RespostaPergunta']> {
  if (escolha.tipo === 'nao_sei') return { simbolo: pergunta.simbolo, nao_sei: true };
  if (escolha.tipo === 'valores') return { simbolo: pergunta.simbolo, valor: escolha.valores[pergunta.simbolo] };
  throw new Error('Escolha uma resposta antes de enviar.');
}

export function passoAtual(p: components['schemas']['Progresso']) {
  return p.triagem_respondidas + p.dinamicas_feitas + 1;
}
