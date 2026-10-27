---
type: community
cohesion: 0.25
members: 8
---

# Endometrite Clínica

**Cohesion:** 0.25 - loosely connected
**Members:** 8 nodes

## Members
- [[Conteúdo purulento ao exame vaginal]] - concept - base/fonte/doencas/endometrite.json
- [[Corrimento com pus após 21 dias do parto]] - concept - base/fonte/doencas/endometrite.json
- [[Endometrite Clínica]] - concept - base/fonte/doencas/endometrite.json
- [[R-END-01 SE Corrimento vaginal E Dias em lactação E Corrimento com pus após 21 dias do parto ENTÃO Endometrite Clínica]] - concept - base/fonte/doencas/endometrite.json
- [[R-END-02 SE Corrimento vaginal E Dias em lactação E Conteúdo purulento ao exame vaginal ENTÃO Endometrite Clínica]] - concept - base/fonte/doencas/endometrite.json
- [[R-END-03 SE Corrimento vaginal E Dias em lactação E Febre ENTÃO Endometrite Clínica]] - concept - base/fonte/doencas/endometrite.json
- [[R-END-04 SE Corrimento vaginal E Dias em lactação ENTÃO Endometrite Clínica]] - concept - base/fonte/doencas/endometrite.json
- [[R-URG-23 SE Endometrite Clínica ENTÃO Monitoramento Clínico Contínuo]] - concept - base/fonte/doencas/endometrite.json

## Live Query (requires Dataview plugin)

```dataview
TABLE source_file, type FROM #community/Endometrite_Clínica
SORT file.name ASC
```

## Connections to other communities
- 10 edges to [[_COMMUNITY_Comum bandeiras, triagem e sinais compartilhados]]
- 1 edge to [[_COMMUNITY_Metrite Puerperal]]

## Top bridge nodes
- [[Endometrite Clínica]] - degree 6, connects to 1 community
- [[R-END-01 SE Corrimento vaginal E Dias em lactação E Corrimento com pus após 21 dias do parto ENTÃO Endometrite Clínica]] - degree 4, connects to 1 community
- [[R-END-02 SE Corrimento vaginal E Dias em lactação E Conteúdo purulento ao exame vaginal ENTÃO Endometrite Clínica]] - degree 4, connects to 1 community
- [[R-END-03 SE Corrimento vaginal E Dias em lactação E Febre ENTÃO Endometrite Clínica]] - degree 4, connects to 1 community
- [[R-END-04 SE Corrimento vaginal E Dias em lactação ENTÃO Endometrite Clínica]] - degree 3, connects to 1 community