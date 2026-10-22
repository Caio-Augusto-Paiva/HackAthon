# Graph Report - HackAtom  (2026-10-21)

## Corpus Check
- 37 files · ~69,571 words
- Verdict: corpus is large enough that graph structure adds value.
- Unclassified: 3 file(s) not represented in the graph (top: (none) 3)

## Summary
- 518 nodes · 880 edges · 34 communities (19 shown, 15 thin omitted)
- Extraction: 86% EXTRACTED · 13% INFERRED · 1% AMBIGUOUS · INFERRED: 117 edges (avg confidence: 0.81)
- Token cost: 0 input · 0 output

## Community Hubs (Navigation)
- [[_COMMUNITY_CLAUDE.md do projeto (PoC Anamnese de Bovinos Leiteiros)|CLAUDE.md do projeto (PoC Anamnese de Bovinos Leiteiros)]]
- [[_COMMUNITY_Checkpoint codex-davi Arquitetura disponível CLIPython, JSON, sessão, inferência e explicação|Checkpoint codex-davi: Arquitetura disponível: CLI/Python, JSON, sessão, inferência e explicação]]
- [[_COMMUNITY_Plano de implementação API (Seção 4)|Plano de implementação API (Seção 4)]]
- [[_COMMUNITY_Motor de inferência (engine)|Motor de inferência (engine/)]]
- [[_COMMUNITY_obrasuperpowers (repositorio de skills)|obra/superpowers (repositorio de skills)]]
- [[_COMMUNITY_Classe Sessao (dialogo, estado, correcao, modo)|Classe Sessao (dialogo, estado, correcao, modo)]]
- [[_COMMUNITY_Task 1 Ambiente e modelos Pydantic|Task 1: Ambiente e modelos Pydantic]]
- [[_COMMUNITY_MSD Vet Manual|MSD Vet Manual]]
- [[_COMMUNITY_validar|validar]]
- [[_COMMUNITY_Alocacao de agente principal e alternativa por prompt de revisao|Alocacao de agente principal e alternativa por prompt de revisao]]
- [[_COMMUNITY_SDD ledger|SDD ledger]]
- [[_COMMUNITY_Google Antigravity (app, IDE e CLI)|Google Antigravity (app, IDE e CLI)]]
- [[_COMMUNITY_Task 1|Task 1]]
- [[_COMMUNITY_Rodada unica de correcao final|Rodada unica de correcao final]]
- [[_COMMUNITY_Contrato OpenAPI versionado e exemplos por operationId|Contrato OpenAPI versionado e exemplos por operationId]]
- [[_COMMUNITY_Task 2|Task 2]]
- [[_COMMUNITY_Task 5|Task 5]]
- [[_COMMUNITY_Condicao.valor|Condicao.valor]]
- [[_COMMUNITY_kbmodelos.py|kb/modelos.py]]
- [[_COMMUNITY_E14 cobre max fora de derivado|E14 cobre max fora de derivado]]
- [[_COMMUNITY_E02 id duplicado|E02 id duplicado]]
- [[_COMMUNITY_Branch sessao-pair-programming|Branch sessao-pair-programming]]
- [[_COMMUNITY_Bandeira some apos correcao (divergencia)|Bandeira some apos correcao (divergencia)]]
- [[_COMMUNITY_Limiares de decisão (descarte, premissa, confirmação etc.)|Limiares de decisão (descarte, premissa, confirmação etc.)]]
- [[_COMMUNITY_Agentes e skills por prompt (decisao de 20102026)|Agentes e skills por prompt (decisao de 20/10/2026)]]
- [[_COMMUNITY_Transcricao da apresentacao RERUM A|Transcricao da apresentacao RERUM [A]]]
- [[_COMMUNITY_Transcricao do documentario RERUM D|Transcricao do documentario RERUM [D]]]
- [[_COMMUNITY_Adaptacoes que a API precisa fazer sobre o motor|Adaptacoes que a API precisa fazer sobre o motor]]
- [[_COMMUNITY_bandeiras_nao_verificadas restrito a regras viaveis e perguntaveis|bandeiras_nao_verificadas restrito a regras viaveis e perguntaveis]]
- [[_COMMUNITY_Prioridade padrao por classe (1005010) e demais correcoes menores|Prioridade padrao por classe (100/50/10) e demais correcoes menores]]
- [[_COMMUNITY_Executor de casos incompleto (inconclusivas e pausa)|Executor de casos incompleto (inconclusivas e pausa)]]

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
10. `Checkpoint codex-davi: Arquitetura disponível: CLI/Python, JSON, sessão, inferência e explicação` - 13 edges

