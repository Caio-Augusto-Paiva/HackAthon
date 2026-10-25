---
type: community
cohesion: 0.13
members: 21
---

# Brucelose, PNCEBT e urgências

**Cohesion:** 0.13 - loosely connected
**Members:** 21 nodes

## Members
- [[Brucelose (brucelose)]] - concept - docs/entrega/03-regras-de-producao.md
- [[Camada 3 - Urgências]] - concept - docs/entrega/03-regras-de-producao.md
- [[Inchaço nos joelhos (higroma)]] - concept - docs/entrega/03-regras-de-producao.md
- [[Monitoramento Clínico Contínuo (observar)]] - concept - docs/entrega/03-regras-de-producao.md
- [[PNCEBT  MAPA (notificação obrigatória)]] - concept - docs/entrega/03-regras-de-producao.md
- [[Seção Brucelose (gravidade alta)]] - concept - docs/entrega/03-regras-de-producao.md
- [[Sorologia para brucelose reagente (sorologia_brucelose_reagente)]] - concept - docs/entrega/03-regras-de-producao.md
- [[Vacinada contra brucelose (vacinada_brucelose)]] - concept - docs/entrega/03-regras-de-producao.md
- [[`R-BRU-02` higroma = sim - brucelose (CF 0,4)]] - concept - docs/entrega/03-regras-de-producao.md
- [[`R-BRU-03` sorologia_brucelose_reagente = sim - brucelose (CF 0,9)]] - concept - docs/entrega/03-regras-de-producao.md
- [[`R-BRU-04` corrimento_vaginal = sim - brucelose (CF 0,05)]] - concept - docs/entrega/03-regras-de-producao.md
- [[`R-BRU-05` vacinada_brucelose = sim - brucelose (CF -0,4)]] - concept - docs/entrega/03-regras-de-producao.md
- [[`R-URG-05` mastite = sim CF ≥ 0,5 - observar (CF 0,8)]] - concept - docs/entrega/03-regras-de-producao.md
- [[`R-URG-06` cetose = sim CF ≥ 0,5 - observar (CF 0,8)]] - concept - docs/entrega/03-regras-de-producao.md
- [[`R-URG-07` acidose = sim CF ≥ 0,5 - observar (CF 0,8)]] - concept - docs/entrega/03-regras-de-producao.md
- [[`R-URG-08` dermatite_digital = sim CF ≥ 0,5 - observar (CF 0,7)]] - concept - docs/entrega/03-regras-de-producao.md
- [[`R-URG-12` retencao_placenta = sim CF ≥ 0,5 - observar (CF 0,8)]] - concept - docs/entrega/03-regras-de-producao.md
- [[`R-URG-13` pneumonia = sim CF ≥ 0,5 - observar (CF 0,8)]] - concept - docs/entrega/03-regras-de-producao.md
- [[`R-URG-16` brucelose = sim CF ≥ 0,5 - chamar_agora (CF 0,99)]] - concept - docs/entrega/03-regras-de-producao.md
- [[`R-URG-18` ibr = sim CF ≥ 0,5 - observar (CF 0,8)]] - concept - docs/entrega/03-regras-de-producao.md
- [[`R-URG-20` tuberculose = sim CF ≥ 0,5 - chamar_agora (CF 0,99)]] - concept - docs/entrega/03-regras-de-producao.md

## Live Query (requires Dataview plugin)

```dataview
TABLE source_file, type FROM #community/Brucelose_PNCEBT_e_urgências
SORT file.name ASC
```

## Connections to other communities
- 9 edges to [[_COMMUNITY_Regras de produção e CF]]
- 8 edges to [[_COMMUNITY_Camada 2 regras de doença]]
- 7 edges to [[_COMMUNITY_Regras de cetose e deslocamento]]
- 4 edges to [[_COMMUNITY_Regras do modo bovino urgente]]
- 3 edges to [[_COMMUNITY_Regras de metrite e retenção]]
- 2 edges to [[_COMMUNITY_Hipocalcemia e periparto]]
- 2 edges to [[_COMMUNITY_Regras de aborto e leptospirose]]
- 2 edges to [[_COMMUNITY_Regras de acidose e BVD]]
- 2 edges to [[_COMMUNITY_Regras de IBR e pneumonia]]
- 1 edge to [[_COMMUNITY_TPB e derivado febre]]
- 1 edge to [[_COMMUNITY_Reticulopericardite traumática]]

## Top bridge nodes
- [[Camada 3 - Urgências]] - degree 21, connects to 10 communities
- [[Brucelose (brucelose)]] - degree 9, connects to 3 communities
- [[`R-BRU-04` corrimento_vaginal = sim - brucelose (CF 0,05)]] - degree 4, connects to 3 communities
- [[Monitoramento Clínico Contínuo (observar)]] - degree 9, connects to 2 communities
- [[`R-URG-20` tuberculose = sim CF ≥ 0,5 - chamar_agora (CF 0,99)]] - degree 4, connects to 2 communities