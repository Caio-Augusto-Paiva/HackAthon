# Prompt de revisão — Seção 6: Entrega — documentação, apresentação, riscos e pontos em aberto

> **Agente:** Gemini Pro (app web) (alternativa: Codex). **Skills:** `writing-plans`, `verification-before-completion` (obra/superpowers); `pptx` (anthropics/skills, source-available) ou Google Slides para os slides. **Por quê:** a revisão é de comunicação e de riscos, não de código; um revisor de outra família de modelo avalia melhor se a apresentação convence a banca. Ver `docs/agentes-e-skills.md`.

> Status da seção: **RASCUNHO, pendente de aprovação** (20/10/2026). Cole tudo abaixo da linha numa IA revisora.

---

Você vai atuar como **revisor técnico independente** de um sistema especialista (trabalho acadêmico, Hackathon UFJF 2026, tema "Anamnese de bovinos leiteiros em lactação"). Esta seção define a documentação obrigatória (processo de desenvolvimento, arquitetura tecnológica e regras de produção), o roteiro da apresentação e da demonstração, as perguntas prováveis da banca e o registro de riscos. Verifique se cada exigência dos organizadores ([A] slides 3, 5, 10, 11, 12 e 15) está atendida e se a apresentação cabe no tempo. Não presuma que a seção está certa nem errada. Verifique por conta própria.

## Restrições obrigatórias do desafio (não são discutíveis)

1. Nenhuma LLM no caminho da decisão em tempo de execução.
2. Decisão determinística e auditável.
3. Open source.
4. Tudo roda em localhost.

## Decisões já tomadas (não reabra; aponte só se criarem contradição)

- D1. Documentação em `docs/entrega/` com 01-processo, 02-arquitetura, 03-regras-de-producao (gerado da base).
- D2. Diário de IA por pessoa em `docs/processo/`.
- D3. Três apresentadores.
- D4. Envio em .zip do código mais PDFs, alvo 18:30.
- D5. Duração da apresentação não consta dos documentos (suposição: 10 min + demo de 4 min, versão curta de 5 min).

## Como revisar

Para cada problema encontrado, responda:

1. **Veredito:** erro / lacuna / decisão em aberto / ressalva menor.
2. **Trecho exato** da seção que sustenta o veredito (se o texto não diz algo, é lacuna, não erro).
3. **Prova:** aponte exigência dos organizadores não atendida, slide que estoura o tempo, pergunta provável da banca que ficou sem resposta, ou risco sem mitigação.
4. **Correção mínima:** uma frase ou parágrafo reescrito, sem mecanismos novos além do necessário.

Regras: não elogie por cortesia; diga qual pergunta responderia o que depender de informação que você não tem; ao final, liste problemas que não estão nesta lista e dê um resumo de 3 linhas do que precisa mudar.

---

## SEÇÃO 6 — Entrega: documentação, apresentação, riscos e pontos em aberto

> Siglas: **A** = motor/base (`engine/`, `kb/`), **B** = API, validador, scripts, **C** = web, e2e (Seção 4.8). **[A]** = `apresentacaoRerun.pdf`; **[D]** = `DocumentárioRerun.pdf`. Tudo que não vem das Seções 1 a 5, de `docs/agentes-e-skills.md` ou de [A]/[D] está marcado **(suposição)**. Nenhum código aqui: só estrutura, roteiros e tabelas.

**O que os organizadores pedem (sem acréscimos):** documentação com processo de desenvolvimento, arquitetura tecnológica e regras de produção utilizadas; apresentação que mostre de forma organizada todo o processo, do uso da IA ao resultado; demonstração em localhost ([A] slide 10; [D] p. 2). Avaliação: nota de 1 a 10 pelo potencial de resolver de fato o problema, com complexidade e assertividade como desempate ([A] slide 3); organização do grupo com a IA e conhecimento adquirido ([A] slide 11); habilidade com agentes de IA, trabalho em equipe, liderança e controle emocional ([A] slide 5). Passo 8 do roteiro: "estude e entenda em detalhes o que foi produzido" ([A] slide 12). Envio até quinta 22/10 às 20:00 por e-mail ou WhatsApp, com nome e telefone de todos ([A] slide 15). **A duração da apresentação não consta dos documentos (suposição: 10 min + demo).**

