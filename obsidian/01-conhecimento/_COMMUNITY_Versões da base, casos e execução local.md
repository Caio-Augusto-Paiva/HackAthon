---
type: community
cohesion: 0.08
members: 42
---

# Versões da base, casos e execução local

**Cohesion:** 0.08 - loosely connected
**Members:** 42 nodes

## Members
- [[Banco SQLite fora do OneDrive]] - rationale - api/README.md
- [[Camadas de símbolos (perguntaficha 0, derivado 1, doença 2, urgência 3)]] - rationale - docs/superpowers/plans/2026-10-21-kb-secao-2.md
- [[Caso de teste da base (entrada e resultado esperado)]] - concept - docs/superpowers/plans/2026-10-21-kb-secao-2.md
- [[Codigos do validador E00-E23 e W01-W03]] - concept - kb/README.md
- [[Comparacao de casos com a versao pai]] - concept - api/README.md
- [[D4 EdicaoBase frouxa (erros de estrutura viram E00)]] - rationale - api/README.md
- [[Dados ficticios e regras como suposicao a validar]] - concept - kb/README.md
- [[Dependências entre símbolos, ciclo e ordem topológica]] - concept - docs/superpowers/plans/2026-10-21-kb-secao-2.md
- [[Especificação de anamnese (docssuperpowersspecs, Seção 2 e 5.1)]] - document - docs/superpowers/plans/2026-10-21-kb-secao-2.md
- [[Foco de revisão do plano]] - rationale - docs/superpowers/plans/2026-10-21-kb-secao-2.md
- [[Forma canônica de negação booleana (X = não)]] - rationale - docs/superpowers/plans/2026-10-21-kb-secao-2.md
- [[Gravacao atomica de versoes (mkstemp, fsync, os.link)]] - rationale - kb/README.md
- [[Guardas de execucao (CF positivo para urgencia e bandeira)]] - concept - engine/README.md
- [[JSON Schemas versionados e test_schema_sincronizado]] - concept - kb/README.md
- [[Pacote kb README (base de conhecimento)]] - document - kb/README.md
- [[Plano de implementação do kb (Seção 2)]] - document - docs/superpowers/plans/2026-10-21-kb-secao-2.md
- [[Portao de ativacao de versao (casos_falhando, confirmar_falhas)]] - concept - api/README.md
- [[Prioridade padrão por classe (100, 50, 10)]] - rationale - docs/superpowers/plans/2026-10-21-kb-secao-2.md
- [[Regra de produção (condições, conclusão, CF)]] - concept - docs/superpowers/plans/2026-10-21-kb-secao-2.md
- [[Restrições globais do kb]] - rationale - docs/superpowers/plans/2026-10-21-kb-secao-2.md
- [[Revisão do motor (docsrevisoes2026-10-21-revisao-motor.md)]] - document - docs/superpowers/plans/2026-10-21-kb-secao-2.md
- [[Script rodar.ps1  rodar.sh (execucao em localhost)]] - concept - api/README.md
- [[Seguranca de entrada carregar_base trata texto como caminho]] - rationale - kb/README.md
- [[Sementes de animais ficticios e reset seguro do banco]] - concept - api/README.md
- [[Servir webdist com rota coringa propria (apifrontend.py)]] - concept - api/README.md
- [[Sessao presa a versao da base com que nasceu]] - concept - api/README.md
- [[Símbolo (variável da base)]] - concept - docs/superpowers/plans/2026-10-21-kb-secao-2.md
- [[Tabela de códigos do validador (E01-E19, W01-W03)]] - concept - docs/superpowers/plans/2026-10-21-kb-secao-2.md
- [[Task 1 Ambiente e modelos Pydantic]] - document - docs/superpowers/plans/2026-10-21-kb-secao-2.md
- [[Task 2 Análise de dependências]] - document - docs/superpowers/plans/2026-10-21-kb-secao-2.md
- [[Task 3 Conversão base-grafo]] - document - docs/superpowers/plans/2026-10-21-kb-secao-2.md
- [[Task 4 Validador]] - document - docs/superpowers/plans/2026-10-21-kb-secao-2.md
- [[Task 5 Repositório de versões]] - document - docs/superpowers/plans/2026-10-21-kb-secao-2.md
- [[Task 6 Integração com o motor, schema e documentação]] - document - docs/superpowers/plans/2026-10-21-kb-secao-2.md
- [[Tela de triagem]] - concept - docs/superpowers/plans/2026-10-21-kb-secao-2.md
- [[Variaveis ANAMNESE_BASE_DIR e ANAMNESE_DB]] - concept - api/README.md
- [[engine.casos.executar_caso (casos de teste reproduziveis)]] - concept - engine/README.md
- [[kbanalise.py (dependencias, ciclo, ordem topologica)]] - concept - kb/README.md
- [[kbcarregador.py Repositorio (versoes imutaveis, ativa.json, hash sha256)]] - concept - kb/README.md
- [[kbgrafo.py (conversao 11 Base - grafo bipartido)]] - concept - kb/README.md
- [[kbmodelos.py (modelos Pydantic, carregar_base, para_motor)]] - concept - kb/README.md
- [[kbvalidador.py (validar, validar_dados, validar_edicao, Relatorio)]] - concept - kb/README.md

## Live Query (requires Dataview plugin)

```dataview
TABLE source_file, type FROM #community/Versões_da_base_casos_e_execução_local
SORT file.name ASC
```

## Connections to other communities
- 4 edges to [[_COMMUNITY_README da API e decisões]]

## Top bridge nodes
- [[Pacote kb README (base de conhecimento)]] - degree 8, connects to 1 community
- [[kbmodelos.py (modelos Pydantic, carregar_base, para_motor)]] - degree 6, connects to 1 community
- [[engine.casos.executar_caso (casos de teste reproduziveis)]] - degree 2, connects to 1 community