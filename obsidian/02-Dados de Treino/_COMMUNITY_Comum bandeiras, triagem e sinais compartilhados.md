---
type: community
cohesion: 0.10
members: 22
---

# Comum: bandeiras, triagem e sinais compartilhados

**Cohesion:** 0.10 - loosely connected
**Members:** 22 nodes

## Members
- [[Apatia]] - concept - base/fonte/comum.json
- [[Apetite]] - concept - base/fonte/comum.json
- [[Atendimento Veterinário Imediato]] - concept - base/fonte/comum.json
- [[Dias em lactação]] - concept - base/fonte/comum.json
- [[Febre]] - concept - base/fonte/comum.json
- [[Inicio lactacao]] - concept - base/fonte/comum.json
- [[Monitoramento Clínico Contínuo]] - concept - base/fonte/comum.json
- [[Queda de produção de leite]] - concept - base/fonte/comum.json
- [[R-BV-01 SE Decúbito ENTÃO Atendimento Veterinário Imediato]] - concept - base/fonte/comum.json
- [[R-BV-02 SE Urina escura ENTÃO Atendimento Veterinário Imediato]] - concept - base/fonte/comum.json
- [[R-BV-03 SE Apetite E Apatia ENTÃO Atendimento Veterinário Imediato]] - concept - base/fonte/comum.json
- [[R-BV-04 SE Hipotermia E Apatia ENTÃO Atendimento Veterinário Imediato]] - concept - base/fonte/comum.json
- [[R-BV-05 SE Inflamação do úbere E Febre E Apatia ENTÃO Atendimento Veterinário Imediato]] - concept - base/fonte/comum.json
- [[R-BV-06 SE Temperatura retal ENTÃO Atendimento Veterinário Imediato]] - concept - base/fonte/comum.json
- [[R-DER-03 SE Dias em lactação ENTÃO Inicio lactacao]] - concept - base/fonte/comum.json
- [[R-DER-04 SE Temperatura retal ENTÃO Febre]] - concept - base/fonte/comum.json
- [[R-DER-07 SE Temperatura ao toque das extremidades ENTÃO Febre]] - concept - base/fonte/comum.json
- [[R-DER-08 SE Temperatura retal ENTÃO Febre]] - concept - base/fonte/comum.json
- [[R-DER-10 SE Temperatura ao toque das extremidades ENTÃO Febre]] - concept - base/fonte/comum.json
- [[Sem evidência de urgência pelos critérios da base]] - concept - base/fonte/comum.json
- [[Temperatura ao toque das extremidades]] - concept - base/fonte/comum.json
- [[Temperatura retal]] - concept - base/fonte/comum.json

## Live Query (requires Dataview plugin)

```dataview
TABLE source_file, type FROM #community/Comum_bandeiras_triagem_e_sinais_compartilhados
SORT file.name ASC
```

## Connections to other communities
- 10 edges to [[_COMMUNITY_Hipocalcemia Puerperal]]
- 7 edges to [[_COMMUNITY_Cetose  Hipercetonemia]]
- 6 edges to [[_COMMUNITY_Deslocamento de Abomaso]]
- 4 edges to [[_COMMUNITY_Tristeza Parasitária Bovina]]
- 3 edges to [[_COMMUNITY_Acidose Ruminal]]
- 3 edges to [[_COMMUNITY_Metrite Puerperal]]
- 2 edges to [[_COMMUNITY_Mastite]]
- 1 edge to [[_COMMUNITY_Dermatite Digital Bovina]]

## Top bridge nodes
- [[Atendimento Veterinário Imediato]] - degree 10, connects to 4 communities
- [[Monitoramento Clínico Contínuo]] - degree 4, connects to 4 communities
- [[Febre]] - degree 9, connects to 3 communities
- [[Apetite]] - degree 7, connects to 3 communities
- [[Inicio lactacao]] - degree 6, connects to 2 communities