---

## 6.1 Documentação

### 6.1.1 Estrutura entregue

```
docs/
├─ entrega/                         # o que a banca lê (versionado; vai no pacote de envio)
│  ├─ README.md                     # índice, como rodar (2 comandos), equipe, mapa do pacote
│  ├─ 01-processo.md                # PROCESSO DE DESENVOLVIMENTO (manual, curado a partir de docs/processo/)
│  ├─ 02-arquitetura.md             # ARQUITETURA TECNOLÓGICA (condensa as Seções 1, 2 e 4)
│  ├─ 03-regras-de-producao.md      # REGRAS DE PRODUÇÃO (GERADO da base ativa; não editar à mão)
│  └─ 04-casos-de-teste.md          # (opcional, GERADO de casos.json + última execução) (suposição)
├─ processo/                        # diário bruto de uso da IA (insumo do 01 e dos slides)
│  ├─ A.md  B.md  C.md              # um por pessoa (já previsto na Seção 5.3, suposição)
│  └─ revisoes-cruzadas.md          # log das revisões entre IAs (6.1.3)
└─ (já existentes) superpowers/specs · superpowers/plans · fontes/fontes.md · prompts/ · pesquisa/
```

**`README.md`:** objetivo (T1 Anamnese, [A] slide 9); restrições cumpridas em uma tabela (sem LLM na decisão, determinístico, open source, localhost, dados fictícios); como rodar (`scripts\rodar.ps1`, Seção 5.2); mapa do pacote; integrantes com nome e telefone (**a preencher pelo grupo; não inventar**); aviso "todo o conhecimento veterinário é suposição a validar".

**`01-processo.md` — índice:**
1. Visão geral e linha do tempo real (terça a quinta) contra o cronograma da Seção 5.3 (marcos cumpridos, cortes aplicados).
2. O passo a passo de [A] slide 12 mapeado ao que foi feito (passos 1 a 8), com link para o artefato de cada passo.
3. Agentes e skills por pessoa e por prompt (`docs/agentes-e-skills.md`): quem usou o quê e por quê (revisor de outra família de modelo, Claude Code reservado ao crítico, janelas de 5 h espalhadas).
4. Resumo do uso da IA: tabela "tarefa → agente → aceito / ajustado / rejeitado" com 2 a 3 casos por pessoa (extraído de `docs/processo/*.md`).
5. Revisões cruzadas entre IAs: resumo do log (6.1.3) com os exemplos de achado procedente e achado refutado.
6. Onde a IA entrou e onde **não** entrou: gera, explica e ajuda a extrair regras; a decisão sai da base e do motor ([A] slides 8 e 13). Nenhuma chamada a LLM em tempo de execução, verificável por teste de arquitetura (Seção 5, `test_inferencia.py`).
7. Decisões do arquiteto (Seções 4.9 e 5.5) e o que o grupo decidiu contra a sugestão da IA.
8. Trabalho em equipe: divisão por pasta, contratos congelados, mocks, ligação de quarta; como os conflitos foram resolvidos.
9. Passo 8 de [A] slide 12 (estudo do que foi produzido): o que cada pessoa aprendeu e a "prova de entendimento" (cada um explica uma parte que não escreveu).
10. Limitações, riscos que ocorreram e próximos passos (resumo da 6.3).

