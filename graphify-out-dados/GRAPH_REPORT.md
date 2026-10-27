# Graph Report - fonte  (2026-10-27)

## Corpus Check
- 26 files · ~0 words
- Verdict: corpus is large enough that graph structure adds value.

## Summary
- 285 nodes · 445 edges · 26 communities
- Extraction: 100% EXTRACTED · 0% INFERRED · 0% AMBIGUOUS
- Token cost: 0 input · 0 output

## Community Hubs (Navigation)
- Comum: bandeiras, triagem e sinais compartilhados
- Acidose Ruminal
- Brucelose
- Diarreia Viral Bovina (BVD)
- Cetose / Hipercetonemia
- Cisto Ovariano
- Dermatite Digital Bovina
- Deslocamento de Abomaso à Direita
- Deslocamento de Abomaso à Esquerda
- Endometrite Clínica
- Flegmão Interdigital (Podridão do Casco)
- Hipocalcemia Puerperal
- Hipomagnesemia
- Rinotraqueíte Infecciosa Bovina (IBR)
- Leptospirose
- Lipidose Hepática (Fígado Gorduroso)
- Mastite
- Metrite Puerperal
- Pneumonia
- Retenção de Placenta
- Reticulopericardite Traumática
- Timpanismo Espumoso
- Timpanismo Gasoso
- Tristeza Parasitária Bovina
- Tuberculose
- Úlcera de Sola / Doença da Linha Branca

## God Nodes (most connected - your core abstractions)
1. `Apetite` - 32 edges
2. `Febre` - 21 edges
3. `Atendimento Veterinário Imediato` - 20 edges
4. `Claudicação` - 15 edges
5. `Dias em lactação` - 14 edges
6. `Início da lactação` - 11 edges
7. `Monitoramento Clínico Contínuo` - 11 edges
8. `Corrimento vaginal` - 10 edges
9. `Queda de produção de leite` - 10 edges
10. `Puerpério` - 9 edges

## Surprising Connections (you probably didn't know these)
- `Apetite` --condicao_de--> `R-ACI-05: SE Apetite ENTÃO Acidose Ruminal`  [EXTRACTED]
  base/fonte/comum.json → base/fonte/doencas/acidose.json
- `Apetite` --condicao_de--> `R-CET-06: SE Apetite ENTÃO Cetose / Hipercetonemia`  [EXTRACTED]
  base/fonte/comum.json → base/fonte/doencas/cetose.json
- `Apetite` --condicao_de--> `R-DAE-04: SE Apetite ENTÃO Deslocamento de Abomaso à Esquerda`  [EXTRACTED]
  base/fonte/comum.json → base/fonte/doencas/deslocamento_abomaso_esquerda.json
- `Apetite` --condicao_de--> `R-LIP-04: SE Apetite ENTÃO Lipidose Hepática (Fígado Gorduroso)`  [EXTRACTED]
  base/fonte/comum.json → base/fonte/doencas/lipidose_hepatica.json
- `Claudicação` --condicao_de--> `R-DD-01: SE Claudicação ENTÃO Dermatite Digital Bovina`  [EXTRACTED]
  base/fonte/comum.json → base/fonte/doencas/dermatite_digital.json

## Communities (26 total, 0 thin omitted)

### Community 0 - "Comum: bandeiras, triagem e sinais compartilhados"
Cohesion: 0.03
Nodes (45): Apatia, Apetite, Claudicação, Corrimento vaginal, Decúbito, Diarreia, Dias em lactação, Hemoparasitas no esfregaço (+37 more)

### Community 1 - "Acidose Ruminal"
Cohesion: 0.22
Nodes (9): Mudança abrupta de concentrado, pH ruminal, Acidose Ruminal, R-ACI-01: SE Diarreia E Apetite ENTÃO Acidose Ruminal, R-ACI-02: SE Mudança abrupta de concentrado E Diarreia ENTÃO Acidose Ruminal, R-ACI-03: SE Fezes com espuma e grãos ENTÃO Acidose Ruminal, R-ACI-04: SE pH ruminal ENTÃO Acidose Ruminal, R-URG-07: SE Acidose Ruminal ENTÃO Monitoramento Clínico Contínuo (+1 more)

