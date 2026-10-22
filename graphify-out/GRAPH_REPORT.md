# Graph Report - secao5-davi  (2026-10-22)

## Corpus Check
- 8 files · ~108,228 words
- Verdict: corpus is large enough that graph structure adds value.

## Summary
- 790 nodes · 1444 edges · 55 communities (40 shown, 15 thin omitted)
- Extraction: 91% EXTRACTED · 9% INFERRED · 0% AMBIGUOUS · INFERRED: 123 edges (avg confidence: 0.81)
- Token cost: indisponível; o agente hospedeiro não expõe uso medido nesta execução.

## Community Hubs (Navigation)
- Requisitos e arquitetura conceitual
- Plano de API localhost
- Persistência e validação da base
- Especificação do sistema especialista
- Casos sintéticos na v0002
- Pesquisa de ferramentas locais
- Sistema visual e componentes
- Sessões, API e motor
- Regras e símbolos da v0002
- Riscos da interface integrada
- Plano histórico frontend implementado
- Hipocalcemia e mobilidade
- Processo documental verificável
- Fontes clínicas contextuais
- Revisão do validador kb
- Snapshot e pressupostos do motor
- Produto e limites clínicos
- Agentes de implementação
- Acidose e sinais digestivos
- Cetose e início da lactação
- Consulta web e correções
- Metrite e puerpério
- Sinais térmicos e urgência
- Ledger de implementação kb
- Arquitetura e demonstração web
- Consulta integrada e pendências
- Contratos e integração localhost
- Entrega e manutenção documental
- Assistentes e instruções
- Ambiente e carregamento kb
- Correções finais da base
- Bandeiras de urgência
- Tristeza parasitária bovina
- Cliente da API e erros
- Ciclos de dependências
- Versionamento imutável da base
- Valores e serialização
- Módulos da base de conhecimento
- E2E e verificação offline
- Precisão numérica da interface
- Validação de grupos max
- Identificadores e telas
- Decisões sobre branches
- Histórico das bandeiras
- Limiares e fatores MYCIN
- Decisão sobre agentes
- Apresentação RERUM
- Documentário RERUM
- Adaptações entre API e motor
- Viabilidade das bandeiras
- Prioridades das regras
- Histórico do executor de casos

## God Nodes (most connected - your core abstractions)
1. `Documento gerado da v0002: 56 regras, 51 símbolos e 8 doenças` - 123 edges
2. `34 casos sintéticos aprovados na v0002 por executar_caso` - 40 edges
3. `v0002 ativa e imutável, pai v0001; ativação não valida clínica` - 39 edges
4. `Riscos abertos R01–R21, web integrada e checklist de fechamento` - 35 edges
5. `Sistema visual documentado do protótipo HackAtom` - 34 edges
6. `Plano histórico do frontend; implementação Tasks 1–8 documentada nas fontes atuais` - 32 edges
7. `CLAUDE.md do projeto (PoC Anamnese de Bovinos Leiteiros)` - 28 edges
8. `Arquitetura implementada: React→FastAPI→Sessao, kb/v0002 e SQLite` - 22 edges
9. `Plano de implementação API (Seção 4)` - 20 edges
10. `Camada web implementada: Início, Anamnese e Parecer` - 18 edges

## Surprising Connections (you probably didn't know these)
- `Cinco tarefas TDD do motor (vermelho antes do verde)` --semantically_similar_to--> `Testes com casos conhecidos por versao da base`  [INFERRED] [semantically similar]
  docs/superpowers/plans/2026-10-20-motor-secao-1.md → CLAUDE.md
- `Status de conferencia das fontes (L, R, N)` --semantically_similar_to--> `Marcacao de suposicao a validar (conhecimento veterinario)`  [INFERRED] [semantically similar]
  docs/fontes/fontes.md → CLAUDE.md
- `Estudo pendente: persistência integral de snapshot, ordem e versão da base` --semantically_similar_to--> `Restauração direta por snapshot integral, sem repetir o diálogo`  [INFERRED] [semantically similar]
  docs/processo/B.md → engine/README.md
- `Decisao deterministica, sem LLM nem rede no caminho` --semantically_similar_to--> `Motor independente de web, banco, LLM e servicos externos`  [INFERRED] [semantically similar]
  api/README.md → engine/README.md
- `Motor independente de web, banco, LLM e servicos externos` --semantically_similar_to--> `kb como pacote folha (nao importa engine)`  [INFERRED] [semantically similar]
  engine/README.md → kb/README.md

