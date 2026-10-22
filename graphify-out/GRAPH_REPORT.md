# Graph Report - secao5-davi  (2026-10-22)

## Corpus Check
- 4 files · ~108,263 words
- Verdict: corpus is large enough that graph structure adds value.

## Summary
- 818 nodes · 1470 edges · 64 communities (46 shown, 18 thin omitted)
- Extraction: 92% EXTRACTED · 7% INFERRED · 0% AMBIGUOUS · INFERRED: 106 edges (avg confidence: 0.82)
- Token cost: indisponível; o agente hospedeiro não fornece uso medido desta execução.

## Community Hubs (Navigation)
- Requisitos e arquitetura conceitual
- Plano de API localhost
- Especificação do sistema especialista
- Casos sintéticos na v0002
- Pesquisa de ferramentas locais
- Sistema visual e componentes
- Regras e símbolos da v0002
- Arquitetura e demonstração web
- Plano histórico frontend implementado
- Hipocalcemia e mobilidade
- Riscos da interface integrada
- Sessões, API e motor
- Fontes clínicas contextuais
- Revisão do validador kb
- Persistência e validação da base
- Agentes de implementação
- Demonstração e troca de modo
- Contratos e integração localhost
- Processo documental verificável
- Consulta web e correções
- Acidose e sinais digestivos
- Cetose e início da lactação
- Backend e isolamento do motor
- Produto e limites clínicos
- Metrite e puerpério
- Sinais térmicos e urgência
- Entrega e manutenção documental
- Ledger de implementação kb
- Modelos e validação do kb
- Snapshot e pressupostos do motor
- Assistentes e instruções
- Ambiente e carregamento kb
- Correções finais da base
- Parecer, retomada e limites
- Bandeiras de urgência
- Tristeza parasitária bovina
- Fontes canônicas e revisões
- Ciclos de dependências
- Versões e execução de casos
- Versionamento imutável da base
- Valores e serialização
- Módulos da base de conhecimento
- E2E e verificação offline
- Cliente da API e erros
- Ensaio humano e entrega final
- Parecer e fatores de certeza
- Validação de grupos max
- Identificadores e telas
- Regras estruturais do validador
- Decisões sobre branches
- Histórico das bandeiras
- Limiares e fatores MYCIN
- Decisão sobre agentes
- Apresentação RERUM
- Entregas e demonstração localhost
- Regulamento e cronograma
- Documentário RERUM
- Adaptações entre API e motor
- Viabilidade das bandeiras
- Prioridades das regras
- Histórico do executor de casos

## God Nodes (most connected - your core abstractions)
1. `Documento gerado da v0002: 56 regras, 51 símbolos e 8 doenças` - 123 edges
2. `CLAUDE.md: instruções atuais do PoC de anamnese bovina` - 55 edges
3. `34 casos sintéticos aprovados na v0002 por executar_caso` - 40 edges
4. `v0002 ativa e imutável, pai v0001; ativação não valida clínica` - 39 edges
5. `Riscos abertos R01–R21, web integrada e checklist de fechamento` - 35 edges
6. `Sistema visual documentado do protótipo HackAtom` - 34 edges
7. `Plano histórico do frontend; implementação Tasks 1–8 documentada nas fontes atuais` - 32 edges
8. `Roteiro atual: consulta React integrada e CLI de reserva` - 30 edges
9. `Arquitetura implementada: React→FastAPI→Sessao, kb/v0002 e SQLite` - 22 edges
10. `Plano de implementação API (Seção 4)` - 20 edges

## Surprising Connections (you probably didn't know these)
- `Cinco tarefas TDD do motor (vermelho antes do verde)` --semantically_similar_to--> `Casos de teste com resultado esperado por versão da base`  [INFERRED] [semantically similar]
  docs/superpowers/plans/2026-10-20-motor-secao-1.md → CLAUDE.md
- `Status de conferencia das fontes (L, R, N)` --semantically_similar_to--> `Conhecimento veterinário sempre como suposição a validar`  [INFERRED] [semantically similar]
  docs/fontes/fontes.md → CLAUDE.md
- `Estudo pendente: persistência integral de snapshot, ordem e versão da base` --semantically_similar_to--> `Restauração direta por snapshot integral, sem repetir o diálogo`  [INFERRED] [semantically similar]
  docs/processo/B.md → engine/README.md
- `Números como string sem coerção, arredondamento ou CF` --semantically_similar_to--> `Valores brutos, 422 preservado e 409 relê sem repetir mutação`  [INFERRED] [semantically similar]
  PRODUCT.md → docs/entrega/02-arquitetura.md
- `Sementes de animais ficticios e reset seguro do banco` --conceptually_related_to--> `kb/validador.py (validar, validar_dados, validar_edicao, Relatorio)`  [INFERRED]
  api/README.md → kb/README.md

## Import Cycles
- None detected.

