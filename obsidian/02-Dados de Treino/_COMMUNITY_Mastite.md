---
type: community
cohesion: 0.17
members: 12
---

# Mastite

**Cohesion:** 0.17 - loosely connected
**Members:** 12 nodes

## Members
- [[Alteração visível do leite]] - concept - base/fonte/doencas/mastite.json
- [[CMT reagente]] - concept - base/fonte/doencas/mastite.json
- [[Evidência agrupada de alteração do leite]] - concept - base/fonte/doencas/mastite.json
- [[Grumos na caneca]] - concept - base/fonte/doencas/mastite.json
- [[Inflamação do úbere]] - concept - base/fonte/doencas/mastite.json
- [[Mastite]] - concept - base/fonte/doencas/mastite.json
- [[R-MAS-01 SE Alteração visível do leite ENTÃO Evidência agrupada de alteração do leite]] - concept - base/fonte/doencas/mastite.json
- [[R-MAS-02 SE Inflamação do úbere ENTÃO Mastite]] - concept - base/fonte/doencas/mastite.json
- [[R-MAS-03 SE Grumos na caneca ENTÃO Evidência agrupada de alteração do leite]] - concept - base/fonte/doencas/mastite.json
- [[R-MAS-04 SE CMT reagente ENTÃO Mastite]] - concept - base/fonte/doencas/mastite.json
- [[R-MAS-05 SE Evidência agrupada de alteração do leite ENTÃO Mastite]] - concept - base/fonte/doencas/mastite.json
- [[R-URG-05 SE Mastite ENTÃO Monitoramento Clínico Contínuo]] - concept - base/fonte/doencas/mastite.json

## Live Query (requires Dataview plugin)

```dataview
TABLE source_file, type FROM #community/Mastite
SORT file.name ASC
```

## Connections to other communities
- 2 edges to [[_COMMUNITY_Comum bandeiras, triagem e sinais compartilhados]]

## Top bridge nodes
- [[Inflamação do úbere]] - degree 2, connects to 1 community
- [[R-URG-05 SE Mastite ENTÃO Monitoramento Clínico Contínuo]] - degree 2, connects to 1 community