**`02-arquitetura.md` — índice:** (1) restrições e como cada uma é atendida; (2) diagrama Mermaid da Seção 4.2 e tabela componente → pasta; (3) tecnologias, versões e licenças (4.1) e descartados; (4) motor: três camadas, MYCIN, triagem, parada, agenda, traço (Seção 1, uma página); (5) base: JSON canônico, versões imutáveis, grafo bipartido, validação (Seção 2); (6) API e contratos (resumo de 4.5, link para `contratos/openapi.json`); (7) persistência SQLite (4.6); (8) testes em quatro camadas (5.1); (9) execução em localhost e offline (5.2); (10) limitações de arquitetura (sem "por que não?", PoC sem autenticação, sensores/APIs fora do escopo).

**`03-regras-de-producao.md` — gerado.** Um script em `scripts/` (nome sugerido `gerar_doc_regras`, **suposição**; sem código nesta fase) lê `base/ativa.json` e a versão que ela aponta, e escreve o Markdown. Assim documento e base nunca divergem. Conteúdo gerado:
- Cabeçalho: versão, `pai`, data, `hash` (4.6), contagem de regras por `status` (`suposicao_a_validar` / `validada`), limiares de `meta.limiares` e limites dinâmicos.
- **Uma tabela por doença** (as 8), mais tabelas para derivados (camada 1), bandeiras vermelhas e urgência (camada 3), com as colunas: `id` | condições em texto legível (ex.: `corrimento_vaginal E puerperio`; `op`, `negado`, `cf_minimo`/`cf_maximo` explícitos) | `cf` | `fonte` (F1 a F12, com link de `docs/fontes/fontes.md`) | `status` | `nota`. Ordem: por `id`.
- Anexos gerados: tabela de símbolos (id, tipo, domínio, pergunta por modo, gravidade) e lista das telas de triagem.
- Rodapé fixo (texto do gerador): "Todo o conhecimento veterinário é suposição a validar; extraído de fontes públicas por IA, sem especialista."
- **Guarda:** um teste em `tests/` regenera e compara com o arquivo commitado (mesmo padrão dos tipos TypeScript, Seção 4.7 item 4); falhou, bloqueia a entrega. O mesmo script (flag para casos) gera o `04-casos-de-teste.md` (**suposição**).

### 6.1.2 Como registrar o uso da IA nos dois dias

Cada pessoa mantém `docs/processo/<A|B|C>.md`, **uma entrada por interação relevante**, escrita na hora (2 min) ou ao fim de cada bloco da Seção 5.3 **(suposição)**. Modelo de entrada:

| Campo | Conteúdo |
|---|---|
| Quando / bloco | data, hora, bloco do cronograma |
| Agente e skill | ex.: Claude Code + `test-driven-development`; Codex; Antigravity (C) |
| Prompt-chave | o texto essencial (não a conversa inteira); anexar o bruto em `docs/processo/anexos/` só se curto |
| Saída resumida | o que o agente devolveu |
| Decisão | **aceito** / **ajustado** / **rejeitado** |
| Por quê | critério usado (teste, fonte, contrato, restrição do desafio) |
| Evidência | commit, teste que passou/falhou, id da regra |

Meta **(suposição)**: ao menos 8 a 10 entradas por pessoa, com ao menos 2 "rejeitado" ou "ajustado" (mostra julgamento, não só aceitação). `01-processo.md` e os slides de IA saem desse diário, não da memória.

### 6.1.3 Log de revisões cruzadas entre IAs

`docs/processo/revisoes-cruzadas.md` tem uma linha por achado: seção, revisor (agente ou pessoa), achado, veredito (procedeu / procedeu em parte / refutado), prova e mudança aplicada. Achados do planejamento (20/10/2026):

