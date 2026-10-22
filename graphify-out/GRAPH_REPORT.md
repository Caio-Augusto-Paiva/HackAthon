# Graph Report - HackAtom  (2026-10-21)

## Corpus Check
- 19 files · ~49,614 words
- Verdict: corpus is large enough that graph structure adds value.

## Summary
- 455 nodes · 735 edges · 35 communities (20 shown, 15 thin omitted)
- Extraction: 84% EXTRACTED · 16% INFERRED · 1% AMBIGUOUS · INFERRED: 115 edges (avg confidence: 0.81)
- Token cost: 0 input · 0 output

## Community Hubs (Navigation)
- Instruções e regras do hackathon
- Especificação: entrega e arquitetura
- Serviços e infraestrutura da API
- README da API e decisões
- Versões da base, casos e execução local
- Skills anthropics e open source
- Domínio veterinário e suposições
- Skills superpowers
- Validador: achados e casos inválidos
- Agentes e alocação por pessoa
- Ambiente e motor (testes)
- Contrato da API (OpenAPI e exemplos)
- Agentes e arquivos de instrução
- Plano do kb e carregar_base
- para_motor e revisão final do kb
- Notas da API para o frontend
- Grafo do kb e ciclos
- Gravação e ativação de versões
- Condicao.valor e E03
- Módulos do kb
- E14 derivado max
- E02 e E21 da triagem
- Branch de trabalho
- Bandeira após correção
- Limiares e combinação MYCIN
- Agentes e skills por prompt
- Transcrição da apresentação [A]
- Transcrição do documentário [D]
- Adaptações da API sobre o motor
- bandeiras_nao_verificadas
- Prioridade padrão por classe
- Executor de casos

## God Nodes (most connected - your core abstractions)
1. `CLAUDE.md do projeto (PoC Anamnese de Bovinos Leiteiros)` - 28 edges
2. `Plano de implementação API (Seção 4)` - 20 edges
3. `Task 1` - 17 edges
4. `Motor de inferencia` - 15 edges
5. `Motor de inferência (engine/)` - 15 edges
6. `Conteudo obrigatorio do plano final (12 itens)` - 13 edges
7. `Especificação PoC Anamnese de Bovinos Leiteiros` - 13 edges
8. `MSD Vet Manual` - 13 edges
9. `Task 5: Criar sessão e EstadoSessao` - 13 edges
10. `Task 1: Ambiente e modelos Pydantic` - 12 edges

## Surprising Connections (you probably didn't know these)
- `Cinco tarefas TDD do motor (vermelho antes do verde)` --semantically_similar_to--> `Testes com casos conhecidos por versao da base`  [INFERRED] [semantically similar]
  docs/superpowers/plans/2026-10-20-motor-secao-1.md → CLAUDE.md
- `Status de conferencia das fontes (L, R, N)` --semantically_similar_to--> `Marcacao de suposicao a validar (conhecimento veterinario)`  [INFERRED] [semantically similar]
  docs/fontes/fontes.md → CLAUDE.md
- `Decisao deterministica, sem LLM nem rede no caminho` --semantically_similar_to--> `Motor independente de web, banco, LLM e servicos externos`  [INFERRED] [semantically similar]
  api/README.md → engine/README.md
- `Motor independente de web, banco, LLM e servicos externos` --semantically_similar_to--> `kb como pacote folha (nao importa engine)`  [INFERRED] [semantically similar]
  engine/README.md → kb/README.md
