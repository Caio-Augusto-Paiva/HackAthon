# Regras de produção — documentação gerada

> GERADO por `scripts/gerar_doc_regras.py`. Edite a base e regenere este arquivo.

Base indicada pelo ponteiro ativo; ativação operacional não é validação clínica.

Versão: `v0008`. Pai declarado: `v0007`. Data declarada na base: `2026-10-26`.

Arquivo: `base/versoes/v0008.json`. SHA-256 do JSON canônico: `f39c076b99df20e8eb492be0df4f073e0dff2d216a22789c5b8a54bb102bf1a6`. O hash usa UTF-8, chaves ordenadas e ausência de espaços, independente das quebras de linha do checkout.

Regras: **164**. Símbolos: **118**. Doenças: **25**.

| Estado | Quantidade |
| --- | --- |
| suposicao_a_validar | 164 |

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
| exclusao | 0,5 |

| Modo | Limite de perguntas dinâmicas |
| --- | --- |
| produtor | 15 |
| veterinario | 30 |

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
| `R-ACI-05` | apetite em {reduzido, ausente} | acidose | 0,05 | 10 | Política do projeto: sinal isolado com peso baixo, para o parecer refletir evidência parcial; CF e regra: suposição do projeto a validar | suposicao_a_validar | Apetite reduzido ou ausente, sozinho, é sinal inespecífico de acidose ruminal. |

## Brucelose — brucelose (gravidade alta)

