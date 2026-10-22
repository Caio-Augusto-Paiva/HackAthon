# Graph Report - HackAtom  (2026-10-22)

## Corpus Check
- 13 files · ~132,489 words
- Verdict: corpus is large enough that graph structure adds value.

## Summary
- 1287 nodes · 2145 edges · 98 communities (77 shown, 21 thin omitted)
- Extraction: 86% EXTRACTED · 13% INFERRED · 0% AMBIGUOUS · INFERRED: 287 edges (avg confidence: 0.84)
- Token cost: 0 input · 0 output

## Community Hubs (Navigation)
- Modos e exemplos de alerta
- Parecer e urgência na interface
- Documentação e backend FastAPI
- Skills e agentes de IA
- Identidade visual e campos
- Regras de produção e CF
- Base de desenvolvimento e sessões
- Riscos e pendências de entrega
- Concorrência e snapshot de sessão
- Roteiro de apresentação
- Perguntas da banca sobre IA
- Bandeira vermelha e desvios
- Cliente tipado e tipografia
- Diário de bordo 22/10
- Motor e API FastAPI
- Demo cronometrada e avisos
- Serviços da casca fina
- Cliente nunca envia CF
- Alerta de bandeira e SPA
- Aquisição de conhecimento
- Diário de bordo 20-21/10
- Perguntas sobre uso offline
- Achados de base inválida
- Barra de confiança e Boi
- Alocação de agentes de IA
- Combinação MYCIN e blocos
- Hipocalcemia e periparto
- Exigências oficiais da entrega
- AGENTS.md e Codex
- Decisões de seleção de perguntas
- TPB e derivado febre
- Atualização do grafo
- Processo de desenvolvimento
- Decisões de reprocessamento
- Cetose e deslocamento de abomaso
- Fonte inválida e Review Focus
- Doenças e acidose ruminal
- Regras do modo bovino urgente
- Demonstração principal local
- Ambiente venv e testes
- Busca direta versus grafo
- Decisão determinística auditável
- Fechamento de interface
- Decisões rejeitadas e passos
- Passo a passo pedido
- Arrumação e rótulos do grafo
- CLI de fonte por doença
- Avaliação da organização
- Duração e fechamento da seção
- Critérios de parada
- Exportação do grafo de dados
- API pública da base
- Fonte separada por doença
- Camadas de inferência
- Metrite e puerpério
- Dermatite digital
- Mastite
- Ferramentas de IA e AGENTS
- Achados do carregador
- Achados do contrato de aresta
- Contrato OpenAPI e exemplos
- Casos clínicos e fonte
- Base ausente e contrato
- Ausência de validação clínica
- Configuração da API
- Acessibilidade e Figma
- Estrutura de pastas
- Caminho do ciclo
- READMEs e caso alerta
- Fonte do grafo 2
- Casos esperados e hackathon
- Acidose ruminal regras
- Achados de ativa.json
- Validação de Condicao
- Análise e carregador
- Arquitetura de kb
- Falhas de API na interface
- Derivado max negativo
- Erros E02 e E21
- Branch de trabalho
- Bandeira após correção
- Limiares e MYCIN
- Agentes e skills por prompt
- Skills não confirmadas
- Embrapa tristeza parasitária
- Transcrição RERUM apresentação
- Regulamento e cronograma
- Transcrição do documentário
- Adaptações da API
- Bandeiras não verificadas
- Prioridade padrão por classe
- Executor de casos incompleto
- Sessão e triagem

## God Nodes (most connected - your core abstractions)
1. `Casos de teste (documentação gerada)` - 42 edges
2. `Base de conhecimento v0004` - 42 edges
3. `engine.casos.executar_caso` - 36 edges
4. `Seção: tabela-resumo dos casos` - 35 edges
5. `Caso fictício de regressão; suposição a validar` - 35 edges
6. `Sistema visual documentado do protótipo HackAtom` - 33 edges
7. `Modo produtor` - 26 edges
8. `Revisão técnica documental da Seção 6, sem validação clínica ou ensaio humano` - 25 edges
9. `Plano de implementação API (Seção 4)` - 21 edges
10. `Task 1` - 17 edges

## Surprising Connections (you probably didn't know these)
- `Decisao deterministica, sem LLM nem rede no caminho` --semantically_similar_to--> `Motor independente de web, banco, LLM e servicos externos`  [INFERRED] [semantically similar]
  api/README.md → engine/README.md
- `Motor independente de web, banco, LLM e servicos externos` --semantically_similar_to--> `kb como pacote folha (nao importa engine)`  [INFERRED] [semantically similar]
  engine/README.md → kb/README.md
- `Estudo humano pendente: snapshot persistido, ordem das respostas e versão da sessão` --semantically_similar_to--> `Restauração direta por snapshot integral, sem repetir o diálogo`  [INFERRED] [semantically similar]
  docs/processo/B.md → engine/README.md
- `Cinco tarefas TDD do motor (vermelho antes do verde)` --semantically_similar_to--> `Casos de teste com resultado esperado por versao da base`  [INFERRED] [semantically similar]
  docs/superpowers/plans/2026-10-20-motor-secao-1.md → CLAUDE.md
- `Status de conferencia das fontes (L, R, N)` --semantically_similar_to--> `Conhecimento veterinario sempre suposicao a validar, citando fonte`  [INFERRED] [semantically similar]
  docs/fontes/fontes.md → CLAUDE.md

## Import Cycles
- None detected.