- `Sementes de animais ficticios e reset seguro do banco` --conceptually_related_to--> `kb/validador.py (validar, validar_dados, validar_edicao, Relatorio)`  [INFERRED]
  api/README.md → kb/README.md

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
- **Premissas de instalacao no Windows a validar** — docs_pesquisa_suposicoes_linha_24_node, docs_pesquisa_suposicoes_rodar_ps1, docs_pesquisa_suposicoes_winget_uv_id, docs_pesquisa_suposicoes_vite_mocks, docs_pesquisa_suposicoes_windows_11_demo, docs_pesquisa_execucao_local_powershell_execution_policy [INFERRED 0.75]
- **Versionamento imutável com validação prévia** — docs_superpowers_plans_2026_10_21_kb_secao_2_task5_carregador, kb_readme_validador [INFERRED 0.75]
- **Ambiente e portabilidade do kb e do motor** — docs_revisoes_2026_10_21_ledger_kb_secao_2_ambiente_venv_python_3_12, docs_revisoes_2026_10_21_ledger_kb_secao_2_comando_de_teste_do_motor_com_python_do_sistema, docs_revisoes_2026_10_21_ledger_kb_secao_2_gitattributes_eol_lf [INFERRED 0.85]
- **Componentes do motor de inferencia** — claude_motor_de_inferencia, claude_encadeamento, claude_resolucao_conflito, claude_fatores_certeza, claude_traco_inferencia, claude_modulo_explicacao [INFERRED 0.85]
- **Decisoes de processo da Secao 2** — docs_revisoes_2026_10_21_ledger_kb_secao_2_execucao_sequencial_das_tarefas, docs_revisoes_2026_10_21_ledger_kb_secao_2_sem_worktree_no_branch, docs_revisoes_2026_10_21_ledger_kb_secao_2_casos_invalidos_como_mutacoes_pytest, docs_revisoes_2026_10_21_ledger_kb_secao_2_modulos_do_kb_implementados_aqui [INFERRED 0.85]
- **Pipeline de planejamento e execucao com skills (obra/superpowers)** — docs_pesquisa_agentes_e_skills_brainstorming, docs_pesquisa_agentes_e_skills_writing_plans, docs_pesquisa_agentes_e_skills_executing_plans, docs_pesquisa_agentes_e_skills_test_driven_development, docs_pesquisa_agentes_e_skills_subagent_driven_development [INFERRED 0.85]
- **Stack de execucao local em localhost** — docs_pesquisa_execucao_local_fastapi_frontend, docs_pesquisa_execucao_local_vite, docs_pesquisa_execucao_local_uv, docs_pesquisa_execucao_local_playwright_webserver, docs_pesquisa_versoes_bibliotecas_uvicorn [INFERRED 0.85]
- **Regras do validador e codigos de erro** — docs_revisoes_2026_10_21_ledger_kb_secao_2_formato_de_id_gera_e20, docs_revisoes_2026_10_21_ledger_kb_secao_2_valor_none_gera_e03, docs_revisoes_2026_10_21_ledger_kb_secao_2_e08_so_sem_condicao_de_triagem, docs_revisoes_2026_10_21_ledger_kb_secao_2_e15_cf_min_e_max_juntos, docs_revisoes_2026_10_21_ledger_kb_secao_2_e16_exige_texto_nos_dois_modos, docs_revisoes_2026_10_21_ledger_kb_secao_2_e17_estrito_com_pivo_zero, docs_revisoes_2026_10_21_ledger_kb_secao_2_e14_cobre_max_fora_de_derivado, docs_revisoes_2026_10_21_ledger_kb_secao_2_novo_e21_tela_simbolo_invalido [INFERRED 0.85]
- **Camadas da API: rotas finas, serviços, repositórios** — docs_superpowers_plans_2026_10_21_api_secao_4_arquitetura_casca_fina, docs_superpowers_plans_2026_10_21_api_secao_4_sessao_servico, docs_superpowers_plans_2026_10_21_api_secao_4_repositorios, docs_superpowers_plans_2026_10_21_api_secao_4_contexto [EXTRACTED 1.00]
- **Reconstrução da sessão a cada requisição via snapshot** — docs_superpowers_plans_2026_10_21_api_secao_4_motor_sem_estado, docs_superpowers_plans_2026_10_21_api_secao_4_snapshot_json, docs_superpowers_plans_2026_10_21_api_secao_4_sessao_motor, docs_superpowers_plans_2026_10_21_api_secao_4_montar_estado, docs_superpowers_plans_2026_10_21_api_secao_4_d2 [EXTRACTED 1.00]
- **Congelamento do contrato da API** — docs_superpowers_plans_2026_10_21_api_secao_4_registro_contratos, docs_superpowers_plans_2026_10_21_api_secao_4_exemplos_contrato, docs_superpowers_plans_2026_10_21_api_secao_4_openapi_json, docs_superpowers_plans_2026_10_21_api_secao_4_exportar_openapi, docs_superpowers_plans_2026_10_21_api_secao_4_d6 [EXTRACTED 1.00]
- **Camadas api -> engine -> kb (dependencia unidirecional)** — api_readme_backend_fastapi_sqlite, engine_readme_sessao, kb_readme_modelos, kb_readme_para_motor [EXTRACTED 1.00]
- **Persistencia e restauracao de sessao sem replay** — api_readme_d1_snapshot_json, api_readme_ordem_respostas, engine_readme_restaurar_exportar, engine_readme_correcao_reprocessa_lotes [EXTRACTED 1.00]
- **Ciclo de versao da base: validar, salvar, executar casos, ativar** — kb_readme_validador, kb_readme_carregador_repositorio, engine_readme_executar_caso, api_readme_portao_ativacao, api_readme_comparacao_versao_pai [INFERRED 0.85]