| # | Seção | Revisor | Achado | Veredito e prova |
|---|---|---|---|---|
| 1 | 1 | Gemini | Separar acumuladores positivo e negativo na combinação MYCIN | **refutado**: aritmética exata, todas as permutações; resultado idêntico ao par a par |
| 2 | 1 | Gemini | Divisão por zero em `comb(+1, −1)` | **procedeu**: teste mostrou 0/0; `cf_regra` limitado a ±0,99 e guarda defensiva |
| 3 | 1 | Gemini | Como `variável op valor` vira CF; condição de ausência | **procedeu** (lacuna): regra de avaliação de condição definida |
| 4 | 1 | Gemini | Variável do veterinário em CF 0 trava regras do produtor | **procedeu**: regras viáveis e diretriz de autoria |
| 5 | 1 | Gemini | Parada sem exigir urgências e sem tratar comorbidade | **procedeu**: triagem obrigatória e novo critério de parada |
| 6 | 1 | Claude (revisão da revisão) | +1 é absorvente: `[+1, −0,5, −0,5]` dá 1 em qualquer ordem | **procedeu**: mesmo limite de ±0,99 |
| 7 | 1 | Claude (revisão da revisão) | Intensidade (leve/moderada/grave) codificada como CF | **procedeu**: intensidade virou valor categórico |
| 8 | 1 | Claude (revisão da revisão) | Seleção de pergunta contava regras já mortas | **procedeu**: só regras viáveis contam |
| 9 | 1 (triagem) | especialista consultado pela equipe | Faltava sinal de excreções/secreções na triagem (metrite, acidose, TPB) | **procedeu em parte**: 6ª tela adicionada; "começariam em CF 0" era exagero (febre já alimentava metrite e TPB) |
| 10 | 1 (triagem) | especialista consultado pela equipe | Chamar a triagem de "Protocolo DART" | **refutado**: DART vem de gado de corte e doença respiratória; nome removido |
| 11 | 1 (triagem) | Claude | Opções que coexistem (diarreia e corrimento) modeladas como escolha única | **procedeu**: telas de múltipla escolha gravam booleanos separados |
| 12 | 3 | Claude, lendo as fontes | Laminite sem fonte (a página do MSD trata de dermatite digital); "cheiro de acetona" ausente da página de cetose — também presente, com CF 0,90, no exemplo de base trazido pela equipe | **procedeu**: laminite trocada por dermatite digital; sinal de acetona removido |
| 13 | 1 | segundo especialista consultado pela equipe | A combinação MYCIN "não é associativa com 4 ou mais evidências" | **refutado**: 4, 5 e 6 evidências em todas as permutações, aritmética exata; prova por `t(x) = sinal(x)·(−ln(1−\|x\|))`, que transforma a combinação em soma |
| 14 | 1 | segundo especialista consultado pela equipe | Variável sem valor ou "não sei" e peso de perguntas através de derivados | **procedeu**: condição sem valor vale 0; peso propagado |
| 15 | 1 | segundo especialista consultado pela equipe | Limiar 0,35 misturado com hipóteses que recebem perguntas | **procedeu**: "hipótese aberta" (−0,2 a 0,80) separada de `hipotese_relevante` (0,35) |
| 16 | 3 e 5 | subagente Sonnet (rascunho da Seção 5) | R-MET-06 e R-CET-08 nunca disparavam (derivado de período só recebe evidência positiva) | **procedeu**: regras testam `dias_em_lactacao`; validador barra o padrão |
| 17 | 3 | subagente Sonnet | Contagem de perguntas exclusivas do veterinário (7 em vez de 8) | **procedeu**: corrigido |
| 18 | 3 | Claude (decisão) | `sem_problema` como regra lia bandeira da mesma camada | decisão: virou resultado padrão; **confirmar com a equipe** |

Regra de ouro do log: **achado numérico só é aceito ou recusado com execução** (aritmética exata, caso-limite, permutações); achado de domínio só com fonte. Isso vira um ponto forte na apresentação ([A] slide 5: habilidade com agentes de IA).

### 6.1.4 Formato final de envio **(suposição)**

Um `.zip` (sem `.venv` e `node_modules`, com `uv.lock` e `package-lock.json`, Seção 5.2) contendo: código-fonte; `docs/entrega/` também em **PDF** (um PDF por documento, geração por Markdown→PDF, ferramenta open source a escolher); slides em **PDF** e no formato editável; `README.md` na raiz. Envio por e-mail e, em paralelo, aviso por WhatsApp, com nome e telefone dos três ([A] slide 15), alvo interno 18:30 (Seção 5.5 decisão 4). O limite de tamanho do anexo é desconhecido: se o zip passar de alguns MB, enviar o código em zip e os PDFs em mensagem separada **(suposição)**.

