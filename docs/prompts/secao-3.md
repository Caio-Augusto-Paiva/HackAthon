# Prompt de revisão — Seção 3: Conhecimento do domínio

> **Agente:** Gemini Pro (app web) com Deep Research e busca no Google (alternativa: Antigravity da pessoa A com a skill `pdf` de anthropics/skills para ler material da Embrapa). **Por quê:** conferir fontes clínicas em português e inglês. **Melhor ainda:** um técnico da RERUM ou alguém de veterinária ([A] slide 13). Ver `docs/agentes-e-skills.md`.

> Status da seção: **aprovada (v2)** (20/10/2026). Após v2: R-MET-06 e R-CET-08 testam `dias_em_lactacao`; 8 perguntas exclusivas do veterinário. v2: laminite trocada por dermatite digital; cheiro de acetona removido (sem fonte); camadas estritas; `cf_minimo`; gravidade; derivado `max` para sinais redundantes. Lista completa de fontes em `docs/fontes/fontes.md`. Cole tudo abaixo da linha numa IA revisora — de preferência peça também revisão a alguém com formação em veterinária ou zootecnia.

---

Você vai atuar como **revisor técnico independente** do conhecimento de domínio de um sistema especialista de triagem (trabalho acadêmico, Hackathon UFJF 2026, tema "Anamnese de bovinos leiteiros em lactação"). Esta seção lista sinais, histórico, sinais derivados e as regras de produção com fatores de certeza (CF, modelo MYCIN) para 8 doenças e 3 urgências.

Não presuma que a seção está certa nem errada. **Todo conteúdo veterinário aqui é suposição a validar.** Verifique cada afirmação clínica contra as fontes citadas (F1–F12) e diga quando a fonte não sustenta a regra.

## Restrições obrigatórias do desafio

1. Nenhuma LLM no caminho da decisão em tempo de execução.
2. Decisão determinística e auditável.
3. Open source; tudo roda em localhost.
4. Dados fictícios apenas.

## Decisões já tomadas (não reabra)

- D1. 8 doenças: mastite clínica, metrite puerperal, tristeza parasitária bovina (TPB), cetose, hipocalcemia, deslocamento de abomaso, acidose ruminal, dermatite digital. Nenhum par mutuamente exclusivo. Urgências: `chamar_agora`, `observar`, `sem_problema`.
- D2. Dois modos (produtor e veterinário), mesma base e mesmo motor.
- D3. Fatos `(variável, valor, CF)`; premissa = mínimo dos CF; `cf_regra` ∈ [−0,99; +0,99]; combinação MYCIN; regra dispara com premissa > 0,2.
- D4. **Três camadas estritas:** regras de `derivado` (entradas: perguntas e ficha) → regras de `doenca` (entradas: perguntas, ficha, derivados) → regras de `urgencia` e `bandeira_vermelha` (entradas: qualquer camada abaixo). Nenhuma regra lê símbolo da própria camada ou de camada acima.
- D5. Triagem obrigatória de 6 telas. Validador exige: cada doença tem ao menos uma regra só com símbolos da triagem (ou derivados cujas entradas são **todas** da triagem); ao menos uma regra só com perguntas do modo produtor; toda bandeira vermelha tem condição sobre símbolo da triagem.
- D6. Bandeira vermelha leva direto a `chamar_agora`. Parecer em porcentagem `max(0, CF) × 100`.

## Como revisar

Para cada problema: (1) veredito (erro clínico / CF implausível / lacuna / ressalva); (2) id da regra ou símbolo; (3) a fonte que contradiz ou a ausência de fonte; (4) correção mínima (nova condição, novo CF, ou remoção). Ao final: sinais importantes que faltam, regras que geram falso positivo óbvio, e resumo de 3 linhas.

---

## SEÇÃO 3 — Conhecimento do domínio (v2)

### 3.1 Fontes

Tabela completa, com status de conferência e fatos extraídos, em `docs/fontes/fontes.md`. Resumo: F1 mastite, F2 metrite, F3–F5 TPB, F6 cetose (**lida**), F7 hipocalcemia, F8 deslocamento de abomaso, F9–F10 acidose, F11–F12 dermatite digital (F12 **lida**). Todas do MSD Veterinary Manual, exceto F5 (Embrapa).

