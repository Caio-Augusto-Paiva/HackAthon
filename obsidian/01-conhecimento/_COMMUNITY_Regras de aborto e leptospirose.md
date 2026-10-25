---
type: community
cohesion: 0.17
members: 12
---

# Regras de aborto e leptospirose

**Cohesion:** 0.17 - loosely connected
**Members:** 12 nodes

## Members
- [[Aborto recente (aborto_recente)]] - concept - docs/entrega/03-regras-de-producao.md
- [[Falhas reprodutivas no lote (falhas_reprodutivas_lote)]] - concept - docs/entrega/03-regras-de-producao.md
- [[Leite rosado ou com sangue (leite_com_sangue)]] - concept - docs/entrega/03-regras-de-producao.md
- [[Leptospirose (leptospirose)]] - concept - docs/entrega/03-regras-de-producao.md
- [[Seção Leptospirose (gravidade alta)]] - concept - docs/entrega/03-regras-de-producao.md
- [[Sorologia para leptospirose reagente (sorologia_leptospirose_reagente)]] - concept - docs/entrega/03-regras-de-producao.md
- [[`R-BRU-01` aborto_recente = sim E historico_retencao_placenta = sim - brucelose (CF 0,4)]] - concept - docs/entrega/03-regras-de-producao.md
- [[`R-BVD-02` aborto_recente = sim E falhas_reprodutivas_lote = sim E febre = sim - bvd (CF 0,4)]] - concept - docs/entrega/03-regras-de-producao.md
- [[`R-LEP-01` aborto_recente = sim E febre = sim - leptospirose (CF 0,4)]] - concept - docs/entrega/03-regras-de-producao.md
- [[`R-LEP-02` leite_com_sangue = sim E queda_producao = sim - leptospirose (CF 0,6)]] - concept - docs/entrega/03-regras-de-producao.md
- [[`R-LEP-03` sorologia_leptospirose_reagente = sim - leptospirose (CF 0,85)]] - concept - docs/entrega/03-regras-de-producao.md
- [[`R-URG-17` leptospirose = sim CF ≥ 0,5 - chamar_agora (CF 0,99)]] - concept - docs/entrega/03-regras-de-producao.md

## Live Query (requires Dataview plugin)

```dataview
TABLE source_file, type FROM #community/Regras_de_aborto_e_leptospirose
SORT file.name ASC
```

## Connections to other communities
- 6 edges to [[_COMMUNITY_Camada 2 regras de doença]]
- 6 edges to [[_COMMUNITY_Regras de produção e CF]]
- 5 edges to [[_COMMUNITY_Regras de cetose e deslocamento]]
- 3 edges to [[_COMMUNITY_Hipocalcemia e periparto]]
- 2 edges to [[_COMMUNITY_Brucelose, PNCEBT e urgências]]
- 1 edge to [[_COMMUNITY_TPB e derivado febre]]
- 1 edge to [[_COMMUNITY_Regras de acidose e BVD]]
- 1 edge to [[_COMMUNITY_Regras de metrite e retenção]]
- 1 edge to [[_COMMUNITY_Regras do modo bovino urgente]]

## Top bridge nodes
- [[Leptospirose (leptospirose)]] - degree 9, connects to 4 communities
- [[`R-BVD-02` aborto_recente = sim E falhas_reprodutivas_lote = sim E febre = sim - bvd (CF 0,4)]] - degree 5, connects to 3 communities
- [[`R-BRU-01` aborto_recente = sim E historico_retencao_placenta = sim - brucelose (CF 0,4)]] - degree 4, connects to 3 communities
- [[Aborto recente (aborto_recente)]] - degree 5, connects to 2 communities
- [[`R-LEP-01` aborto_recente = sim E febre = sim - leptospirose (CF 0,4)]] - degree 4, connects to 2 communities