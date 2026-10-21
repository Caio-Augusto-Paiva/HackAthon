# Prompt de revisão — Seção 5: Testes, execução em localhost, cronograma e plano de corte

> **Agente:** Gemini Pro (app web) (alternativa: Antigravity da pessoa C). **Skills:** `writing-plans`, `test-driven-development` (obra/superpowers); `webapp-testing` (anthropics/skills) ou `playwright-skill` (lackeyjb, MIT). **Por quê:** o cronograma é revisão de raciocínio; os cenários ponta a ponta pedem conhecimento de Playwright. Ver `docs/agentes-e-skills.md`.

> Status da seção: **aprovada** (20/10/2026). Cole tudo abaixo da linha numa IA revisora.

---

Você vai atuar como **revisor técnico independente** da especificação de um sistema especialista (trabalho acadêmico, Hackathon UFJF 2026, tema "Anamnese de bovinos leiteiros em lactação"). Esta seção define a estratégia de testes em quatro camadas (com 30 casos conhecidos), a execução em localhost, o cronograma por pessoa até quinta 22/10 às 20:00 e o plano de corte. Verifique se o cronograma é realista para 3 pessoas com agentes de IA, se os casos esperados batem com as regras da Seção 3 e se algo obrigatório pelos organizadores ficou de fora. Não presuma que a seção está certa nem errada. Verifique por conta própria.

## Restrições obrigatórias do desafio (não são discutíveis)

1. Nenhuma LLM no caminho da decisão em tempo de execução.
2. Decisão determinística e auditável.
3. Open source.
4. Tudo roda em localhost.

## Decisões já tomadas (não reabra; aponte só se criarem contradição)

- D1. Implementação começa quarta 21/10 08:00 (terça à noite: até 2 h de preparo).
- D2. Entrega até quinta 22/10 às 20:00 por e-mail ou WhatsApp com nome e telefone de todos ([A] slide 15), alvo interno 18:30.
- D3. Apresentação e demonstração em localhost sexta 23/10 às 9:00.
- D4. Três pessoas (A motor, B API/validador/scripts, C web/e2e) com agentes de IA diferentes.
- D5. Documentação obrigatória: processo de desenvolvimento, arquitetura tecnológica e regras de produção ([A] slide 10).
- D6. O plano de corte nunca corta motor, triagem, parecer, por quê/como, casos de teste, localhost, documentação e apresentação.

## Como revisar

Para cada problema encontrado, responda:

1. **Veredito:** erro / lacuna / decisão em aberto / ressalva menor.
2. **Trecho exato** da seção que sustenta o veredito (se o texto não diz algo, é lacuna, não erro).
3. **Prova:** aponte bloco do cronograma sobrecarregado, caso cujo esperado contradiz as regras da Seção 3, ou comando que não funciona no Windows.
4. **Correção mínima:** uma frase ou parágrafo reescrito, sem mecanismos novos além do necessário.

Regras: não elogie por cortesia; diga qual pergunta responderia o que depender de informação que você não tem; ao final, liste problemas que não estão nesta lista e dê um resumo de 3 linhas do que precisa mudar.

---

## SEÇÃO 5 — Testes, execução em localhost, cronograma e plano de corte

> Siglas: **CA** = `chamar_agora`, **OB** = `observar`, **SP** = `sem_problema`. Faixas em porcentagem (`max(0, CF) × 100`). Tudo que não vem das Seções 1 a 4 ou de [A]/[D] está marcado **(suposição)**.

## 5.1 Estratégia de testes

### Visão geral (quatro camadas)

| Camada | Cobre | Pasta | Ferramenta | Comando | Quando roda |
|---|---|---|---|---|---|
| 1. Motor | cálculo de CF, avaliação, agenda, seleção, parada, parecer, traço | `tests/engine/` | pytest + hypothesis | `uv run pytest tests/engine -q` | a cada commit de A |
| 2. Validador e grafo | os erros e avisos da Seção 2, ida e volta regras ↔ grafo, camadas, ciclos | `tests/kb/` | pytest | `uv run pytest tests/kb -q` | a cada commit de A ou B; também ao salvar versão (via API) |
| 3. Casos conhecidos | `base/casos/casos.json` executado contra cada versão | `tests/casos/` | pytest (usa `engine/casos.py`) | `uv run pytest tests/casos -q` | antes de ativar versão; antes da entrega |
| 4a. Contrato da API | respostas e exemplos contra `contratos/openapi.json`; erros; sincronia dos tipos | `tests/api/` | pytest + httpx | `uv run pytest tests/api -q` | a cada commit de B; antes da entrega |
| 4b. Ponta a ponta | fluxos reais no navegador | `e2e/` | Playwright (Chromium) | `cd e2e && npx playwright test` **(suposição: `e2e/` com `package.json` próprio, para resolver `@playwright/test` sem depender de `web/node_modules`)** | quinta 12:00 em diante; antes da entrega |

