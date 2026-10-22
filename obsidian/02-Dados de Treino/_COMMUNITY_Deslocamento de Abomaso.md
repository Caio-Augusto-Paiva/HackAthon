---
type: community
cohesion: 0.25
members: 8
---

# Deslocamento de Abomaso

**Cohesion:** 0.25 - loosely connected
**Members:** 8 nodes

## Members
- [[Deslocamento de Abomaso]] - concept - base/fonte/doencas/deslocamento_abomaso.json
- [[Flanco esquerdo afundado]] - concept - base/fonte/doencas/deslocamento_abomaso.json
- [[Ping no flanco esquerdo]] - concept - base/fonte/doencas/deslocamento_abomaso.json
- [[R-DAB-01 SE Inicio lactacao E Apetite E Queda de produção de leite ENTÃO Deslocamento de Abomaso]] - concept - base/fonte/doencas/deslocamento_abomaso.json
- [[R-DAB-02 SE Inicio lactacao E Flanco esquerdo afundado ENTÃO Deslocamento de Abomaso]] - concept - base/fonte/doencas/deslocamento_abomaso.json
- [[R-DAB-03 SE Ping no flanco esquerdo ENTÃO Deslocamento de Abomaso]] - concept - base/fonte/doencas/deslocamento_abomaso.json
- [[R-DAB-04 SE Apetite ENTÃO Deslocamento de Abomaso]] - concept - base/fonte/doencas/deslocamento_abomaso.json
- [[R-URG-03 SE Deslocamento de Abomaso ENTÃO Atendimento Veterinário Imediato]] - concept - base/fonte/doencas/deslocamento_abomaso.json

## Live Query (requires Dataview plugin)

```dataview
TABLE source_file, type FROM #community/Deslocamento_de_Abomaso
SORT file.name ASC
```

## Connections to other communities
- 6 edges to [[_COMMUNITY_Comum bandeiras, triagem e sinais compartilhados]]

## Top bridge nodes
- [[R-DAB-01 SE Inicio lactacao E Apetite E Queda de produção de leite ENTÃO Deslocamento de Abomaso]] - degree 4, connects to 1 community
- [[R-DAB-02 SE Inicio lactacao E Flanco esquerdo afundado ENTÃO Deslocamento de Abomaso]] - degree 3, connects to 1 community
- [[R-URG-03 SE Deslocamento de Abomaso ENTÃO Atendimento Veterinário Imediato]] - degree 2, connects to 1 community
- [[R-DAB-04 SE Apetite ENTÃO Deslocamento de Abomaso]] - degree 2, connects to 1 community