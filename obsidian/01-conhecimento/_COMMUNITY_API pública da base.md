---
type: community
cohesion: 0.17
members: 13
---

# API pública da base

**Cohesion:** 0.17 - loosely connected
**Members:** 13 nodes

## Members
- [[API pública separar, gravar_fonte, ler_fonte]] - code - docs/superpowers/specs/2026-10-22-grafo-dados-por-doenca-design.md
- [[CLI python -m kb.fonte separar, juntar, juntar --salvar]] - code - docs/superpowers/specs/2026-10-22-grafo-dados-por-doenca-design.md
- [[Erros da junção id duplicado, doença sem símbolo tipo doenca, JSON inválido]] - concept - docs/superpowers/specs/2026-10-22-grafo-dados-por-doenca-design.md
- [[Formato em disco de basefonte]] - concept - docs/superpowers/specs/2026-10-22-grafo-dados-por-doenca-design.md
- [[Ids novos entram ao final; ids sumidos do índice são removidos (edição legítima)]] - concept - docs/superpowers/specs/2026-10-22-grafo-dados-por-doenca-design.md
- [[Junção une comum e doencas.json, ordena pelo índice]] - concept - docs/superpowers/specs/2026-10-22-grafo-dados-por-doenca-design.md
- [[Repositorio.salvar_nova valida antes de gravar]] - code - docs/superpowers/specs/2026-10-22-grafo-dados-por-doenca-design.md
- [[Serialização igual à do repositório (ensure_ascii=False, indent 2, exclude_none)]] - concept - docs/superpowers/specs/2026-10-22-grafo-dados-por-doenca-design.md
- [[basefonte passa a ser o que a equipe edita; juntar gera próxima versão via salvar_nova]] - concept - docs/superpowers/specs/2026-10-22-grafo-dados-por-doenca-design.md
- [[comum.json (meta, simbolos, regras, layout)]] - code - docs/superpowers/specs/2026-10-22-grafo-dados-por-doenca-design.md
- [[doencasid.json (doenca, simbolos, regras)]] - code - docs/superpowers/specs/2026-10-22-grafo-dados-por-doenca-design.md
- [[indice.json (ordem_simbolos, ordem_regras)]] - code - docs/superpowers/specs/2026-10-22-grafo-dados-por-doenca-design.md
- [[kbfonte.py — separar e juntar]] - code - docs/superpowers/specs/2026-10-22-grafo-dados-por-doenca-design.md

## Live Query (requires Dataview plugin)

```dataview
TABLE source_file, type FROM #community/API_pública_da_base
SORT file.name ASC
```

## Connections to other communities
- 3 edges to [[_COMMUNITY_Cliente nunca envia CF]]
- 2 edges to [[_COMMUNITY_Fonte inválida e Review Focus]]
- 1 edge to [[_COMMUNITY_Documentação e backend FastAPI]]
- 1 edge to [[_COMMUNITY_Parecer e urgência na interface (2)]]
- 1 edge to [[_COMMUNITY_Arrumação e rótulos do grafo]]

## Top bridge nodes
- [[kbfonte.py — separar e juntar]] - degree 10, connects to 4 communities
- [[Junção une comum e doencas.json, ordena pelo índice]] - degree 5, connects to 1 community
- [[Repositorio.salvar_nova valida antes de gravar]] - degree 3, connects to 1 community
- [[basefonte passa a ser o que a equipe edita; juntar gera próxima versão via salvar_nova]] - degree 2, connects to 1 community