| ID | Condições | Conclusão | CF | Prioridade | Fonte | Estado | Nota |
| --- | --- | --- | --- | --- | --- | --- | --- |
| `R-BRU-01` | aborto_recente = sim E historico_retencao_placenta = sim | brucelose | 0,4 | 10 | Referência clínica contextual: [referência](https://www.msdvetmanual.com/pt/reproductive-system/brucelose-em-animais-de-grande-porte/brucelose-em-bovinos); CF e tradução para regra: suposição do projeto a validar | suposicao_a_validar | Aborto no terço final seguido de retenção de placenta é o quadro clássico da brucelose. |
| `R-BRU-02` | higroma = sim | brucelose | 0,4 | 10 | Referência clínica contextual: [referência](https://www.msdvetmanual.com/pt/reproductive-system/brucelose-em-animais-de-grande-porte/brucelose-em-bovinos); CF e tradução para regra: suposição do projeto a validar | suposicao_a_validar | Higroma carpal é achado sugestivo de brucelose crônica no rebanho. |
| `R-BRU-03` | sorologia_brucelose_reagente = sim | brucelose | 0,9 | 10 | Referência clínica contextual: [referência](https://www.msdvetmanual.com/pt/reproductive-system/brucelose-em-animais-de-grande-porte/brucelose-em-bovinos); CF e tradução para regra: suposição do projeto a validar | suposicao_a_validar | Sorologia reagente apoia brucelose; a confirmação segue o regulamento do PNCEBT. |
| `R-BRU-04` | corrimento_vaginal = sim | brucelose | 0,05 | 10 | Política do projeto: sinal isolado com peso baixo, para o parecer refletir evidência parcial; CF e regra: suposição do projeto a validar | suposicao_a_validar | Corrimento vaginal, sozinho, é sinal inespecífico. |
| `R-BRU-05` | vacinada_brucelose = sim | brucelose | -0,4 | 10 | Referência clínica contextual: [referência](https://www.msdvetmanual.com/pt/reproductive-system/brucelose-em-animais-de-grande-porte/brucelose-em-bovinos); CF e tradução para regra: suposição do projeto a validar | suposicao_a_validar | Diferencial: vacinação na idade correta reduz, mas não exclui, a brucelose. |

## Diarreia Viral Bovina (BVD) — bvd (gravidade alta)

| ID | Condições | Conclusão | CF | Prioridade | Fonte | Estado | Nota |
| --- | --- | --- | --- | --- | --- | --- | --- |
| `R-BVD-01` | diarreia = sim E feridas_boca = sim | bvd | 0,6 | 10 | Referência clínica contextual: [referência](https://www.msdvetmanual.com/pt/infectious-diseases/diarreia-viral-bovina/diarreia-viral-bovina-e-complexo-da-doen%C3%A7a-das-mucosas); CF e tradução para regra: suposição do projeto a validar | suposicao_a_validar | Diarreia com erosões orais é o quadro típico da BVD. |
| `R-BVD-02` | aborto_recente = sim E falhas_reprodutivas_lote = sim E febre = sim | bvd | 0,4 | 10 | Referência clínica contextual: [referência](https://www.msdvetmanual.com/pt/infectious-diseases/diarreia-viral-bovina/diarreia-viral-bovina-e-complexo-da-doen%C3%A7a-das-mucosas); CF e tradução para regra: suposição do projeto a validar | suposicao_a_validar | Aborto com falhas reprodutivas no lote é compatível com BVD. |
| `R-BVD-03` | antigeno_bvdv = sim | bvd | 0,9 | 10 | Referência clínica contextual: [referência](https://www.msdvetmanual.com/pt/infectious-diseases/diarreia-viral-bovina/diarreia-viral-bovina-e-complexo-da-doen%C3%A7a-das-mucosas); CF e tradução para regra: suposição do projeto a validar | suposicao_a_validar | Detecção de BVDV apoia a doença. |
| `R-BVD-04` | diarreia = sim E febre = sim | bvd | 0,1 | 10 | Política do projeto: sinal isolado com peso baixo, para o parecer refletir evidência parcial; CF e regra: suposição do projeto a validar | suposicao_a_validar | Diarreia com febre, sozinha, é sinal inespecífico. |
| `R-BVD-05` | fezes_aquosas_espuma_graos = sim E mudanca_abrupta_concentrado = sim | bvd | -0,4 | 10 | Referência clínica contextual: [referência](https://www.msdvetmanual.com/pt/infectious-diseases/diarreia-viral-bovina/diarreia-viral-bovina-e-complexo-da-doen%C3%A7a-das-mucosas); CF e tradução para regra: suposição do projeto a validar | suposicao_a_validar | Diferencial: fezes aquosas com grãos e espuma após mudança brusca para concentrado apontam para acidose, não para BVD. |

## Cetose / Hipercetonemia — cetose (gravidade media)

| ID | Condições | Conclusão | CF | Prioridade | Fonte | Estado | Nota |
| --- | --- | --- | --- | --- | --- | --- | --- |
| `R-CET-01` | inicio_lactacao = sim E apetite em {reduzido, ausente} E queda_producao = sim | cetose | 0,4 | 10 | Referência clínica contextual: [referência](https://www.msdvetmanual.com/metabolic-disorders/hyperketonemia-in-cattle/hyperketonemia-in-cattle); CF e tradução para regra: suposição do projeto a validar | suposicao_a_validar | Hiporexia e queda de produção no início da lactação são sinais inespecíficos; outras doenças podem coexistir. |
| `R-CET-02` | inicio_lactacao = sim E halito_adocicado_acetona = sim | cetose | 0,5 | 10 | Referência clínica contextual: [referência](https://www.msdvetmanual.com/metabolic-disorders/hyperketonemia-in-cattle/hyperketonemia-in-cattle); CF e tradução para regra: suposição do projeto a validar | suposicao_a_validar | Relato de odor de acetona pode apoiar a hipótese, mas é subjetivo e requer confirmação. |
| `R-CET-03` | inicio_lactacao = sim E recusa_concentrado_come_volumoso = sim | cetose | 0,45 | 10 | Referência clínica contextual: [referência](https://www.msdvetmanual.com/metabolic-disorders/hyperketonemia-in-cattle/hyperketonemia-in-cattle); CF e tradução para regra: suposição do projeto a validar | suposicao_a_validar | Recusa seletiva de concentrado é um achado inespecífico e não confirma cetose isoladamente. |
| `R-CET-04` | bhb_sanguineo ≥ 1,2 | cetose | 0,85 | 10 | Referência clínica contextual: [referência](https://www.msdvetmanual.com/metabolic-disorders/hyperketonemia-in-cattle/hyperketonemia-in-cattle); CF e tradução para regra: suposição do projeto a validar | suposicao_a_validar | BHB sanguíneo de pelo menos 1,2 mmol/L é compatível com hipercetonemia; sinais adicionais são necessários para caracterizar cetose clínica. |
| `R-CET-05` | fita_urina_corpos_cetonicos = sim | cetose | 0,7 | 10 | Referência clínica contextual: [referência](https://www.msdvetmanual.com/metabolic-disorders/hyperketonemia-in-cattle/hyperketonemia-in-cattle); CF e tradução para regra: suposição do projeto a validar | suposicao_a_validar | Teste urinário positivo sustenta cetonúria; depende da técnica e do tempo de leitura e não confirma sozinho cetose clínica. |
| `R-CET-06` | apetite em {reduzido, ausente} | cetose | 0,05 | 10 | Política do projeto: sinal isolado com peso baixo, para o parecer refletir evidência parcial; CF e regra: suposição do projeto a validar | suposicao_a_validar | Apetite reduzido ou ausente, sozinho, é sinal inespecífico de cetose. |

## Cisto Ovariano — cisto_ovariano (gravidade baixa)

| ID | Condições | Conclusão | CF | Prioridade | Fonte | Estado | Nota |
| --- | --- | --- | --- | --- | --- | --- | --- |
| `R-CIS-01` | dias_em_lactacao > 40 E apetite = normal E cio_irregular_ou_constante = sim | cisto_ovariano | 0,6 | 10 | Referência clínica contextual: [referência](https://www.msdvetmanual.com/pt/reproductive-system/doen%C3%A7a-do-ov%C3%A1rio-c%C3%ADstico/doen%C3%A7a-do-ov%C3%A1rio-c%C3%ADstico-folicular-em-vacas); CF e tradução para regra: suposição do projeto a validar | suposicao_a_validar | Cio irregular ou constante depois de 40 dias do parto, em vaca que come normalmente, é a queixa típica do cisto folicular; anestro também ocorre. Só se pergunta à vaca sem perda de apetite: com apetite reduzido, outras hipóteses vêm antes no limite de perguntas do produtor. |
| `R-CIS-02` | dias_em_lactacao > 40 E estrutura_ovariana_maior_25mm = sim | cisto_ovariano | 0,85 | 10 | Referência clínica contextual: [referência](https://www.msdvetmanual.com/pt/reproductive-system/doen%C3%A7a-do-ov%C3%A1rio-c%C3%ADstico/doen%C3%A7a-do-ov%C3%A1rio-c%C3%ADstico-folicular-em-vacas); CF e tradução para regra: suposição do projeto a validar | suposicao_a_validar | Estrutura ovariana com líquido maior que 25 mm, persistente e sem corpo lúteo, caracteriza a doença do ovário cístico. |
| `R-CIS-03` | dias_em_lactacao > 40 E corrimento_vaginal = sim | cisto_ovariano | -0,2 | 10 | Referência clínica contextual: [referência](https://www.msdvetmanual.com/pt/reproductive-system/doen%C3%A7a-do-ov%C3%A1rio-c%C3%ADstico/doen%C3%A7a-do-ov%C3%A1rio-c%C3%ADstico-folicular-em-vacas); CF e tradução para regra: suposição do projeto a validar | suposicao_a_validar | Diferencial: corrimento vaginal anormal aponta para o útero (endometrite), não para o ovário. |
| `R-CIS-04` | dias_em_lactacao > 40 E cio_irregular_ou_constante = sim | cisto_ovariano | 0,05 | 10 | Política do projeto: sinal isolado com peso baixo, para o parecer refletir evidência parcial; CF e regra: suposição do projeto a validar | suposicao_a_validar | Cio irregular ou constante depois de 40 dias do parto, sem o contexto de apetite normal, é sinal inespecífico de cisto ovariano. |

## Dermatite Digital Bovina — dermatite_digital (gravidade baixa)

| ID | Condições | Conclusão | CF | Prioridade | Fonte | Estado | Nota |
| --- | --- | --- | --- | --- | --- | --- | --- |
| `R-DD-01` | claudicacao = sim | dermatite_digital | 0,3 | 10 | Referência clínica contextual: [referência](https://www.msdvetmanual.com/musculoskeletal-system/lameness-in-cattle/lameness-originating-in-the-hoof-in-cattle); CF e tradução para regra: suposição do projeto a validar | suposicao_a_validar | Claudicação é inespecífica e pode decorrer de várias doenças locomotoras. |
| `R-DD-02` | claudicacao = sim E dor_flexao_talao = sim | dermatite_digital | 0,5 | 10 | Referência clínica contextual: [referência](https://www.msdvetmanual.com/musculoskeletal-system/lameness-in-cattle/lameness-originating-in-the-hoof-in-cattle); CF e tradução para regra: suposição do projeto a validar | suposicao_a_validar | Dor no talão com claudicação localiza o problema, mas não substitui inspeção de lesão característica. |
| `R-DD-03` | lesao_erosiva_talao_morango = sim | dermatite_digital | 0,85 | 10 | Referência clínica contextual: [referência](https://www.msdvetmanual.com/musculoskeletal-system/lameness-in-cattle/lameness-originating-in-the-hoof-in-cattle); CF e tradução para regra: suposição do projeto a validar | suposicao_a_validar | Lesão ulcerativa circunscrita e granulomatosa no espaço interdigital/talão com aspecto de framboesa/morango. |

## Deslocamento de Abomaso à Direita — deslocamento_abomaso_direita (gravidade alta)

| ID | Condições | Conclusão | CF | Prioridade | Fonte | Estado | Nota |
| --- | --- | --- | --- | --- | --- | --- | --- |
| `R-DAD-01` | inicio_lactacao = sim E apetite em {reduzido, ausente} E fezes_escassas = sim | deslocamento_abomaso_direita | 0,3 | 10 | Referência clínica contextual: [referência](https://www.msdvetmanual.com/pt/digestive-system/doen%C3%A7as-do-abomaso/deslocamento-do-abomaso-para-a-esquerda-ou-direita-e-v%C3%B3lvulo-abomasal-em-bovinos); CF e tradução para regra: suposição do projeto a validar | suposicao_a_validar | Redução da ingestão e de fezes no pós-parto é compatível com deslocamento; não indica o lado. |
| `R-DAD-02` | distensao_flanco_direito = sim E apetite em {reduzido, ausente} | deslocamento_abomaso_direita | 0,75 | 10 | Referência clínica contextual: [referência](https://www.msdvetmanual.com/pt/digestive-system/doen%C3%A7as-do-abomaso/deslocamento-do-abomaso-para-a-esquerda-ou-direita-e-v%C3%B3lvulo-abomasal-em-bovinos); CF e tradução para regra: suposição do projeto a validar | suposicao_a_validar | Distensão do flanco direito sugere acúmulo no abomaso deslocado à direita. Exige apetite reduzido ou ausente na triagem para a pergunta só ser feita quando há sinal compatível, poupando o limite de perguntas do produtor (concessão de seleção; suposição a validar). |
| `R-DAD-03` | ping_flanco_direito = sim | deslocamento_abomaso_direita | 0,9 | 10 | Referência clínica contextual: [referência](https://www.msdvetmanual.com/pt/digestive-system/doen%C3%A7as-do-abomaso/deslocamento-do-abomaso-para-a-esquerda-ou-direita-e-v%C3%B3lvulo-abomasal-em-bovinos); CF e tradução para regra: suposição do projeto a validar | suposicao_a_validar | Ping no flanco direito apoia deslocamento à direita ou vólvulo; exige diferenciação de ceco e cólon com gás. |
| `R-DAD-04` | desidratacao = sim E apetite em {reduzido, ausente} | deslocamento_abomaso_direita | 0,3 | 10 | Referência clínica contextual: [referência](https://www.msdvetmanual.com/pt/digestive-system/doen%C3%A7as-do-abomaso/deslocamento-do-abomaso-para-a-esquerda-ou-direita-e-v%C3%B3lvulo-abomasal-em-bovinos); CF e tradução para regra: suposição do projeto a validar | suposicao_a_validar | Desidratação acompanha o quadro obstrutivo do deslocamento à direita. Exige apetite reduzido ou ausente na triagem para a pergunta só ser feita quando há sinal compatível, poupando o limite de perguntas do produtor (concessão de seleção; suposição a validar). |
| `R-DAD-05` | apetite em {reduzido, ausente} E apatia = sim | deslocamento_abomaso_direita | 0,05 | 10 | Política do projeto: sinal isolado com peso baixo, para o parecer refletir evidência parcial; CF e regra: suposição do projeto a validar | suposicao_a_validar | Apetite reduzido com abatimento, sozinho, é sinal inespecífico. |
| `R-DAD-06` | ping_metalico_flanco_esquerdo = sim | deslocamento_abomaso_direita | -0,6 | 10 | Referência clínica contextual: [referência](https://www.msdvetmanual.com/pt/digestive-system/doen%C3%A7as-do-abomaso/deslocamento-do-abomaso-para-a-esquerda-ou-direita-e-v%C3%B3lvulo-abomasal-em-bovinos); CF e tradução para regra: suposição do projeto a validar | suposicao_a_validar | Diferencial: ping no flanco esquerdo aponta para deslocamento à esquerda, não à direita. |

## Deslocamento de Abomaso à Esquerda — deslocamento_abomaso_esquerda (gravidade alta)

| ID | Condições | Conclusão | CF | Prioridade | Fonte | Estado | Nota |
| --- | --- | --- | --- | --- | --- | --- | --- |
| `R-DAE-01` | inicio_lactacao = sim E apetite em {reduzido, ausente} E queda_producao = sim | deslocamento_abomaso_esquerda | 0,3 | 10 | Referência clínica contextual: [referência](https://www.msdvetmanual.com/pt/digestive-system/doen%C3%A7as-do-abomaso/deslocamento-do-abomaso-para-a-esquerda-ou-direita-e-v%C3%B3lvulo-abomasal-em-bovinos); CF e tradução para regra: suposição do projeto a validar | suposicao_a_validar | Sinais inespecíficos de redução de ingestão e lactação no pós-parto de vacas de alta produção. |
| `R-DAE-02` | inicio_lactacao = sim E flanco_esquerdo_afundado = sim | deslocamento_abomaso_esquerda | 0,4 | 10 | Referência clínica contextual: [referência](https://www.msdvetmanual.com/pt/digestive-system/doen%C3%A7as-do-abomaso/deslocamento-do-abomaso-para-a-esquerda-ou-direita-e-v%C3%B3lvulo-abomasal-em-bovinos); CF e tradução para regra: suposição do projeto a validar | suposicao_a_validar | Retração do flanco pode acompanhar redução da ingestão; é inespecífica para deslocamento de abomaso. |
| `R-DAE-03` | ping_metalico_flanco_esquerdo = sim | deslocamento_abomaso_esquerda | 0,9 | 10 | Referência clínica contextual: [referência](https://www.msdvetmanual.com/pt/digestive-system/doen%C3%A7as-do-abomaso/deslocamento-do-abomaso-para-a-esquerda-ou-direita-e-v%C3%B3lvulo-abomasal-em-bovinos); CF e tradução para regra: suposição do projeto a validar | suposicao_a_validar | Ping à esquerda em localização compatível apoia deslocamento à esquerda; exige diferenciação de outras estruturas com gás. |
| `R-DAE-04` | apetite em {reduzido, ausente} | deslocamento_abomaso_esquerda | 0,05 | 10 | Política do projeto: sinal isolado com peso baixo, para o parecer refletir evidência parcial; CF e regra: suposição do projeto a validar | suposicao_a_validar | Apetite reduzido ou ausente, sozinho, é sinal inespecífico de deslocamento de abomaso. |
| `R-DAE-05` | inicio_lactacao = sim E fezes_escassas = sim | deslocamento_abomaso_esquerda | 0,2 | 10 | Referência clínica contextual: [referência](https://www.msdvetmanual.com/pt/digestive-system/doen%C3%A7as-do-abomaso/deslocamento-do-abomaso-para-a-esquerda-ou-direita-e-v%C3%B3lvulo-abomasal-em-bovinos); CF e tradução para regra: suposição do projeto a validar | suposicao_a_validar | Pouco esterco no início da lactação é compatível com deslocamento de abomaso. |
| `R-DAE-06` | ping_flanco_direito = sim | deslocamento_abomaso_esquerda | -0,6 | 10 | Referência clínica contextual: [referência](https://www.msdvetmanual.com/pt/digestive-system/doen%C3%A7as-do-abomaso/deslocamento-do-abomaso-para-a-esquerda-ou-direita-e-v%C3%B3lvulo-abomasal-em-bovinos); CF e tradução para regra: suposição do projeto a validar | suposicao_a_validar | Diferencial: ping no flanco direito aponta para deslocamento à direita, não à esquerda. |

## Endometrite Clínica — endometrite (gravidade media)

| ID | Condições | Conclusão | CF | Prioridade | Fonte | Estado | Nota |
| --- | --- | --- | --- | --- | --- | --- | --- |
| `R-END-01` | corrimento_vaginal = sim E dias_em_lactacao > 21 E corrimento_com_pus_apos_21_dias = sim | endometrite | 0,7 | 10 | Referência clínica contextual: [referência](https://www.msdvetmanual.com/pt/reproductive-system/doen%C3%A7as-uterinas-em-animais-de-produ%C3%A7%C3%A3o/endometrite-em-animais-de-produ%C3%A7%C3%A3o); CF e tradução para regra: suposição do projeto a validar | suposicao_a_validar | Corrimento com pus depois de 21 dias do parto, sem sinais sistêmicos, define endometrite clínica. Só vale com corrimento observado na triagem. |
| `R-END-02` | corrimento_vaginal = sim E dias_em_lactacao > 21 E metricheck_purulento = sim | endometrite | 0,85 | 10 | Referência clínica contextual: [referência](https://www.msdvetmanual.com/pt/reproductive-system/doen%C3%A7as-uterinas-em-animais-de-produ%C3%A7%C3%A3o/endometrite-em-animais-de-produ%C3%A7%C3%A3o); CF e tradução para regra: suposição do projeto a validar | suposicao_a_validar | Conteúdo purulento ou mucopurulento ao exame vaginal depois de 21 dias do parto sustenta endometrite clínica. |
| `R-END-03` | corrimento_vaginal = sim E dias_em_lactacao > 21 E febre = sim | endometrite | -0,4 | 10 | Referência clínica contextual: [referência](https://www.msdvetmanual.com/pt/reproductive-system/doen%C3%A7as-uterinas-em-animais-de-produ%C3%A7%C3%A3o/endometrite-em-animais-de-produ%C3%A7%C3%A3o); CF e tradução para regra: suposição do projeto a validar | suposicao_a_validar | Diferencial: a endometrite clínica não tem sinais sistêmicos; febre aponta para outro quadro infeccioso. |
| `R-END-04` | corrimento_vaginal = sim E dias_em_lactacao > 21 | endometrite | 0,05 | 10 | Política do projeto: sinal isolado com peso baixo, para o parecer refletir evidência parcial; CF e regra: suposição do projeto a validar | suposicao_a_validar | Corrimento vaginal depois de 21 dias do parto, sozinho, é sinal inespecífico de endometrite. |

## Flegmão Interdigital (Podridão do Casco) — flegmao_interdigital (gravidade media)

| ID | Condições | Conclusão | CF | Prioridade | Fonte | Estado | Nota |
| --- | --- | --- | --- | --- | --- | --- | --- |
| `R-FLE-01` | claudicacao = sim E inchaco_entre_unhas_mau_cheiro = sim | flegmao_interdigital | 0,65 | 10 | Referência clínica contextual: [referência](https://www.msdvetmanual.com/pt/musculoskeletal-system/claudica%C3%A7%C3%A3o-em-bovinos/claudica%C3%A7%C3%A3o-com-origem-no-casco-em-bovinos); CF e tradução para regra: suposição do projeto a validar | suposicao_a_validar | Manqueira aguda com inchaço entre as unhas e mau cheiro é o quadro típico da podridão do casco. |
| `R-FLE-02` | claudicacao = sim E fissura_interdigital_necrotica = sim | flegmao_interdigital | 0,85 | 10 | Referência clínica contextual: [referência](https://www.msdvetmanual.com/pt/musculoskeletal-system/claudica%C3%A7%C3%A3o-em-bovinos/claudica%C3%A7%C3%A3o-com-origem-no-casco-em-bovinos); CF e tradução para regra: suposição do projeto a validar | suposicao_a_validar | Fissura interdigital com necrose e odor fétido sustenta flegmão interdigital. |
| `R-FLE-03` | claudicacao = sim E febre = sim | flegmao_interdigital | 0,2 | 10 | Referência clínica contextual: [referência](https://www.msdvetmanual.com/pt/musculoskeletal-system/claudica%C3%A7%C3%A3o-em-bovinos/claudica%C3%A7%C3%A3o-com-origem-no-casco-em-bovinos); CF e tradução para regra: suposição do projeto a validar | suposicao_a_validar | Febre com manqueira apoia infecção de tecidos moles do pé; é sinal inespecífico. |
| `R-FLE-04` | claudicacao = sim E mancar_pata_traseira_sem_inchaco = sim | flegmao_interdigital | -0,4 | 10 | Referência clínica contextual: [referência](https://www.msdvetmanual.com/pt/musculoskeletal-system/claudica%C3%A7%C3%A3o-em-bovinos/claudica%C3%A7%C3%A3o-com-origem-no-casco-em-bovinos); CF e tradução para regra: suposição do projeto a validar | suposicao_a_validar | Diferencial: manqueira sem inchaço do pé contraria flegmão interdigital, que incha o espaço entre as unhas. |
| `R-FLE-05` | claudicacao = sim | flegmao_interdigital | 0,05 | 10 | Política do projeto: sinal isolado com peso baixo, para o parecer refletir evidência parcial; CF e regra: suposição do projeto a validar | suposicao_a_validar | Claudicação, sozinha, é sinal inespecífico de flegmão interdigital. |

## Hipocalcemia Puerperal — hipocalcemia (gravidade alta)

| ID | Condições | Conclusão | CF | Prioridade | Fonte | Estado | Nota |
| --- | --- | --- | --- | --- | --- | --- | --- |
| `R-HIP-01` | decubito = sim E periparto_imediato = sim | hipocalcemia | 0,65 | 10 | Referência clínica contextual: [referência](https://www.msdvetmanual.com/metabolic-disorders/parturient-paresis-in-ruminants/parturient-paresis-in-cows); CF e tradução para regra: suposição do projeto a validar | suposicao_a_validar | Vaca caída nas primeiras 72 horas pós-parto sugere paresia por hipocalcemia puerperal. |
| `R-HIP-02` | periparto_imediato = sim E pescoco_em_s = sim E hipotermia = sim | hipocalcemia | 0,8 | 10 | Referência clínica contextual: [referência](https://www.msdvetmanual.com/metabolic-disorders/parturient-paresis-in-ruminants/parturient-paresis-in-cows); CF e tradução para regra: suposição do projeto a validar | suposicao_a_validar | Perda do tônus cervical e hipotermia periférica sustentam fase parética clínica. |
| `R-HIP-03` | calcio_serico < 1,5 | hipocalcemia | 0,9 | 10 | Referência clínica contextual: [referência](https://www.msdvetmanual.com/metabolic-disorders/parturient-paresis-in-ruminants/parturient-paresis-in-cows); CF e tradução para regra: suposição do projeto a validar | suposicao_a_validar | Cálcio sérico total < 1,5 mmol/L (ou < 6,0 mg/dL) confirma hipocalcemia bioquímica acentuada. |
| `R-HIP-04` | febre = sim | hipocalcemia | -0,4 | 10 | Referência clínica contextual: [referência](https://www.msdvetmanual.com/metabolic-disorders/parturient-paresis-in-ruminants/parturient-paresis-in-cows); CF e tradução para regra: suposição do projeto a validar | suposicao_a_validar | Paresia puerperal clássica é afebril; presença de pirexia enfraquece a hipótese primária. |
| `R-HIP-05` | decubito = sim E dias_em_lactacao > 3 | hipocalcemia | 0,2 | 10 | Política do projeto: sinal isolado com peso baixo, para o parecer refletir evidência parcial; CF e regra: suposição do projeto a validar | suposicao_a_validar | Vaca caída fora do periparto imediato ainda sugere, com peso baixo, hipocalcemia. |
| `R-HIP-06` | hipotermia = sim E dias_em_lactacao > 3 | hipocalcemia | 0,15 | 10 | Política do projeto: sinal isolado com peso baixo, para o parecer refletir evidência parcial; CF e regra: suposição do projeto a validar | suposicao_a_validar | Temperatura abaixo de 38 °C, fora do periparto imediato, é sinal fraco de hipocalcemia. |

## Hipomagnesemia — hipomagnesemia (gravidade alta)

| ID | Condições | Conclusão | CF | Prioridade | Fonte | Estado | Nota |
| --- | --- | --- | --- | --- | --- | --- | --- |
| `R-HMG-01` | tremores = sim E agitacao = sim E apetite em {reduzido, ausente} | hipomagnesemia | 0,6 | 10 | Referência clínica contextual: [referência](https://www.msdvetmanual.com/pt/metabolic-disorders/dist%C3%BArbios-do-metabolismo-do-magn%C3%A9sio/tetania-hipomagnes%C3%AAmica-em-bovinos-e-ovinos); CF e tradução para regra: suposição do projeto a validar | suposicao_a_validar | Tremores com agitação são o quadro nervoso típico da tetania hipomagnesêmica. Exige apetite reduzido ou ausente na triagem para a pergunta só ser feita quando há sinal compatível, poupando o limite de perguntas do produtor (concessão de seleção; suposição a validar). |
| `R-HMG-02` | pasto_novo_adubado = sim E apetite em {reduzido, ausente} | hipomagnesemia | 0,3 | 10 | Referência clínica contextual: [referência](https://www.msdvetmanual.com/pt/metabolic-disorders/dist%C3%BArbios-do-metabolismo-do-magn%C3%A9sio/tetania-hipomagnes%C3%AAmica-em-bovinos-e-ovinos); CF e tradução para regra: suposição do projeto a validar | suposicao_a_validar | Mudança recente para pasto tenro ou adubado é fator de risco de falta de magnésio. Exige apetite reduzido ou ausente na triagem para a pergunta só ser feita quando há sinal compatível, poupando o limite de perguntas do produtor (concessão de seleção; suposição a validar). |
| `R-HMG-03` | magnesio_serico < 1,2 | hipomagnesemia | 0,9 | 10 | Referência clínica contextual: [referência](https://www.msdvetmanual.com/pt/metabolic-disorders/dist%C3%BArbios-do-metabolismo-do-magn%C3%A9sio/tetania-hipomagnes%C3%AAmica-em-bovinos-e-ovinos); CF e tradução para regra: suposição do projeto a validar | suposicao_a_validar | Magnésio abaixo de 1,2 mg/dL é compatível com tetania. |
| `R-HMG-04` | decubito = sim E extremidades = normal | hipomagnesemia | 0,05 | 10 | Política do projeto: sinal isolado com peso baixo, para o parecer refletir evidência parcial; CF e regra: suposição do projeto a validar | suposicao_a_validar | Decúbito sem extremidades frias, sozinho, é sinal inespecífico. |
| `R-HMG-05` | magnesio_serico ≥ 1,8 | hipomagnesemia | -0,7 | 10 | Referência clínica contextual: [referência](https://www.msdvetmanual.com/pt/metabolic-disorders/dist%C3%BArbios-do-metabolismo-do-magn%C3%A9sio/tetania-hipomagnes%C3%AAmica-em-bovinos-e-ovinos); CF e tradução para regra: suposição do projeto a validar | suposicao_a_validar | Diferencial: magnésio sérico normal torna a hipomagnesemia improvável. |

## Rinotraqueíte Infecciosa Bovina (IBR) — ibr (gravidade media)

| ID | Condições | Conclusão | CF | Prioridade | Fonte | Estado | Nota |
| --- | --- | --- | --- | --- | --- | --- | --- |
| `R-IBR-01` | focinho_avermelhado = sim E secrecao_nasal = sim E queda_producao = sim | ibr | 0,6 | 10 | Referência clínica contextual: [referência](https://www.msdvetmanual.com/pt/respiratory-system/complexo-das-doen%C3%A7as-respirat%C3%B3rias-dos-bovinos/infec%C3%A7%C3%B5es-virais-associadas-ao-complexo-das-doen%C3%A7as-respirat%C3%B3rias-dos-bovinos-em-bovinos); CF e tradução para regra: suposição do projeto a validar | suposicao_a_validar | Focinho vermelho com secreção nasal é o quadro típico da rinotraqueíte. |
| `R-IBR-02` | olhos_lacrimejando = sim E febre = sim | ibr | 0,4 | 10 | Referência clínica contextual: [referência](https://www.msdvetmanual.com/pt/respiratory-system/complexo-das-doen%C3%A7as-respirat%C3%B3rias-dos-bovinos/infec%C3%A7%C3%B5es-virais-associadas-ao-complexo-das-doen%C3%A7as-respirat%C3%B3rias-dos-bovinos-em-bovinos); CF e tradução para regra: suposição do projeto a validar | suposicao_a_validar | Conjuntivite com febre é compatível com BoHV-1. |
| `R-IBR-03` | pcr_bohv1 = sim | ibr | 0,9 | 10 | Referência clínica contextual: [referência](https://www.msdvetmanual.com/pt/respiratory-system/complexo-das-doen%C3%A7as-respirat%C3%B3rias-dos-bovinos/infec%C3%A7%C3%B5es-virais-associadas-ao-complexo-das-doen%C3%A7as-respirat%C3%B3rias-dos-bovinos-em-bovinos); CF e tradução para regra: suposição do projeto a validar | suposicao_a_validar | Detecção de BoHV-1 apoia IBR. |
| `R-IBR-04` | febre = sim E queda_producao = sim | ibr | 0,05 | 10 | Política do projeto: sinal isolado com peso baixo, para o parecer refletir evidência parcial; CF e regra: suposição do projeto a validar | suposicao_a_validar | Febre com queda de produção, sozinhas, são sinais inespecíficos. |
| `R-IBR-05` | ausculta_crepitacoes = sim | ibr | -0,3 | 10 | Referência clínica contextual: [referência](https://www.msdvetmanual.com/pt/respiratory-system/complexo-das-doen%C3%A7as-respirat%C3%B3rias-dos-bovinos/infec%C3%A7%C3%B5es-virais-associadas-ao-complexo-das-doen%C3%A7as-respirat%C3%B3rias-dos-bovinos-em-bovinos); CF e tradução para regra: suposição do projeto a validar | suposicao_a_validar | Diferencial: crepitações pulmonares apontam para pneumonia bacteriana mais do que para IBR. |

## Leptospirose — leptospirose (gravidade alta)

| ID | Condições | Conclusão | CF | Prioridade | Fonte | Estado | Nota |
| --- | --- | --- | --- | --- | --- | --- | --- |
| `R-LEP-01` | aborto_recente = sim E febre = sim | leptospirose | 0,4 | 10 | Referência clínica contextual: [referência](https://www.msdvetmanual.com/pt/infectious-diseases/leptospirose/leptospirose-em-ruminantes); CF e tradução para regra: suposição do projeto a validar | suposicao_a_validar | Aborto com febre é compatível com leptospirose aguda. |
| `R-LEP-02` | leite_com_sangue = sim E queda_producao = sim E leite_alterado = sim | leptospirose | 0,6 | 10 | Referência clínica contextual: [referência](https://www.msdvetmanual.com/pt/infectious-diseases/leptospirose/leptospirose-em-ruminantes); CF e tradução para regra: suposição do projeto a validar | suposicao_a_validar | Leite sanguinolento com queda brusca de produção sugere leptospirose. Só vale com leite alterado: leite com sangue já é leite alterado, e a pergunta não contradiz a triagem. |
| `R-LEP-03` | sorologia_leptospirose_reagente = sim | leptospirose | 0,85 | 10 | Referência clínica contextual: [referência](https://www.msdvetmanual.com/pt/infectious-diseases/leptospirose/leptospirose-em-ruminantes); CF e tradução para regra: suposição do projeto a validar | suposicao_a_validar | Título significativo na soroaglutinação apoia leptospirose. |
| `R-LEP-04` | urina_escura = sim E febre = sim | leptospirose | 0,1 | 10 | Política do projeto: sinal isolado com peso baixo, para o parecer refletir evidência parcial; CF e regra: suposição do projeto a validar | suposicao_a_validar | Urina escura com febre, sozinha, é sinal inespecífico. |
| `R-LEP-05` | esfregaco_hemoparasitas = sim | leptospirose | -0,5 | 10 | Referência clínica contextual: [referência](https://www.msdvetmanual.com/pt/infectious-diseases/leptospirose/leptospirose-em-ruminantes); CF e tradução para regra: suposição do projeto a validar | suposicao_a_validar | Diferencial: hemoparasitas no esfregaço explicam a hemólise por tristeza parasitária. |

## Lipidose Hepática (Fígado Gorduroso) — lipidose_hepatica (gravidade alta)

| ID | Condições | Conclusão | CF | Prioridade | Fonte | Estado | Nota |
| --- | --- | --- | --- | --- | --- | --- | --- |
| `R-LIP-01` | inicio_lactacao = sim E apetite em {reduzido, ausente} E vaca_gorda_no_parto = sim | lipidose_hepatica | 0,55 | 10 | Referência clínica contextual: [referência](https://www.msdvetmanual.com/pt/metabolic-disorders/lipidose-hep%C3%A1tica/doen%C3%A7a-do-f%C3%ADgado-gorduroso-em-bovinos); CF e tradução para regra: suposição do projeto a validar | suposicao_a_validar | Vaca gorda no parto que perde o apetite no início da lactação tem risco alto de fígado gorduroso; costuma vir junto com cetose. |
| `R-LIP-02` | apetite em {reduzido, ausente} E enzimas_hepaticas_elevadas = sim | lipidose_hepatica | 0,8 | 10 | Referência clínica contextual: [referência](https://www.msdvetmanual.com/pt/metabolic-disorders/lipidose-hep%C3%A1tica/doen%C3%A7a-do-f%C3%ADgado-gorduroso-em-bovinos); CF e tradução para regra: suposição do projeto a validar | suposicao_a_validar | Enzimas hepáticas elevadas com apetite reduzido apoiam lipidose hepática; a confirmação é a biópsia hepática. |
| `R-LIP-03` | inicio_lactacao = sim E apetite em {reduzido, ausente} E NÃO (vaca_gorda_no_parto = sim) | lipidose_hepatica | -0,3 | 10 | Referência clínica contextual: [referência](https://www.msdvetmanual.com/pt/metabolic-disorders/lipidose-hep%C3%A1tica/doen%C3%A7a-do-f%C3%ADgado-gorduroso-em-bovinos); CF e tradução para regra: suposição do projeto a validar | suposicao_a_validar | Diferencial: vaca sem excesso de condição corporal no parto tem risco menor de fígado gorduroso. |
| `R-LIP-04` | apetite em {reduzido, ausente} | lipidose_hepatica | 0,05 | 10 | Política do projeto: sinal isolado com peso baixo, para o parecer refletir evidência parcial; CF e regra: suposição do projeto a validar | suposicao_a_validar | Apetite reduzido ou ausente, sozinho, é sinal inespecífico de lipidose hepática. |

## Mastite — mastite (gravidade media)

| ID | Condições | Conclusão | CF | Prioridade | Fonte | Estado | Nota |
| --- | --- | --- | --- | --- | --- | --- | --- |
| `R-MAS-02` | ubere_inflamado = sim | mastite | 0,5 | 10 | Referência clínica contextual: [referência](https://www.msdvetmanual.com/reproductive-system/mastitis-in-large-animals/mastitis-in-cattle); CF e tradução para regra: suposição do projeto a validar | suposicao_a_validar | Edema, calor ou dor no úbere sustentam inflamação mamária; não identificam isoladamente o agente causal. |
| `R-MAS-04` | cmt_reagente = sim | mastite | 0,4 | 10 | Referência clínica contextual: [referência](https://www.msdvetmanual.com/reproductive-system/mastitis-in-large-animals/mastitis-in-cattle); CF e tradução para regra: suposição do projeto a validar | suposicao_a_validar | CMT reagente indica aumento de células somáticas e sustenta inflamação; não diferencia sozinho mastite clínica de subclínica. |
| `R-MAS-05` | evidencia_alteracao_leite = sim | mastite | 0,99 | 10 | Referência clínica contextual: [referência](https://www.msdvetmanual.com/reproductive-system/mastitis-in-large-animals/mastitis-in-cattle); CF e tradução para regra: suposição do projeto a validar | suposicao_a_validar | Propaga a maior evidência de alteração do leite sem somar novamente o resultado da caneca. A multiplicação por 0,99 evita peso unitário fora do contrato. |

## Metrite Puerperal — metrite (gravidade alta)

| ID | Condições | Conclusão | CF | Prioridade | Fonte | Estado | Nota |
| --- | --- | --- | --- | --- | --- | --- | --- |
| `R-MET-01` | puerperio = sim E corrimento_fetido = sim E corrimento_vaginal = sim | metrite | 0,75 | 10 | Referência clínica contextual: [referência](https://www.msdvetmanual.com/reproductive-system/uterine-diseases-in-production-animals/metritis-in-production-animals); CF e tradução para regra: suposição do projeto a validar | suposicao_a_validar | Corrimento fétido no puerpério sustenta a hipótese de metrite; não estabelece sozinho toxemia. Só vale com corrimento observado: sem corrimento, o cheiro da secreção não é perguntado. |
| `R-MET-02` | corrimento_vaginal = sim E puerperio = sim E febre = sim | metrite | 0,45 | 10 | Referência clínica contextual: [referência](https://www.msdvetmanual.com/reproductive-system/uterine-diseases-in-production-animals/metritis-in-production-animals); CF e tradução para regra: suposição do projeto a validar | suposicao_a_validar | Corrimento inespecífico somado a febre no puerpério sugere complicação infecciosa uterina. |
| `R-MET-03` | puerperio = sim E utero_aumentado_palpacao = sim E corrimento_vaginal = sim | metrite | 0,35 | 10 | Referência clínica contextual: [referência](https://www.msdvetmanual.com/reproductive-system/uterine-diseases-in-production-animals/metritis-in-production-animals); CF e tradução para regra: suposição do projeto a validar | suposicao_a_validar | Aumento uterino no puerpério recebe apoio apenas quando há corrimento vaginal anormal; tamanho isolado não confirma infecção. |
| `R-MET-04` | historico_retencao_placenta = sim E puerperio = sim | metrite | 0,25 | 10 | Referência clínica contextual: [referência](https://www.msdvetmanual.com/reproductive-system/uterine-diseases-in-production-animals/metritis-in-production-animals); CF e tradução para regra: suposição do projeto a validar | suposicao_a_validar | Retenção de membranas fetais é fator de risco epidemiológico para infecção ascendente. |

## Pneumonia — pneumonia (gravidade media)

| ID | Condições | Conclusão | CF | Prioridade | Fonte | Estado | Nota |
| --- | --- | --- | --- | --- | --- | --- | --- |
| `R-PNE-01` | tosse = sim E apetite em {reduzido, ausente} | pneumonia | 0,45 | 10 | Referência clínica contextual: [referência](https://www.msdvetmanual.com/pt/respiratory-system/complexo-das-doen%C3%A7as-respirat%C3%B3rias-dos-bovinos/vis%C3%A3o-geral-sobre-o-complexo-das-doen%C3%A7as-respirat%C3%B3rias-dos-bovinos); CF e tradução para regra: suposição do projeto a validar | suposicao_a_validar | Tosse com queda de apetite sugere doença respiratória com comprometimento geral. Exige apetite reduzido ou ausente na triagem para a pergunta só ser feita quando há sinal compatível, poupando o limite de perguntas do produtor (concessão de seleção; suposição a validar). |
| `R-PNE-02` | respiracao_ofegante = sim E apetite em {reduzido, ausente} | pneumonia | 0,4 | 10 | Referência clínica contextual: [referência](https://www.msdvetmanual.com/pt/respiratory-system/complexo-das-doen%C3%A7as-respirat%C3%B3rias-dos-bovinos/vis%C3%A3o-geral-sobre-o-complexo-das-doen%C3%A7as-respirat%C3%B3rias-dos-bovinos); CF e tradução para regra: suposição do projeto a validar | suposicao_a_validar | Respiração com esforço apoia doença respiratória do trato inferior. Exige apetite reduzido ou ausente na triagem para a pergunta só ser feita quando há sinal compatível, poupando o limite de perguntas do produtor (concessão de seleção; suposição a validar). |
| `R-PNE-03` | ausculta_crepitacoes = sim | pneumonia | 0,8 | 10 | Referência clínica contextual: [referência](https://www.msdvetmanual.com/pt/respiratory-system/complexo-das-doen%C3%A7as-respirat%C3%B3rias-dos-bovinos/vis%C3%A3o-geral-sobre-o-complexo-das-doen%C3%A7as-respirat%C3%B3rias-dos-bovinos); CF e tradução para regra: suposição do projeto a validar | suposicao_a_validar | Crepitações cranioventrais à auscultação apoiam broncopneumonia. |
| `R-PNE-04` | secrecao_nasal = sim E apetite em {reduzido, ausente} | pneumonia | 0,3 | 10 | Referência clínica contextual: [referência](https://www.msdvetmanual.com/pt/respiratory-system/complexo-das-doen%C3%A7as-respirat%C3%B3rias-dos-bovinos/vis%C3%A3o-geral-sobre-o-complexo-das-doen%C3%A7as-respirat%C3%B3rias-dos-bovinos); CF e tradução para regra: suposição do projeto a validar | suposicao_a_validar | Secreção nasal é compatível com doença respiratória bovina, mas não localiza o pulmão. Exige apetite reduzido ou ausente na triagem para a pergunta só ser feita quando há sinal compatível, poupando o limite de perguntas do produtor (concessão de seleção; suposição a validar). |
| `R-PNE-05` | febre = sim E apatia = sim | pneumonia | 0,1 | 10 | Política do projeto: sinal isolado com peso baixo, para o parecer refletir evidência parcial; CF e regra: suposição do projeto a validar | suposicao_a_validar | Febre com abatimento, sozinha, é sinal inespecífico. |
| `R-PNE-06` | distensao_flanco_esquerdo = sim E apetite em {reduzido, ausente} | pneumonia | -0,3 | 10 | Referência clínica contextual: [referência](https://www.msdvetmanual.com/pt/respiratory-system/complexo-das-doen%C3%A7as-respirat%C3%B3rias-dos-bovinos/vis%C3%A3o-geral-sobre-o-complexo-das-doen%C3%A7as-respirat%C3%B3rias-dos-bovinos); CF e tradução para regra: suposição do projeto a validar | suposicao_a_validar | Diferencial: barriga estufada sugere que a dificuldade respiratória vem da compressão pelo rúmen, não do pulmão. Exige apetite reduzido ou ausente na triagem para a pergunta só ser feita quando há sinal compatível, poupando o limite de perguntas do produtor (concessão de seleção; suposição a validar). |

## Retenção de Placenta — retencao_placenta (gravidade media)

| ID | Condições | Conclusão | CF | Prioridade | Fonte | Estado | Nota |
| --- | --- | --- | --- | --- | --- | --- | --- |
| `R-RPL-01` | puerperio = sim E membranas_expostas_vulva = sim | retencao_placenta | 0,8 | 10 | Referência clínica contextual: [referência](https://www.msdvetmanual.com/pt/reproductive-system/reten%C3%A7%C3%A3o-de-membranas-fetais-em-animais-de-grande-porte-placenta-retida/reten%C3%A7%C3%A3o-de-membranas-fetais-em-vacas); CF e tradução para regra: suposição do projeto a validar | suposicao_a_validar | Restos de placenta visíveis na vulva no pós-parto indicam retenção de membranas fetais. |
| `R-RPL-02` | puerperio = sim E placenta_nao_expulsa_24h = sim | retencao_placenta | 0,7 | 10 | Referência clínica contextual: [referência](https://www.msdvetmanual.com/pt/reproductive-system/reten%C3%A7%C3%A3o-de-membranas-fetais-em-animais-de-grande-porte-placenta-retida/reten%C3%A7%C3%A3o-de-membranas-fetais-em-vacas); CF e tradução para regra: suposição do projeto a validar | suposicao_a_validar | Falha na expulsão da placenta em até 24 horas define a retenção de membranas fetais. |
| `R-RPL-03` | palpacao_membranas_retidas = sim | retencao_placenta | 0,9 | 10 | Referência clínica contextual: [referência](https://www.msdvetmanual.com/pt/reproductive-system/reten%C3%A7%C3%A3o-de-membranas-fetais-em-animais-de-grande-porte-placenta-retida/reten%C3%A7%C3%A3o-de-membranas-fetais-em-vacas); CF e tradução para regra: suposição do projeto a validar | suposicao_a_validar | Membranas retidas ao exame confirmam a suspeita de retenção. |
| `R-RPL-04` | historico_retencao_placenta = sim E puerperio = sim | retencao_placenta | 0,35 | 10 | Referência clínica contextual: [referência](https://www.msdvetmanual.com/pt/reproductive-system/reten%C3%A7%C3%A3o-de-membranas-fetais-em-animais-de-grande-porte-placenta-retida/reten%C3%A7%C3%A3o-de-membranas-fetais-em-vacas); CF e tradução para regra: suposição do projeto a validar | suposicao_a_validar | Retenção registrada na ficha neste parto apoia a hipótese no puerpério. Peso reduzido para 0,35 (concessão): com 0,5 a retenção chegava ao limiar de exclusão antes de se perguntar o corrimento fétido e a metrite era descartada cedo demais. |
| `R-RPL-05` | corrimento_vaginal = sim E puerperio = sim | retencao_placenta | 0,1 | 10 | Política do projeto: sinal isolado com peso baixo, para o parecer refletir evidência parcial; CF e regra: suposição do projeto a validar | suposicao_a_validar | Corrimento vaginal no puerpério, sozinho, é sinal inespecífico. |
| `R-RPL-06` | dias_em_lactacao > 7 | retencao_placenta | -0,5 | 10 | Referência clínica contextual: [referência](https://www.msdvetmanual.com/pt/reproductive-system/reten%C3%A7%C3%A3o-de-membranas-fetais-em-animais-de-grande-porte-placenta-retida/reten%C3%A7%C3%A3o-de-membranas-fetais-em-vacas); CF e tradução para regra: suposição do projeto a validar | suposicao_a_validar | Diferencial: depois da primeira semana pós-parto, o quadro uterino tende a ser metrite, não retenção recente. |

## Reticulopericardite Traumática — reticulopericardite_traumatica (gravidade alta)

| ID | Condições | Conclusão | CF | Prioridade | Fonte | Estado | Nota |
| --- | --- | --- | --- | --- | --- | --- | --- |
| `R-RPT-01` | costas_arqueadas = sim E gemido = sim E apetite em {reduzido, ausente} | reticulopericardite_traumatica | 0,7 | 10 | Referência clínica contextual: [referência](https://www.msdvetmanual.com/pt/digestive-system/doen%C3%A7as-do-pr%C3%A9-est%C3%B4mago-em-ruminantes/reticuloperitonite-traum%C3%A1tica-em-bovinos); CF e tradução para regra: suposição do projeto a validar | suposicao_a_validar | Dorso arqueado com gemido sugere dor cranial do abdome por corpo estranho. Exige apetite reduzido ou ausente na triagem para a pergunta só ser feita quando há sinal compatível, poupando o limite de perguntas do produtor (concessão de seleção; suposição a validar). |
| `R-RPT-03` | prova_dor_reticular = sim | reticulopericardite_traumatica | 0,85 | 10 | Referência clínica contextual: [referência](https://www.msdvetmanual.com/pt/digestive-system/doen%C3%A7as-do-pr%C3%A9-est%C3%B4mago-em-ruminantes/reticuloperitonite-traum%C3%A1tica-em-bovinos); CF e tradução para regra: suposição do projeto a validar | suposicao_a_validar | Prova de dor reticular positiva apoia reticuloperitonite traumática. |
| `R-RPT-04` | edema_barbela = sim E febre = sim | reticulopericardite_traumatica | 0,6 | 10 | Referência clínica contextual: [referência](https://www.msdvetmanual.com/pt/digestive-system/doen%C3%A7as-do-pr%C3%A9-est%C3%B4mago-em-ruminantes/reticuloperitonite-traum%C3%A1tica-em-bovinos); CF e tradução para regra: suposição do projeto a validar | suposicao_a_validar | Edema de barbela com febre sugere extensão ao pericárdio. |
| `R-RPT-05` | apetite em {reduzido, ausente} E queda_producao = sim E febre = sim | reticulopericardite_traumatica | 0,1 | 10 | Política do projeto: sinal isolado com peso baixo, para o parecer refletir evidência parcial; CF e regra: suposição do projeto a validar | suposicao_a_validar | Apetite e produção em queda com febre, sozinhos, são sinais inespecíficos. |
| `R-RPT-06` | ping_metalico_flanco_esquerdo = sim | reticulopericardite_traumatica | -0,4 | 10 | Referência clínica contextual: [referência](https://www.msdvetmanual.com/pt/digestive-system/doen%C3%A7as-do-pr%C3%A9-est%C3%B4mago-em-ruminantes/reticuloperitonite-traum%C3%A1tica-em-bovinos); CF e tradução para regra: suposição do projeto a validar | suposicao_a_validar | Diferencial: ping no flanco esquerdo aponta para deslocamento de abomaso como causa da dor. |

## Timpanismo Espumoso — timpanismo_espumoso (gravidade alta)

| ID | Condições | Conclusão | CF | Prioridade | Fonte | Estado | Nota |
| --- | --- | --- | --- | --- | --- | --- | --- |
| `R-TES-01` | distensao_flanco_esquerdo = sim E pasto_leguminosa_recente = sim E apetite em {reduzido, ausente} | timpanismo_espumoso | 0,7 | 10 | Referência clínica contextual: [referência](https://www.msdvetmanual.com/pt/digestive-system/doen%C3%A7as-do-pr%C3%A9-est%C3%B4mago-em-ruminantes/timpanismo-em-ruminantes); CF e tradução para regra: suposição do projeto a validar | suposicao_a_validar | Distensão esquerda após leguminosa ou pasto tenro é o quadro típico do timpanismo espumoso. Exige apetite reduzido ou ausente na triagem para a pergunta só ser feita quando há sinal compatível, poupando o limite de perguntas do produtor (concessão de seleção; suposição a validar). |
| `R-TES-02` | outros_animais_estufados = sim E apetite em {reduzido, ausente} | timpanismo_espumoso | 0,3 | 10 | Referência clínica contextual: [referência](https://www.msdvetmanual.com/pt/digestive-system/doen%C3%A7as-do-pr%C3%A9-est%C3%B4mago-em-ruminantes/timpanismo-em-ruminantes); CF e tradução para regra: suposição do projeto a validar | suposicao_a_validar | Vários animais estufados ao mesmo tempo sugerem causa alimentar comum. Exige apetite reduzido ou ausente na triagem para a pergunta só ser feita quando há sinal compatível, poupando o limite de perguntas do produtor (concessão de seleção; suposição a validar). |
| `R-TES-03` | espuma_sonda = sim | timpanismo_espumoso | 0,9 | 10 | Referência clínica contextual: [referência](https://www.msdvetmanual.com/pt/digestive-system/doen%C3%A7as-do-pr%C3%A9-est%C3%B4mago-em-ruminantes/timpanismo-em-ruminantes); CF e tradução para regra: suposição do projeto a validar | suposicao_a_validar | Conteúdo espumoso pela sonda sem alívio caracteriza o gás preso em espuma. |
| `R-TES-04` | apetite = ausente E queda_producao = sim | timpanismo_espumoso | 0,05 | 10 | Política do projeto: sinal isolado com peso baixo, para o parecer refletir evidência parcial; CF e regra: suposição do projeto a validar | suposicao_a_validar | Apetite ausente com queda de produção, sozinho, é sinal inespecífico. |
| `R-TES-05` | gas_livre_sonda = sim | timpanismo_espumoso | -0,7 | 10 | Referência clínica contextual: [referência](https://www.msdvetmanual.com/pt/digestive-system/doen%C3%A7as-do-pr%C3%A9-est%C3%B4mago-em-ruminantes/timpanismo-em-ruminantes); CF e tradução para regra: suposição do projeto a validar | suposicao_a_validar | Diferencial: gás livre que sai pela sonda indica timpanismo gasoso, não espumoso. |

## Timpanismo Gasoso — timpanismo_gasoso (gravidade alta)

| ID | Condições | Conclusão | CF | Prioridade | Fonte | Estado | Nota |
| --- | --- | --- | --- | --- | --- | --- | --- |
| `R-TGA-01` | distensao_flanco_esquerdo = sim E engasgo = sim E apetite em {reduzido, ausente} | timpanismo_gasoso | 0,6 | 10 | Referência clínica contextual: [referência](https://www.msdvetmanual.com/pt/digestive-system/doen%C3%A7as-do-pr%C3%A9-est%C3%B4mago-em-ruminantes/timpanismo-em-ruminantes); CF e tradução para regra: suposição do projeto a validar | suposicao_a_validar | Distensão esquerda com sinais de engasgo sugere gás livre retido por obstrução esofágica. Exige apetite reduzido ou ausente na triagem para a pergunta só ser feita quando há sinal compatível, poupando o limite de perguntas do produtor (concessão de seleção; suposição a validar). |
| `R-TGA-03` | gas_livre_sonda = sim | timpanismo_gasoso | 0,9 | 10 | Referência clínica contextual: [referência](https://www.msdvetmanual.com/pt/digestive-system/doen%C3%A7as-do-pr%C3%A9-est%C3%B4mago-em-ruminantes/timpanismo-em-ruminantes); CF e tradução para regra: suposição do projeto a validar | suposicao_a_validar | Gás livre pela sonda com alívio da distensão caracteriza o timpanismo gasoso. |
| `R-TGA-04` | apetite = ausente E apatia = sim | timpanismo_gasoso | 0,05 | 10 | Política do projeto: sinal isolado com peso baixo, para o parecer refletir evidência parcial; CF e regra: suposição do projeto a validar | suposicao_a_validar | Apetite ausente com abatimento, sozinho, é sinal inespecífico. |
| `R-TGA-05` | espuma_sonda = sim | timpanismo_gasoso | -0,7 | 10 | Referência clínica contextual: [referência](https://www.msdvetmanual.com/pt/digestive-system/doen%C3%A7as-do-pr%C3%A9-est%C3%B4mago-em-ruminantes/timpanismo-em-ruminantes); CF e tradução para regra: suposição do projeto a validar | suposicao_a_validar | Diferencial: conteúdo espumoso pela sonda indica timpanismo espumoso, não gasoso. |

## Tristeza Parasitária Bovina — tpb (gravidade alta)

| ID | Condições | Conclusão | CF | Prioridade | Fonte | Estado | Nota |
| --- | --- | --- | --- | --- | --- | --- | --- |
| `R-TPB-01` | febre = sim E urina_escura = sim | tpb | 0,7 | 10 | Referência clínica contextual: [referência](https://www.msdvetmanual.com/circulatory-system/blood-parasites/anaplasmosis-in-ruminants); CF e tradução para regra: suposição do projeto a validar; [referência](https://www.msdvetmanual.com/circulatory-system/blood-parasites/babesiosis-in-animals) | suposicao_a_validar | Combinação de febre aguda e hemoglobinúria por hemólise intravascular típica de babesiose. |
| `R-TPB-02` | mucosas_palidas_ou_ictericas = sim | tpb | 0,6 | 10 | Referência clínica contextual: [referência](https://www.msdvetmanual.com/circulatory-system/blood-parasites/anaplasmosis-in-ruminants); CF e tradução para regra: suposição do projeto a validar | suposicao_a_validar | Palidez ou icterícia mantêm TPB entre as hipóteses mesmo sem febre na medição atual; não identificam a causa da anemia ou icterícia. |
| `R-TPB-03` | carrapatos_historico_recente = sim E febre = sim | tpb | 0,35 | 10 | Referência clínica contextual: [referência](https://www.msdvetmanual.com/circulatory-system/blood-parasites/anaplasmosis-in-ruminants); CF e tradução para regra: suposição do projeto a validar; [referência](https://www.msdvetmanual.com/circulatory-system/blood-parasites/babesiosis-in-animals) | suposicao_a_validar | Exposição ao vetor carrapato combinada com febre é indicativo epidemiológico inicial. |
| `R-TPB-04` | esfregaco_hemoparasitas = sim | tpb | 0,9 | 10 | Referência clínica contextual: [referência](https://www.msdvetmanual.com/circulatory-system/blood-parasites/anaplasmosis-in-ruminants); CF e tradução para regra: suposição do projeto a validar; [referência](https://www.msdvetmanual.com/circulatory-system/blood-parasites/babesiosis-in-animals) | suposicao_a_validar | Esfregaço compatível sustenta infecção por hemoparasitas, mesmo sem febre atual; não distingue sozinho doença ativa de estado de portador. |

## Tuberculose — tuberculose (gravidade alta)

| ID | Condições | Conclusão | CF | Prioridade | Fonte | Estado | Nota |
| --- | --- | --- | --- | --- | --- | --- | --- |
| `R-TUB-01` | emagrecimento_progressivo = sim E tosse = sim E queda_producao = sim E apetite em {normal, reduzido} | tuberculose | 0,5 | 10 | Referência clínica contextual: [referência](https://www.msdvetmanual.com/pt/generalized-conditions/vis%C3%A3o-geral-da-tuberculose-em-animais/vis%C3%A3o-geral-da-tuberculose-em-animais); CF e tradução para regra: suposição do projeto a validar | suposicao_a_validar | Emagrecimento progressivo com tosse, em vaca com queda de produção, é compatível com tuberculose. Só vale quando a vaca ainda come: "emagrece mesmo comendo" não se aplica a apetite ausente. |
| `R-TUB-02` | linfonodos_aumentados = sim E queda_producao = sim | tuberculose | 0,4 | 10 | Referência clínica contextual: [referência](https://www.msdvetmanual.com/pt/generalized-conditions/vis%C3%A3o-geral-da-tuberculose-em-animais/vis%C3%A3o-geral-da-tuberculose-em-animais); CF e tradução para regra: suposição do projeto a validar | suposicao_a_validar | Linfonodos superficiais aumentados apoiam tuberculose. |
| `R-TUB-03` | tuberculina_reagente = sim | tuberculose | 0,9 | 10 | Referência clínica contextual: [referência](https://www.msdvetmanual.com/pt/generalized-conditions/vis%C3%A3o-geral-da-tuberculose-em-animais/vis%C3%A3o-geral-da-tuberculose-em-animais); CF e tradução para regra: suposição do projeto a validar | suposicao_a_validar | Tuberculinização reagente apoia tuberculose; a confirmação segue o regulamento do PNCEBT. |
| `R-TUB-04` | apetite = normal E queda_producao = sim | tuberculose | 0,05 | 10 | Política do projeto: sinal isolado com peso baixo, para o parecer refletir evidência parcial; CF e regra: suposição do projeto a validar | suposicao_a_validar | Queda de produção com apetite normal, sozinha, é sinal inespecífico. |
| `R-TUB-05` | febre = sim | tuberculose | -0,3 | 10 | Referência clínica contextual: [referência](https://www.msdvetmanual.com/pt/generalized-conditions/vis%C3%A3o-geral-da-tuberculose-em-animais/vis%C3%A3o-geral-da-tuberculose-em-animais); CF e tradução para regra: suposição do projeto a validar | suposicao_a_validar | Diferencial: febre aguda sugere outra causa; a tuberculose costuma ser crônica e sem febre alta. |

## Úlcera de Sola / Doença da Linha Branca — ulcera_sola (gravidade media)

| ID | Condições | Conclusão | CF | Prioridade | Fonte | Estado | Nota |
| --- | --- | --- | --- | --- | --- | --- | --- |
| `R-ULC-01` | claudicacao = sim E mancar_pata_traseira_sem_inchaco = sim | ulcera_sola | 0,55 | 10 | Referência clínica contextual: [referência](https://www.msdvetmanual.com/pt/musculoskeletal-system/claudica%C3%A7%C3%A3o-em-bovinos/claudica%C3%A7%C3%A3o-com-origem-no-casco-em-bovinos); CF e tradução para regra: suposição do projeto a validar | suposicao_a_validar | Manqueira de pata traseira sem inchaço do pé é o quadro típico de lesão de sola ou da linha branca; não substitui o exame do casco. |
| `R-ULC-02` | claudicacao = sim E lesao_sola_pinca_dor = sim | ulcera_sola | 0,85 | 10 | Referência clínica contextual: [referência](https://www.msdvetmanual.com/pt/musculoskeletal-system/claudica%C3%A7%C3%A3o-em-bovinos/claudica%C3%A7%C3%A3o-com-origem-no-casco-em-bovinos); CF e tradução para regra: suposição do projeto a validar | suposicao_a_validar | Dor à pinça localizada na sola ou na linha branca, com lesão após o casqueamento, sustenta úlcera de sola ou doença da linha branca. |
| `R-ULC-03` | claudicacao = sim E lesao_erosiva_talao_morango = sim | ulcera_sola | -0,3 | 10 | Referência clínica contextual: [referência](https://www.msdvetmanual.com/pt/musculoskeletal-system/claudica%C3%A7%C3%A3o-em-bovinos/claudica%C3%A7%C3%A3o-com-origem-no-casco-em-bovinos); CF e tradução para regra: suposição do projeto a validar | suposicao_a_validar | Diferencial: lesão em morango no talão aponta para dermatite digital; não exclui lesão de sola em outra unha. |
| `R-ULC-04` | claudicacao = sim E inchaco_entre_unhas_mau_cheiro = sim | ulcera_sola | -0,4 | 10 | Referência clínica contextual: [referência](https://www.msdvetmanual.com/pt/musculoskeletal-system/claudica%C3%A7%C3%A3o-em-bovinos/claudica%C3%A7%C3%A3o-com-origem-no-casco-em-bovinos); CF e tradução para regra: suposição do projeto a validar | suposicao_a_validar | Diferencial: inchaço entre as unhas com mau cheiro aponta para flegmão interdigital, não para lesão de sola. |
| `R-ULC-05` | claudicacao = sim | ulcera_sola | 0,05 | 10 | Política do projeto: sinal isolado com peso baixo, para o parecer refletir evidência parcial; CF e regra: suposição do projeto a validar | suposicao_a_validar | Claudicação, sozinha, é sinal inespecífico de úlcera de sola. |

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
| `R-URG-03` | deslocamento_abomaso_esquerda = sim [CF ≥ 0,5] | chamar_agora | 0,99 | 50 | Política de triagem do projeto, Seções 1 e 3; suposição a validar | suposicao_a_validar | Aplica a política de gravidade do projeto quando o CF de deslocamento_abomaso_esquerda é pelo menos 0,50. Não prescreve tratamento nem estabelece diagnóstico definitivo. |
| `R-URG-04` | metrite = sim [CF ≥ 0,5] | chamar_agora | 0,99 | 50 | Política de triagem do projeto, Seções 1 e 3; suposição a validar | suposicao_a_validar | Aplica a política de gravidade do projeto quando o CF de metrite é pelo menos 0,50. Não prescreve tratamento nem estabelece diagnóstico definitivo. |
| `R-URG-05` | mastite = sim [CF ≥ 0,5] | observar | 0,8 | 50 | Política de triagem do projeto, Seções 1 e 3; suposição a validar | suposicao_a_validar | Aplica a política de gravidade do projeto quando o CF de mastite é pelo menos 0,50. Não prescreve tratamento nem estabelece diagnóstico definitivo. |
| `R-URG-06` | cetose = sim [CF ≥ 0,5] | observar | 0,8 | 50 | Política de triagem do projeto, Seções 1 e 3; suposição a validar | suposicao_a_validar | Aplica a política de gravidade do projeto quando o CF de cetose é pelo menos 0,50. Não prescreve tratamento nem estabelece diagnóstico definitivo. |
| `R-URG-07` | acidose = sim [CF ≥ 0,5] | observar | 0,8 | 50 | Política de triagem do projeto, Seções 1 e 3; suposição a validar | suposicao_a_validar | Aplica a política de gravidade do projeto quando o CF de acidose é pelo menos 0,50. Não prescreve tratamento nem estabelece diagnóstico definitivo. |
| `R-URG-08` | dermatite_digital = sim [CF ≥ 0,5] | observar | 0,7 | 50 | Política de triagem do projeto, Seções 1 e 3; suposição a validar | suposicao_a_validar | Aplica a política de gravidade do projeto quando o CF de dermatite_digital é pelo menos 0,50. Não prescreve tratamento nem estabelece diagnóstico definitivo. |
| `R-URG-09` | deslocamento_abomaso_direita = sim [CF ≥ 0,5] | chamar_agora | 0,99 | 50 | Política de triagem do projeto, Seções 1 e 3; suposição a validar | suposicao_a_validar | Aplica a política de gravidade do projeto quando o CF de deslocamento_abomaso_direita é pelo menos 0,50. Não prescreve tratamento nem estabelece diagnóstico definitivo. |
| `R-URG-10` | timpanismo_espumoso = sim [CF ≥ 0,5] | chamar_agora | 0,99 | 50 | Política de triagem do projeto, Seções 1 e 3; suposição a validar | suposicao_a_validar | Aplica a política de gravidade do projeto quando o CF de timpanismo_espumoso é pelo menos 0,50. Não prescreve tratamento nem estabelece diagnóstico definitivo. |
| `R-URG-11` | timpanismo_gasoso = sim [CF ≥ 0,5] | chamar_agora | 0,99 | 50 | Política de triagem do projeto, Seções 1 e 3; suposição a validar | suposicao_a_validar | Aplica a política de gravidade do projeto quando o CF de timpanismo_gasoso é pelo menos 0,50. Não prescreve tratamento nem estabelece diagnóstico definitivo. |
| `R-URG-12` | retencao_placenta = sim [CF ≥ 0,5] | observar | 0,8 | 50 | Política de triagem do projeto, Seções 1 e 3; suposição a validar | suposicao_a_validar | Aplica a política de gravidade do projeto quando o CF de retencao_placenta é pelo menos 0,50. Não prescreve tratamento nem estabelece diagnóstico definitivo. |
| `R-URG-13` | pneumonia = sim [CF ≥ 0,5] | observar | 0,8 | 50 | Política de triagem do projeto, Seções 1 e 3; suposição a validar | suposicao_a_validar | Aplica a política de gravidade do projeto quando o CF de pneumonia é pelo menos 0,50. Não prescreve tratamento nem estabelece diagnóstico definitivo. |
| `R-URG-14` | reticulopericardite_traumatica = sim [CF ≥ 0,5] | chamar_agora | 0,99 | 50 | Política de triagem do projeto, Seções 1 e 3; suposição a validar | suposicao_a_validar | Aplica a política de gravidade do projeto quando o CF de reticulopericardite_traumatica é pelo menos 0,50. Não prescreve tratamento nem estabelece diagnóstico definitivo. |
| `R-URG-15` | hipomagnesemia = sim [CF ≥ 0,5] | chamar_agora | 0,99 | 50 | Política de triagem do projeto, Seções 1 e 3; suposição a validar | suposicao_a_validar | Aplica a política de gravidade do projeto quando o CF de hipomagnesemia é pelo menos 0,50. Não prescreve tratamento nem estabelece diagnóstico definitivo. |
| `R-URG-16` | brucelose = sim [CF ≥ 0,5] | chamar_agora | 0,99 | 50 | Política de triagem do projeto, Seções 1 e 3; suposição a validar | suposicao_a_validar | Aplica a política de gravidade do projeto quando o CF de brucelose é pelo menos 0,50. Doença de notificação obrigatória (PNCEBT, MAPA). Não prescreve tratamento nem estabelece diagnóstico definitivo. |
| `R-URG-17` | leptospirose = sim [CF ≥ 0,5] | chamar_agora | 0,99 | 50 | Política de triagem do projeto, Seções 1 e 3; suposição a validar | suposicao_a_validar | Aplica a política de gravidade do projeto quando o CF de leptospirose é pelo menos 0,50. Não prescreve tratamento nem estabelece diagnóstico definitivo. |
| `R-URG-18` | ibr = sim [CF ≥ 0,5] | observar | 0,8 | 50 | Política de triagem do projeto, Seções 1 e 3; suposição a validar | suposicao_a_validar | Aplica a política de gravidade do projeto quando o CF de ibr é pelo menos 0,50. Não prescreve tratamento nem estabelece diagnóstico definitivo. |
| `R-URG-19` | bvd = sim [CF ≥ 0,5] | chamar_agora | 0,99 | 50 | Política de triagem do projeto, Seções 1 e 3; suposição a validar | suposicao_a_validar | Aplica a política de gravidade do projeto quando o CF de bvd é pelo menos 0,50. Não prescreve tratamento nem estabelece diagnóstico definitivo. |
| `R-URG-20` | tuberculose = sim [CF ≥ 0,5] | chamar_agora | 0,99 | 50 | Política de triagem do projeto, Seções 1 e 3; suposição a validar | suposicao_a_validar | Aplica a política de gravidade do projeto quando o CF de tuberculose é pelo menos 0,50. Doença de notificação obrigatória (PNCEBT, MAPA). Não prescreve tratamento nem estabelece diagnóstico definitivo. |
| `R-URG-21` | ulcera_sola = sim [CF ≥ 0,5] | observar | 0,7 | 50 | Política de triagem do projeto, Seções 1 e 3; suposição a validar | suposicao_a_validar | Aplica a política de gravidade do projeto quando o CF de ulcera_sola é pelo menos 0,50. Não prescreve tratamento nem estabelece diagnóstico definitivo. |
| `R-URG-22` | flegmao_interdigital = sim [CF ≥ 0,5] | observar | 0,8 | 50 | Política de triagem do projeto, Seções 1 e 3; suposição a validar | suposicao_a_validar | Aplica a política de gravidade do projeto quando o CF de flegmao_interdigital é pelo menos 0,50. Não prescreve tratamento nem estabelece diagnóstico definitivo. |
| `R-URG-23` | endometrite = sim [CF ≥ 0,5] | observar | 0,7 | 50 | Política de triagem do projeto, Seções 1 e 3; suposição a validar | suposicao_a_validar | Aplica a política de gravidade do projeto quando o CF de endometrite é pelo menos 0,50. Não prescreve tratamento nem estabelece diagnóstico definitivo. |
| `R-URG-24` | cisto_ovariano = sim [CF ≥ 0,5] | observar | 0,6 | 50 | Política de triagem do projeto, Seções 1 e 3; suposição a validar | suposicao_a_validar | Aplica a política de gravidade do projeto quando o CF de cisto_ovariano é pelo menos 0,50. Não prescreve tratamento nem estabelece diagnóstico definitivo. |
| `R-URG-25` | lipidose_hepatica = sim [CF ≥ 0,5] | chamar_agora | 0,99 | 50 | Política de triagem do projeto, Seções 1 e 3; suposição a validar | suposicao_a_validar | Aplica a política de gravidade do projeto quando o CF de lipidose_hepatica é pelo menos 0,50. Não prescreve tratamento nem estabelece diagnóstico definitivo. |

## Símbolos

| ID | Nome | Tipo | Domínio | Pergunta: produtor | Pergunta: veterinário | Gravidade | Combinação |
| --- | --- | --- | --- | --- | --- | --- | --- |
| aborto_recente | Aborto recente | pergunta | tipo: booleano | A vaca abortou nesta gestação ou nos últimos meses? | Aborto recente, sobretudo no terço final da gestação? | — | mycin |
| acidose | Acidose Ruminal | doenca | tipo: booleano | — | — | media | mycin |
| agitacao | Agitação ou reação exagerada | pergunta | tipo: booleano | A vaca está agitada, cambaleando ou se assusta demais com barulho e toque? | Hiperexcitabilidade, ataxia ou hiperestesia? | — | mycin |
| antigeno_bvdv | BVDV detectado | pergunta | tipo: booleano | — | ELISA de antígeno ou PCR para BVDV positivo? | — | mycin |
| apatia | Apatia | pergunta | tipo: booleano | A vaca está abatida ou pouco responsiva? | Animal apático ou com resposta reduzida ao ambiente? | — | mycin |
| apetite | Apetite | pergunta | tipo: categorico, valores: {normal, reduzido, ausente} | Como está o apetite: normal, reduzido ou ausente? | Apetite normal, reduzido ou ausente? | — | mycin |
| ausculta_crepitacoes | Crepitações à auscultação pulmonar | pergunta | tipo: booleano | — | Crepitações ou sibilos à auscultação pulmonar, sobretudo na região cranioventral? | — | mycin |
| bhb_sanguineo | BHB sanguíneo | pergunta | casas_decimais: 2, max: 20, min: 0, tipo: numerico, unidade: mmol/L | — | Qual é a concentração sanguínea de BHB, em mmol/L? | — | mycin |
| brucelose | Brucelose | doenca | tipo: booleano | — | — | alta | mycin |
| bvd | Diarreia Viral Bovina (BVD) | doenca | tipo: booleano | — | — | alta | mycin |
| calcio_serico | Cálcio sérico total | pergunta | casas_decimais: 2, max: 20, min: 0, tipo: numerico, unidade: mmol/L | — | Qual é o cálcio sérico total, em mmol/L? | — | mycin |
| carrapatos_historico_recente | Exposição recente a carrapatos | pergunta | tipo: booleano | Foram vistos carrapatos na vaca recentemente? | Histórico recente de exposição a carrapatos? | — | mycin |
| cetose | Cetose / Hipercetonemia | doenca | tipo: booleano | — | — | media | mycin |
| chamar_agora | Atendimento Veterinário Imediato | urgencia | tipo: booleano | — | — | — | mycin |
| cio_irregular_ou_constante | Cio irregular ou constante | pergunta | tipo: booleano | A vaca está com cio irregular ou quase constante desde o parto? | Cios frequentes, irregulares ou comportamento de ninfomania após o período voluntário de espera? | — | mycin |
| cisto_ovariano | Cisto Ovariano | doenca | tipo: booleano | — | — | baixa | mycin |
| claudicacao | Claudicação | pergunta | tipo: booleano | A vaca está mancando ou poupando uma pata? | Presença de claudicação? | — | mycin |
| cmt_reagente | CMT reagente | pergunta | tipo: booleano | — | O CMT foi reagente conforme a leitura do teste? | — | mycin |
| corrimento_com_pus_apos_21_dias | Corrimento com pus após 21 dias do parto | pergunta | tipo: booleano | A secreção da vulva tem pus (grossa, amarelada ou esbranquiçada)? | Corrimento vaginal purulento ou mucopurulento após 21 dias do parto? | — | mycin |
| corrimento_fetido | Corrimento vaginal fétido | pergunta | tipo: booleano | A secreção da vulva tem cheiro forte e desagradável? | Corrimento vaginal fétido observado? | — | mycin |
| corrimento_vaginal | Corrimento vaginal | pergunta | tipo: booleano | Há saída de secreção anormal pela vulva? | Presença de corrimento vaginal anormal? | — | mycin |
| costas_arqueadas | Costas arqueadas | pergunta | tipo: booleano | A vaca fica com as costas arqueadas e evita deitar ou descer rampas? | Postura antiálgica com dorso arqueado? | — | mycin |
| decubito | Decúbito | pergunta | tipo: booleano | A vaca está caída e não consegue se levantar? | Animal em decúbito, incapaz de se levantar? | — | mycin |
| dermatite_digital | Dermatite Digital Bovina | doenca | tipo: booleano | — | — | baixa | mycin |
| desidratacao | Desidratação | pergunta | tipo: booleano | Os olhos estão fundos ou a pele demora a voltar quando beliscada? | Desidratação evidente (enoftalmia, turgor cutâneo reduzido)? | — | mycin |
| deslocamento_abomaso_direita | Deslocamento de Abomaso à Direita | doenca | tipo: booleano | — | — | alta | mycin |
| deslocamento_abomaso_esquerda | Deslocamento de Abomaso à Esquerda | doenca | tipo: booleano | — | — | alta | mycin |
| diarreia | Diarreia | pergunta | tipo: booleano | A vaca está com diarreia? | Presença de diarreia? | — | mycin |
| dias_em_lactacao | Dias em lactação | ficha | casas_decimais: 0, max: 1000, min: 0, tipo: numerico, unidade: dias | Há quantos dias a vaca pariu? | Dias transcorridos desde o último parto? | — | mycin |
| distensao_flanco_direito | Barriga estufada do lado direito | pergunta | tipo: booleano | A barriga está estufada do lado direito? | Distensão do flanco direito, na região das últimas costelas? | — | mycin |
| distensao_flanco_esquerdo | Barriga estufada do lado esquerdo | pergunta | tipo: booleano | A barriga está estufada do lado esquerdo, alta como um balão? | Distensão do flanco esquerdo (fossa paralombar abaulada)? | — | mycin |
| dor_flexao_talao | Dor na região do talão | pergunta | tipo: booleano | A vaca demonstra dor na região do talão ao se movimentar? | Dor localizada na região dos bulbos do talão? | — | mycin |
| edema_barbela | Edema de barbela ou peito | pergunta | tipo: booleano | — | Edema de barbela, jugulares ingurgitadas ou bulhas cardíacas abafadas? | — | mycin |
| emagrecimento_progressivo | Emagrecimento progressivo | pergunta | tipo: booleano | A vaca vem emagrecendo aos poucos, mesmo comendo? | Perda progressiva de condição corporal? | — | mycin |
| endometrite | Endometrite Clínica | doenca | tipo: booleano | — | — | media | mycin |
| engasgo | Engasgo ou dificuldade de engolir | pergunta | tipo: booleano | A vaca parece engasgada, babando ou com esforço para engolir? | Sinais de obstrução esofágica (sialorreia, esforço de deglutição)? | — | mycin |
| enzimas_hepaticas_elevadas | Enzimas hepáticas elevadas | pergunta | tipo: booleano | — | Enzimas hepáticas elevadas no sangue (AST ou GGT acima da referência)? | — | mycin |
| esfregaco_hemoparasitas | Hemoparasitas no esfregaço | pergunta | tipo: booleano | — | Esfregaço sanguíneo com estruturas compatíveis com Babesia ou Anaplasma? | — | mycin |
| espuma_sonda | Conteúdo espumoso na sonda | pergunta | tipo: booleano | — | Sonda orogástrica traz conteúdo espumoso sem aliviar a distensão? | — | mycin |
| estrutura_ovariana_maior_25mm | Estrutura ovariana maior que 25 mm | pergunta | tipo: booleano | — | Estrutura ovariana com líquido maior que 25 mm, à palpação retal ou ao ultrassom, persistente e sem corpo lúteo? | — | mycin |
| evidencia_alteracao_leite | Evidência agrupada de alteração do leite | derivado | tipo: booleano | — | — | — | max |
| extremidades | Temperatura ao toque das extremidades | pergunta | tipo: categorico, valores: {normal, quente, fria} | As orelhas e as patas parecem normais, quentes ou frias ao toque? | Extremidades normais, quentes ou frias à palpação? | — | mycin |
| falhas_reprodutivas_lote | Falhas reprodutivas no lote | pergunta | tipo: booleano | Várias vacas do lote estão repetindo cio ou abortando? | Aumento de repetição de cio, abortos ou bezerros fracos no rebanho? | — | mycin |
| febre | Febre | derivado | tipo: booleano | — | — | — | mycin |
| feridas_boca | Feridas na boca | pergunta | tipo: booleano | Há feridas na boca, na gengiva ou na língua, com baba? | Erosões ou úlceras na mucosa oral? | — | mycin |
| fezes_aquosas_espuma_graos | Fezes com espuma e grãos | pergunta | tipo: booleano | As fezes estão muito líquidas, com espuma ou grãos inteiros? | Fezes aquosas, com espuma ou grãos não digeridos? | — | mycin |
| fezes_escassas | Pouco esterco | pergunta | tipo: booleano | A vaca está fazendo pouco esterco, menos que o normal? | Fezes escassas ou ausentes nas últimas horas? | — | mycin |
| fissura_interdigital_necrotica | Fissura interdigital necrótica | pergunta | tipo: booleano | — | Fissura na pele interdigital com tecido necrótico e odor fétido? | — | mycin |
| fita_urina_corpos_cetonicos | Corpos cetônicos na urina | pergunta | tipo: booleano | — | Teste urinário para corpos cetônicos positivo, lido no tempo indicado pelo fabricante? | — | mycin |
| flanco_esquerdo_afundado | Flanco esquerdo afundado | pergunta | tipo: booleano | A região do flanco esquerdo parece mais afundada que o habitual? | Fossa paralombar esquerda retraída? | — | mycin |
| flegmao_interdigital | Flegmão Interdigital (Podridão do Casco) | doenca | tipo: booleano | — | — | media | mycin |
| focinho_avermelhado | Focinho muito vermelho | pergunta | tipo: booleano | O focinho está muito vermelho, com feridas ou crostas? | Hiperemia ou lesões no plano nasal (focinho vermelho)? | — | mycin |
| gas_livre_sonda | Gás livre na sonda | pergunta | tipo: booleano | — | Sonda orogástrica libera gás livre e alivia a distensão? | — | mycin |
| gemido | Gemido | pergunta | tipo: booleano | A vaca geme quando respira, se deita ou se levanta? | Gemido expiratório espontâneo? | — | mycin |
| halito_adocicado_acetona | Hálito adocicado | pergunta | tipo: booleano | O hálito da vaca tem cheiro adocicado, semelhante à acetona? | Odor adocicado ou de acetona no hálito? | — | mycin |
| higroma | Inchaço nos joelhos | pergunta | tipo: booleano | A vaca tem inchaço nos joelhos (higroma)? | Higroma carpal? | — | mycin |
| hipocalcemia | Hipocalcemia Puerperal | doenca | tipo: booleano | — | — | alta | mycin |
| hipomagnesemia | Hipomagnesemia | doenca | tipo: booleano | — | — | alta | mycin |
| hipotermia | Hipotermia | derivado | tipo: booleano | — | — | — | mycin |
| historico_retencao_placenta | Histórico de retenção de placenta | ficha | tipo: booleano | Houve retenção de placenta neste parto? | Retenção de membranas fetais após o último parto? | — | mycin |
| ibr | Rinotraqueíte Infecciosa Bovina (IBR) | doenca | tipo: booleano | — | — | media | mycin |
| inchaco_entre_unhas_mau_cheiro | Inchaço entre as unhas com mau cheiro | pergunta | tipo: booleano | O pé está inchado entre as unhas, com cheiro ruim? | Aumento de volume interdigital, simétrico, com odor fétido? | — | mycin |
| inicio_lactacao | Início da lactação | derivado | tipo: booleano | — | — | — | mycin |
| leite_alterado | Alteração visível do leite | pergunta | tipo: booleano | O leite apresenta grumos, sangue ou aspecto aguado? | Alteração macroscópica do leite? | — | mycin |
| leite_com_sangue | Leite rosado ou com sangue | pergunta | tipo: booleano | O leite saiu rosado ou com sangue? | Leite sanguinolento com úbere flácido (agalaxia)? | — | mycin |
| leptospirose | Leptospirose | doenca | tipo: booleano | — | — | alta | mycin |
| lesao_erosiva_talao_morango | Lesão característica no talão | pergunta | tipo: booleano | — | Lesão erosiva ou ulcerativa, avermelhada e dolorosa no talão ou espaço interdigital? | — | mycin |
| lesao_sola_pinca_dor | Dor à pinça na sola ou na linha branca | pergunta | tipo: booleano | — | Dor à pinça de casco na sola ou na linha branca, com lesão visível após o casqueamento? | — | mycin |
| linfonodos_aumentados | Ínguas aumentadas | pergunta | tipo: booleano | Há caroços (ínguas) aumentados no pescoço, na frente da paleta ou na virilha? | Linfonodos superficiais aumentados? | — | mycin |
| lipidose_hepatica | Lipidose Hepática (Fígado Gorduroso) | doenca | tipo: booleano | — | — | alta | mycin |
| magnesio_serico | Magnésio sérico | pergunta | casas_decimais: 1, max: 10, min: 0, tipo: numerico, unidade: mg/dL | — | Qual é o magnésio sérico, em mg/dL? | — | mycin |
| mancar_pata_traseira_sem_inchaco | Manqueira de pata traseira sem inchaço | pergunta | tipo: booleano | A vaca manca de uma pata de trás, sem inchaço visível no pé? | Claudicação de membro pélvico sem aumento de volume digital ou interdigital? | — | mycin |
| mastite | Mastite | doenca | tipo: booleano | — | — | media | mycin |
| membranas_expostas_vulva | Restos de placenta na vulva | pergunta | tipo: booleano | Há restos de placenta pendurados para fora da vulva? | Membranas fetais expostas pela vulva? | — | mycin |
| metricheck_purulento | Conteúdo purulento ao exame vaginal | pergunta | tipo: booleano | — | Exame vaginal (Metricheck ou espéculo) com conteúdo purulento ou mucopurulento? | — | mycin |
| metrite | Metrite Puerperal | doenca | tipo: booleano | — | — | alta | mycin |
| mucosas_palidas_ou_ictericas | Mucosas pálidas ou amareladas | pergunta | tipo: booleano | A parte interna da pálpebra ou da vulva está muito pálida ou amarelada? | Mucosas pálidas ou ictéricas à inspeção? | — | mycin |
| mudanca_abrupta_concentrado | Mudança abrupta de concentrado | pergunta | tipo: booleano | Houve aumento brusco de ração ou acesso excessivo a grãos? | Mudança abrupta de concentrado ou acesso excessivo a grãos? | — | mycin |
| observar | Monitoramento Clínico Contínuo | urgencia | tipo: booleano | — | — | — | mycin |
| olhos_lacrimejando | Olhos lacrimejando | pergunta | tipo: booleano | Os olhos estão vermelhos ou lacrimejando muito? | Conjuntivite com lacrimejamento? | — | mycin |
| outros_animais_estufados | Outros animais estufados | pergunta | tipo: booleano | Outras vacas do mesmo lote também estão estufadas? | Outros animais do lote com distensão abdominal? | — | mycin |
| palpacao_membranas_retidas | Membranas retidas ao exame | pergunta | tipo: booleano | — | Membranas fetais retidas no útero ao exame vaginal ou retal, mais de 24 horas após o parto? | — | mycin |
| pasto_leguminosa_recente | Pasto de leguminosa recente | pergunta | tipo: booleano | A vaca comeu nas últimas horas pasto de leguminosa (alfafa, trevo) ou capim muito novo e molhado? | Ingestão recente de leguminosa ou pastagem muito tenra? | — | mycin |
| pasto_novo_adubado | Pasto novo e adubado | pergunta | tipo: booleano | A vaca foi solta há pouco tempo em pasto novo, muito verde ou adubado? | Mudança recente para pastagem tenra ou adubada com potássio e nitrogênio? | — | mycin |
| pcr_bohv1 | BoHV-1 detectado | pergunta | tipo: booleano | — | PCR ou isolamento de BoHV-1 positivo em secreção nasal ou ocular? | — | mycin |
| periparto_imediato | Periparto imediato | derivado | tipo: booleano | — | — | — | mycin |
| pescoco_em_s | Desvio cervical em S | pergunta | tipo: booleano | A vaca mantém o pescoço curvado em forma de S? | Desvio cervical em S observado? | — | mycin |
| ph_ruminal | pH ruminal | pergunta | casas_decimais: 1, max: 14, min: 0, tipo: numerico, unidade: pH | — | Qual é o pH ruminal medido, considerando método e momento da coleta? | — | mycin |
| ping_flanco_direito | Ping no flanco direito | pergunta | tipo: booleano | — | Ping metálico no flanco direito à percussão e auscultação simultâneas? | — | mycin |
| ping_metalico_flanco_esquerdo | Ping no flanco esquerdo | pergunta | tipo: booleano | — | Ping metálico no flanco esquerdo à percussão e auscultação simultâneas? | — | mycin |
| placenta_nao_expulsa_24h | Placenta não saiu em 24 horas | pergunta | tipo: booleano | A placenta continuou presa por mais de um dia após o parto? | Membranas fetais não expulsas em até 24 horas após o parto? | — | mycin |
| pneumonia | Pneumonia | doenca | tipo: booleano | — | — | media | mycin |
| prova_dor_reticular | Prova de dor reticular | pergunta | tipo: booleano | — | Prova de dor reticular positiva (bastão ou pinçamento da cernelha) com gemido? | — | mycin |
| puerperio | Puerpério | derivado | tipo: booleano | — | — | — | mycin |
| queda_producao | Queda de produção de leite | pergunta | tipo: booleano | A produção de leite caiu em relação ao habitual? | Queda da produção em relação ao padrão individual? | — | mycin |
| recusa_concentrado_come_volumoso | Recusa seletiva de concentrado | pergunta | tipo: booleano | A vaca recusa a ração, mas ainda come capim ou feno? | Recusa de concentrado com manutenção da ingestão de volumoso? | — | mycin |
| respiracao_ofegante | Respiração com esforço | pergunta | tipo: booleano | A vaca respira com esforço, rápido ou de boca aberta? | Taquipneia ou dispneia evidente? | — | mycin |
| retencao_placenta | Retenção de Placenta | doenca | tipo: booleano | — | — | media | mycin |
| reticulopericardite_traumatica | Reticulopericardite Traumática | doenca | tipo: booleano | — | — | alta | mycin |
| secrecao_nasal | Secreção nasal | pergunta | tipo: booleano | Está escorrendo catarro ou secreção pelo nariz? | Secreção nasal mucosa ou mucopurulenta? | — | mycin |
| sem_problema | Sem evidência de urgência pelos critérios da base | urgencia | tipo: booleano | — | — | — | mycin |
| sorologia_brucelose_reagente | Sorologia para brucelose reagente | pergunta | tipo: booleano | — | Teste sorológico para brucelose (AAT, 2-ME ou FPA) reagente? | — | mycin |
| sorologia_leptospirose_reagente | Sorologia para leptospirose reagente | pergunta | tipo: booleano | — | Soroaglutinação microscópica para leptospirose com título significativo? | — | mycin |
| temperatura_retal | Temperatura retal | pergunta | casas_decimais: 1, max: 45, min: 30, tipo: numerico, unidade: °C | — | Qual é a temperatura retal medida em °C? | — | mycin |
| teste_caneca_grumos | Grumos na caneca | pergunta | tipo: booleano | O teste da caneca mostrou grumos no leite? | Grumos detectados no teste da caneca? | — | mycin |
| timpanismo_espumoso | Timpanismo Espumoso | doenca | tipo: booleano | — | — | alta | mycin |
| timpanismo_gasoso | Timpanismo Gasoso | doenca | tipo: booleano | — | — | alta | mycin |
| tosse | Tosse | pergunta | tipo: booleano | A vaca está tossindo? | Tosse espontânea ou provocada presente? | — | mycin |
| tpb | Tristeza Parasitária Bovina | doenca | tipo: booleano | — | — | alta | mycin |
| tremores | Tremores musculares | pergunta | tipo: booleano | A vaca está com tremores ou espasmos nos músculos? | Fasciculações ou tremores musculares? | — | mycin |
| tuberculina_reagente | Tuberculinização reagente | pergunta | tipo: booleano | — | Teste tuberculínico (cervical comparativo) reagente? | — | mycin |
| tuberculose | Tuberculose | doenca | tipo: booleano | — | — | alta | mycin |
| ubere_inflamado | Inflamação do úbere | pergunta | tipo: booleano | O úbere está inchado, quente ou dolorido? | Há edema, calor ou dor no úbere? | — | mycin |
| ulcera_sola | Úlcera de Sola / Doença da Linha Branca | doenca | tipo: booleano | — | — | media | mycin |
| urina_escura | Urina escura | pergunta | tipo: booleano | A urina está avermelhada ou escura como café? | Urina avermelhada ou castanha observada? | — | mycin |
| utero_aumentado_palpacao | Aumento uterino à palpação | pergunta | tipo: booleano | — | Útero aumentado à palpação retal, considerado o período após o parto? | — | mycin |
| vaca_gorda_no_parto | Vaca gorda no parto | pergunta | tipo: booleano | A vaca estava muito gorda quando pariu? | Escore de condição corporal elevado no parto (3,75 ou mais, em 5)? | — | mycin |
| vacinada_brucelose | Vacinada contra brucelose | pergunta | tipo: booleano | A vaca foi vacinada contra brucelose quando bezerra (3 a 8 meses)? | Vacinação B19 ou RB51 comprovada? | — | mycin |

## Telas de triagem

| Ordem | ID | Seleção | Símbolos | Texto: produtor | Texto: veterinário | Alternativas por modo |
| --- | --- | --- | --- | --- | --- | --- |
| 1 | dias_em_lactacao | unica | dias_em_lactacao | Há quantos dias ocorreu o último parto? | Há quantos dias ocorreu o último parto? |  |
| 2 | estado_termico | unica | extremidades, temperatura_retal | Como estão as extremidades da vaca (orelhas e patas): normais, quentes ou frias? | Qual é a temperatura retal, em °C? | produtor: extremidades; veterinario: temperatura_retal |
| 3 | atitude_locomocao | multipla | apatia, claudicacao, decubito | Marque as alterações: abatimento, mancar ou incapacidade de se levantar. Sem alteração: nenhuma opção. | Marque as alterações: abatimento, mancar ou incapacidade de se levantar. Sem alteração: nenhuma opção. |  |
| 4 | apetite_ruminacao | unica | apetite | Informe o apetite: normal, reduzido ou ausente. | Informe o apetite: normal, reduzido ou ausente. |  |
| 5 | producao_leite | multipla | queda_producao, leite_alterado, ubere_inflamado | Marque as alterações: queda de produção, leite alterado ou úbere inflamado. Sem alteração: nenhuma opção. | Marque as alterações: queda de produção, leite alterado ou úbere inflamado. Sem alteração: nenhuma opção. |  |
| 6 | excrecoes | multipla | diarreia, corrimento_vaginal, urina_escura | Marque as alterações: diarreia, corrimento vaginal anormal ou urina escura. Sem alteração: nenhuma opção. | Marque as alterações: diarreia, corrimento vaginal anormal ou urina escura. Sem alteração: nenhuma opção. |  |

## Leitura e limites

O derivado `evidencia_alteracao_leite` usa `max`: inspeção do leite e teste da caneca não são somados como achados independentes. As regras R-MAS-01 e R-MAS-03 estão na camada 1; R-MAS-05 propaga o grupo para a doença. A ordem das tabelas é editorial; a agenda é calculada pelo motor.

Este documento descreve a base de desenvolvimento disponibilizada. Não demonstra equivalência integral com a Seção 3 da especificação nem aprovação para uso clínico.

Todo o conhecimento veterinário é suposição a validar; extraído de fontes públicas por IA, sem especialista.
