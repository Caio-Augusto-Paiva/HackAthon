# Prompt de revisão — Seção 1: Motor de inferência

> Status da seção: **aprovada (v5)** em 20/10/2026. v4 incorporou: avaliação de condição, guarda 0/0, regras viáveis, triagem obrigatória de 6 telas, novo critério de parada e testes do motor. v5: três camadas estritas, `cf_minimo`/`cf_maximo`, combinação `max` para derivados redundantes, gravidade como desempate, bloco de diagnóstico diferencial, dermatite digital no lugar de laminite. Cole tudo abaixo da linha numa IA revisora (Gemini, Codex etc.).

---

Você vai atuar como **revisor técnico independente** da especificação de um sistema especialista (trabalho acadêmico, Hackathon UFJF 2026, tema "Anamnese de bovinos leiteiros em lactação"). A arquitetura segue o modelo conceitual: base de conhecimento, motor de inferência, memória de trabalho, módulo de explicação, interface, aquisição de conhecimento e fontes externas.

Não presuma que a seção está certa nem errada. Verifique por conta própria.

## Restrições obrigatórias do desafio (não são discutíveis)

1. Nenhuma LLM no caminho da decisão em tempo de execução: a decisão sai da base de conhecimento explícita e do motor de inferência.
2. Decisão determinística e auditável.
3. Open source.
4. Tudo roda em localhost.

## Decisões já tomadas (não reabra; aponte só se criarem contradição)

- D1. Escopo de 8 doenças: mastite clínica, metrite puerperal, tristeza parasitária bovina, cetose, hipocalcemia, deslocamento de abomaso, acidose ruminal, dermatite digital. Urgências: `chamar_agora`, `observar`, `sem_problema`.
- D2. Dois modos (produtor e veterinário) com **a mesma base e o mesmo motor**; só mudam o texto e as perguntas oferecidas. A urgência do produtor sai do mesmo resultado do motor.
- D3. Motor próprio em Python puro: encadeamento para trás dirigido por objetivo (escolhe as perguntas) e propagação para frente dos CF (modelo MYCIN).
- D4. Urgência é modelada como regras da própria base. Bandeira vermelha leva direto a `chamar_agora`, independentemente do CF das doenças.
- D5. O parecer lista as 8 doenças, em ordem decrescente, em porcentagem, nos dois modos.
- D6. **Nenhum par das 8 doenças é mutuamente exclusivo**; comorbidades são reportadas juntas.
- D7. Triagem obrigatória de 6 telas no início; o limite de perguntas vale só para a fase dinâmica.
- D8. Todo o conhecimento veterinário é suposição a validar (extraído de fontes públicas por IA, sem especialista).

## Como revisar

Para cada problema encontrado, responda:

1. **Veredito:** erro / lacuna / decisão em aberto / ressalva menor.
2. **Trecho exato** da seção que sustenta o veredito. Se o texto simplesmente não diz algo, diga que é lacuna, não erro.
3. **Prova:** se o ponto for numérico ou algorítmico, **execute código** (aritmética exata com `fractions`, casos-limite como ±1, todas as permutações de ordem) e mostre o resultado.
4. **Correção mínima:** uma frase ou parágrafo reescrito. Não proponha mecanismos novos além do necessário.

Regras: não elogie por cortesia; se algo depender de informação que você não tem, diga qual pergunta a responderia; ao final, liste problemas relevantes que não estão nesta lista, e dê um resumo de 3 linhas do que precisa mudar.

---

## SEÇÃO 1 — Motor de inferência (v4)

**Pacote:** `engine/`, Python puro, sem dependência de web, testável sozinho.

### Fatos e condições

Fato: `(variável, valor, CF)` com CF em [−1, +1]. Só fatos observados chegam a ±1.

- **Booleanas:** o mapeamento de resposta é sim = +1, não = −1, "não sei" = 0, e vale **só** para perguntas booleanas. A condição `X` usa o CF do fato; a condição negada (`X == não`) usa −CF. Assim, resposta "não" para febre (CF −1) satisfaz `febre == não` com +1.
- **Categóricas e numéricas:** o fato guarda valor e CF separados. Se o valor satisfaz o operador, o CF da condição é o CF do fato; se não satisfaz, é −CF.
- **Intensidade** (leve/moderada/grave) é **valor categórico, nunca CF**. O CF expressa só a certeza da resposta.

### Regras

`id`, condições (conjunção de `variável op valor`), `cf_regra`, conclusão, `prioridade`, `classe` (`evidencia` | `bandeira_vermelha` | `urgencia`).