## Surprising Connections (you probably didn't know these)
- `Cinco tarefas TDD do motor (vermelho antes do verde)` --semantically_similar_to--> `Testes com casos conhecidos por versao da base`  [INFERRED] [semantically similar]
  docs/superpowers/plans/2026-10-20-motor-secao-1.md → CLAUDE.md
- `Status de conferencia das fontes (L, R, N)` --semantically_similar_to--> `Marcacao de suposicao a validar (conhecimento veterinario)`  [INFERRED] [semantically similar]
  docs/fontes/fontes.md → CLAUDE.md
- `Decisao deterministica, sem LLM nem rede no caminho` --semantically_similar_to--> `Motor independente de web, banco, LLM e servicos externos`  [INFERRED] [semantically similar]
  api/README.md → engine/README.md
- `Motor independente de web, banco, LLM e servicos externos` --semantically_similar_to--> `kb como pacote folha (nao importa engine)`  [INFERRED] [semantically similar]
  engine/README.md → kb/README.md
- `Estudo pendente: persistência integral de snapshot, ordem e versão da base` --semantically_similar_to--> `Restauração direta por snapshot integral, sem repetir o diálogo`  [INFERRED] [semantically similar]
  docs/processo/B.md → engine/README.md

## Import Cycles
- None detected.

