import { FormularioResposta, type PropriedadesFormulario } from './FormularioResposta';
import type { TelaTriagem as Tela } from './mapearResposta';

export function TelaTriagem({ tela, ...propriedades }: PropriedadesFormulario & { tela: Tela }) {
  return <FormularioResposta {...propriedades} campos={tela.campos} multipla={tela.selecao === 'multipla'} permiteNaoSei={tela.permite_nao_sei} />;
}