- `cf_regra` ∈ [−0,99; +0,99]. Valor negativo = regra de exclusão (evidência contra).
- Premissa = **mínimo** dos CF das condições. A regra só dispara com premissa > `limiar_premissa` (0,2). Esse limiar vale **só** para o CF da premissa.
- CF da conclusão = `premissa × cf_regra`.
- **Limites de CF na condição:** `cf_minimo` (a condição só vale se o CF do símbolo ≥ valor) e `cf_maximo` (só vale se ≤ valor). Valendo, a condição usa o próprio CF do símbolo (ou −CF, para `cf_maximo`). Usados nas regras de urgência ("doença com CF ≥ 0,50").
- **Três camadas estritas**, avaliadas nesta ordem: (1) regras que concluem `derivado`, com entradas em perguntas e ficha; (2) regras que concluem `doenca`, com entradas em perguntas, ficha e derivados; (3) regras de `bandeira_vermelha` e `urgencia`, com entradas em qualquer camada abaixo. Nenhuma regra lê símbolo da própria camada ou de camada acima. `sem_problema` não é regra: é o resultado quando nenhuma regra de urgência disparou e todas as doenças estão ≤ 0,35.

### Combinação (MYCIN)

Duas evidências da mesma conclusão: ambas positivas, `a + b(1−a)`; ambas negativas, `a + b(1+a)`; sinais mistos, `(a+b) / (1 − min(|a|,|b|))`.

- O resultado **independe da ordem dos disparos** (verificado em aritmética exata, em todas as permutações). A forma par a par fica; não trocar por acumuladores separados (dão resultado idêntico).
- Como `cf_regra` ≤ 0,99 em módulo, conclusões nunca chegam a ±1 e o caso 0/0 não ocorre. Mesmo assim há **guarda defensiva**: denominador 0 retorna 0.
- Motivo do limite ±0,99: com `cf_regra = +1` e premissa 1, a conclusão chega a +1 e trava (`[+1, −0,5, −0,5]` dá 1 em qualquer ordem).
- **Derivado com `combinacao: max`:** quando as entradas são redundantes (sinais sinônimos ou correlacionados, como distocia e retenção de placenta), o derivado recebe o **maior** CF das regras que disparam, em vez da soma MYCIN, para não inflar a evidência. Só é permitido se todas as regras desse derivado tiverem `cf_regra` positivo. Sinais independentes continuam como regras separadas somadas por MYCIN.

### Troca de modo sem perder dados

Fatos são guardados por **variável**, não por texto de pergunta. A resposta do produtor ("orelhas frias/quentes") e a do veterinário ("temperatura retal") alimentam **sinais derivados** (`febre`, `hipotermia`) por regras com CF próprios, e o MYCIN combina as fontes. O motor recalcula tudo a partir do conjunto de fatos a cada resposta, o que também permite corrigir uma resposta anterior.

### Triagem obrigatória (`meta.triagem`)

Seis telas fixas, perguntadas primeiro e nessa ordem; depois entra a seleção dinâmica. Telas de múltipla escolha gravam **símbolos booleanos separados** (marcado = +1, não marcado = −1, "não sei" na tela = 0 para todos). Texto por modo; os símbolos são os mesmos nos dois.

1. `dias_em_lactacao` (numérico; vem da ficha, perguntado só se ausente).
2. Estado térmico (escolha única): veterinário informa `temperatura_retal`; produtor informa `extremidades` (fria / normal / quente). Alimentam `febre` e `hipotermia`. "Orelhas frias" sugere hipocalcemia (suposição a validar).
3. Atitude e locomoção (múltipla): `apatia`, `claudicacao`, `decubito`. Nenhum marcado = alerta.
4. Apetite e ruminação (escolha única): `apetite` = normal / reduzido / ausente.
5. Produção e aspecto do leite (múltipla): `queda_producao`, `leite_alterado` (grumos, sangue, aguado), `ubere_inflamado`.
6. Excreções e secreções (múltipla): `diarreia`, `fezes_ressecadas`, `corrimento_vaginal`, `urina_escura`.

"Respondida" inclui "não sei", para a triagem nunca travar o diálogo. A triagem **não conta** no limite de perguntas. Marcar `decubito` dispara a bandeira já na triagem (pausa no modo produtor).

### Bandeiras vermelhas

Regras de classe `bandeira_vermelha`, com conclusão fixa `chamar_agora`. Disparam quando a premissa passa de 0,2 (resposta "sim"), sem depender do CF de nenhuma doença; "não sei" não dispara. Depois de disparada, a urgência **não desce mais**. No modo produtor, a interface pausa com o alerta ("sintoma grave, chame um veterinário o mais rápido possível") e oferece *Ver parecer* e *Continuar as perguntas*; o quadro urgente fica fixo no topo. No modo veterinário, mostra o mesmo quadro em linguagem técnica, sem pausar.

### Parecer

Lista **todas as 8 doenças em ordem decrescente de CF** (desempate por id), com **porcentagem nos dois modos**: `% = max(0, CF) × 100`, arredondado. CF < −0,2 aparece como 0% "descartada"; entre −0,2 e 0,2, como 0% "sem evidência". A porcentagem é **grau de confiança do sistema, não probabilidade**, e a tela diz isso. O CF bruto aparece na explicação "como?". A urgência vem das bandeiras e, na ausência delas, das regras de classe `urgencia` (gravidade × confiança).

