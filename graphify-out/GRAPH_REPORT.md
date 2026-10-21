# Graph Report - HackAtom  (2026-10-21)

## Corpus Check
- 32 files · ~53,865 words
- Verdict: corpus is large enough that graph structure adds value.
- Unclassified: 2 file(s) not represented in the graph (top: (none) 2)

## Summary
- 304 nodes · 474 edges · 17 communities (10 shown, 7 thin omitted)
- Extraction: 86% EXTRACTED · 13% INFERRED · 0% AMBIGUOUS · INFERRED: 63 edges (avg confidence: 0.82)
- Token cost: 0 input · 0 output

## Community Hubs (Navigation)
- Arquitetura disponível: CLI/Python, JSON, sessão, inferência e explicação
- Motor de inferência (engine/)
- Motor de inferencia
- Motor de inferência da seção 1
- Sessao: triagem, perguntas e correções
- Playwright Test webServer
- MSD Vet Manual
- obra/superpowers (repositorio de skills)
- Google Antigravity (app, IDE e CLI)
- Potencial com intervalos conservadores
- Traco de inferencia
- Playwright
- SQLite
- Agentes e skills por prompt (decisao de 20/10/2026)
- Transcricao da apresentacao RERUM [A]
- Transcricao do documentario RERUM [D]

## God Nodes (most connected - your core abstractions)
1. `Motor de inferência (engine/)` - 15 edges
2. `Especificação PoC Anamnese de Bovinos Leiteiros` - 13 edges
3. `MSD Vet Manual` - 13 edges
4. `Arquitetura disponível: CLI/Python, JSON, sessão, inferência e explicação` - 13 edges
5. `Índice da entrega parcial: branch codex-davi, referência inicial 898512c` - 13 edges
6. `Plano de execução da documentação parcial do núcleo e base existentes` - 13 edges
7. `Motor de inferencia` - 12 edges
8. `Processo verificável do checkpoint de 21/10/2026` - 12 edges
9. `Sessao: triagem, perguntas e correções` - 12 edges
10. `HackAtom: T1 Anamnese explicável de bovinos leiteiros` - 11 edges

## Surprising Connections (you probably didn't know these)
- `Status de conferencia das fontes (L, R, N)` --semantically_similar_to--> `Marcacao de suposicao a validar (conhecimento veterinario)`  [INFERRED] [semantically similar]
  docs/fontes/fontes.md → CLAUDE.md
- `Cinco tarefas TDD do motor (vermelho antes do verde)` --semantically_similar_to--> `Testes com casos conhecidos por versao da base`  [INFERRED] [semantically similar]
  docs/superpowers/plans/2026-10-20-motor-secao-1.md → CLAUDE.md
- `Estudo pendente: persistência integral de snapshot, ordem e versão da base` --semantically_similar_to--> `Restauração direta por snapshot integral, sem repetir o diálogo`  [INFERRED] [semantically similar]
  docs/processo/B.md → engine/README.md
- `Cinco tarefas TDD do motor (vermelho antes do verde)` --implements--> `Motor de inferência da seção 1`  [EXTRACTED]
  docs/superpowers/plans/2026-10-20-motor-secao-1.md → engine/README.md
- `Restauracao da sessao a partir do banco (ausente, bloqueia a API)` --conceptually_related_to--> `Memoria de trabalho`  [INFERRED]
  docs/revisoes/2026-10-21-revisao-motor.md → CLAUDE.md

## Import Cycles
- None detected.