---

## 6.2 Apresentação

### 6.2.1 Roteiro slide a slide (versão de 10 min + demo de 4 min) **(suposição de duração)**

| # | Slide | Mensagem em uma frase | Quem | Tempo |
|---|---|---|---|---|
| 1 | Problema e tema | Triagem de bovinos leiteiros em lactação é difícil de explicar e de auditar; escolhemos o tema T1 Anamnese ([A] slide 9). | C | 0:45 |
| 2 | Sistema especialista e motor de inferência | Um sistema especialista separa conhecimento (regras) de raciocínio (motor): encadeamento, incerteza (CF) e explicação "por quê?/como?" ([A] slide 12, passo 2). | A | 1:00 |
| 3 | Arquitetura | Os sete componentes do modelo conceitual ([A] slide 14) viram módulos: `engine/`, `kb/`, `api/`, `web/` (diagrama da Seção 4.2). | B | 1:15 |
| 4 | O motor | Encadeamento para trás escolhe a próxima pergunta, propagação MYCIN combina evidências sem depender da ordem, em três camadas; triagem de 6 telas e critério de parada explícitos. | A | 1:45 |
| 5 | Base e editor | A base é JSON versionado e imutável; o editor em grafo valida (ciclos, camadas, inalcançáveis) e só salva nova versão sem erros. | B | 1:00 |
| 6 | Domínio | 8 doenças, regras ligadas a 12 fontes (F1 a F12), todas marcadas "suposição a validar"; fora do escopo: foot rot e diagnóstico definitivo. | C | 1:00 |
| 7 | Testes | 30 casos conhecidos rodam contra cada versão da base; ativar com casos falhando exige confirmação ([A] slide 13). | B | 0:45 |
| D | **Demonstração** (6.2.2) | O mesmo motor atende produtor e veterinário e explica cada conclusão. | C conduz; A e B comentam | 4:00 |
| 8 | Uso da IA e organização da equipe | Três pessoas, agentes diferentes por tarefa, revisão sempre por outra família de modelo, achados numéricos decididos por execução. | C, depois A e B (30 s cada) | 1:30 |
| 9 | Limitações e próximos passos | Conhecimento sem especialista, CF não calibrados, sem "por que não?"; próximos: validar com a RERUM/veterinário, calibrar com dados reais, sensores/APIs. | A | 0:45 |
| 10 | Encerramento e perguntas | O que aprendemos e onde a decisão sai: da base e do motor, nunca da LLM. | C | 0:15 |

Total dos slides: 10:00 mais a demo (4:00) = 14:00 **(suposição; ajustar quando a organização informar a duração)**. Slide 8 conteúdo: tabela agente por pessoa (A: Claude Code; B: Codex; C: Antigravity com agente de navegador; Gemini Pro para pesquisa, documentação e slides), skills (`obra/superpowers`: `test-driven-development`, `verification-before-completion`, `requesting-code-review`), 3 exemplos do log 6.1.3 (itens 2, 13 e 16) e uma linha sobre limites de janela de 5 h.

**Versão curta de 5 min (suposição):** fundir 1+2 (A, 0:30); 3+4 (B e A, 1:00); 6 (C, 0:30); 8 (C, 0:45); **demo reduzida a 2:00** (só o caso do produtor com bandeira + "como?" e o editor rodando casos, sem a troca de modo); 9 (A, 0:15). Slides 5 e 7 ficam como apoio para perguntas.

**Convenção visual (suposição):** um diagrama por slide, no máximo 3 linhas de texto, cada afirmação de domínio com o selo "suposição a validar". Fontes empacotadas, sem CDN (Seção 5.2).

### 6.2.2 Roteiro da demonstração (3 a 4 min, localhost:8000)

