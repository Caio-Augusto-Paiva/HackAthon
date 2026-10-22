# Prompt para o Codex — Frontend React (22/10/2026)

> **Agente:** Codex. **Skills:** `impeccable` (ativa em toda edição de UI), `test-driven-development` e `verification-before-completion` (obra/superpowers). **MCP:** Figma (modo Dev) para tokens, medidas e SVG do boi. Cole tudo abaixo da linha.

---

Você vai construir o frontend em `web/` (React 19 + TypeScript + Vite 8) do sistema especialista "Anamnese Bovina", **já conectado** à API FastAPI (`api/`) e ao motor de inferência (`engine/`), reproduzindo o protótipo do Figma.

1. **Atualize a branch:** `git checkout codex-davi && git pull && git merge origin/sessao-pair-programming` (traz a API, o motor e a base ativa `v0002`). Rode `.venv/Scripts/python -m pytest -q` uma vez para confirmar que está verde.
2. **Leia, nesta ordem:** `docs/superpowers/plans/2026-10-22-frontend-web.md` (o plano; é a sua lista de tarefas), `api/README.md` (seção "Para o frontend"), `contratos/openapi.json` e `contratos/exemplos/*.json`.
3. **Figma (modo Dev):** arquivo `https://www.figma.com/design/MUiGJ81WjX97iyjX0yE6jz/HackAtom`, página "Protótipo". Frames: `01 · Início` (9:2), `02 · Pergunta 1` (9:42), `02b · erro de digitação` (24:192), `03 · Pergunta 2 + barra lateral` (9:99), `04 · Pergunta múltipla` (10:43), `05 · Alerta` (10:144), `06 · Parecer` (10:217); componentes na seção "Componentes" (6:19); variáveis na coleção "Tokens". Use `get_design_context`, `get_variable_defs` e exporte o SVG `Ilustração/Boi`. As barras de confiança no Figma são gradiente só por limitação do protótipo: no React são uma barra comum (`role="meter"`).
4. **Execute o plano tarefa a tarefa**, com TDD (teste falhando → código → teste passando → commit) e a skill `impeccable` ativa em toda mudança de UI (Task 1 cria `PRODUCT.md`/`DESIGN.md`; Task 8 é o passe `detect` + `audit` + `polish`).
5. **Regras duras:**
   - Não edite `api/`, `engine/`, `kb/`, `base/`, `contratos/` nem os testes deles. Precisou de algo da API? Registre em `docs/entrega/06-riscos-e-pendencias.md` e siga.
   - O frontend não calcula CF nem decide nada clínico: renderiza `EstadoSessao.proxima`, envia a resposta e mostra o que a API devolve.
   - Números digitados vão como **a string que o usuário digitou**; o backend aceita só dígitos ASCII dentro de min/max/casas e devolve 422 `resposta_invalida` — mostre essa mensagem no campo.
   - Tudo local: fontes via `@fontsource`, sem CDN, sem chamadas externas.
6. **Entrega:** commits por tarefa e push na `codex-davi` ao fim de cada tarefa. Ao final: `npm test`, `npm run build`, `npx playwright test` e `scripts\rodar.ps1 -SemNavegador` servindo a SPA em `http://localhost:8000/`. Responda com a lista de commits, o resultado dos testes, capturas das 6 telas e as pendências registradas.