## Communities (35 total, 15 thin omitted)

### Community 0 - "Instruções e regras do hackathon"
Cohesion: 0.07
Nodes (60): CLAUDE.md do projeto (PoC Anamnese de Bovinos Leiteiros), Aquisicao de conhecimento, Motor de regras em Python independente de interface, Base de conhecimento, Testes com casos conhecidos por versao da base, Componentes da arquitetura (modelo conceitual), Conteudo obrigatorio do plano final (12 itens), Criterios de avaliacao do hackathon (+52 more)

### Community 1 - "Especificação: entrega e arquitetura"
Cohesion: 0.07
Nodes (48): Apresentação e roteiro da demonstração, Bandeiras vermelhas (chamar_agora), Base de conhecimento JSON versionada (kb/), Três camadas estritas (derivado, doença, urgência), Casos de teste conhecidos (31 casos), Contratos da API e formato único de erro, Correções e recálculo dos fatos, Critérios de parada (confirmação, limite, exaustão) (+40 more)

### Community 2 - "Serviços e infraestrutura da API"
Cohesion: 0.08
Nodes (41): Bandeira vermelha e pausa de alerta, base_servico.py, casos_servico.py, Configuracao (api/config.py), Contexto e obter_contexto, criar_app / main.py, Pacote engine (motor), ErroApi e fábricas de erro (+33 more)

### Community 3 - "README da API e decisões"
Cohesion: 0.06
Nodes (33): API README (api/), Backend FastAPI + SQLite (casca fina sobre motor e kb), Concorrencia: BEGIN IMMEDIATE e conferencia de revisao, Host confiavel (TrustedHostMiddleware contra DNS rebinding), Importacao de animais CSV/JSON sem 500, ordem_respostas no snapshot (reprocessar lotes na correcao), Especificacao autorizada da secao 1 (docs/prompts/secao-1.md), Revisao do motor de inferencia (21/10/2026) (+25 more)

### Community 4 - "Versões da base, casos e execução local"
Cohesion: 0.08
Nodes (33): Comparacao de casos com a versao pai, Portao de ativacao de versao (casos_falhando, confirmar_falhas), Script rodar.ps1 / rodar.sh (execucao em localhost), Sementes de animais ficticios e reset seguro do banco, Servir web/dist com rota coringa propria (api/frontend.py), Sessao presa a versao da base com que nasceu, Variaveis ANAMNESE_BASE_DIR e ANAMNESE_DB, Caso de teste da base (entrada e resultado esperado) (+25 more)

### Community 5 - "Skills anthropics e open source"
Cohesion: 0.08
Nodes (26): anthropics/skills (repositorio), frontend-design (skill), playwright-skill (lackeyjb), pptx (skill, source-available), Restricao de open source do hackathon, skill-creator (skill), webapp-testing (skill), uv (sync, run, python pin) (+18 more)

