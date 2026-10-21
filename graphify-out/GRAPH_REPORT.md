# Graph Report - HackAtom  (2026-10-21)

## Corpus Check
- 2 files · ~37,407 words
- Verdict: corpus is large enough that graph structure adds value.

## Summary
- 299 nodes · 491 edges · 19 communities (12 shown, 7 thin omitted)
- Extraction: 77% EXTRACTED · 22% INFERRED · 1% AMBIGUOUS · INFERRED: 109 edges (avg confidence: 0.82)
- Token cost: 0 input · 0 output

## Community Hubs (Navigation)
- Instruções e regras do hackathon
- Especificação: entrega e arquitetura
- Pacote kb (Seção 2)
- Planejamento, agentes e alocação
- Execução local e ferramentas
- Domínio veterinário e suposições
- Instruções e regras do hackathon (2)
- Skills obra/superpowers
- Agentes e arquivos de instrução
- Potencial e parada (implementação)
- Bandeira após correção
- Interface, memória e lacunas da API
- Instruções e regras do hackathon (3)
- Pacote kb (Seção 2) (2)
- Agentes e skills por prompt
- Transcrição da apresentação [A]
- Transcrição do documentário [D]
- README do motor
- Função analisar()

## God Nodes (most connected - your core abstractions)
1. `CLAUDE.md do projeto (PoC Anamnese de Bovinos Leiteiros)` - 28 edges
2. `Motor de inferencia` - 16 edges
3. `Motor de inferência (engine/)` - 15 edges
4. `Conteudo obrigatorio do plano final (12 itens)` - 13 edges
5. `Especificação PoC Anamnese de Bovinos Leiteiros` - 13 edges
6. `MSD Vet Manual` - 13 edges
7. `Task 1: Ambiente e modelos Pydantic` - 13 edges
8. `Plano de implementação do kb (Seção 2)` - 11 edges
9. `Motor de inferencia da secao 1 (pacote engine)` - 10 edges
10. `Componentes da arquitetura (modelo conceitual)` - 10 edges

## Surprising Connections (you probably didn't know these)
- `Cinco tarefas TDD do motor (vermelho antes do verde)` --semantically_similar_to--> `Testes com casos conhecidos por versao da base`  [INFERRED] [semantically similar]
  docs/superpowers/plans/2026-10-20-motor-secao-1.md → CLAUDE.md
- `Fraction evita arredondar conclusao quase certa` --semantically_similar_to--> `Decisao deterministica e auditavel`  [INFERRED] [semantically similar]
  engine/README.md → CLAUDE.md
- `Status de conferencia das fontes (L, R, N)` --semantically_similar_to--> `Marcacao de suposicao a validar (conhecimento veterinario)`  [INFERRED] [semantically similar]
  docs/fontes/fontes.md → CLAUDE.md
- `Pydantic fixado em >=2.14,<2.15 (README)` --conceptually_related_to--> `Plano de implementação do kb (Seção 2)`  [AMBIGUOUS]
  kb/README.md → docs/superpowers/plans/2026-10-21-kb-secao-2.md
- `Aresta.ordem opcional e ordem por lista` --conceptually_related_to--> `Task 3: Conversão base-grafo`  [AMBIGUOUS]
  kb/README.md → docs/superpowers/plans/2026-10-21-kb-secao-2.md

## Import Cycles
- None detected.

