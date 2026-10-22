# Processo de desenvolvimento — consolidado em 22/10/2026

Este relato foi curado a partir dos artefatos versionados e do histórico Git até `d9eda27`. Distingue implementação, planejamento e informação ainda não fornecida pelas pessoas. Os registros de 21/10 são checkpoints históricos, atualizados abaixo com a integração de 22/10. As letras dos diários correspondem ao planejamento original; não comprovam autoria pessoal. Nomes, contatos e responsabilidades informados estão no [índice](README.md).

## Problema e método

O tema escolhido foi T1 Anamnese: tornar a triagem de bovinos leiteiros em lactação explícita e explicável. Em um sistema especialista, a base armazena o conhecimento em regras e o motor aplica essas regras aos fatos observados. Aqui, a seleção de perguntas é dirigida a hipóteses e a propagação usa fatores de certeza MYCIN. O traço permite responder por que uma pergunta foi feita e como uma hipótese recebeu evidências.

A IA foi usada para planejamento, revisão de contratos, exploração de falhas, preparação de testes, implementação assistida e redação. A consulta não usa IA generativa: o programa recebe fatos e executa Python e JSON locais. O conhecimento veterinário continua sem validação clínica registrada.

## Linha do tempo comprovável

| Data | Evidência | Resultado |
|---|---|---|
| 20/10 | [Especificação consolidada](../superpowers/specs/2026-10-20-anamnese-bovinos-design.md), [plano do motor](../superpowers/plans/2026-10-20-motor-secao-1.md) e histórico Git | Escopo, camadas, CF, contratos e tarefas foram documentados |
| 21/10 | [Revisão do motor](../revisoes/2026-10-21-revisao-motor.md), referência `ce6874b` | Falhas e divergências foram registradas antes das correções |
| 21/10 | `aaa7841` e seis commits de `75bcc45` a `6e35b6f` | Ajustes em bandeiras, casos, CF de urgência, adaptação de dados, restauração e explicação da triagem |
| 21/10 | `f0d8c6f`, `a3e73eb` e `a677283` | Reprocessamento de bandeiras consolidado pela ordem real das respostas; restauração e regressões ampliadas |
| 21/10 | `898512c` | Base revisada integrada como desenvolvimento, com 51 símbolos, 56 regras, dois exemplos e 25 testes específicos |
| 21/10 | Este pacote e `scripts/gerar_doc_regras.py` | Documentação derivada da implementação, geração de tabelas e guarda contra divergência |
| 22/10 | `f46cd6e` e documentos 03/04 | Integração dos 34 casos sintéticos, API e persistência; riscos de coleta R15/R16 registrados |
| 22/10 | `7494e3e`, `cff6704`, `web/QUALIDADE.md` | Consulta React integrada ao backend, base ativa `v0002`, fontes e SVGs locais, verificação de acessibilidade e quatro larguras |
| 22/10 | `1593149`, `85210ca`, `09f5754` | Troca produtor ↔ especialista na mesma sessão, histórico corrigível e parecer único; 60 testes de interface e 11 E2E no checkpoint |
| 22/10 | `d9eda27` | Grafo e Obsidian atualizados após a integração; navegação documental separada do runtime |

O cronograma original é uma previsão, não um registro de horários cumpridos. A consulta web já pode ser demonstrada em localhost; a CLI é uma reserva. Editor gráfico, material visual final, licença e ensaio humano continuam pendentes. Os testes de software não comprovam validação clínica nem preparo da máquina reserva.

## Passo a passo pedido pelos organizadores

| Passo de [A], slide 12 | Artefato/evidência | Estado |
|---|---|---|
| 1. Escolher agente de IA | [Alocação de agentes](../agentes-e-skills.md) e registro desta sessão com Codex | Planejado e parcialmente registrado em execução |
| 2. Entender sistema especialista e motor | Seção 1 da especificação e [arquitetura](02-arquitetura.md) | Documentado |
| 3. Escolher tecnologia | Python no núcleo; FastAPI/Pydantic e SQLite na API; React 19, TypeScript e Vite 8 em `web/` | Componentes integrados; detalhes no documento 02 |
| 4. Pesquisar contexto do negócio | [Fontes](../fontes/fontes.md) e notas de fonte em cada regra | Pesquisa registrada; calibração pendente |
| 5. Definir escopo e arquitetura | Especificação canônica e diagrama do documento 02 | Documentado |
| 6. Definir regras | Base ativa `v0002` e documento 03 gerado | 56 regras disponíveis, todas como suposição |
| 7. Implementar e testar | `engine/`, `kb/`, `api/`, `web/`, testes e casos executáveis | Checkpoint integrado: 1066 testes Python aprovados, 1 ignorado, 170 subtestes; 60 Vitest e 11 E2E, sem somar novamente os 132 unittest coletados por pytest |
| 8. Estudar e entender a produção | Perguntas de treino do documento 05 | Ensaio individual e cruzado a registrar pelo grupo |