### Community 2 - "Brucelose"
Cohesion: 0.20
Nodes (10): Inchaço nos joelhos, Vacinada contra brucelose, Sorologia para brucelose reagente, Brucelose, R-BRU-01: SE Aborto recente E Histórico de retenção de placenta ENTÃO Brucelose, R-BRU-02: SE Inchaço nos joelhos ENTÃO Brucelose, R-BRU-03: SE Sorologia para brucelose reagente ENTÃO Brucelose, R-BRU-04: SE Corrimento vaginal ENTÃO Brucelose (+2 more)

### Community 3 - "Diarreia Viral Bovina (BVD)"
Cohesion: 0.20
Nodes (10): Feridas na boca, Falhas reprodutivas no lote, BVDV detectado, Diarreia Viral Bovina (BVD), R-BVD-01: SE Diarreia E Feridas na boca ENTÃO Diarreia Viral Bovina (BVD), R-BVD-02: SE Aborto recente E Falhas reprodutivas no lote E Febre ENTÃO Diarreia Viral Bovina (BVD), R-BVD-03: SE BVDV detectado ENTÃO Diarreia Viral Bovina (BVD), R-BVD-04: SE Diarreia E Febre ENTÃO Diarreia Viral Bovina (BVD) (+2 more)

### Community 4 - "Cetose / Hipercetonemia"
Cohesion: 0.17
Nodes (12): BHB sanguíneo, Corpos cetônicos na urina, Hálito adocicado, Recusa seletiva de concentrado, Cetose / Hipercetonemia, R-CET-01: SE Início da lactação E Apetite E Queda de produção de leite ENTÃO Cetose / Hipercetonemia, R-CET-02: SE Início da lactação E Hálito adocicado ENTÃO Cetose / Hipercetonemia, R-CET-03: SE Início da lactação E Recusa seletiva de concentrado ENTÃO Cetose / Hipercetonemia (+4 more)

### Community 5 - "Cisto Ovariano"
Cohesion: 0.29
Nodes (8): Cio irregular ou constante, Estrutura ovariana maior que 25 mm, Cisto Ovariano, R-CIS-01: SE Dias em lactação E Apetite E Cio irregular ou constante ENTÃO Cisto Ovariano, R-CIS-02: SE Dias em lactação E Estrutura ovariana maior que 25 mm ENTÃO Cisto Ovariano, R-CIS-03: SE Dias em lactação E Corrimento vaginal ENTÃO Cisto Ovariano, R-CIS-04: SE Dias em lactação E Apetite E Cio irregular ou constante ENTÃO Cisto Ovariano, R-URG-24: SE Cisto Ovariano ENTÃO Monitoramento Clínico Contínuo

### Community 6 - "Dermatite Digital Bovina"
Cohesion: 0.29
Nodes (7): Dor na região do talão, Dermatite Digital Bovina, R-DD-02: SE Claudicação E Dor na região do talão ENTÃO Dermatite Digital Bovina, R-DD-01: SE Claudicação ENTÃO Dermatite Digital Bovina, R-DD-03: SE Lesão característica no talão ENTÃO Dermatite Digital Bovina, R-DD-04: SE Claudicação E Inchaço entre as unhas com mau cheiro ENTÃO Dermatite Digital Bovina, R-URG-08: SE Dermatite Digital Bovina ENTÃO Monitoramento Clínico Contínuo

### Community 7 - "Deslocamento de Abomaso à Direita"
Cohesion: 0.20
Nodes (10): Barriga estufada do lado direito, Desidratação, Deslocamento de Abomaso à Direita, R-DAD-01: SE Início da lactação E Apetite E Pouco esterco ENTÃO Deslocamento de Abomaso à Direita, R-DAD-02: SE Barriga estufada do lado direito E Apetite ENTÃO Deslocamento de Abomaso à Direita, R-DAD-03: SE Ping no flanco direito ENTÃO Deslocamento de Abomaso à Direita, R-DAD-04: SE Desidratação E Apetite ENTÃO Deslocamento de Abomaso à Direita, R-DAD-05: SE Apetite E Apatia ENTÃO Deslocamento de Abomaso à Direita (+2 more)

