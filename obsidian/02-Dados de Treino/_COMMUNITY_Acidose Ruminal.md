---
type: community
cohesion: 0.20
members: 11
---

# Acidose Ruminal

**Cohesion:** 0.20 - loosely connected
**Members:** 11 nodes

## Members
- [[Acidose Ruminal]] - concept - base/fonte/doencas/acidose.json
- [[Diarreia]] - concept - base/fonte/doencas/acidose.json
- [[Fezes com espuma e grãos]] - concept - base/fonte/doencas/acidose.json
- [[Mudança abrupta de concentrado]] - concept - base/fonte/doencas/acidose.json
- [[R-ACI-01 SE Diarreia E Apetite ENTÃO Acidose Ruminal]] - concept - base/fonte/doencas/acidose.json
- [[R-ACI-02 SE Mudança abrupta de concentrado E Diarreia ENTÃO Acidose Ruminal]] - concept - base/fonte/doencas/acidose.json
- [[R-ACI-03 SE Fezes com espuma e grãos ENTÃO Acidose Ruminal]] - concept - base/fonte/doencas/acidose.json
- [[R-ACI-04 SE pH ruminal ENTÃO Acidose Ruminal]] - concept - base/fonte/doencas/acidose.json
- [[R-ACI-05 SE Apetite ENTÃO Acidose Ruminal]] - concept - base/fonte/doencas/acidose.json
- [[R-URG-07 SE Acidose Ruminal ENTÃO Monitoramento Clínico Contínuo]] - concept - base/fonte/doencas/acidose.json
- [[pH ruminal]] - concept - base/fonte/doencas/acidose.json

## Live Query (requires Dataview plugin)

```dataview
TABLE source_file, type FROM #community/Acidose_Ruminal
SORT file.name ASC
```

## Connections to other communities
- 3 edges to [[_COMMUNITY_Comum bandeiras, triagem e sinais compartilhados]]

## Top bridge nodes
- [[R-ACI-01 SE Diarreia E Apetite ENTÃO Acidose Ruminal]] - degree 3, connects to 1 community
- [[R-URG-07 SE Acidose Ruminal ENTÃO Monitoramento Clínico Contínuo]] - degree 2, connects to 1 community
- [[R-ACI-05 SE Apetite ENTÃO Acidose Ruminal]] - degree 2, connects to 1 community