# HackAtom — anamnese explicável de bovinos leiteiros

Prova de conceito do tema T1 do Hackathon UFJF 2026. O núcleo executa regras explícitas, combina fatores de certeza pelo modelo MYCIN e explica as conclusões. A IA auxilia o desenvolvimento; a decisão em execução sai da base e do motor.

**Estado integrado, branch `codex-davi`:** interface React conectada ao motor local, base ativa `v0003`, módulo `kb/` e API FastAPI com persistência SQLite. São 27 operações HTTP e 34 casos sintéticos versionados. O editor gráfico permanece pendente. Todo conhecimento veterinário e todo CF permanecem como suposição a validar. O resultado não constitui diagnóstico nem recomendação terapêutica.

## Executar a demonstração do motor

Requer Python 3.12 ou superior. Abra um terminal na raiz deste repositório. O motor e os utilitários desta entrega usam somente a biblioteca padrão, sem instalação de pacotes.

```powershell
python -m unittest discover -s tests/engine -t .
python -m engine base/versoes/v0003.json base/desenvolvimento/casos/alerta-decubito.json
```

O primeiro comando executa os testes do motor e da base de desenvolvimento. O segundo executa um caso sintético, imprime JSON com `status: "passou"` e código de saída 0. Veja o [exemplo mamário e o uso Python](base/desenvolvimento/LEIA-ME.txt).

Para instalar as dependências, executar a API em `localhost:8000` e preparar o banco com dados fictícios, siga o [README da API](api/README.md). O contrato e a validação da base estão no [README de `kb/`](kb/README.md). Após instalar `.[dev]` no ambiente virtual, execute a suíte completa com `.venv\Scripts\python -m pytest`.

## Interface

A interface em `web/` reproduz o protótipo do Figma com os SVGs originais, cores e fontes locais. Requer Node.js 24 e as dependências Python instaladas no `.venv`. Na raiz:

```powershell
powershell -ExecutionPolicy Bypass -File scripts\rodar.ps1 -SemNavegador
```

Abra **http://localhost:8000/**. O script mantém o banco existente e, se `web/dist/index.html` estiver ausente, executa `npm ci` e `npm run build` antes de iniciar a API. A instalação inicial precisa de internet; a consulta usa apenas recursos locais. `/api/docs` continua disponível, com a limitação de CDN documentada nos riscos.

Para desenvolver e testar a interface:

```powershell
cd web
npm.cmd ci
npm.cmd test
npm.cmd run build
npx.cmd playwright install chromium
npx.cmd playwright test
```

O Playwright inicia sua própria API com SQLite temporário e a base ativa; deixe a porta 8000 livre. `npm.cmd run dev` inicia o Vite com proxy para a API em 8000. Após alterar o frontend, compile novamente antes de iniciar o servidor de demonstração: um build existente é preservado pelo inicializador.

O navegador renderiza `EstadoSessao.proxima`, envia números como a string digitada e mostra os erros 422 no campo. CF, hipóteses, urgência, seleção das perguntas e explicações são decisões do backend. Há triagem única/múltipla, correção de respostas desta navegação, pausa de bandeira, por quê e parecer com evidências. Veja [qualidade e alcance dos testes](web/QUALIDADE.md) e [roteiro da demo](docs/entrega/05-apresentacao-e-demo.md).

## Documentação

- [Índice da entrega e atendimento às exigências](docs/entrega/README.md).
- [Processo de desenvolvimento](docs/entrega/01-processo.md).
- [Arquitetura implementada](docs/entrega/02-arquitetura.md).
- [61 regras de produção geradas da base](docs/entrega/03-regras-de-producao.md).
- [Resultados dos 34 casos sintéticos](docs/entrega/04-casos-de-teste.md).
- [Roteiro de apresentação, demonstração e perguntas](docs/entrega/05-apresentacao-e-demo.md).
- [Riscos, pendências e checklist de envio](docs/entrega/06-riscos-e-pendencias.md).
- [Revisão técnica da Seção 6](docs/revisoes/2026-10-22-revisao-secao-6.md).
- [Contrato detalhado do motor](engine/README.md).
- [Grafo 2: dados de treino por doença](obsidian/02-Dados%20de%20Treino/README.md) e a [spec do grafo 2](docs/superpowers/specs/2026-10-22-grafo-dados-por-doenca-design.md).
- Estado atual (após `0300cdb`): **1080 testes Python** (motor 134, kb 296, API 629, casos 9, documentação 12) e 170 subtestes, e **71 Vitest em 11 arquivos**; os 6 arquivos de spec E2E não foram rodados. Histórico: no fechamento de 22/10 (após `7587de4`), 1077 testes Python aprovados, 170 subtestes aprovados, 0 ignorados; 68 Vitest em 11 arquivos; E2E (6 specs) não rodados neste checkpoint. Histórico (`09f5754`): 1066 Python, 60 Vitest, 11 E2E.

## Manter as tabelas sincronizadas

```powershell
python scripts/gerar_doc_regras.py --casos base/casos/casos.json
python scripts/gerar_doc_regras.py --casos base/casos/casos.json --verificar
```

O segundo comando retorna 1 se o conteúdo gerado divergir do arquivo versionado. A suíte também verifica esse sincronismo. Sem `--base`, o gerador segue `base/ativa.json`, atualmente `v0003`. As versões são imutáveis: alteração de regra exige nova versão e execução dos casos antes de ativar. A ativação é operacional e não representa aprovação clínica. As contagens e os resultados reais ficam em [evidências de verificação](docs/entrega/evidencias-verificacao.json).

## Equipe e licença

Os nomes, telefones e responsabilidades informados pela equipe estão no [índice da entrega](docs/entrega/README.md); o grupo deve conferir os dados antes do envio. A licença do código do projeto ainda não foi declarada em um arquivo `LICENSE`; essa decisão continua pendente para atender integralmente à exigência de código aberto.