## Hyperedges (group relationships)
- **Busca sob demanda por pergunta, comunidade ou visão geral excepcional** — claude_grafo_conhecimento, claude_graphify_query, claude_obsidian_vault_conhecimento, claude_graph_report [EXTRACTED 1.00]
- **Fechar bloco documental: atualizar, exportar e separar commit** — claude_manter_grafo_atualizado, claude_graphify_update, claude_obsidian_vault_conhecimento, claude_exclusoes_atualizacao [EXTRACTED 1.00]
- **Correção térmica com troca temporária, trava e reconciliação da sessão** — docs_entrega_05_apresentacao_e_demo_historico_corrigivel, docs_entrega_05_apresentacao_e_demo_correcao_termica_transacional, docs_entrega_05_apresentacao_e_demo_trava_interacao, docs_entrega_05_apresentacao_e_demo_reconciliacao_get, docs_entrega_05_apresentacao_e_demo_parecer_unico_api [EXTRACTED 1.00]
- **Geração de regras/casos e verificação de sincronismo documental** — docs_superpowers_plans_2026_10_21_documentacao_entrega_parcial_geracao_verificacao_docs, readme_documentacao_sincronizada, docs_entrega_03_regras_de_producao_regras_geradas, docs_entrega_04_casos_de_teste_casos_sinteticos [EXTRACTED 1.00]
- **Camadas api -> engine -> kb (dependencia unidirecional)** — api_readme_backend_fastapi_sqlite, engine_readme_sessao, kb_readme_modelos, kb_readme_para_motor [EXTRACTED 1.00]
- **Pacotes api -> engine -> kb e web** — docs_superpowers_specs_2026_10_20_anamnese_bovinos_design_pacote_api, docs_superpowers_specs_2026_10_20_anamnese_bovinos_design_pacote_engine, docs_superpowers_specs_2026_10_20_anamnese_bovinos_design_pacote_kb, docs_superpowers_specs_2026_10_20_anamnese_bovinos_design_pacote_web [EXTRACTED 1.00]
- **Camadas da API: rotas finas, serviços, repositórios** — docs_superpowers_plans_2026_10_21_api_secao_4_arquitetura_casca_fina, docs_superpowers_plans_2026_10_21_api_secao_4_sessao_servico, docs_superpowers_plans_2026_10_21_api_secao_4_repositorios, docs_superpowers_plans_2026_10_21_api_secao_4_contexto [EXTRACTED 1.00]
- **Ciclo de edição e validação da base** — docs_superpowers_specs_2026_10_20_anamnese_bovinos_design_editor_grafico, docs_superpowers_specs_2026_10_20_anamnese_bovinos_design_validador_kb, docs_superpowers_specs_2026_10_20_anamnese_bovinos_design_versionamento_imutavel, docs_superpowers_specs_2026_10_20_anamnese_bovinos_design_casos_teste [EXTRACTED 1.00]
- **Congelamento do contrato da API** — docs_superpowers_plans_2026_10_21_api_secao_4_registro_contratos, docs_superpowers_plans_2026_10_21_api_secao_4_exemplos_contrato, docs_superpowers_plans_2026_10_21_api_secao_4_openapi_json, docs_superpowers_plans_2026_10_21_api_secao_4_exportar_openapi, docs_superpowers_plans_2026_10_21_api_secao_4_d6 [EXTRACTED 1.00]
- **Identidade documentada: cores, fontes, composição, profundidade eSVGs** — design_sistema_visual, design_tipografia, design_composicao_desktop, design_profundidade, design_formas [EXTRACTED 1.00]
- **Divergencias e lacunas da revisao do motor (21/10/2026)** — docs_revisoes_2026_10_21_revisao_motor_bandeira_apos_correcao, docs_revisoes_2026_10_21_revisao_motor_percentual_parecer, docs_revisoes_2026_10_21_revisao_motor_restauracao_sessao, docs_revisoes_2026_10_21_revisao_motor_traco_sessao, docs_revisoes_2026_10_21_revisao_motor_executor_casos [EXTRACTED 1.00]
- **Consulta web implementada: tipos, respostas, hipóteses, explicações ehistórico** — docs_entrega_02_arquitetura_web_implementada, docs_entrega_02_arquitetura_tipos_cliente, docs_entrega_02_arquitetura_respostas_erros, docs_entrega_02_arquitetura_hipoteses_explicacoes, docs_entrega_02_arquitetura_historico_correcao, docs_entrega_02_arquitetura_precisao_contrato, docs_entrega_02_arquitetura_assets_e2e [EXTRACTED 1.00]
- **E2E automático eSPA local coexistem compendências físicas eclínicas** — docs_entrega_06_riscos_e_pendencias_qualidade_frontend, docs_entrega_06_riscos_e_pendencias_r20, docs_entrega_06_riscos_e_pendencias_rede_spa, docs_entrega_06_riscos_e_pendencias_r01, secao5_r17_swagger_cdn [EXTRACTED 1.00]
- **Persistencia e restauracao de sessao sem replay** — api_readme_d1_snapshot_json, api_readme_ordem_respostas, engine_readme_restaurar_exportar, engine_readme_correcao_reprocessa_lotes [EXTRACTED 1.00]
- **Reconstrução da sessão a cada requisição via snapshot** — docs_superpowers_plans_2026_10_21_api_secao_4_motor_sem_estado, docs_superpowers_plans_2026_10_21_api_secao_4_snapshot_json, docs_superpowers_plans_2026_10_21_api_secao_4_sessao_motor, docs_superpowers_plans_2026_10_21_api_secao_4_montar_estado, docs_superpowers_plans_2026_10_21_api_secao_4_d2 [EXTRACTED 1.00]
- **Três camadas de avaliação de regras** — docs_superpowers_specs_2026_10_20_anamnese_bovinos_design_derivados_sinais, docs_superpowers_specs_2026_10_20_anamnese_bovinos_design_dominio_8_doencas, docs_superpowers_specs_2026_10_20_anamnese_bovinos_design_urgencia_gravidade_confianca, docs_superpowers_specs_2026_10_20_anamnese_bovinos_design_bandeiras_vermelhas, docs_superpowers_specs_2026_10_20_anamnese_bovinos_design_camadas_tres [EXTRACTED 1.00]
- **Premissas de instalacao no Windows a validar** — docs_pesquisa_suposicoes_linha_24_node, docs_pesquisa_suposicoes_rodar_ps1, docs_pesquisa_suposicoes_winget_uv_id, docs_pesquisa_suposicoes_vite_mocks, docs_pesquisa_suposicoes_windows_11_demo, docs_pesquisa_execucao_local_powershell_execution_policy [INFERRED 0.75]
- **Versionamento imutável com validação prévia** — docs_superpowers_plans_2026_10_21_kb_secao_2_task5_carregador, kb_readme_validador [INFERRED 0.75]
- **Ambiente e portabilidade do kb e do motor** — docs_revisoes_2026_10_21_ledger_kb_secao_2_ambiente_venv_python_3_12, docs_revisoes_2026_10_21_ledger_kb_secao_2_comando_de_teste_do_motor_com_python_do_sistema, docs_revisoes_2026_10_21_ledger_kb_secao_2_gitattributes_eol_lf [INFERRED 0.85]
- **Ciclo de versao da base: validar, salvar, executar casos, ativar** — kb_readme_validador, kb_readme_carregador_repositorio, engine_readme_executar_caso, api_readme_portao_ativacao, api_readme_comparacao_versao_pai [INFERRED 0.85]
- **Decisoes de processo da Secao 2** — docs_revisoes_2026_10_21_ledger_kb_secao_2_execucao_sequencial_das_tarefas, docs_revisoes_2026_10_21_ledger_kb_secao_2_sem_worktree_no_branch, docs_revisoes_2026_10_21_ledger_kb_secao_2_casos_invalidos_como_mutacoes_pytest, docs_revisoes_2026_10_21_ledger_kb_secao_2_modulos_do_kb_implementados_aqui [INFERRED 0.85]
- **Pipeline de planejamento e execucao com skills (obra/superpowers)** — docs_pesquisa_agentes_e_skills_brainstorming, docs_pesquisa_agentes_e_skills_writing_plans, docs_pesquisa_agentes_e_skills_executing_plans, docs_pesquisa_agentes_e_skills_test_driven_development, docs_pesquisa_agentes_e_skills_subagent_driven_development [INFERRED 0.85]
- **Stack de execucao local em localhost** — docs_pesquisa_execucao_local_fastapi_frontend, docs_pesquisa_execucao_local_vite, docs_pesquisa_execucao_local_uv, docs_pesquisa_execucao_local_playwright_webserver, docs_pesquisa_versoes_bibliotecas_uvicorn [INFERRED 0.85]
- **Regras do validador e codigos de erro** — docs_revisoes_2026_10_21_ledger_kb_secao_2_formato_de_id_gera_e20, docs_revisoes_2026_10_21_ledger_kb_secao_2_valor_none_gera_e03, docs_revisoes_2026_10_21_ledger_kb_secao_2_e08_so_sem_condicao_de_triagem, docs_revisoes_2026_10_21_ledger_kb_secao_2_e15_cf_min_e_max_juntos, docs_revisoes_2026_10_21_ledger_kb_secao_2_e16_exige_texto_nos_dois_modos, docs_revisoes_2026_10_21_ledger_kb_secao_2_e17_estrito_com_pivo_zero, docs_revisoes_2026_10_21_ledger_kb_secao_2_e14_cobre_max_fora_de_derivado, docs_revisoes_2026_10_21_ledger_kb_secao_2_novo_e21_tela_simbolo_invalido [INFERRED 0.85]

