# Entrega — índice para a equipe e a banca

Documentação das **Seções 5 e 6 e da consulta web integrada** na branch `codex-davi`, com base ativa `v0002`. A [revisão da Seção 6](../revisoes/2026-10-22-revisao-secao-6.md) confronta o roteiro histórico com as fontes oficiais e a implementação até `d9eda27`. Os checkpoints anteriores são preservados como histórico, sem serem apresentados como estado atual.

O estado atual contém consulta React em `web/`, `kb/`, API FastAPI com 27 operações HTTP, SQLite, scripts de localhost, base ativa `v0002` e 34 casos sintéticos. Consulte [a API](../../api/README.md), [a base editorial](../../kb/README.md) e [o README principal](../../README.md). O editor gráfico permanece pendente. API, motor, kb, contratos e versões imutáveis foram preservados na implementação da interface.

O projeto aborda **T1 Anamnese**: coleta estruturada de sinais e histórico de bovinos leiteiros em lactação, com triagem explicável. A exigência e os critérios vêm das [transcrições oficiais da apresentação](../fontes/transcricao-apresentacao-rerum.md) e do [documentário](../fontes/transcricao-documentario-rerum.md). As transcrições são referências locais dos PDFs, não novos requisitos.

## Documentos disponíveis

| Arquivo | Conteúdo | Situação |
|---|---|---|
| [01-processo](01-processo.md) | Linha do tempo verificável, uso de IA, decisões e evidências | Preparado; faltam relatos pessoais de B/C e confirmação da equipe |
| [02-arquitetura](02-arquitetura.md) | Núcleo implementado, contratos, limites e componentes planejados | Preparado com distinção entre presente e futuro |
| [03-regras-de-producao](03-regras-de-producao.md) | Todas as regras, fontes, CF, símbolos e triagem | Gerado da ativa `v0002`, ainda de desenvolvimento |
| [04-casos-de-teste](04-casos-de-teste.md) | Entradas, critérios e resultados dos 34 casos sintéticos | Gerado por execução real |
| [05-apresentacao-e-demo](05-apresentacao-e-demo.md) | Roteiros de 10 e 5 minutos, demo e perguntas da banca | Roteiro preparado; duração oficial e ensaio pendentes |
| [06-riscos-e-pendencias](06-riscos-e-pendencias.md) | Riscos, lacunas, responsáveis por papel e checklist de envio | Registro aberto |
| [07-ensaio-e-envio](07-ensaio-e-envio.md) | Formulários de ensaio, pacote e comprovante de envio | Modelo a preencher; não constitui execução |

## Executar o checkpoint

Na raiz do repositório, com Python 3.12+:

```powershell
.venv/Scripts/python -m pytest -q
.venv/Scripts/python -m unittest discover -s tests/engine -t .
.venv/Scripts/python scripts/gerar_doc_regras.py --casos base/casos/casos.json --verificar
```

A verificação integrada contém **1066 testes Python aprovados, 1 ignorado e 170 subtestes aprovados**. A execução separada de **132 testes unittest** já está contida no pytest, não é somada. São **34 casos sintéticos, zero falhas na ativa**, uma contagem distinta de testes e de validação clínica. Os dois exemplos originais foram preservados nesse conjunto. As saídas históricas e o alcance do ensaio HTTP ficam em [evidencias-verificacao.json](evidencias-verificacao.json). O checkpoint da troca de modo (`09f5754`) registra **60 testes de interface e 11 E2E**, descritos em [QUALIDADE.md](../../web/QUALIDADE.md); 39/8 são as contagens históricas da integração inicial. O inicializador serve a SPA em localhost:8000.

## Atendimento às exigências oficiais

