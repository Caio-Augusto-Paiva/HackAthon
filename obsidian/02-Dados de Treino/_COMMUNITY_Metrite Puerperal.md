---
type: community
cohesion: 0.23
members: 12
---

# Metrite Puerperal

**Cohesion:** 0.23 - loosely connected
**Members:** 12 nodes

## Members
- [[Aumento uterino à palpação]] - concept - base/fonte/doencas/metrite.json
- [[Corrimento vaginal]] - concept - base/fonte/doencas/metrite.json
- [[Corrimento vaginal fétido]] - concept - base/fonte/doencas/metrite.json
- [[Histórico de retenção de placenta]] - concept - base/fonte/doencas/metrite.json
- [[Metrite Puerperal]] - concept - base/fonte/doencas/metrite.json
- [[Puerpério]] - concept - base/fonte/doencas/metrite.json
- [[R-DER-02 SE Dias em lactação ENTÃO Puerpério]] - concept - base/fonte/doencas/metrite.json
- [[R-MET-01 SE Puerpério E Corrimento vaginal fétido ENTÃO Metrite Puerperal]] - concept - base/fonte/doencas/metrite.json
- [[R-MET-02 SE Corrimento vaginal E Puerpério E Febre ENTÃO Metrite Puerperal]] - concept - base/fonte/doencas/metrite.json
- [[R-MET-03 SE Puerpério E Aumento uterino à palpação E Corrimento vaginal ENTÃO Metrite Puerperal]] - concept - base/fonte/doencas/metrite.json
- [[R-MET-04 SE Histórico de retenção de placenta E Puerpério ENTÃO Metrite Puerperal]] - concept - base/fonte/doencas/metrite.json
- [[R-URG-04 SE Metrite Puerperal ENTÃO Atendimento Veterinário Imediato]] - concept - base/fonte/doencas/metrite.json

## Live Query (requires Dataview plugin)

```dataview
TABLE source_file, type FROM #community/Metrite_Puerperal
SORT file.name ASC
```

## Connections to other communities
- 3 edges to [[_COMMUNITY_Comum bandeiras, triagem e sinais compartilhados]]

## Top bridge nodes
- [[R-MET-02 SE Corrimento vaginal E Puerpério E Febre ENTÃO Metrite Puerperal]] - degree 4, connects to 1 community
- [[R-DER-02 SE Dias em lactação ENTÃO Puerpério]] - degree 2, connects to 1 community
- [[R-URG-04 SE Metrite Puerperal ENTÃO Atendimento Veterinário Imediato]] - degree 2, connects to 1 community