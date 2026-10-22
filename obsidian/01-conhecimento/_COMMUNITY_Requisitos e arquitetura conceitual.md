---
type: community
members: 71
---

# Requisitos e arquitetura conceitual

**Members:** 71 nodes

## Members
- [[dot-graphifyignore exclusões da busca no grafo]] - document - CLAUDE.md
- [[AGENTS.md instruções de busca e manutenção documental]] - document - AGENTS.md
- [[API atual com FastAPI e SQLite]] - concept - CLAUDE.md
- [[Aquisição de conhecimento por especialista e engenheiro]] - concept - CLAUDE.md
- [[Arquitetura atual engine, kb, API, web e base versionada]] - document - CLAUDE.md
- [[Arquivos indicados, código e testes usam busca direta]] - rationale - CLAUDE.md
- [[Atualização do grafo uma vez por bloco documental]] - rationale - CLAUDE.md
- [[Atualização única ao encerrar bloco documental]] - rationale - AGENTS.md
- [[Autorizacao explicita supera a fase de planejamento do CLAUDE]] - rationale - docs/superpowers/plans/2026-10-20-motor-secao-1.md
- [[Avaliação potencial, complexidade, assertividade e organização com IA]] - concept - CLAUDE.md
- [[Base explícita de conhecimento e versões imutáveis]] - concept - CLAUDE.md
- [[Brainstorming não refazer sem pedido]] - rationale - CLAUDE.md
- [[Busca direta quando o arquivo é conhecido; grafo para localizar desconhecidos]] - rationale - AGENTS.md
- [[CLAUDE.md instruções atuais do PoC de anamnese bovina]] - document - CLAUDE.md
- [[Casos de teste com resultado esperado por versão da base]] - rationale - CLAUDE.md
- [[Cinco tarefas TDD do motor (vermelho antes do verde)]] - concept - docs/superpowers/plans/2026-10-20-motor-secao-1.md
- [[Cofre Obsidian 01-conhecimento e reserva 02-a-definir]] - document - CLAUDE.md
- [[Componentes do modelo conceitual exigido]] - document - CLAUDE.md
- [[Conduta requisitos comprovados e suposições explícitas]] - document - CLAUDE.md
- [[Conhecimento veterinário sempre como suposição a validar]] - rationale - CLAUDE.md
- [[Cronograma oficial de 20 a 23 de outubro de 2026]] - concept - CLAUDE.md
- [[Código e testes fora do escopo do grafo]] - rationale - CLAUDE.md
- [[Dados fictícios apenas]] - rationale - CLAUDE.md
- [[Decisão determinística e auditável]] - rationale - CLAUDE.md
- [[Desenho canônico da anamnese bovina]] - document - CLAUDE.md
- [[Desenvolvimento apoiado por agente de IA]] - concept - CLAUDE.md
- [[Dicas do hackathon (slide 13)]] - concept - docs/fontes/transcricao-apresentacao-rerum.md
- [[Diretrizes passo a passo (slide 12)]] - concept - docs/fontes/transcricao-apresentacao-rerum.md
- [[Editor gráfico da base fora do escopo do PoC]] - concept - CLAUDE.md
- [[Encadeamento como responsabilidade do motor]] - rationale - CLAUDE.md
- [[Especificação e planos aprovados; implementação e entrega em curso]] - document - CLAUDE.md
- [[Execução completa em localhost]] - rationale - CLAUDE.md
- [[Explicação por quê e como a partir do traço]] - concept - CLAUDE.md
- [[Fase atual implementação e entrega]] - rationale - CLAUDE.md
- [[Fontes externas no modelo; sensores fora do PoC]] - concept - CLAUDE.md
- [[Fontes oficiais A apresentação RERUM e D documentário]] - document - CLAUDE.md
- [[Frontend React e TypeScript; editor gráfico excluído]] - concept - CLAUDE.md
- [[GRAPH_REPORT visão geral excepcional do projeto]] - document - CLAUDE.md
- [[Grafo de conhecimento ferramenta de busca sob demanda]] - rationale - CLAUDE.md
- [[Interface que pergunta, coleta respostas e apresenta parecer]] - concept - CLAUDE.md
- [[LLM fora da decisão em tempo de execução]] - rationale - CLAUDE.md
- [[Linguagens implementadas Python e React com TypeScript]] - concept - CLAUDE.md
- [[Memória de trabalho da sessão]] - concept - CLAUDE.md
- [[Modelo conceitual de sistema especialista (slide 14)]] - concept - docs/fontes/transcricao-apresentacao-rerum.md
- [[Motor Python com biblioteca padrão]] - concept - CLAUDE.md
- [[Motor de inferência com base e fatos explícitos]] - concept - CLAUDE.md
- [[Mudanças só em código, testes, web, prompts e rascunhos não atualizam grafo]] - rationale - CLAUDE.md
- [[Passo a passo sugerido pelos organizadores]] - document - CLAUDE.md
- [[Persistência SQLite na API]] - concept - CLAUDE.md
- [[Pesos de certeza CF explícitos na base]] - concept - CLAUDE.md
- [[Planejamento não refazer sem pedido]] - rationale - CLAUDE.md
- [[Planos aprovados e documentação de entrega disponível]] - document - CLAUDE.md
- [[Processo atual executar implementação e entrega já aprovadas]] - document - CLAUDE.md
- [[Projeto proposto (slide 8)]] - concept - docs/fontes/transcricao-apresentacao-rerum.md
- [[Projeto proposto Hackathon 2026 (documento D, paginas 2 e 3)]] - concept - docs/fontes/transcricao-documentario-rerum.md
- [[Resolução de conflitos entre regras]] - rationale - CLAUDE.md
- [[Restauracao da sessao a partir do banco (ausente, bloqueia a API)]] - concept - docs/revisoes/2026-10-21-revisao-motor.md
- [[Restrição oficial de código aberto]] - rationale - CLAUDE.md
- [[Sensores fora do escopo do PoC]] - concept - CLAUDE.md
- [[Sistema especialista para anamnese de bovinos leiteiros]] - concept - CLAUDE.md
- [[Skills nao confirmadas (FastAPI, pytest, React Flow, Vite)]] - concept - docs/agentes-e-skills.md
- [[Status de conferencia das fontes (L, R, N)]] - rationale - docs/fontes/fontes.md
- [[T1 Anamnese sinais, histórico e triagem explicável]] - concept - CLAUDE.md
- [[Temas T1 a T3 (documento D, pagina 3)]] - concept - docs/fontes/transcricao-documentario-rerum.md
- [[Temas T1 a T3 (slide 9)]] - concept - docs/fontes/transcricao-apresentacao-rerum.md
- [[Testes localizar diretamente fora do grafo]] - rationale - CLAUDE.md
- [[Traco da sessao reacumula eventos (parcial)]] - concept - docs/revisoes/2026-10-21-revisao-motor.md
- [[Transcrição Markdown de PDF composto apenas por imagens]] - rationale - CLAUDE.md
- [[Traço de inferência para explicar as conclusões]] - concept - CLAUDE.md
- [[graphify --update extração incremental única ao fechar o bloco]] - concept - CLAUDE.md
- [[graphify query primeira opção para localizar informação desconhecida]] - concept - CLAUDE.md

## Live Query (requires Dataview plugin)

```dataview
TABLE source_file, type FROM #community/Requisitos_e_arquitetura_conceitual
SORT file.name ASC
```

## Connections to other communities
- 1 edge to [[_COMMUNITY_Entrega, revisão e contatos]]
- 1 edge to [[_COMMUNITY_Agentes de implementação]]
- 1 edge to [[_COMMUNITY_Fontes clínicas contextuais]]

## Top bridge nodes
- [[Restrição oficial de código aberto]] - degree 5, connects to 1 community
- [[Projeto proposto Hackathon 2026 (documento D, paginas 2 e 3)]] - degree 3, connects to 1 community
- [[Status de conferencia das fontes (L, R, N)]] - degree 2, connects to 1 community