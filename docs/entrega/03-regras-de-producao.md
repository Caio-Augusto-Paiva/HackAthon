# Regras de produção — documentação gerada

> GERADO por `scripts/gerar_doc_regras.py`. Edite a base e regenere este arquivo.

Base de desenvolvimento; não é uma base ativa aprovada.

Versão: `3.1.0-revisao1`. Pai declarado: `3.0.0`. Data declarada na base: `2026-10-21`.

Arquivo: `base/desenvolvimento/anamnese-bovinos-v3.1.0-revisao1.json`. SHA-256 do JSON canônico: `395e2b49eb7db736b779b3eb9404707c81c27a60eac31eb6ecbcff2c9aaba1cf`. O hash usa UTF-8, chaves ordenadas e ausência de espaços, independente das quebras de linha do checkout.

Regras: **56**. Símbolos: **51**. Doenças: **8**.

| Estado | Quantidade |
| --- | --- |
| suposicao_a_validar | 56 |

As fontes descrevem o contexto clínico. Os números de CF são escolhas de modelagem do projeto; não são probabilidades nem valores publicados nessas referências.

## Limiares e limites

| Critério | Valor |
| --- | --- |
| descarte | -0,2 |
| premissa | 0,2 |
| hipotese_relevante | 0,35 |
| exaustao | 0,6 |
| potencial | 0,7 |
| confirmacao | 0,8 |
| bloco_principal | 0,5 |
| bloco_diferencial | 0,2 |

| Modo | Limite de perguntas dinâmicas |
| --- | --- |
| produtor | 12 |
| veterinario | 25 |

A triagem não consome o limite dinâmico. Premissa exige CF estritamente maior que 0,20. `sem_problema` é um resultado calculado pelo motor, sem regra de produção própria.

## Derivados — camada 1