A lista é dividida em blocos visuais: **Hipóteses principais** (≥ 50%), **Diagnóstico diferencial / sinais inespecíficos** (20% a 50%) e **Pouco provável ou descartada** (< 20%). Cada doença mostra também sua gravidade (alta, média, baixa).

### Resolução de conflito

Agenda ordenada por `prioridade` (decrescente), depois especificidade (mais condições primeiro), depois `id`. Entre urgências disparadas, a mais urgente vence. A agenda não altera os CF (a combinação independe da ordem); só decide a urgência e a ordem de avaliação.

### Próxima pergunta (fase dinâmica)

- **Regra viável:** regra que ainda pode atingir premissa > 0,2 com os fatos conhecidos e as variáveis perguntáveis no modo atual. Exclui regra morta por condição conhecida e regra com variável exclusiva do veterinário ainda não respondida, no modo produtor.
- Escolha: variável desconhecida, perguntável no modo atual, que aparece em mais regras **viáveis** de hipóteses abertas, ponderada por |`cf_regra`|; empate pela maior **gravidade** da hipótese servida (alta > média > baixa), depois por `id`.
- Variáveis exclusivas do veterinário não são perguntadas no modo produtor, mas, se já respondidas, seus fatos continuam valendo.
- **Diretriz de autoria:** não misturar sinal do produtor e exame do veterinário na mesma conjunção. Usar uma regra do produtor (`cf_regra` menor) e uma regra de confirmação do veterinário (`cf_regra` maior), que se somam via MYCIN.

### Parada

Limiares nomeados em `meta.limiares` da base (calibráveis e versionados): `premissa` 0,2; `hipotese_aberta` 0,35; `exaustao` 0,60; `potencial` 0,70; `confirmacao` 0,80.

**Potencial máximo** de uma hipótese: combinação MYCIN do CF atual com todos os `cf_regra` positivos das suas regras viáveis, supondo premissa 1. É um limite superior válido porque a combinação de positivos é monotônica e evidência negativa só reduz. Quando a regra depende de sinal derivado, o potencial é propagado de baixo para cima pelo grafo acíclico.

O motor **encerra por confirmação** quando ao menos uma doença tem CF ≥ 0,80 **e**:

- (a) toda a `meta.triagem` foi respondida;
- (b) nenhuma outra hipótese com CF atual > 0,35 tem potencial máximo ≥ 0,70;
- (c) nenhuma regra `bandeira_vermelha` com alguma condição ativada (CF > 0,2) tem condição ainda desconhecida e perguntável no modo atual.

Comorbidade: não há distância mínima entre hipóteses; todas as doenças ≥ 0,80 saem juntas.

Outras saídas:
- acabaram as perguntas aplicáveis ao modo;
- atingiu o limite da **fase dinâmica** (12 perguntas no produtor, 25 no veterinário; a triagem não conta);
- nenhuma hipótese aberta tem potencial máximo ≥ 0,60.

Ao parar por limite, o parecer destaca as hipóteses inconclusivas (CF > 0,35) e as bandeiras não verificadas.

### Traço

Lista ordenada de eventos: `pergunta_feita` (com o motivo), `fato_adicionado` (com origem: resposta, ficha, importação ou regra), `regra_disparada` (fatos de entrada com CF, CF de saída) e `cf_combinado` (antes/depois). **"Por quê?"** é o motivo gravado no evento da pergunta; **"Como?"** percorre o traço de trás para frente, da conclusão até as respostas. Limitação declarada: o traço não responde "por que **não** é a doença X?".

### Testes do motor

- Embaralhar a ordem das evidências não muda o resultado (tolerância de ponto flutuante).
- Caso +1/−1 sem exceção (guarda retorna 0).
- `febre == não` com resposta "não" dispara a regra.
- Tela de múltipla escolha grava um booleano por opção; "não sei" grava 0 em todos.
- Com CF ≥ 0,80 e triagem incompleta, o motor não encerra.
- Líder em 0,85 e outra hipótese em 0,5 com potencial ≥ 0,70: continua; com potencial < 0,70: encerra e lista as duas.
- Bandeira com condição ativada e outra condição pendente impede a parada.
- Duas doenças ≥ 0,80 encerram e aparecem juntas.
- Modo produtor: nenhuma pergunta é escolhida por causa de regra inviável; hipótese > 0,35 cujo potencial depende só de variável exclusiva do veterinário não bloqueia a parada.
- O limite conta só perguntas dinâmicas.
- Potencial máximo propagado por sinal derivado é ≥ ao CF alcançado em qualquer sequência de respostas (teste de propriedade).
- Derivado `max`: duas regras positivas de 0,9 dão 0,9 (não 0,99).
- `cf_minimo 0,50`: doença em 0,49 não dispara a urgência; em 0,50 dispara.
- Camadas: regra de doença que lê outra doença é rejeitada pelo validador.
- Empate na próxima pergunta é resolvido pela gravidade antes do `id`.
