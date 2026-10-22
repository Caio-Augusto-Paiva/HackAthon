# Frontend `web/` (React) — Plano de implementação

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:executing-plans (Codex) task-by-task, com `impeccable` ativo em toda edição de UI. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** aplicação React + TypeScript em `web/` que reproduz o protótipo do Figma (anamnese no estilo Akinator) e conversa de verdade com a API FastAPI e o motor, rodando em `http://localhost:8000`.

**Architecture:** SPA Vite servida pelo próprio FastAPI (`web/dist`, montado por `api/frontend.py`). O backend dita a próxima tela (`EstadoSessao.proxima`); o frontend só renderiza, envia respostas e mostra explicações. Tipos gerados do `contratos/openapi.json`; nada de regra clínica ou cálculo de CF no cliente.

**Tech Stack:** Node 24 LTS, Vite 8, React 19, TypeScript 5.x (não usar 7.0), React Router 7, `openapi-typescript` 7, Vitest + Testing Library + jsdom, `@playwright/test` 1.64, `@fontsource/varela-round` e `@fontsource/nunito-sans` (fontes locais, sem CDN). Sem TanStack Query, sem biblioteca de componentes, sem CSS-in-JS: CSS Modules + variáveis CSS.

**Spec:** `docs/superpowers/specs/2026-10-20-anamnese-bovinos-design.md` (Seção 4.4, 4.5, 4.7, 5.1 camada 4b, 5.2) + `api/README.md` (seção "Para o frontend") + Figma `https://www.figma.com/design/MUiGJ81WjX97iyjX0yE6jz/HackAtom` (página "Protótipo").

## Global Constraints

- Tudo roda em LOCALHOST, sem nuvem e sem CDN: fontes via `@fontsource`, ícones como SVG inline. Nenhuma LLM no caminho da decisão.
- **Não editar** `api/`, `engine/`, `kb/`, `base/`, `contratos/`, `tests/api/`, `tests/engine/`, `tests/kb/`. Se a API não expuser algo necessário, registre o pedido em `docs/entrega/06-riscos-e-pendencias.md` e siga sem ele.
- O cliente **nunca envia CF**. Envia `valor` ou `"nao_sei": true`.
- Tipos só de `web/src/api/tipos.gerado.ts` (gerado; não editar à mão). Tipagem estrita (`"strict": true`, sem `any`).
- Textos em português do Brasil, com acento; termos do produto: "verificação", "modo especialista" (= `modo: "veterinario"` na API), "modo produtor" (= `"produtor"`), "parecer", "Por que estou perguntando isso?".
- Fidelidade ao Figma (modo Dev): tokens `cor/*` da coleção "Tokens" viram variáveis CSS com o mesmo nome (`--cor-fundo-escuro` etc.); Varela Round nos títulos, Nunito Sans no resto; raio 18–32 px; sombra claymórfica macia (drop shadow com desfoque + duas inner shadows), **nunca** sombra dura sem desfoque.
- Acessibilidade: contraste ≥ 4,5:1, foco visível em tudo, alvos ≥ 44 px, radio/checkbox nativos (estilizados) com `<fieldset>/<legend>`, modal com foco preso e `Esc` só onde a ação é segura, `prefers-reduced-motion` respeitado, `lang="pt-BR"`.
- Entrada numérica: `inputmode="numeric"` (ou `decimal` quando o domínio tiver casas), filtra no cliente com `^[0-9]{1,6}([.,][0-9]{1,3})?$`, mas **a regra é do backend** (422 `resposta_invalida` é exibido no campo). Nunca concatenar entrada em URL; IDs de rota sempre com `encodeURIComponent`.
- Comandos: `cd web && npm ci && npm run gerar-tipos && npm test && npm run build`; e2e `npx playwright test` com a API em `:8000`.

## Review Focus

1. **409 `conflito` / `ja_respondida` por duplo clique** → o botão fica desabilitado durante o envio; ao receber 409, faz `GET /api/sessoes/{id}` e re-renderiza sem mensagem de erro técnica (teste na Task 4).
2. **Número inválido digitado** (`12,5` em dias, `1e3`, colado com espaço) → mensagem no campo "Use só números…" vinda do 422, botão volta a habilitar, nada avança (Task 2 e Task 4).
3. **`proxima: null` com `alerta.pausa`** (bandeira no modo produtor) → abre o modal de alerta, não uma tela vazia (Task 5).
4. **API fora do ar / sem base ativa (409 em `POST /sessoes`)** → tela de início mostra erro amigável com "Tentar de novo", nunca tela branca (Task 3).
5. **Sessão encerrada por `ver_parecer` ou por parada do motor** → vai ao parecer; "Continuar respondendo" reabre e volta à pergunta (Task 5/6).

---

## Mapa de arquivos

