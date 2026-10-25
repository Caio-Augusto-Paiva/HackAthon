---
type: community
cohesion: 0.13
members: 20
---

# Regras de acidose e BVD

**Cohesion:** 0.13 - loosely connected
**Members:** 20 nodes

## Members
- [[Acidose Ruminal (acidose)]] - concept - docs/entrega/03-regras-de-producao.md
- [[BVDV detectado (antigeno_bvdv)]] - concept - docs/entrega/03-regras-de-producao.md
- [[Diarreia (diarreia)]] - concept - docs/entrega/03-regras-de-producao.md
- [[Diarreia Viral Bovina (BVD) (bvd)]] - concept - docs/entrega/03-regras-de-producao.md
- [[Feridas na boca (feridas_boca)]] - concept - docs/entrega/03-regras-de-producao.md
- [[Fezes com espuma e grãos (fezes_aquosas_espuma_graos)]] - concept - docs/entrega/03-regras-de-producao.md
- [[Mudança abrupta de concentrado (mudanca_abrupta_concentrado)]] - concept - docs/entrega/03-regras-de-producao.md
- [[Seção Acidose Ruminal (gravidade media)]] - concept - docs/entrega/03-regras-de-producao.md
- [[Seção Diarreia Viral Bovina (BVD) (gravidade alta)]] - concept - docs/entrega/03-regras-de-producao.md
- [[`R-ACI-01` diarreia = sim E apetite em {reduzido, ausente} - acidose (CF 0,35)]] - concept - docs/entrega/03-regras-de-producao.md
- [[`R-ACI-02` mudanca_abrupta_concentrado = sim E diarreia = sim - acidose (CF 0,55)]] - concept - docs/entrega/03-regras-de-producao.md
- [[`R-ACI-03` fezes_aquosas_espuma_graos = sim - acidose (CF 0,5)]] - concept - docs/entrega/03-regras-de-producao.md
- [[`R-ACI-04` ph_ruminal  5,5 - acidose (CF 0,88)]] - concept - docs/entrega/03-regras-de-producao.md
- [[`R-ACI-05` apetite em {reduzido, ausente} - acidose (CF 0,05)]] - concept - docs/entrega/03-regras-de-producao.md
- [[`R-BVD-01` diarreia = sim E feridas_boca = sim - bvd (CF 0,6)]] - concept - docs/entrega/03-regras-de-producao.md
- [[`R-BVD-03` antigeno_bvdv = sim - bvd (CF 0,9)]] - concept - docs/entrega/03-regras-de-producao.md
- [[`R-BVD-04` diarreia = sim E febre = sim - bvd (CF 0,1)]] - concept - docs/entrega/03-regras-de-producao.md
- [[`R-BVD-05` fezes_aquosas_espuma_graos = sim E mudanca_abrupta_concentrado = sim - bvd (CF -0,4)]] - concept - docs/entrega/03-regras-de-producao.md
- [[`R-URG-19` bvd = sim CF ≥ 0,5 - chamar_agora (CF 0,99)]] - concept - docs/entrega/03-regras-de-producao.md
- [[pH ruminal (ph_ruminal)]] - concept - docs/entrega/03-regras-de-producao.md

## Live Query (requires Dataview plugin)

```dataview
TABLE source_file, type FROM #community/Regras_de_acidose_e_BVD
SORT file.name ASC
```

## Connections to other communities
- 10 edges to [[_COMMUNITY_Regras de cetose e deslocamento]]
- 10 edges to [[_COMMUNITY_Regras de produção e CF]]
- 9 edges to [[_COMMUNITY_Camada 2 regras de doença]]
- 3 edges to [[_COMMUNITY_Hipocalcemia e periparto]]
- 2 edges to [[_COMMUNITY_Brucelose, PNCEBT e urgências]]
- 1 edge to [[_COMMUNITY_Regras de aborto e leptospirose]]
- 1 edge to [[_COMMUNITY_Regras do modo bovino urgente]]
- 1 edge to [[_COMMUNITY_Regras de metrite e retenção]]

## Top bridge nodes
- [[Acidose Ruminal (acidose)]] - degree 11, connects to 3 communities
- [[Diarreia Viral Bovina (BVD) (bvd)]] - degree 10, connects to 3 communities
- [[Diarreia (diarreia)]] - degree 7, connects to 3 communities
- [[`R-ACI-05` apetite em {reduzido, ausente} - acidose (CF 0,05)]] - degree 4, connects to 3 communities
- [[`R-BVD-04` diarreia = sim E febre = sim - bvd (CF 0,1)]] - degree 5, connects to 2 communities