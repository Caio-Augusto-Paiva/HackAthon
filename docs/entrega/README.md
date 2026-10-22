# Entrega parcial — índice para a equipe e a banca

Checkpoint documental de **21/10/2026**, baseado no código disponível na branch `codex-davi`. Referência inicial da implementação auditada: commit `898512c`. Esta pasta registra o que podia ser executado nesse checkpoint e o trabalho restante naquele momento.

**Nota da integração em `sessao-pair-programming`:** esta branch também contém o módulo `kb/`, a API FastAPI, a persistência SQLite e os scripts de execução em localhost. Consulte [a API](../../api/README.md), [o módulo da base](../../kb/README.md) e [o README principal](../../README.md) para o estado integrado. As contagens de 135 testes e as pendências de API/banco nos documentos deste pacote pertencem ao checkpoint original; não são uma avaliação atual desses componentes. A interface web, o editor gráfico e a validação clínica continuam pendentes.

O projeto aborda **T1 Anamnese**: coleta estruturada de sinais e histórico de bovinos leiteiros em lactação, com triagem explicável. A exigência e os critérios vêm das [transcrições oficiais da apresentação](../fontes/transcricao-apresentacao-rerum.md) e do [documentário](../fontes/transcricao-documentario-rerum.md). As transcrições são referências locais dos PDFs, não novos requisitos.

## Documentos disponíveis

| Arquivo | Conteúdo | Situação |
|---|---|---|
| [01-processo](01-processo.md) | Linha do tempo verificável, uso de IA, decisões e evidências | Preparado; faltam relatos pessoais de B/C e confirmação da equipe |
| [02-arquitetura](02-arquitetura.md) | Núcleo implementado, contratos, limites e componentes planejados | Preparado com distinção entre presente e futuro |
| [03-regras-de-producao](03-regras-de-producao.md) | Todas as regras, fontes, CF, símbolos e triagem | Gerado da base de desenvolvimento |
| [04-casos-de-teste](04-casos-de-teste.md) | Entradas, critérios e resultados dos dois exemplos disponíveis | Gerado por execução real |
| [05-apresentacao-e-demo](05-apresentacao-e-demo.md) | Roteiros de 10 e 5 minutos, demo e perguntas da banca | Roteiro preparado; duração oficial e ensaio pendentes |
| [06-riscos-e-pendencias](06-riscos-e-pendencias.md) | Riscos, lacunas, responsáveis por papel e checklist de envio | Registro aberto |

## Executar o checkpoint

Na raiz do repositório, com Python 3.12+:

```powershell
python -m unittest discover
python -m engine base/desenvolvimento/anamnese-bovinos-v3.1.0-revisao1.json base/desenvolvimento/casos/alerta-decubito.json
```

A verificação atual contém **135 testes automatizados**: 100 do núcleo e suas regressões, 25 da base e integração, 10 da geração de documentação. Os **dois casos sintéticos** são outra contagem: não são 135 casos clínicos. Há execução local por terminal; a aplicação completa em navegador e `scripts/rodar.ps1` continuam planejados.

## Atendimento às exigências oficiais

| Exigência | Evidência disponível | Situação |
|---|---|---|
| IA apoiando o desenvolvimento — [A], slides 3 e 7 | [Processo](01-processo.md), testes e histórico de commits | Comprovado nesta sessão; diários das demais pessoas incompletos |
| Decisão por regras, sem LLM em execução — [A], slides 8 e 13 | `engine/` e teste de arquitetura | Atendido no núcleo disponível |
| Determinismo e auditoria — [A], slide 8 | `Fraction`, agenda, traço, snapshot e testes de ordem/reprocessamento | Atendido nos contratos testados; inclui a ordem das respostas da sessão |
| Solução em localhost — [A], slide 10 | Núcleo executável localmente, sem serviço externo | Parcial: falta a aplicação final em localhost |
| Processo, arquitetura e regras — [A], slide 10; [D], p. 2 | Documentos 01, 02 e 03 desta pasta | Adiantado para o escopo implementado |
| Demonstração em funcionamento — [A], slide 10 | CLI e exemplos executáveis | Disponível por terminal; demonstração web pendente |
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

O código atual está em `engine/`, a base em `base/desenvolvimento/`, os testes em `tests/` e os geradores em `scripts/`. As fontes oficiais e o planejamento estão em `docs/fontes/` e `docs/superpowers/`. O grafo navegável e seu cofre ficam em `graphify-out/` e `obsidian/01-conhecimento/`.

Esta entrega parcial contém fontes Markdown. PDFs finais, slides em PDF e formato editável, vídeo de reserva, licença e pacote `.zip` final ainda dependem da conclusão/revisão do grupo. Não há `uv.lock` ou `package-lock.json` para os componentes ainda não implementados; o núcleo atual não exige esses gerenciadores.

Prazo informado nos documentos oficiais: **22/10/2026 às 20:00**. Apresentação: **23/10/2026 às 09:00**. O alvo interno de envio às **18:30** é uma decisão da equipe no planejamento. Duração da fala, limite de anexo e infraestrutura da apresentação precisam de confirmação com a organização.
