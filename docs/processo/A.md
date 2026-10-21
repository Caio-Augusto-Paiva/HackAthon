# Registro verificável — motor, base e documentação

Data de referência: 21/10/2026. Papel A do planejamento; pessoa responsável a confirmar. Este arquivo é um registro técnico curado desta sessão e do histórico indicado, não um depoimento pessoal escrito por um integrante. Horários não foram registrados e não foram reconstruídos artificialmente.

| Interação/tarefa | Agente e método observados | Decisão | Motivo e evidência |
|---|---|---|---|
| Correção de bandeiras sem relação com a resposta alterada | Codex; revisão e TDD | Ajustado | Regressões e `75bcc45`; implementação posterior consolidada por ordem real em `a677283` |
| Casos com inconclusivas adicionais | Codex; TDD | Aceito | Inclusão de conjunto, não igualdade; `21116e1` |
| CF não positivo de urgência/bandeira | Codex; TDD | Aceito | Validação e defesa no resultado final; `8b40861` |
| Adaptação de objetos `model_dump` com valores nulos | Codex; TDD | Aceito | Excluir campos nulos antes da adaptação; `2718273` |
| Restauração calculando duas vezes | Codex; TDD | Ajustado | Restauração por fábrica privada, sem cálculo inicial redundante; `82bdd5e` e refinamento em `a3e73eb` |
| Explicação de perguntas da triagem | Codex; TDD | Aceito | Origem, motivo e `serve_a` por dependência; `6e35b6f` |
| JSON apresentado como pronto após revisão | Codex; execução de cenários | Ajustado | Compatível com o motor, mas não clinicamente validado; integração em desenvolvimento no `898512c` |
| Duplicação de sinal mamário e exigência universal de febre em TPB | Codex; testes da base | Ajustado | Grupo `max` e caminhos sem febre; 25 testes de base/CLI |
| Aprovação clínica baseada apenas em teste verde | Codex; verificação de evidências | Rejeitado | Preservado `suposicao_a_validar`; CF não calibrados |
| Documentação de entrega da Seção 6 | Codex; writing-plans, TDD e verification-before-completion | Aceito no escopo existente | Gerador, dez testes e documentos curados, com pendências explícitas |

O plano de agentes previa divisão diferente para implementação e revisão. Esta tabela registra o que é comprovável nesta sessão; não atribui a Codex commits executados por outra sessão apenas por estarem na mesma branch.

Antes do envio, a pessoa responsável deve acrescentar: nome, horários/blocos reais que souber comprovar, decisões humanas tomadas, dificuldades de integração e o que aprendeu ao explicar uma parte própria e uma alheia. Acrescentar relatos de revisão por outro modelo somente quando houver evidência.
