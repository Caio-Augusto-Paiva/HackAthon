---
type: community
cohesion: 0.25
members: 9
---

# Casos clínicos e fonte

**Cohesion:** 0.25 - loosely connected
**Members:** 9 nodes

## Members
- [[34 casos clínicos com mesmo resultado lendo v0002 e grafo exato]] - concept - docs/superpowers/specs/2026-10-22-grafo-dados-por-doenca-design.md
- [[CLI python -m kb.fonte separar, juntar, juntar --salvar]] - code - docs/superpowers/specs/2026-10-22-grafo-dados-por-doenca-design.md
- [[Invariante juntar(separar(v0002)) == v0002]] - concept - docs/superpowers/specs/2026-10-22-grafo-dados-por-doenca-design.md
- [[Objetivos separar, editar em basefonte, grafo 2 sem IA, motor lê do grafo exato]] - concept - docs/superpowers/specs/2026-10-22-grafo-dados-por-doenca-design.md
- [[Repositorio.salvar_nova valida antes de gravar]] - code - docs/superpowers/specs/2026-10-22-grafo-dados-por-doenca-design.md
- [[Testes da spec]] - concept - docs/superpowers/specs/2026-10-22-grafo-dados-por-doenca-design.md
- [[basefonte passa a ser o que a equipe edita; juntar gera próxima versão via salvar_nova]] - concept - docs/superpowers/specs/2026-10-22-grafo-dados-por-doenca-design.md
- [[testskbtest_exportar_grafo.py_1]] - code - docs/superpowers/specs/2026-10-22-grafo-dados-por-doenca-design.md
- [[testskbtest_fonte.py_1]] - code - docs/superpowers/specs/2026-10-22-grafo-dados-por-doenca-design.md

## Live Query (requires Dataview plugin)

```dataview
TABLE source_file, type FROM #community/Casos_clínicos_e_fonte
SORT file.name ASC
```

## Connections to other communities
- 2 edges to [[_COMMUNITY_Parecer e urgência na interface]]
- 2 edges to [[_COMMUNITY_Cliente nunca envia CF]]
- 1 edge to [[_COMMUNITY_Documentação e backend FastAPI]]
- 1 edge to [[_COMMUNITY_Fonte inválida e Review Focus]]
- 1 edge to [[_COMMUNITY_Exportação do grafo de dados]]
- 1 edge to [[_COMMUNITY_API pública da base]]
- 1 edge to [[_COMMUNITY_Arquitetura de kb]]

## Top bridge nodes
- [[Objetivos separar, editar em basefonte, grafo 2 sem IA, motor lê do grafo exato]] - degree 5, connects to 2 communities
- [[testskbtest_exportar_grafo.py_1]] - degree 4, connects to 2 communities
- [[34 casos clínicos com mesmo resultado lendo v0002 e grafo exato]] - degree 3, connects to 1 community
- [[Repositorio.salvar_nova valida antes de gravar]] - degree 3, connects to 1 community
- [[testskbtest_fonte.py_1]] - degree 3, connects to 1 community