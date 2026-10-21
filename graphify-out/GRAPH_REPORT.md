# Graph Report - HackAtom  (2026-10-21)

## Corpus Check
- Corpus is ~33,777 words - fits in a single context window. You may not need a graph.

## Summary
- 241 nodes · 323 edges · 19 communities (12 shown, 7 thin omitted)
- Extraction: 80% EXTRACTED · 19% INFERRED · 1% AMBIGUOUS · INFERRED: 61 edges (avg confidence: 0.82)
- Tokens: histórico registrado de 520.209 tokens; atualização incremental atual sem medição disponível.

## Community Hubs (Navigation)
- Motor de inferência (engine/)
- Sessao: triagem, perguntas e correções
- Playwright Test webServer
- Motor de inferência da seção 1
- Motor de inferencia
- MSD Vet Manual
- obra/superpowers (repositorio de skills)
- Testes com casos conhecidos por versao da base
- Google Antigravity (app, IDE e CLI)
- Limite da fase de planejamento (sem implementacao)
- CF MYCIN com Fraction
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
4. `Motor de inferencia` - 12 edges
5. `Sessao: triagem, perguntas e correções` - 12 edges
6. `Motor de inferência da seção 1` - 11 edges
7. `CLAUDE.md do projeto (PoC Anamnese de Bovinos Leiteiros)` - 9 edges
8. `Base de conhecimento JSON versionada (kb/)` - 9 edges
9. `Alocacao de agente principal e alternativa por prompt de revisao` - 9 edges
10. `Conhecimento de domínio: 8 doenças` - 8 edges

## Surprising Connections (you probably didn't know these)
- `Status de conferencia das fontes (L, R, N)` --semantically_similar_to--> `Marcacao de suposicao a validar (conhecimento veterinario)`  [INFERRED] [semantically similar]
  docs/fontes/fontes.md → CLAUDE.md
- `Cinco tarefas TDD do motor (vermelho antes do verde)` --semantically_similar_to--> `Testes com casos conhecidos por versao da base`  [INFERRED] [semantically similar]
  docs/superpowers/plans/2026-10-20-motor-secao-1.md → CLAUDE.md
- `Cinco tarefas TDD do motor (vermelho antes do verde)` --implements--> `Motor de inferência da seção 1`  [EXTRACTED]
  docs/superpowers/plans/2026-10-20-motor-secao-1.md → engine/README.md
- `Modelo conceitual de sistema especialista (slide 14)` --references--> `Motor de inferencia`  [EXTRACTED]
  docs/fontes/transcricao-apresentacao-rerum.md → CLAUDE.md
- `Dicas do hackathon (slide 13)` --references--> `Testes com casos conhecidos por versao da base`  [EXTRACTED]
  docs/fontes/transcricao-apresentacao-rerum.md → CLAUDE.md

## Import Cycles
- None detected.