Comando único antes de commitar: `uv run ruff check . && uv run pytest tests/engine tests/kb tests/casos tests/api -q`. Tempo-alvo: abaixo de 30 s **(suposição)**. Fixtures em `tests/fixtures/` (mini-bases, bases inválidas, prontuários fictícios). Dados fictícios apenas.

### Camada 1 — Unitários do motor (`tests/engine/`)

Lista da Seção 1, agrupada por arquivo. Cada teste usa mini-base própria em `tests/fixtures/`, nunca a base real.

| Arquivo | Testes |
|---|---|
| `test_cf.py` | embaralhar a ordem das evidências não muda o resultado (hypothesis, tolerância de ponto flutuante); caso +1/−1 sem exceção (guarda 0/0 retorna 0); derivado `max`: duas regras de 0,9 dão 0,9, não 0,99; as três formas de combinação (positivos, negativos, mistos) com valores exatos em `fractions` |
| `test_avaliacao.py` | `febre == não` com resposta "não" dispara; categórica/numérica: satisfaz → CF do fato, não satisfaz → −CF; premissa = mínimo; regra só dispara com premissa > 0,2; `cf_minimo 0,50`: doença em 0,49 não dispara a urgência, em 0,50 dispara; ordem das três camadas |
| `test_memoria.py` | tela de múltipla escolha grava um booleano por opção; "não sei" grava 0 em todos; fatos guardados por variável; corrigir resposta substitui o fato; trocar modo preserva fatos |
| `test_agenda.py` | ordem: prioridade, depois especificidade, depois id; urgência mais urgente vence; bandeira disparada nunca desce |
| `test_selecao.py` | modo produtor nunca escolhe pergunta por causa de regra inviável; variável exclusiva do veterinário não é perguntada no produtor, mas fato já respondido continua valendo; empate resolvido pela gravidade antes do id |
| `test_parada.py` | CF ≥ 0,80 com triagem incompleta não encerra; líder 0,85 e outra hipótese em 0,5 com potencial ≥ 0,70: continua; com potencial < 0,70: encerra e lista as duas; bandeira com condição ativada e outra pendente impede a parada; duas doenças ≥ 0,80 encerram juntas; hipótese > 0,35 cujo potencial depende só de variável do veterinário não bloqueia no produtor; o limite conta só perguntas dinâmicas; propriedade: potencial propagado por derivado ≥ CF alcançado em qualquer sequência de respostas (hypothesis) |
| `test_parecer.py` | 8 doenças sempre presentes, ordem decrescente com desempate por id; `percentual` e `situacao` (limites −0,2 e 0,2); três blocos nos cortes 50% e 20%; `sem_problema` só se nenhuma urgência disparou e todas ≤ 0,35, senão `observar` |
| `test_traco_explicacao.py` | os quatro tipos de evento; "por quê?" é o motivo gravado no evento da pergunta; "como?" percorre do resultado às respostas, com derivados aninhados |
| `test_inferencia.py` | determinismo (mesma entrada, mesmo resultado e mesmo traço); recalcular do zero após cada resposta dá o mesmo que acumular; nenhum import de `api`, `web` ou `sqlite3` em `engine/` (teste de arquitetura, **suposição**) |

**Definição de pronto (camada 1):** todos os testes da Seção 1 existem e passam; escritos antes do código de cada módulo (TDD); cobertura das linhas de `engine/` acima de 90% **(suposição)**; sem teste marcado `skip`.

### Camada 2 — Validador e grafo (`tests/kb/`)

| Arquivo | Testes |
|---|---|
| `test_validador_erros.py` | um teste parametrizado: cada arquivo `tests/fixtures/kb_invalidas/E##_*.json` deve produzir exatamente o erro de mesmo código e nenhum outro. E01 símbolo indefinido (condição, conclusão, tela); E02 id duplicado; E03 valor fora do domínio ou `op` incompatível; E04 `cf` fora de ±0,99; E05 ciclo; E06 regra inalcançável (inclui condição negada sobre derivado sem regra de CF negativo); E07 bandeira que não conclui `chamar_agora`; E08 bandeira sem condição de triagem; E09 doença sem regra; E10 doença sem regra só do produtor; E11 cobertura da triagem; E12 camadas; E13 doença sem `gravidade`; E14 derivado `max` com `cf` negativo; E15 `cf_minimo`/`cf_maximo` inválido; E16 tela de triagem sem texto em um modo; E17 limiares fora de ordem; E18 regra sem `fonte` |
| `test_validador_avisos.py` | símbolo perguntável nunca usado; duas regras com mesmas condições e sinais opostos; contagem de regras `suposicao_a_validar` |
| `test_analise.py` | ciclo direto e indireto; ordem topológica; classificação em camadas; alcançabilidade |
| `test_grafo.py` | ida e volta: `regras → grafo → regras` idêntico, byte a byte após ordenar, para a mini-base e para a base real; `cf_minimo`/`cf_maximo`/`negado` preservados nas arestas; mover nó altera só `layout`, nunca as regras |
| `test_carregador.py` | salvar cria `vNNNN.json` com `pai` e nunca sobrescreve; `ativa.json`; hash detecta arquivo alterado à mão |
| `test_base_real.py` | toda versão em `base/versoes/` valida sem erros; validar a base real não dispara E11 (cobertura) para nenhuma das 8 doenças; nenhuma regra usa condição negada sobre derivado de período |

