---
type: community
cohesion: 0.22
members: 10
---

# TPB e derivado febre

**Cohesion:** 0.22 - loosely connected
**Members:** 10 nodes

## Members
- [[Exposição recente a carrapatos (carrapatos_historico_recente)]] - concept - docs/entrega/03-regras-de-producao.md
- [[Hemoparasitas no esfregaço (esfregaco_hemoparasitas)]] - concept - docs/entrega/03-regras-de-producao.md
- [[Mucosas pálidas ou amareladas (mucosas_palidas_ou_ictericas)]] - concept - docs/entrega/03-regras-de-producao.md
- [[Seção Tristeza Parasitária Bovina (gravidade alta)]] - concept - docs/entrega/03-regras-de-producao.md
- [[Tristeza Parasitária Bovina (tpb)]] - concept - docs/entrega/03-regras-de-producao.md
- [[`R-LEP-05` esfregaco_hemoparasitas = sim - leptospirose (CF -0,5)]] - concept - docs/entrega/03-regras-de-producao.md
- [[`R-TPB-02` mucosas_palidas_ou_ictericas = sim - tpb (CF 0,6)]] - concept - docs/entrega/03-regras-de-producao.md
- [[`R-TPB-03` carrapatos_historico_recente = sim E febre = sim - tpb (CF 0,35)]] - concept - docs/entrega/03-regras-de-producao.md
- [[`R-TPB-04` esfregaco_hemoparasitas = sim - tpb (CF 0,9)]] - concept - docs/entrega/03-regras-de-producao.md
- [[`R-URG-02` tpb = sim CF ≥ 0,5 - chamar_agora (CF 0,99)]] - concept - docs/entrega/03-regras-de-producao.md

## Live Query (requires Dataview plugin)

```dataview
TABLE source_file, type FROM #community/TPB_e_derivado_febre
SORT file.name ASC
```

## Connections to other communities
- 5 edges to [[_COMMUNITY_Regras de produção e CF]]
- 4 edges to [[_COMMUNITY_Camada 2 regras de doença]]
- 4 edges to [[_COMMUNITY_Regras de cetose e deslocamento]]
- 2 edges to [[_COMMUNITY_Hipocalcemia e periparto]]
- 1 edge to [[_COMMUNITY_Regras de aborto e leptospirose]]
- 1 edge to [[_COMMUNITY_Regras do modo bovino urgente]]
- 1 edge to [[_COMMUNITY_Brucelose, PNCEBT e urgências]]

## Top bridge nodes
- [[Tristeza Parasitária Bovina (tpb)]] - degree 9, connects to 3 communities
- [[`R-LEP-05` esfregaco_hemoparasitas = sim - leptospirose (CF -0,5)]] - degree 4, connects to 2 communities
- [[`R-TPB-03` carrapatos_historico_recente = sim E febre = sim - tpb (CF 0,35)]] - degree 4, connects to 2 communities
- [[Hemoparasitas no esfregaço (esfregaco_hemoparasitas)]] - degree 4, connects to 2 communities
- [[`R-URG-02` tpb = sim CF ≥ 0,5 - chamar_agora (CF 0,99)]] - degree 3, connects to 2 communities