| Exigência | Evidência disponível | Situação |
|---|---|---|
| IA apoiando o desenvolvimento — [A], slides 3 e 7 | [Processo](01-processo.md), testes e histórico de commits | Evidência técnica disponível; relatos pessoais dos três integrantes ainda incompletos |
| Decisão por regras, sem LLM em execução — [A], slides 8 e 13 | `engine/` e teste de arquitetura | Atendido no núcleo disponível |
| Determinismo e auditoria — [A], slide 8 | `Fraction`, agenda, traço, snapshot e testes de ordem/reprocessamento | Atendido nos contratos testados; inclui a ordem das respostas da sessão |
| Solução em localhost — [A], slide 10 | React, motor, `kb/`, API, SQLite e `scripts/rodar.ps1` | Consulta web integrada e E2E com API real; editor pendente |
| Processo, arquitetura e regras — [A], slide 10; [D], p. 2 | Documentos 01, 02 e 03 desta pasta | Documentados para o escopo implementado; complementação pessoal do processo pendente |
| Demonstração em funcionamento — [A], slide 10 | CLI, fluxo HTTP e consulta web até parecer, por quê/como; casos executados na API | Ensaio HTTP histórico e E2E de navegador disponíveis; apresentação e ensaio humano pendentes |
| Ferramentas e código aberto — [A], slides 3 e 13 | Código disponível; núcleo só com biblioteca padrão, API/web com dependências declaradas | Licença do projeto e revisão final de licenças pendentes; requisito não encerrado |
| Apresentação do processo ao resultado — [A], slide 10 | Roteiro e perguntas no documento 05 | Falta material visual final e ensaio |
| Nome e telefone de todos no envio — [A], slide 15 | Tabela abaixo, informada pela equipe | Dados presentes; conferência final e inclusão na mensagem de envio ainda necessárias |

Dados dos exemplos são sintéticos. Todas as **56 regras** permanecem em `suposicao_a_validar`; há zero regras registradas como `validada`. Fontes clínicas contextuais não demonstram calibração dos CF nem participação de especialista na revisão desta base.

## Equipe — dados informados para conferência antes do envio

Os dados abaixo foram informados pela equipe; a grafia de Davi Monção Fernandes foi confirmada nesta revisão. As referências A/B/C identificam as linhas da equipe, mas não atribuem automaticamente a cada pessoa as interações dos diários históricos com as mesmas letras. As responsabilidades reais informadas prevalecem sobre a divisão de pastas originalmente planejada.

| Referência | Nome completo | Número de telefone | Responsabilidade informada |
|---|---|---|
| A | Caio Augusto de Paiva Teixeira | (32)99996-0047 | Arquitetura dos sistemas, Arquitetura dos prompts |
| B | Davi Monção Fernandes | (32)99967-0773 | Motor de inferência, documentação |
| C | Luis Henrique Poubel Buettel | (32)98803-1744 | Base de conhecimento (JSON), banco de dados |

## Mapa do pacote e trabalho restante

O código atual está em `engine/`, `kb/`, `api/` e `web/`; a versão ativa em `base/versoes/`, os casos em `base/casos/`, a cópia de desenvolvimento em `base/desenvolvimento/`, os testes Python em `tests/`, os testes da interface em `web/src/` e `web/e2e/` e os utilitários em `scripts/`. As fontes oficiais e o planejamento estão em `docs/fontes/` e `docs/superpowers/`. O grafo navegável e seu cofre ficam em `graphify-out/` e `obsidian/01-conhecimento/`.

Esta entrega contém fontes Markdown, capturas da interface e evidências de software. PDFs finais, slides em PDF e formato editável, vídeo de reserva, licença e pacote `.zip` final ainda dependem da conclusão/revisão do grupo. Dependências Python estão em `pyproject.toml`; as do frontend, em `web/package.json` e `web/package-lock.json`. Os arquivos instalados e o build não entram no versionamento.

O roteiro usa **10 minutos de fala + 4 de demo**, como estimativas confirmadas pela equipe, não como duração oficial. A alternativa curta de 5 minutos fica como reserva editorial. O pacote ainda não foi montado nem enviado. O plano cita `uv.lock`, mas esse arquivo não existe no checkout auditado; não se promete instalação Python reproduzível por esse lockfile. Antes de empacotar, seguir o [checklist de fechamento](06-riscos-e-pendencias.md).

Prazo informado nos documentos oficiais: **22/10/2026 às 20:00**. Apresentação: **23/10/2026 às 09:00**. O alvo interno de envio às **18:30** é uma decisão da equipe no planejamento. Duração da fala, limite de anexo e infraestrutura da apresentação precisam de confirmação com a organização.