**Definição de pronto (camada 2):** os 18 erros e os 3 avisos têm fixture e teste; ida e volta passa na base real; o validador roda sobre `v0001.json` sem erros.

### Camada 3 — Casos conhecidos (`tests/casos/` + `base/casos/casos.json`)

`tests/casos/test_casos_por_versao.py` parametriza versão × caso. A versão **ativa** deve passar todos; versões antigas só reportam (não falham o pytest) **(suposição, pois um caso pode ter sido criado depois delas)**. Execuções gravadas em `execucoes_casos`/`resultados_casos` (Seção 4.6).

**Convenções do executor (`engine/casos.py`), todas (suposição) a registrar na Seção 2:**
- pergunta dinâmica feita e ausente em `respostas` → `nao_sei`; resposta em `respostas` que o motor não pede (parou antes) → ignorada;
- bandeira com pausa → o executor registra `continuar` automaticamente; `esperado.bandeira` confere a regra;
- campos opcionais propostos para `Caso`: `continuacao` (modo, triagem extra, respostas) e `limite_dinamico` (substitui o de `meta` só na execução). Ver decisão 3 em 5.5;
- valores abaixo foram estimados à mão com os CF da Seção 3 v2; A confere na implementação e alarga a faixa se preciso. Faixas não listadas não são checadas.

**Padrões.** Ficha-padrão: `raca_grupo` cruzada, `retencao_placenta` e `parto_distocico` falsos, `historico_mastite_12m` falso, demais campos nulos. Triagem-padrão (TP): nada marcado, `apetite` normal; produtor com `extremidades` normal (febre −0,40), veterinário com `temperatura_retal` informada. Abaixo só aparecem os **desvios**. Todos os casos são inventados (**suposição a validar**).

