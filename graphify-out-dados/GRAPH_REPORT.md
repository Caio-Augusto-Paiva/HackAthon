# Graph Report - fonte  (2026-10-22)

## Corpus Check
- 9 files · ~0 words
- Verdict: corpus is large enough that graph structure adds value.

## Summary
- 112 nodes · 149 edges · 9 communities
- Extraction: 100% EXTRACTED · 0% INFERRED · 0% AMBIGUOUS
- Token cost: 0 input · 0 output

## Community Hubs (Navigation)
- Comum: bandeiras, triagem e sinais compartilhados
- Acidose Ruminal
- Cetose / Hipercetonemia
- Dermatite Digital Bovina
- Deslocamento de Abomaso
- Hipocalcemia Puerperal
- Mastite
- Metrite Puerperal
- Tristeza Parasitária Bovina

## God Nodes (most connected - your core abstractions)
1. `Atendimento Veterinário Imediato` - 10 edges
2. `Febre` - 9 edges
3. `Apetite` - 7 edges
4. `Cetose / Hipercetonemia` - 7 edges
5. `Hipocalcemia Puerperal` - 7 edges
6. `Hipotermia` - 6 edges
7. `Inicio lactacao` - 6 edges
8. `Acidose Ruminal` - 6 edges
9. `Dias em lactação` - 5 edges
10. `Temperatura retal` - 5 edges

## Surprising Connections (you probably didn't know these)
- `Apetite` --condicao_de--> `R-ACI-05: SE Apetite ENTÃO Acidose Ruminal`  [EXTRACTED]
  base/fonte/comum.json → base/fonte/doencas/acidose.json
- `Apetite` --condicao_de--> `R-CET-06: SE Apetite ENTÃO Cetose / Hipercetonemia`  [EXTRACTED]
  base/fonte/comum.json → base/fonte/doencas/cetose.json
- `Apetite` --condicao_de--> `R-DAB-04: SE Apetite ENTÃO Deslocamento de Abomaso`  [EXTRACTED]
  base/fonte/comum.json → base/fonte/doencas/deslocamento_abomaso.json
- `Dias em lactação` --condicao_de--> `R-DER-01: SE Dias em lactação ENTÃO Periparto imediato`  [EXTRACTED]
  base/fonte/comum.json → base/fonte/doencas/hipocalcemia.json
- `Dias em lactação` --condicao_de--> `R-DER-02: SE Dias em lactação ENTÃO Puerperio`  [EXTRACTED]
  base/fonte/comum.json → base/fonte/doencas/metrite.json

## Communities (9 total, 0 thin omitted)

### Community 0 - "Comum: bandeiras, triagem e sinais compartilhados"
Cohesion: 0.10
Nodes (22): Apatia, Apetite, Dias em lactação, Temperatura ao toque das extremidades, Queda de produção de leite, Temperatura retal, Febre, Inicio lactacao (+14 more)

### Community 1 - "Acidose Ruminal"
Cohesion: 0.20
Nodes (11): Diarreia, Fezes com espuma e grãos, Mudança abrupta de concentrado, pH ruminal, Acidose Ruminal, R-ACI-01: SE Diarreia E Apetite ENTÃO Acidose Ruminal, R-ACI-02: SE Mudança abrupta de concentrado E Diarreia ENTÃO Acidose Ruminal, R-ACI-03: SE Fezes com espuma e grãos ENTÃO Acidose Ruminal (+3 more)

### Community 2 - "Cetose / Hipercetonemia"
Cohesion: 0.17
Nodes (12): BHB sanguíneo, Corpos cetônicos na urina, Hálito adocicado, Recusa seletiva de concentrado, Cetose / Hipercetonemia, R-CET-01: SE Inicio lactacao E Apetite E Queda de produção de leite ENTÃO Cetose / Hipercetonemia, R-CET-02: SE Inicio lactacao E Hálito adocicado ENTÃO Cetose / Hipercetonemia, R-CET-03: SE Inicio lactacao E Recusa seletiva de concentrado ENTÃO Cetose / Hipercetonemia (+4 more)

### Community 3 - "Dermatite Digital Bovina"
Cohesion: 0.29
Nodes (8): Claudicação, Dor na região do talão, Lesão característica no talão, Dermatite Digital Bovina, R-DD-02: SE Claudicação E Dor na região do talão ENTÃO Dermatite Digital Bovina, R-DD-01: SE Claudicação ENTÃO Dermatite Digital Bovina, R-DD-03: SE Lesão característica no talão ENTÃO Dermatite Digital Bovina, R-URG-08: SE Dermatite Digital Bovina ENTÃO Monitoramento Clínico Contínuo

### Community 4 - "Deslocamento de Abomaso"
Cohesion: 0.25
Nodes (8): Flanco esquerdo afundado, Ping no flanco esquerdo, Deslocamento de Abomaso, R-DAB-01: SE Inicio lactacao E Apetite E Queda de produção de leite ENTÃO Deslocamento de Abomaso, R-DAB-02: SE Inicio lactacao E Flanco esquerdo afundado ENTÃO Deslocamento de Abomaso, R-DAB-03: SE Ping no flanco esquerdo ENTÃO Deslocamento de Abomaso, R-URG-03: SE Deslocamento de Abomaso ENTÃO Atendimento Veterinário Imediato, R-DAB-04: SE Apetite ENTÃO Deslocamento de Abomaso

### Community 5 - "Hipocalcemia Puerperal"
Cohesion: 0.14
Nodes (17): Cálcio sérico total, Decúbito, Desvio cervical em S, Hipotermia, Periparto imediato, Hipocalcemia Puerperal, R-DER-01: SE Dias em lactação ENTÃO Periparto imediato, R-DER-05: SE Temperatura retal ENTÃO Hipotermia (+9 more)

### Community 6 - "Mastite"
Cohesion: 0.17
Nodes (12): CMT reagente, Alteração visível do leite, Grumos na caneca, Inflamação do úbere, Evidência agrupada de alteração do leite, Mastite, R-MAS-01: SE Alteração visível do leite ENTÃO Evidência agrupada de alteração do leite, R-MAS-03: SE Grumos na caneca ENTÃO Evidência agrupada de alteração do leite (+4 more)

### Community 7 - "Metrite Puerperal"
Cohesion: 0.23
Nodes (12): Corrimento vaginal fétido, Corrimento vaginal, Histórico de retenção de placenta, Aumento uterino à palpação, Puerperio, Metrite Puerperal, R-DER-02: SE Dias em lactação ENTÃO Puerperio, R-MET-02: SE Corrimento vaginal E Puerperio E Febre ENTÃO Metrite Puerperal (+4 more)

### Community 8 - "Tristeza Parasitária Bovina"
Cohesion: 0.20
Nodes (10): Exposição recente a carrapatos, Hemoparasitas no esfregaço, Mucosas pálidas ou amareladas, Urina escura, Tristeza Parasitária Bovina, R-TPB-01: SE Febre E Urina escura ENTÃO Tristeza Parasitária Bovina, R-TPB-03: SE Exposição recente a carrapatos E Febre ENTÃO Tristeza Parasitária Bovina, R-TPB-02: SE Mucosas pálidas ou amareladas ENTÃO Tristeza Parasitária Bovina (+2 more)

## Knowledge Gaps
- **23 isolated node(s):** `BHB sanguíneo`, `Cálcio sérico total`, `Exposição recente a carrapatos`, `CMT reagente`, `Corrimento vaginal fétido` (+18 more)
  These have ≤1 connection - possible missing edges. (Counts symbols only; 23 node(s) total have ≤1 connection when file, concept and rationale nodes are included.)