## Hyperedges (group relationships)
- **Checkpoint distingue testes de software, casos sintéticos e validação clínica pendente** — docs_entrega_readme_evidencia_testes, docs_entrega_04_casos_de_teste_casos_sinteticos, docs_entrega_03_regras_de_producao_fontes_contextuais_cf_nao_validado, docs_entrega_readme_atendimento_parcial_exigencias [EXTRACTED 1.00]
- **Geração de regras/casos e verificação de sincronismo documental** — docs_superpowers_plans_2026_10_21_documentacao_entrega_parcial_geracao_verificacao_docs, readme_documentacao_sincronizada, docs_entrega_03_regras_de_producao_regras_geradas, docs_entrega_04_casos_de_teste_casos_sinteticos [EXTRACTED 1.00]
- **Pacotes api -> engine -> kb e web** — docs_superpowers_specs_2026_10_20_anamnese_bovinos_design_pacote_api, docs_superpowers_specs_2026_10_20_anamnese_bovinos_design_pacote_engine, docs_superpowers_specs_2026_10_20_anamnese_bovinos_design_pacote_kb, docs_superpowers_specs_2026_10_20_anamnese_bovinos_design_pacote_web [EXTRACTED 1.00]
- **Ciclo de edição e validação da base** — docs_superpowers_specs_2026_10_20_anamnese_bovinos_design_editor_grafico, docs_superpowers_specs_2026_10_20_anamnese_bovinos_design_validador_kb, docs_superpowers_specs_2026_10_20_anamnese_bovinos_design_versionamento_imutavel, docs_superpowers_specs_2026_10_20_anamnese_bovinos_design_casos_teste [EXTRACTED 1.00]
- **Divergencias e lacunas da revisao do motor (21/10/2026)** — docs_revisoes_2026_10_21_revisao_motor_bandeira_apos_correcao, docs_revisoes_2026_10_21_revisao_motor_percentual_parecer, docs_revisoes_2026_10_21_revisao_motor_restauracao_sessao, docs_revisoes_2026_10_21_revisao_motor_traco_sessao, docs_revisoes_2026_10_21_revisao_motor_executor_casos [EXTRACTED 1.00]
- **Modelo conceitual de sistema especialista (slide 14)** — claude_motor_de_inferencia, claude_base_conhecimento, claude_memoria_de_trabalho, claude_modulo_explicacao, claude_interface_usuario, claude_aquisicao_conhecimento, claude_fontes_dados_externas [EXTRACTED 1.00]
- **Três camadas de avaliação de regras** — docs_superpowers_specs_2026_10_20_anamnese_bovinos_design_derivados_sinais, docs_superpowers_specs_2026_10_20_anamnese_bovinos_design_dominio_8_doencas, docs_superpowers_specs_2026_10_20_anamnese_bovinos_design_urgencia_gravidade_confianca, docs_superpowers_specs_2026_10_20_anamnese_bovinos_design_bandeiras_vermelhas, docs_superpowers_specs_2026_10_20_anamnese_bovinos_design_camadas_tres [EXTRACTED 1.00]
- **Premissas de instalacao no Windows a validar** — docs_pesquisa_suposicoes_linha_24_node, docs_pesquisa_suposicoes_rodar_ps1, docs_pesquisa_suposicoes_winget_uv_id, docs_pesquisa_suposicoes_vite_mocks, docs_pesquisa_suposicoes_windows_11_demo, docs_pesquisa_execucao_local_powershell_execution_policy [INFERRED 0.75]
- **Pipeline de planejamento e execucao com skills (obra/superpowers)** — docs_pesquisa_agentes_e_skills_brainstorming, docs_pesquisa_agentes_e_skills_writing_plans, docs_pesquisa_agentes_e_skills_executing_plans, docs_pesquisa_agentes_e_skills_test_driven_development, docs_pesquisa_agentes_e_skills_subagent_driven_development [INFERRED 0.85]
- **Stack de execucao local em localhost** — docs_pesquisa_execucao_local_fastapi_frontend, docs_pesquisa_execucao_local_vite, docs_pesquisa_execucao_local_uv, docs_pesquisa_execucao_local_playwright_webserver, docs_pesquisa_versoes_bibliotecas_uvicorn [INFERRED 0.85]

## Communities (17 total, 7 thin omitted)

### Community 0 - "Arquitetura disponível: CLI/Python, JSON, sessão, inferência e explicação"
Cohesion: 0.08
Nodes (41): Base de desenvolvimento 3.1.0-revisao1: 51 símbolos, 56 regras, 8 doenças e 6 telas, Exemplos sintéticos de alerta e sinais mamários pela CLI, Histórico: correções do motor e integração de desenvolvimento em 898512c, IA aplicada ao desenvolvimento e à documentação, fora da consulta, Processo verificável do checkpoint de 21/10/2026, Arquitetura disponível: CLI/Python, JSON, sessão, inferência e explicação, Contratos de sessão, parecer, porque/como e snapshot integral, Integração futura: FastAPI/Pydantic, React, SQLite e editor em grafo (+33 more)

### Community 1 - "Motor de inferência (engine/)"
Cohesion: 0.07
Nodes (48): Apresentação e roteiro da demonstração, Bandeiras vermelhas (chamar_agora), Base de conhecimento JSON versionada (kb/), Três camadas estritas (derivado, doença, urgência), Casos de teste conhecidos (31 casos), Contratos da API e formato único de erro, Correções e recálculo dos fatos, Critérios de parada (confirmação, limite, exaustão) (+40 more)

### Community 2 - "Motor de inferencia"
Cohesion: 0.08
Nodes (29): CLAUDE.md do projeto (PoC Anamnese de Bovinos Leiteiros), Aquisicao de conhecimento, Motor de regras em Python independente de interface, Base de conhecimento, Testes com casos conhecidos por versao da base, Criterios de avaliacao do hackathon, Cronograma e entrega do hackathon (20 a 23/10), Editor grafico do fluxo da anamnese (+21 more)

### Community 3 - "Motor de inferência da seção 1"
Cohesion: 0.07
Nodes (24): Alocacao de agente principal e alternativa por prompt de revisao, anthropics/skills (pptx, docx, pdf, webapp-testing, frontend-design), Antigravity (plano Pro), Claude Code (Claude Pro), Codex (ChatGPT Plus), Gemini Pro (Google AI Pro, app web), Implementacao por pessoa (A, B, C) com agente principal e reserva, Fontes do projeto (fontes oficiais e de dominio) (+16 more)