Preparo: `rodar.ps1` já em execução na máquina principal e na reserva (Seção 5.5 decisão 5); Wi-Fi desligado; fichas fictícias semeadas (um animal com parto há 1 dia, **suposição de que a semente o inclui**).

| Tempo | Passo | O que mostrar |
|---|---|---|
| 0:00–0:15 | Abrir Animais | Fichas fictícias; escolher a vaca com parto há 1 dia; **modo produtor** |
| 0:15–1:30 | **Caso do produtor com bandeira vermelha** (espelha C-HIP-01) | Tela de estado térmico: extremidades frias; tela de atitude: marcar **decúbito** → alerta com pausa ("chame um veterinário o mais rápido possível", regra R-BV-01) → *Continuar as perguntas* → o quadro urgente fica fixo no topo → parecer com hipocalcemia em "Hipóteses principais" e o aviso "porcentagem não é probabilidade" |
| 1:30–2:15 | **"Por quê?" e "Como?"** | Clicar "Por quê?" numa pergunta (motivo gravado no momento da escolha); "Como?" em hipocalcemia: regras R-HIP-01/02, derivado `periparto_imediato` vindo de `dias_em_lactacao`, combinação MYCIN antes/depois, origem `ficha` ou `resposta` |
| 2:15–3:00 | **Caso do veterinário** com **troca de modo** (espelha C-MODO-01) | Sessão nova no modo produtor: apetite reduzido, queda de produção, costelas saltadas; trocar para veterinário (respostas permanecem, limite passa de 12 para 25); informar temperatura 38,4 e "ping" positivo → deslocamento de abomaso em hipóteses principais, linguagem técnica |
| 3:00–3:50 | **Editor salvando versão e rodando casos** | Abrir o grafo; mudar o CF de R-MAS-02; (opcional) criar aresta que viola camadas e mostrar o erro `camada` bloqueando; salvar → nova versão → painel de casos: passou/falhou/mudou contra a versão pai; mostrar "Ativar" como ação separada |

Cortes se faltar tempo: tirar o erro de camada e a troca de modo (a versão curta já os omite). Cada passo tem um dono: C opera, A explica motor e "como?", B explica editor e versões **(suposição)**.

**Plano B (se a máquina falhar):** (1) máquina reserva com o mesmo preparo e servidor já no ar (Seção 5.5 decisão 5); (2) **vídeo gravado da demonstração** (3 a 4 min, mesmo roteiro, gravado na quinta 16–18 durante o ensaio 1, em duas cópias: no notebook e no celular, **suposição**); (3) PDF dos slides com capturas de tela de cada passo. O vídeo cobre falha de projetor ou de máquina, mas não substitui o localhost: se for usado, dizer isso à banca e oferecer a execução ao vivo assim que possível (Seção 5.2, item 5).

### 6.2.3 Perguntas prováveis da banca (respostas curtas)

1. **Por que não usar uma LLM?** Porque o desafio exige que a decisão saia de base explícita e motor ([A] slides 8 e 13): com regras e CF a decisão é determinística, auditável e repete exatamente. A IA entrou no desenvolvimento, não na execução.
2. **O CF é probabilidade?** Não. É grau de confiança do sistema (modelo MYCIN, de −1 a +1); a tela e o parecer dizem isso. Porcentagem = `max(0, CF) × 100`.
3. **Como validaram o conhecimento veterinário?** Ainda não por especialista: foi extraído de fontes públicas citadas (F1 a F12, em especial MSD Veterinary Manual) e cada regra está marcada `suposicao_a_validar`. Próximo passo: validação com a RERUM ou um veterinário.
4. **De onde vêm os CF?** São estimativas nossas, sem calibração com dados reais; por isso os casos usam faixas largas e os limiares ficam em `meta.limiares`, versionados.
5. **Como o sistema decide a próxima pergunta?** Por encadeamento para trás dirigido por objetivo: escolhe a variável que aparece em mais regras viáveis das hipóteses abertas, ponderada por |`cf_regra`|, com gravidade e `id` como desempate.
6. **O que acontece com vaca em estado grave?** Bandeira vermelha leva direto a `chamar_agora`, sem depender do CF das doenças, e a urgência não desce mais; no modo produtor a interface pausa com o alerta.
7. **Como garantem que editar a base não quebra nada?** Versões imutáveis, validação que bloqueia (ciclos, camadas, inalcançáveis) e 30 casos executados na nova versão e na pai; ativar com falhas exige confirmação explícita.
8. **Qual a diferença entre produtor e veterinário?** Nenhuma na lógica: mesma base e mesmo motor; mudam só o texto e as perguntas oferecidas, e a troca no meio da sessão preserva as respostas.
9. **Quais as limitações?** Oito doenças; sem "por que **não** é a doença X?"; foot rot fora do escopo; sensores e APIs fora do PoC; dados fictícios; conhecimento não validado.
10. **O que a equipe aprendeu / quem entende o quê?** Cada pessoa explica sua parte e uma parte alheia; mostrar o diário `docs/processo/` e o log de revisões, inclusive um achado de IA que refutamos com teste em aritmética exata (itens 1 e 13 do log).