### Community 8 - "Deslocamento de Abomaso à Esquerda"
Cohesion: 0.22
Nodes (9): Flanco esquerdo afundado, Deslocamento de Abomaso à Esquerda, R-URG-03: SE Deslocamento de Abomaso à Esquerda ENTÃO Atendimento Veterinário Imediato, R-DAE-01: SE Início da lactação E Apetite E Queda de produção de leite ENTÃO Deslocamento de Abomaso à Esquerda, R-DAE-02: SE Início da lactação E Flanco esquerdo afundado ENTÃO Deslocamento de Abomaso à Esquerda, R-DAE-03: SE Ping no flanco esquerdo ENTÃO Deslocamento de Abomaso à Esquerda, R-DAE-04: SE Apetite ENTÃO Deslocamento de Abomaso à Esquerda, R-DAE-05: SE Início da lactação E Pouco esterco ENTÃO Deslocamento de Abomaso à Esquerda (+1 more)

### Community 9 - "Endometrite Clínica"
Cohesion: 0.25
Nodes (8): Corrimento com pus após 21 dias do parto, Conteúdo purulento ao exame vaginal, Endometrite Clínica, R-END-01: SE Corrimento vaginal E Dias em lactação E Corrimento com pus após 21 dias do parto ENTÃO Endometrite Clínica, R-END-02: SE Corrimento vaginal E Dias em lactação E Conteúdo purulento ao exame vaginal ENTÃO Endometrite Clínica, R-END-03: SE Corrimento vaginal E Dias em lactação E Febre ENTÃO Endometrite Clínica, R-END-04: SE Corrimento vaginal E Dias em lactação ENTÃO Endometrite Clínica, R-URG-23: SE Endometrite Clínica ENTÃO Monitoramento Clínico Contínuo

### Community 10 - "Flegmão Interdigital (Podridão do Casco)"
Cohesion: 0.22
Nodes (9): Fissura interdigital necrótica, Flegmão Interdigital (Podridão do Casco), R-FLE-01: SE Claudicação E Inchaço entre as unhas com mau cheiro ENTÃO Flegmão Interdigital (Podridão do Casco), R-FLE-02: SE Claudicação E Fissura interdigital necrótica ENTÃO Flegmão Interdigital (Podridão do Casco), R-FLE-03: SE Claudicação E Febre ENTÃO Flegmão Interdigital (Podridão do Casco), R-FLE-04: SE Claudicação E Manqueira de pata traseira sem inchaço ENTÃO Flegmão Interdigital (Podridão do Casco), R-FLE-05: SE Claudicação ENTÃO Flegmão Interdigital (Podridão do Casco), R-FLE-06: SE Claudicação E Lesão característica no talão ENTÃO Flegmão Interdigital (Podridão do Casco) (+1 more)

### Community 11 - "Hipocalcemia Puerperal"
Cohesion: 0.14
Nodes (16): Cálcio sérico total, Desvio cervical em S, Hipotermia, Periparto imediato, Hipocalcemia Puerperal, R-DER-01: SE Dias em lactação ENTÃO Periparto imediato, R-DER-05: SE Temperatura retal ENTÃO Hipotermia, R-DER-06: SE Temperatura ao toque das extremidades ENTÃO Hipotermia (+8 more)

### Community 12 - "Hipomagnesemia"
Cohesion: 0.20
Nodes (11): Tremores musculares, Agitação ou reação exagerada, Pasto novo e adubado, Magnésio sérico, Hipomagnesemia, R-HMG-01: SE Tremores musculares E Agitação ou reação exagerada E Apetite ENTÃO Hipomagnesemia, R-HMG-02: SE Pasto novo e adubado E Apetite ENTÃO Hipomagnesemia, R-HMG-03: SE Magnésio sérico ENTÃO Hipomagnesemia (+3 more)

### Community 13 - "Rinotraqueíte Infecciosa Bovina (IBR)"
Cohesion: 0.20
Nodes (10): Focinho muito vermelho, Olhos lacrimejando, BoHV-1 detectado, Rinotraqueíte Infecciosa Bovina (IBR), R-IBR-01: SE Focinho muito vermelho E Secreção nasal E Queda de produção de leite ENTÃO Rinotraqueíte Infecciosa Bovina (IBR), R-IBR-02: SE Olhos lacrimejando E Febre ENTÃO Rinotraqueíte Infecciosa Bovina (IBR), R-IBR-03: SE BoHV-1 detectado ENTÃO Rinotraqueíte Infecciosa Bovina (IBR), R-IBR-04: SE Febre E Queda de produção de leite ENTÃO Rinotraqueíte Infecciosa Bovina (IBR) (+2 more)