## Hyperedges (group relationships)
- **Identidade documentada: cores com acento rosa, fontes, composição, profundidade e SVGs** — design_sistema_visual, design_tipografia, design_composicao_desktop, design_profundidade, design_formas [EXTRACTED 1.00]
- **Geração de regras/casos e verificação de sincronismo documental** — docs_superpowers_plans_2026_10_21_documentacao_entrega_parcial_geracao_verificacao_docs [EXTRACTED 1.00]
- **Camadas api -> engine -> kb (dependencia unidirecional)** — api_readme_backend_fastapi_sqlite, engine_readme_sessao, kb_readme_modelos, kb_readme_para_motor [EXTRACTED 1.00]
- **Pacotes api -> engine -> kb e web** — docs_superpowers_specs_2026_10_20_anamnese_bovinos_design_pacote_api, docs_superpowers_specs_2026_10_20_anamnese_bovinos_design_pacote_engine, docs_superpowers_specs_2026_10_20_anamnese_bovinos_design_pacote_kb, docs_superpowers_specs_2026_10_20_anamnese_bovinos_design_pacote_web [EXTRACTED 1.00]
- **Camadas da API: rotas finas, serviços, repositórios** — docs_superpowers_plans_2026_10_21_api_secao_4_arquitetura_casca_fina, docs_superpowers_plans_2026_10_21_api_secao_4_sessao_servico, docs_superpowers_plans_2026_10_21_api_secao_4_repositorios, docs_superpowers_plans_2026_10_21_api_secao_4_contexto [EXTRACTED 1.00]
- **Ciclo de edição e validação da base** — docs_superpowers_specs_2026_10_20_anamnese_bovinos_design_editor_grafico, docs_superpowers_specs_2026_10_20_anamnese_bovinos_design_validador_kb, docs_superpowers_specs_2026_10_20_anamnese_bovinos_design_versionamento_imutavel, docs_superpowers_specs_2026_10_20_anamnese_bovinos_design_casos_teste [EXTRACTED 1.00]
- **Componentes do modelo conceitual** — claude_base_conhecimento, claude_motor_de_inferencia, claude_memoria_de_trabalho, claude_modulo_explicacao, claude_interface_usuario, claude_aquisicao_conhecimento, claude_fontes_dados_externas [EXTRACTED 1.00]
- **Restricoes obrigatorias do desafio** — claude_restricao_nao_usar_llm, claude_restricao_decisao_deterministica, claude_restricao_open_source, claude_restricao_localhost, claude_desenvolvimento_com_ia [EXTRACTED 1.00]
- **Congelamento do contrato da API** — docs_superpowers_plans_2026_10_21_api_secao_4_registro_contratos, docs_superpowers_plans_2026_10_21_api_secao_4_exemplos_contrato, docs_superpowers_plans_2026_10_21_api_secao_4_openapi_json, docs_superpowers_plans_2026_10_21_api_secao_4_exportar_openapi, docs_superpowers_plans_2026_10_21_api_secao_4_d6 [EXTRACTED 1.00]
- **Divergencias e lacunas da revisao do motor (21/10/2026)** — docs_revisoes_2026_10_21_revisao_motor_bandeira_apos_correcao, docs_revisoes_2026_10_21_revisao_motor_percentual_parecer, docs_revisoes_2026_10_21_revisao_motor_restauracao_sessao, docs_revisoes_2026_10_21_revisao_motor_traco_sessao, docs_revisoes_2026_10_21_revisao_motor_executor_casos [EXTRACTED 1.00]
- **Tasks 1-8 do frontend** — docs_superpowers_plans_2026_10_22_frontend_web_task_1, docs_superpowers_plans_2026_10_22_frontend_web_task_2, docs_superpowers_plans_2026_10_22_frontend_web_task_3, docs_superpowers_plans_2026_10_22_frontend_web_task_4, docs_superpowers_plans_2026_10_22_frontend_web_task_5, docs_superpowers_plans_2026_10_22_frontend_web_task_6, docs_superpowers_plans_2026_10_22_frontend_web_task_7, docs_superpowers_plans_2026_10_22_frontend_web_task_8 [EXTRACTED 1.00]
- **Pipeline base -> fonte por doença -> grafo exato -> cofre Obsidian** — docs_superpowers_plans_2026_10_22_grafo_dados_por_doenca_fonte_py, docs_superpowers_plans_2026_10_22_grafo_dados_por_doenca_exportar_py, docs_superpowers_plans_2026_10_22_grafo_dados_por_doenca_script_grafo_dados [EXTRACTED 1.00]
- **Persistencia e restauracao de sessao sem replay** — api_readme_d1_snapshot_json, api_readme_ordem_respostas, engine_readme_restaurar_exportar, engine_readme_correcao_reprocessa_lotes [EXTRACTED 1.00]
- **Reconstrução da sessão a cada requisição via snapshot** — docs_superpowers_plans_2026_10_21_api_secao_4_motor_sem_estado, docs_superpowers_plans_2026_10_21_api_secao_4_snapshot_json, docs_superpowers_plans_2026_10_21_api_secao_4_sessao_motor, docs_superpowers_plans_2026_10_21_api_secao_4_montar_estado, docs_superpowers_plans_2026_10_21_api_secao_4_d2 [EXTRACTED 1.00]
- **Arquivos de base/fonte (comum, doenca, indice)** — docs_superpowers_specs_2026_10_22_grafo_dados_por_doenca_design_comum_json, docs_superpowers_specs_2026_10_22_grafo_dados_por_doenca_design_doenca_json, docs_superpowers_specs_2026_10_22_grafo_dados_por_doenca_design_indice_json [EXTRACTED 1.00]
- **Três camadas de avaliação de regras** — docs_superpowers_specs_2026_10_20_anamnese_bovinos_design_derivados_sinais, docs_superpowers_specs_2026_10_20_anamnese_bovinos_design_dominio_8_doencas, docs_superpowers_specs_2026_10_20_anamnese_bovinos_design_urgencia_gravidade_confianca, docs_superpowers_specs_2026_10_20_anamnese_bovinos_design_bandeiras_vermelhas, docs_superpowers_specs_2026_10_20_anamnese_bovinos_design_camadas_tres [EXTRACTED 1.00]
- **Premissas de instalacao no Windows a validar** — docs_pesquisa_suposicoes_linha_24_node, docs_pesquisa_suposicoes_rodar_ps1, docs_pesquisa_suposicoes_winget_uv_id, docs_pesquisa_suposicoes_vite_mocks, docs_pesquisa_suposicoes_windows_11_demo, docs_pesquisa_execucao_local_powershell_execution_policy [INFERRED 0.75]
- **Versionamento imutável com validação prévia** — docs_superpowers_plans_2026_10_21_kb_secao_2_task5_carregador, kb_readme_validador [INFERRED 0.75]
- **Ambiente e portabilidade do kb e do motor** — docs_revisoes_2026_10_21_ledger_kb_secao_2_ambiente_venv_python_3_12, docs_revisoes_2026_10_21_ledger_kb_secao_2_comando_de_teste_do_motor_com_python_do_sistema, docs_revisoes_2026_10_21_ledger_kb_secao_2_gitattributes_eol_lf [INFERRED 0.85]
- **Ciclo de versao da base: validar, salvar, executar casos, ativar** — kb_readme_validador, kb_readme_carregador_repositorio, engine_readme_executar_caso, api_readme_portao_ativacao, api_readme_comparacao_versao_pai [INFERRED 0.85]
- **Decisoes de processo da Secao 2** — docs_revisoes_2026_10_21_ledger_kb_secao_2_execucao_sequencial_das_tarefas, docs_revisoes_2026_10_21_ledger_kb_secao_2_sem_worktree_no_branch, docs_revisoes_2026_10_21_ledger_kb_secao_2_casos_invalidos_como_mutacoes_pytest, docs_revisoes_2026_10_21_ledger_kb_secao_2_modulos_do_kb_implementados_aqui [INFERRED 0.85]
- **Pipeline de planejamento e execucao com skills (obra/superpowers)** — docs_pesquisa_agentes_e_skills_brainstorming, docs_pesquisa_agentes_e_skills_writing_plans, docs_pesquisa_agentes_e_skills_executing_plans, docs_pesquisa_agentes_e_skills_test_driven_development, docs_pesquisa_agentes_e_skills_subagent_driven_development [INFERRED 0.85]
- **Stack de execucao local em localhost** — docs_pesquisa_execucao_local_fastapi_frontend, docs_pesquisa_execucao_local_vite, docs_pesquisa_execucao_local_uv, docs_pesquisa_execucao_local_playwright_webserver, docs_pesquisa_versoes_bibliotecas_uvicorn [INFERRED 0.85]
- **Regras do validador e codigos de erro** — docs_revisoes_2026_10_21_ledger_kb_secao_2_formato_de_id_gera_e20, docs_revisoes_2026_10_21_ledger_kb_secao_2_valor_none_gera_e03, docs_revisoes_2026_10_21_ledger_kb_secao_2_e08_so_sem_condicao_de_triagem, docs_revisoes_2026_10_21_ledger_kb_secao_2_e15_cf_min_e_max_juntos, docs_revisoes_2026_10_21_ledger_kb_secao_2_e16_exige_texto_nos_dois_modos, docs_revisoes_2026_10_21_ledger_kb_secao_2_e17_estrito_com_pivo_zero, docs_revisoes_2026_10_21_ledger_kb_secao_2_e14_cobre_max_fora_de_derivado, docs_revisoes_2026_10_21_ledger_kb_secao_2_novo_e21_tela_simbolo_invalido [INFERRED 0.85]
- **Sete componentes do modelo conceitual dos organizadores** — docs_entrega_02_arquitetura_comp_interface, docs_entrega_02_arquitetura_comp_motor, docs_entrega_02_arquitetura_comp_base, docs_entrega_02_arquitetura_comp_memoria, docs_entrega_02_arquitetura_comp_explicacao, docs_entrega_02_arquitetura_comp_aquisicao, docs_entrega_02_arquitetura_comp_fontes_externas [EXTRACTED 1.00]
- **Pacote de documentação obrigatória da entrega (processo, arquitetura, regras, casos, apresentação, riscos)** — docs_entrega_01_processo, docs_entrega_02_arquitetura, docs_entrega_readme_doc_03_regras, docs_entrega_readme_doc_04_casos, docs_entrega_readme_doc_05_apresentacao, docs_entrega_readme_doc_06_riscos [EXTRACTED 1.00]
- **Fluxo de cálculo de certeza (observação, CF da premissa, combinação, parecer)** — docs_entrega_02_arquitetura_observacao, docs_entrega_02_arquitetura_cf_premissa_minimo, docs_entrega_02_arquitetura_combinacao_cf, docs_entrega_02_arquitetura_blocos_parecer [INFERRED 0.95]
- **Regras que derivam febre e hipotermia** — docs_entrega_03_regras_de_producao_r_der_04, docs_entrega_03_regras_de_producao_r_der_07, docs_entrega_03_regras_de_producao_r_der_08, docs_entrega_03_regras_de_producao_r_der_10, docs_entrega_03_regras_de_producao_der_febre [EXTRACTED 1.00]
- **Grupo de evidência do leite (max) alimentando mastite** — docs_entrega_03_regras_de_producao_r_mas_01, docs_entrega_03_regras_de_producao_r_mas_03, docs_entrega_03_regras_de_producao_r_mas_05, docs_entrega_03_regras_de_producao_der_evidencia_leite, docs_entrega_03_regras_de_producao_combinacao_max [EXTRACTED 1.00]
- **Fluxo de triagem em três camadas** — docs_entrega_03_regras_de_producao_camada1, docs_entrega_03_regras_de_producao_camada2, docs_entrega_03_regras_de_producao_camada3, docs_entrega_03_regras_de_producao_urg_chamar_agora, docs_entrega_03_regras_de_producao_urg_observar [INFERRED 0.85]
- **Casos ambíguos sem sinal adicional (R15)** — docs_entrega_04_casos_de_teste_c_met_03, docs_entrega_04_casos_de_teste_c_tpb_03, docs_entrega_04_casos_de_teste_c_hip_03, docs_entrega_04_casos_de_teste_c_dab_03, docs_entrega_04_casos_de_teste_c_aci_03 [EXTRACTED 1.00]
- **Casos com pausa de alerta** — docs_entrega_04_casos_de_teste_c_tpb_01, docs_entrega_04_casos_de_teste_c_hip_01, docs_entrega_04_casos_de_teste_c_bv_01, docs_entrega_04_casos_de_teste_c_bv_02, docs_entrega_04_casos_de_teste_dev_bv_01 [EXTRACTED 1.00]
- **Casos que testam bandeiras R-BV** — docs_entrega_04_casos_de_teste_c_mas_02, docs_entrega_04_casos_de_teste_c_hip_02, docs_entrega_04_casos_de_teste_c_bv_01, docs_entrega_04_casos_de_teste_c_bv_02, docs_entrega_04_casos_de_teste_c_bv_03 [INFERRED 0.85]
- **Sequência dos 7 passos da demonstração de 4 minutos** — docs_entrega_05_apresentacao_e_demo_demo_passo1_inicio, docs_entrega_05_apresentacao_e_demo_demo_passo2_validacao, docs_entrega_05_apresentacao_e_demo_demo_passo3_produtor_mastite, docs_entrega_05_apresentacao_e_demo_demo_passo4_troca_especialista, docs_entrega_05_apresentacao_e_demo_demo_passo5_parecer_como, docs_entrega_05_apresentacao_e_demo_demo_passo6_alerta_hipocalcemia, docs_entrega_05_apresentacao_e_demo_demo_passo7_relatorio_limites [EXTRACTED 1.00]
- **Riscos clínicos e de interpretação do CF** — docs_entrega_06_riscos_e_pendencias_r01, docs_entrega_06_riscos_e_pendencias_r02, docs_entrega_06_riscos_e_pendencias_r03, docs_entrega_06_riscos_e_pendencias_r09, docs_entrega_06_riscos_e_pendencias_r15, docs_entrega_06_riscos_e_pendencias_r16 [INFERRED 0.85]
- **Riscos de entrega, ensaio e demo** — docs_entrega_06_riscos_e_pendencias_r10, docs_entrega_06_riscos_e_pendencias_r11, docs_entrega_06_riscos_e_pendencias_r12, docs_entrega_06_riscos_e_pendencias_r13, docs_entrega_06_riscos_e_pendencias_r23, docs_entrega_06_riscos_e_pendencias_r24 [INFERRED 0.85]