## Hyperedges (group relationships)
- **Checkpoint distingue testes de software, casos sintéticos e validação clínica pendente** — docs_entrega_readme_evidencia_testes, docs_entrega_04_casos_de_teste_casos_sinteticos, docs_entrega_03_regras_de_producao_fontes_contextuais_cf_nao_validado, docs_entrega_readme_atendimento_parcial_exigencias [EXTRACTED 1.00]
- **Geração de regras/casos e verificação de sincronismo documental** — docs_superpowers_plans_2026_10_21_documentacao_entrega_parcial_geracao_verificacao_docs, readme_documentacao_sincronizada, docs_entrega_03_regras_de_producao_regras_geradas, docs_entrega_04_casos_de_teste_casos_sinteticos [EXTRACTED 1.00]
- **Camadas api -> engine -> kb (dependencia unidirecional)** — api_readme_backend_fastapi_sqlite, engine_readme_sessao, kb_readme_modelos, kb_readme_para_motor [EXTRACTED 1.00]
- **Pacotes api -> engine -> kb e web** — docs_superpowers_specs_2026_10_20_anamnese_bovinos_design_pacote_api, docs_superpowers_specs_2026_10_20_anamnese_bovinos_design_pacote_engine, docs_superpowers_specs_2026_10_20_anamnese_bovinos_design_pacote_kb, docs_superpowers_specs_2026_10_20_anamnese_bovinos_design_pacote_web [EXTRACTED 1.00]
- **Camadas da API: rotas finas, serviços, repositórios** — docs_superpowers_plans_2026_10_21_api_secao_4_arquitetura_casca_fina, docs_superpowers_plans_2026_10_21_api_secao_4_sessao_servico, docs_superpowers_plans_2026_10_21_api_secao_4_repositorios, docs_superpowers_plans_2026_10_21_api_secao_4_contexto [EXTRACTED 1.00]
- **Ciclo de edição e validação da base** — docs_superpowers_specs_2026_10_20_anamnese_bovinos_design_editor_grafico, docs_superpowers_specs_2026_10_20_anamnese_bovinos_design_validador_kb, docs_superpowers_specs_2026_10_20_anamnese_bovinos_design_versionamento_imutavel, docs_superpowers_specs_2026_10_20_anamnese_bovinos_design_casos_teste [EXTRACTED 1.00]
- **Congelamento do contrato da API** — docs_superpowers_plans_2026_10_21_api_secao_4_registro_contratos, docs_superpowers_plans_2026_10_21_api_secao_4_exemplos_contrato, docs_superpowers_plans_2026_10_21_api_secao_4_openapi_json, docs_superpowers_plans_2026_10_21_api_secao_4_exportar_openapi, docs_superpowers_plans_2026_10_21_api_secao_4_d6 [EXTRACTED 1.00]
- **Divergencias e lacunas da revisao do motor (21/10/2026)** — docs_revisoes_2026_10_21_revisao_motor_bandeira_apos_correcao, docs_revisoes_2026_10_21_revisao_motor_percentual_parecer, docs_revisoes_2026_10_21_revisao_motor_restauracao_sessao, docs_revisoes_2026_10_21_revisao_motor_traco_sessao, docs_revisoes_2026_10_21_revisao_motor_executor_casos [EXTRACTED 1.00]
- **Fluxo de manutencao do grafo de conhecimento** — claude_grafo_conhecimento, claude_manter_grafo_atualizado, claude_graphify_update, claude_obsidian_vault_conhecimento, claude_graph_report [EXTRACTED 1.00]
- **Modelo conceitual de sistema especialista (slide 14)** — claude_motor_de_inferencia, claude_base_conhecimento, claude_memoria_de_trabalho, claude_modulo_explicacao, claude_interface_usuario, claude_aquisicao_conhecimento, claude_fontes_dados_externas [EXTRACTED 1.00]
- **Persistencia e restauracao de sessao sem replay** — api_readme_d1_snapshot_json, api_readme_ordem_respostas, engine_readme_restaurar_exportar, engine_readme_correcao_reprocessa_lotes [EXTRACTED 1.00]
- **Reconstrução da sessão a cada requisição via snapshot** — docs_superpowers_plans_2026_10_21_api_secao_4_motor_sem_estado, docs_superpowers_plans_2026_10_21_api_secao_4_snapshot_json, docs_superpowers_plans_2026_10_21_api_secao_4_sessao_motor, docs_superpowers_plans_2026_10_21_api_secao_4_montar_estado, docs_superpowers_plans_2026_10_21_api_secao_4_d2 [EXTRACTED 1.00]
- **Restricoes obrigatorias do desafio** — claude_restricao_nao_usar_llm, claude_restricao_decisao_deterministica, claude_restricao_open_source, claude_restricao_localhost [EXTRACTED 1.00]
- **Três camadas de avaliação de regras** — docs_superpowers_specs_2026_10_20_anamnese_bovinos_design_derivados_sinais, docs_superpowers_specs_2026_10_20_anamnese_bovinos_design_dominio_8_doencas, docs_superpowers_specs_2026_10_20_anamnese_bovinos_design_urgencia_gravidade_confianca, docs_superpowers_specs_2026_10_20_anamnese_bovinos_design_bandeiras_vermelhas, docs_superpowers_specs_2026_10_20_anamnese_bovinos_design_camadas_tres [EXTRACTED 1.00]
- **Premissas de instalacao no Windows a validar** — docs_pesquisa_suposicoes_linha_24_node, docs_pesquisa_suposicoes_rodar_ps1, docs_pesquisa_suposicoes_winget_uv_id, docs_pesquisa_suposicoes_vite_mocks, docs_pesquisa_suposicoes_windows_11_demo, docs_pesquisa_execucao_local_powershell_execution_policy [INFERRED 0.75]
- **Versionamento imutável com validação prévia** — docs_superpowers_plans_2026_10_21_kb_secao_2_task5_carregador, kb_readme_validador [INFERRED 0.75]
- **Ambiente e portabilidade do kb e do motor** — docs_revisoes_2026_10_21_ledger_kb_secao_2_ambiente_venv_python_3_12, docs_revisoes_2026_10_21_ledger_kb_secao_2_comando_de_teste_do_motor_com_python_do_sistema, docs_revisoes_2026_10_21_ledger_kb_secao_2_gitattributes_eol_lf [INFERRED 0.85]
- **Ciclo de versao da base: validar, salvar, executar casos, ativar** — kb_readme_validador, kb_readme_carregador_repositorio, engine_readme_executar_caso, api_readme_portao_ativacao, api_readme_comparacao_versao_pai [INFERRED 0.85]
- **Componentes do motor de inferencia** — claude_motor_de_inferencia, claude_encadeamento, claude_resolucao_conflito, claude_fatores_certeza, claude_traco_inferencia, claude_modulo_explicacao [INFERRED 0.85]
- **Decisoes de processo da Secao 2** — docs_revisoes_2026_10_21_ledger_kb_secao_2_execucao_sequencial_das_tarefas, docs_revisoes_2026_10_21_ledger_kb_secao_2_sem_worktree_no_branch, docs_revisoes_2026_10_21_ledger_kb_secao_2_casos_invalidos_como_mutacoes_pytest, docs_revisoes_2026_10_21_ledger_kb_secao_2_modulos_do_kb_implementados_aqui [INFERRED 0.85]
- **Pipeline de planejamento e execucao com skills (obra/superpowers)** — docs_pesquisa_agentes_e_skills_brainstorming, docs_pesquisa_agentes_e_skills_writing_plans, docs_pesquisa_agentes_e_skills_executing_plans, docs_pesquisa_agentes_e_skills_test_driven_development, docs_pesquisa_agentes_e_skills_subagent_driven_development [INFERRED 0.85]
- **Stack de execucao local em localhost** — docs_pesquisa_execucao_local_fastapi_frontend, docs_pesquisa_execucao_local_vite, docs_pesquisa_execucao_local_uv, docs_pesquisa_execucao_local_playwright_webserver, docs_pesquisa_versoes_bibliotecas_uvicorn [INFERRED 0.85]
- **Regras do validador e codigos de erro** — docs_revisoes_2026_10_21_ledger_kb_secao_2_formato_de_id_gera_e20, docs_revisoes_2026_10_21_ledger_kb_secao_2_valor_none_gera_e03, docs_revisoes_2026_10_21_ledger_kb_secao_2_e08_so_sem_condicao_de_triagem, docs_revisoes_2026_10_21_ledger_kb_secao_2_e15_cf_min_e_max_juntos, docs_revisoes_2026_10_21_ledger_kb_secao_2_e16_exige_texto_nos_dois_modos, docs_revisoes_2026_10_21_ledger_kb_secao_2_e17_estrito_com_pivo_zero, docs_revisoes_2026_10_21_ledger_kb_secao_2_e14_cobre_max_fora_de_derivado, docs_revisoes_2026_10_21_ledger_kb_secao_2_novo_e21_tela_simbolo_invalido [INFERRED 0.85]