## Import Cycles
- None detected.

## Hyperedges (group relationships)
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

## Communities (55 total, 15 thin omitted)

### Community 0 - "Requisitos e arquitetura conceitual"
Cohesion: 0.07
Nodes (60): CLAUDE.md do projeto (PoC Anamnese de Bovinos Leiteiros), Aquisicao de conhecimento, Motor de regras em Python independente de interface, Base de conhecimento, Testes com casos conhecidos por versao da base, Componentes da arquitetura (modelo conceitual), Conteudo obrigatorio do plano final (12 itens), Criterios de avaliacao do hackathon (+52 more)

### Community 1 - "Plano de API localhost"
Cohesion: 0.07
Nodes (50): 27 endpoints da Seção 4.5, Bandeira vermelha e pausa de alerta, base_servico.py, casos_servico.py, Configuracao (api/config.py), Contexto e obter_contexto, criar_app / main.py, Pacote engine (motor) (+42 more)

### Community 2 - "Persistência e validação da base"
Cohesion: 0.05
Nodes (47): API README (api/), Backend FastAPI + SQLite (casca fina sobre motor e kb), Host confiavel (TrustedHostMiddleware contra DNS rebinding), Script rodar.ps1 / rodar.sh (execucao em localhost), Sementes de animais ficticios e reset seguro do banco, Servir web/dist com rota coringa propria (api/frontend.py), Sessao presa a versao da base com que nasceu, Variaveis ANAMNESE_BASE_DIR e ANAMNESE_DB (+39 more)

### Community 3 - "Especificação do sistema especialista"
Cohesion: 0.07
Nodes (48): Apresentação e roteiro da demonstração, Bandeiras vermelhas (chamar_agora), Base de conhecimento JSON versionada (kb/), Três camadas estritas (derivado, doença, urgência), Casos de teste conhecidos (31 casos), Contratos da API e formato único de erro, Correções e recálculo dos fatos, Critérios de parada (confirmação, limite, exaustão) (+40 more)

### Community 4 - "Casos sintéticos na v0002"
Cohesion: 0.10
Nodes (47): Exemplos sintéticos de alerta e sinais mamários pela CLI, Cetose / Hipercetonemia (cetose), Dermatite Digital Bovina (dermatite_digital), Deslocamento de Abomaso (deslocamento_abomaso), Mastite (mastite), R-BV-01: chamar_agora (CF 0,99), C-ACI-01: passou, observar, acidose, C-ACI-02: passou, observar, acidose (+39 more)

### Community 5 - "Pesquisa de ferramentas locais"
Cohesion: 0.05
Nodes (42): anthropics/skills (repositorio), brainstorming (skill), executing-plans (skill), frontend-design (skill), playwright-skill (lackeyjb), pptx (skill, source-available), Restricao de open source do hackathon, skill-creator (skill) (+34 more)

### Community 6 - "Sistema visual e componentes"
Cohesion: 0.07
Nodes (30): Barras role=meter com preenchimento sólido, Botão laranja primário e branco/verde secundário, Campo numérico textual preserva entrada ao erro, Composição desktop 1440 px derivada dos frames, Token cor/acento: #f0913a, Token cor/acento-escuro: #b9601a, Token cor/alerta: #e8a317, Token cor/creme: #f6f1e4 (+22 more)

### Community 7 - "Sessões, API e motor"
Cohesion: 0.10
Nodes (19): Comparacao de casos com a versao pai, Concorrencia: BEGIN IMMEDIATE e conferencia de revisao, Importacao de animais CSV/JSON sem 500, ordem_respostas no snapshot (reprocessar lotes na correcao), Portao de ativacao de versao (casos_falhando, confirmar_falhas), Cortes de bloco nao lidos de meta.limiares, Percentual do parecer max(0, CF) x 100 (divergencia), Bandeira vermelha: pausa, continuar, ver_parecer (+11 more)

### Community 8 - "Regras e símbolos da v0002"
Cohesion: 0.14
Nodes (24): BHB sanguíneo (bhb_sanguineo), CMT reagente (cmt_reagente), Evidência agrupada de alteração do leite (evidencia_alteracao_leite), Corpos cetônicos na urina (fita_urina_corpos_cetonicos), Alteração visível do leite (leite_alterado), Lesão característica no talão (lesao_erosiva_talao_morango), Monitoramento Clínico Contínuo (observar), Ping no flanco esquerdo (ping_metalico_flanco_esquerdo) (+16 more)

