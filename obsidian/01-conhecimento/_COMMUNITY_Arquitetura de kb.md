---
type: community
cohesion: 0.40
members: 6
---

# Arquitetura de kb

**Cohesion:** 0.40 - moderately connected
**Members:** 6 nodes

## Members
- [[Arquitetura kbfonte.py, kbexportar_grafo.py, scriptsgrafo_dados.py]] - concept - docs/superpowers/plans/2026-10-22-grafo-dados-por-doenca.md
- [[carregar_do_grafo(caminho) - Base_1]] - code - docs/superpowers/specs/2026-10-22-grafo-dados-por-doenca-design.md
- [[grafo_exato.json = base_para_grafo(base)]] - code - docs/superpowers/specs/2026-10-22-grafo-dados-por-doenca-design.md
- [[kbexportar_grafo.py]] - code - docs/superpowers/plans/2026-10-22-grafo-dados-por-doenca.md
- [[kbexportar_grafo.py — grafo exato e entrada do graphify]] - code - docs/superpowers/specs/2026-10-22-grafo-dados-por-doenca-design.md
- [[kbfonte.py]] - code - docs/superpowers/plans/2026-10-22-grafo-dados-por-doenca.md

## Live Query (requires Dataview plugin)

```dataview
TABLE source_file, type FROM #community/Arquitetura_de_kb
SORT file.name ASC
```

## Connections to other communities
- 2 edges to [[_COMMUNITY_Cliente nunca envia CF]]
- 2 edges to [[_COMMUNITY_Arrumação e rótulos do grafo]]
- 2 edges to [[_COMMUNITY_Exportação do grafo de dados]]
- 2 edges to [[_COMMUNITY_API pública da base]]
- 1 edge to [[_COMMUNITY_Parecer e urgência na interface]]
- 1 edge to [[_COMMUNITY_CLI de fonte por doença]]
- 1 edge to [[_COMMUNITY_Casos clínicos e fonte]]

## Top bridge nodes
- [[kbexportar_grafo.py — grafo exato e entrada do graphify]] - degree 6, connects to 3 communities
- [[Arquitetura kbfonte.py, kbexportar_grafo.py, scriptsgrafo_dados.py]] - degree 4, connects to 2 communities
- [[carregar_do_grafo(caminho) - Base_1]] - degree 4, connects to 2 communities
- [[kbfonte.py]] - degree 3, connects to 2 communities
- [[kbexportar_grafo.py]] - degree 3, connects to 1 community