---

## 6.3 Riscos e pontos em aberto

### 6.3.1 Tabela de riscos (probabilidade e impacto são estimativas, **suposição**)

| # | Risco | Prob. | Imp. | Mitigação | Dono |
|---|---|---|---|---|---|
| 1 | Conhecimento veterinário sem validação de especialista | alta | alto | Marcar tudo `suposicao_a_validar`; citar F1 a F12; avisar no parecer, na doc gerada e nos slides; tentar validação parcial (6.4, decisão 1); pedir à RERUM ([A] slide 13) | A |
| 2 | CF não calibrados (qualquer ajuste muda o resultado) | alta | médio | Faixas largas nos casos; limiares versionados em `meta`; calibração na quinta 08–12; explicar CF ≠ probabilidade | A |
| 3 | Prazo (2,5 dias, 3 pessoas) | média | alto | Plano de corte 5.4 (ordem: extras, importação, edição, 8→6 doenças); congelamentos quinta 12:00 e 14:00; marcos verificáveis; nunca cortar motor, triagem, parecer, por quê/como, casos, localhost, docs, apresentação | A (coordena marcos) |
| 4 | Limites de uso dos agentes (janelas de 5 h e limite semanal) | alta | médio | Antigravity de cada pessoa como reserva; Claude Code só no crítico, nunca em revisão; trabalhar em blocos, prompts enxutos, registrar consumo; Gemini Pro (3 assentos) para documentação | cada um (A pelo Claude Code) |
| 5 | Integração entre pessoas (motor × API × web) | média | alto | Contratos e exemplos congelados quarta 09:00; mocks para C; serviço falso para B; ligação quarta 18–20; dono por pasta; mudança de contrato = commit pequeno avisado | B |
| 6 | Ambiente Windows e demonstração offline | média | alto | `rodar.ps1 -SoPreparar` na máquina da demo até quinta 18:00; segunda máquina; sem CDN nem fontes externas; ensaio com Wi-Fi desligado quinta à noite e sexta 08:00; vídeo (plano B) | B |
| 7 | Licença das skills source-available (`pptx`, `docx` de anthropics/skills) | baixa | baixo | São ferramenta de produção de slides, não fazem parte da solução (**suposição**); se a banca discordar, Google Slides ou LibreOffice Impress; skills de código em `obra/superpowers` (MIT) | C |
| 8 | TypeScript e versões a confirmar na instalação (TS 5.x/6.x, não 7.0; ids `winget`; flag `--offline` do `uv`; rota coringa do FastAPI) | média | médio | Travar em `uv.lock` e `package-lock.json`; conferir na terça à noite (2 h); se o `openapi-typescript` falhar, fixar a versão do TS que ele aceita | C (web) e B (uv/FastAPI) |
| 9 | Regressão da base ao editar | média | alto | Versões imutáveis com `pai`; 30 casos na nova e na pai, mostrando passou/falhou/mudou; ativar com falhas exige `confirmar_falhas`; `tests/casos` antes da entrega | A |
| 10 | Falha no envio (anexo grande, e-mail ou WhatsApp) | média | alto | Alvo 18:30; dois canais; confirmar recebimento; pacote sem `.venv`/`node_modules`; PDFs separados se preciso | C |
| 11 | Equipe não dominar o que a IA gerou (passo 8 de [A] slide 12; perguntas da banca) | média | alto | Cada um explica sua parte e uma alheia no ensaio; diário `docs/processo/`; estudar o motor e as regras na quinta à tarde; lista 6.2.3 | todos |

