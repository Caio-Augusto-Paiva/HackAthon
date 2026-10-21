# Prompt de revisão — Seção 2: Base de conhecimento e editor gráfico

> Status da seção: **v3** (20/10/2026). v2: triagem e limiares. v3: `cf_minimo`/`cf_maximo`, camadas estritas, `gravidade`, `combinacao` em derivados, dermatite digital no lugar de laminite. Cole tudo abaixo da linha numa IA revisora.

---

Você vai atuar como **revisor técnico independente** da especificação de um sistema especialista (trabalho acadêmico, Hackathon UFJF 2026, tema "Anamnese de bovinos leiteiros em lactação"). Esta seção descreve o **formato da base de conhecimento**, a conversão entre ela e o grafo do editor visual, o versionamento, a validação e os casos de teste. Não presuma que a seção está certa nem errada. Verifique por conta própria.

## Restrições obrigatórias do desafio (não são discutíveis)

1. Nenhuma LLM no caminho da decisão em tempo de execução.
2. Decisão determinística e auditável.
3. Open source.
4. Tudo roda em localhost.

## Decisões já tomadas (não reabra; aponte só se criarem contradição)

- D1. 8 doenças: mastite clínica, metrite puerperal, tristeza parasitária bovina, cetose, hipocalcemia, deslocamento de abomaso, acidose ruminal, dermatite digital. Urgências: `chamar_agora`, `observar`, `sem_problema`. Nenhum par é mutuamente exclusivo.
- D2. Dois modos (produtor e veterinário) com a mesma base e o mesmo motor.
- D3. O grafo do editor é uma **rede de regras** (variáveis/sinais, regras com CF, conclusões); a ordem das perguntas dinâmicas não é desenhada, o motor a deduz. Há uma triagem fixa de 6 telas no início.
- D4. Editor com nível B: visualizar, editar CF/condições/textos, adicionar e remover nós e arestas, salvar nova versão com validação e execução dos casos de teste. O nível C (criar do zero, desfazer/refazer, comparar versões) é previsto, fora do escopo base.
- D5. Ficha de animal (dados fictícios) e histórico de anamneses no SQLite; importação de prontuário (CSV/JSON) alimenta a memória de trabalho.
- D6. Todo conhecimento veterinário é suposição a validar (extraído por IA de fontes públicas, citadas, sem especialista).
- D7. Regras do motor (resumo da Seção 1): fatos `(variável, valor, CF)`; premissa = mínimo dos CF; `cf_regra` ∈ [−0,99; +0,99]; combinação MYCIN; bandeira vermelha → `chamar_agora`; parada por confirmação exige triagem completa, hipóteses abertas sem potencial e bandeiras ativadas verificadas.

## Como revisar

Para cada problema encontrado, responda:

1. **Veredito:** erro / lacuna / decisão em aberto / ressalva menor.
2. **Trecho exato** da seção que sustenta o veredito (se o texto não diz algo, é lacuna, não erro).
3. **Prova:** se o ponto for algorítmico (ciclos, alcançabilidade, ida e volta grafo ↔ JSON), descreva ou execute um contraexemplo concreto.
4. **Correção mínima:** uma frase ou parágrafo reescrito, sem mecanismos novos além do necessário.

Regras: não elogie por cortesia; diga qual pergunta responderia o que depender de informação que você não tem; ao final, liste problemas que não estão nesta lista e dê um resumo de 3 linhas do que precisa mudar.

---

## SEÇÃO 2 — Base de conhecimento e editor gráfico (v2)

**Formato canônico: JSON**, validado por modelos Pydantic (fonte única da verdade; deles se exporta o JSON Schema e os tipos TypeScript do frontend). Não uso YAML: o YAML 1.1 lido pelo PyYAML converte `no` e `yes` em booleanos, e nossas respostas e valores são palavras em português. O humano edita pelo grafo, então a legibilidade do arquivo importa menos do que a ausência de ambiguidade. Observações vão em campos `nota`.

**Arquivos.**
```
base/
  versoes/v0001.json, v0002.json …   (imutáveis)
  ativa.json                          {"versao": "v0002"}
  casos/casos.json                    (casos de teste, compartilhados)
```
Os arquivos são a fonte da verdade (e vão para o git); o SQLite guarda só o índice de versões e os resultados de teste. O editor **nunca sobrescreve**: salvar cria o próximo `vNNNN.json` com `pai`.

**Estrutura do arquivo.** `meta`, `simbolos[]`, `regras[]`, `layout`.
- **`meta`:** `versao`, `pai`, `autor`, `data`, `nota`, mais:
  - `limiares`: `premissa` 0,2; `hipotese_aberta` 0,35; `exaustao` 0,60; `potencial` 0,70; `confirmacao` 0,80.
  - `limite_dinamico`: `produtor` 12, `veterinario` 25 (a triagem não conta).
  - `triagem`: lista ordenada de 6 telas. Cada tela tem `id`, `selecao` (`unica` | `multipla`), `simbolos` (ids que a tela grava) e textos por modo (`produtor`, `veterinario`), incluindo o rótulo de cada opção.
