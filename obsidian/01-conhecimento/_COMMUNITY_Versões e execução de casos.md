---
type: community
members: 6
---

# Versões e execução de casos

**Members:** 6 nodes

## Members
- [[Comparacao de casos com a versao pai]] - concept - api/README.md
- [[Gravacao atomica de versoes (mkstemp, fsync, os.link)]] - rationale - kb/README.md
- [[Portao de ativacao de versao (casos_falhando, confirmar_falhas)]] - concept - api/README.md
- [[Sessao presa a versao da base com que nasceu]] - concept - api/README.md
- [[engine.casos.executar_caso (casos de teste reproduziveis)]] - concept - engine/README.md
- [[kbcarregador.py Repositorio (versoes imutaveis, ativa.json, hash sha256)]] - concept - kb/README.md

## Live Query (requires Dataview plugin)

```dataview
TABLE source_file, type FROM #community/Versões_e_execução_de_casos
SORT file.name ASC
```

## Connections to other communities
- 2 edges to [[_COMMUNITY_Modelos e validação do kb]]
- 1 edge to [[_COMMUNITY_Sessões, API e motor]]
- 1 edge to [[_COMMUNITY_Casos sintéticos na v0002]]

## Top bridge nodes
- [[kbcarregador.py Repositorio (versoes imutaveis, ativa.json, hash sha256)]] - degree 6, connects to 2 communities
- [[engine.casos.executar_caso (casos de teste reproduziveis)]] - degree 2, connects to 1 community