### 6.3.2 Pontos em aberto que dependem de alguém de fora ou da instalação

**Dependem de fora:**
- Validação das regras, CF e limiares por veterinário ou zootecnista, ou técnico da RERUM ([A] slide 13). Sem isso, o status continua `suposicao_a_validar` em todas as regras.
- Duração da apresentação, tempo de demonstração e se haverá projetor, rede ou máquina fornecida: **não constam de [A]/[D]**; perguntar à organização antes de sexta.
- Tamanho máximo de anexo e formato aceito: não constam de [A]/[D]. Os canais (e-mail ou WhatsApp) e o contato de suporte estão em [A] slide 15.
- Nome e telefone dos três integrantes (a preencher no README).
- Se a banca usa casos de teste próprios para medir "assertividade" ([A] slide 3) **(suposição de que pode usar)**: pedir exemplos à RERUM, se possível.

**Dependem de confirmação na instalação (terça à noite):**
- Versões do `docs/pesquisa/versoes-bibliotecas.md` (pesquisadas em 20/10/2026); linha do TypeScript (5.x/6.x) compatível com `openapi-typescript`; Node 24 LTS; Vite 8 com o Node instalado.
- Ids do `winget` para `uv` e Node; flag `uv sync --frozen --offline`; função do FastAPI para servir a SPA (senão rota coringa); `playwright install chromium` no Windows.
- Fontes F1 a F5 e F7 a F11 conferidas só por resumo de busca (status R em `docs/fontes/fontes.md`): ler integralmente antes de citar na documentação.
- Limite do Deep Research do Gemini e comportamento do Antigravity CLI para AI Pro: não confirmados (`docs/pesquisa/agentes-e-skills.md`).
- Decisão da Seção 3.8 item 6 (`sem_problema` como resultado padrão, "a confirmar") e valores de CF dos 30 casos (estimados à mão; A confere na implementação).

---

## 6.4 Decisões tomadas pelo arquiteto

1. **Validação veterinária.** (a) Manter tudo `suposicao_a_validar` e dizê-lo na banca; (b) tentar até quinta 12:00 uma revisão parcial por veterinário ou RERUM e marcar `validada` só o que for revisado. **Decidido: (b),** como tentativa de baixo custo, caindo em (a) sem perda se ninguém responder.
2. **Formato do diário de IA.** (a) `docs/processo/<pessoa>.md` escrito à mão pelas três pessoas, curado; (b) exportar a transcrição bruta de cada agente e resumir depois. **Decidido: (a),** com anexos brutos só para os 3 a 5 prompts mais importantes por pessoa, porque a transcrição inteira é longa e some entre janelas de 5 h.
3. **Apresentadores.** (a) Três vozes (A, B, C) conforme 6.2.1; (b) um apresentador único e os outros só na demo e nas perguntas. **Decidido: (a),** pois [A] slide 5 avalia trabalho em equipe e liderança, e cada um defende a pasta que construiu.
4. **Formato de envio.** (a) `.zip` do código mais PDFs de documentação e slides, por e-mail com aviso no WhatsApp; (b) só o repositório compactado com a documentação em Markdown. **Decidido: (a),** pois PDF abre em qualquer máquina da banca e o zip leva o código reproduzível (`uv.lock`, `package-lock.json`).