### Community 6 - "Domínio veterinário e suposições"
Cohesion: 0.13
Nodes (15): Acidose ruminal (categoria), Acidose ruminal subaguda, Anaplasmose, Babesiose, Cetose bovina (hiperCetonemia), Dermatite digital, Deslocamento de abomaso, Embrapa ADM158 (tristeza parasitaria) (+7 more)

### Community 7 - "Skills superpowers"
Cohesion: 0.16
Nodes (16): brainstorming (skill), executing-plans (skill), subagent-driven-development (skill), obra/superpowers (repositorio de skills), systematic-debugging (skill), test-driven-development (skill), verification-before-completion (skill), writing-plans (skill) (+8 more)

### Community 8 - "Validador: achados e casos inválidos"
Cohesion: 0.13
Nodes (11): Achado E06 doenca sem regra, Arquivos kb_invalidas Secao 5.1, E08 bandeira sem triagem, E11 criterio de triagem, E15 cf_minimo e cf_maximo, E16 texto da tela de triagem, E17 ordem de limiares, E20 id_invalido (+3 more)

### Community 9 - "Agentes e alocação por pessoa"
Cohesion: 0.16
Nodes (10): Alocacao de agente principal e alternativa por prompt de revisao, anthropics/skills (pptx, docx, pdf, webapp-testing, frontend-design), Antigravity (plano Pro), Claude Code (Claude Pro), Codex (ChatGPT Plus), Gemini Pro (Google AI Pro, app web), Implementacao por pessoa (A, B, C) com agente principal e reserva, Fontes do projeto (fontes oficiais e de dominio) (+2 more)

### Community 10 - "Ambiente e motor (testes)"
Cohesion: 0.23
Nodes (10): Achado fato numerico inerte no teste, Ambiente venv, engine.modelos.Base.de_dict, .gitattributes, Pacote engine, SDD ledger, Spec anamnese bovinos, Task 6 (+2 more)

### Community 11 - "Contrato da API (OpenAPI e exemplos)"
Cohesion: 0.29
Nodes (9): 27 endpoints da Seção 4.5, contratos/exemplos (27 exemplos), api/exportar_openapi.py, contratos/openapi.json versionado, operationId estável por rota, registro.py CONTRATOS por operationId, Schemas Pydantic (sessao, parecer, explicacao, animal, base), Task 3: Schemas Pydantic e exemplos de contrato (+1 more)

### Community 12 - "Agentes e arquivos de instrução"
Cohesion: 0.42
Nodes (9): AGENTS.md (instrucoes do projeto), Google Antigravity (app, IDE e CLI), Claude Code, CLAUDE.md (instrucoes do projeto), OpenAI Codex (CLI, IDE, app desktop), Gemini CLI, GEMINI.md (instrucoes do projeto), Limites de uso dos planos (+1 more)

### Community 13 - "Plano do kb e carregar_base"
Cohesion: 0.28
Nodes (7): Achado carregar_base excecoes nativas, Achado prioridade zero no teste, carregar_base, Plano kb secao 2, pyproject.toml, Task 1, tests/kb/test_modelos.py

### Community 14 - "para_motor e revisão final do kb"
Cohesion: 0.28
Nodes (7): Achado kb aceita base invalida, Achado ordem ausente no contrato, Aresta.ordem, kb/__init__.py, para_motor, Revisao final, validar_edicao

### Community 15 - "Notas da API para o frontend"
Cohesion: 0.25
Nodes (6): API sobe sem a base (409 conflito em vez de 500), Contrato OpenAPI versionado e exemplos por operationId, Formato unico de erro (codigos e X-Requisicao-Id), Notas para o frontend (proxima nulo, reabrir, 409 conflito), Mapa de 27 rotas por arquivo (prefixo /api), Testes da API (pytest, marca lento, base minima de fixtures)

