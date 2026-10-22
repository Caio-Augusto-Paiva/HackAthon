# Entrega parcial — índice para a equipe e a banca

Documentação da execução da **Seção 5** na branch `codex-davi`, após integrar o baseline `f46cd6e`. O checkpoint inicial `898512c` é histórico: os documentos de processo preservam o contexto em que foram escritos.

O estado atual contém `kb/`, API FastAPI com 27 operações HTTP, SQLite, scripts de localhost, base ativa `v0002` e 34 casos sintéticos. Consulte [a API](../../api/README.md), [a base editorial](../../kb/README.md) e [o README principal](../../README.md). Interface web e editor gráfico estão em andamento em outra sessão. Os diretórios `api/`, `web/`, `contratos/` e `tests/api/` não foram alterados nesta execução; a equipe fará a integração na branch compartilhada.

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

## Executar o checkpoint

Na raiz do repositório, com Python 3.12+:

```powershell
.venv/Scripts/python -m pytest -q
.venv/Scripts/python -m unittest discover -s tests/engine -t .
.venv/Scripts/python scripts/gerar_doc_regras.py --casos base/casos/casos.json --verificar
```

A verificação desta etapa contém **1006 testes aprovados, 1 ignorado e 110 subtestes aprovados**. A execução separada de **125 testes unittest** já está contida no pytest, não é somada. São **34 casos sintéticos, zero falhas na ativa**, uma contagem distinta de testes e de validação clínica. Os dois exemplos originais foram preservados nesse conjunto. As saídas completas e o alcance do ensaio HTTP ficam em [evidencias-verificacao.json](evidencias-verificacao.json). A aplicação em navegador é trabalho paralelo; `scripts/rodar.ps1` já está implementado.

## Atendimento às exigências oficiais

| Exigência | Evidência disponível | Situação |
|---|---|---|
| IA apoiando o desenvolvimento — [A], slides 3 e 7 | [Processo](01-processo.md), testes e histórico de commits | Comprovado nesta sessão; diários das demais pessoas incompletos |
| Decisão por regras, sem LLM em execução — [A], slides 8 e 13 | `engine/` e teste de arquitetura | Atendido no núcleo disponível |
| Determinismo e auditoria — [A], slide 8 | `Fraction`, agenda, traço, snapshot e testes de ordem/reprocessamento | Atendido nos contratos testados; inclui a ordem das respostas da sessão |
| Solução em localhost — [A], slide 10 | Motor, `kb/`, API, SQLite e `scripts/rodar.ps1` | Backend disponível; frontend/E2E em andamento |
| Processo, arquitetura e regras — [A], slide 10; [D], p. 2 | Documentos 01, 02 e 03 desta pasta | Adiantado para o escopo implementado |
| Demonstração em funcionamento — [A], slide 10 | CLI e fluxo HTTP até parecer, por quê/como e execução dos casos | Ensaio registrado nas evidências; apresentação humana e navegador pendentes |
| Ferramentas e código aberto — [A], slides 3 e 13 | Fontes do núcleo disponíveis; runtime sem bibliotecas externas | Licença do projeto e revisão final de licenças pendentes |
| Apresentação do processo ao resultado — [A], slide 10 | Roteiro e perguntas no documento 05 | Falta material visual final e ensaio |
| Nome e telefone de todos no envio — [A], slide 15 | Campos abaixo | A preencher pela equipe |

Dados dos exemplos são sintéticos. Todas as **56 regras** permanecem em `suposicao_a_validar`; há zero regras registradas como `validada`. Fontes clínicas contextuais não demonstram calibração dos CF nem participação de especialista na revisão desta base.

## Equipe — preenchimento obrigatório antes do envio

Os papéis abaixo vêm do planejamento e não identificam pessoas por inferência do nome de uma branch ou de um autor de commit.

| Papel planejado | Nome completo | Responsabilidade prevista |
|---|---|---|
| A | Caio Augusto de Paiva Teixeira | Arquitetura dos sistemas, Arquitetura dos prompts |
| B | Davi MOnção Fernades | Motor de inferência, Documentação |
| C | Luis Henrique Poubel Buettel | Base de conhecimento, Banco de Dados(Jason) |

## Mapa do pacote e trabalho restante

O código atual está em `engine/`, `kb/` e `api/`; a versão ativa em `base/versoes/`, os casos em `base/casos/`, a cópia de desenvolvimento em `base/desenvolvimento/`, os testes em `tests/` e os utilitários em `scripts/`. As fontes oficiais e o planejamento estão em `docs/fontes/` e `docs/superpowers/`. O grafo navegável e seu cofre ficam em `graphify-out/` e `obsidian/01-conhecimento/`.

Esta entrega contém fontes Markdown e evidências de software. PDFs finais, slides em PDF e formato editável, vídeo de reserva, licença e pacote `.zip` final ainda dependem da conclusão/revisão do grupo. Dependências Python estão em `pyproject.toml`; a instalação foi feita em `.venv`. Nenhum manifesto ou lock do frontend foi alterado por esta sessão.

Prazo informado nos documentos oficiais: **22/10/2026 às 20:00**. Apresentação: **23/10/2026 às 09:00**. O alvo interno de envio às **18:30** é uma decisão da equipe no planejamento. Duração da fala, limite de anexo e infraestrutura da apresentação precisam de confirmação com a organização.