| id | Descrição | Modo | Entradas principais (dias = `dias_em_lactacao`) | Esperado |
|---|---|---|---|---|
| C-MAS-01 | mastite típica | P | dias 90; leite_alterado, ubere_inflamado, queda_producao | OB; top1 mastite; mastite 75–100; parada confirmacao |
| C-MAS-02 | mastite típica com sinais sistêmicos | V | dias 150; temp 40,2; apatia, leite_alterado, ubere_inflamado; apetite reduzido; cmt_positivo sim | CA (R-BV-05); top1 mastite; mastite 75–100; tpb 0–45 |
| C-MAS-03 | mastite ambígua | P | dias 90; só ubere_inflamado; caneca não sei; um_quarto não | OB; top1 mastite; mastite 45–75 |
| C-MET-01 | metrite típica | P | dias 6; corrimento_vaginal; apetite reduzido; extremidades quente; corrimento_fetido sim; ficha retencao_placenta sim | CA; top1 metrite; metrite 75–100 |
| C-MET-02 | metrite típica | V | dias 8; temp 39,9; corrimento_vaginal; apetite reduzido; utero_aumentado_palpacao sim | CA; top1 metrite; metrite 75–100; hipocalcemia 0–10 |
| C-MET-03 | metrite ambígua (sensível ao limiar 0,50) | P | dias 12; só corrimento_vaginal; corrimento_fetido não sei | CA; top1 metrite; metrite 45–75 |
| C-TPB-01 | TPB típica | P | dias 100; ficha raca europeia; extremidades quente; apatia, urina_escura; mucosas_palidas sim; carrapatos sim | CA (R-BV-02); top1 tpb; tpb 70–100 |
| C-TPB-02 | TPB típica | V | dias 200; temp 40,1; apatia, urina_escura; esfregaco_hemoparasita sim; mucosas sim | CA (R-BV-02); top1 tpb; tpb 85–100 |
| C-TPB-03 | TPB ambígua | P | dias 100; ficha europeia; extremidades quente; apatia; carrapatos sim; mucosas não sei | OB; top3_contem tpb; tpb 30–50 |
| C-CET-01 | cetose típica | P | dias 25; apetite reduzido; queda_producao; fezes_ressecadas; sinais_nervosos sim; perda_condicao_corporal sim | OB; top1 cetose; cetose 75–100; deslocamento_abomaso 0–50 |
| C-CET-02 | cetose típica | V | dias 30; temp 38,6; apetite reduzido; queda_producao; fezes_ressecadas; bhb 1,8; ping não; costelas não | OB; top1 cetose; cetose 85–100; deslocamento_abomaso 20–55 |
| C-CET-03 | cetose ambígua | P | dias 20; apetite reduzido; queda_producao; abdomen_vazio não sei | OB; top3_contem cetose e deslocamento_abomaso; cetose 35–60 |
| C-HIP-01 | hipocalcemia típica, vaca caída | P | dias 1; decubito; extremidades fria | CA (R-BV-01); top1 hipocalcemia; hipocalcemia 80–100; parada confirmacao |
| C-HIP-02 | hipocalcemia típica, sem decúbito | V | dias 2; temp 37,2; apatia; apetite reduzido; calcio 1,1 | CA (R-BV-04); top1 hipocalcemia; hipocalcemia 85–100 |
| C-HIP-03 | hipocalcemia ambígua | P | dias 2; extremidades fria; fraqueza_tremores não sei | OB; top1 hipocalcemia; hipocalcemia 25–50 |
| C-DAB-01 | deslocamento de abomaso típico (produtor não vê o ping) | P | dias 35; apetite reduzido; queda_producao; costelas_esquerdas_saltadas sim | CA; top1 deslocamento_abomaso; deslocamento_abomaso 50–75; cetose 35–60 |
| C-DAB-02 | deslocamento de abomaso típico | V | dias 20; temp 38,5; apetite reduzido; queda_producao; ping_flanco_esquerdo sim | CA; top1 deslocamento_abomaso; deslocamento_abomaso 85–100; cetose 35–60 |
| C-DAB-03 | deslocamento de abomaso ambíguo | P | dias 35; apetite reduzido; costelas sim | OB; top1 deslocamento_abomaso; deslocamento_abomaso 30–55 |
| C-ACI-01 | acidose típica | P | dias 80; diarreia; apetite reduzido; mudanca_dieta_recente sim; graos_nas_fezes sim | OB; top1 acidose; acidose 75–100 |
| C-ACI-02 | acidose típica | V | dias 60; temp 38,7; diarreia; apatia; apetite reduzido; ph_ruminal 5,2 | OB; top1 acidose; acidose 85–100 |
| C-ACI-03 | acidose ambígua | P | dias 80; só diarreia; mudanca_dieta não sei; graos sim | OB; top1 acidose; acidose 40–60 |
| C-DD-01 | dermatite digital típica | P | dias 150; claudicacao; ferida_vermelha_entre_unhas sim | OB; top1 dermatite_digital; dermatite_digital 80–100 |
| C-DD-02 | dermatite digital típica | V | dias 150; temp 38,5; claudicacao; lesao_dd_ativa sim | OB; top1 dermatite_digital; dermatite_digital 85–100 |
| C-DD-03 | dermatite digital ambígua (sinal contra exclusão de foot rot) | P | dias 150; claudicacao; ferida sim; inchaco_simetrico_acima_casco sim; casos_podais não sei | OB; top1 dermatite_digital; dermatite_digital 60–90 |
| C-BV-01 | decúbito na triagem, sem doença que o explique (urgência independe do CF) | P | dias 200; decubito, apatia | CA (R-BV-01), alerta com pausa; todas as doenças 0–35 |
| C-BV-03 | febre muito alta isolada | V | dias 100; temp 41,3 | CA (R-BV-06); todas as doenças 0–35 |
| C-COM-01 | comorbidade mastite + metrite | P | dias 5; corrimento_vaginal, leite_alterado, ubere_inflamado; corrimento_fetido sim | CA; top3_contem mastite e metrite; ambas 75–100; parada confirmacao |
| C-MODO-01 | troca de modo sem perder respostas | P→V | dias 40; produtor: apetite reduzido, queda_producao, costelas sim; continuação veterinário: temp 38,4, ping sim | CA; top1 deslocamento_abomaso; deslocamento_abomaso 85–100; cetose 35–60 |
| C-LIM-01 | parada por limite (caso vago) | P | dias 10; apetite reduzido, queda_producao, diarreia, claudicacao; `limite_dinamico` 3; respostas não sei | OB; motivo_parada limite; `inconclusivas` contém cetose, acidose, dermatite_digital; cetose 35–70 |
| C-SAD-01 | animal saudável | P | dias 120; TP | SP; todas as doenças 0–20; motivo_parada em {sem_potencial, sem_perguntas} **(suposição)** |

Cobertura da Seção 2: 8 doenças × (2 típicos + 1 ambíguo) = 24; bandeira (C-BV-01 com decúbito, C-BV-03, e as bandeiras R-BV-02/04/05 dentro de C-TPB-0x, C-HIP-02, C-MAS-02); comorbidade; troca de modo; parada por limite; saudável. Total: **30**. Observação à Seção 3: a tabela 3.4 diz 7 perguntas exclusivas do veterinário, mas a lista traz 8 (`cmt_positivo`, `utero_aumentado_palpacao`, `esfregaco_hemoparasita`, `bhb_sanguineo`, `calcio_sanguineo`, `ping_flanco_esquerdo`, `ph_ruminal`, `lesao_dd_ativa`); corrigir o número.