## Communities (98 total, 21 thin omitted)

### Community 0 - "Modos e exemplos de alerta"
Cohesion: 0.08
Nodes (98): Exemplos sintéticos de alerta e sinais mamários pela CLI, Limite de perguntas dinâmicas por modo, Modo produtor, Modo veterinário, Urgência sem_problema, Bandeira R-BV-01, Bandeira R-BV-02, Bandeira R-BV-03 (+90 more)

### Community 1 - "Parecer e urgência na interface"
Cohesion: 0.06
Nodes (57): ComoChegou: 'Como cheguei aqui?' abre GET /como/{doenca}, Faixa de urgência: chamar_agora vermelho, observar âmbar, sem_problema verde, Tudo em localhost, sem nuvem e sem CDN; nenhuma LLM na decisão, final=false mostra aviso 'Parecer parcial', Parecer: tabela <table> com 8 doenças em ordem decrescente nos 3 blocos, 'Por que estou perguntando isso?' abre GET /porque/{simbolo}, Selo de gravidade com texto, não só cor, Sessão encerrada por ver_parecer/parada do motor vai ao parecer; Continuar respondendo reabre (+49 more)

### Community 2 - "Documentação e backend FastAPI"
Cohesion: 0.05
Nodes (48): .md em docs/, CLAUDE.md, engine/README.md, API README (api/), Backend FastAPI + SQLite (casca fina sobre motor e kb), Host confiavel (TrustedHostMiddleware contra DNS rebinding), Script rodar.ps1 / rodar.sh (execucao em localhost), Sementes de animais ficticios e reset seguro do banco, Servir web/dist com rota coringa propria (api/frontend.py), Sessao presa a versao da base com que nasceu (+40 more)

### Community 3 - "Skills e agentes de IA"
Cohesion: 0.05
Nodes (42): anthropics/skills (repositorio), brainstorming (skill), executing-plans (skill), frontend-design (skill), playwright-skill (lackeyjb), pptx (skill, source-available), Restricao de open source do hackathon, skill-creator (skill) (+34 more)

### Community 4 - "Identidade visual e campos"
Cohesion: 0.05
Nodes (45): Identidade Figma e autoridade API preservadas, Barras role=meter com preenchimento sólido, Botão primário rosa e secundário branco com contorno verde, Campo numérico textual preserva entrada ao erro, Composição desktop 1440 px derivada dos frames, Token cor/acento: #f4a6a6, Token cor/acento-escuro: #b5545c, Token cor/alerta: #e8a317 (+37 more)