### 3.2 Histórico (ficha do animal e importação de prontuário)

| símbolo | tipo | uso |
|---|---|---|
| `dias_em_lactacao` | numérico (dias desde o parto) | triagem; gera os sinais de período |
| `numero_lactacoes` | numérico | registrado; sem regra no PoC (sem fonte) |
| `raca_grupo` | categórico: europeia / zebuína / cruzada | TPB (F5) |
| `retencao_placenta` | booleano (último parto) | metrite (suposição) |
| `parto_distocico` | booleano (último parto) | metrite (suposição) |
| `historico_mastite_12m` | booleano | mastite (suposição) |
| `mudanca_dieta_recente` | booleano (aumento brusco de concentrado nos últimos 3 dias) | acidose (F9); também perguntável |
| `casos_podais_no_rebanho` | booleano | dermatite digital (F12, doença de rebanho); também perguntável |

### 3.3 Sinais derivados (camada 1)

Combinação padrão MYCIN. `combinacao: max` é usada quando as entradas são **redundantes** (mesmo fenômeno, fontes correlacionadas), para não inflar a soma.
```
R-DER-01  SE dias_em_lactacao ≤ 3               ENTÃO periparto_imediato  +0,99 | F7 (48 h + margem)
R-DER-02  SE dias_em_lactacao ≤ 21              ENTÃO puerperio           +0,99 | F2
R-DER-03  SE dias_em_lactacao ≤ 42              ENTÃO inicio_lactacao     +0,99 | F6 (6 semanas)
R-DER-04  SE temperatura_retal ≥ 39,5           ENTÃO febre               +0,95 | F2      [vet]
R-DER-05  SE temperatura_retal < 38,0           ENTÃO hipotermia          +0,90 | suposição [vet]
R-DER-06  SE 38,0 ≤ temperatura_retal < 39,5    ENTÃO febre               −0,90 | suposição [vet]
R-DER-07  SE extremidades = quente              ENTÃO febre               +0,50 | suposição [produtor]
R-DER-08  SE extremidades = fria                ENTÃO hipotermia          +0,60 | F7       [produtor]
R-DER-09  SE extremidades = normal              ENTÃO febre               −0,40 | suposição [produtor]
R-DER-10  SE retencao_placenta                  ENTÃO parto_complicado    +0,90 | suposição  (combinacao: max)
R-DER-11  SE parto_distocico                    ENTÃO parto_complicado    +0,90 | suposição  (combinacao: max)
```
`febre` e `hipotermia` usam MYCIN (termômetro e extremidades são evidências independentes e podem se contradizer). `parto_complicado` usa `max` (distocia e retenção de placenta são correlacionadas).
Derivados de triagem (contam para a cobertura): `periparto_imediato`, `puerperio`, `inicio_lactacao`, `febre`, `hipotermia` — todas as entradas vêm de `meta.triagem`. `parto_complicado` **não** conta.
Os derivados de período (`periparto_imediato`, `puerperio`, `inicio_lactacao`) só recebem evidência positiva: fora da janela ficam em CF 0, não −1. Por isso as regras de exclusão por período (R-MET-06, R-CET-08, R-HIP-06) testam `dias_em_lactacao` direto, nunca o derivado negado.

### 3.4 Perguntas da fase dinâmica