### Community 4 - "Sessao: triagem, perguntas e correções"
Cohesion: 0.08
Nodes (22): Fontes de dados externas, Memoria de trabalho, Adaptacoes que a API precisa fazer sobre o motor, Bandeira some apos correcao (divergencia), bandeiras_nao_verificadas restrito a regras viaveis e perguntaveis, Prioridade padrao por classe (100/50/10) e demais correcoes menores, Cortes de bloco nao lidos de meta.limiares, Executor de casos incompleto (inconclusivas e pausa) (+14 more)

### Community 5 - "Playwright Test webServer"
Cohesion: 0.08
Nodes (26): anthropics/skills (repositorio), frontend-design (skill), playwright-skill (lackeyjb), pptx (skill, source-available), Restricao de open source do hackathon, skill-creator (skill), webapp-testing (skill), uv (sync, run, python pin) (+18 more)

### Community 6 - "MSD Vet Manual"
Cohesion: 0.10
Nodes (21): Conteudo obrigatorio do plano final (12 itens), Limite da fase de planejamento (sem implementacao), Skill superpowers:brainstorming, Skill superpowers:writing-plans, Skills em formato aberto (.agents/skills, .claude/skills, AGENTS.md), obra/superpowers (skills em formato aberto), Acidose ruminal (categoria), Acidose ruminal subaguda (+13 more)

### Community 7 - "obra/superpowers (repositorio de skills)"
Cohesion: 0.16
Nodes (16): brainstorming (skill), executing-plans (skill), subagent-driven-development (skill), obra/superpowers (repositorio de skills), systematic-debugging (skill), test-driven-development (skill), verification-before-completion (skill), writing-plans (skill) (+8 more)

### Community 8 - "Google Antigravity (app, IDE e CLI)"
Cohesion: 0.42
Nodes (9): AGENTS.md (instrucoes do projeto), Google Antigravity (app, IDE e CLI), Claude Code, CLAUDE.md (instrucoes do projeto), OpenAI Codex (CLI, IDE, app desktop), Gemini CLI, GEMINI.md (instrucoes do projeto), Limites de uso dos planos (+1 more)

### Community 10 - "Traco de inferencia"
Cohesion: 0.67
Nodes (3): Modulo de explicacao (por que e como), Traco de inferencia, Traco da sessao reacumula eventos (parcial)

## Ambiguous Edges - Review These
- `uv (sync, run, python pin)` → `Python 3.15.0`  [AMBIGUOUS]
  docs/pesquisa/execucao-local.md · relation: conceptually_related_to
- `Limites de uso dos planos` → `Gemini CLI`  [AMBIGUOUS]
  docs/pesquisa/agentes-e-skills.md · relation: references

## Knowledge Gaps
- **53 isolated node(s):** `Fatos (variável, valor, CF) e avaliação de condições`, `Resolução de conflito (agenda)`, `Persistência SQLite`, `Fontes de domínio F1 a F12`, `Fontes de dados externas` (+48 more)
  These have ≤1 connection - possible missing edges or undocumented components. (Counts symbols only; 70 node(s) total have ≤1 connection when file, concept and rationale nodes are included.)
- **7 thin communities (<3 nodes) omitted from report** — run `graphify query` to explore isolated nodes.

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **Why does `Motor de inferência da seção 1` connect `Motor de inferência da seção 1` to `Motor de inferencia`, `Sessao: triagem, perguntas e correções`?**
  _High betweenness centrality (0.090) - this node is a cross-community bridge._
- **What connects `Fatos (variável, valor, CF) e avaliação de condições`, `Resolução de conflito (agenda)`, `Persistência SQLite` to the rest of the system?**
  _53 weakly-connected nodes found - possible documentation gaps or missing edges._
- **Should `Arquitetura disponível: CLI/Python, JSON, sessão, inferência e explicação` be split into smaller, more focused modules?**
  _Cohesion score 0.07731694828469023 - nodes in this community are weakly interconnected._
- **Why does `Alocacao de agente principal e alternativa por prompt de revisao` connect `Motor de inferência da seção 1` to `MSD Vet Manual`?**
  _High betweenness centrality (0.067) - this node is a cross-community bridge._
- **Should `Motor de inferência (engine/)` be split into smaller, more focused modules?**
  _Cohesion score 0.07039187227866474 - nodes in this community are weakly interconnected._

### Low-confidence Hints
_AMBIGUOUS edges — the extractor was unsure. Verify before acting on these._

- **What is the exact relationship between `uv (sync, run, python pin)` and `Python 3.15.0`?**
  _Edge tagged AMBIGUOUS (relation: conceptually_related_to) - confidence is low._
- **What is the exact relationship between `Limites de uso dos planos` and `Gemini CLI`?**
  _Edge tagged AMBIGUOUS (relation: references) - confidence is low._
## Proveniência desta atualização

- 15 documentos lidos integralmente; cobertura conferida por contagem de linhas.
- Extração semântica pelo agente local; métricas de tokens desta chamada indisponíveis.
- Código do motor, testes e scripts fora do corpus semântico; base e casos estão descritos nos documentos gerados.
