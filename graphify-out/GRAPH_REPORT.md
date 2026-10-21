# Graph Report - HackAtom  (2026-10-21)

## Corpus Check
- Corpus is ~33,148 words - fits in a single context window. You may not need a graph.

## Summary
- 238 nodes · 319 edges · 23 communities (14 shown, 9 thin omitted)
- Extraction: 76% EXTRACTED · 24% INFERRED · 1% AMBIGUOUS · INFERRED: 76 edges (avg confidence: 0.82)
- Token cost: 520,209 input · 0 output

## Community Hubs (Navigation)
- Instruções e regras do hackathon
- Especificação: entrega e arquitetura
- Motor: CF, parada e bandeiras
- Execução local e ferramentas
- Domínio veterinário e suposições
- Planejamento, agentes e alocação
- Skills obra/superpowers
- Componentes do sistema especialista
- Revisão do motor e conformidade
- Interface, memória e lacunas da API
- Agentes e arquivos de instrução
- Skills Anthropic e licença
- Potencial e parada (implementação)
- Explicação e traço
- Bandeira após correção
- Dados fictícios e base de demonstração
- Playwright
- SQLite
- Agentes e skills por prompt
- Transcrição da apresentação [A]
- Transcrição do documentário [D]
- README do motor
- Função analisar()

## God Nodes (most connected - your core abstractions)
1. `Motor de inferência (engine/)` - 15 edges
2. `Especificação PoC Anamnese de Bovinos Leiteiros` - 13 edges
3. `Motor de inferencia` - 13 edges
4. `MSD Vet Manual` - 13 edges
5. `Motor de inferencia da secao 1 (pacote engine)` - 10 edges
6. `Base de conhecimento JSON versionada (kb/)` - 9 edges
7. `CLAUDE.md do projeto (PoC Anamnese de Bovinos Leiteiros)` - 9 edges
8. `Alocacao de agente principal e alternativa por prompt de revisao` - 9 edges
9. `Conhecimento de domínio: 8 doenças` - 8 edges
10. `obra/superpowers (repositorio de skills)` - 7 edges

## Surprising Connections (you probably didn't know these)
- `Cinco tarefas TDD do motor (vermelho antes do verde)` --semantically_similar_to--> `Testes com casos conhecidos por versao da base`  [INFERRED] [semantically similar]
  docs/superpowers/plans/2026-10-20-motor-secao-1.md → CLAUDE.md
- `Fraction evita arredondar conclusao quase certa` --semantically_similar_to--> `Decisao deterministica e auditavel`  [INFERRED] [semantically similar]
  engine/README.md → CLAUDE.md
- `Status de conferencia das fontes (L, R, N)` --semantically_similar_to--> `Marcacao de suposicao a validar (conhecimento veterinario)`  [INFERRED] [semantically similar]
  docs/fontes/fontes.md → CLAUDE.md
- `Motor de inferencia da secao 1 (pacote engine)` --references--> `Plano de implementacao do motor (secao 1)`  [EXTRACTED]
  engine/README.md → docs/superpowers/plans/2026-10-20-motor-secao-1.md
- `Executor de casos (engine.casos)` --implements--> `Testes com casos conhecidos por versao da base`  [INFERRED]
  engine/README.md → CLAUDE.md

## Import Cycles
- None detected.

