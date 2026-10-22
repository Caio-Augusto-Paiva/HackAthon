---
type: community
cohesion: 0.24
members: 11
---

# Separar e juntar fonte

**Cohesion:** 0.24 - loosely connected
**Members:** 11 nodes

## Members
- [[CLI python -m kb.fonte separarjuntar (--salvar --autor --nota)]] - code - docs/superpowers/plans/2026-10-22-grafo-dados-por-doenca.md
- [[Junção arquivos em ordem alfabética, ordena pelo índice, desconhecidos ao final]] - concept - docs/superpowers/plans/2026-10-22-grafo-dados-por-doenca.md
- [[Regras de separação determinísticas]] - concept - docs/superpowers/specs/2026-10-22-grafo-dados-por-doenca-design.md
- [[Regras de separação uso transitivo, exclusivo à doença, urgência, resto em comum]] - concept - docs/superpowers/plans/2026-10-22-grafo-dados-por-doenca.md
- [[Task 1 separar e juntar (kbfonte.py)]] - concept - docs/superpowers/plans/2026-10-22-grafo-dados-por-doenca.md
- [[Uso de uma doença D símbolos das condições das regras que concluem D, com derivados transitivos]] - concept - docs/superpowers/specs/2026-10-22-grafo-dados-por-doenca-design.md
- [[Vai para comum.json meta, layout, compartilhados, bandeiras vermelhas, derivados compartilhados]] - concept - docs/superpowers/specs/2026-10-22-grafo-dados-por-doenca-design.md
- [[Vai para o arquivo de D símbolo D, símbolos exclusivos, regras de D, derivados exclusivos, urgência citando D]] - concept - docs/superpowers/specs/2026-10-22-grafo-dados-por-doenca-design.md
- [[gravar_fonte(base, pasta)]] - code - docs/superpowers/plans/2026-10-22-grafo-dados-por-doenca.md
- [[ler_fonte(pasta) - Base]] - code - docs/superpowers/plans/2026-10-22-grafo-dados-por-doenca.md
- [[separar(base) - dictstr, dict]] - code - docs/superpowers/plans/2026-10-22-grafo-dados-por-doenca.md

## Live Query (requires Dataview plugin)

```dataview
TABLE source_file, type FROM #community/Separar_e_juntar_fonte
SORT file.name ASC
```

## Connections to other communities
- 3 edges to [[_COMMUNITY_Testes de leitura da fonte]]
- 2 edges to [[_COMMUNITY_Exportação do grafo exato]]
- 2 edges to [[_COMMUNITY_Formato em disco da fonte]]
- 1 edge to [[_COMMUNITY_Especificação e arquitetura do sistema]]
- 1 edge to [[_COMMUNITY_Módulos de fonte e grafo]]

## Top bridge nodes
- [[Task 1 separar e juntar (kbfonte.py)]] - degree 10, connects to 3 communities
- [[ler_fonte(pasta) - Base]] - degree 5, connects to 3 communities
- [[Regras de separação determinísticas]] - degree 5, connects to 1 community
- [[Junção arquivos em ordem alfabética, ordena pelo índice, desconhecidos ao final]] - degree 3, connects to 1 community