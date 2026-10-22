import { ErroApi } from '../api/cliente';
import { obterSessao, responder, trocarModo, type EstadoSessao, type Modo, type Tela } from '../api/sessao';

type Resultado = { estado?: EstadoSessao; gravada: boolean; erro?: Error };
const erroPublico = (erro: unknown) => erro instanceof Error ? erro : new Error('Não consegui corrigir a resposta. Tente novamente.');
const lerEstado = (id: string) => obterSessao(id).catch(() => undefined);

/** Corrige o fato original e restaura o modo escolhido; a página mantém sua trava até terminar. */
export async function corrigirTelaEmOutroModo(id: string, tela: Tela, corpo: unknown, origem: Modo, destino: Modo): Promise<Resultado> {
  try { await trocarModo(id, origem); }
  catch (erro) { return { estado: await lerEstado(id), gravada: false, erro: erroPublico(erro) }; }
  let gravada = false;
  let erro: Error | undefined;
  let estado: EstadoSessao | undefined;
  try { await responder(id, tela, corpo, true); gravada = true; }
  catch (falha) {
    erro = erroPublico(falha);
    if (falha instanceof ErroApi && falha.status === 409) estado = await lerEstado(id);
  }
  if (estado?.modo !== destino) {
    try { estado = await trocarModo(id, destino); }
    catch { estado = await lerEstado(id); }
  }
  if (!estado || estado.modo !== destino) {
    const nome = destino === 'veterinario' ? 'especialista' : 'produtor';
    const registro = gravada ? 'A resposta foi corrigida.' : 'Não foi possível confirmar a correção.';
    return { estado, gravada, erro: new Error(`${registro} Não consegui retornar ao modo ${nome}. Confira o modo atual e tente a troca novamente.`) };
  }
  return { estado, gravada, erro };
}
