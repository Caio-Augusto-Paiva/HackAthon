---
type: community
cohesion: 0.25
members: 8
---

# Reticulopericardite traumática

**Cohesion:** 0.25 - loosely connected
**Members:** 8 nodes

## Members
- [[Edema de barbela ou peito (edema_barbela)]] - concept - docs/entrega/03-regras-de-producao.md
- [[Prova de dor reticular (prova_dor_reticular)]] - concept - docs/entrega/03-regras-de-producao.md
- [[Reticulopericardite Traumática (reticulopericardite_traumatica)]] - concept - docs/entrega/03-regras-de-producao.md
- [[Seção Reticulopericardite Traumática (gravidade alta)]] - concept - docs/entrega/03-regras-de-producao.md
- [[`R-RPT-03` prova_dor_reticular = sim - reticulopericardite_traumatica (CF 0,85)]] - concept - docs/entrega/03-regras-de-producao.md
- [[`R-RPT-04` edema_barbela = sim E febre = sim - reticulopericardite_traumatica (CF 0,6)]] - concept - docs/entrega/03-regras-de-producao.md
- [[`R-RPT-05` apetite em {reduzido, ausente} E queda_producao = sim E febre = sim - reticulopericardite_traumatica (CF 0,1)]] - concept - docs/entrega/03-regras-de-producao.md
- [[`R-URG-14` reticulopericardite_traumatica = sim CF ≥ 0,5 - chamar_agora (CF 0,99)]] - concept - docs/entrega/03-regras-de-producao.md

## Live Query (requires Dataview plugin)

```dataview
TABLE source_file, type FROM #community/Reticulopericardite_traumática
SORT file.name ASC
```

## Connections to other communities
- 5 edges to [[_COMMUNITY_Camada 2 regras de doença]]
- 5 edges to [[_COMMUNITY_Regras de cetose e deslocamento]]
- 4 edges to [[_COMMUNITY_Regras de produção e CF]]
- 3 edges to [[_COMMUNITY_Hipocalcemia e periparto]]
- 1 edge to [[_COMMUNITY_Regras do modo bovino urgente]]
- 1 edge to [[_COMMUNITY_Brucelose, PNCEBT e urgências]]

## Top bridge nodes
- [[Reticulopericardite Traumática (reticulopericardite_traumatica)]] - degree 9, connects to 3 communities
- [[`R-RPT-05` apetite em {reduzido, ausente} E queda_producao = sim E febre = sim - reticulopericardite_traumatica (CF 0,1)]] - degree 6, connects to 3 communities
- [[`R-RPT-04` edema_barbela = sim E febre = sim - reticulopericardite_traumatica (CF 0,6)]] - degree 4, connects to 2 communities
- [[`R-URG-14` reticulopericardite_traumatica = sim CF ≥ 0,5 - chamar_agora (CF 0,99)]] - degree 3, connects to 2 communities
- [[Edema de barbela ou peito (edema_barbela)]] - degree 3, connects to 2 communities