## Communities (34 total, 15 thin omitted)

### Community 0 - "CLAUDE.md do projeto (PoC Anamnese de Bovinos Leiteiros)"
Cohesion: 0.07
Nodes (60): CLAUDE.md do projeto (PoC Anamnese de Bovinos Leiteiros), Aquisicao de conhecimento, Motor de regras em Python independente de interface, Base de conhecimento, Testes com casos conhecidos por versao da base, Componentes da arquitetura (modelo conceitual), Conteudo obrigatorio do plano final (12 itens), Criterios de avaliacao do hackathon (+52 more)

### Community 1 - "Checkpoint codex-davi: Arquitetura disponível: CLI/Python, JSON, sessão, inferência e explicação"
Cohesion: 0.07
Nodes (42): Base de desenvolvimento 3.1.0-revisao1: 51 símbolos, 56 regras, 8 doenças e 6 telas, Exemplos sintéticos de alerta e sinais mamários pela CLI, Checkpoint codex-davi: Histórico: correções do motor e integração de desenvolvimento em 898512c, Checkpoint codex-davi: IA aplicada ao desenvolvimento e à documentação, fora da consulta, Checkpoint codex-davi: Processo verificável do checkpoint de 21/10/2026, Checkpoint codex-davi: Arquitetura disponível: CLI/Python, JSON, sessão, inferência e explicação, Checkpoint codex-davi: Contratos de sessão, parecer, porque/como e snapshot integral, Checkpoint codex-davi: Integração futura: FastAPI/Pydantic, React, SQLite e editor em grafo (+34 more)

### Community 2 - "Plano de implementação API (Seção 4)"
Cohesion: 0.07
Nodes (50): 27 endpoints da Seção 4.5, Bandeira vermelha e pausa de alerta, base_servico.py, casos_servico.py, Configuracao (api/config.py), Contexto e obter_contexto, criar_app / main.py, Pacote engine (motor) (+42 more)

### Community 3 - "Motor de inferência (engine/)"
Cohesion: 0.07
Nodes (48): Apresentação e roteiro da demonstração, Bandeiras vermelhas (chamar_agora), Base de conhecimento JSON versionada (kb/), Três camadas estritas (derivado, doença, urgência), Casos de teste conhecidos (31 casos), Contratos da API e formato único de erro, Correções e recálculo dos fatos, Critérios de parada (confirmação, limite, exaustão) (+40 more)