## Hyperedges (group relationships)
- **Pacotes api -> engine -> kb e web** — docs_superpowers_specs_2026_10_20_anamnese_bovinos_design_pacote_api, docs_superpowers_specs_2026_10_20_anamnese_bovinos_design_pacote_engine, docs_superpowers_specs_2026_10_20_anamnese_bovinos_design_pacote_kb, docs_superpowers_specs_2026_10_20_anamnese_bovinos_design_pacote_web [EXTRACTED 1.00]
- **Ciclo de edição e validação da base** — docs_superpowers_specs_2026_10_20_anamnese_bovinos_design_editor_grafico, docs_superpowers_specs_2026_10_20_anamnese_bovinos_design_validador_kb, docs_superpowers_specs_2026_10_20_anamnese_bovinos_design_versionamento_imutavel, docs_superpowers_specs_2026_10_20_anamnese_bovinos_design_casos_teste [EXTRACTED 1.00]
- **Divergencias e lacunas da revisao do motor (21/10/2026)** — docs_revisoes_2026_10_21_revisao_motor_bandeira_apos_correcao, docs_revisoes_2026_10_21_revisao_motor_percentual_parecer, docs_revisoes_2026_10_21_revisao_motor_restauracao_sessao, docs_revisoes_2026_10_21_revisao_motor_traco_sessao, docs_revisoes_2026_10_21_revisao_motor_executor_casos [EXTRACTED 1.00]
- **Fluxo de manutencao do grafo de conhecimento** — claude_grafo_conhecimento, claude_manter_grafo_atualizado, claude_graphify_update, claude_obsidian_vault_conhecimento, claude_graph_report [EXTRACTED 1.00]
- **Modelo conceitual de sistema especialista (slide 14)** — claude_motor_de_inferencia, claude_base_conhecimento, claude_memoria_de_trabalho, claude_modulo_explicacao, claude_interface_usuario, claude_aquisicao_conhecimento, claude_fontes_dados_externas [EXTRACTED 1.00]
- **Restricoes obrigatorias do desafio** — claude_restricao_nao_usar_llm, claude_restricao_decisao_deterministica, claude_restricao_open_source, claude_restricao_localhost [EXTRACTED 1.00]
- **Três camadas de avaliação de regras** — docs_superpowers_specs_2026_10_20_anamnese_bovinos_design_derivados_sinais, docs_superpowers_specs_2026_10_20_anamnese_bovinos_design_dominio_8_doencas, docs_superpowers_specs_2026_10_20_anamnese_bovinos_design_urgencia_gravidade_confianca, docs_superpowers_specs_2026_10_20_anamnese_bovinos_design_bandeiras_vermelhas, docs_superpowers_specs_2026_10_20_anamnese_bovinos_design_camadas_tres [EXTRACTED 1.00]
- **Compatibilidade kb-motor** — kb_readme_para_motor, kb_readme_engine, kb_readme_div_exclude_none, kb_readme_div_prioridade, kb_readme_test_integracao [INFERRED 0.75]
- **Premissas de instalacao no Windows a validar** — docs_pesquisa_suposicoes_linha_24_node, docs_pesquisa_suposicoes_rodar_ps1, docs_pesquisa_suposicoes_winget_uv_id, docs_pesquisa_suposicoes_vite_mocks, docs_pesquisa_suposicoes_windows_11_demo, docs_pesquisa_execucao_local_powershell_execution_policy [INFERRED 0.75]
- **Versionamento imutável com validação prévia** — kb_readme_carregador, docs_superpowers_plans_2026_10_21_kb_secao_2_task5_carregador, kb_readme_validador, kb_readme_lf_sha256 [INFERRED 0.75]
- **Componentes do motor de inferencia** — claude_motor_de_inferencia, claude_encadeamento, claude_resolucao_conflito, claude_fatores_certeza, claude_traco_inferencia, claude_modulo_explicacao [INFERRED 0.85]
- **Componentes do motor de inferencia da secao 1** — engine_readme_inferir, engine_readme_analisar, engine_readme_parada, engine_readme_sessao_api, engine_readme_parecer, engine_readme_porque_como [INFERRED 0.85]
- **Pipeline de planejamento e execucao com skills (obra/superpowers)** — docs_pesquisa_agentes_e_skills_brainstorming, docs_pesquisa_agentes_e_skills_writing_plans, docs_pesquisa_agentes_e_skills_executing_plans, docs_pesquisa_agentes_e_skills_test_driven_development, docs_pesquisa_agentes_e_skills_subagent_driven_development [INFERRED 0.85]
- **Pipeline de validação da base** — kb_readme_validador, kb_readme_analise, kb_readme_codigos, docs_superpowers_plans_2026_10_21_kb_secao_2_task4_validador, docs_superpowers_plans_2026_10_21_kb_secao_2_tabela_codigos [INFERRED 0.85]
- **Stack de execucao local em localhost** — docs_pesquisa_execucao_local_fastapi_frontend, docs_pesquisa_execucao_local_vite, docs_pesquisa_execucao_local_uv, docs_pesquisa_execucao_local_playwright_webserver, docs_pesquisa_versoes_bibliotecas_uvicorn [INFERRED 0.85]

