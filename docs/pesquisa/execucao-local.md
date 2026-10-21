# Pesquisa: execução local (FastAPI + Vite + uv + Playwright + pytest + Hypothesis)

Data da pesquisa: 2026-10-20. Fontes: documentação oficial, lida por WebFetch. Quando a página oficial não trouxe o ponto, a linha diz "não confirmado".

---

## 1. FastAPI servindo build do Vite (SPA) no mesmo processo

**Resposta:** FastAPI tem `app.frontend()`. Sirva a pasta `dist` na raiz com `directory="dist"`. Com `fallback="index.html"` (padrão `"auto"`), rotas de página sem arquivo devolvem `index.html`, mas só para GET/HEAD com `Accept: text/html`. Arquivos ausentes (JS, CSS, imagens) continuam 404. Rotas de API (path operations) têm prioridade sobre o frontend. `StaticFiles(html=True)` sozinho não faz fallback de SPA: ele só serve `index.html` de diretórios (confirmado na doc do Starlette). Versão do FastAPI em que `app.frontend()` surgiu: não confirmado.

**Exemplo:**
```
app.frontend("/", directory="dist", fallback="index.html")
```

**Status:** confirmado (comportamento e prioridade de rotas). Versão de introdução: não confirmado.
**URL:** https://fastapi.tiangolo.com/ja/tutorial/frontend/ (versão em japonês, lida integralmente nos trechos relevantes); https://fastapi.tiangolo.com/tutorial/static-files/ ; https://www.starlette.dev/staticfiles/

---

## 2. uv (Astral): ambiente, `uv sync`, `uv run`, pin de Python

**Resposta:** `uv sync` instala no ambiente do projeto os pacotes do `uv.lock` e remove pacotes extras por padrão. `--locked` falha se o lock estiver desatualizado; `--frozen` usa o lock sem verificar. `uv run <comando>` executa dentro do ambiente do projeto. `uv python pin 3.12` cria `.python-version` no diretório atual (`--global` grava no diretório de configuração do usuário). Sim, uv baixa uma versão de Python sozinho quando ela é necessária e não está instalada. Não confirmado: o que acontece quando o pin fica fora de `requires-python`, e a regra de "patch mais recente já instalado" citada em fonte de terceiros.

**Exemplo:**
```
uv python pin 3.12
uv sync
uv run pytest
```

**Status:** confirmado (sync, lock, run, pin, download automático). Pontos de conflito com `requires-python` e patch: não confirmado.
**URL:** https://docs.astral.sh/uv/concepts/projects/sync/ ; https://docs.astral.sh/uv/concepts/python-versions/ ; https://docs.astral.sh/uv/guides/install-python/ ; https://docs.astral.sh/uv/reference/cli/

---

## 3. Playwright Test: `webServer` com comando Python (uvicorn) no Windows

**Resposta:** Os campos existem e têm estes valores. `command` é o comando shell que sobe o servidor. `url` é considerado pronto quando responde 2xx, 3xx, 400, 401, 402 ou 403. `reuseExistingServer: true` reutiliza um servidor já ativo; `false` dá erro se a porta já estiver ocupada; a doc sugere `!process.env.CI`. `timeout` é em milissegundos, padrão 60000. Não confirmado: que um comando Python (uvicorn) funcione no Windows, pois a doc não cita Python. Na doc, `gracefulShutdown` é ignorado no Windows.

**Exemplo:**
```
uv run uvicorn app.main:app --port 8000
```
(Esse é o valor do campo `command`; `url` = `http://localhost:8000`.)

**Status:** confirmado (campos e valores). Uvicorn/Python no Windows: não confirmado.
**URL:** https://playwright.dev/docs/test-webserver

---

## 4. Windows PowerShell: execução de `.ps1` e política padrão

**Resposta:** A doc oficial é contraditória sobre o padrão no Windows cliente. A entrada "Default" e a descrição de RemoteSigned dizem que o padrão é RemoteSigned. A seção "Undefined" e o texto de fallback dizem que, sem política em nenhum escopo, o efetivo é Restricted, "the default for Windows clients". Restricted bloqueia qualquer `.ps1`. Para descobrir a política real, rode `Get-ExecutionPolicy -List`. Para rodar sem mudar a configuração global, use `-ExecutionPolicy Bypass`: ele vale só para a sessão e não grava nada. Scripts baixados da internet podem ter a marca "vindo da internet"; `Unblock-File` remove essa marca. Não confirmado: qual das duas afirmações vale na sua máquina.

**Exemplo:**
```
powershell -ExecutionPolicy Bypass -File rodar.ps1
```
Para PowerShell 7: `pwsh -ExecutionPolicy Bypass -File rodar.ps1`.

