---
type: community
cohesion: 0.22
members: 10
---

# Formato em disco da fonte

**Cohesion:** 0.22 - loosely connected
**Members:** 10 nodes

## Members
- [[API pública separar, gravar_fonte, ler_fonte]] - code - docs/superpowers/specs/2026-10-22-grafo-dados-por-doenca-design.md
- [[Erros da junção id duplicado, doença sem símbolo tipo doenca, JSON inválido]] - concept - docs/superpowers/specs/2026-10-22-grafo-dados-por-doenca-design.md
- [[Formato em disco de basefonte]] - concept - docs/superpowers/specs/2026-10-22-grafo-dados-por-doenca-design.md
- [[Ids novos entram ao final; ids sumidos do índice são removidos (edição legítima)]] - concept - docs/superpowers/specs/2026-10-22-grafo-dados-por-doenca-design.md
- [[Junção une comum e doencas.json, ordena pelo índice]] - concept - docs/superpowers/specs/2026-10-22-grafo-dados-por-doenca-design.md
- [[Serialização igual à do repositório (ensure_ascii=False, indent 2, exclude_none)]] - concept - docs/superpowers/specs/2026-10-22-grafo-dados-por-doenca-design.md
- [[comum.json (meta, simbolos, regras, layout)]] - code - docs/superpowers/specs/2026-10-22-grafo-dados-por-doenca-design.md
- [[doencasid.json (doenca, simbolos, regras)]] - code - docs/superpowers/specs/2026-10-22-grafo-dados-por-doenca-design.md
- [[indice.json (ordem_simbolos, ordem_regras)]] - code - docs/superpowers/specs/2026-10-22-grafo-dados-por-doenca-design.md
- [[kbfonte.py — separar e juntar]] - code - docs/superpowers/specs/2026-10-22-grafo-dados-por-doenca-design.md

## Live Query (requires Dataview plugin)

```dataview
TABLE source_file, type FROM #community/Formato_em_disco_da_fonte
SORT file.name ASC
```

## Connections to other communities
- 2 edges to [[_COMMUNITY_Módulos de fonte e grafo]]
- 2 edges to [[_COMMUNITY_Separar e juntar fonte]]
- 1 edge to [[_COMMUNITY_Especificação e arquitetura do sistema]]
- 1 edge to [[_COMMUNITY_Grafo 2 por doença]]
- 1 edge to [[_COMMUNITY_Grafo exato e testes]]

## Top bridge nodes
- [[kbfonte.py — separar e juntar]] - degree 10, connects to 5 communities
- [[Junção une comum e doencas.json, ordena pelo índice]] - degree 5, connects to 1 community