### Community 9 - "Riscos da interface integrada"
Cohesion: 0.11
Nodes (20): Demo web de 4 min: erro 422, mastite 80 e alerta por decúbito, UI preservou regras, versões imutáveis, contratos e API/motor/kb, Verificação web: oito E2E Chromium, seis telas e axe selecionado, R01: Conhecimento clínico e CF sem validação especializada, R02: Confiança excessiva por sinais correlacionados, R03: Falso entendimento de `sem_problema`, R04: Editor gráfico ainda pendente, R05: Regressão na restauração da sessão (+12 more)

### Community 10 - "Plano histórico frontend implementado"
Cohesion: 0.13
Nodes (14): Varela Round em títulos e Nunito Sans no conteúdo, Botao, opções, numérico, confiança, boi, balão, progresso e modal, tokens cor/* do Figma, Varela Round e Nunito Sans, hipóteses desde segunda pergunta e explicação Por quê, início cria animal anônimo e sessão no modo escolhido, Vocabulário pt-BR: verificação, especialista, produtor e parecer, audit/polish, responsivo 375/768/1024/1440 e estados, Plano histórico do frontend; implementação Tasks 1–8 documentada nas fontes atuais (+6 more)

### Community 11 - "Hipocalcemia e mobilidade"
Cohesion: 0.11
Nodes (19): Cálcio sérico total (calcio_serico), Claudicação (claudicacao), Decúbito (decubito), Dias em lactação (dias_em_lactacao), Dor na região do talão (dor_flexao_talao), Hipocalcemia Puerperal (hipocalcemia), Periparto imediato (periparto_imediato), Desvio cervical em S (pescoco_em_s) (+11 more)

### Community 12 - "Processo documental verificável"
Cohesion: 0.20
Nodes (14): Checkpoint codex-davi: Histórico: correções do motor e integração de desenvolvimento em 898512c, Checkpoint codex-davi: Processo verificável do checkpoint de 21/10/2026, Pendentes: ensaio humano sem Wi-Fi, reserva, contatos e arquivos finais, Roteiro: consulta React em localhost e CLI de reserva, Preparação: 10 minutos de fala mais 4 de demo; alternativa de 5 minutos, Fechamento: editor, licença, contatos, ensaio humano e pacote final, Equipe informada: Caio, Davi e Luis; telefones ainda pendentes, Papel A: pessoa, blocos reais, decisões humanas e aprendizado a completar (+6 more)

### Community 13 - "Fontes clínicas contextuais"
Cohesion: 0.15
Nodes (15): Acidose ruminal (categoria), Acidose ruminal subaguda, Anaplasmose, Babesiose, Cetose bovina (hiperCetonemia), Dermatite digital, Deslocamento de abomaso, Embrapa ADM158 (tristeza parasitaria) (+7 more)

### Community 14 - "Revisão do validador kb"
Cohesion: 0.13
Nodes (11): Achado E06 doenca sem regra, Arquivos kb_invalidas Secao 5.1, E08 bandeira sem triagem, E11 criterio de triagem, E15 cf_minimo e cf_maximo, E16 texto da tela de triagem, E17 ordem de limiares, E20 id_invalido (+3 more)

### Community 15 - "Snapshot e pressupostos do motor"
Cohesion: 0.17
Nodes (6): Base de desenvolvimento 3.1.0-revisao1: 51 símbolos, 56 regras, 8 doenças e 6 telas, Achados procedentes de motor, restauração e contrato de dados, Log de revisões: evidência e proveniência do checkpoint, Ajustes propostos: max mamário e caminhos de TPB sem febre, Motor Python 3.12+ independente de web, banco, LLM e serviços externos, Sessao: triagem, diálogo, modo, bandeiras, parecer e porque/como

### Community 16 - "Produto e limites clínicos"
Cohesion: 0.12
Nodes (16): Identidade Figma e autoridade API preservadas, Alerta não fecha por Esc/fundo; outros diálogos devolvem foco, Valores brutos, 422 preservado e 409 relê sem repetir mutação, Pausa exige alerta mesmo com proxima nulo, Produto: Anamnese Bovina explicável, Rede, base ausente, carregamento, duplo envio e 409, Percentual é confiança do sistema; regras não validadas, Prova de conceito localhost com casos e animais fictícios (+8 more)

### Community 17 - "Agentes de implementação"
Cohesion: 0.16
Nodes (10): Alocacao de agente principal e alternativa por prompt de revisao, anthropics/skills (pptx, docx, pdf, webapp-testing, frontend-design), Antigravity (plano Pro), Claude Code (Claude Pro), Codex (ChatGPT Plus), Gemini Pro (Google AI Pro, app web), Implementacao por pessoa (A, B, C) com agente principal e reserva, Fontes do projeto (fontes oficiais e de dominio) (+2 more)

### Community 18 - "Acidose e sinais digestivos"
Cohesion: 0.17
Nodes (13): Acidose Ruminal (acidose), Diarreia (diarreia), Fezes com espuma e grãos (fezes_aquosas_espuma_graos), Mudança abrupta de concentrado (mudanca_abrupta_concentrado), pH ruminal (ph_ruminal), R-ACI-01: acidose (CF 0,35), R-ACI-02: acidose (CF 0,55), R-ACI-03: acidose (CF 0,5) (+5 more)

### Community 19 - "Cetose e início da lactação"
Cohesion: 0.18
Nodes (13): Apetite (apetite), Flanco esquerdo afundado (flanco_esquerdo_afundado), Hálito adocicado (halito_adocicado_acetona), Inicio lactacao (inicio_lactacao), Queda de produção de leite (queda_producao), R-BV-03: chamar_agora (CF 0,99), R-CET-01: cetose (CF 0,4), R-CET-02: cetose (CF 0,5) (+5 more)

### Community 20 - "Consulta web e correções"
Cohesion: 0.23
Nodes (9): Fontes/SVG/CSS locais e E2E com SQLite temporário/v0002, Top 4 desde segunda pergunta; porquê/como e regras do backend, Voltar/PUT limitado à navegação atual, Tipos OpenAPI gerados e cliente centraliza erros, Camada web implementada: Início, Anamnese e Parecer, R19: histórico de correção restrito à navegação atual, parecer de oito doenças, blocos e Como cheguei aqui, Task 5: Alerta de bandeira — implementada com alcance documentado (+1 more)

### Community 21 - "Metrite e puerpério"
Cohesion: 0.23
Nodes (12): Corrimento vaginal fétido (corrimento_fetido), Corrimento vaginal (corrimento_vaginal), Metrite Puerperal (metrite), Puerperio (puerperio), R-DER-02: puerperio (CF 0,99), R-MET-01: metrite (CF 0,75), R-MET-02: metrite (CF 0,45), R-MET-03: metrite (CF 0,35) (+4 more)

### Community 22 - "Sinais térmicos e urgência"
Cohesion: 0.24
Nodes (12): Temperatura ao toque das extremidades (extremidades), Febre (febre), Hipotermia (hipotermia), R-DER-04: febre (CF 0,95), R-DER-05: hipotermia (CF 0,85), R-DER-06: hipotermia (CF 0,6), R-DER-07: febre (CF 0,45), R-DER-08: febre (CF -0,9) (+4 more)

### Community 23 - "Ledger de implementação kb"
Cohesion: 0.23
Nodes (10): Achado fato numerico inerte no teste, Ambiente venv, engine.modelos.Base.de_dict, .gitattributes, Pacote engine, SDD ledger, Spec anamnese bovinos, Task 6 (+2 more)

### Community 24 - "Arquitetura e demonstração web"
Cohesion: 0.20
Nodes (3): Arquitetura implementada: React→FastAPI→Sessao, kb/v0002 e SQLite, Motor padrão; API em .[dev] e build web com Node 24/lockfile npm, Sete componentes do modelo dos organizadores

### Community 25 - "Consulta integrada e pendências"
Cohesion: 0.20
Nodes (9): Integração implementada: React, FastAPI/Pydantic, SQLite e scripts localhost, Exigências: consulta web localhost e E2E disponíveis; editor e entrega final pendentes, Papel B planejado: API, contratos, validação editorial, scripts e persistência, Pendências: editor gráfico, licença, telefones e validação clínica, HackAtom: anamnese explicável com interface React integrada, Integração implementada: React, motor, v0002, kb, FastAPI e SQLite, Inicializador preserva banco/build e compila SPA se ausente, Vitest/build e Playwright com API própria/SQLite temporário (+1 more)

### Community 26 - "Contratos e integração localhost"
Cohesion: 0.22
Nodes (5): Contrato OpenAPI versionado e exemplos por operationId, Notas para o frontend (proxima nulo, reabrir, 409 conflito), Testes da API (pytest, marca lento, base minima de fixtures), Checkpoint codex-davi: IA aplicada ao desenvolvimento e à documentação, fora da consulta, Contratos de sessão, parecer, porque/como e snapshot integral

### Community 27 - "Entrega e manutenção documental"
Cohesion: 0.22
Nodes (6): Proveniência: v0002 ativa, pai v0001, 56 regras sem validação clínica, Envio: alvo interno 22/10 às 18:30 e prazo oficial às 20:00, Datas oficiais: entrega 22/10/2026 20h; apresentação 23/10/2026 09h, 1066 testes Python, 170 subtestes, 39 testes de interface e 8 E2E; 34 casos sintéticos, Índice da Seção 5 e da consulta web integrada na codex-davi, Plano: extração semântica, atualização Graphify e exportação Obsidian

### Community 28 - "Assistentes e instruções"
Cohesion: 0.42
Nodes (9): AGENTS.md (instrucoes do projeto), Google Antigravity (app, IDE e CLI), Claude Code, CLAUDE.md (instrucoes do projeto), OpenAI Codex (CLI, IDE, app desktop), Gemini CLI, GEMINI.md (instrucoes do projeto), Limites de uso dos planos (+1 more)

### Community 29 - "Ambiente e carregamento kb"
Cohesion: 0.28
Nodes (7): Achado carregar_base excecoes nativas, Achado prioridade zero no teste, carregar_base, Plano kb secao 2, pyproject.toml, Task 1, tests/kb/test_modelos.py

### Community 30 - "Correções finais da base"
Cohesion: 0.28
Nodes (7): Achado kb aceita base invalida, Achado ordem ausente no contrato, Aresta.ordem, kb/__init__.py, para_motor, Revisao final, validar_edicao

### Community 31 - "Bandeiras de urgência"
Cohesion: 0.29
Nodes (8): Apatia (apatia), Atendimento Veterinário Imediato (chamar_agora), R-BV-04: chamar_agora (CF 0,99), R-BV-05: chamar_agora (CF 0,99), R-BV-06: chamar_agora (CF 0,99), R-MAS-02: mastite (CF 0,5), R-URG-03: chamar_agora (CF 0,99), Inflamação do úbere (ubere_inflamado)

### Community 32 - "Tristeza parasitária bovina"
Cohesion: 0.25
Nodes (8): Exposição recente a carrapatos (carrapatos_historico_recente), Hemoparasitas no esfregaço (esfregaco_hemoparasitas), Mucosas pálidas ou amareladas (mucosas_palidas_ou_ictericas), R-TPB-02: tpb (CF 0,6), R-TPB-03: tpb (CF 0,35), R-TPB-04: tpb (CF 0,9), R-URG-02: chamar_agora (CF 0,99), Tristeza Parasitária Bovina (tpb)

### Community 33 - "Cliente da API e erros"
Cohesion: 0.29
Nodes (6): API sobe sem a base (409 conflito em vez de 500), Formato unico de erro (codigos e X-Requisicao-Id), Mapa de 27 rotas por arquivo (prefixo /api), cliente tipado e ErroApi padronizado, PRODUCT.md e DESIGN.md a partir do protótipo, Task 1: Projeto, tokens e cliente API — implementada com alcance documentado

### Community 34 - "Ciclos de dependências"
Cohesion: 0.43
Nodes (6): Achado direcao do caminho do ciclo, Achado op e negado None viram default, encontrar_ciclo, kb/grafo.py, Task 2, Task 3

### Community 35 - "Versionamento imutável da base"
Cohesion: 0.53
Nodes (5): Achado temporario fixo ativa.json.tmp, Achado pai explicito nao verificado, ativa.json, salvar_nova, Task 5

### Community 36 - "Valores e serialização"
Cohesion: 0.40
Nodes (4): Achado Condicao valor int, Condicao.valor, E03 valor_invalido, model_fields_set da Aresta

### Community 37 - "Módulos da base de conhecimento"
Cohesion: 0.33
Nodes (4): kb/analise.py, kb/carregador.py, kb/modelos.py, LimiteDinamico

### Community 38 - "E2E e verificação offline"
Cohesion: 0.33
Nodes (5): Camada 4b Playwright com API real e ativa v0002, Task 7: Integração localhost e E2E — implementada com alcance documentado, Ensaio HTTP histórico na v0001: saúde, sessão, explicações e 34/34 casos, Backend ensaiado com TCP/DNS externos bloqueados nos processos Python, R17: HTML Swagger 200 não comprova interface offline por dependência CDN

### Community 39 - "Precisão numérica da interface"
Cohesion: 0.50
Nodes (3): v0002 explicita limites e casas decimais, Precisão não exposta por proxima; backend valida casas decimais, R18: casas_decimais ausente no contrato da próxima pergunta

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
- **147 isolated node(s):** `graphify --update`, `.graphifyignore (escopo do grafo)`, `Arquivos kb_invalidas Secao 5.1`, `E15 cf_minimo e cf_maximo`, `E16 texto da tela de triagem` (+142 more)
  These have ≤1 connection - possible missing edges or undocumented components. (Counts symbols only; 181 node(s) total have ≤1 connection when file, concept and rationale nodes are included.)
- **15 thin communities (<3 nodes) omitted from report** — run `graphify query` to explore isolated nodes.

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **Why does `Documento gerado da v0002: 56 regras, 51 símbolos e 8 doenças` connect `Regras e símbolos da v0002` to `Tristeza parasitária bovina`, `Casos sintéticos na v0002`, `Hipocalcemia e mobilidade`, `Processo documental verificável`, `Snapshot e pressupostos do motor`, `Acidose e sinais digestivos`, `Cetose e início da lactação`, `Metrite e puerpério`, `Sinais térmicos e urgência`, `Arquitetura e demonstração web`, `Consulta integrada e pendências`, `Entrega e manutenção documental`, `Bandeiras de urgência`?**
  _High betweenness centrality (0.125) - this node is a cross-community bridge._
- **What connects `graphify --update`, `.graphifyignore (escopo do grafo)`, `Arquivos kb_invalidas Secao 5.1` to the rest of the system?**
  _147 weakly-connected nodes found - possible documentation gaps or missing edges._
- **Should `Requisitos e arquitetura conceitual` be split into smaller, more focused modules?**
  _Cohesion score 0.06584723441615452 - nodes in this community are weakly interconnected._
- **Why does `Arquitetura implementada: React→FastAPI→Sessao, kb/v0002 e SQLite` connect `Arquitetura e demonstração web` to `Casos sintéticos na v0002`, `Precisão numérica da interface`, `Regras e símbolos da v0002`, `Riscos da interface integrada`, `Processo documental verificável`, `Snapshot e pressupostos do motor`, `Consulta web e correções`, `Consulta integrada e pendências`, `Contratos e integração localhost`, `Entrega e manutenção documental`?**
  _High betweenness centrality (0.077) - this node is a cross-community bridge._
- **Should `Plano de API localhost` be split into smaller, more focused modules?**
  _Cohesion score 0.0671602326811211 - nodes in this community are weakly interconnected._

### Low-confidence Hints
_AMBIGUOUS edges — the extractor was unsure. Verify before acting on these._

- **What is the exact relationship between `Task 1` and `kb/__init__.py`?**
  _Edge tagged AMBIGUOUS (relation: references) - confidence is low._
- **What is the exact relationship between `Achado kb aceita base invalida` and `E14 cobre max fora de derivado`?**
  _Edge tagged AMBIGUOUS (relation: rationale_for) - confidence is low._
## Auditoria da atualização documental frontend

- Corpus detectado: 44 arquivos; 7 documentos novos/alterados e 1 plano reextraído para refletir o estado atual.
- Nenhuma mudança de código no corpus documental; web/ e docs/entrega/capturas/ excluídos conforme .graphifyignore.
- Todos os 718 IDs anteriores foram preservados, com descrições corrigidas onde necessário.
- Leitura integral dos 8 documentos verificada por contagem de linhas e SHA256.
- Frontend das Tasks 1–8 implementado conforme documentos atuais; editor gráfico e validação clínica permanecem pendentes.
- Tokens e custo financeiro desta execução: indisponíveis, não medidos. Zeros internos do esquema não representam medição.
- A tentativa anterior foi interrompida por limite de uso antes da publicação; esta rodada foi retomada com nova verificação de hashes.
- `graphify-out/` e `obsidian/01-conhecimento/` foram atualizados na árvore de trabalho; nenhum commit ou stage foi feito por esta atualização.