## Communities (64 total, 18 thin omitted)

### Community 0 - "Requisitos e arquitetura conceitual"
Cohesion: 0.05
Nodes (48): AGENTS.md: instruções de busca e manutenção documental, CLAUDE.md: instruções atuais do PoC de anamnese bovina, Aquisição de conhecimento por especialista e engenheiro, Motor Python com biblioteca padrão, Base explícita de conhecimento e versões imutáveis, Componentes do modelo conceitual exigido, Planos aprovados e documentação de entrega disponível, Avaliação: potencial, complexidade, assertividade e organização com IA (+40 more)

### Community 1 - "Plano de API localhost"
Cohesion: 0.07
Nodes (50): 27 endpoints da Seção 4.5, Bandeira vermelha e pausa de alerta, base_servico.py, casos_servico.py, Configuracao (api/config.py), Contexto e obter_contexto, criar_app / main.py, Pacote engine (motor) (+42 more)

### Community 2 - "Especificação do sistema especialista"
Cohesion: 0.07
Nodes (48): Apresentação e roteiro da demonstração, Bandeiras vermelhas (chamar_agora), Base de conhecimento JSON versionada (kb/), Três camadas estritas (derivado, doença, urgência), Casos de teste conhecidos (31 casos), Contratos da API e formato único de erro, Correções e recálculo dos fatos, Critérios de parada (confirmação, limite, exaustão) (+40 more)