### Community 14 - "Leptospirose"
Cohesion: 0.22
Nodes (9): Leite rosado ou com sangue, Sorologia para leptospirose reagente, Leptospirose, R-LEP-01: SE Aborto recente E Febre ENTÃO Leptospirose, R-LEP-02: SE Leite rosado ou com sangue E Queda de produção de leite E Alteração visível do leite ENTÃO Leptospirose, R-LEP-03: SE Sorologia para leptospirose reagente ENTÃO Leptospirose, R-LEP-04: SE Urina escura E Febre ENTÃO Leptospirose, R-LEP-05: SE Hemoparasitas no esfregaço ENTÃO Leptospirose (+1 more)

### Community 15 - "Lipidose Hepática (Fígado Gorduroso)"
Cohesion: 0.29
Nodes (8): Vaca gorda no parto, Enzimas hepáticas elevadas, Lipidose Hepática (Fígado Gorduroso), R-LIP-01: SE Início da lactação E Apetite E Vaca gorda no parto ENTÃO Lipidose Hepática (Fígado Gorduroso), R-LIP-02: SE Início da lactação E Apetite E Enzimas hepáticas elevadas ENTÃO Lipidose Hepática (Fígado Gorduroso), R-LIP-03: SE Início da lactação E Apetite E Vaca gorda no parto ENTÃO Lipidose Hepática (Fígado Gorduroso), R-LIP-04: SE Apetite ENTÃO Lipidose Hepática (Fígado Gorduroso), R-URG-25: SE Lipidose Hepática (Fígado Gorduroso) ENTÃO Atendimento Veterinário Imediato

### Community 16 - "Mastite"
Cohesion: 0.17
Nodes (12): CMT reagente, Alteração visível do leite, Grumos na caneca, Inflamação do úbere, Evidência agrupada de alteração do leite, Mastite, R-MAS-01: SE Alteração visível do leite ENTÃO Evidência agrupada de alteração do leite, R-MAS-03: SE Grumos na caneca ENTÃO Evidência agrupada de alteração do leite (+4 more)

### Community 17 - "Metrite Puerperal"
Cohesion: 0.25
Nodes (8): Corrimento vaginal fétido, Aumento uterino à palpação, Metrite Puerperal, R-MET-02: SE Corrimento vaginal E Puerpério E Febre ENTÃO Metrite Puerperal, R-MET-03: SE Puerpério E Aumento uterino à palpação E Corrimento vaginal ENTÃO Metrite Puerperal, R-MET-01: SE Puerpério E Corrimento vaginal fétido E Corrimento vaginal ENTÃO Metrite Puerperal, R-MET-04: SE Histórico de retenção de placenta E Puerpério ENTÃO Metrite Puerperal, R-URG-04: SE Metrite Puerperal ENTÃO Atendimento Veterinário Imediato

### Community 18 - "Pneumonia"
Cohesion: 0.22
Nodes (9): Respiração com esforço, Pneumonia, R-PNE-01: SE Tosse E Apetite ENTÃO Pneumonia, R-PNE-02: SE Respiração com esforço E Apetite ENTÃO Pneumonia, R-PNE-03: SE Crepitações à auscultação pulmonar ENTÃO Pneumonia, R-PNE-04: SE Secreção nasal E Apetite ENTÃO Pneumonia, R-PNE-05: SE Febre E Apatia ENTÃO Pneumonia, R-PNE-06: SE Barriga estufada do lado esquerdo E Apetite ENTÃO Pneumonia (+1 more)

### Community 19 - "Retenção de Placenta"
Cohesion: 0.18
Nodes (11): Restos de placenta na vulva, Placenta não saiu em 24 horas, Membranas retidas ao exame, Retenção de Placenta, R-RPL-01: SE Puerpério E Restos de placenta na vulva ENTÃO Retenção de Placenta, R-RPL-02: SE Puerpério E Placenta não saiu em 24 horas ENTÃO Retenção de Placenta, R-RPL-03: SE Membranas retidas ao exame ENTÃO Retenção de Placenta, R-RPL-04: SE Histórico de retenção de placenta E Puerpério ENTÃO Retenção de Placenta (+3 more)

### Community 20 - "Reticulopericardite Traumática"
Cohesion: 0.18
Nodes (11): Costas arqueadas, Gemido, Prova de dor reticular, Edema de barbela ou peito, Reticulopericardite Traumática, R-RPT-01: SE Costas arqueadas E Gemido E Apetite ENTÃO Reticulopericardite Traumática, R-RPT-03: SE Prova de dor reticular ENTÃO Reticulopericardite Traumática, R-RPT-04: SE Edema de barbela ou peito E Febre ENTÃO Reticulopericardite Traumática (+3 more)