### Community 5 - "Regras de produção e CF"
Cohesion: 0.07
Nodes (27): Regras de produção — documentação gerada, Agenda calculada pelo motor, Combinação max, Combinação mycin, Derivado evidencia_alteracao_leite, Estado suposicao_a_validar, scripts/gerar_doc_regras.py, SHA-256 do JSON canônico (+19 more)

### Community 6 - "Base de desenvolvimento e sessões"
Cohesion: 0.09
Nodes (14): Base de desenvolvimento 3.1.0-revisao1: 51 símbolos, 56 regras, 8 doenças e 6 telas, Papel A: pessoa, blocos reais, decisões humanas e aprendizado a completar, Decisões verificáveis de motor, base e documentação, Papel A: registro técnico curado, sem depoimento pessoal atribuído, Papel B: diário a preencher, sem interações ou resultados inventados, Escopo original do diário B e API já integrada; relato pessoal pendente, Papel C: diário a preencher, sem interações ou aprendizado inventados, Escopo original do diário C e integração React já presente; relato humano pendente (+6 more)

### Community 7 - "Riscos e pendências de entrega"
Cohesion: 0.09
Nodes (5): R08: Documentação manual divergir da implementação (média), R22: Reprodutibilidade Python sem lockfile (média), R24: Elegibilidade e presença sem confirmação (alta), Modelo de ensaio e envio não preenchido; não comprova execução, Revisão técnica documental da Seção 6, sem validação clínica ou ensaio humano

### Community 8 - "Concorrência e snapshot de sessão"
Cohesion: 0.10
Nodes (19): Comparacao de casos com a versao pai, Concorrencia: BEGIN IMMEDIATE e conferencia de revisao, Importacao de animais CSV/JSON sem 500, ordem_respostas no snapshot (reprocessar lotes na correcao), Portao de ativacao de versao (casos_falhando, confirmar_falhas), Cortes de bloco nao lidos de meta.limiares, Percentual do parecer max(0, CF) x 100 (divergencia), Bandeira vermelha: pausa, continuar, ver_parecer (+11 more)

### Community 9 - "Roteiro de apresentação"
Cohesion: 0.10
Nodes (24): Roteiro de apresentação e demonstração, Ensaio e reserva, Exemplo aritmético de CF (0,60 e 0,50 = 0,80), Fala principal de 10 minutos, Papéis de fala A/B/C, Pergunta: o que cada integrante aprendeu?, Slide 1: Problema e T1 Anamnese (0:45), Slide 2: O que é sistema especialista (1:00) (+16 more)

### Community 10 - "Perguntas da banca sobre IA"
Cohesion: 0.11
Nodes (20): Perguntas: correção de resposta e ordem importam?, Pergunta: onde está o editor?, Pergunta: o que acontece com 'não sei'?, Pergunta: onde está a IA na consulta?, Pergunta: atende integralmente a open source?, Pergunta: o que significa sem_problema?, Pergunta: quem validou pesos e casos clínicos?, Pergunta: como mudar a base sem perder rastreabilidade? (+12 more)

### Community 11 - "Bandeira vermelha e desvios"
Cohesion: 0.16
Nodes (19): Bandeira vermelha e pausa de alerta, Pacote engine (motor), EstadoSessao, explicacao_servico.py (parecer, porque, como, traco), Pacote kb (base de conhecimento), estado.py montar_estado, Plano de implementação API (Seção 4), Revisão do motor 2026-10-21 (+11 more)