## Communities (19 total, 7 thin omitted)

### Community 0 - "Instruções e regras do hackathon"
Cohesion: 0.08
Nodes (49): CLAUDE.md do projeto (PoC Anamnese de Bovinos Leiteiros), Aquisicao de conhecimento, Base de conhecimento, Testes com casos conhecidos por versao da base, Componentes da arquitetura (modelo conceitual), Conteudo obrigatorio do plano final (12 itens), Criterios de avaliacao do hackathon, Cronograma e entrega do hackathon (20 a 23/10) (+41 more)

### Community 1 - "Especificação: entrega e arquitetura"
Cohesion: 0.07
Nodes (48): Apresentação e roteiro da demonstração, Bandeiras vermelhas (chamar_agora), Base de conhecimento JSON versionada (kb/), Três camadas estritas (derivado, doença, urgência), Casos de teste conhecidos (31 casos), Contratos da API e formato único de erro, Correções e recálculo dos fatos, Critérios de parada (confirmação, limite, exaustão) (+40 more)

### Community 2 - "Pacote kb (Seção 2)"
Cohesion: 0.09
Nodes (33): Caso de teste da base (entrada e resultado esperado), Dependências entre símbolos, ciclo e ordem topológica, Plano de implementação do kb (Seção 2), Regra de produção (condições, conclusão, CF), Revisão do motor (docs/revisoes/2026-10-21-revisao-motor.md), Símbolo (variável da base), Especificação de anamnese (docs/superpowers/specs, Seção 2 e 5.1), Tabela de códigos do validador (E01-E19, W01-W03) (+25 more)

### Community 3 - "Planejamento, agentes e alocação"
Cohesion: 0.08
Nodes (24): Motor de regras em Python independente de interface, Alocacao de agente principal e alternativa por prompt de revisao, anthropics/skills (pptx, docx, pdf, webapp-testing, frontend-design), Antigravity (plano Pro), Claude Code (Claude Pro), Codex (ChatGPT Plus), Gemini Pro (Google AI Pro, app web), Implementacao por pessoa (A, B, C) com agente principal e reserva (+16 more)

### Community 4 - "Execução local e ferramentas"
Cohesion: 0.08
Nodes (26): anthropics/skills (repositorio), frontend-design (skill), playwright-skill (lackeyjb), pptx (skill, source-available), Restricao de open source do hackathon, skill-creator (skill), webapp-testing (skill), uv (sync, run, python pin) (+18 more)

### Community 5 - "Domínio veterinário e suposições"
Cohesion: 0.11
Nodes (16): Acidose ruminal (categoria), Acidose ruminal subaguda, Anaplasmose, Babesiose, Cetose bovina (hiperCetonemia), Dermatite digital, Deslocamento de abomaso, Embrapa ADM158 (tristeza parasitaria) (+8 more)

### Community 6 - "Instruções e regras do hackathon (2)"
Cohesion: 0.15
Nodes (17): Encadeamento para frente e para tras, Limite da fase de planejamento (sem implementacao), Grafo de conhecimento — ler PRIMEIRO, em todo prompt, graphify-out/GRAPH_REPORT.md (indice do grafo), graphify query, graphify --update, .graphifyignore (escopo do grafo), Manter o grafo atualizado (+9 more)

### Community 7 - "Skills obra/superpowers"
Cohesion: 0.16
Nodes (16): brainstorming (skill), executing-plans (skill), subagent-driven-development (skill), obra/superpowers (repositorio de skills), systematic-debugging (skill), test-driven-development (skill), verification-before-completion (skill), writing-plans (skill) (+8 more)

### Community 8 - "Agentes e arquivos de instrução"
Cohesion: 0.42
Nodes (9): AGENTS.md (instrucoes do projeto), Google Antigravity (app, IDE e CLI), Claude Code, CLAUDE.md (instrucoes do projeto), OpenAI Codex (CLI, IDE, app desktop), Gemini CLI, GEMINI.md (instrucoes do projeto), Limites de uso dos planos (+1 more)