| Arquivo | Responsabilidade |
|---|---|
| `web/package.json`, `vite.config.ts`, `tsconfig.json`, `index.html` | projeto; proxy `/api` → `http://127.0.0.1:8000`; build em `web/dist` |
| `web/src/api/tipos.gerado.ts` | gerado por `openapi-typescript ../contratos/openapi.json` |
| `web/src/api/cliente.ts` | `fetch` tipado, erro único → `ErroApi` |
| `web/src/api/sessao.ts` | funções por operação (`criarSessao`, `responderTriagem`…) |
| `web/src/estilo/tokens.css`, `global.css` | variáveis do Figma, reset, foco, seleção, scrollbar |
| `web/src/componentes/*` | `Botao`, `OpcaoResposta`, `CampoNumerico`, `BarraConfianca`, `Boi`, `Balao`, `BarraProgresso`, `Modal` |
| `web/src/anamnese/*` | `TelaTriagem`, `PerguntaDinamica`, `BarraHipoteses`, `AlertaBandeira`, `PorQue`, `mapearResposta.ts` |
| `web/src/paginas/*` | `Inicio`, `Anamnese`, `Parecer` |
| `web/e2e/*.spec.ts` | Playwright |

---

### Task 1: Projeto, tokens, cliente da API

**Files:** Create `web/` (Vite React TS), `web/src/estilo/*`, `web/src/api/cliente.ts`, `web/src/api/cliente.test.ts`, `web/.gitignore` (`node_modules`, `dist`); Modify raiz `.gitignore` se precisar.

**Interfaces — Produces:**
- `class ErroApi extends Error { status: number; codigo: string; requisicaoId: string; detalhes: Detalhe[] }`
- `async function chamar<T>(metodo: 'GET'|'POST'|'PUT'|'PATCH', caminho: string, corpo?: unknown): Promise<T>` — prefixa `/api`, JSON, lança `ErroApi` a partir de `{erro:{codigo,mensagem,requisicao_id,detalhes}}`; erro de rede vira `ErroApi(status 0, codigo 'sem_conexao')`.
- Scripts npm: `dev`, `build`, `test`, `gerar-tipos`, `e2e`.

- [ ] **Step 1:** Antes de qualquer UI, rode o setup do impeccable (`<skill>/scripts/impeccable context`); como não há `PRODUCT.md`, rode `/impeccable init` respondendo a partir deste plano e do protótipo (produto: triagem explicável de vaca leiteira; usuários: produtor e veterinário; tom: lúdico como Akinator, mas sério na gravidade) e depois `/impeccable document` **a partir do Figma** para gerar `DESIGN.md` (tokens, tipografia, sombra claymórfica, componentes). Commit `docs: PRODUCT.md e DESIGN.md do frontend`.
- [ ] **Step 2: Testes que falham** (`cliente.test.ts`, `fetch` mockado): `lança ErroApi com codigo e requisicaoId do corpo de erro`; `erro de rede vira codigo sem_conexao`; `GET devolve o JSON tipado`.
- [ ] **Step 3:** `npm test` → FAIL (módulo inexistente).
- [ ] **Step 4:** Implementar cliente, `tokens.css` com as 16 variáveis `cor/*` do Figma (valores em `get_variable_defs` do modo Dev), `global.css` (fundo `--cor-fundo-escuro`, `::selection`, `:focus-visible` com anel laranja 3 px, scrollbar), fontes `@fontsource`, `gerar-tipos`.
- [ ] **Step 5:** `npm test` → PASS; `npm run build` gera `web/dist`.
- [ ] **Step 6:** Commit `feat(web): projeto Vite, tokens do Figma e cliente da API`.

### Task 2: Componentes base

**Files:** `web/src/componentes/{Botao,OpcaoResposta,CampoNumerico,BarraConfianca,Boi,Balao,BarraProgresso,Modal}.tsx` + `.module.css` + testes.

**Interfaces — Produces:**
- `Botao({variante:'primario'|'secundario', carregando?, disabled?, onClick, children})` — `carregando` desabilita e mostra rótulo com `aria-busy`.
- `OpcaoResposta({tipo:'unica'|'multipla', name, value, checked, onChange, children})` — input nativo `radio`/`checkbox` estilizado como no Figma (marcador círculo/quadrado, estado selecionado laranja).
- `CampoNumerico({rotulo, unidade, min, max, casas, valor, onChange, erro})` — rejeita no `onChange` caracteres fora de `[0-9.,]`; mostra `erro` abaixo com `aria-describedby`/`aria-invalid`.
- `BarraConfianca({percentual, rotulo})` — `role="meter"` com `aria-valuenow`.
- `Boi({tamanho})` — o SVG do Figma (`Ilustração/Boi`, exporte do modo Dev), `aria-hidden` quando decorativo.