### Community 16 - "Grafo do kb e ciclos"
Cohesion: 0.43
Nodes (6): Achado direcao do caminho do ciclo, Achado op e negado None viram default, encontrar_ciclo, kb/grafo.py, Task 2, Task 3

### Community 17 - "Gravação e ativação de versões"
Cohesion: 0.53
Nodes (5): Achado temporario fixo ativa.json.tmp, Achado pai explicito nao verificado, ativa.json, salvar_nova, Task 5

### Community 18 - "Condicao.valor e E03"
Cohesion: 0.40
Nodes (4): Achado Condicao valor int, Condicao.valor, E03 valor_invalido, model_fields_set da Aresta

### Community 19 - "Módulos do kb"
Cohesion: 0.33
Nodes (4): kb/analise.py, kb/carregador.py, kb/modelos.py, LimiteDinamico

## Ambiguous Edges - Review These
- `uv (sync, run, python pin)` → `Python 3.15.0`  [AMBIGUOUS]
  docs/pesquisa/execucao-local.md · relation: conceptually_related_to
- `Limites de uso dos planos` → `Gemini CLI`  [AMBIGUOUS]
  docs/pesquisa/agentes-e-skills.md · relation: references
- `Task 1` → `kb/__init__.py`  [AMBIGUOUS]
  docs/revisoes/2026-10-21-ledger-kb-secao-2.md · relation: references
- `Achado temporario fixo ativa.json.tmp` → `Escrita interrompida apaga arquivo novo`  [AMBIGUOUS]
  docs/revisoes/2026-10-21-ledger-kb-secao-2.md · relation: conceptually_related_to
- `Achado kb aceita base invalida` → `E14 cobre max fora de derivado`  [AMBIGUOUS]
  docs/revisoes/2026-10-21-ledger-kb-secao-2.md · relation: rationale_for

## Knowledge Gaps
- **82 isolated node(s):** `graphify --update`, `.graphifyignore (escopo do grafo)`, `Skills em formato aberto (.agents/skills, .claude/skills, AGENTS.md)`, `Executor de casos incompleto (inconclusivas e pausa)`, `Traco da sessao reacumula eventos (parcial)` (+77 more)
  These have ≤1 connection - possible missing edges or undocumented components. (Counts symbols only; 107 node(s) total have ≤1 connection when file, concept and rationale nodes are included.)
- **15 thin communities (<3 nodes) omitted from report** — run `graphify query` to explore isolated nodes.

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **Why does `Conteudo obrigatorio do plano final (12 itens)` connect `Instruções e regras do hackathon` to `Domínio veterinário e suposições`?**
  _High betweenness centrality (0.015) - this node is a cross-community bridge._
- **Are the 2 inferred relationships involving `Motor de inferencia` (e.g. with `Memoria de trabalho` and `Sistema especialista`) actually correct?**
  _`Motor de inferencia` has 2 INFERRED edges - model-reasoned connections that need verification._
- **What connects `graphify --update`, `.graphifyignore (escopo do grafo)`, `Skills em formato aberto (.agents/skills, .claude/skills, AGENTS.md)` to the rest of the system?**
  _82 weakly-connected nodes found - possible documentation gaps or missing edges._
- **Should `Instruções e regras do hackathon` be split into smaller, more focused modules?**
  _Cohesion score 0.06971153846153846 - nodes in this community are weakly interconnected._
- **Should `Especificação: entrega e arquitetura` be split into smaller, more focused modules?**
  _Cohesion score 0.07039187227866474 - nodes in this community are weakly interconnected._

### Low-confidence Hints
_AMBIGUOUS edges — the extractor was unsure. Verify before acting on these._

- **What is the exact relationship between `uv (sync, run, python pin)` and `Python 3.15.0`?**
  _Edge tagged AMBIGUOUS (relation: conceptually_related_to) - confidence is low._
- **What is the exact relationship between `Limites de uso dos planos` and `Gemini CLI`?**
  _Edge tagged AMBIGUOUS (relation: references) - confidence is low._