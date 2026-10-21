# Versões de bibliotecas e linguagens (pesquisa de 20/10/2026)

Pesquisa feita em 20/10/2026. Onde a página oficial não trouxe a data de lançamento, o campo está como "não confirmado". Versões e licenças vêm dos registros oficiais (PyPI, npm, python.org, nodejs.org, endoflife.date, docs.astral.sh, playwright.dev) lidos via WebFetch/WebSearch.

| item | versão | data | licença | compatibilidade | fonte URL | status confirmado/não confirmado |
|---|---|---|---|---|---|---|
| Python (estável mais recente) | 3.15.0 | 09/10/2026 | PSF-2.0 (não re-verificado) | Windows: instalador oficial e Python install manager; 3.14.8 é a linha anterior (30/09/2026) | https://www.python.org/downloads/ ; https://endoflife.date/python | confirmado (versão e data) |
| FastAPI | 0.156.4 | 20/10/2026 | MIT | Python >=3.10 | https://pypi.org/project/fastapi/ | confirmado |
| Pydantic (v2) | 2.14.1 | 11/10/2026 (entrada do changelog) | MIT (não re-verificado) | Python não confirmado | https://pypi.org/project/pydantic/ | parcial (versão confirmada; Python não confirmado) |
| uvicorn | 0.54.0 | 25/09/2026 | BSD-3-Clause | Python >=3.10 | https://pypi.org/project/uvicorn/ | confirmado |
| pytest | 9.1.1 | 19/06/2026 | MIT | Python >=3.10 | https://pypi.org/project/pytest/ | confirmado |
| hypothesis | 6.170.5 | 20/10/2026 | MPL-2.0 | Python >=3.11 | https://pypi.org/project/hypothesis/ | confirmado |
| httpx | 0.28.1 | 06/12/2024 (última estável) | BSD-3-Clause | Python >=3.8 | https://pypi.org/project/httpx/ | confirmado (pré-release 1.0.dev6 em 31/08/2026, não usar) |
| uv (Astral) | 0.13.4 | 20/10/2026 | MIT OR Apache-2.0 | binário standalone, sem Python exigido | https://pypi.org/project/uv/ ; https://docs.astral.sh/uv/getting-started/installation/ | confirmado |
| ruff (Astral) | 0.17.1 | 15/10/2026 | MIT | Python >=3.7 (wheel próprio) | https://pypi.org/project/ruff/ | confirmado |
| Node.js LTS | 24.22.0 "Krypton" | 14/10/2026 | MIT (não re-verificado) | Node 24 entra em Maintenance em 20/10/2026 e fim de vida em 30/04/2028 | https://nodejs.org/dist/index.json ; https://cdn.jsdelivr.net/gh/nodejs/release@main/README.md | confirmado (versão); Node 26 vira LTS em 28/10/2026 |
| TypeScript | 7.0.2 | não confirmado | Apache-2.0 | Node >=16.20.0 (engines) | https://registry.npmjs.org/typescript | parcial (data não confirmada) |
| Vite | 8.3.4 | não confirmado | MIT | Node ^20.19.0 \|\| >=22.12.0 | https://registry.npmjs.org/vite | parcial (data não confirmada) |
| React | 19.3.1 | não confirmado | MIT | não confirmado | https://registry.npmjs.org/react | parcial (data não confirmada) |
| React DOM | 19.3.1 | não confirmado | MIT | acompanha React 19.3.1 | https://registry.npmjs.org/react-dom | parcial (data não confirmada) |
| @xyflow/react (React Flow) | 12.12.0 | não confirmado | MIT | não confirmado | https://registry.npmjs.org/@xyflow%2freact | parcial (nome do pacote e licença confirmados) |
| reactflow (pacote antigo, NÃO usar) | 11.11.4 | não confirmado | MIT | legado (v11) | https://registry.npmjs.org/reactflow | confirmado (apenas como legado) |
| @dagrejs/dagre (layout) | 3.1.1 | não confirmado | MIT | não confirmado | https://registry.npmjs.org/@dagrejs%2fdagre | parcial (data não confirmada) |
| elkjs (layout alternativo) | 0.12.0 | não confirmado | EPL-2.0 OR GPL-3.0-or-later (dupla; escolher EPL-2.0) | não confirmado | https://registry.npmjs.org/elkjs | parcial (data não confirmada) |
| @playwright/test | 1.64.1 | não confirmado | Apache-2.0 | Node >=20 | https://registry.npmjs.org/@playwright%2ftest ; https://playwright.dev/docs/browsers | parcial (data não confirmada) |
| openapi-typescript | 7.13.0 | não confirmado | MIT | não confirmado | https://registry.npmjs.org/openapi-typescript | parcial (data não confirmada) |
| @tanstack/react-query | 5.104.5 | não confirmado | MIT | não confirmado | https://registry.npmjs.org/@tanstack%2freact-query | parcial (data não confirmada) |

## Observações

- **Nome do pacote React Flow:** o atual é `@xyflow/react` (v12, MIT). O pacote `reactflow` é a linha v11 e não deve ser usado em projeto novo. Confirmado.
- **Playwright no Windows:** é preciso rodar `npx playwright install` depois de instalar o pacote, porque os navegadores não vêm com ele. Os binários ficam em `%USERPROFILE%\AppData\Local\ms-playwright` (pode ser trocado com `PLAYWRIGHT_BROWSERS_PATH`). `install-deps` é voltado a Linux/CI e não é necessário no Windows.
- **Node.js:** para o PoC, a LTS ativa hoje é a 24 (Krypton), que entra em Maintenance em 20/10/2026. A 26 vira LTS ativa em 28/10/2026, e as datas podem mudar segundo o próprio cronograma oficial.
- **Python:** 3.15.0 é a estável mais recente. A compatibilidade de cada biblioteca com 3.15 não foi testada nesta pesquisa; confirmar antes de fixar a versão no projeto.
- **uv no Windows:** instalação por `winget install --id=astral-sh.uv -e` ou por `irm https://astral.sh/uv/install.ps1 | iex`. A documentação não informa versão mínima de Windows.
- **Datas npm:** o registro npm não trouxe a data de publicação nesta consulta. Ficam como "não confirmado" até uma verificação direta em npmjs.com ou GitHub Releases.