| símbolo | produtor | veterinário | serve a |
|---|---|---|---|
| `teste_caneca_positivo` | sim ("grumos no teste da caneca de fundo escuro?") | sim | mastite (F1) |
| `cmt_positivo` | — | sim | mastite (F1) |
| `um_quarto_afetado` | sim | sim | mastite (suposição) |
| `corrimento_fetido` | sim ("cheiro forte, aquoso, marrom-avermelhado?") | sim | metrite (F2) |
| `utero_aumentado_palpacao` | — | sim | metrite (F2) |
| `carrapatos_presentes` | sim | sim | TPB (F3, F5) |
| `mucosas_palidas_amareladas` | sim ("olho/gengiva pálidos ou amarelados?") | sim | TPB (F3, F5) |
| `esfregaco_hemoparasita` | — | sim | TPB (F3, F4) |
| `abdomen_vazio` | sim ("barriga murcha, vazia?") | sim | cetose (F6) |
| `sinais_nervosos` | sim ("lambe ou mastiga objetos, anda sem coordenação?") | sim | cetose (F6) |
| `perda_condicao_corporal` | sim | sim | cetose (F6) |
| `bhb_sanguineo` | — | sim (mmol/L) | cetose (F6) |
| `fraqueza_tremores` | sim | sim | hipocalcemia (suposição) |
| `calcio_sanguineo` | — | sim (mmol/L) | hipocalcemia (F7) |
| `ping_flanco_esquerdo` | — | sim | deslocamento de abomaso (F8) |
| `costelas_esquerdas_saltadas` | sim | sim | deslocamento de abomaso (F8) |
| `mudanca_dieta_recente` | sim (se a ficha não tiver) | sim | acidose (F9) |
| `graos_nas_fezes` | sim | sim | acidose (F9) |
| `ph_ruminal` | — | sim | acidose (F9) |
| `ferida_vermelha_entre_unhas` | sim ("ferida vermelha e dolorida entre as unhas ou atrás do casco?") | sim | dermatite digital (F12) |
| `lesao_dd_ativa` | — | sim (ulcerada, dolorosa, > 2 cm) | dermatite digital (F12) |
| `inchaco_simetrico_acima_casco` | sim | sim | dermatite digital — exclusão (F12, sugere foot rot) |
| `casos_podais_no_rebanho` | sim (se a ficha não tiver) | sim | dermatite digital (F12) |

Total: 23 perguntas dinâmicas (8 exclusivas do veterinário) + cerca de 15 símbolos gravados pela triagem.

### 3.5 Regras por doença (camada 2)

Formato: `id [onde] SE condições ENTÃO doença cf | fonte`. `[T]` = só símbolos de triagem ou derivados de triagem; `[P]` = perguntável no modo produtor; `[V]` = usa variável exclusiva do veterinário. **Todas com `status: suposicao_a_validar`.** CF são estimativas minhas.

**Mastite clínica (`mastite`, gravidade média)**
```
R-MAS-01 [T] SE leite_alterado                         ENTÃO mastite +0,70 | F1
R-MAS-02 [T] SE ubere_inflamado                        ENTÃO mastite +0,60 | F1
R-MAS-03 [P] SE teste_caneca_positivo                  ENTÃO mastite +0,65 | F1
R-MAS-04 [P] SE um_quarto_afetado                      ENTÃO mastite +0,30 | suposição
R-MAS-05 [V] SE cmt_positivo                           ENTÃO mastite +0,75 | F1
R-MAS-06 [P] SE historico_mastite_12m                  ENTÃO mastite +0,15 | suposição
R-MAS-07 [T] SE leite_alterado = não E ubere_inflamado = não ENTÃO mastite −0,60 | suposição
```

**Metrite puerperal (`metrite`, gravidade alta)**
```
R-MET-01 [T] SE corrimento_vaginal E puerperio         ENTÃO metrite +0,60 | F2
R-MET-02 [T] SE febre E puerperio E apetite ∈ {reduzido, ausente} ENTÃO metrite +0,35 | F2
R-MET-03 [P] SE corrimento_fetido E puerperio          ENTÃO metrite +0,80 | F2
R-MET-04 [P] SE parto_complicado                       ENTÃO metrite +0,30 | suposição
R-MET-05 [V] SE utero_aumentado_palpacao E puerperio   ENTÃO metrite +0,50 | F2
R-MET-06 [T] SE dias_em_lactacao > 21                  ENTÃO metrite −0,80 | F2 (janela de 21 dias)
```

