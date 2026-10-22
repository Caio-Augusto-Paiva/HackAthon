# Log de revisões — evidência e proveniência

Este registro reúne achados demonstráveis no checkpoint de 21/10/2026. A especificação contém relatos históricos de revisões por Gemini, Claude e especialistas consultados durante o planejamento; esses relatos permanecem na fonte original e não são apresentados aqui como novas revisões clínicas da base integrada.

| Escopo | Revisor/registro | Achado | Veredito | Prova e aplicação |
|---|---|---|---|---|
| Motor | Revisão de código consolidada no repositório | Correção não relacionada poderia apagar bandeira histórica | Procedeu | Regressões de dependência; evolução para reprocessamento por ordem real em `a677283` |
| Motor/casos | Revisão técnica com Codex | Inconclusivas eram comparadas por igualdade total | Procedeu | `21116e1`, saída deve conter as esperadas |
| Motor | Revisão técnica com Codex | Urgência poderia ser selecionada com CF final negativo | Procedeu | `8b40861`, validação de regra e filtro defensivo |
| Restauração | Revisão técnica com Codex | Repetir respostas antigas pode falhar após correção | Procedeu | Snapshot direto e testes de restauração; preservar ordem dos lotes |
| Contrato de dados | Revisão do JSON com Codex | Tipos, domínios, classes e operadores não correspondiam ao motor | Procedeu | Carregamento direto em `Base.de_dict` e integração `898512c` |
| Conhecimento | Revisão do JSON com Codex | Caneca e inspeção duplicavam a alteração do leite | Procedeu na modelagem proposta | Grupo derivado `max`; validação clínica pendente |
| Conhecimento | Revisão do JSON com Codex | Todos os caminhos de TPB exigiam febre | Procedeu na modelagem proposta | R-TPB-02/04 sem essa exigência, fontes contextuais e testes |
| Comunicação | Curadoria documental com Codex | 30/31 casos, editor e aplicação web podiam ser descritos como entregues | Procedeu no checkpoint inicial | Dois exemplos disponíveis à época; atualização de 22/10 distingue os 34 casos atuais e a consulta web integrada do editor fora de escopo |
| Documentação | Testes do gerador | Texto específico do grupo mamário aparecia mesmo numa mini-base sem esse símbolo | Procedeu | Teste falhou; gerador passou a incluir a nota somente quando o símbolo existe |
| Qualidade clínica | Decisão registrada na sessão | Testes de software seriam suficientes para aprovação clínica | Refutado como conclusão | Regras mantidas como suposição; riscos de correlação documentados |

Para acrescentar uma revisão independente, registrar pessoa/modelo efetivo, data, arquivo/linha, hipótese, execução ou fonte, veredito e commit. Não preencher a coluna de revisor com outra família de modelo apenas porque isso estava previsto no planejamento.

## Atualização técnica — 22/10/2026

| Escopo | Revisor/registro | Achado | Veredito | Prova e aplicação |
|---|---|---|---|---|
| Frontend, troca de modo | Codex, revisão em contexto separado; família diferente não comprovada | Corrigir a tela térmica antiga usava símbolos indisponíveis no modo atual; conflito podia apagar o histórico local | Procedeu | Regressões RED → GREEN, reconciliação por GET e correção sob trava; `85210ca`, `09f5754` e `web/e2e/troca-modo.spec.ts` |
| Entrega, Seção 6 | Codex; executing-plans e verificação documental | Roteiro prometia editor; processo e diários negavam integração já presente; contatos e contagens desatualizados | Procedeu | Relatório `docs/revisoes/2026-10-22-revisao-secao-6.md`, fontes A/D, contrato e arquivos locais; correções nos documentos manuais |
| Tempo e proveniência | Codex; cálculo dos intervalos e conferência de fontes | Tratar 10 + 4 como duração oficial, ou planejamento de agentes como uso pessoal comprovado | Refutado como conclusão | Somatórios 600 + 240 segundos; duração continua estimativa confirmada pela equipe, e relatos pessoais continuam pendentes |

Esta tabela não comprova ensaio humano, validação clínica nem revisão de toda a entrega por outra família de modelo. A revisão final em contexto separado deve registrar o que efetivamente conferiu, sem transformar a identidade planejada de um agente em fato.