- [ ] **Step 1: Testes que falham:** `Botao carregando fica desabilitado`; `OpcaoResposta multipla é checkbox acessível pelo rótulo`; `CampoNumerico ignora letras e sinal: digitar "1a-2" resulta em "12"`; `CampoNumerico mostra erro com aria-invalid`; `BarraConfianca expõe aria-valuenow=64`.
- [ ] **Step 2:** `npm test` → FAIL. **Step 3:** implementar comparando com os componentes `Botão`, `Opção de resposta`, `Campo numérico`, `Item de hipótese` do Figma (seção "Componentes", node `6:19`). **Step 4:** PASS. **Step 5:** commit `feat(web): componentes base do protótipo`.

### Task 3: Página Início (`/`) — criar sessão

**Files:** `web/src/paginas/Inicio.tsx`, `web/src/api/sessao.ts`, testes. Figma: `01 · Início` (node `9:2`).

**Interfaces — Produces:** `iniciarVerificacao(modo:'produtor'|'veterinario'): Promise<EstadoSessao>` — `POST /api/animais` com `{brinco:'ANON-'+Date.now().toString(36)+aleatorio4, nome:'Animal da verificação', ficha:{}}` e depois `POST /api/sessoes {animal_id, modo}`; navega para `/anamnese/{sessao_id}`.

- [ ] **Step 1: Testes que falham:** `botão "Iniciar verificação" cria sessão no modo produtor`; `"Iniciar verificação como especialista" usa modo veterinario`; `aviso vermelho "No modo especialista as perguntas têm complexidade maior…" fica logo abaixo do botão e é ligado a ele por aria-describedby`; `409 sem base ativa mostra "Nenhuma base ativa. Peça para ativar uma versão." com botão Tentar de novo`; `sem_conexao mostra "Não consegui falar com o sistema. Ele está rodando?"`.
- [ ] **Steps 2–5:** FAIL → implementar fiel ao frame (boi grande à esquerda, título, cartão creme) → PASS → commit `feat(web): tela de início`.

### Task 4: Página Anamnese (`/anamnese/:sessaoId`) — perguntas e barra lateral

**Files:** `web/src/paginas/Anamnese.tsx`, `web/src/anamnese/{TelaTriagem,PerguntaDinamica,BarraHipoteses,PorQue}.tsx`, `mapearResposta.ts`, testes. Figma: `02`, `02b`, `03`, `04` (nodes `9:42`, `24:192`, `9:99`, `10:43`).

**Interfaces — Produces:**
- `paraCorpoTriagem(tela:TelaTriagem, escolha:Escolha): RespostaTriagem` — **múltipla**: `{valores:{[simbolo]:boolean}}` com todos os `campos`; "Nenhuma alteração" = todos `false`; "Não sei" = `{nao_sei:true}`. **Única**: `{valores:{[simbolo]: valor}}` — booleano → `true/false`; categórico → o `valor` da opção; numérico → **a string digitada** (o backend valida).
- `paraCorpoPergunta(p:PerguntaDinamica, escolha:Escolha): RespostaPergunta` — `{simbolo, valor}` ou `{simbolo, nao_sei:true}`; booleano mostra "Sim / Não / Não sei".
- `passoAtual(progresso) = triagem_respondidas + dinamicas_feitas + 1`; total exibido "de até `triagem_total + limite_dinamico`".

- [ ] **Step 1: Testes que falham** (fetch mockado com exemplos de `contratos/exemplos/*.json`):
  - `tela de triagem múltipla envia valores booleanos de todos os campos`;
  - `"Nenhuma alteração" envia todos false`; `"Não sei" envia nao_sei true`;
  - `pergunta numérica envia a string digitada e mostra a mensagem do 422 no campo`;
  - `barra lateral não aparece na primeira pergunta e aparece a partir da segunda`, alimentada por `GET /api/sessoes/{id}/parecer` (top 4 itens de todos os blocos por `percentual`, com `BarraConfianca`), atualizada a cada resposta;
  - `"Por que estou perguntando isso?" abre GET /porque/{simbolo} com motivo e serve_a`;
  - `duplo clique em Responder faz um só POST` e `409 recarrega o estado sem mensagem técnica` (Review Focus 1);
  - `fase "encerrada" sem pausa navega para /parecer/{id}`.
- [ ] **Steps 2–5:** FAIL → implementar (balão com o boi falando, barra de progresso, coluna de opções 560 px, barra lateral 380 px "O que estou pensando" com a nota "A porcentagem é a confiança do sistema, não uma probabilidade.") → PASS → commit `feat(web): anamnese com perguntas e barra de hipóteses`.

### Task 5: Alerta de bandeira vermelha