## Julgamento sobre sugestões da IA

Os exemplos abaixo têm evidência no código e nos testes; não são depoimentos atribuídos a pessoas que não forneceram diário.

| Tarefa ou sugestão | Agente/registro | Decisão e motivo | Evidência |
|---|---|---|---|
| Reconstruir a sessão repetindo chamadas de resposta | Revisão técnica assistida por Codex | Rejeitado: uma correção pode mudar a pergunta seguinte; usar snapshot direto | `Sessao.restaurar`, `test_restauracao_nao_repete_respostas_com_ordem_ja_alterada_por_correcao` |
| Limpar todas as bandeiras em qualquer correção | Revisão assistida e regressões | Ajustado: reprocessar os lotes na ordem real, conservando gatilhos de prefixos válidos | `a677283`, `tests/engine/test_reprocessamento.py` |
| Comparar inconclusivas pelo conjunto inteiro | Revisão assistida por Codex | Ajustado: exigir que a saída contenha as esperadas | `21116e1`, testes de inconclusivas |
| Usar caneca e alteração visual do leite como apoios independentes | Revisão do JSON com Codex | Ajustado: grupo derivado `max`, preservando os pesos originais | R-MAS-01/03/05, teste de duplicação de evidência |
| Exigir febre em toda regra de TPB | Revisão do JSON com Codex | Ajustado na base proposta: mantidos caminhos sem febre; critérios permanecem a validar | R-TPB-02/04 e testes específicos |
| Tratar a base como clinicamente aprovada após testes | Decisão registrada nesta sessão | Rejeitado: os testes verificam comportamento, não acurácia clínica | Estado `suposicao_a_validar` em todas as regras |
| Escrever tabelas de regras manualmente | Documentação com Codex | Ajustado: tabelas geradas da base e conferidas por teste | `scripts/gerar_doc_regras.py`, `tests/documentacao/` |

## IA, skills e revisões

Na sessão documentada foram aplicadas as skills `using-superpowers`, `receiving-code-review`, `test-driven-development`, `systematic-debugging`, `verification-before-completion` e, para organizar esta entrega, `writing-plans`. Graphify mantém os documentos navegáveis e exporta o cofre do Obsidian. São ferramentas de desenvolvimento e documentação; não compõem o caminho de inferência.

Na implementação da interface, os registros incluem Codex, Figma, `impeccable`, TDD e verificação antes da conclusão. O checkpoint de troca de modo usou execução inline e uma revisão técnica em contexto separado; isso não comprova revisão por outra família de modelo. O [relatório web](../../web/QUALIDADE.md) registra o alcance dos testes e os achados corrigidos. A revisão da Seção 6 usa `executing-plans` para auditar e corrigir documentação, sem modificar o sistema de decisão.

O documento de alocação descreve intenção de usar outras famílias de modelos. Este checkpoint não comprova que todas as revisões previstas foram realizadas, nem que cada integrante usou determinada ferramenta. O [log de revisões](../processo/revisoes-cruzadas.md) separa correções verificadas de relatos históricos. Os [diários A](../processo/A.md), [B](../processo/B.md) e [C](../processo/C.md) precisam de complementação pelos responsáveis.

Não foram criadas entradas pessoais para atingir a meta sugerida de 8–10 interações por pessoa. Essa meta é uma convenção interna, não uma exigência dos organizadores. Horários, decisões humanas, ferramentas usadas por cada pessoa e prova de entendimento devem ser preenchidos pelos próprios integrantes.

## Organização e aprendizado a registrar

O núcleo mantém uma fronteira independente: a API pode consumir estado, parecer, explicações e snapshot sem importar conhecimento clínico de dentro do motor. A base entra como dado. A correção de contrato foi verificada antes da integração da base; nenhuma assinatura do motor precisou ser alterada para essa integração.

Revisões reais evidenciaram três aprendizados: ausência de um dado não equivale a uma resposta negativa; fatos finais e ordem de chegada têm papéis distintos nas bandeiras históricas; teste verde não calibra um peso clínico. Cada integrante deve explicar no ensaio uma regra, uma combinação de CF, um limite do modelo e uma parte que não escreveu. O resultado desse ensaio permanece a preencher, sem relato fictício de aprendizado pessoal.

As limitações e as ações seguintes estão no [registro de riscos](06-riscos-e-pendencias.md). Esta documentação não converte metas futuras em trabalho concluído.