- **Símbolo** (namespace único para tudo que a regra lê ou conclui): `id`, `tipo` (`pergunta` | `ficha` | `derivado` | `doenca` | `urgencia`), `dominio` (`booleano`, `categorico` com valores, ou `numerico` com min/max/unidade), `nome` e, quando perguntável na fase dinâmica, `pergunta` e `por_que` **por modo** (`produtor`, `veterinario`; texto ausente = não perguntável naquele modo), `campo_ficha` (tipo `ficha`), `fonte`, `gravidade` (obrigatório em `doenca`: `alta` | `media` | `baixa`), `combinacao` (só em `derivado`: `mycin`, padrão, ou `max`).
- **Regra:** `id`, `se` (lista de `{simbolo, op, valor, negado, cf_minimo?, cf_maximo?}`; `op` ∈ `=`, `≠`, `<`, `≤`, `>`, `≥`, `em`), `entao` (`{simbolo, cf}`), `prioridade`, `classe` (`evidencia` | `bandeira_vermelha` | `urgencia`), `fonte` (citação), `status` (`suposicao_a_validar` | `validada`), `nota`.

**Grafo ↔ regras.** O grafo é **bipartido**: nós de símbolo e nós de regra. Aresta símbolo→regra é uma condição (carrega `op`, `valor`, `negado`); aresta regra→símbolo é a conclusão (carrega `cf`). Cada regra do JSON é exatamente um nó de regra, então a conversão é 1:1 e sem perda, nos dois sentidos. Símbolos da triagem aparecem com um selo de triagem. O `layout` guarda x, y por id e fica **separado** da semântica: mover um nó não cria versão semântica nem ruído no diff. O grafo não carrega nenhuma lógica que não esteja no JSON. A triagem e os limiares são editados num painel de `meta`, fora do grafo.

**Ciclo de edição (nível B).** Carregar a ativa → editar → *Salvar* → o backend valida e **bloqueia se houver erro** → grava `vNNNN.json` → roda `casos.json` na nova versão e na anterior → mostra o que passou, falhou e mudou → *Ativar* é uma ação separada. Desfazer/refazer e comparação (nível C) são operações sobre arquivos imutáveis e não mudam o formato.

**Validação** (pacote `kb/`, usado pelo editor, pela API e pelos testes).
- *Erros (bloqueiam):*
  - símbolo indefinido em condição, conclusão ou tela de triagem; id duplicado;
  - valor fora do domínio ou `op` incompatível com o tipo; `cf` fora de ±0,99;
  - **ciclo** na dependência símbolo→regra→símbolo (DFS; a propagação para frente e o cálculo de potencial exigem grafo acíclico);
  - **regra inalcançável** (condição em símbolo derivado que nenhuma regra conclui, ou em pergunta sem texto em nenhum modo, fora da triagem e sem campo de ficha, ou **condição negada sobre derivado que nenhuma regra conclui com CF negativo** — essa condição nunca vale, porque o derivado fica em CF 0 e −0 = 0);
  - bandeira vermelha cuja conclusão não é `chamar_agora`;
  - **bandeira vermelha sem nenhuma condição sobre símbolo da triagem** (senão ela nunca seria exigida antes da parada);
  - doença sem nenhuma regra; doença sem nenhuma regra só com símbolos perguntáveis no modo produtor;
  - **cobertura da triagem:** doença sem nenhuma regra cujas condições sejam todas símbolos da triagem ou derivados cujas entradas são **todas** da triagem;
  - **camadas:** regra que lê símbolo da própria camada ou de camada acima (camada 1 `derivado` ← perguntas e ficha; camada 2 `doenca` ← perguntas, ficha e derivados; camada 3 `bandeira_vermelha`/`urgencia` ← qualquer camada abaixo);
  - `doenca` sem `gravidade`; derivado `max` com alguma regra de `cf` negativo; `cf_minimo`/`cf_maximo` fora de [0, 1] ou usados em símbolo que não seja `doenca`/`derivado`;
  - tela de triagem sem texto em algum dos dois modos (símbolo de ficha dispensa);
  - limiares fora da ordem `premissa < hipotese_aberta < exaustao < potencial < confirmacao`;
  - regra sem `fonte`.
- *Avisos:* símbolo perguntável nunca usado; duas regras com as mesmas condições e conclusão de sinal oposto; contagem de regras ainda `suposicao_a_validar`.

**Casos de teste** (`casos.json`): `id`, `descricao`, `modo`, `ficha`, `triagem` (respostas das 6 telas), `respostas` (símbolo → valor, fase dinâmica), opcionais `continuacao` (troca de modo no meio: novo `modo`, triagem extra e respostas) e `limite_dinamico` (substitui o de `meta` só nessa execução), e `esperado` (`urgencia`, `bandeira` opcional, `top1` ou `top3_contem`, **faixas de porcentagem por doença**, e opcionalmente `motivo_parada`). Uso faixas, não valores exatos, para o teste não quebrar a cada ajuste de CF. Cobertura: por doença, ao menos 2 casos típicos e 1 ambíguo; casos de bandeira vermelha (incluindo decúbito na triagem); um caso de comorbidade; um caso de troca de modo (respostas do produtor mais continuação como veterinário); um caso de parada por limite. Os casos são inventados por nós, então são **suposição a validar**. Cada execução fica registrada por versão. Convenções do executor (`engine/casos.py`): pergunta dinâmica feita e ausente em `respostas` vale "não sei"; resposta que o motor não chegou a pedir é ignorada; bandeira com pausa recebe `continuar` automaticamente. A versão ativa precisa passar todos os casos; versões antigas só reportam.

**Dimensão estimada** (suposição, para caber em dois dias e meio): cerca de 50 a 60 símbolos perguntáveis (dos quais cerca de 15 gravados pela triagem), 15 sinais derivados, 8 doenças, 3 urgências, 100 regras e 30 casos de teste.