### Community 3 - "Casos sintéticos na v0002"
Cohesion: 0.09
Nodes (50): Exemplos sintéticos de alerta e sinais mamários pela CLI, Cetose / Hipercetonemia (cetose), Dermatite Digital Bovina (dermatite_digital), Deslocamento de Abomaso (deslocamento_abomaso), Mastite (mastite), R-BV-01: chamar_agora (CF 0,99), C-ACI-01: passou, observar, acidose, C-ACI-02: passou, observar, acidose (+42 more)

### Community 4 - "Pesquisa de ferramentas locais"
Cohesion: 0.05
Nodes (42): anthropics/skills (repositorio), brainstorming (skill), executing-plans (skill), frontend-design (skill), playwright-skill (lackeyjb), pptx (skill, source-available), Restricao de open source do hackathon, skill-creator (skill) (+34 more)

### Community 5 - "Sistema visual e componentes"
Cohesion: 0.07
Nodes (30): Barras role=meter com preenchimento sólido, Botão laranja primário e branco/verde secundário, Campo numérico textual preserva entrada ao erro, Composição desktop 1440 px derivada dos frames, Token cor/acento: #f0913a, Token cor/acento-escuro: #b9601a, Token cor/alerta: #e8a317, Token cor/creme: #f6f1e4 (+22 more)

### Community 6 - "Regras e símbolos da v0002"
Cohesion: 0.14
Nodes (24): BHB sanguíneo (bhb_sanguineo), CMT reagente (cmt_reagente), Evidência agrupada de alteração do leite (evidencia_alteracao_leite), Corpos cetônicos na urina (fita_urina_corpos_cetonicos), Alteração visível do leite (leite_alterado), Lesão característica no talão (lesao_erosiva_talao_morango), Monitoramento Clínico Contínuo (observar), Ping no flanco esquerdo (ping_metalico_flanco_esquerdo) (+16 more)

### Community 7 - "Arquitetura e demonstração web"
Cohesion: 0.10
Nodes (10): Base de desenvolvimento 3.1.0-revisao1: 51 símbolos, 56 regras, 8 doenças e 6 telas, Checkpoint codex-davi: Histórico: correções do motor e integração de desenvolvimento em 898512c, Arquitetura implementada: React→FastAPI→Sessao, kb/v0002 e SQLite, Motor padrão; API em .[dev] e build web com Node 24/lockfile npm, Sete componentes do modelo dos organizadores, Evidência registrada: 1066 Python, 170 subtestes, 39 interface e 8 E2E, Decisões verificáveis de motor, base e documentação, Achados procedentes de motor, restauração e contrato de dados (+2 more)

