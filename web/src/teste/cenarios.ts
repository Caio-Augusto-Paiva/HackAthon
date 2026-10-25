import criacao from '../../../contratos/exemplos/criar_sessao.json';
import dinamica from '../../../contratos/exemplos/obter_sessao.json';
import pausa from '../../../contratos/exemplos/responder_triagem.json';
import parecer from '../../../contratos/exemplos/obter_parecer.json';
import porque from '../../../contratos/exemplos/obter_porque.json';
import como from '../../../contratos/exemplos/obter_como.json';
import type { components } from '../api/tipos.gerado';

type Estado = components['schemas']['EstadoSessao'];
export const segunda = criacao.resposta as Estado;
export const primeira: Estado = {
  ...segunda, revisao: 0, progresso: { ...segunda.progresso, triagem_respondidas: 0 },
  proxima: { tipo: 'tela_triagem', tela_id: 'dias_em_lactacao', selecao: 'unica', permite_nao_sei: true,
    titulo: 'Há quantos dias a vaca pariu?', campos: [{ simbolo: 'dias_em_lactacao', entrada: 'numerico',
      rotulo: 'Número de dias desde o parto', opcoes: null, unidade: 'dias', min: 0, max: 1000 }] },
};
export const multipla: Estado = {
  ...segunda, revisao: 2, progresso: { ...segunda.progresso, triagem_respondidas: 2 },
  proxima: { tipo: 'tela_triagem', tela_id: 'atitude_locomocao', selecao: 'multipla', permite_nao_sei: true,
    titulo: 'Como está a postura da vaca?', campos: [
      ['apatia', 'Abatida'], ['claudicacao', 'Mancando'], ['decubito', 'Caída, sem conseguir se levantar'],
    ].map(([simbolo, rotulo]) => ({ simbolo, rotulo, entrada: 'booleano', opcoes: null, unidade: null, min: null, max: null })) },
};
export const perguntaDinamica = dinamica.resposta as Estado;
export const estadoPausado = pausa.resposta as Estado;
const parecerBase = parecer.resposta as components['schemas']['Parecer'];
// O exemplo do contrato traz tratamento só na hipocalcemia; a cetose (32%) ganha um para cobrir mais de um link.
export const exemploParecer: components['schemas']['Parecer'] = { ...parecerBase, blocos: parecerBase.blocos.map(b => ({ ...b,
  itens: b.itens.map(i => i.doenca === 'cetose' ? { ...i, tratamento: { titulo: 'Cetose em vacas leiteiras', url: 'https://www.embrapa.br/busca-de-publicacoes/-/publicacao/cetose' } } : i) })) };
export const exemploPorque = porque.resposta;
export const exemploComo = como.resposta;

export function resposta(dados: unknown, status = 200) {
  return new Response(JSON.stringify(dados), { status, headers: { 'Content-Type': 'application/json' } });
}