## Hyperedges (group relationships)
- **Pacotes api -> engine -> kb e web** — docs_superpowers_specs_2026_10_20_anamnese_bovinos_design_pacote_api, docs_superpowers_specs_2026_10_20_anamnese_bovinos_design_pacote_engine, docs_superpowers_specs_2026_10_20_anamnese_bovinos_design_pacote_kb, docs_superpowers_specs_2026_10_20_anamnese_bovinos_design_pacote_web [EXTRACTED 1.00]
- **Ciclo de edição e validação da base** — docs_superpowers_specs_2026_10_20_anamnese_bovinos_design_editor_grafico, docs_superpowers_specs_2026_10_20_anamnese_bovinos_design_validador_kb, docs_superpowers_specs_2026_10_20_anamnese_bovinos_design_versionamento_imutavel, docs_superpowers_specs_2026_10_20_anamnese_bovinos_design_casos_teste [EXTRACTED 1.00]
- **Divergencias e lacunas da revisao do motor (21/10/2026)** — docs_revisoes_2026_10_21_revisao_motor_bandeira_apos_correcao, docs_revisoes_2026_10_21_revisao_motor_percentual_parecer, docs_revisoes_2026_10_21_revisao_motor_restauracao_sessao, docs_revisoes_2026_10_21_revisao_motor_traco_sessao, docs_revisoes_2026_10_21_revisao_motor_executor_casos [EXTRACTED 1.00]
- **Modelo conceitual de sistema especialista (slide 14)** — claude_motor_de_inferencia, claude_base_conhecimento, claude_memoria_de_trabalho, claude_modulo_explicacao, claude_interface_usuario, claude_aquisicao_conhecimento, claude_fontes_dados_externas [EXTRACTED 1.00]
- **Três camadas de avaliação de regras** — docs_superpowers_specs_2026_10_20_anamnese_bovinos_design_derivados_sinais, docs_superpowers_specs_2026_10_20_anamnese_bovinos_design_dominio_8_doencas, docs_superpowers_specs_2026_10_20_anamnese_bovinos_design_urgencia_gravidade_confianca, docs_superpowers_specs_2026_10_20_anamnese_bovinos_design_bandeiras_vermelhas, docs_superpowers_specs_2026_10_20_anamnese_bovinos_design_camadas_tres [EXTRACTED 1.00]
- **Premissas de instalacao no Windows a validar** — docs_pesquisa_suposicoes_linha_24_node, docs_pesquisa_suposicoes_rodar_ps1, docs_pesquisa_suposicoes_winget_uv_id, docs_pesquisa_suposicoes_vite_mocks, docs_pesquisa_suposicoes_windows_11_demo, docs_pesquisa_execucao_local_powershell_execution_policy [INFERRED 0.75]
- **Pipeline de planejamento e execucao com skills (obra/superpowers)** — docs_pesquisa_agentes_e_skills_brainstorming, docs_pesquisa_agentes_e_skills_writing_plans, docs_pesquisa_agentes_e_skills_executing_plans, docs_pesquisa_agentes_e_skills_test_driven_development, docs_pesquisa_agentes_e_skills_subagent_driven_development [INFERRED 0.85]
- **Stack de execucao local em localhost** — docs_pesquisa_execucao_local_fastapi_frontend, docs_pesquisa_execucao_local_vite, docs_pesquisa_execucao_local_uv, docs_pesquisa_execucao_local_playwright_webserver, docs_pesquisa_versoes_bibliotecas_uvicorn [INFERRED 0.85]

## Communities (19 total, 7 thin omitted)

### Community 0 - "Motor de inferência (engine/)"
Cohesion: 0.07
Nodes (48): Apresentação e roteiro da demonstração, Bandeiras vermelhas (chamar_agora), Base de conhecimento JSON versionada (kb/), Três camadas estritas (derivado, doença, urgência), Casos de teste conhecidos (31 casos), Contratos da API e formato único de erro, Correções e recálculo dos fatos, Critérios de parada (confirmação, limite, exaustão) (+40 more)

### Community 1 - "Sessao: triagem, perguntas e correções"
Cohesion: 0.08
Nodes (24): Fontes de dados externas, Memoria de trabalho, Adaptacoes que a API precisa fazer sobre o motor, Arvore da secao 4.3 da especificacao (sessao, validacao, modelos), Bandeira some apos correcao (divergencia), bandeiras_nao_verificadas restrito a regras viaveis e perguntaveis, Tabela de conformidade com a especificacao (16 itens), Cortes de bloco nao lidos de meta.limiares (+16 more)

### Community 2 - "Playwright Test webServer"
Cohesion: 0.08
Nodes (26): anthropics/skills (repositorio), frontend-design (skill), playwright-skill (lackeyjb), pptx (skill, source-available), Restricao de open source do hackathon, skill-creator (skill), webapp-testing (skill), uv (sync, run, python pin) (+18 more)

### Community 3 - "Motor de inferência da seção 1"
Cohesion: 0.09
Nodes (18): Alocacao de agente principal e alternativa por prompt de revisao, anthropics/skills (pptx, docx, pdf, webapp-testing, frontend-design), Antigravity (plano Pro), Claude Code (Claude Pro), Codex (ChatGPT Plus), Gemini Pro (Google AI Pro, app web), Implementacao por pessoa (A, B, C) com agente principal e reserva, Fontes do projeto (fontes oficiais e de dominio) (+10 more)

### Community 4 - "Motor de inferencia"
Cohesion: 0.12
Nodes (20): CLAUDE.md do projeto (PoC Anamnese de Bovinos Leiteiros), Motor de regras em Python independente de interface, Criterios de avaliacao do hackathon, Cronograma e entrega do hackathon (20 a 23/10), Encadeamento para frente e para tras, Fatores de certeza (CF), Interface do usuario, Motor de inferencia (+12 more)

### Community 5 - "MSD Vet Manual"
Cohesion: 0.13
Nodes (16): Conteudo obrigatorio do plano final (12 itens), Acidose ruminal (categoria), Acidose ruminal subaguda, Anaplasmose, Babesiose, Cetose bovina (hiperCetonemia), Dermatite digital, Deslocamento de abomaso (+8 more)