**Files:** `web/src/anamnese/AlertaBandeira.tsx`, `web/src/componentes/Modal.tsx`, testes. Figma: `05 · Alerta` (node `10:144`).

**Interfaces — Consumes:** `EstadoSessao.alerta {nivel, regras, pausa, acoes, texto}`; `POST /api/sessoes/{id}/acoes/bandeira {acao}`.

- [ ] **Step 1: Testes que falham:** `alerta.pausa abre modal com foco no primeiro botão e foco preso`; `"Ver parecer agora" envia ver_parecer e navega ao parecer`; `"Continuar respondendo" envia continuar e volta à pergunta`; `acoes ["ver_parecer"] (sessão encerrada) mostra só um botão`; `modal não fecha com Esc nem clique fora` (é alerta de segurança).
- [ ] **Steps 2–5:** FAIL → implementar → PASS → commit `feat(web): alerta de bandeira vermelha`.

### Task 6: Página Parecer (`/parecer/:sessaoId`)

**Files:** `web/src/paginas/Parecer.tsx`, `web/src/anamnese/ComoChegou.tsx`, testes. Figma: `06 · Parecer` (node `10:217`).

**Interfaces — Consumes:** `GET /parecer` (`blocos[].itens[]` com `doenca, nome, gravidade, percentual, situacao`; `urgencia {nivel, texto}`; `aviso`); `GET /como/{doenca}`.

- [ ] **Step 1: Testes que falham:** `tabela lista as 8 doenças em ordem decrescente de percentual, agrupadas pelos 3 blocos com os títulos do Figma`; `selo de gravidade alta/média/baixa com as cores do Figma e texto (não só cor)`; `faixa de urgência usa urgencia.texto e muda de cor por nível` (chamar_agora vermelho, observar âmbar, sem_problema verde); `"Como cheguei aqui?" abre GET /como/{doenca da 1ª linha} e lista evidências e regras`; `"Nova verificação" volta ao início`; `final=false mostra aviso "Parecer parcial"`.
- [ ] **Steps 2–5:** FAIL → implementar (tabela semântica `<table>` com `<caption>`, números tabulares) → PASS → commit `feat(web): parecer em tabela decrescente`.

### Task 7: Integração em localhost e ponta a ponta

**Files:** `web/e2e/{fluxo-produtor,bandeira,especialista,numero-invalido}.spec.ts`, `web/playwright.config.ts`; Modify `scripts/rodar.ps1` e `scripts/rodar.sh` **só** para rodar `npm ci && npm run build` em `web/` quando `web/dist` não existir; `README.md` (raiz) seção "Interface".

- [ ] **Step 1:** Playwright contra a API real (`webServer`: `.venv/Scripts/python -m uvicorn api.main:app --port 8000` com `ANAMNESE_DB` temporário e a base ativa `v0002`). Cenários: produtor completo até o parecer; bandeira (marcar "caída, sem conseguir se levantar") → modal → ver parecer com urgência "chamar agora"; especialista vê pergunta técnica; digitar `12,5` em dias mostra erro e não avança, `12` avança.
- [ ] **Step 2:** `npx playwright test` → PASS (instale só `chromium`).
- [ ] **Step 3:** `powershell -ExecutionPolicy Bypass -File scripts\rodar.ps1 -SemNavegador` serve a SPA em `http://localhost:8000/` e `/api/docs` continua no ar. Commit `feat(web): integração localhost e e2e`.

### Task 8: Passe de qualidade com impeccable

- [ ] **Step 1:** `<skill>/scripts/impeccable detect --json web/src` e corrigir os achados reais.
- [ ] **Step 2:** `/impeccable audit web/src` (a11y, desempenho, responsivo 375/768/1024/1440) e `/impeccable polish web/src`; conferir lado a lado com os frames do Figma (screenshots do modo Dev).
- [ ] **Step 3:** Estados obrigatórios presentes: carregando (esqueleto no balão e nas opções), erro, vazio, desabilitado, foco. Movimento: uma só transição autoral entre perguntas (o balão "fala": fade + leve subida, `prefers-reduced-motion` desliga).
- [ ] **Step 4:** `npm test && npm run build && npx playwright test` verdes. Commit `polish(web): passe de qualidade impeccable`.

---

## Self-review

| Requisito | Tarefa |
|---|---|
| Tela inicial com boi, 2 botões e aviso vermelho | 3 |
| Perguntas fechadas por opções; numéricas abertas e validadas no backend | 2, 4 |
| Barra lateral de hipóteses a partir da 2ª pergunta | 4 |
| Bandeira vermelha com pausa (modo produtor) | 5 |
| Parecer em tabela decrescente com chances | 6 |
| Por quê / Como (explicação) | 4, 6 |
| Conectado à API real e ao motor, em localhost | 1, 7 |
| Camada 4b (Playwright) | 7 |