### Community 12 - "Cliente tipado e tipografia"
Cohesion: 0.12
Nodes (20): Varela Round em títulos e Nunito Sans no conteúdo, Global Constraints, chamar<T>(metodo, caminho, corpo): prefixa /api, erro de rede vira sem_conexao, web/src/api/cliente.ts (fetch tipado), Comandos: npm ci, gerar-tipos, test, build; e2e playwright com API em :8000, web/src/componentes/*, PRODUCT.md e DESIGN.md gerados a partir do Figma, web/e2e/*.spec.ts (Playwright) (+12 more)

### Community 13 - "Diário de bordo 22/10"
Cohesion: 0.11
Nodes (18): 22/10 Grafo e Obsidian atualizados (d9eda27), 22/10 Consulta React integrada, base v0002 (7494e3e, cff6704), Codex, Figma e impeccable na interface, Diários A, B e C a complementar, Graphify e cofre Obsidian como ferramentas auxiliares, Seção: IA, skills e revisões, Revisão por outra família de modelo não comprovada, Skills aplicadas (superpowers, TDD, debugging, verification, writing-plans) (+10 more)

### Community 14 - "Motor e API FastAPI"
Cohesion: 0.14
Nodes (19): 22/10 Troca produtor-especialista e parecer único (1593149, 85210ca, 09f5754), analisar, API FastAPI + SQLite, Base.de_dict, Sessao(base, modo, ficha, limite_dinamico), Componente: memória de trabalho, Seção: Contratos Python disponíveis, Fluxo implementado (diagrama Mermaid) (+11 more)

### Community 15 - "Demo cronometrada e avisos"
Cohesion: 0.11
Nodes (19): Aviso fixo 'Este parecer não é um laudo' e /privacidade, Comandos da CLI python -m engine, Demo 0:00-0:30: abrir localhost e iniciar verificação, Demo 0:30-1:00: entrada inválida 12,5 e erro 422, Demo 1:00-2:00: caso C-MAS-01 no produtor e por quê, Demo 2:00-2:40: mudar para modo especialista, Demo 2:40-3:10: parecer e Como cheguei aqui?, Demo 3:10-3:40: caso C-HIP-01 e alerta chamar_agora (+11 more)

### Community 16 - "Serviços da casca fina"
Cohesion: 0.18
Nodes (14): base_servico.py, casos_servico.py, Esquema SQLite (7 tabelas), ficha.py (dias_em_lactacao, validar_ficha, ficha_para_motor), api/frontend.py montar_frontend, importacao.py (CSV/JSON de prontuário), api/db/repositorios.py (único lugar com SQL), Scripts de execução (rodar, resetar_db, semear) (+6 more)

### Community 17 - "Cliente nunca envia CF"
Cohesion: 0.13
Nodes (17): Cliente nunca envia CF: envia valor ou nao_sei, kb/ não importa graphify, Motor, API, validador e casos não mudam; v0002 continua ativa, Objetivo: separar base por doença com junção exata, gerar grafo 2 sem IA, provar motor lê do grafo exato, Pasta do cofre obsidian/02-Dados de Treino/ e saída graphify-out-dados/, Grafo 2 — base por doença: plano de implementação, Global Constraints do grafo 2, Serialização JSON ensure_ascii=False, indent=2, exclude_none (igual kb.carregador._json) (+9 more)

### Community 18 - "Alerta de bandeira e SPA"
Cohesion: 0.12
Nodes (16): AlertaBandeira: modal com ver_parecer/continuar via POST acoes/bandeira, web/src/anamnese/*, Arquitetura: SPA Vite servida pelo FastAPI (web/dist, api/frontend.py), Camada 4b de testes (Playwright), Modal (foco preso, sem Esc em alerta), Objetivo: SPA React+TS que reproduz o protótipo do Figma e conversa com a API, proxima null com alerta.pausa abre modal de alerta, Plano de implementação Frontend web/ (React) (+8 more)

### Community 19 - "Aquisição de conhecimento"
Cohesion: 0.15
Nodes (16): Aquisicao de conhecimento por especialista e engenheiro, Base de conhecimento: regras de producao, variaveis, pesos CF, versionada, kb/: validacao e versoes da base, Componentes da arquitetura (Modelo Conceitual), Editor grafico da base fora do escopo do PoC, Encadeamento, Fatores de certeza CF e incerteza, Fontes de dados externas: prontuario, sensores, APIs (+8 more)

### Community 20 - "Diário de bordo 20-21/10"
Cohesion: 0.17
Nodes (16): 20/10 Especificação e plano do motor, 21/10 Ajustes de bandeiras, CF de urgência, restauração (aaa7841, 75bcc45..6e35b6f), 21/10 Base revisada de desenvolvimento (898512c), 21/10 Reprocessamento de bandeiras pela ordem real (f0d8c6f, a3e73eb, a677283), 21/10 Revisão do motor (ce6874b), 22/10 Integração dos 34 casos, API e persistência (f46cd6e), 22/10 Base v0003 e potencial (c2dd78d, 0300cdb, 950087e), Seção: Linha do tempo comprovável (+8 more)

### Community 21 - "Perguntas sobre uso offline"
Cohesion: 0.15
Nodes (16): Pergunta: roda sem internet?, Pergunta: porcentagem é chance de doença?, Slide 8: Riscos e próximos passos (0:45), Swagger /api/docs depende de CDN, Riscos, lacunas e fechamento da entrega, Achados da Camada 3 (Seção 5, codex-davi), Contagens: 34 casos JSON (31 adaptados, 2 originais, 1 regressão), Correção de resposta exercitada via Sessao (+8 more)

### Community 22 - "Achados de base inválida"
Cohesion: 0.13
Nodes (11): Achado E06 doenca sem regra, Arquivos kb_invalidas Secao 5.1, E08 bandeira sem triagem, E11 criterio de triagem, E15 cf_minimo e cf_maximo, E16 texto da tela de triagem, E17 ordem de limiares, E20 id_invalido (+3 more)

### Community 23 - "Barra de confiança e Boi"
Cohesion: 0.15
Nodes (17): Review Focus (5 pontos de risco), BarraConfianca (role=meter, aria-valuenow), Barra lateral 'O que estou pensando' (top 4 por percentual, a partir da 2ª pergunta), Boi (SVG do Figma, aria-hidden), Botao (variante, carregando, aria-busy), CampoNumerico (rejeita fora de [0-9.,], aria-invalid), Botao, OpcaoResposta, CampoNumerico, BarraConfianca, Boi, Balao, BarraProgresso, Modal, 409 conflito/ja_respondida por duplo clique: botão desabilitado e recarrega sessão (+9 more)

### Community 24 - "Alocação de agentes de IA"
Cohesion: 0.14
Nodes (12): Alocacao de agente principal e alternativa por prompt de revisao, anthropics/skills (pptx, docx, pdf, webapp-testing, frontend-design), Antigravity (plano Pro), Claude Code (Claude Pro), Codex (ChatGPT Plus), Skills em formato aberto (.agents/skills, .claude/skills, AGENTS.md), Gemini Pro (Google AI Pro, app web), Implementacao por pessoa (A, B, C) com agente principal e reserva (+4 more)

### Community 25 - "Combinação MYCIN e blocos"
Cohesion: 0.15
Nodes (15): Blocos do parecer: principal >=0,50, diferencial 0,20-0,50, pouco provável <=0,20, CF da premissa = mínimo; dispara se > 0,20, Combinação MYCIN de CF (três casos de sinal), Componente: base de conhecimento, Componente: fontes externas de fatos, Componente: interface com o usuário, Componente: motor de inferência, Inferência em três camadas (+7 more)

### Community 26 - "Hipocalcemia e periparto"
Cohesion: 0.14
Nodes (15): Derivado hipotermia, Derivado periparto_imediato, Hipocalcemia Puerperal (hipocalcemia), R-ACI-05 apetite baixo isolado → acidose, R-CET-06 apetite baixo isolado → cetose, R-DAB-04 apetite baixo isolado → abomaso, R-DER-01 dias≤3 → periparto_imediato, R-DER-05 temp<38 → hipotermia (+7 more)

### Community 27 - "Exigências oficiais da entrega"
Cohesion: 0.17
Nodes (16): Entrega: índice para a equipe e a banca, Seção: Atendimento às exigências oficiais, Seção: Equipe (A, B, C), Exigência: apresentação do processo ao resultado (A slide 10), Exigência: ferramentas e código aberto (A slides 3 e 13) - licença pendente, Exigência: demonstração em funcionamento (A slide 10), Exigência: IA apoiando o desenvolvimento (A slides 3 e 7), Exigência: até três integrantes (A slide 3) (+8 more)

### Community 28 - "AGENTS.md e Codex"
Cohesion: 0.17
Nodes (15): AGENTS.md: instrucoes para o Codex, Codex como agente destinatario, Escrever tudo em portugues, AGENTS.md: instrucoes de busca e manutencao documental, Instrucoes do projeto em CLAUDE.md: mesmas regras para todos os agentes, CLAUDE.md: instrucoes do PoC Anamnese de Bovinos Leiteiros, Arquitetura comum aos tres temas: base + motor + aplicacao, O desafio: aplicacao para usuario final com base explicita e motor de inferencia (+7 more)

### Community 29 - "Decisões de seleção de perguntas"
Cohesion: 0.14
Nodes (13): Seleção de perguntas dirigida a hipóteses, Componente: aquisição de conhecimento, README principal HackAtom, Base v0003 (pai da v0004), Base ativa v0004, Editor gráfico pendente, Estado integrado na branch codex-davi, evidencias-verificacao.json (+5 more)

### Community 30 - "TPB e derivado febre"
Cohesion: 0.16
Nodes (15): Derivado febre, Tristeza Parasitária Bovina (tpb), Regras de evidência contrária (CF negativo), R-BV-05 úbere inflamado + febre + apatia → chamar_agora, R-DER-04 temp≥39,5 → febre, R-DER-07 extremidades quentes → febre, R-DER-08 temp<39,5 → contra febre, R-DER-09 temp≥38 → contra hipotermia (+7 more)

### Community 31 - "Atualização do grafo"
Cohesion: 0.16
Nodes (14): Atualizacao unica ao encerrar bloco documental, graphify export obsidian --dir obsidian/01-conhecimento, /graphify . --update, Commit separado do grafo, Codigo, testes, web, docs/prompts e docs/rascunhos nao pedem atualizacao, Commit separado chore(grafo): atualiza grafo, Primeira extracao do grafo custou ~520 mil tokens (cost.json), Mudancas so em codigo, testes, web, prompts e rascunhos nao pedem atualizacao (+6 more)

### Community 32 - "Processo de desenvolvimento"
Cohesion: 0.27
Nodes (14): Processo de desenvolvimento (01-processo), Fronteira independente do núcleo, Seção: Organização e aprendizado a registrar, Arquitetura tecnológica (02-arquitetura), Núcleo Python independente de interface, banco e base, 03-regras-de-producao (gerado da ativa v0004), 04-casos-de-teste (gerado por execução real), 05-apresentacao-e-demo (roteiros 10 e 5 min, perguntas da banca) (+6 more)

### Community 33 - "Decisões de reprocessamento"
Cohesion: 0.14
Nodes (10): Seção: Julgamento sobre sugestões da IA, Agenda e prioridades (bandeiras 100, urgências 50, evidências 10), Bandeira vermelha leva a chamar_agora, Continuar respondendo após encerrar pelo alerta (R21), Critérios de parada, Seção: Diálogo, parada e bandeiras, inferir(base, fatos) sem estado vs determinismo da sessão, Operador max em derivados positivos (+2 more)

### Community 34 - "Cetose e deslocamento de abomaso"
Cohesion: 0.15
Nodes (14): Derivado inicio_lactacao, Deslocamento de Abomaso (deslocamento_abomaso), Cetose / Hipercetonemia (cetose), R-CET-01 início lactação + apetite baixo + queda → cetose, R-CET-02 hálito de acetona → cetose, R-CET-03 recusa de concentrado → cetose, R-CET-04 BHB≥1,2 → cetose, R-CET-05 fita de urina positiva → cetose (+6 more)

### Community 35 - "Fonte inválida e Review Focus"
Cohesion: 0.19
Nodes (14): FonteInvalida(ValueError) com mensagem em português, Review Focus (5 riscos), Caminho com espaço: script recebe como argumento único, Id de regra duplicado entre arquivos: erro cita id e os dois arquivos, Sem indice.json: junta mesmo assim, novos ao final, Regra de urgência que cita duas doenças vai para comum.json, test_doenca_sem_simbolo, test_id_duplicado_entre_arquivos (+6 more)

### Community 36 - "Doenças e acidose ruminal"
Cohesion: 0.17
Nodes (11): Acidose ruminal (categoria), Acidose ruminal subaguda, Anaplasmose, Babesiose, Cetose bovina (hiperCetonemia), Foot rot (podridao de casco), Hipocalcemia puerperal (paresia parturiente), Mastite bovina (+3 more)

### Community 37 - "Regras do modo bovino urgente"
Cohesion: 0.18
Nodes (12): R-BV-01 decúbito → chamar_agora, R-BV-02 urina escura → chamar_agora, R-BV-03 apetite ausente + apatia → chamar_agora, R-BV-04 hipotermia + apatia → chamar_agora, R-BV-06 temperatura≥41 → chamar_agora, Seção Telas de triagem, Tela 4 apetite_ruminacao, Tela 3 atitude_locomocao (+4 more)

### Community 38 - "Demonstração principal local"
Cohesion: 0.17
Nodes (12): Demonstração principal em localhost (4 min), scripts/rodar.ps1 e banco ANAMNESE_DB, Slide 6: Evidência de funcionamento (1:00), R09: Contagem de testes confundida com validação clínica (alta), R25: Teste Vitest intermitente (baixa), Resultados: 1082 testes backend, 170 subtestes, 72 Vitest, 34/34 casos, Slide 13: Resultados verificados (0:55), Slide 14: Documentação (0:30) (+4 more)

### Community 39 - "Ambiente venv e testes"
Cohesion: 0.23
Nodes (10): Achado fato numerico inerte no teste, Ambiente venv, engine.modelos.Base.de_dict, .gitattributes, Pacote engine, SDD ledger, Spec anamnese bovinos, Task 6 (+2 more)

### Community 40 - "Busca direta versus grafo"
Cohesion: 0.24
Nodes (11): Abrir so o trecho em source_file/location em vez de varrer docs/, Busca direta (rg) quando o arquivo ja e indicado ou e codigo e testes, Grafo de conhecimento so quando precisar procurar, graphify query para localizar decisao, regra, fonte ou requisito, Nao ler grafo nem GRAPH_REPORT no inicio da tarefa, Quando nao usar o grafo: arquivo indicado, informacao ja conhecida, codigo e testes, Grafo de conhecimento: ferramenta de busca sob demanda, GRAPH_REPORT.md: visao geral rara (~7 mil tokens) (+3 more)

### Community 41 - "Decisão determinística auditável"
Cohesion: 0.20
Nodes (11): Demonstracao em localhost, Modulo de explicacao: por que e como, Decisao deterministica e auditavel, Rodar por completo em localhost, sem nuvem obrigatoria, Nao usar a LLM como sistema especialista; sem LLM no caminho da decisao, Restricoes obrigatorias, Traco de inferencia, Entrega, demonstracao e localhost (slides 10 e 15) (+3 more)

### Community 42 - "Fechamento de interface"
Cohesion: 0.24
Nodes (11): 22/10 Fechamento de interface (61f0994..f4341cd), 22/10 Explicações em linguagem comum e base v0004 (1e2065a..0a76d75), Animações respeitando prefers-reduced-motion, Aviso: parecer não é um laudo e página /privacidade, Seção: Camada web implementada, Componente: módulo de explicação, Módulo de explicação (traco.py, explicacao.py), Histórico local de navegação e correção por PUT (+3 more)

### Community 43 - "Decisões rejeitadas e passos"
Cohesion: 0.18
Nodes (8): Passo 3: escolher tecnologia (Python, FastAPI, SQLite, React 19, Vite 8), exportar / Sessao.restaurar, fractions.Fraction (aritmética racional), Snapshot JSON: exportar e restaurar, Stack web: React 19, TypeScript 5, Vite 8, Vitest, Playwright, axe, Seção: Tecnologias e dependências, Exigência: determinismo e auditoria (A slide 8), Exigência: decisão por regras, sem LLM em execução (A slides 8 e 13)

### Community 44 - "Passo a passo pedido"
Cohesion: 0.18
Nodes (10): Seção: Passo a passo pedido pelos organizadores, Passo 1: escolher agente de IA, Passo 8: estudar a produção (ensaio a registrar), Passo 7: implementar e testar, Passo 6: definir regras (61, todas suposição), Estado dos testes (1082 Python, 72 Vitest) e histórico, Seção: Executar o checkpoint, 61 regras em suposicao_a_validar, zero validadas (+2 more)

### Community 45 - "Arrumação e rótulos do grafo"
Cohesion: 0.20
Nodes (11): Arrumação: renomear 02-a-definir, reescrever README, atualizar CLAUDE.md, AGENTS.md, .graphifyignore, graph.json com 107 nós, Rótulos de comunidade pela doença predominante do source_file ou 'Comum', scripts/grafo_dados.py (build_from_json dedup=False, cluster, relatório, HTML, cofre), pytest -q completo verde, Task 3: cofre e visualização (scripts/grafo_dados.py) + arrumação, Arrumação: renomear 02-a-definir -> 02-Dados de Treino; atualizar CLAUDE.md, AGENTS.md, .graphifyignore, Custo de tokens zero (sem IA) (+3 more)

### Community 46 - "CLI de fonte por doença"
Cohesion: 0.24
Nodes (11): CLI python -m kb.fonte separar/juntar (--salvar --autor --nota), gravar_fonte(base, pasta), Junção: arquivos em ordem alfabética, ordena pelo índice, desconhecidos ao final, ler_fonte(pasta) -> Base, Regras de separação: uso transitivo, exclusivo à doença, urgência, resto em comum, separar(base) -> dict[str, dict], Task 1: separar e juntar (kb/fonte.py), Vai para comum.json: meta, layout, compartilhados, bandeiras vermelhas, derivados compartilhados (+3 more)

### Community 47 - "Avaliação da organização"
Cohesion: 0.20
Nodes (10): Apresentacao obrigatoria do processo, do uso da IA ao resultado, Avaliacao da organizacao do grupo com a IA e conhecimento adquirido, Avaliacao: nota 1 a 10 pelo potencial de resolver o problema, Cronograma: inicio 20/10 9h, envio 22/10 20h, apresentacao 23/10 9h, Complexidade e assertividade desempatam e definem nota de partida, Desenvolvimento apoiado por agente de IA, docs/entrega: documentacao de entrega, Documentacao obrigatoria: processo, arquitetura tecnologica, regras de producao (+2 more)

### Community 48 - "Duração e fechamento da seção"
Cohesion: 0.20
Nodes (8): Duração estimada 10+4 min (não oficial), Pergunta: quando e como será entregue?, Fechamento da Seção 6 — 22/10/2026, Perguntas de encerramento e revisão formal, R11: Tempo da fala e infraestrutura desconhecidos (média), R13: Envio incompleto ou fora do prazo (alta), R23: Material editorial tratado como entrega concluída (alta), A confirmar antes da apresentação

### Community 49 - "Critérios de parada"
Cohesion: 0.20
Nodes (10): Critérios de parada: CF >= 0,80, teto 0,70, 12/25 perguntas, Dois grafos: documentação e dados das 8 doenças (112 nós, 149 relações), Hierarquia de modelos e processo spec-plano-teste-revisão, Base: 8 doenças, 51 símbolos, 61 regras, 34 casos, Slide 7: Funcionamento da consulta (0:40), Slide 8: Base de conhecimento (0:40), Slide 9: Grafos (0:35), Slide 10: Arquitetura (0:45) (+2 more)

### Community 50 - "Exportação do grafo de dados"
Cohesion: 0.29
Nodes (10): carregar_do_grafo(caminho) -> Base, CLI python -m kb.exportar_grafo, exportar(origem, saida) grava grafo_exato.json e extracao.json, extracao(base, origem_por_id) no esquema graphify (nós sim:/regra:, arestas condicao_de/conclui), Grafo editado com aresta para nó inexistente: grafo_para_base levanta erro, test_casos_iguais_lendo_do_grafo (34 casos), test_extracao_no_esquema_do_graphify (51 sim:, 56 regra:), test_carregar_do_grafo_igual_v0002 (+2 more)

### Community 51 - "API pública da base"
Cohesion: 0.22
Nodes (10): API pública: separar, gravar_fonte, ler_fonte, comum.json (meta, simbolos, regras, layout), doencas/<id>.json (doenca, simbolos, regras), Erros da junção: id duplicado, doença sem símbolo tipo doenca, JSON inválido, kb/fonte.py — separar e juntar, Formato em disco de base/fonte/, Ids novos entram ao final; ids sumidos do índice são removidos (edição legítima), indice.json (ordem_simbolos, ordem_regras) (+2 more)

### Community 52 - "Fonte separada por doença"
Cohesion: 0.33
Nodes (8): 22/10 Fonte separada por doença e grafo 2 (b08bb63..9a13eaa), Seção: Base por doença e grafo 2, kb/exportar_grafo.py e grafo exato, base/fonte/comum.json e doencas/<doença>.json, Grafo 2 do Obsidian (112 nós, 149 arestas, 9 comunidades, custo zero), python -m kb.fonte juntar (--salvar), Repositorio.salvar_nova (nova versão com pai), Grafo 2: dados de treino por doença

### Community 53 - "Camadas de inferência"
Cohesion: 0.28
Nodes (8): Camada 1 (derivados), Camada 2 (hipóteses por doença), Camada 3 (desfecho de triagem), Política de triagem do projeto (Seções 1 e 3), Seção Bandeiras vermelhas — camada 3, Seção Derivados — camada 1, Seção Urgências — camada 3, Tela 1 dias_em_lactacao

### Community 54 - "Metrite e puerpério"
Cohesion: 0.22
Nodes (9): Derivado puerperio, Metrite Puerperal (metrite), R-DER-02 dias≤21 → puerperio, R-MET-01 puerpério + corrimento fétido → metrite, R-MET-02 corrimento + puerpério + febre → metrite, R-MET-03 puerpério + útero aumentado + corrimento → metrite, R-MET-04 retenção de placenta + puerpério → metrite, R-URG-04 metrite CF≥0,5 → chamar_agora (+1 more)

### Community 55 - "Dermatite digital"
Cohesion: 0.22
Nodes (9): Dermatite Digital Bovina (dermatite_digital), R-DD-01 claudicação → dermatite digital, R-DD-02 claudicação + dor no talão → dermatite digital, R-DD-03 lesão em morango → dermatite digital, R-URG-06 cetose CF≥0,5 → observar, R-URG-07 acidose CF≥0,5 → observar, R-URG-08 dermatite digital CF≥0,5 → observar, Seção Dermatite Digital Bovina (gravidade baixa) (+1 more)

### Community 56 - "Mastite"
Cohesion: 0.22
Nodes (9): Mastite (mastite), MSD Veterinary Manual (referência clínica contextual), R-MAS-02 úbere inflamado → mastite, R-MAS-04 CMT reagente → mastite, R-URG-05 mastite CF≥0,5 → observar, Seção Cetose / Hipercetonemia (gravidade média), Seção Hipocalcemia Puerperal (gravidade alta), Seção Mastite (gravidade média) (+1 more)

### Community 57 - "Ferramentas de IA e AGENTS"
Cohesion: 0.42
Nodes (9): AGENTS.md (instrucoes do projeto), Google Antigravity (app, IDE e CLI), Claude Code, CLAUDE.md (instrucoes do projeto), OpenAI Codex (CLI, IDE, app desktop), Gemini CLI, GEMINI.md (instrucoes do projeto), Limites de uso dos planos (+1 more)

### Community 58 - "Achados do carregador"
Cohesion: 0.28
Nodes (7): Achado carregar_base excecoes nativas, Achado prioridade zero no teste, carregar_base, Plano kb secao 2, pyproject.toml, Task 1, tests/kb/test_modelos.py

### Community 59 - "Achados do contrato de aresta"
Cohesion: 0.28
Nodes (7): Achado kb aceita base invalida, Achado ordem ausente no contrato, Aresta.ordem, kb/__init__.py, para_motor, Revisao final, validar_edicao

### Community 60 - "Contrato OpenAPI e exemplos"
Cohesion: 0.39
Nodes (8): 27 endpoints da Seção 4.5, contratos/exemplos (27 exemplos), api/exportar_openapi.py, contratos/openapi.json versionado, operationId estável por rota, registro.py CONTRATOS por operationId, Task 3: Schemas Pydantic e exemplos de contrato, Task 12: OpenAPI versionado e teste de contrato

### Community 61 - "Casos clínicos e fonte"
Cohesion: 0.25
Nodes (9): 34 casos clínicos com mesmo resultado lendo v0002 e grafo exato, CLI python -m kb.fonte: separar, juntar, juntar --salvar, base/fonte/ passa a ser o que a equipe edita; juntar gera próxima versão via salvar_nova, Invariante: juntar(separar(v0002)) == v0002, Objetivos: separar, editar em base/fonte/, grafo 2 sem IA, motor lê do grafo exato, Repositorio.salvar_nova valida antes de gravar, tests/kb/test_exportar_grafo.py, tests/kb/test_fonte.py (+1 more)

### Community 62 - "Base ausente e contrato"
Cohesion: 0.25
Nodes (6): API sobe sem a base (409 conflito em vez de 500), Contrato OpenAPI versionado e exemplos por operationId, Formato unico de erro (codigos e X-Requisicao-Id), Notas para o frontend (proxima nulo, reabrir, 409 conflito), Mapa de 27 rotas por arquivo (prefixo /api), Testes da API (pytest, marca lento, base minima de fixtures)

### Community 63 - "Ausência de validação clínica"
Cohesion: 0.25
Nodes (7): Seção: Problema e método, Ausência de validação clínica, Sistema especialista: base de regras + motor, Tema T1 Anamnese, Traço: por quê e como, Sem validação clínica nem autenticação neste recorte, Seção: Testes, execução e limites

### Community 64 - "Configuração da API"
Cohesion: 0.39
Nodes (7): Configuracao (api/config.py), Contexto e obter_contexto, criar_app / main.py, ErroApi e fábricas de erro, Formato único de erro, Tabela de códigos de erro HTTP, Task 1: Esqueleto do app, config e formato único de erro

### Community 65 - "Acessibilidade e Figma"
Cohesion: 0.29
Nodes (8): Acessibilidade: contraste 4,5:1, foco visível, alvos 44 px, fieldset/legend, reduced-motion, lang pt-BR, Estados obrigatórios: carregando, erro, vazio, desabilitado, foco, Figma HackAtom, página Protótipo (modo Dev), Skill impeccable (context, init, document, detect, audit, polish), Passe de qualidade: audit/polish, responsivo 375/768/1024/1440, Task 2: Componentes base, Task 8: Passe de qualidade com impeccable, Uma transição autoral: balão fala (fade + leve subida), reduced-motion desliga

### Community 66 - "Estrutura de pastas"
Cohesion: 0.38
Nodes (7): api/: FastAPI + SQLite, engine/: motor Python so com biblioteca padrao, web/: React + TypeScript feito pelo Codex, Dados ficticios apenas, Especificacao e planos aprovados; sem refazer brainstorming, Estado atual: fase de implementacao e entrega, Spec canonica 2026-10-20-anamnese-bovinos-design.md

### Community 67 - "Caminho do ciclo"
Cohesion: 0.43
Nodes (6): Achado direcao do caminho do ciclo, Achado op e negado None viram default, encontrar_ciclo, kb/grafo.py, Task 2, Task 3

### Community 68 - "READMEs e caso alerta"
Cohesion: 0.33
Nodes (7): README da API, Caso alerta-decubito (demo CLI), README de kb/, Suíte completa pytest, Python 3.12+ somente biblioteca padrão, Seção: Executar a demonstração do motor, Comando unittest do motor

### Community 69 - "Fonte do grafo 2"
Cohesion: 0.33
Nodes (6): base/fonte/: origem dos dados do grafo 2, Grafo 2: dados das doencas gerado sem IA, Nao rodar /graphify em obsidian/02-Dados de Treino, Regenerar com kb.exportar_grafo + scripts/grafo_dados.py, base/: versoes imutaveis, ativa em base/ativa.json, obsidian/02-Dados de Treino: grafo 2 dos dados das 8 doencas sem IA

### Community 70 - "Casos esperados e hackathon"
Cohesion: 0.33
Nodes (6): Casos de teste com resultado esperado por versao da base, Open source; linguagem a escolha do grupo, Dicas do hackathon (slide 13), Projeto proposto (slide 8), Projeto proposto Hackathon 2026 (documento D, paginas 2 e 3), Cinco tarefas TDD do motor (vermelho antes do verde)

### Community 71 - "Acidose ruminal regras"
Cohesion: 0.33
Nodes (6): Acidose Ruminal (acidose), R-ACI-01 diarreia + apetite baixo → acidose, R-ACI-02 mudança de concentrado + diarreia → acidose, R-ACI-03 fezes com espuma e grãos → acidose, R-ACI-04 pH ruminal<5,5 → acidose, Seção Acidose Ruminal (gravidade média)

### Community 72 - "Achados de ativa.json"
Cohesion: 0.53
Nodes (5): Achado temporario fixo ativa.json.tmp, Achado pai explicito nao verificado, ativa.json, salvar_nova, Task 5

### Community 73 - "Validação de Condicao"
Cohesion: 0.40
Nodes (4): Achado Condicao valor int, Condicao.valor, E03 valor_invalido, model_fields_set da Aresta

### Community 74 - "Análise e carregador"
Cohesion: 0.33
Nodes (4): kb/analise.py, kb/carregador.py, kb/modelos.py, LimiteDinamico

### Community 75 - "Arquitetura de kb"
Cohesion: 0.40
Nodes (6): Arquitetura: kb/fonte.py, kb/exportar_grafo.py, scripts/grafo_dados.py, kb/exportar_grafo.py, kb/fonte.py, carregar_do_grafo(caminho) -> Base, kb/exportar_grafo.py — grafo exato e entrada do graphify, grafo_exato.json = base_para_grafo(base)

### Community 76 - "Falhas de API na interface"
Cohesion: 0.50
Nodes (5): Aviso vermelho do modo especialista ligado ao botão por aria-describedby, API fora do ar ou sem base ativa (409): erro amigável com Tentar de novo, iniciarVerificacao(modo): POST /api/animais e /api/sessoes, Início cria animal anônimo ANON-… e sessão no modo escolhido, Task 3: Página Início (/) criar sessão

## Ambiguous Edges - Review These
- `uv (sync, run, python pin)` → `Python 3.15.0`  [AMBIGUOUS]
  docs/pesquisa/execucao-local.md · relation: conceptually_related_to
- `Limites de uso dos planos` → `Gemini CLI`  [AMBIGUOUS]
  docs/pesquisa/agentes-e-skills.md · relation: references
- `Task 1` → `kb/__init__.py`  [AMBIGUOUS]
  docs/revisoes/2026-10-21-ledger-kb-secao-2.md · relation: references
- `Achado kb aceita base invalida` → `E14 cobre max fora de derivado`  [AMBIGUOUS]
  docs/revisoes/2026-10-21-ledger-kb-secao-2.md · relation: rationale_for
- `Achado temporario fixo ativa.json.tmp` → `Escrita interrompida apaga arquivo novo`  [AMBIGUOUS]
  docs/revisoes/2026-10-21-ledger-kb-secao-2.md · relation: conceptually_related_to

## Knowledge Gaps
- **287 isolated node(s):** `Token cor/primaria-escura: #173d22`, `Token cor/texto: #1e2a20`, `Token cor/fundo-escuro: #1f4d2c`, `Token cor/fundo-medio: #2e6b3f`, `Token cor/primaria: #2e6b3f` (+282 more)
  These have ≤1 connection - possible missing edges or undocumented components. (Counts symbols only; 337 node(s) total have ≤1 connection when file, concept and rationale nodes are included.)
- **21 thin communities (<3 nodes) omitted from report** — run `graphify query` to explore isolated nodes.

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **Why does `MSD Vet Manual` connect `Doenças e acidose ruminal` to `Modos e exemplos de alerta`, `Aquisição de conhecimento`?**
  _High betweenness centrality (0.270) - this node is a cross-community bridge._
- **Are the 7 inferred relationships involving `Base de conhecimento v0004` (e.g. with `Bandeira R-BV-01` and `Bandeira R-BV-02`) actually correct?**
  _`Base de conhecimento v0004` has 7 INFERRED edges - model-reasoned connections that need verification._
- **What connects `Token cor/primaria-escura: #173d22`, `Token cor/texto: #1e2a20`, `Token cor/fundo-escuro: #1f4d2c` to the rest of the system?**
  _287 weakly-connected nodes found - possible documentation gaps or missing edges._
- **Should `Modos e exemplos de alerta` be split into smaller, more focused modules?**
  _Cohesion score 0.07940594059405941 - nodes in this community are weakly interconnected._
- **Why does `Conhecimento veterinario sempre suposicao a validar, citando fonte` connect `Aquisição de conhecimento` to `AGENTS.md e Codex`?**
  _High betweenness centrality (0.264) - this node is a cross-community bridge._

### Low-confidence Hints
_AMBIGUOUS edges — the extractor was unsure. Verify before acting on these._

- **What is the exact relationship between `uv (sync, run, python pin)` and `Python 3.15.0`?**
  _Edge tagged AMBIGUOUS (relation: conceptually_related_to) - confidence is low._
- **What is the exact relationship between `Limites de uso dos planos` and `Gemini CLI`?**
  _Edge tagged AMBIGUOUS (relation: references) - confidence is low._