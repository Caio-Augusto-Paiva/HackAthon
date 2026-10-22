---
type: community
cohesion: 0.21
members: 12
---

# Módulos de fonte e grafo

**Cohesion:** 0.21 - loosely connected
**Members:** 12 nodes

## Members
- [[Arquitetura kbfonte.py, kbexportar_grafo.py, scriptsgrafo_dados.py]] - concept - docs/superpowers/plans/2026-10-22-grafo-dados-por-doenca.md
- [[Custo de tokens zero (sem IA)]] - concept - docs/superpowers/specs/2026-10-22-grafo-dados-por-doenca-design.md
- [[Rótulos de comunidade pela doença predominante do source_file ou 'Comum']] - concept - docs/superpowers/plans/2026-10-22-grafo-dados-por-doenca.md
- [[Saídas graph.json, GRAPH_REPORT.md, graph.html e cofre Obsidian]] - concept - docs/superpowers/specs/2026-10-22-grafo-dados-por-doenca-design.md
- [[carregar_do_grafo(caminho) - Base]] - code - docs/superpowers/specs/2026-10-22-grafo-dados-por-doenca-design.md
- [[extracao.json no esquema do graphify (simid, regraid, condicao_de, conclui, EXTRACTED)]] - code - docs/superpowers/specs/2026-10-22-grafo-dados-por-doenca-design.md
- [[grafo_exato.json = base_para_grafo(base)]] - code - docs/superpowers/specs/2026-10-22-grafo-dados-por-doenca-design.md
- [[kbexportar_grafo.py]] - code - docs/superpowers/plans/2026-10-22-grafo-dados-por-doenca.md
- [[kbexportar_grafo.py — grafo exato e entrada do graphify]] - code - docs/superpowers/specs/2026-10-22-grafo-dados-por-doenca-design.md
- [[kbfonte.py]] - code - docs/superpowers/plans/2026-10-22-grafo-dados-por-doenca.md
- [[scriptsgrafo_dados.py (build_from_json dedup=False, cluster, relatório, HTML, cofre)]] - code - docs/superpowers/plans/2026-10-22-grafo-dados-por-doenca.md
- [[scriptsgrafo_dados.py — cofre e visualização (Python do graphify)]] - code - docs/superpowers/specs/2026-10-22-grafo-dados-por-doenca-design.md

## Live Query (requires Dataview plugin)

```dataview
TABLE source_file, type FROM #community/Módulos_de_fonte_e_grafo
SORT file.name ASC
```

## Connections to other communities
- 3 edges to [[_COMMUNITY_Grafo 2 por doença]]
- 3 edges to [[_COMMUNITY_Exportação do grafo exato]]
- 2 edges to [[_COMMUNITY_Formato em disco da fonte]]
- 2 edges to [[_COMMUNITY_Grafo exato e testes]]
- 1 edge to [[_COMMUNITY_Separar e juntar fonte]]
- 1 edge to [[_COMMUNITY_Cofre e visualização grafo 2]]

## Top bridge nodes
- [[kbexportar_grafo.py — grafo exato e entrada do graphify]] - degree 6, connects to 2 communities
- [[carregar_do_grafo(caminho) - Base]] - degree 4, connects to 2 communities
- [[kbfonte.py]] - degree 3, connects to 2 communities
- [[scriptsgrafo_dados.py — cofre e visualização (Python do graphify)]] - degree 5, connects to 1 community
- [[Arquitetura kbfonte.py, kbexportar_grafo.py, scriptsgrafo_dados.py]] - degree 4, connects to 1 community