**Definição de pronto (camada 3):** 30 casos na versão ativa, todos passando (ou falha documentada com decisão do arquiteto); cada doença com 2 típicos e 1 ambíguo; execução registrada no SQLite; rodar a suíte inteira em menos de 10 s **(suposição)**.

### Camada 4a — Contrato da API (`tests/api/`)

| Arquivo | Testes |
|---|---|
| `test_exemplos.py` | cada `contratos/exemplos/*.json` valida contra o schema Pydantic da rota |
| `test_contrato_openapi.py` | respostas reais validam contra `contratos/openapi.json`; regenerar `openapi.json` e `tipos.gerado.ts` e comparar com o commitado (Seção 4.7 item 4) |
| `test_erros.py` | um teste por linha da tabela de erros da 4.4 (404, 409 ×4, 422 ×5, 500), todos no formato `{ "erro": {...} }` |
| `test_sessoes.py` | fluxo completo com serviço falso e, depois, com motor real; `revisao` sobe; PATCH de modo preserva respostas; sessão presa à `versao_base`; POST em tela já respondida → `ja_respondida`; pergunta de veterinário no modo produtor → `resposta_invalida`; bandeira: `pausa` só no produtor |
| `test_base.py` | validar sem salvar; salvar com erro → 422 `base_invalida` e nada gravado; salvar válido roda casos em nova e pai; ativar com casos falhando → 409 `casos_falhando`, com `confirmar_falhas` → 200 |
| `test_animais.py` | CRUD, brinco duplicado → 409; importação CSV e JSON, `gravar=false` não grava, linhas rejeitadas |

**Definição de pronto (camada 4a):** todas as rotas "núcleo" da tabela 4.5 cobertas; 100% dos códigos de erro da 4.4; teste de sincronia dos tipos verde.

### Camada 4b — Ponta a ponta (`e2e/`)

Banco e pasta `base/` temporários por execução, copiados de uma fixture (variáveis de ambiente lidas por `api/config.py`, **suposição**). `webServer` do Playwright sobe o uvicorn na :8000 e espera `/api/saude`.

| # | Cenário | Passos |
|---|---|---|
| E2E-01 | Anamnese do produtor até o parecer | abrir Animais → escolher "Mimosa" → iniciar em modo produtor → responder as 6 telas (leite alterado e úbere inflamado) → ver quadro de urgência → parecer com blocos e aviso "não é probabilidade" → clicar "Por quê?" numa pergunta e "Como?" em mastite e ver as regras R-MAS-01 e R-MAS-02 |
| E2E-02 | Bandeira vermelha com pausa | iniciar produtor → tela 3 marcando decúbito → aparece alerta com pausa e texto "chame um veterinário" → "Continuar as perguntas" → alerta some e o quadro urgente fica no topo → repetir e escolher "Ver parecer" |
| E2E-03 | Troca de modo | produtor responde triagem e 1 pergunta → trocar para veterinário → progresso e respostas continuam → responder temperatura e pergunta do veterinário → parecer em linguagem técnica com a mesma urgência |
| E2E-04 | Importação de prontuário | tela Animais → importar `tests/fixtures/prontuario.csv` com simulação → ver criados, atualizados e rejeitados → confirmar gravação → animal novo aparece, campo `origem: importacao` visível no "Como?" |
| E2E-05 | Editor: salvar versão e rodar casos | abrir Editor → ver grafo → mudar o CF de R-MAS-02 → criar uma aresta que viola as camadas (doença → regra de outra doença) → painel de validação mostra o erro `camada` e bloqueia salvar → remover a aresta → salvar (v0002) → painel de casos mostra passou/falhou/mudou → ativar |
| E2E-06 | Corrigir resposta anterior | no meio da fase dinâmica voltar a uma tela, corrigir (PUT) → parecer recalculado, nenhuma resposta perdida |

**Definição de pronto (camada 4b):** os 6 cenários verdes em Chromium, em máquina limpa, sem internet **(suposição: `--offline` do Chromium não é necessário; basta Wi-Fi desligado)**; cada falha gera trace do Playwright em `e2e/test-results/` **(suposição)**. Se o prazo apertar, os cenários 01, 02 e 05 são o mínimo (ver 5.4).

## 5.2 Execução em localhost

### Pré-requisitos (Windows 11, **suposição** de que a demonstração roda em Windows)
Git; `uv` (`winget install --id astral-sh.uv -e`, **suposição de id**); Node 24 LTS (`winget install OpenJS.NodeJS.LTS`, **suposição de id**; confirmar a linha 24); Chromium do Playwright. Python 3.14 é instalado pelo `uv`. Nenhum Docker.