**Status:** confirmado (flag `-ExecutionPolicy` e `-File`; Bypass sem bloqueio nem prompt; escopo da sessão). Padrão exato do Windows 11 cliente: conflitante na doc, não confirmado.
**URL:** https://learn.microsoft.com/en-us/powershell/module/microsoft.powershell.core/about/about_execution_policies ; https://learn.microsoft.com/en-us/powershell/module/microsoft.powershell.core/about/about_powershell_exe?view=powershell-5.1 ; https://learn.microsoft.com/en-us/powershell/module/microsoft.powershell.core/about/about_pwsh?view=powershell-7.5

---

## 5. Vite: build e `server.proxy`

**Resposta:** O comando de build é `vite build` (no projeto, normalmente `npm run build` com o script que chama `vite build`). A pasta de saída padrão é `dist`, definida por `build.outDir` (confirmado). `server.proxy` encaminha requisições cujo caminho começa com a chave para o alvo. Para `/api`, use `target` e, se necessário, `changeOrigin: true`. Esse proxy só vale no servidor de desenvolvimento. Não confirmado: suporte a WebSocket por `ws: true`, que aparece só em fonte de terceiros.

**Exemplo:**
```
npx vite build
```
(Proxy: chave `/api`, `target: http://localhost:8000`, `changeOrigin: true`.)

**Status:** confirmado (build, dist, proxy por prefixo com target e changeOrigin).
**URL:** https://vite.dev/guide/build ; https://vite.dev/config/build-options ; https://vite.dev/config/server-options

---

## 6. pytest: parametrizar a partir de JSON com ids legíveis

**Resposta:** A forma usual é `pytest.mark.parametrize` (a assinatura é a de `pytest.Metafunc.parametrize`). Para ids legíveis, use `pytest.param(..., id="nome")`, que a doc oficial descreve como o id do conjunto de parâmetros. A doc oficial de parametrize não trata de carregar JSON: o padrão usual é ler o JSON no módulo de teste (ou em `conftest.py`) e passar a lista ao `parametrize`. Não confirmado: o trecho lido do argumento `ids=` do `parametrize` e o funcionamento de `None` nesse argumento. O hook `pytest_make_parametrize_id` existe, mas não foi lido em detalhe.

**Exemplo:**
```
pytest -v tests/test_casos.py
```

**Status:** confirmado (`parametrize` e `pytest.param(id=...)`). Carregamento de JSON e `ids=`: não confirmado na doc oficial lida.
**URL:** https://docs.pytest.org/en/stable/how-to/parametrize.html ; https://docs.pytest.org/en/stable/reference/reference.html

---

## 7. Hypothesis: listas de floats em intervalo e invariância à permutação

**Resposta:** As assinaturas estão confirmadas. `st.floats(min_value, max_value, ...)` aceita limites inclusivos por padrão. Com qualquer limite definido, `allow_nan=True` é erro. Com os dois limites definidos, `allow_infinity=True` é erro. Então, para [-0.99, 0.99], passe `allow_nan=False` e `allow_infinity=False`. `st.lists(elements, min_size=0, max_size=None, unique=False, ...)` gera listas. `st.permutations(values)` gera permutações de uma coleção ordenada fixa (`values`). Não confirmado: a forma de permutar uma lista gerada dentro do próprio teste (por exemplo, combinando com `st.data()`). A página lida não mostra esse uso.

**Exemplo:**
```
st.lists(st.floats(min_value=-0.99, max_value=0.99, allow_nan=False, allow_infinity=False))
```

**Status:** confirmado (`floats`, `lists`, `permutations` e as restrições de NaN e infinito). Padrão de permutar lista gerada: não confirmado.
**URL:** https://hypothesis.readthedocs.io/en/latest/reference/strategies.html

---

## Resumo de status

| # | Item | Status |
|---|---|---|
| 1 | FastAPI + Vite SPA (`app.frontend`, fallback) | confirmado; versão não confirmada |
| 2 | uv (`sync`, `run`, `python pin`, download automático) | confirmado; conflito com `requires-python` não confirmado |
| 3 | Playwright `webServer` (campos) | confirmado; uvicorn no Windows não confirmado |
| 4 | PowerShell `-ExecutionPolicy Bypass -File` | confirmado; padrão cliente conflitante na doc |
| 5 | Vite build e `server.proxy` | confirmado |
| 6 | pytest parametrize com `pytest.param(id=...)` | confirmado; carregamento de JSON e `ids=` não confirmados |
| 7 | Hypothesis floats, lists, permutations | confirmado; permutar lista gerada não confirmado |
