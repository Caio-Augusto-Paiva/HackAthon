---
type: community
cohesion: 0.18
members: 12
---

# Regras do modo bovino urgente

**Cohesion:** 0.18 - loosely connected
**Members:** 12 nodes

## Members
- [[R-BV-01 decúbito → chamar_agora]] - concept - docs/entrega/03-regras-de-producao.md
- [[R-BV-02 urina escura → chamar_agora]] - concept - docs/entrega/03-regras-de-producao.md
- [[R-BV-03 apetite ausente + apatia → chamar_agora]] - concept - docs/entrega/03-regras-de-producao.md
- [[R-BV-04 hipotermia + apatia → chamar_agora]] - concept - docs/entrega/03-regras-de-producao.md
- [[R-BV-06 temperatura≥41 → chamar_agora]] - concept - docs/entrega/03-regras-de-producao.md
- [[Seção Telas de triagem]] - document - docs/entrega/03-regras-de-producao.md
- [[Tela 2 estado_termico]] - concept - docs/entrega/03-regras-de-producao.md
- [[Tela 3 atitude_locomocao]] - concept - docs/entrega/03-regras-de-producao.md
- [[Tela 4 apetite_ruminacao]] - concept - docs/entrega/03-regras-de-producao.md
- [[Tela 5 producao_leite]] - concept - docs/entrega/03-regras-de-producao.md
- [[Tela 6 excrecoes]] - concept - docs/entrega/03-regras-de-producao.md
- [[Urgência chamar_agora (Atendimento Veterinário Imediato)]] - concept - docs/entrega/03-regras-de-producao.md

## Live Query (requires Dataview plugin)

```dataview
TABLE source_file, type FROM #community/Regras_do_modo_bovino_urgente
SORT file.name ASC
```

## Connections to other communities
- 3 edges to [[_COMMUNITY_TPB e derivado febre]]
- 2 edges to [[_COMMUNITY_Hipocalcemia e periparto]]
- 1 edge to [[_COMMUNITY_Cetose e deslocamento de abomaso]]
- 1 edge to [[_COMMUNITY_Metrite e puerpério]]
- 1 edge to [[_COMMUNITY_Camadas de inferência]]

## Top bridge nodes
- [[Urgência chamar_agora (Atendimento Veterinário Imediato)]] - degree 10, connects to 4 communities
- [[Seção Telas de triagem]] - degree 6, connects to 1 community
- [[R-BV-04 hipotermia + apatia → chamar_agora]] - degree 2, connects to 1 community
- [[Tela 2 estado_termico]] - degree 2, connects to 1 community