### Community 6 - "obra/superpowers (repositorio de skills)"
Cohesion: 0.16
Nodes (16): brainstorming (skill), executing-plans (skill), subagent-driven-development (skill), obra/superpowers (repositorio de skills), systematic-debugging (skill), test-driven-development (skill), verification-before-completion (skill), writing-plans (skill) (+8 more)

### Community 7 - "Testes com casos conhecidos por versao da base"
Cohesion: 0.25
Nodes (9): Aquisicao de conhecimento, Base de conhecimento, Testes com casos conhecidos por versao da base, Editor grafico do fluxo da anamnese, FastAPI + Pydantic, pytest, React Flow, Skills nao confirmadas (FastAPI, pytest, React Flow, Vite) (+1 more)

### Community 8 - "Google Antigravity (app, IDE e CLI)"
Cohesion: 0.42
Nodes (9): AGENTS.md (instrucoes do projeto), Google Antigravity (app, IDE e CLI), Claude Code, CLAUDE.md (instrucoes do projeto), OpenAI Codex (CLI, IDE, app desktop), Gemini CLI, GEMINI.md (instrucoes do projeto), Limites de uso dos planos (+1 more)

### Community 9 - "Limite da fase de planejamento (sem implementacao)"
Cohesion: 0.40
Nodes (5): Limite da fase de planejamento (sem implementacao), Skill superpowers:brainstorming, Skill superpowers:writing-plans, Skills em formato aberto (.agents/skills, .claude/skills, AGENTS.md), obra/superpowers (skills em formato aberto)

### Community 10 - "CF MYCIN com Fraction"
Cohesion: 0.33
Nodes (4): Prioridade padrao por classe (100/50/10) e demais correcoes menores, CF MYCIN com Fraction, inferir(base, fatos): núcleo sem estado, Testes unittest e coleta pytest

### Community 12 - "Traco de inferencia"
Cohesion: 0.67
Nodes (3): Modulo de explicacao (por que e como), Traco de inferencia, Traco da sessao reacumula eventos (parcial)

## Ambiguous Edges - Review These
- `Limites de uso dos planos` → `Gemini CLI`  [AMBIGUOUS]
  docs/pesquisa/agentes-e-skills.md · relation: references
- `uv (sync, run, python pin)` → `Python 3.15.0`  [AMBIGUOUS]
  docs/pesquisa/execucao-local.md · relation: conceptually_related_to

## Knowledge Gaps
- **52 isolated node(s):** `Motor de regras em Python independente de interface`, `Criterios de avaliacao do hackathon`, `Cronograma e entrega do hackathon (20 a 23/10)`, `Encadeamento para frente e para tras`, `Fatores de certeza (CF)` (+47 more)
  These have ≤1 connection - possible missing edges or undocumented components. (Counts symbols only; 69 node(s) total have ≤1 connection when file, concept and rationale nodes are included.)
- **7 thin communities (<3 nodes) omitted from report** — run `graphify query` to explore isolated nodes.

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **Why does `Motor de inferência da seção 1` connect `Motor de inferência da seção 1` to `Sessao: triagem, perguntas e correções`, `CF MYCIN com Fraction`, `Testes com casos conhecidos por versao da base`?**
  _High betweenness centrality (0.143) - this node is a cross-community bridge._
- **What connects `Motor de regras em Python independente de interface`, `Criterios de avaliacao do hackathon`, `Cronograma e entrega do hackathon (20 a 23/10)` to the rest of the system?**
  _52 weakly-connected nodes found - possible documentation gaps or missing edges._
- **Should `Motor de inferência (engine/)` be split into smaller, more focused modules?**
  _Cohesion score 0.07039187227866474 - nodes in this community are weakly interconnected._
- **Why does `Alocacao de agente principal e alternativa por prompt de revisao` connect `Motor de inferência da seção 1` to `Limite da fase de planejamento (sem implementacao)`?**
  _High betweenness centrality (0.107) - this node is a cross-community bridge._
- **Should `Sessao: triagem, perguntas e correções` be split into smaller, more focused modules?**
  _Cohesion score 0.07816091954022988 - nodes in this community are weakly interconnected._

### Low-confidence Hints
_AMBIGUOUS edges — the extractor was unsure. Verify before acting on these._

- **What is the exact relationship between `Limites de uso dos planos` and `Gemini CLI`?**
  _Edge tagged AMBIGUOUS (relation: references) - confidence is low._
- **What is the exact relationship between `uv (sync, run, python pin)` and `Python 3.15.0`?**
  _Edge tagged AMBIGUOUS (relation: conceptually_related_to) - confidence is low._