## Hyperedges (group relationships)
- **Três camadas de avaliação de regras** — docs_superpowers_specs_2026_10_20_anamnese_bovinos_design_derivados_sinais, docs_superpowers_specs_2026_10_20_anamnese_bovinos_design_dominio_8_doencas, docs_superpowers_specs_2026_10_20_anamnese_bovinos_design_urgencia_gravidade_confianca, docs_superpowers_specs_2026_10_20_anamnese_bovinos_design_bandeiras_vermelhas, docs_superpowers_specs_2026_10_20_anamnese_bovinos_design_camadas_tres [EXTRACTED 1.00]
- **Pacotes api -> engine -> kb e web** — docs_superpowers_specs_2026_10_20_anamnese_bovinos_design_pacote_api, docs_superpowers_specs_2026_10_20_anamnese_bovinos_design_pacote_engine, docs_superpowers_specs_2026_10_20_anamnese_bovinos_design_pacote_kb, docs_superpowers_specs_2026_10_20_anamnese_bovinos_design_pacote_web [EXTRACTED 1.00]
- **Ciclo de edição e validação da base** — docs_superpowers_specs_2026_10_20_anamnese_bovinos_design_editor_grafico, docs_superpowers_specs_2026_10_20_anamnese_bovinos_design_validador_kb, docs_superpowers_specs_2026_10_20_anamnese_bovinos_design_versionamento_imutavel, docs_superpowers_specs_2026_10_20_anamnese_bovinos_design_casos_teste [EXTRACTED 1.00]
- **Modelo conceitual de sistema especialista (slide 14)** — claude_motor_de_inferencia, claude_base_conhecimento, claude_memoria_de_trabalho, claude_modulo_explicacao, claude_interface_usuario, claude_aquisicao_conhecimento, claude_fontes_dados_externas [EXTRACTED 1.00]
- **Componentes do motor de inferencia da secao 1** — engine_readme_inferir, engine_readme_analisar, engine_readme_parada, engine_readme_sessao_api, engine_readme_parecer, engine_readme_porque_como [INFERRED 0.85]
- **Divergencias e lacunas da revisao do motor (21/10/2026)** — docs_revisoes_2026_10_21_revisao_motor_bandeira_apos_correcao, docs_revisoes_2026_10_21_revisao_motor_percentual_parecer, docs_revisoes_2026_10_21_revisao_motor_restauracao_sessao, docs_revisoes_2026_10_21_revisao_motor_traco_sessao, docs_revisoes_2026_10_21_revisao_motor_executor_casos [EXTRACTED 1.00]
- **Pipeline de planejamento e execucao com skills (obra/superpowers)** — docs_pesquisa_agentes_e_skills_brainstorming, docs_pesquisa_agentes_e_skills_writing_plans, docs_pesquisa_agentes_e_skills_executing_plans, docs_pesquisa_agentes_e_skills_test_driven_development, docs_pesquisa_agentes_e_skills_subagent_driven_development [INFERRED 0.85]
- **Stack de execucao local em localhost** — docs_pesquisa_execucao_local_fastapi_frontend, docs_pesquisa_execucao_local_vite, docs_pesquisa_execucao_local_uv, docs_pesquisa_execucao_local_playwright_webserver, docs_pesquisa_versoes_bibliotecas_uvicorn [INFERRED 0.85]
- **Premissas de instalacao no Windows a validar** — docs_pesquisa_suposicoes_linha_24_node, docs_pesquisa_suposicoes_rodar_ps1, docs_pesquisa_suposicoes_winget_uv_id, docs_pesquisa_suposicoes_vite_mocks, docs_pesquisa_suposicoes_windows_11_demo, docs_pesquisa_execucao_local_powershell_execution_policy [INFERRED 0.75]

## Communities (23 total, 9 thin omitted)

### Community 0 - "Instruções e regras do hackathon"
Cohesion: 0.09
Nodes (24): CLAUDE.md do projeto (PoC Anamnese de Bovinos Leiteiros), Motor de regras em Python independente de interface, Criterios de avaliacao do hackathon, Cronograma e entrega do hackathon (20 a 23/10), Encadeamento para frente e para tras, Fatores de certeza (CF), Motor de inferencia, Resolucao de conflito (+16 more)

### Community 1 - "Especificação: entrega e arquitetura"
Cohesion: 0.13
Nodes (27): Apresentação e roteiro da demonstração, Base de conhecimento JSON versionada (kb/), Três camadas estritas (derivado, doença, urgência), Casos de teste conhecidos (31 casos), Contratos da API e formato único de erro, Cronograma por blocos até quinta 22/10, Decisões do arquiteto (4.9, 5.5, 6.4), Sinais derivados (camada 1) (+19 more)

### Community 2 - "Motor: CF, parada e bandeiras"
Cohesion: 0.12
Nodes (21): Bandeiras vermelhas (chamar_agora), Correções e recálculo dos fatos, Critérios de parada (confirmação, limite, exaustão), Explicação por quê? e como?, Fatos (variável, valor, CF) e avaliação de condições, Importação de prontuário CSV/JSON, Hipótese aberta, Limiares nomeados em meta.limiares (+13 more)

### Community 3 - "Execução local e ferramentas"
Cohesion: 0.11
Nodes (18): playwright-skill (lackeyjb), webapp-testing (skill), uv (sync, run, python pin), Vite (build e server.proxy), Linha 24 do Node.js (a confirmar), rodar.ps1 (script de execucao), VITE_USAR_MOCKS (modo dev), Demonstracao em Windows 11 (+10 more)

### Community 4 - "Domínio veterinário e suposições"
Cohesion: 0.13
Nodes (16): Conteudo obrigatorio do plano final (12 itens), Acidose ruminal (categoria), Acidose ruminal subaguda, Anaplasmose, Babesiose, Cetose bovina (hiperCetonemia), Dermatite digital, Deslocamento de abomaso (+8 more)

### Community 5 - "Planejamento, agentes e alocação"
Cohesion: 0.12
Nodes (15): Limite da fase de planejamento (sem implementacao), Skill superpowers:brainstorming, Skill superpowers:writing-plans, Alocacao de agente principal e alternativa por prompt de revisao, anthropics/skills (pptx, docx, pdf, webapp-testing, frontend-design), Antigravity (plano Pro), Claude Code (Claude Pro), Codex (ChatGPT Plus) (+7 more)

### Community 6 - "Skills obra/superpowers"
Cohesion: 0.16
Nodes (16): brainstorming (skill), executing-plans (skill), subagent-driven-development (skill), obra/superpowers (repositorio de skills), systematic-debugging (skill), test-driven-development (skill), verification-before-completion (skill), writing-plans (skill) (+8 more)

### Community 7 - "Componentes do sistema especialista"
Cohesion: 0.17
Nodes (12): Aquisicao de conhecimento, Base de conhecimento, Testes com casos conhecidos por versao da base, Editor grafico do fluxo da anamnese, FastAPI + Pydantic, pytest, React Flow, Skills nao confirmadas (FastAPI, pytest, React Flow, Vite) (+4 more)