**Tristeza parasitária bovina (`tpb`, gravidade alta)**
```
R-TPB-01 [T] SE urina_escura E febre                   ENTÃO tpb +0,70 | F3
R-TPB-02 [T] SE febre E apatia                         ENTÃO tpb +0,30 | F5
R-TPB-03 [P] SE mucosas_palidas_amareladas             ENTÃO tpb +0,60 | F3, F4, F5
R-TPB-04 [P] SE carrapatos_presentes E febre           ENTÃO tpb +0,45 | F3, F5
R-TPB-05 [P] SE raca_grupo = europeia                  ENTÃO tpb +0,10 | F5
R-TPB-06 [V] SE esfregaco_hemoparasita                 ENTÃO tpb +0,90 | F3, F4
R-TPB-07 [T] SE febre = não E urina_escura = não       ENTÃO tpb −0,50 | suposição
```

**Cetose (`cetose`, gravidade média)**
```
R-CET-01 [T] SE inicio_lactacao E apetite ∈ {reduzido, ausente} E queda_producao ENTÃO cetose +0,45 | F6
R-CET-02 [T] SE inicio_lactacao E fezes_ressecadas     ENTÃO cetose +0,30 | F6
R-CET-03 [P] SE sinais_nervosos E inicio_lactacao      ENTÃO cetose +0,40 | F6
R-CET-04 [P] SE perda_condicao_corporal E inicio_lactacao ENTÃO cetose +0,30 | F6
R-CET-05 [P] SE abdomen_vazio E inicio_lactacao        ENTÃO cetose +0,25 | F6
R-CET-06 [V] SE bhb_sanguineo ≥ 1,2                    ENTÃO cetose +0,85 | F6
R-CET-07 [T] SE febre                                  ENTÃO cetose −0,30 | suposição (cetose primária é afebril)
R-CET-08 [T] SE dias_em_lactacao > 42                  ENTÃO cetose −0,60 | F6 (risco nas 6 primeiras semanas)
```

**Hipocalcemia / febre do leite (`hipocalcemia`, gravidade alta)**
```
R-HIP-01 [T] SE decubito E periparto_imediato          ENTÃO hipocalcemia +0,80 | F7
R-HIP-02 [T] SE hipotermia E periparto_imediato        ENTÃO hipocalcemia +0,60 | F7
R-HIP-03 [P] SE fraqueza_tremores E periparto_imediato ENTÃO hipocalcemia +0,50 | suposição
R-HIP-04 [V] SE calcio_sanguineo < 1,5                 ENTÃO hipocalcemia +0,90 | F7
R-HIP-05 [T] SE febre                                  ENTÃO hipocalcemia −0,50 | F7 (afebril)
R-HIP-06 [T] SE dias_em_lactacao > 7                   ENTÃO hipocalcemia −0,70 | F7 (até 48 h; margem suposição)
```

**Deslocamento de abomaso (`deslocamento_abomaso`, gravidade alta)**
```
R-DAB-01 [T] SE inicio_lactacao E apetite ∈ {reduzido, ausente} E queda_producao ENTÃO deslocamento_abomaso +0,30 | F8
R-DAB-02 [T] SE febre = não E apetite ∈ {reduzido, ausente} ENTÃO deslocamento_abomaso +0,15 | F8 (vitais normais)
R-DAB-03 [P] SE costelas_esquerdas_saltadas            ENTÃO deslocamento_abomaso +0,40 | F8
R-DAB-04 [V] SE ping_flanco_esquerdo                   ENTÃO deslocamento_abomaso +0,90 | F8
```

**Acidose ruminal (`acidose`, gravidade média)**
```
R-ACI-01 [T] SE diarreia E apetite ∈ {reduzido, ausente} ENTÃO acidose +0,40 | F9
R-ACI-02 [P] SE mudanca_dieta_recente                  ENTÃO acidose +0,60 | F9
R-ACI-03 [P] SE graos_nas_fezes                        ENTÃO acidose +0,50 | F9
R-ACI-04 [T] SE diarreia E apatia                      ENTÃO acidose +0,20 | suposição
R-ACI-05 [V] SE ph_ruminal < 5,5                       ENTÃO acidose +0,90 | F9
```

