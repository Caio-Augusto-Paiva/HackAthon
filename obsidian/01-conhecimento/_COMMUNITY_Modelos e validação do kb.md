---
type: community
members: 11
---

# Modelos e validação do kb

**Members:** 11 nodes

## Members
- [[Codigos do validador E00-E23 e W01-W03]] - concept - kb/README.md
- [[D4 EdicaoBase frouxa (erros de estrutura viram E00)]] - rationale - api/README.md
- [[Dados ficticios e regras como suposicao a validar]] - concept - kb/README.md
- [[Guardas de execucao (CF positivo para urgencia e bandeira)]] - concept - engine/README.md
- [[JSON Schemas versionados e test_schema_sincronizado]] - concept - kb/README.md
- [[Pacote kb README (base de conhecimento)]] - document - kb/README.md
- [[Seguranca de entrada carregar_base trata texto como caminho]] - rationale - kb/README.md
- [[kbanalise.py (dependencias, ciclo, ordem topologica)]] - concept - kb/README.md
- [[kbgrafo.py (conversao 11 Base - grafo bipartido)]] - concept - kb/README.md
- [[kbmodelos.py (modelos Pydantic, carregar_base, para_motor)]] - concept - kb/README.md
- [[kbvalidador.py (validar, validar_dados, validar_edicao, Relatorio)]] - concept - kb/README.md

## Live Query (requires Dataview plugin)

```dataview
TABLE source_file, type FROM #community/Modelos_e_validação_do_kb
SORT file.name ASC
```

## Connections to other communities
- 5 edges to [[_COMMUNITY_Persistência e validação da base]]
- 3 edges to [[_COMMUNITY_Backend e isolamento do motor]]
- 2 edges to [[_COMMUNITY_Versões e execução de casos]]
- 1 edge to [[_COMMUNITY_Contratos e integração localhost]]
- 1 edge to [[_COMMUNITY_Entrega e manutenção documental]]
- 1 edge to [[_COMMUNITY_Snapshot e pressupostos do motor]]

## Top bridge nodes
- [[kbvalidador.py (validar, validar_dados, validar_edicao, Relatorio)]] - degree 10, connects to 3 communities
- [[Pacote kb README (base de conhecimento)]] - degree 9, connects to 3 communities
- [[kbmodelos.py (modelos Pydantic, carregar_base, para_motor)]] - degree 7, connects to 3 communities
- [[kbgrafo.py (conversao 11 Base - grafo bipartido)]] - degree 4, connects to 1 community
- [[kbanalise.py (dependencias, ciclo, ordem topologica)]] - degree 3, connects to 1 community