### Preparo único (com internet; terça à noite e repetir na máquina da demo)
```
git clone <repositório> hackatom && cd hackatom
uv sync --frozen
npm --prefix web ci
npm --prefix web run build
npm --prefix e2e ci
cd e2e && npx playwright install chromium && cd ..
powershell -ExecutionPolicy Bypass -File scripts\rodar.ps1 -SoPreparar
```
`-SoPreparar` **(suposição de nome)** executa as etapas 1 a 4 abaixo sem subir o servidor.

### Execução diária (2 comandos, README)
```
powershell -ExecutionPolicy Bypass -File scripts\rodar.ps1
```
Abre `http://localhost:8000`. Em Linux/macOS: `scripts/rodar.sh` (mesmo roteiro; fora da demo).

### O que `scripts/rodar.ps1` faz
1. Confere `uv` e `node` no PATH; se faltar, aborta com mensagem em português.
2. `uv sync --frozen` (rápido se `.venv` já existe; com `-Offline`, usa `uv sync --frozen --offline`, **suposição de flag**).
3. Se `web/dist` não existe ou `web/src` é mais novo: `npm --prefix web ci` (se faltar `node_modules`) e `npm --prefix web run build`.
4. Se o arquivo SQLite não existe: cria o esquema (`api/db/esquema.sql`) e semeia animais fictícios (`scripts/semear_fictícios`); `-Reset` apaga e recria.
5. Sobe `uv run uvicorn api.main:app --host 127.0.0.1 --port 8000`.
   O `api/main.py` serve `web/dist` e devolve `index.html` para qualquer rota fora de `/api` (rota coringa), para o React funcionar ao recarregar a página. Se a versão instalada do FastAPI tiver função própria para isso, pode substituir a rota coringa (a confirmar na instalação; ver `docs/pesquisa/execucao-local.md`).
6. Espera `GET /api/saude` responder (até 30 s **(suposição)**), imprime a URL e abre o navegador padrão. Ctrl+C encerra.

### Modo desenvolvimento
- Backend: `uv run uvicorn api.main:app --reload --port 8000`.
- Frontend: `npm --prefix web run dev` → Vite em `http://localhost:5173`, proxy `/api` → `:8000` (`web/vite.config.ts`).
- Sem backend (C trabalhando sozinho): variável de ambiente que ativa `web/src/api/mocks/` lendo `contratos/exemplos/` **(suposição: `VITE_USAR_MOCKS=1`)**.
- Depois de mudar um schema: `scripts/gerar_tipos` e commit dos arquivos gerados (4.7).

### Garantir que a demonstração roda sem internet
1. Todo o preparo (clone, `uv sync`, `npm ci`, build, `playwright install`) acontece com rede, na própria máquina da demo, até **quinta 18:00**.
2. O build do `web` não pode referenciar CDN, Google Fonts ou imagens externas: fontes do sistema ou empacotadas; `grep -rn "http" web/src web/index.html` revisado a mão **(suposição)**.
3. Nenhuma chamada de rede no backend (não há LLM no caminho; o motor é Python puro).
4. Ensaio **com Wi-Fi desligado**: `rodar.ps1` do zero (apagando `web/dist` e o `.db`), E2E-01 e E2E-05 manualmente. Feito na quinta à noite e na sexta às 08:00 **(suposição de horário)**.
5. Plano B: segunda máquina com o mesmo preparo; vídeo curto de gravação da demonstração (resolve falha de projetor, não substitui o localhost).
6. `.venv` e `node_modules` ficam fora do git; o repositório entregue leva `uv.lock` e `package-lock.json` (reprodutível).

## 5.3 Cronograma (blocos de ~2 h)

Pessoas e pastas (Seção 4.8): **A** = `engine/`, `kb/`, `tests/engine`, `tests/kb`; **B** = `api/`, `tests/api`, `scripts/`; **C** = `web/`, `e2e/`. B assume `kb/validador.py`, `kb/grafo.py` e `tests/kb` (decisão 1 de 5.5; a Seção 4.8 já foi ajustada). Antes do código de cada módulo vem o teste. Cada pessoa registra prompts e decisões em `docs/processo/<pessoa>.md` **(suposição)** (insumo da documentação de processo e da apresentação).