### Community 21 - "Timpanismo Espumoso"
Cohesion: 0.22
Nodes (9): Pasto de leguminosa recente, Outros animais estufados, Timpanismo Espumoso, R-TES-01: SE Barriga estufada do lado esquerdo E Pasto de leguminosa recente E Apetite ENTÃO Timpanismo Espumoso, R-TES-02: SE Outros animais estufados E Apetite ENTÃO Timpanismo Espumoso, R-TES-03: SE Conteúdo espumoso na sonda ENTÃO Timpanismo Espumoso, R-TES-04: SE Apetite E Queda de produção de leite ENTÃO Timpanismo Espumoso, R-TES-05: SE Gás livre na sonda ENTÃO Timpanismo Espumoso (+1 more)

### Community 22 - "Timpanismo Gasoso"
Cohesion: 0.29
Nodes (7): Engasgo ou dificuldade de engolir, Timpanismo Gasoso, R-TGA-01: SE Barriga estufada do lado esquerdo E Engasgo ou dificuldade de engolir E Apetite ENTÃO Timpanismo Gasoso, R-TGA-03: SE Gás livre na sonda ENTÃO Timpanismo Gasoso, R-TGA-04: SE Apetite E Apatia ENTÃO Timpanismo Gasoso, R-TGA-05: SE Conteúdo espumoso na sonda ENTÃO Timpanismo Gasoso, R-URG-11: SE Timpanismo Gasoso ENTÃO Atendimento Veterinário Imediato

### Community 23 - "Tristeza Parasitária Bovina"
Cohesion: 0.25
Nodes (8): Exposição recente a carrapatos, Mucosas pálidas ou amareladas, Tristeza Parasitária Bovina, R-TPB-01: SE Febre E Urina escura ENTÃO Tristeza Parasitária Bovina, R-TPB-03: SE Exposição recente a carrapatos E Febre ENTÃO Tristeza Parasitária Bovina, R-TPB-02: SE Mucosas pálidas ou amareladas ENTÃO Tristeza Parasitária Bovina, R-TPB-04: SE Hemoparasitas no esfregaço ENTÃO Tristeza Parasitária Bovina, R-URG-02: SE Tristeza Parasitária Bovina ENTÃO Atendimento Veterinário Imediato

### Community 24 - "Tuberculose"
Cohesion: 0.20
Nodes (10): Emagrecimento progressivo, Ínguas aumentadas, Tuberculinização reagente, Tuberculose, R-TUB-01: SE Emagrecimento progressivo E Tosse E Queda de produção de leite E Apetite ENTÃO Tuberculose, R-TUB-02: SE Ínguas aumentadas E Queda de produção de leite ENTÃO Tuberculose, R-TUB-03: SE Tuberculinização reagente ENTÃO Tuberculose, R-TUB-04: SE Apetite E Queda de produção de leite ENTÃO Tuberculose (+2 more)

### Community 25 - "Úlcera de Sola / Doença da Linha Branca"
Cohesion: 0.22
Nodes (9): Dor à pinça na sola ou na linha branca, Úlcera de Sola / Doença da Linha Branca, R-ULC-01: SE Claudicação E Manqueira de pata traseira sem inchaço ENTÃO Úlcera de Sola / Doença da Linha Branca, R-ULC-02: SE Claudicação E Dor à pinça na sola ou na linha branca ENTÃO Úlcera de Sola / Doença da Linha Branca, R-ULC-03: SE Claudicação E Lesão característica no talão ENTÃO Úlcera de Sola / Doença da Linha Branca, R-ULC-04: SE Claudicação E Inchaço entre as unhas com mau cheiro ENTÃO Úlcera de Sola / Doença da Linha Branca, R-ULC-05: SE Claudicação ENTÃO Úlcera de Sola / Doença da Linha Branca, R-ULC-06: SE Claudicação E Dor na região do talão ENTÃO Úlcera de Sola / Doença da Linha Branca (+1 more)

## Knowledge Gaps
- **51 isolated node(s):** `BHB sanguíneo`, `Cálcio sérico total`, `Exposição recente a carrapatos`, `CMT reagente`, `Corrimento vaginal fétido` (+46 more)
  These have ≤1 connection - possible missing edges. (Counts symbols only; 51 node(s) total have ≤1 connection when file, concept and rationale nodes are included.)