| ID | Condições | Conclusão | CF | Prioridade | Fonte | Estado | Nota |
| --- | --- | --- | --- | --- | --- | --- | --- |
| `R-DER-01` | dias_em_lactacao ≤ 3 | periparto_imediato | 0,99 | 10 | Política de triagem do projeto, Seções 1 e 3; suposição a validar | suposicao_a_validar | Janela padrão de risco para distúrbios puerperais agudos imediatos. |
| `R-DER-02` | dias_em_lactacao ≤ 21 | puerperio | 0,99 | 10 | Política de triagem do projeto, Seções 1 e 3; suposição a validar | suposicao_a_validar | Janela clínica padronizada de puerpério e involução uterina primária. |
| `R-DER-03` | dias_em_lactacao ≤ 42 | inicio_lactacao | 0,99 | 10 | Política de triagem do projeto, Seções 1 e 3; suposição a validar | suposicao_a_validar | Janela de seis semanas adotada pela especificação do projeto; não exclui doença fora desse período. |
| `R-DER-04` | temperatura_retal ≥ 39,5 | febre | 0,95 | 10 | Política de triagem do projeto, Seções 1 e 3; suposição a validar | suposicao_a_validar | Temperatura no corte operacional de febre; o contexto clínico e ambiental permanece necessário. |
| `R-DER-05` | temperatura_retal < 38 | hipotermia | 0,85 | 10 | Política de triagem do projeto, Seções 1 e 3; suposição a validar | suposicao_a_validar | Temperatura abaixo do corte operacional de hipotermia; não identifica sua causa. |
| `R-DER-06` | extremidades = fria | hipotermia | 0,6 | 10 | Política de triagem do projeto, Seções 1 e 3; suposição a validar | suposicao_a_validar | Extremidades frias são um indício indireto, de menor confiança, de hipotermia ou comprometimento circulatório. |
| `R-DER-07` | extremidades = quente | febre | 0,45 | 10 | Política de triagem do projeto, Seções 1 e 3; suposição a validar | suposicao_a_validar | Calor periférico percebido ao toque é um indício indireto de febre; não substitui termometria. |
| `R-DER-08` | temperatura_retal < 39,5 | febre | -0,9 | 10 | Política de triagem do projeto, Seções 1 e 3; suposição a validar | suposicao_a_validar | Medição abaixo do corte operacional de febre fornece evidência contrária; não exclui infecção. |
| `R-DER-09` | temperatura_retal ≥ 38 | hipotermia | -0,9 | 10 | Política de triagem do projeto, Seções 1 e 3; suposição a validar | suposicao_a_validar | Medição acima do corte operacional fornece evidência contrária à hipotermia central; extremidades frias podem ter outras causas. |
| `R-DER-10` | extremidades = normal | febre | -0,4 | 10 | Política de triagem do projeto, Seções 1 e 3; suposição a validar | suposicao_a_validar | Extremidades percebidas como normais são evidência contrária fraca à febre; não substituem termometria. |
| `R-MAS-01` | leite_alterado = sim | evidencia_alteracao_leite | 0,6 | 10 | Referência clínica contextual: [referência](https://www.msdvetmanual.com/reproductive-system/mastitis-in-large-animals/mastitis-in-cattle); CF e tradução para regra: suposição do projeto a validar | suposicao_a_validar | Alteração macroscópica do leite alimenta o grupo de evidência mamária compartilhado com a caneca. |
| `R-MAS-03` | teste_caneca_grumos = sim | evidencia_alteracao_leite | 0,65 | 10 | Referência clínica contextual: [referência](https://www.msdvetmanual.com/reproductive-system/mastitis-in-large-animals/mastitis-in-cattle); CF e tradução para regra: suposição do projeto a validar | suposicao_a_validar | Grumos na caneca alimentam o mesmo grupo da alteração visual do leite, evitando contagem duplicada. |

## Acidose Ruminal — acidose (gravidade media)

| ID | Condições | Conclusão | CF | Prioridade | Fonte | Estado | Nota |
| --- | --- | --- | --- | --- | --- | --- | --- |
| `R-ACI-01` | diarreia = sim E apetite em {reduzido, ausente} | acidose | 0,35 | 10 | Referência clínica contextual: [referência](https://www.msdvetmanual.com/digestive-system/diseases-of-the-ruminant-forestomach/grain-overload-in-ruminants); CF e tradução para regra: suposição do projeto a validar | suposicao_a_validar | Hiporexia com fezes diarreicas sugere distúrbio fermentativo gastrointestinal. |
| `R-ACI-02` | mudanca_abrupta_concentrado = sim E diarreia = sim | acidose | 0,55 | 10 | Referência clínica contextual: [referência](https://www.msdvetmanual.com/digestive-system/diseases-of-the-ruminant-forestomach/grain-overload-in-ruminants); CF e tradução para regra: suposição do projeto a validar | suposicao_a_validar | Sobrecarga alimentar de grãos associada à diarreia aponta fermentação ruminal acelerada. |
| `R-ACI-03` | fezes_aquosas_espuma_graos = sim | acidose | 0,5 | 10 | Referência clínica contextual: [referência](https://www.msdvetmanual.com/digestive-system/diseases-of-the-ruminant-forestomach/grain-overload-in-ruminants); CF e tradução para regra: suposição do projeto a validar | suposicao_a_validar | Fezes aquosas, espuma e grãos não digeridos apoiam distúrbio digestivo, sem confirmar a etiologia. |
| `R-ACI-04` | ph_ruminal < 5,5 | acidose | 0,88 | 10 | Referência clínica contextual: [referência](https://www.msdvetmanual.com/digestive-system/diseases-of-the-ruminant-forestomach/grain-overload-in-ruminants); CF e tradução para regra: suposição do projeto a validar | suposicao_a_validar | pH ruminal abaixo de 5,5 apoia acidificação ruminal conforme método, horário da coleta e quadro clínico; não confirma sozinho acidose sistêmica nem distingue apresentação aguda de subaguda. |

## Cetose / Hipercetonemia — cetose (gravidade media)

| ID | Condições | Conclusão | CF | Prioridade | Fonte | Estado | Nota |
| --- | --- | --- | --- | --- | --- | --- | --- |
| `R-CET-01` | inicio_lactacao = sim E apetite em {reduzido, ausente} E queda_producao = sim | cetose | 0,4 | 10 | Referência clínica contextual: [referência](https://www.msdvetmanual.com/metabolic-disorders/hyperketonemia-in-cattle/hyperketonemia-in-cattle); CF e tradução para regra: suposição do projeto a validar | suposicao_a_validar | Hiporexia e queda de produção no início da lactação são sinais inespecíficos; outras doenças podem coexistir. |
| `R-CET-02` | inicio_lactacao = sim E halito_adocicado_acetona = sim | cetose | 0,5 | 10 | Referência clínica contextual: [referência](https://www.msdvetmanual.com/metabolic-disorders/hyperketonemia-in-cattle/hyperketonemia-in-cattle); CF e tradução para regra: suposição do projeto a validar | suposicao_a_validar | Relato de odor de acetona pode apoiar a hipótese, mas é subjetivo e requer confirmação. |
| `R-CET-03` | inicio_lactacao = sim E recusa_concentrado_come_volumoso = sim | cetose | 0,45 | 10 | Referência clínica contextual: [referência](https://www.msdvetmanual.com/metabolic-disorders/hyperketonemia-in-cattle/hyperketonemia-in-cattle); CF e tradução para regra: suposição do projeto a validar | suposicao_a_validar | Recusa seletiva de concentrado é um achado inespecífico e não confirma cetose isoladamente. |
| `R-CET-04` | bhb_sanguineo ≥ 1,2 | cetose | 0,85 | 10 | Referência clínica contextual: [referência](https://www.msdvetmanual.com/metabolic-disorders/hyperketonemia-in-cattle/hyperketonemia-in-cattle); CF e tradução para regra: suposição do projeto a validar | suposicao_a_validar | BHB sanguíneo de pelo menos 1,2 mmol/L é compatível com hipercetonemia; sinais adicionais são necessários para caracterizar cetose clínica. |
| `R-CET-05` | fita_urina_corpos_cetonicos = sim | cetose | 0,7 | 10 | Referência clínica contextual: [referência](https://www.msdvetmanual.com/metabolic-disorders/hyperketonemia-in-cattle/hyperketonemia-in-cattle); CF e tradução para regra: suposição do projeto a validar | suposicao_a_validar | Teste urinário positivo sustenta cetonúria; depende da técnica e do tempo de leitura e não confirma sozinho cetose clínica. |

## Dermatite Digital Bovina — dermatite_digital (gravidade baixa)

| ID | Condições | Conclusão | CF | Prioridade | Fonte | Estado | Nota |
| --- | --- | --- | --- | --- | --- | --- | --- |
| `R-DD-01` | claudicacao = sim | dermatite_digital | 0,3 | 10 | Referência clínica contextual: [referência](https://www.msdvetmanual.com/musculoskeletal-system/lameness-in-cattle/lameness-originating-in-the-hoof-in-cattle); CF e tradução para regra: suposição do projeto a validar | suposicao_a_validar | Claudicação é inespecífica e pode decorrer de várias doenças locomotoras. |
| `R-DD-02` | claudicacao = sim E dor_flexao_talao = sim | dermatite_digital | 0,5 | 10 | Referência clínica contextual: [referência](https://www.msdvetmanual.com/musculoskeletal-system/lameness-in-cattle/lameness-originating-in-the-hoof-in-cattle); CF e tradução para regra: suposição do projeto a validar | suposicao_a_validar | Dor no talão com claudicação localiza o problema, mas não substitui inspeção de lesão característica. |
| `R-DD-03` | lesao_erosiva_talao_morango = sim | dermatite_digital | 0,85 | 10 | Referência clínica contextual: [referência](https://www.msdvetmanual.com/musculoskeletal-system/lameness-in-cattle/lameness-originating-in-the-hoof-in-cattle); CF e tradução para regra: suposição do projeto a validar | suposicao_a_validar | Lesão ulcerativa circunscrita e granulomatosa no espaço interdigital/talão com aspecto de framboesa/morango. |

## Deslocamento de Abomaso — deslocamento_abomaso (gravidade alta)

| ID | Condições | Conclusão | CF | Prioridade | Fonte | Estado | Nota |
| --- | --- | --- | --- | --- | --- | --- | --- |
| `R-DAB-01` | inicio_lactacao = sim E apetite em {reduzido, ausente} E queda_producao = sim | deslocamento_abomaso | 0,3 | 10 | Referência clínica contextual: [referência](https://www.msdvetmanual.com/digestive-system/diseases-of-the-abomasum-in-cattle/abomasal-displacement-and-volvulus-in-cattle); CF e tradução para regra: suposição do projeto a validar | suposicao_a_validar | Sinais inespecíficos de redução de ingestão e lactação no pós-parto de vacas de alta produção. |
| `R-DAB-02` | inicio_lactacao = sim E flanco_esquerdo_afundado = sim | deslocamento_abomaso | 0,4 | 10 | Referência clínica contextual: [referência](https://www.msdvetmanual.com/digestive-system/diseases-of-the-abomasum-in-cattle/abomasal-displacement-and-volvulus-in-cattle); CF e tradução para regra: suposição do projeto a validar | suposicao_a_validar | Retração do flanco pode acompanhar redução da ingestão; é inespecífica para deslocamento de abomaso. |
| `R-DAB-03` | ping_metalico_flanco_esquerdo = sim | deslocamento_abomaso | 0,9 | 10 | Referência clínica contextual: [referência](https://www.msdvetmanual.com/digestive-system/diseases-of-the-abomasum-in-cattle/abomasal-displacement-and-volvulus-in-cattle); CF e tradução para regra: suposição do projeto a validar | suposicao_a_validar | Ping à esquerda em localização compatível apoia deslocamento à esquerda; exige diferenciação de outras estruturas com gás e não cobre deslocamento à direita ou vólvulo. |

## Hipocalcemia Puerperal — hipocalcemia (gravidade alta)

| ID | Condições | Conclusão | CF | Prioridade | Fonte | Estado | Nota |
| --- | --- | --- | --- | --- | --- | --- | --- |
| `R-HIP-01` | decubito = sim E periparto_imediato = sim | hipocalcemia | 0,65 | 10 | Referência clínica contextual: [referência](https://www.msdvetmanual.com/metabolic-disorders/parturient-paresis-in-ruminants/parturient-paresis-in-cows); CF e tradução para regra: suposição do projeto a validar | suposicao_a_validar | Vaca caída nas primeiras 72 horas pós-parto sugere paresia por hipocalcemia puerperal. |
| `R-HIP-02` | periparto_imediato = sim E pescoco_em_s = sim E hipotermia = sim | hipocalcemia | 0,8 | 10 | Referência clínica contextual: [referência](https://www.msdvetmanual.com/metabolic-disorders/parturient-paresis-in-ruminants/parturient-paresis-in-cows); CF e tradução para regra: suposição do projeto a validar | suposicao_a_validar | Perda do tônus cervical e hipotermia periférica sustentam fase parética clínica. |
| `R-HIP-03` | calcio_serico < 1,5 | hipocalcemia | 0,9 | 10 | Referência clínica contextual: [referência](https://www.msdvetmanual.com/metabolic-disorders/parturient-paresis-in-ruminants/parturient-paresis-in-cows); CF e tradução para regra: suposição do projeto a validar | suposicao_a_validar | Cálcio sérico total < 1,5 mmol/L (ou < 6,0 mg/dL) confirma hipocalcemia bioquímica acentuada. |
| `R-HIP-04` | febre = sim | hipocalcemia | -0,4 | 10 | Referência clínica contextual: [referência](https://www.msdvetmanual.com/metabolic-disorders/parturient-paresis-in-ruminants/parturient-paresis-in-cows); CF e tradução para regra: suposição do projeto a validar | suposicao_a_validar | Paresia puerperal clássica é afebril; presença de pirexia enfraquece a hipótese primária. |

## Mastite — mastite (gravidade media)

| ID | Condições | Conclusão | CF | Prioridade | Fonte | Estado | Nota |
| --- | --- | --- | --- | --- | --- | --- | --- |
| `R-MAS-02` | ubere_inflamado = sim | mastite | 0,5 | 10 | Referência clínica contextual: [referência](https://www.msdvetmanual.com/reproductive-system/mastitis-in-large-animals/mastitis-in-cattle); CF e tradução para regra: suposição do projeto a validar | suposicao_a_validar | Edema, calor ou dor no úbere sustentam inflamação mamária; não identificam isoladamente o agente causal. |
| `R-MAS-04` | cmt_reagente = sim | mastite | 0,4 | 10 | Referência clínica contextual: [referência](https://www.msdvetmanual.com/reproductive-system/mastitis-in-large-animals/mastitis-in-cattle); CF e tradução para regra: suposição do projeto a validar | suposicao_a_validar | CMT reagente indica aumento de células somáticas e sustenta inflamação; não diferencia sozinho mastite clínica de subclínica. |
| `R-MAS-05` | evidencia_alteracao_leite = sim | mastite | 0,99 | 10 | Referência clínica contextual: [referência](https://www.msdvetmanual.com/reproductive-system/mastitis-in-large-animals/mastitis-in-cattle); CF e tradução para regra: suposição do projeto a validar | suposicao_a_validar | Propaga a maior evidência de alteração do leite sem somar novamente o resultado da caneca. A multiplicação por 0,99 evita peso unitário fora do contrato. |

## Metrite Puerperal — metrite (gravidade alta)

| ID | Condições | Conclusão | CF | Prioridade | Fonte | Estado | Nota |
| --- | --- | --- | --- | --- | --- | --- | --- |
| `R-MET-01` | puerperio = sim E corrimento_fetido = sim | metrite | 0,75 | 10 | Referência clínica contextual: [referência](https://www.msdvetmanual.com/reproductive-system/uterine-diseases-in-production-animals/metritis-in-production-animals); CF e tradução para regra: suposição do projeto a validar | suposicao_a_validar | Corrimento fétido no puerpério sustenta a hipótese de metrite; não estabelece sozinho toxemia. |
| `R-MET-02` | corrimento_vaginal = sim E puerperio = sim E febre = sim | metrite | 0,45 | 10 | Referência clínica contextual: [referência](https://www.msdvetmanual.com/reproductive-system/uterine-diseases-in-production-animals/metritis-in-production-animals); CF e tradução para regra: suposição do projeto a validar | suposicao_a_validar | Corrimento inespecífico somado a febre no puerpério sugere complicação infecciosa uterina. |
| `R-MET-03` | puerperio = sim E utero_aumentado_palpacao = sim E corrimento_vaginal = sim | metrite | 0,35 | 10 | Referência clínica contextual: [referência](https://www.msdvetmanual.com/reproductive-system/uterine-diseases-in-production-animals/metritis-in-production-animals); CF e tradução para regra: suposição do projeto a validar | suposicao_a_validar | Aumento uterino no puerpério recebe apoio apenas quando há corrimento vaginal anormal; tamanho isolado não confirma infecção. |
| `R-MET-04` | retencao_placenta = sim E puerperio = sim | metrite | 0,25 | 10 | Referência clínica contextual: [referência](https://www.msdvetmanual.com/reproductive-system/uterine-diseases-in-production-animals/metritis-in-production-animals); CF e tradução para regra: suposição do projeto a validar | suposicao_a_validar | Retenção de membranas fetais é fator de risco epidemiológico para infecção ascendente. |

## Tristeza Parasitária Bovina — tpb (gravidade alta)

| ID | Condições | Conclusão | CF | Prioridade | Fonte | Estado | Nota |
| --- | --- | --- | --- | --- | --- | --- | --- |
| `R-TPB-01` | febre = sim E urina_escura = sim | tpb | 0,7 | 10 | Referência clínica contextual: [referência](https://www.msdvetmanual.com/circulatory-system/blood-parasites/anaplasmosis-in-ruminants); CF e tradução para regra: suposição do projeto a validar; [referência](https://www.msdvetmanual.com/circulatory-system/blood-parasites/babesiosis-in-animals) | suposicao_a_validar | Combinação de febre aguda e hemoglobinúria por hemólise intravascular típica de babesiose. |
| `R-TPB-02` | mucosas_palidas_ou_ictéricas = sim | tpb | 0,6 | 10 | Referência clínica contextual: [referência](https://www.msdvetmanual.com/circulatory-system/blood-parasites/anaplasmosis-in-ruminants); CF e tradução para regra: suposição do projeto a validar | suposicao_a_validar | Palidez ou icterícia mantêm TPB entre as hipóteses mesmo sem febre na medição atual; não identificam a causa da anemia ou icterícia. |
| `R-TPB-03` | carrapatos_historico_recente = sim E febre = sim | tpb | 0,35 | 10 | Referência clínica contextual: [referência](https://www.msdvetmanual.com/circulatory-system/blood-parasites/anaplasmosis-in-ruminants); CF e tradução para regra: suposição do projeto a validar; [referência](https://www.msdvetmanual.com/circulatory-system/blood-parasites/babesiosis-in-animals) | suposicao_a_validar | Exposição ao vetor carrapato combinada com febre é indicativo epidemiológico inicial. |
| `R-TPB-04` | esfregaco_hemoparasitas = sim | tpb | 0,9 | 10 | Referência clínica contextual: [referência](https://www.msdvetmanual.com/circulatory-system/blood-parasites/anaplasmosis-in-ruminants); CF e tradução para regra: suposição do projeto a validar; [referência](https://www.msdvetmanual.com/circulatory-system/blood-parasites/babesiosis-in-animals) | suposicao_a_validar | Esfregaço compatível sustenta infecção por hemoparasitas, mesmo sem febre atual; não distingue sozinho doença ativa de estado de portador. |

## Bandeiras vermelhas — camada 3

| ID | Condições | Conclusão | CF | Prioridade | Fonte | Estado | Nota |
| --- | --- | --- | --- | --- | --- | --- | --- |
| `R-BV-01` | decubito = sim | chamar_agora | 0,99 | 100 | Política de triagem do projeto, Seções 1 e 3; suposição a validar | suposicao_a_validar | Incapacidade de se levantar exige avaliação veterinária imediata, independentemente da hipótese causal. |
| `R-BV-02` | urina_escura = sim | chamar_agora | 0,99 | 100 | Política de triagem do projeto, Seções 1 e 3; suposição a validar | suposicao_a_validar | Urina escura é sinal de alerta adotado pelo projeto; a cor isolada não identifica hemoglobinúria nem sua causa. |
| `R-BV-03` | apetite = ausente E apatia = sim | chamar_agora | 0,99 | 100 | Política de triagem do projeto, Seções 1 e 3; suposição a validar | suposicao_a_validar | Ausência de apetite associada à apatia atende ao critério de alerta do projeto. |
| `R-BV-04` | hipotermia = sim E apatia = sim | chamar_agora | 0,99 | 100 | Política de triagem do projeto, Seções 1 e 3; suposição a validar | suposicao_a_validar | Evidência de hipotermia com apatia atende ao critério de alerta do projeto; não confirma choque. |
| `R-BV-05` | ubere_inflamado = sim E febre = sim E apatia = sim | chamar_agora | 0,99 | 100 | Política de triagem do projeto, Seções 1 e 3; suposição a validar | suposicao_a_validar | Alteração inflamatória do úbere com febre e apatia sugere comprometimento sistêmico e atende ao critério de alerta. |
| `R-BV-06` | temperatura_retal ≥ 41 | chamar_agora | 0,99 | 100 | Política de triagem do projeto, Seções 1 e 3; suposição a validar | suposicao_a_validar | Temperatura medida de pelo menos 41 °C atende ao corte de alerta do projeto; não identifica a causa. |

## Urgências — camada 3

| ID | Condições | Conclusão | CF | Prioridade | Fonte | Estado | Nota |
| --- | --- | --- | --- | --- | --- | --- | --- |
| `R-URG-01` | hipocalcemia = sim [CF ≥ 0,5] | chamar_agora | 0,99 | 50 | Política de triagem do projeto, Seções 1 e 3; suposição a validar | suposicao_a_validar | Aplica a política de gravidade do projeto quando o CF de hipocalcemia é pelo menos 0,50. Não prescreve tratamento nem estabelece diagnóstico definitivo. |
| `R-URG-02` | tpb = sim [CF ≥ 0,5] | chamar_agora | 0,99 | 50 | Política de triagem do projeto, Seções 1 e 3; suposição a validar | suposicao_a_validar | Aplica a política de gravidade do projeto quando o CF de tpb é pelo menos 0,50. Não prescreve tratamento nem estabelece diagnóstico definitivo. |
| `R-URG-03` | deslocamento_abomaso = sim [CF ≥ 0,5] | chamar_agora | 0,99 | 50 | Política de triagem do projeto, Seções 1 e 3; suposição a validar | suposicao_a_validar | Aplica a política de gravidade do projeto quando o CF de deslocamento_abomaso é pelo menos 0,50. Não prescreve tratamento nem estabelece diagnóstico definitivo. |
| `R-URG-04` | metrite = sim [CF ≥ 0,5] | chamar_agora | 0,99 | 50 | Política de triagem do projeto, Seções 1 e 3; suposição a validar | suposicao_a_validar | Aplica a política de gravidade do projeto quando o CF de metrite é pelo menos 0,50. Não prescreve tratamento nem estabelece diagnóstico definitivo. |
| `R-URG-05` | mastite = sim [CF ≥ 0,5] | observar | 0,8 | 50 | Política de triagem do projeto, Seções 1 e 3; suposição a validar | suposicao_a_validar | Aplica a política de gravidade do projeto quando o CF de mastite é pelo menos 0,50. Não prescreve tratamento nem estabelece diagnóstico definitivo. |
| `R-URG-06` | cetose = sim [CF ≥ 0,5] | observar | 0,8 | 50 | Política de triagem do projeto, Seções 1 e 3; suposição a validar | suposicao_a_validar | Aplica a política de gravidade do projeto quando o CF de cetose é pelo menos 0,50. Não prescreve tratamento nem estabelece diagnóstico definitivo. |
| `R-URG-07` | acidose = sim [CF ≥ 0,5] | observar | 0,8 | 50 | Política de triagem do projeto, Seções 1 e 3; suposição a validar | suposicao_a_validar | Aplica a política de gravidade do projeto quando o CF de acidose é pelo menos 0,50. Não prescreve tratamento nem estabelece diagnóstico definitivo. |
| `R-URG-08` | dermatite_digital = sim [CF ≥ 0,5] | observar | 0,7 | 50 | Política de triagem do projeto, Seções 1 e 3; suposição a validar | suposicao_a_validar | Aplica a política de gravidade do projeto quando o CF de dermatite_digital é pelo menos 0,50. Não prescreve tratamento nem estabelece diagnóstico definitivo. |

## Símbolos

| ID | Nome | Tipo | Domínio | Pergunta: produtor | Pergunta: veterinário | Gravidade | Combinação |
| --- | --- | --- | --- | --- | --- | --- | --- |
| acidose | Acidose Ruminal | doenca | tipo: booleano | — | — | media | mycin |
| apatia | Apatia | pergunta | tipo: booleano | A vaca está abatida ou pouco responsiva? | Animal apático ou com resposta reduzida ao ambiente? | — | mycin |
| apetite | Apetite | pergunta | tipo: categorico, valores: {normal, reduzido, ausente} | Como está o apetite: normal, reduzido ou ausente? | Apetite normal, reduzido ou ausente? | — | mycin |
| bhb_sanguineo | BHB sanguíneo | pergunta | min: 0, tipo: numerico, unidade: mmol/L | — | Qual é a concentração sanguínea de BHB, em mmol/L? | — | mycin |
| calcio_serico | Cálcio sérico total | pergunta | min: 0, tipo: numerico, unidade: mmol/L | — | Qual é o cálcio sérico total, em mmol/L? | — | mycin |
| carrapatos_historico_recente | Exposição recente a carrapatos | pergunta | tipo: booleano | Foram vistos carrapatos na vaca recentemente? | Histórico recente de exposição a carrapatos? | — | mycin |
| cetose | Cetose / Hipercetonemia | doenca | tipo: booleano | — | — | media | mycin |
| chamar_agora | Atendimento Veterinário Imediato | urgencia | tipo: booleano | — | — | — | mycin |
| claudicacao | Claudicação | pergunta | tipo: booleano | A vaca está mancando ou poupando uma pata? | Presença de claudicação? | — | mycin |
| cmt_reagente | CMT reagente | pergunta | tipo: booleano | — | O CMT foi reagente conforme a leitura do teste? | — | mycin |
| corrimento_fetido | Corrimento vaginal fétido | pergunta | tipo: booleano | A secreção da vulva tem cheiro forte e desagradável? | Corrimento vaginal fétido observado? | — | mycin |
| corrimento_vaginal | Corrimento vaginal | pergunta | tipo: booleano | Há saída de secreção anormal pela vulva? | Presença de corrimento vaginal anormal? | — | mycin |
| decubito | Decúbito | pergunta | tipo: booleano | A vaca está caída e não consegue se levantar? | Animal em decúbito, incapaz de se levantar? | — | mycin |
| dermatite_digital | Dermatite Digital Bovina | doenca | tipo: booleano | — | — | baixa | mycin |
| deslocamento_abomaso | Deslocamento de Abomaso | doenca | tipo: booleano | — | — | alta | mycin |
| diarreia | Diarreia | pergunta | tipo: booleano | A vaca está com diarreia? | Presença de diarreia? | — | mycin |
| dias_em_lactacao | Dias em lactação | ficha | min: 0, tipo: numerico, unidade: dias | Há quantos dias a vaca pariu? | Dias transcorridos desde o último parto? | — | mycin |
| dor_flexao_talao | Dor na região do talão | pergunta | tipo: booleano | A vaca demonstra dor na região do talão ao se movimentar? | Dor localizada na região dos bulbos do talão? | — | mycin |
| esfregaco_hemoparasitas | Hemoparasitas no esfregaço | pergunta | tipo: booleano | — | Esfregaço sanguíneo com estruturas compatíveis com Babesia ou Anaplasma? | — | mycin |
| evidencia_alteracao_leite | Evidência agrupada de alteração do leite | derivado | tipo: booleano | — | — | — | max |
| extremidades | Temperatura ao toque das extremidades | pergunta | tipo: categorico, valores: {normal, quente, fria} | As orelhas e as patas parecem normais, quentes ou frias ao toque? | Extremidades normais, quentes ou frias à palpação? | — | mycin |
| febre | Febre | derivado | tipo: booleano | — | — | — | mycin |
| fezes_aquosas_espuma_graos | Fezes com espuma e grãos | pergunta | tipo: booleano | As fezes estão muito líquidas, com espuma ou grãos inteiros? | Fezes aquosas, com espuma ou grãos não digeridos? | — | mycin |
| fita_urina_corpos_cetonicos | Corpos cetônicos na urina | pergunta | tipo: booleano | — | Teste urinário para corpos cetônicos positivo, lido no tempo indicado pelo fabricante? | — | mycin |
| flanco_esquerdo_afundado | Flanco esquerdo afundado | pergunta | tipo: booleano | A região do flanco esquerdo parece mais afundada que o habitual? | Fossa paralombar esquerda retraída? | — | mycin |
| halito_adocicado_acetona | Hálito adocicado | pergunta | tipo: booleano | O hálito da vaca tem cheiro adocicado, semelhante à acetona? | Odor adocicado ou de acetona no hálito? | — | mycin |
| hipocalcemia | Hipocalcemia Puerperal | doenca | tipo: booleano | — | — | alta | mycin |
| hipotermia | Hipotermia | derivado | tipo: booleano | — | — | — | mycin |
| inicio_lactacao | Inicio lactacao | derivado | tipo: booleano | — | — | — | mycin |
| leite_alterado | Alteração visível do leite | pergunta | tipo: booleano | O leite apresenta grumos, sangue ou aspecto aguado? | Alteração macroscópica do leite? | — | mycin |
| lesao_erosiva_talao_morango | Lesão característica no talão | pergunta | tipo: booleano | — | Lesão erosiva ou ulcerativa, avermelhada e dolorosa no talão ou espaço interdigital? | — | mycin |
| mastite | Mastite | doenca | tipo: booleano | — | — | media | mycin |
| metrite | Metrite Puerperal | doenca | tipo: booleano | — | — | alta | mycin |
| mucosas_palidas_ou_ictéricas | Mucosas pálidas ou amareladas | pergunta | tipo: booleano | A parte interna da pálpebra ou da vulva está muito pálida ou amarelada? | Mucosas pálidas ou ictéricas à inspeção? | — | mycin |
| mudanca_abrupta_concentrado | Mudança abrupta de concentrado | pergunta | tipo: booleano | Houve aumento brusco de ração ou acesso excessivo a grãos? | Mudança abrupta de concentrado ou acesso excessivo a grãos? | — | mycin |
| observar | Monitoramento Clínico Contínuo | urgencia | tipo: booleano | — | — | — | mycin |
| periparto_imediato | Periparto imediato | derivado | tipo: booleano | — | — | — | mycin |
| pescoco_em_s | Desvio cervical em S | pergunta | tipo: booleano | A vaca mantém o pescoço curvado em forma de S? | Desvio cervical em S observado? | — | mycin |
| ph_ruminal | pH ruminal | pergunta | max: 14, min: 0, tipo: numerico, unidade: pH | — | Qual é o pH ruminal medido, considerando método e momento da coleta? | — | mycin |
| ping_metalico_flanco_esquerdo | Ping no flanco esquerdo | pergunta | tipo: booleano | — | Ping metálico no flanco esquerdo à percussão e auscultação simultâneas? | — | mycin |
| puerperio | Puerperio | derivado | tipo: booleano | — | — | — | mycin |
| queda_producao | Queda de produção de leite | pergunta | tipo: booleano | A produção de leite caiu em relação ao habitual? | Queda da produção em relação ao padrão individual? | — | mycin |
| recusa_concentrado_come_volumoso | Recusa seletiva de concentrado | pergunta | tipo: booleano | A vaca recusa a ração, mas ainda come capim ou feno? | Recusa de concentrado com manutenção da ingestão de volumoso? | — | mycin |
| retencao_placenta | Histórico de retenção de placenta | ficha | tipo: booleano | Houve retenção de placenta neste parto? | Retenção de membranas fetais após o último parto? | — | mycin |
| sem_problema | Sem evidência de urgência pelos critérios da base | urgencia | tipo: booleano | — | — | — | mycin |
| temperatura_retal | Temperatura retal | pergunta | tipo: numerico, unidade: °C | — | Qual é a temperatura retal medida em °C? | — | mycin |
| teste_caneca_grumos | Grumos na caneca | pergunta | tipo: booleano | O teste da caneca mostrou grumos no leite? | Grumos detectados no teste da caneca? | — | mycin |
| tpb | Tristeza Parasitária Bovina | doenca | tipo: booleano | — | — | alta | mycin |
| ubere_inflamado | Inflamação do úbere | pergunta | tipo: booleano | O úbere está inchado, quente ou dolorido? | Há edema, calor ou dor no úbere? | — | mycin |
| urina_escura | Urina escura | pergunta | tipo: booleano | A urina está avermelhada ou escura como café? | Urina avermelhada ou castanha observada? | — | mycin |
| utero_aumentado_palpacao | Aumento uterino à palpação | pergunta | tipo: booleano | — | Útero aumentado à palpação retal, considerado o período após o parto? | — | mycin |

## Telas de triagem

| Ordem | ID | Seleção | Símbolos | Texto: produtor | Texto: veterinário | Alternativas por modo |
| --- | --- | --- | --- | --- | --- | --- |
| 1 | dias_em_lactacao | unica | dias_em_lactacao | Há quantos dias ocorreu o último parto? | Há quantos dias ocorreu o último parto? |  |
| 2 | estado_termico | unica | extremidades, temperatura_retal | Informe o estado térmico: extremidades normais, quentes ou frias; no modo veterinário, temperatura retal em °C. | Informe o estado térmico: extremidades normais, quentes ou frias; no modo veterinário, temperatura retal em °C. | produtor: extremidades; veterinario: temperatura_retal |
| 3 | atitude_locomocao | multipla | apatia, claudicacao, decubito | Marque as alterações: abatimento, mancar ou incapacidade de se levantar. Sem alteração: nenhuma opção. | Marque as alterações: abatimento, mancar ou incapacidade de se levantar. Sem alteração: nenhuma opção. |  |
| 4 | apetite_ruminacao | unica | apetite | Informe o apetite: normal, reduzido ou ausente. | Informe o apetite: normal, reduzido ou ausente. |  |
| 5 | producao_leite | multipla | queda_producao, leite_alterado, ubere_inflamado | Marque as alterações: queda de produção, leite alterado ou úbere inflamado. Sem alteração: nenhuma opção. | Marque as alterações: queda de produção, leite alterado ou úbere inflamado. Sem alteração: nenhuma opção. |  |
| 6 | excrecoes | multipla | diarreia, corrimento_vaginal, urina_escura | Marque as alterações: diarreia, corrimento vaginal anormal ou urina escura. Sem alteração: nenhuma opção. | Marque as alterações: diarreia, corrimento vaginal anormal ou urina escura. Sem alteração: nenhuma opção. |  |

## Leitura e limites

O derivado `evidencia_alteracao_leite` usa `max`: inspeção do leite e teste da caneca não são somados como achados independentes. As regras R-MAS-01 e R-MAS-03 estão na camada 1; R-MAS-05 propaga o grupo para a doença. A ordem das tabelas é editorial; a agenda é calculada pelo motor.

Este documento descreve a base de desenvolvimento disponibilizada. Não demonstra equivalência integral com a Seção 3 da especificação nem aprovação para uso clínico.

Todo o conhecimento veterinário é suposição a validar; extraído de fontes públicas por IA, sem especialista.
