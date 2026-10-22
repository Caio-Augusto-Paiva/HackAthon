import type { components, operations } from './tipos.gerado';
import { chamar } from './cliente';

export type EstadoSessao = components['schemas']['EstadoSessao'];
export type Modo = EstadoSessao['modo'];
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