### Community 4 - "obra/superpowers (repositorio de skills)"
Cohesion: 0.05
Nodes (42): anthropics/skills (repositorio), brainstorming (skill), executing-plans (skill), frontend-design (skill), playwright-skill (lackeyjb), pptx (skill, source-available), Restricao de open source do hackathon, skill-creator (skill) (+34 more)

### Community 5 - "Classe Sessao (dialogo, estado, correcao, modo)"
Cohesion: 0.06
Nodes (36): API README (api/), Backend FastAPI + SQLite (casca fina sobre motor e kb), Comparacao de casos com a versao pai, Concorrencia: BEGIN IMMEDIATE e conferencia de revisao, Host confiavel (TrustedHostMiddleware contra DNS rebinding), Importacao de animais CSV/JSON sem 500, ordem_respostas no snapshot (reprocessar lotes na correcao), Portao de ativacao de versao (casos_falhando, confirmar_falhas) (+28 more)

### Community 6 - "Task 1: Ambiente e modelos Pydantic"
Cohesion: 0.09
Nodes (30): Script rodar.ps1 / rodar.sh (execucao em localhost), Sementes de animais ficticios e reset seguro do banco, Servir web/dist com rota coringa propria (api/frontend.py), Sessao presa a versao da base com que nasceu, Variaveis ANAMNESE_BASE_DIR e ANAMNESE_DB, Caso de teste da base (entrada e resultado esperado), Dependências entre símbolos, ciclo e ordem topológica, Plano de implementação do kb (Seção 2) (+22 more)

### Community 7 - "MSD Vet Manual"
Cohesion: 0.13
Nodes (15): Acidose ruminal (categoria), Acidose ruminal subaguda, Anaplasmose, Babesiose, Cetose bovina (hiperCetonemia), Dermatite digital, Deslocamento de abomaso, Embrapa ADM158 (tristeza parasitaria) (+7 more)

### Community 8 - "validar"
Cohesion: 0.13
Nodes (11): Achado E06 doenca sem regra, Arquivos kb_invalidas Secao 5.1, E08 bandeira sem triagem, E11 criterio de triagem, E15 cf_minimo e cf_maximo, E16 texto da tela de triagem, E17 ordem de limiares, E20 id_invalido (+3 more)

### Community 9 - "Alocacao de agente principal e alternativa por prompt de revisao"
Cohesion: 0.16
Nodes (10): Alocacao de agente principal e alternativa por prompt de revisao, anthropics/skills (pptx, docx, pdf, webapp-testing, frontend-design), Antigravity (plano Pro), Claude Code (Claude Pro), Codex (ChatGPT Plus), Gemini Pro (Google AI Pro, app web), Implementacao por pessoa (A, B, C) com agente principal e reserva, Fontes do projeto (fontes oficiais e de dominio) (+2 more)

### Community 10 - "SDD ledger"
Cohesion: 0.23
Nodes (10): Achado fato numerico inerte no teste, Ambiente venv, engine.modelos.Base.de_dict, .gitattributes, Pacote engine, SDD ledger, Spec anamnese bovinos, Task 6 (+2 more)

### Community 11 - "Google Antigravity (app, IDE e CLI)"
Cohesion: 0.42
Nodes (9): AGENTS.md (instrucoes do projeto), Google Antigravity (app, IDE e CLI), Claude Code, CLAUDE.md (instrucoes do projeto), OpenAI Codex (CLI, IDE, app desktop), Gemini CLI, GEMINI.md (instrucoes do projeto), Limites de uso dos planos (+1 more)

### Community 12 - "Task 1"
Cohesion: 0.28
Nodes (7): Achado carregar_base excecoes nativas, Achado prioridade zero no teste, carregar_base, Plano kb secao 2, pyproject.toml, Task 1, tests/kb/test_modelos.py

### Community 13 - "Rodada unica de correcao final"
Cohesion: 0.28
Nodes (7): Achado kb aceita base invalida, Achado ordem ausente no contrato, Aresta.ordem, kb/__init__.py, para_motor, Revisao final, validar_edicao