| Bloco | A (motor e base) | B (API, validador, scripts) | C (web e e2e) |
|---|---|---|---|
| **Ter 20/10 noite (≤ 2 h, suposição)** | instalar uv/Node; criar repo, `pyproject.toml` e esqueleto `engine/` e `kb/`; pytest rodando com 0 testes | `api/main.py` com `/api/saude`; esqueleto de `scripts/rodar.ps1` | scaffold Vite + React + TS; `npm run build` ok; Playwright instalado |
| Marco terça | repositório compartilhado; os três rodam `rodar.ps1` e veem a página servida pelo FastAPI | | |
| **Qua 08–10** | `kb/modelos.py` (Pydantic) e `carregador.py`; `engine/cf.py` e `memoria.py` com testes primeiro | **Passo 0:** `api/schemas/`, `contratos/exemplos/`, `openapi.json`, tipos (até 09:00); esquema SQLite | `cliente.ts`, mocks, tipos gerados, rotas e páginas Animais; `TelaTriagem` |
| **Qua 10–12** | `avaliacao.py`, `kb/analise.py` (camadas, ciclos) com testes | `kb/validador.py` e `kb/grafo.py` com `tests/kb` (precisa de `modelos.py` às 10:00); rotas de animais | `PerguntaDinamica`, `SeletorModo`, página Anamnese (contra mocks) |
| **Qua 12–14** | `agenda.py`, `inferencia.py` (3 camadas), `traco.py` | rotas de sessões com serviço falso (lê exemplos); `tests/api` de contrato | `AlertaBandeira`, `QuadroUrgencia`, `ParecerBlocos` |
| **Qua 14–16** | `selecao.py`, `parada.py` com os testes da Seção 1 | `base/versoes/v0001.json` (transcrição das Seções 3.3 a 3.7 por agente mecânico) validada pelo validador; rotas de base | `PorQue`, `Como`, página Parecer |
| **Qua 16–18** | `parecer.py`, `explicacao.py`, `casos.py`; **gatilho 18:00: `tests/engine` verdes** | `sessao_servico` contra a interface do motor; `importacao.py`; `rodar.ps1` completo | Editor em leitura: `CanvasGrafo`, `NoSimbolo`, `NoRegra`, dagre |
| **Qua 18–20** | ligação: depurar `v0001` contra o motor real | troca o serviço falso pelo `inferencia.py` de A | desliga os mocks; E2E-01 e E2E-02 |
| Marco quarta 20:00 | **fluxo produtor ponta a ponta com motor real** (triagem, perguntas, parecer, por quê/como) sobre `v0001` válida | | |
| Qua 20–22 | folga opcional (não planejar trabalho; evita desgaste) | | |
| **Qui 08–10** | `casos.json` (30 casos da 5.1, mecânico) e `tests/casos`; primeira calibração de CF | `POST /base/versoes`, `PUT /base/ativa`, execuções; `tests/api` de base | Editor nível B: `PainelPropriedades`, `PainelMeta` |
| **Qui 10–12** | calibração até 30/30; revisão das regras contra a Seção 3 | importação (CSV/JSON); `tests/api` de importação | `PainelValidacao`, `PainelCasos`, salvar e ativar; E2E-03 a E2E-05 |
| **Qui 12:00** | **congelamento de funcionalidades:** só correções e documentação | | |
| Marco 12:00 | `casos.json` 30/30 na ativa; editor salva e roda casos; E2E-01 a E2E-03 verdes | | |
| **Qui 12–14** | corrigir falhas; começar texto de regras de produção (gerado da base) | corrigir falhas; E2E-04 a E2E-06 | corrigir falhas; esqueleto dos slides |
| **Qui 14:00** | **congelamento de código:** só correção de bug; tag `entrega-rc1` | | |
| **Qui 14–16** | documentação: motor e **regras de produção** | documentação: **arquitetura tecnológica**, README, execução | documentação: **processo de desenvolvimento** (uso da IA por pessoa); slides |
| **Qui 16–18** | slides do motor e da base; ensaio 1 (A cronometra) | verificação a frio: clone limpo, `rodar.ps1`, Wi-Fi desligado; suíte completa + E2E | slides de interface e de uso da IA; ensaio 1 |
| **Qui 18:00–18:30** | empacotar (tag `entrega`, zip sem `.venv`/`node_modules`, documentação, slides) e **enviar** por e-mail ou WhatsApp com nome e telefone dos três ([A] slide 15); confirmar recebimento | | |
| Qui 18:30–20:00 | margem (prazo 20:00) e ensaio 2; sem mudar código | | |
| Sex 23/10 08:00 | ensaio offline na máquina da demo; apresentação às 09:00 | | |

**Marcos verificáveis:** terça `rodar.ps1` abre a página; quarta 09:00 contratos congelados e tipos gerados; quarta 18:00 `tests/engine` verdes; quarta 20:00 produtor ponta a ponta com motor real; quinta 12:00 30/30 casos, editor salva e roda casos; quinta 14:00 código congelado; quinta 18:30 enviado.

## 5.4 Plano de corte

Corte da primeira linha para baixo. A lista **não** corta: motor, triagem, parecer, "por quê?/como?", casos de teste, execução em localhost, as três peças de documentação e a apresentação (são exigências de [A] slides 8 e 10 e a base da avaliação).

