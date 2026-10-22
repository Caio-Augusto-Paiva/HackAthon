---
type: community
cohesion: 0.06
members: 57
---

# Modelos e validação da base

**Cohesion:** 0.06 - loosely connected
**Members:** 57 nodes

## Members
- [[API README (api)]] - document - api/README.md
- [[Arvore da secao 4.3 da especificacao (sessao, validacao, modelos)]] - concept - docs/revisoes/2026-10-21-revisao-motor.md
- [[Backend FastAPI + SQLite (casca fina sobre motor e kb)]] - concept - api/README.md
- [[Camadas de símbolos (perguntaficha 0, derivado 1, doença 2, urgência 3)]] - rationale - docs/superpowers/plans/2026-10-21-kb-secao-2.md
- [[Caso de teste da base (entrada e resultado esperado)]] - concept - docs/superpowers/plans/2026-10-21-kb-secao-2.md
- [[Codigos do validador E00-E23 e W01-W03]] - concept - kb/README.md
- [[Comparacao de casos com a versao pai]] - concept - api/README.md
- [[Compatibilidade com o motor via para_motor (exclude_none)]] - concept - kb/README.md
- [[D4 EdicaoBase frouxa (erros de estrutura viram E00)]] - rationale - api/README.md
- [[Dados ficticios e regras como suposicao a validar]] - concept - kb/README.md
- [[Decisao deterministica, sem LLM nem rede no caminho]] - rationale - api/README.md
- [[Demonstracao executavel (python -m engine) com base artificial]] - concept - engine/README.md
- [[Dependências entre símbolos, ciclo e ordem topológica]] - concept - docs/superpowers/plans/2026-10-21-kb-secao-2.md
- [[Divergencias kb x motor (prioridade, layout, operadores ASCII)]] - concept - kb/README.md
- [[Especificacao autorizada da secao 1 (docspromptssecao-1.md)]] - document - docs/superpowers/plans/2026-10-20-motor-secao-1.md
- [[Especificacao canonica do projeto (anamnese bovinos)]] - document - docs/revisoes/2026-10-21-revisao-motor.md
- [[Especificação de anamnese (docssuperpowersspecs, Seção 2 e 5.1)]] - document - docs/superpowers/plans/2026-10-21-kb-secao-2.md
- [[Evidencia final 56 testes sem falhas]] - concept - docs/superpowers/plans/2026-10-20-motor-secao-1.md
- [[Ficha com null tratada como nao sei (deve ser ausente)]] - concept - docs/revisoes/2026-10-21-revisao-motor.md
- [[Foco de revisão do plano]] - rationale - docs/superpowers/plans/2026-10-21-kb-secao-2.md
- [[Focos da revisao (sem valor, contradicoes, loops, bandeiras)]] - concept - docs/superpowers/plans/2026-10-20-motor-secao-1.md
- [[Forma canônica de negação booleana (X = não)]] - rationale - docs/superpowers/plans/2026-10-21-kb-secao-2.md
- [[Gravacao atomica de versoes (mkstemp, fsync, os.link)]] - rationale - kb/README.md
- [[Guardas de execucao (CF positivo para urgencia e bandeira)]] - concept - engine/README.md
- [[Host confiavel (TrustedHostMiddleware contra DNS rebinding)]] - concept - api/README.md
- [[JSON Schemas versionados e test_schema_sincronizado]] - concept - kb/README.md
- [[Motor de inferencia README (engine)]] - document - engine/README.md
- [[Motor independente de web, banco, LLM e servicos externos]] - rationale - engine/README.md
- [[Organizacao dos modulos do motor]] - concept - engine/README.md
- [[Pacote kb README (base de conhecimento)]] - document - kb/README.md
- [[Plano de implementacao do motor (secao 1)]] - document - docs/superpowers/plans/2026-10-20-motor-secao-1.md
- [[Plano de implementação do kb (Seção 2)]] - document - docs/superpowers/plans/2026-10-21-kb-secao-2.md
- [[Portao de ativacao de versao (casos_falhando, confirmar_falhas)]] - concept - api/README.md
- [[Prioridade padrão por classe (100, 50, 10)]] - rationale - docs/superpowers/plans/2026-10-21-kb-secao-2.md
- [[Regra de produção (condições, conclusão, CF)]] - concept - docs/superpowers/plans/2026-10-21-kb-secao-2.md
- [[Restrições globais do kb]] - rationale - docs/superpowers/plans/2026-10-21-kb-secao-2.md
- [[Revisao do motor de inferencia (21102026)]] - document - docs/revisoes/2026-10-21-revisao-motor.md
- [[Revisão do motor (docsrevisoes2026-10-21-revisao-motor.md)]] - document - docs/superpowers/plans/2026-10-21-kb-secao-2.md
- [[Seguranca de entrada carregar_base trata texto como caminho]] - rationale - kb/README.md
- [[Sessao presa a versao da base com que nasceu]] - concept - api/README.md
- [[Símbolo (variável da base)]] - concept - docs/superpowers/plans/2026-10-21-kb-secao-2.md
- [[Tabela de conformidade com a especificacao (16 itens)]] - concept - docs/revisoes/2026-10-21-revisao-motor.md
- [[Tabela de códigos do validador (E01-E19, W01-W03)]] - concept - docs/superpowers/plans/2026-10-21-kb-secao-2.md
- [[Task 1 Ambiente e modelos Pydantic]] - document - docs/superpowers/plans/2026-10-21-kb-secao-2.md
- [[Task 2 Análise de dependências]] - document - docs/superpowers/plans/2026-10-21-kb-secao-2.md
- [[Task 3 Conversão base-grafo]] - document - docs/superpowers/plans/2026-10-21-kb-secao-2.md
- [[Task 4 Validador]] - document - docs/superpowers/plans/2026-10-21-kb-secao-2.md
- [[Task 5 Repositório de versões]] - document - docs/superpowers/plans/2026-10-21-kb-secao-2.md
- [[Task 6 Integração com o motor, schema e documentação]] - document - docs/superpowers/plans/2026-10-21-kb-secao-2.md
- [[Tela de triagem]] - concept - docs/superpowers/plans/2026-10-21-kb-secao-2.md
- [[engine.casos.executar_caso (casos de teste reproduziveis)]] - concept - engine/README.md
- [[kb como pacote folha (nao importa engine)]] - rationale - kb/README.md
- [[kbanalise.py (dependencias, ciclo, ordem topologica)]] - concept - kb/README.md
- [[kbcarregador.py Repositorio (versoes imutaveis, ativa.json, hash sha256)]] - concept - kb/README.md
- [[kbgrafo.py (conversao 11 Base - grafo bipartido)]] - concept - kb/README.md
- [[kbmodelos.py (modelos Pydantic, carregar_base, para_motor)]] - concept - kb/README.md
- [[kbvalidador.py (validar, validar_dados, validar_edicao, Relatorio)]] - concept - kb/README.md

## Live Query (requires Dataview plugin)

```dataview
TABLE source_file, type FROM #community/Modelos_e_validação_da_base
SORT file.name ASC
```

## Connections to other communities
- 3 edges to [[_COMMUNITY_Sessão, snapshot e parecer]]
- 2 edges to [[_COMMUNITY_Arquitetura e demonstração]]
- 1 edge to [[_COMMUNITY_Casos sintéticos na v0002]]
- 1 edge to [[_COMMUNITY_Frontend planejado e contrato API]]

## Top bridge nodes
- [[kbvalidador.py (validar, validar_dados, validar_edicao, Relatorio)]] - degree 10, connects to 1 community
- [[kbmodelos.py (modelos Pydantic, carregar_base, para_motor)]] - degree 7, connects to 1 community
- [[Backend FastAPI + SQLite (casca fina sobre motor e kb)]] - degree 6, connects to 1 community
- [[Motor de inferencia README (engine)]] - degree 6, connects to 1 community
- [[kbcarregador.py Repositorio (versoes imutaveis, ativa.json, hash sha256)]] - degree 6, connects to 1 community