### Community 14 - "Contrato OpenAPI versionado e exemplos por operationId"
Cohesion: 0.25
Nodes (6): API sobe sem a base (409 conflito em vez de 500), Contrato OpenAPI versionado e exemplos por operationId, Formato unico de erro (codigos e X-Requisicao-Id), Notas para o frontend (proxima nulo, reabrir, 409 conflito), Mapa de 27 rotas por arquivo (prefixo /api), Testes da API (pytest, marca lento, base minima de fixtures)

### Community 15 - "Task 2"
Cohesion: 0.43
Nodes (6): Achado direcao do caminho do ciclo, Achado op e negado None viram default, encontrar_ciclo, kb/grafo.py, Task 2, Task 3

### Community 16 - "Task 5"
Cohesion: 0.53
Nodes (5): Achado temporario fixo ativa.json.tmp, Achado pai explicito nao verificado, ativa.json, salvar_nova, Task 5

### Community 17 - "Condicao.valor"
Cohesion: 0.40
Nodes (4): Achado Condicao valor int, Condicao.valor, E03 valor_invalido, model_fields_set da Aresta

### Community 18 - "kb/modelos.py"
Cohesion: 0.33
Nodes (4): kb/analise.py, kb/carregador.py, kb/modelos.py, LimiteDinamico

## Ambiguous Edges - Review These
- `Task 1` → `kb/__init__.py`  [AMBIGUOUS]
  docs/revisoes/2026-10-21-ledger-kb-secao-2.md · relation: references
- `Achado kb aceita base invalida` → `E14 cobre max fora de derivado`  [AMBIGUOUS]
  docs/revisoes/2026-10-21-ledger-kb-secao-2.md · relation: rationale_for
- `Achado temporario fixo ativa.json.tmp` → `Escrita interrompida apaga arquivo novo`  [AMBIGUOUS]
  docs/revisoes/2026-10-21-ledger-kb-secao-2.md · relation: conceptually_related_to
- `Limites de uso dos planos` → `Gemini CLI`  [AMBIGUOUS]
  docs/pesquisa/agentes-e-skills.md · relation: references
- `uv (sync, run, python pin)` → `Python 3.15.0`  [AMBIGUOUS]
  docs/pesquisa/execucao-local.md · relation: conceptually_related_to

## Knowledge Gaps
- **84 isolated node(s):** `graphify --update`, `.graphifyignore (escopo do grafo)`, `Spec anamnese bovinos`, `pyproject.toml`, `Aresta.ordem` (+79 more)
  These have ≤1 connection - possible missing edges or undocumented components. (Counts symbols only; 110 node(s) total have ≤1 connection when file, concept and rationale nodes are included.)
- **15 thin communities (<3 nodes) omitted from report** — run `graphify query` to explore isolated nodes.

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **Why does `Conteudo obrigatorio do plano final (12 itens)` connect `CLAUDE.md do projeto (PoC Anamnese de Bovinos Leiteiros)` to `MSD Vet Manual`?**
  _High betweenness centrality (0.012) - this node is a cross-community bridge._
- **Are the 2 inferred relationships involving `Motor de inferencia` (e.g. with `Sistema especialista` and `Memoria de trabalho`) actually correct?**
  _`Motor de inferencia` has 2 INFERRED edges - model-reasoned connections that need verification._
- **What connects `graphify --update`, `.graphifyignore (escopo do grafo)`, `Spec anamnese bovinos` to the rest of the system?**
  _84 weakly-connected nodes found - possible documentation gaps or missing edges._
- **Should `CLAUDE.md do projeto (PoC Anamnese de Bovinos Leiteiros)` be split into smaller, more focused modules?**
  _Cohesion score 0.06971153846153846 - nodes in this community are weakly interconnected._
- **Should `Checkpoint codex-davi: Arquitetura disponível: CLI/Python, JSON, sessão, inferência e explicação` be split into smaller, more focused modules?**
  _Cohesion score 0.0742447516641065 - nodes in this community are weakly interconnected._

### Low-confidence Hints
_AMBIGUOUS edges — the extractor was unsure. Verify before acting on these._

- **What is the exact relationship between `Task 1` and `kb/__init__.py`?**
  _Edge tagged AMBIGUOUS (relation: references) - confidence is low._
- **What is the exact relationship between `Achado kb aceita base invalida` and `E14 cobre max fora de derivado`?**
  _Edge tagged AMBIGUOUS (relation: rationale_for) - confidence is low._