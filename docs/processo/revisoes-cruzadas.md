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
| Comunicação | Curadoria documental com Codex | 30/31 casos, editor e aplicação web podiam ser descritos como entregues | Procedeu | Documentos usam dois casos reais do projeto e separam trabalho planejado |
| Documentação | Testes do gerador | Texto específico do grupo mamário aparecia mesmo numa mini-base sem esse símbolo | Procedeu | Teste falhou; gerador passou a incluir a nota somente quando o símbolo existe |
| Qualidade clínica | Decisão registrada na sessão | Testes de software seriam suficientes para aprovação clínica | Refutado como conclusão | Regras mantidas como suposição; riscos de correlação documentados |

Para acrescentar uma revisão independente, registrar pessoa/modelo efetivo, data, arquivo/linha, hipótese, execução ou fonte, veredito e commit. Não preencher a coluna de revisor com outra família de modelo apenas porque isso estava previsto no planejamento.