### Community 8 - "Revisão do motor e conformidade"
Cohesion: 0.17
Nodes (12): Fontes de dados externas, Especificacao autorizada da secao 1 (docs/prompts/secao-1.md), Revisao do motor de inferencia (21/10/2026), Arvore da secao 4.3 da especificacao (sessao, validacao, modelos), Tabela de conformidade com a especificacao (16 itens), Ficha com null tratada como nao sei (deve ser ausente), Plano de implementacao do motor (secao 1), Evidencia final: 56 testes sem falhas (+4 more)

### Community 9 - "Interface, memória e lacunas da API"
Cohesion: 0.22
Nodes (9): Interface do usuario, Memoria de trabalho, Adaptacoes que a API precisa fazer sobre o motor, Cortes de bloco nao lidos de meta.limiares, Percentual do parecer max(0, CF) x 100 (divergencia), Restauracao da sessao a partir do banco (ausente, bloqueia a API), Modos produtor e veterinario, Parecer final em tres blocos (+1 more)

### Community 10 - "Agentes e arquivos de instrução"
Cohesion: 0.42
Nodes (9): AGENTS.md (instrucoes do projeto), Google Antigravity (app, IDE e CLI), Claude Code, CLAUDE.md (instrucoes do projeto), OpenAI Codex (CLI, IDE, app desktop), Gemini CLI, GEMINI.md (instrucoes do projeto), Limites de uso dos planos (+1 more)

### Community 11 - "Skills Anthropic e licença"
Cohesion: 0.25
Nodes (8): anthropics/skills (repositorio), frontend-design (skill), pptx (skill, source-available), Restricao de open source do hackathon, skill-creator (skill), React 19.3.1, reactflow 11.11.4 (legado, nao usar), @xyflow/react 12.12.0 (React Flow)

### Community 13 - "Explicação e traço"
Cohesion: 0.67
Nodes (4): Modulo de explicacao (por que e como), Traco de inferencia, Traco da sessao reacumula eventos (parcial), Explicacoes por que e como

### Community 14 - "Bandeira após correção"
Cohesion: 0.67
Nodes (3): Bandeira some apos correcao (divergencia), bandeiras_nao_verificadas restrito a regras viaveis e perguntaveis, Bandeira: alerta com pausa e encerramento

## Ambiguous Edges - Review These
- `Gemini CLI` → `Limites de uso dos planos`  [AMBIGUOUS]
  docs/pesquisa/agentes-e-skills.md · relation: references
- `uv (sync, run, python pin)` → `Python 3.15.0`  [AMBIGUOUS]
  docs/pesquisa/execucao-local.md · relation: conceptually_related_to

## Knowledge Gaps
- **45 isolated node(s):** `Fatos (variável, valor, CF) e avaliação de condições`, `Resolução de conflito (agenda)`, `Fontes de domínio F1 a F12`, `Persistência SQLite`, `Agentes e skills por prompt (decisao de 20/10/2026)` (+40 more)
  These have ≤1 connection - possible missing edges or undocumented components. (Counts symbols only; 59 node(s) total have ≤1 connection when file, concept and rationale nodes are included.)
- **9 thin communities (<3 nodes) omitted from report** — run `graphify query` to explore isolated nodes.

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **Why does `Motor de inferencia da secao 1 (pacote engine)` connect `Instruções e regras do hackathon` to `Revisão do motor e conformidade`, `Planejamento, agentes e alocação`, `Componentes do sistema especialista`?**
  _High betweenness centrality (0.114) - this node is a cross-community bridge._
- **Are the 2 inferred relationships involving `Motor de inferencia da secao 1 (pacote engine)` (e.g. with `Motor de regras em Python independente de interface` and `Motor de inferencia`) actually correct?**
  _`Motor de inferencia da secao 1 (pacote engine)` has 2 INFERRED edges - model-reasoned connections that need verification._
- **What connects `Fatos (variável, valor, CF) e avaliação de condições`, `Resolução de conflito (agenda)`, `Fontes de domínio F1 a F12` to the rest of the system?**
  _45 weakly-connected nodes found - possible documentation gaps or missing edges._
- **Should `Instruções e regras do hackathon` be split into smaller, more focused modules?**
  _Cohesion score 0.09032258064516129 - nodes in this community are weakly interconnected._
- **Why does `Motor de inferencia` connect `Instruções e regras do hackathon` to `Interface, memória e lacunas da API`, `Componentes do sistema especialista`?**
  _High betweenness centrality (0.112) - this node is a cross-community bridge._

### Low-confidence Hints
_AMBIGUOUS edges — the extractor was unsure. Verify before acting on these._

- **What is the exact relationship between `Gemini CLI` and `Limites de uso dos planos`?**
  _Edge tagged AMBIGUOUS (relation: references) - confidence is low._
- **What is the exact relationship between `uv (sync, run, python pin)` and `Python 3.15.0`?**
  _Edge tagged AMBIGUOUS (relation: conceptually_related_to) - confidence is low._