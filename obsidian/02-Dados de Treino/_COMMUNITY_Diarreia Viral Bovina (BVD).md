---
type: community
cohesion: 0.20
members: 10
---

# Diarreia Viral Bovina (BVD)

**Cohesion:** 0.20 - loosely connected
**Members:** 10 nodes

## Members
- [[BVDV detectado]] - concept - base/fonte/doencas/bvd.json
- [[Diarreia Viral Bovina (BVD)]] - concept - base/fonte/doencas/bvd.json
- [[Falhas reprodutivas no lote]] - concept - base/fonte/doencas/bvd.json
- [[Feridas na boca]] - concept - base/fonte/doencas/bvd.json
- [[R-BVD-01 SE Diarreia E Feridas na boca ENTÃO Diarreia Viral Bovina (BVD)]] - concept - base/fonte/doencas/bvd.json
- [[R-BVD-02 SE Aborto recente E Falhas reprodutivas no lote E Febre ENTÃO Diarreia Viral Bovina (BVD)]] - concept - base/fonte/doencas/bvd.json
- [[R-BVD-03 SE BVDV detectado ENTÃO Diarreia Viral Bovina (BVD)]] - concept - base/fonte/doencas/bvd.json
- [[R-BVD-04 SE Diarreia E Febre ENTÃO Diarreia Viral Bovina (BVD)]] - concept - base/fonte/doencas/bvd.json
- [[R-BVD-05 SE Fezes com espuma e grãos E Mudança abrupta de concentrado ENTÃO Diarreia Viral Bovina (BVD)]] - concept - base/fonte/doencas/bvd.json
- [[R-URG-19 SE Diarreia Viral Bovina (BVD) ENTÃO Atendimento Veterinário Imediato]] - concept - base/fonte/doencas/bvd.json

## Live Query (requires Dataview plugin)

```dataview
TABLE source_file, type FROM #community/Diarreia_Viral_Bovina_BVD
SORT file.name ASC
```

## Connections to other communities
- 7 edges to [[_COMMUNITY_Comum bandeiras, triagem e sinais compartilhados]]
- 1 edge to [[_COMMUNITY_Acidose Ruminal]]

## Top bridge nodes
- [[R-BVD-05 SE Fezes com espuma e grãos E Mudança abrupta de concentrado ENTÃO Diarreia Viral Bovina (BVD)]] - degree 3, connects to 2 communities
- [[R-BVD-02 SE Aborto recente E Falhas reprodutivas no lote E Febre ENTÃO Diarreia Viral Bovina (BVD)]] - degree 4, connects to 1 community
- [[R-BVD-01 SE Diarreia E Feridas na boca ENTÃO Diarreia Viral Bovina (BVD)]] - degree 3, connects to 1 community
- [[R-BVD-04 SE Diarreia E Febre ENTÃO Diarreia Viral Bovina (BVD)]] - degree 3, connects to 1 community
- [[R-URG-19 SE Diarreia Viral Bovina (BVD) ENTÃO Atendimento Veterinário Imediato]] - degree 2, connects to 1 community