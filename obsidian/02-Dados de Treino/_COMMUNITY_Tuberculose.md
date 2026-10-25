---
type: community
cohesion: 0.20
members: 10
---

# Tuberculose

**Cohesion:** 0.20 - loosely connected
**Members:** 10 nodes

## Members
- [[Emagrecimento progressivo]] - concept - base/fonte/doencas/tuberculose.json
- [[R-TUB-01 SE Emagrecimento progressivo E Tosse E Queda de produção de leite E Apetite ENTÃO Tuberculose]] - concept - base/fonte/doencas/tuberculose.json
- [[R-TUB-02 SE Ínguas aumentadas E Queda de produção de leite ENTÃO Tuberculose]] - concept - base/fonte/doencas/tuberculose.json
- [[R-TUB-03 SE Tuberculinização reagente ENTÃO Tuberculose]] - concept - base/fonte/doencas/tuberculose.json
- [[R-TUB-04 SE Apetite E Queda de produção de leite ENTÃO Tuberculose]] - concept - base/fonte/doencas/tuberculose.json
- [[R-TUB-05 SE Febre ENTÃO Tuberculose]] - concept - base/fonte/doencas/tuberculose.json
- [[R-URG-20 SE Tuberculose ENTÃO Atendimento Veterinário Imediato]] - concept - base/fonte/doencas/tuberculose.json
- [[Tuberculinização reagente]] - concept - base/fonte/doencas/tuberculose.json
- [[Tuberculose]] - concept - base/fonte/doencas/tuberculose.json
- [[Ínguas aumentadas]] - concept - base/fonte/doencas/tuberculose.json

## Live Query (requires Dataview plugin)

```dataview
TABLE source_file, type FROM #community/Tuberculose
SORT file.name ASC
```

## Connections to other communities
- 8 edges to [[_COMMUNITY_Comum bandeiras, triagem e sinais compartilhados]]

## Top bridge nodes
- [[R-TUB-01 SE Emagrecimento progressivo E Tosse E Queda de produção de leite E Apetite ENTÃO Tuberculose]] - degree 5, connects to 1 community
- [[R-TUB-02 SE Ínguas aumentadas E Queda de produção de leite ENTÃO Tuberculose]] - degree 3, connects to 1 community
- [[R-TUB-04 SE Apetite E Queda de produção de leite ENTÃO Tuberculose]] - degree 3, connects to 1 community
- [[R-TUB-05 SE Febre ENTÃO Tuberculose]] - degree 2, connects to 1 community
- [[R-URG-20 SE Tuberculose ENTÃO Atendimento Veterinário Imediato]] - degree 2, connects to 1 community