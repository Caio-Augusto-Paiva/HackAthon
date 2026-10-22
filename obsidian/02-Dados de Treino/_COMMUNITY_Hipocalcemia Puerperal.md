---
type: community
cohesion: 0.14
members: 17
---

# Hipocalcemia Puerperal

**Cohesion:** 0.14 - loosely connected
**Members:** 17 nodes

## Members
- [[Cálcio sérico total]] - concept - base/fonte/doencas/hipocalcemia.json
- [[Decúbito]] - concept - base/fonte/doencas/hipocalcemia.json
- [[Desvio cervical em S]] - concept - base/fonte/doencas/hipocalcemia.json
- [[Hipocalcemia Puerperal]] - concept - base/fonte/doencas/hipocalcemia.json
- [[Hipotermia]] - concept - base/fonte/doencas/hipocalcemia.json
- [[Periparto imediato]] - concept - base/fonte/doencas/hipocalcemia.json
- [[R-DER-01 SE Dias em lactação ENTÃO Periparto imediato]] - concept - base/fonte/doencas/hipocalcemia.json
- [[R-DER-05 SE Temperatura retal ENTÃO Hipotermia]] - concept - base/fonte/doencas/hipocalcemia.json
- [[R-DER-06 SE Temperatura ao toque das extremidades ENTÃO Hipotermia]] - concept - base/fonte/doencas/hipocalcemia.json
- [[R-DER-09 SE Temperatura retal ENTÃO Hipotermia]] - concept - base/fonte/doencas/hipocalcemia.json
- [[R-HIP-01 SE Decúbito E Periparto imediato ENTÃO Hipocalcemia Puerperal]] - concept - base/fonte/doencas/hipocalcemia.json
- [[R-HIP-02 SE Periparto imediato E Desvio cervical em S E Hipotermia ENTÃO Hipocalcemia Puerperal]] - concept - base/fonte/doencas/hipocalcemia.json
- [[R-HIP-03 SE Cálcio sérico total ENTÃO Hipocalcemia Puerperal]] - concept - base/fonte/doencas/hipocalcemia.json
- [[R-HIP-04 SE Febre ENTÃO Hipocalcemia Puerperal]] - concept - base/fonte/doencas/hipocalcemia.json
- [[R-HIP-05 SE Decúbito E Dias em lactação ENTÃO Hipocalcemia Puerperal]] - concept - base/fonte/doencas/hipocalcemia.json
- [[R-HIP-06 SE Hipotermia E Dias em lactação ENTÃO Hipocalcemia Puerperal]] - concept - base/fonte/doencas/hipocalcemia.json
- [[R-URG-01 SE Hipocalcemia Puerperal ENTÃO Atendimento Veterinário Imediato]] - concept - base/fonte/doencas/hipocalcemia.json

## Live Query (requires Dataview plugin)

```dataview
TABLE source_file, type FROM #community/Hipocalcemia_Puerperal
SORT file.name ASC
```

## Connections to other communities
- 10 edges to [[_COMMUNITY_Comum bandeiras, triagem e sinais compartilhados]]

## Top bridge nodes
- [[Hipotermia]] - degree 6, connects to 1 community
- [[Decúbito]] - degree 3, connects to 1 community
- [[R-HIP-05 SE Decúbito E Dias em lactação ENTÃO Hipocalcemia Puerperal]] - degree 3, connects to 1 community
- [[R-HIP-06 SE Hipotermia E Dias em lactação ENTÃO Hipocalcemia Puerperal]] - degree 3, connects to 1 community
- [[R-DER-01 SE Dias em lactação ENTÃO Periparto imediato]] - degree 2, connects to 1 community