import { FormularioResposta, type PropriedadesFormulario } from './FormularioResposta';
import type { PerguntaDinamica as Pergunta } from './mapearResposta';

export function PerguntaDinamica({ pergunta, ...propriedades }: PropriedadesFormulario & { pergunta: Pergunta }) {
  return <FormularioResposta {...propriedades} campos={[{ ...pergunta, rotulo: pergunta.texto }]}
    multipla={false} permiteNaoSei={pergunta.permite_nao_sei} />;
}