| # | Cortar | Gatilho | A demo perde | Ganho (suposição) |
|---|---|---|---|---|
| 1 | Rotas **extra** (`/traco`, `/animais/{id}/sessoes`, listagem de execuções) e a página de histórico | não implementar antes do marco de quarta 20:00; só se sobrar tempo depois | histórico de anamneses por animal e traço bruto na tela; "como?" cobre a auditoria | 2 h (B e C) |
| 2 | E2E-06 e E2E-04 reduzidos a teste de API; e2e fica com 01, 02, 03, 05 | quinta 10:00 e `tests/api` ainda não está verde | nenhuma perda visível na demo; menos rede de segurança | 1,5 h (C) |
| 3 | Importação de prontuário: primeiro só JSON sem CSV; depois cortar a tela (ficha vem da semente) | quinta 10:00 sem `tests/api` de importação verde (passo a); quinta 12:00 sem fluxo na tela (passo b) | componente "fontes de dados externas" ([A] slide 14) fica só na semente de fichas e na API; dizer isso na apresentação | 2 h (B e C) |
| 4 | Editor nível B → A (só visualizar e validar, sem editar na tela): primeiro tirar adicionar/remover nós e arestas (passo a), depois a edição de CF/texto (passo b) | quarta 18:00 `CanvasGrafo` não lê o grafo real (passo a); quinta 10:00 `PainelPropriedades` não salva (passo b) | edição visual da base ("aquisição de conhecimento"); a nova versão passa a ser demonstrada editando o JSON em `base/versoes` e rodando os casos pelo `PainelCasos` | 3 a 4 h (C e B) |
| 5 | Troca de modo no meio da sessão (PATCH) vira escolha só no início | quarta 20:00 sem E2E-03 verde | uma das decisões D6 (mesma base, dois modos) fica demonstrada só entre sessões, não em uma | 1 h (B, C) |
| 6 | De 8 para 6 doenças: remover dermatite digital e acidose, com suas regras e casos (-6) | quarta 20:00 sem fluxo ponta a ponta com motor real, ou quinta 10:00 com mais de 8 casos falhando | menos cobertura de domínio; escopo D1 reduzido (decisão do arquiteto) | 3 h (A) |

Ordem do que protege a nota: a avaliação premia assertividade e potencial de resolver o problema ([A] slides 3 e 11); por isso a lista corta periferia (extras, importação, edição) antes de reduzir o núcleo clínico.

### 5.5 Decisões tomadas pelo arquiteto

1. **Quem é dono de `kb/validador.py`, `kb/grafo.py` e `tests/kb/`?** (a) A mantém (4.8 como está); (b) B assume. **Decidido: (b).** A já carrega motor, parada, parecer, casos e 30 casos para calibrar, e B fica ocioso na quarta de manhã esperando o motor.
2. **Lacuna na Seção 3:** R-MET-06 (`puerperio = não`) e R-CET-08 (`inicio_lactacao = não`) nunca disparam, porque R-DER-02 e R-DER-03 só emitem evidência positiva e, com `dias_em_lactacao` = 120, o derivado fica em CF 0, não −1. (a) trocar as condições por `dias_em_lactacao > 21` e `> 42`, como R-HIP-06; (b) criar regras derivadas negativas (−0,99). **Decidido: (a).** não cria regra nem símbolo novo e preserva as três camadas. Aplicado na Seção 3 (R-MET-06 e R-CET-08) e generalizado no validador da Seção 2.
3. **Onde ficam os casos de troca de modo e de parada por limite?** (a) em `casos.json`, com campos opcionais `continuacao` e `limite_dinamico` no modelo `Caso`; (b) em testes pytest dedicados, fora do `casos.json`. **Decidido: (a).** o `PainelCasos` do editor só enxerga o que está em `casos.json`, e a Seção 2 exige esses dois casos no conjunto.
4. **Alvo interno de envio na quinta:** (a) 18:30 (margem de 1 h 30 antes das 20:00); (b) 19:30. **Decidido: (a).** e-mail com anexo grande e WhatsApp falham de forma imprevisível, e ensaio e ajuste fino podem vir depois do envio, sem mudar código.
5. **Máquina da demonstração:** (a) só a do apresentante, com preparo único; (b) duas máquinas com o mesmo preparo. **Decidido: (b).** se `rodar.ps1 -SoPreparar` funcionar em um comando (custo de 30 min), porque a sexta às 09:00 não admite reinstalação.

### 5.6 Impacto nas Seções 2, 3 e 4 (já aplicado)
- Seção 2: `Caso` ganha `continuacao` e `limite_dinamico` opcionais e as convenções do executor; o validador trata como erro a condição negada sobre derivado sem regra de CF negativo.
- Seção 3: R-MET-06 e R-CET-08 testam `dias_em_lactacao > 21` e `> 42`; são 8 (não 7) perguntas exclusivas do veterinário.
- Seção 4.8: B assume `kb/validador.py`, `kb/grafo.py` e `tests/kb`.