### Community 8 - "Plano histórico frontend implementado"
Cohesion: 0.13
Nodes (14): Varela Round em títulos e Nunito Sans no conteúdo, Botao, opções, numérico, confiança, boi, balão, progresso e modal, tokens cor/* do Figma, Varela Round e Nunito Sans, hipóteses desde segunda pergunta e explicação Por quê, início cria animal anônimo e sessão no modo escolhido, Vocabulário pt-BR: verificação, especialista, produtor e parecer, audit/polish, responsivo 375/768/1024/1440 e estados, Plano histórico do frontend; implementação Tasks 1–8 documentada nas fontes atuais (+6 more)

### Community 9 - "Hipocalcemia e mobilidade"
Cohesion: 0.11
Nodes (19): Cálcio sérico total (calcio_serico), Claudicação (claudicacao), Decúbito (decubito), Dias em lactação (dias_em_lactacao), Dor na região do talão (dor_flexao_talao), Hipocalcemia Puerperal (hipocalcemia), Periparto imediato (periparto_imediato), Desvio cervical em S (pescoco_em_s) (+11 more)

### Community 10 - "Riscos da interface integrada"
Cohesion: 0.11
Nodes (19): UI preservou regras, versões imutáveis, contratos e API/motor/kb, Verificação web: oito E2E Chromium, seis telas e axe selecionado, R01: Conhecimento clínico e CF sem validação especializada, R02: Confiança excessiva por sinais correlacionados, R03: Falso entendimento de `sem_problema`, R04: Editor gráfico ainda pendente, R05: Regressão na restauração da sessão, R06: Divergência entre v0001 e especificação clínica (+11 more)

### Community 11 - "Sessões, API e motor"
Cohesion: 0.15
Nodes (12): Concorrencia: BEGIN IMMEDIATE e conferencia de revisao, Importacao de animais CSV/JSON sem 500, ordem_respostas no snapshot (reprocessar lotes na correcao), Bandeira vermelha: pausa, continuar, ver_parecer, Correcao reprocessa respostas em lotes na ordem real, Nucleo sem estado inferir() e analisar(), Observacoes com valor, cf e origem (resposta, ficha, importacao), Explicacao por que? e como? (porque/como) (+4 more)

### Community 12 - "Fontes clínicas contextuais"
Cohesion: 0.15
Nodes (15): Acidose ruminal (categoria), Acidose ruminal subaguda, Anaplasmose, Babesiose, Cetose bovina (hiperCetonemia), Dermatite digital, Deslocamento de abomaso, Embrapa ADM158 (tristeza parasitaria) (+7 more)

### Community 13 - "Revisão do validador kb"
Cohesion: 0.13
Nodes (11): Achado E06 doenca sem regra, Arquivos kb_invalidas Secao 5.1, E08 bandeira sem triagem, E11 criterio de triagem, E15 cf_minimo e cf_maximo, E16 texto da tela de triagem, E17 ordem de limiares, E20 id_invalido (+3 more)

### Community 14 - "Persistência e validação da base"
Cohesion: 0.24
Nodes (13): Caso de teste da base (entrada e resultado esperado), Plano de implementação do kb (Seção 2), Regra de produção (condições, conclusão, CF), Revisão do motor (docs/revisoes/2026-10-21-revisao-motor.md), Símbolo (variável da base), Especificação de anamnese (docs/superpowers/specs, Seção 2 e 5.1), Task 1: Ambiente e modelos Pydantic, Task 2: Análise de dependências (+5 more)

### Community 15 - "Agentes de implementação"
Cohesion: 0.14
Nodes (12): Alocacao de agente principal e alternativa por prompt de revisao, anthropics/skills (pptx, docx, pdf, webapp-testing, frontend-design), Antigravity (plano Pro), Claude Code (Claude Pro), Codex (ChatGPT Plus), Skills em formato aberto (.agents/skills, .claude/skills, AGENTS.md), Gemini Pro (Google AI Pro, app web), Implementacao por pessoa (A, B, C) com agente principal e reserva (+4 more)

### Community 16 - "Demonstração e troca de modo"
Cohesion: 0.28
Nodes (8): Modo especialista da interface corresponde a veterinario na API, Demo web: 422, troca produtor/especialista, parecer único e alerta, E2E sintético com API real cobre troca e correções, Parecer parcial permite trocar modo e retomar anamnese, Parecer único da API combina fatos antes e depois da troca, Preparação: banco fora do OneDrive e build local, Roteiro atual: consulta React integrada e CLI de reserva, Tempos hipotéticos: fala de 10 min e demo de 4 min; alternativa de 5 min

### Community 17 - "Contratos e integração localhost"
Cohesion: 0.13
Nodes (9): Contrato OpenAPI versionado e exemplos por operationId, Notas para o frontend (proxima nulo, reabrir, 409 conflito), Mapa de 27 rotas por arquivo (prefixo /api), Script rodar.ps1 / rodar.sh (execucao em localhost), Sementes de animais ficticios e reset seguro do banco, Servir web/dist com rota coringa propria (api/frontend.py), Testes da API (pytest, marca lento, base minima de fixtures), Variaveis ANAMNESE_BASE_DIR e ANAMNESE_DB (+1 more)

### Community 18 - "Processo documental verificável"
Cohesion: 0.20
Nodes (10): Checkpoint codex-davi: Processo verificável do checkpoint de 21/10/2026, Proveniência: v0002 ativa, pai v0001, 56 regras sem validação clínica, Papel A: pessoa, blocos reais, decisões humanas e aprendizado a completar, Papel A: registro técnico curado, sem depoimento pessoal atribuído, Papel C: diário a preencher, sem interações ou aprendizado inventados, Papel C planejado: interface, testes de navegador, demo e apresentação, Log de revisões: evidência e proveniência do checkpoint, Ajustes propostos: max mamário e caminhos de TPB sem febre (+2 more)

### Community 19 - "Consulta web e correções"
Cohesion: 0.15
Nodes (12): Fontes/SVG/CSS locais e E2E com SQLite temporário/v0002, v0002 explicita limites e casas decimais, Top 4 desde segunda pergunta; porquê/como e regras do backend, Voltar/PUT limitado à navegação atual, Precisão não exposta por proxima; backend valida casas decimais, Valores brutos, 422 preservado e 409 relê sem repetir mutação, Tipos OpenAPI gerados e cliente centraliza erros, Camada web implementada: Início, Anamnese e Parecer (+4 more)

### Community 20 - "Acidose e sinais digestivos"
Cohesion: 0.17
Nodes (13): Acidose Ruminal (acidose), Diarreia (diarreia), Fezes com espuma e grãos (fezes_aquosas_espuma_graos), Mudança abrupta de concentrado (mudanca_abrupta_concentrado), pH ruminal (ph_ruminal), R-ACI-01: acidose (CF 0,35), R-ACI-02: acidose (CF 0,55), R-ACI-03: acidose (CF 0,5) (+5 more)

### Community 21 - "Cetose e início da lactação"
Cohesion: 0.18
Nodes (13): Apetite (apetite), Flanco esquerdo afundado (flanco_esquerdo_afundado), Hálito adocicado (halito_adocicado_acetona), Inicio lactacao (inicio_lactacao), Queda de produção de leite (queda_producao), R-BV-03: chamar_agora (CF 0,99), R-CET-01: cetose (CF 0,4), R-CET-02: cetose (CF 0,5) (+5 more)

### Community 22 - "Backend e isolamento do motor"
Cohesion: 0.21
Nodes (9): API README (api/), Backend FastAPI + SQLite (casca fina sobre motor e kb), Host confiavel (TrustedHostMiddleware contra DNS rebinding), Arvore da secao 4.3 da especificacao (sessao, validacao, modelos), Motor de inferencia README (engine/), Demonstracao executavel (python -m engine) com base artificial, Organizacao dos modulos do motor, Divergencias kb x motor (prioridade, layout, operadores ASCII) (+1 more)

### Community 23 - "Produto e limites clínicos"
Cohesion: 0.17
Nodes (12): Identidade Figma e autoridade API preservadas, Produto: Anamnese Bovina explicável, Rede, base ausente, carregamento, duplo envio e 409, Percentual é confiança do sistema; regras não validadas, Prova de conceito localhost com casos e animais fictícios, Diálogo Akinator com regras explícitas e CF MYCIN, Editor visual fora do frontend de anamnese, Não sei é resposta explícita, diferente de Não ou ausência (+4 more)

### Community 24 - "Metrite e puerpério"
Cohesion: 0.23
Nodes (12): Corrimento vaginal fétido (corrimento_fetido), Corrimento vaginal (corrimento_vaginal), Metrite Puerperal (metrite), Puerperio (puerperio), R-DER-02: puerperio (CF 0,99), R-MET-01: metrite (CF 0,75), R-MET-02: metrite (CF 0,45), R-MET-03: metrite (CF 0,35) (+4 more)

### Community 25 - "Sinais térmicos e urgência"
Cohesion: 0.24
Nodes (12): Temperatura ao toque das extremidades (extremidades), Febre (febre), Hipotermia (hipotermia), R-DER-04: febre (CF 0,95), R-DER-05: hipotermia (CF 0,85), R-DER-06: hipotermia (CF 0,6), R-DER-07: febre (CF 0,45), R-DER-08: febre (CF -0,9) (+4 more)

### Community 26 - "Entrega e manutenção documental"
Cohesion: 0.20
Nodes (7): Envio: alvo interno 22/10 às 18:30 e prazo oficial às 20:00, Atendimento documentado e pendências de entrega, Base ativa v0002 e versões imutáveis preservadas, 898512c e f46cd6e são checkpoints históricos, Prazos oficiais: envio 22/10/2026 20h e apresentação 23/10/2026 09h, Índice da Seção 5 e consulta web; checkpoints históricos distinguidos, Pacote final pendente: PDFs, slides, vídeo, licença e ZIP

### Community 27 - "Ledger de implementação kb"
Cohesion: 0.23
Nodes (10): Achado fato numerico inerte no teste, Ambiente venv, engine.modelos.Base.de_dict, .gitattributes, Pacote engine, SDD ledger, Spec anamnese bovinos, Task 6 (+2 more)

### Community 28 - "Modelos e validação do kb"
Cohesion: 0.29
Nodes (9): Guardas de execucao (CF positivo para urgencia e bandeira), Pacote kb README (base de conhecimento), kb/analise.py (dependencias, ciclo, ordem topologica), Codigos do validador E00-E23 e W01-W03, Dados ficticios e regras como suposicao a validar, kb/grafo.py (conversao 1:1 Base <-> grafo bipartido), kb/modelos.py (modelos Pydantic, carregar_base, para_motor), JSON Schemas versionados e test_schema_sincronizado (+1 more)

### Community 29 - "Snapshot e pressupostos do motor"
Cohesion: 0.20
Nodes (5): Contratos de sessão, parecer, porque/como e snapshot integral, Integração implementada: React, FastAPI/Pydantic, SQLite e scripts localhost, Papel B: diário a preencher, sem interações ou resultados inventados, Papel B planejado: API, contratos, validação editorial, scripts e persistência, Pendências: editor gráfico, licença, telefones e validação clínica

### Community 30 - "Assistentes e instruções"
Cohesion: 0.42
Nodes (9): AGENTS.md (instrucoes do projeto), Google Antigravity (app, IDE e CLI), Claude Code, CLAUDE.md (instrucoes do projeto), OpenAI Codex (CLI, IDE, app desktop), Gemini CLI, GEMINI.md (instrucoes do projeto), Limites de uso dos planos (+1 more)

### Community 31 - "Ambiente e carregamento kb"
Cohesion: 0.28
Nodes (7): Achado carregar_base excecoes nativas, Achado prioridade zero no teste, carregar_base, Plano kb secao 2, pyproject.toml, Task 1, tests/kb/test_modelos.py

### Community 32 - "Correções finais da base"
Cohesion: 0.28
Nodes (7): Achado kb aceita base invalida, Achado ordem ausente no contrato, Aresta.ordem, kb/__init__.py, para_motor, Revisao final, validar_edicao

### Community 33 - "Parecer, retomada e limites"
Cohesion: 0.32
Nodes (5): Alerta não fecha por Esc/fundo; outros diálogos devolvem foco, parecer de oito doenças, blocos e Como cheguei aqui, Task 5: Alerta de bandeira — implementada com alcance documentado, Task 6: Parecer e explicações — implementada com alcance documentado, Pausa exige alerta mesmo com proxima nulo

### Community 34 - "Bandeiras de urgência"
Cohesion: 0.29
Nodes (8): Apatia (apatia), Atendimento Veterinário Imediato (chamar_agora), R-BV-04: chamar_agora (CF 0,99), R-BV-05: chamar_agora (CF 0,99), R-BV-06: chamar_agora (CF 0,99), R-MAS-02: mastite (CF 0,5), R-URG-03: chamar_agora (CF 0,99), Inflamação do úbere (ubere_inflamado)

### Community 35 - "Tristeza parasitária bovina"
Cohesion: 0.25
Nodes (8): Exposição recente a carrapatos (carrapatos_historico_recente), Hemoparasitas no esfregaço (esfregaco_hemoparasitas), Mucosas pálidas ou amareladas (mucosas_palidas_ou_ictericas), R-TPB-02: tpb (CF 0,6), R-TPB-03: tpb (CF 0,35), R-TPB-04: tpb (CF 0,9), R-URG-02: chamar_agora (CF 0,99), Tristeza Parasitária Bovina (tpb)

### Community 36 - "Fontes canônicas e revisões"
Cohesion: 0.25
Nodes (8): Especificacao autorizada da secao 1 (docs/prompts/secao-1.md), Revisao do motor de inferencia (21/10/2026), Tabela de conformidade com a especificacao (16 itens), Ficha com null tratada como nao sei (deve ser ausente), Plano de implementacao do motor (secao 1), Evidencia final: 56 testes sem falhas, Focos da revisao (sem valor, contradicoes, loops, bandeiras), Especificacao canonica do projeto (anamnese bovinos)

### Community 37 - "Ciclos de dependências"
Cohesion: 0.43
Nodes (6): Achado direcao do caminho do ciclo, Achado op e negado None viram default, encontrar_ciclo, kb/grafo.py, Task 2, Task 3

### Community 38 - "Versões e execução de casos"
Cohesion: 0.33
Nodes (5): Comparacao de casos com a versao pai, Portao de ativacao de versao (casos_falhando, confirmar_falhas), Sessao presa a versao da base com que nasceu, engine.casos.executar_caso (casos de teste reproduziveis), kb/carregador.py Repositorio (versoes imutaveis, ativa.json, hash sha256)

### Community 39 - "Versionamento imutável da base"
Cohesion: 0.53
Nodes (5): Achado temporario fixo ativa.json.tmp, Achado pai explicito nao verificado, ativa.json, salvar_nova, Task 5

### Community 40 - "Valores e serialização"
Cohesion: 0.40
Nodes (4): Achado Condicao valor int, Condicao.valor, E03 valor_invalido, model_fields_set da Aresta

### Community 41 - "Módulos da base de conhecimento"
Cohesion: 0.33
Nodes (4): kb/analise.py, kb/carregador.py, kb/modelos.py, LimiteDinamico

### Community 42 - "E2E e verificação offline"
Cohesion: 0.33
Nodes (5): Camada 4b Playwright com API real e ativa v0002, Task 7: Integração localhost e E2E — implementada com alcance documentado, Ensaio HTTP histórico na v0001: saúde, sessão, explicações e 34/34 casos, Backend ensaiado com TCP/DNS externos bloqueados nos processos Python, R17: HTML Swagger 200 não comprova interface offline por dependência CDN

### Community 43 - "Cliente da API e erros"
Cohesion: 0.40
Nodes (5): API sobe sem a base (409 conflito em vez de 500), Formato unico de erro (codigos e X-Requisicao-Id), cliente tipado e ErroApi padronizado, PRODUCT.md e DESIGN.md a partir do protótipo, Task 1: Projeto, tokens e cliente API — implementada com alcance documentado

### Community 44 - "Ensaio humano e entrega final"
Cohesion: 0.40
Nodes (3): Pendentes: ensaio humano, material visual final e tempo oficial, Fechamento: editor, licença, contatos, ensaio humano e pacote final, Equipe informada com nomes, telefones e responsabilidades

### Community 45 - "Parecer e fatores de certeza"
Cohesion: 0.50
Nodes (4): Cortes de bloco nao lidos de meta.limiares, Percentual do parecer max(0, CF) x 100 (divergencia), parecer(): tres blocos, CF, percentuais, urgencia, Percentual max(0,CF)*100 e cortes de bloco por meta.limiares

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
- **149 isolated node(s):** `Arquivos kb_invalidas Secao 5.1`, `E15 cf_minimo e cf_maximo`, `E16 texto da tela de triagem`, `E17 ordem de limiares`, `E20 id_invalido` (+144 more)
  These have ≤1 connection - possible missing edges or undocumented components. (Counts symbols only; 186 node(s) total have ≤1 connection when file, concept and rationale nodes are included.)
- **18 thin communities (<3 nodes) omitted from report** — run `graphify query` to explore isolated nodes.

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **Why does `Índice da Seção 5 e consulta web; checkpoints históricos distinguidos` connect `Entrega e manutenção documental` to `Casos sintéticos na v0002`, `Regras e símbolos da v0002`, `Arquitetura e demonstração web`, `Riscos da interface integrada`, `Ensaio humano e entrega final`, `Demonstração e troca de modo`, `Processo documental verificável`, `Backend e isolamento do motor`, `Modelos e validação do kb`?**
  _High betweenness centrality (0.183) - this node is a cross-community bridge._
- **What connects `Arquivos kb_invalidas Secao 5.1`, `E15 cf_minimo e cf_maximo`, `E16 texto da tela de triagem` to the rest of the system?**
  _149 weakly-connected nodes found - possible documentation gaps or missing edges._
- **Should `Requisitos e arquitetura conceitual` be split into smaller, more focused modules?**
  _Cohesion score 0.05191146881287726 - nodes in this community are weakly interconnected._
- **Why does `Documento gerado da v0002: 56 regras, 51 símbolos e 8 doenças` connect `Regras e símbolos da v0002` to `Bandeiras de urgência`, `Tristeza parasitária bovina`, `Casos sintéticos na v0002`, `Arquitetura e demonstração web`, `Hipocalcemia e mobilidade`, `Demonstração e troca de modo`, `Processo documental verificável`, `Acidose e sinais digestivos`, `Cetose e início da lactação`, `Metrite e puerpério`, `Sinais térmicos e urgência`, `Entrega e manutenção documental`?**
  _High betweenness centrality (0.163) - this node is a cross-community bridge._
- **Should `Plano de API localhost` be split into smaller, more focused modules?**
  _Cohesion score 0.0671602326811211 - nodes in this community are weakly interconnected._

### Low-confidence Hints
_AMBIGUOUS edges — the extractor was unsure. Verify before acting on these._

- **What is the exact relationship between `Task 1` and `kb/__init__.py`?**
  _Edge tagged AMBIGUOUS (relation: references) - confidence is low._
- **What is the exact relationship between `Achado kb aceita base invalida` and `E14 cobre max fora de derivado`?**
  _Edge tagged AMBIGUOUS (relation: rationale_for) - confidence is low._
## Auditoria do bloco de troca de modo

- Uma atualização incremental ao fechar o bloco: 4 documentos e 310 linhas lidas integralmente, com SHA256 conferido.
- Preservados os 790 IDs do checkpoint anterior, com conceitos e descrições atualizados.
- Grafo usado para busca sob demanda; mudanças só em código ou web não exigem atualização.
- Demonstração documenta troca produtor/especialista sem reinício e correção térmica PATCH origem → PUT → PATCH destino, sob trava, com reconciliação GET.
- Editor gráfico e sensores ficam fora do escopo do PoC; conhecimento clínico continua suposição a validar.
- Origem documental legada corrigida em memória: 17 nós e 92 arestas marcados como AST; IDs preservados.
- Tokens e custo financeiro desta execução: indisponíveis, não medidos; zeros de esquema não são medições.
- Saídas escritas em graphify-out/ e obsidian/01-conhecimento/ na árvore de trabalho; sem stage, commit ou push pelo extrator.