### Community 10 - "Bandeira após correção"
Cohesion: 0.67
Nodes (3): Bandeira some apos correcao (divergencia), bandeiras_nao_verificadas restrito a regras viaveis e perguntaveis, Bandeira: alerta com pausa e encerramento

### Community 11 - "Interface, memória e lacunas da API"
Cohesion: 0.67
Nodes (3): Cortes de bloco nao lidos de meta.limiares, Percentual do parecer max(0, CF) x 100 (divergencia), Parecer final em tres blocos

### Community 12 - "Instruções e regras do hackathon (3)"
Cohesion: 0.67
Nodes (3): Resolucao de conflito, Prioridade padrao por classe (100/50/10) e demais correcoes menores, Agenda em camadas (prioridade, especificidade, id)

## Ambiguous Edges - Review These
- `uv (sync, run, python pin)` → `Python 3.15.0`  [AMBIGUOUS]
  docs/pesquisa/execucao-local.md · relation: conceptually_related_to
- `Limites de uso dos planos` → `Gemini CLI`  [AMBIGUOUS]
  docs/pesquisa/agentes-e-skills.md · relation: references
- `Plano de implementação do kb (Seção 2)` → `Pydantic fixado em >=2.14,<2.15 (README)`  [AMBIGUOUS]
  kb/README.md · relation: conceptually_related_to
- `Task 3: Conversão base-grafo` → `Aresta.ordem opcional e ordem por lista`  [AMBIGUOUS]
  kb/README.md · relation: conceptually_related_to
- `Task 4: Validador` → `Função validar_edicao`  [AMBIGUOUS]
  kb/README.md · relation: conceptually_related_to

## Knowledge Gaps
- **50 isolated node(s):** `Skills em formato aberto (.agents/skills, .claude/skills, AGENTS.md)`, `Prioridade padrao por classe (100/50/10) e demais correcoes menores`, `Executor de casos incompleto (inconclusivas e pausa)`, `Guardas de validacao do nucleo`, `Nucleo inferir(base, fatos), sem estado` (+45 more)
  These have ≤1 connection - possible missing edges or undocumented components. (Counts symbols only; 66 node(s) total have ≤1 connection when file, concept and rationale nodes are included.)
- **7 thin communities (<3 nodes) omitted from report** — run `graphify query` to explore isolated nodes.

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **Why does `Motor de inferencia` connect `Instruções e regras do hackathon` to `Planejamento, agentes e alocação`, `Instruções e regras do hackathon (3)`, `Instruções e regras do hackathon (2)`?**
  _High betweenness centrality (0.062) - this node is a cross-community bridge._
- **Are the 3 inferred relationships involving `Motor de inferencia` (e.g. with `Memoria de trabalho` and `Sistema especialista`) actually correct?**
  _`Motor de inferencia` has 3 INFERRED edges - model-reasoned connections that need verification._
- **What connects `Skills em formato aberto (.agents/skills, .claude/skills, AGENTS.md)`, `Prioridade padrao por classe (100/50/10) e demais correcoes menores`, `Executor de casos incompleto (inconclusivas e pausa)` to the rest of the system?**
  _50 weakly-connected nodes found - possible documentation gaps or missing edges._
- **Should `Instruções e regras do hackathon` be split into smaller, more focused modules?**
  _Cohesion score 0.07922077922077922 - nodes in this community are weakly interconnected._
- **Why does `Conteudo obrigatorio do plano final (12 itens)` connect `Instruções e regras do hackathon` to `Domínio veterinário e suposições`, `Instruções e regras do hackathon (2)`?**
  _High betweenness centrality (0.053) - this node is a cross-community bridge._

### Low-confidence Hints
_AMBIGUOUS edges — the extractor was unsure. Verify before acting on these._

- **What is the exact relationship between `uv (sync, run, python pin)` and `Python 3.15.0`?**
  _Edge tagged AMBIGUOUS (relation: conceptually_related_to) - confidence is low._
- **What is the exact relationship between `Limites de uso dos planos` and `Gemini CLI`?**
  _Edge tagged AMBIGUOUS (relation: references) - confidence is low._