**Dermatite digital (`dermatite_digital`, gravidade baixa)**
```
R-DD-01 [T] SE claudicacao                             ENTÃO dermatite_digital +0,40 | F11 (lesão de casco mais comum em leiteiras)
R-DD-02 [T] SE claudicacao E febre = não E apetite = normal ENTÃO dermatite_digital +0,25 | suposição (quadro local)
R-DD-03 [P] SE ferida_vermelha_entre_unhas             ENTÃO dermatite_digital +0,75 | F12
R-DD-04 [P] SE casos_podais_no_rebanho                 ENTÃO dermatite_digital +0,20 | F12 (doença de rebanho)
R-DD-05 [V] SE lesao_dd_ativa                          ENTÃO dermatite_digital +0,90 | F12
R-DD-06 [P] SE inchaco_simetrico_acima_casco           ENTÃO dermatite_digital −0,40 | F12 (aponta foot rot)
```
Observação: foot rot (pododermatite) fica fora do escopo; o inchaço simétrico só reduz a confiança em dermatite digital, e o parecer recomenda exame do casco.

### 3.6 Bandeiras vermelhas (camada 3, classe `bandeira_vermelha`, conclusão `chamar_agora`)

Todas têm ao menos uma condição de triagem (exigência do validador).
```
R-BV-01 SE decubito                                    | vaca caída: hipocalcemia, choque, trauma (F7)
R-BV-02 SE urina_escura                                | hemólise: TPB aguda (F3)
R-BV-03 SE apetite = ausente E apatia                  | quadro sistêmico grave (suposição)
R-BV-04 SE hipotermia E apatia                         | colapso circulatório (F7)
R-BV-05 SE ubere_inflamado E febre E apatia            | mastite com sinais sistêmicos (F1, coliformes)
R-BV-06 SE temperatura_retal ≥ 41,0                    | febre muito alta (vet; limiar suposição)
```

### 3.7 Urgência por gravidade × confiança (camada 3, classe `urgencia`)

Gravidade é atributo do símbolo `doenca` (suposição): **alta** — TPB, hipocalcemia, deslocamento de abomaso, metrite; **média** — mastite, cetose, acidose; **baixa** — dermatite digital. Condições usam `cf_minimo`.
```
R-URG-<doença> (uma por doença):
  gravidade alta:  SE <doença> [cf_minimo 0,50]  ENTÃO chamar_agora +0,90
  gravidade média: SE <doença> [cf_minimo 0,50]  ENTÃO observar     +0,90
  gravidade baixa: SE <doença> [cf_minimo 0,50]  ENTÃO observar     +0,90
```
"A mais urgente vence." `sem_problema` **não é regra**: é o resultado quando nenhuma regra de urgência ou bandeira disparou e todas as doenças estão ≤ 0,35. Nos demais casos sem regra disparada, o resultado é `observar`. Assim nenhuma regra da camada 3 lê outra da mesma camada.

### 3.8 Impacto nas Seções 1 e 2

Aplicados (aprovados em 20/10):
1. `cf_minimo` na condição; três camadas estritas.
2. `gravidade` no símbolo `doenca`: usada na interface e como desempate na escolha da próxima pergunta.
3. Derivado de triagem só conta para a cobertura se **todas** as entradas vierem de `meta.triagem`.
4. "OU" com sinais redundantes vira derivado com `combinacao: max`; com sinais independentes, vira regras separadas.
5. Hipóteses entre 20% e 50% aparecem num bloco separado na interface: "Diagnóstico diferencial / sinais inespecíficos".

6. `sem_problema` sai das regras e vira resultado padrão (evita regra da camada 3 lendo bandeira da mesma camada). **Decisão minha, a confirmar.**

### 3.9 Riscos de domínio

- CF são estimativas sem calibração com dados reais; os casos de teste usam faixas largas por isso.
- Sinais de triagem inespecíficos (apetite, queda de leite) somam em várias doenças: espere três ou quatro hipóteses entre 20% e 50% em casos vagos. Vão para o bloco "Diagnóstico diferencial".
- Hemoglobinúria também ocorre em hipofosfatemia pós-parto e hemoglobinúria bacilar (fora do escopo); o parecer não deve afirmar TPB com certeza só por urina escura.
- Foot rot fica fora do escopo e pode ser confundido com dermatite digital pelo produtor.
