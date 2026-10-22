# Roteiro de apresentação e demonstração — versão disponível

Este roteiro acompanha a execução da Seção 5 em `codex-davi`: motor, `kb/`, base ativa `v0001`, API FastAPI com 27 operações e persistência SQLite. A interface web e o editor gráfico estão em andamento em outra sessão; não há evidência de teste de navegador neste trabalho. Nomes e responsabilidades informados pela equipe estão no [índice](README.md); as transições e a participação humana precisam de ensaio.

A duração oficial não consta dos materiais fornecidos. **10 minutos de fala mais 4 de demonstração** e a alternativa de **5 minutos incluindo demo** são hipóteses de preparação, sujeitas à confirmação com a organização. O conteúdo abaixo é um roteiro editorial; slides finais e PDFs ainda precisam ser produzidos/revisados.

## Fala principal — 10 minutos

| Slide | Mensagem e evidência visual sugerida | Papel | Tempo |
|---|---|---|---|
| 1. Problema e T1 Anamnese | Coletar sinais e tornar o raciocínio de triagem explicável; citar [A], slide 9 | C | 0:45 |
| 2. O que é sistema especialista | Mostrar fato → regra → conclusão; IA auxiliou a construção, motor faz a consulta | A | 1:00 |
| 3. Arquitetura disponível | Diagrama do documento 02: API FastAPI, SQLite, `kb`, versão ativa, motor e explicação; web/editor em andamento | B | 1:15 |
| 4. Raciocínio e segurança | Três camadas, premissa mínima, combinação MYCIN, seis telas e bandeiras; um único exemplo numérico | A | 1:45 |
| 5. Base e limites clínicos | 8 doenças, 56 regras, todas como suposição; fontes contextuais não calibram CF | C | 1:00 |
| 6. Evidência de funcionamento | 1006 testes aprovados, 1 ignorado, 110 subtestes e 34 casos sintéticos; resultados pela API gravados no SQLite; não confundir com validação clínica | B | 1:00 |
| 7. IA e julgamento da equipe | Três exemplos comprovados: restauração direta, regra de TPB sem febre e rejeição de aprovação clínica automática; 40 s por papel | A/B/C | 2:00 |
| 8. Riscos e próximos passos | Revisão especializada, licença, web/editor, limitações de coleta R15/R16, Swagger offline e ensaio físico sem rede | A | 0:45 |
| 9. Encerramento | A decisão é reproduzível a partir da base, fatos e ordem; mostrar repositório e limitações | C | 0:30 |

Total: **600 segundos (10:00)**. A demo soma **240 segundos (4:00)**; total de preparação: **14:00**, sem perguntas da banca. Não acrescentar uma demonstração de componente planejado para preencher o tempo.

Um exemplo de CF pode usar dois apoios positivos independentes de 0,60 e 0,50: `0,60 + 0,50 × (1 − 0,60) = 0,80`. É uma ilustração aritmética, não calibração clínica. Explique que sinais duplicados não devem ser considerados independentes; a base agrupa leite/caneca com `max`.

## Demonstração principal — API em localhost, 4 minutos

Instalar o ambiente uma vez seguindo [api/README.md](../../api/README.md). Antes da demo, conferir a versão ativa e o banco fora do OneDrive. O `-Reset` apaga o SQLite escolhido: usá-lo apenas no banco fictício destinado ao ensaio.

```powershell
$env:ANAMNESE_DB = "$env:LOCALAPPDATA\anamnese\anamnese.db"
powershell -ExecutionPolicy Bypass -File scripts\rodar.ps1 -Reset -SemNavegador
```

| Intervalo | Ação | Evidência a mostrar |
|---|---|---|
| 0:00–0:30 | Consultar `GET /api/saude` e a versão ativa | HTTP 200; `base/ativa.json` aponta para `v0001` |
| 0:30–1:00 | Criar animal fictício e sessão em modo produtor | `POST /api/animais` e `POST /api/sessoes` retornam 201; sessão vinculada a `v0001` |
| 1:00–2:00 | Responder as telas de triagem e as perguntas dinâmicas | `POST /api/sessoes/{id}/triagem/{tela}` e `/respostas`; para o exemplo mamário, marcar leite alterado e úbere inflamado |
| 2:00–3:00 | Abrir parecer, por quê e como | `/parecer`, `/porque/{simbolo}` e `/como/mastite` retornam 200 e explicações das regras |
| 3:00–3:40 | Executar os casos pela API | `POST /api/base/versoes/v0001/execucoes` com `{"casos":null}`: 34 passaram, zero falhas, execução persistida |
| 3:40–4:00 | Mostrar limites e evidências | R15/R16, CF não é probabilidade e validação clínica pendente |

`/api/docs` serve o HTML do Swagger, mas usa recursos externos de CDN na configuração atual. Não prometer Swagger utilizável sem internet; o roteiro offline deve usar chamadas HTTP locais ou a CLI. O ensaio automatizado HTTP está em [evidencias-verificacao.json](evidencias-verificacao.json); não substitui ensaio humano nem teste E2E do frontend. Encerrar o servidor com Ctrl+C ao terminar.

## Reserva — núcleo por terminal, 4 minutos

Preparar Python 3.12+, abrir a raiz do repositório e deixar os dois comandos abaixo disponíveis. Nenhuma instalação de pacotes é necessária para o núcleo. A equipe ainda precisa registrar o ensaio na máquina principal e na reserva, com rede desligada.

| Intervalo | Ação executável | O que explicar |
|---|---|---|
| 0:00–0:30 | Mostrar o resumo de `python -m unittest discover -s tests/engine -t .` | Quantidade, conclusão real e separação entre testes e casos clínicos |
| 0:30–1:10 | Executar o caso `alerta-decubito.json` | `chamar_agora`, R-BV-01 e `alerta.pausa: true`; o executor reconhece a pausa automaticamente |
| 1:10–2:00 | Executar o trecho Python abaixo, até `como` | Estado, pausa, razão da pergunta e encadeamento de hipocalcemia |
| 2:00–2:50 | Continuar o trecho com troca de modo e snapshot | Mesmos fatos, termometria adicional, preservação de ordem e restauração sem banco |
| 2:50–3:30 | Executar `sinais-mamarios.json` | Primeira hipótese mastite e `observar`, conforme critérios deste exemplo |
| 3:30–4:00 | Abrir os documentos 03 e 06 | Fonte/CF/rastreabilidade e o que permanece não validado |

Comandos da CLI:

```powershell
python -m engine base/desenvolvimento/anamnese-bovinos-v3.1.0-revisao1.json base/desenvolvimento/casos/alerta-decubito.json
python -m engine base/desenvolvimento/anamnese-bovinos-v3.1.0-revisao1.json base/desenvolvimento/casos/sinais-mamarios.json
```

Trecho para o interpretador Python aberto na raiz do repositório:

```python
import json
from pathlib import Path
from engine.sessao import Sessao

base = json.loads(Path('base/desenvolvimento/anamnese-bovinos-v3.1.0-revisao1.json').read_text(encoding='utf-8'))
s = Sessao(base, modo='produtor', ficha={'dias_em_lactacao': 2})
print(s.estado()['proxima'])
print(s.porque('extremidades'))
s.responder_triagem('estado_termico', 'normal')
s.responder_triagem('atitude_locomocao', ['decubito'])
print(s.estado()['urgencia'], s.estado()['pausa'], s.estado()['bandeiras'])
print(s.como('hipocalcemia'))

s.trocar_modo('veterinario')
print(s.estado()['proxima'])
s.responder_triagem('estado_termico', 38.5)
snapshot = json.loads(json.dumps(s.exportar()))
restaurada = Sessao.restaurar(base, **snapshot)
print(restaurada.estado() == s.estado())
```

Não apresentar a saída da CLI como tela web nem a pausa automática do executor como clique humano. O snapshot do trecho acima demonstra o contrato do núcleo; a persistência SQLite é exercitada separadamente pelas rotas da API.

## Versão curta — 5 minutos incluindo demo

| Bloco | Papel | Tempo |
|---|---|---|
| Problema e objetivo | C | 0:30 |
| Sistema especialista e arquitetura atual | A/B | 0:45 |
| Base e testes reais | B | 0:30 |
| Um exemplo de julgamento sobre a IA | A | 0:30 |
| Demo reduzida: bandeira, explicação e exemplo mamário | C conduz | 2:00 |
| Limitações e próximos passos | A | 0:30 |
| Encerramento | C | 0:15 |

Total: **300 segundos (5:00)**. A troca de modo e a restauração ficam como apoio para perguntas.

## Perguntas prováveis da banca

| Pergunta | Resposta apoiada pelo estado atual |
|---|---|
| Onde está a IA durante a consulta? | Na ferramenta de desenvolvimento, fora do runtime. As conclusões vêm de Python, fatos e JSON locais. |
| Como provar o raciocínio? | Exibir a regra, a premissa, a contribuição de CF e a combinação no traço de `como`. |
| Por que perguntar isso? | `porque` conserva o motivo do instante da escolha; triagem tem origem, posição da tela e doenças alimentadas. |
| A porcentagem é chance de a vaca ter a doença? | Não. É a apresentação do CF do sistema; o próprio parecer contém o aviso. |
| Quem validou os pesos clínicos? | Não há validação especializada registrada para esta base. Todas as regras continuam como suposição. |
| Quantos casos clínicos foram validados? | Nenhum conjunto clínico real. Há 34 casos sintéticos de regressão, dois deles os exemplos originais, e testes automatizados de software. |
| Pode haver mais de uma doença? | Sim. Não há exclusão mútua forçada, e há teste de coexistência de mastite e hipocalcemia. |
| O que acontece com “não sei”? | CF zero, sem inferência de ausência; a resposta é contabilizada para evitar repetição. |
| Corrigir uma resposta muda uma bandeira? | Pode mudar. O motor reprocessa os valores corrigidos na ordem real dos lotes, preservando gatilhos históricos ainda justificados. |
| A ordem importa? | O cálculo de CF é testado com permutações; a memória de alertas da sessão também depende da ordem de chegada, que é persistida no snapshot. |
| O sistema roda sem internet? | Motor, base e API executam localmente. Resultados do ensaio e seu alcance estão nas evidências; Wi-Fi fisicamente desligado e navegador completo ainda exigem ensaio da equipe. Swagger usa CDN. |
| Onde está o editor? | Em andamento em outra sessão. Neste recorte, JSON, validador, conversão de grafo e rotas de versões estão disponíveis; não se afirma conclusão da edição visual. |
| Por que essas oito doenças? | São o recorte definido pela equipe na especificação. Não representam todos os diagnósticos diferenciais da clínica bovina. |
| O que significa `sem_problema`? | Ausência de um gatilho de urgência pelos critérios atuais; não é comprovação de saúde ou segurança clínica. |
| Como mudam a base sem perder rastreabilidade? | `kb.Repositorio` grava versões imutáveis; a API executa casos, controla a ativação e prende a sessão à versão. Alteração de regra exige nova versão; `v0001` foi preservada. |
| O projeto atende integralmente a open source? | O código está disponível; falta registrar a licença do projeto e revisar o pacote final. Não declarar essa pendência resolvida. |

## Ensaio e reserva

Cada pessoa deve explicar uma regra e uma parte que não escreveu, identificar uma limitação e demonstrar o trecho sob sua responsabilidade. Registrar resultado, dúvida e correção no diário correspondente. Preparar captura ou vídeo da execução atual como reserva, sem substituir a demonstração real exigida. Ainda faltam registro de ensaio, arquivos visuais e confirmação do tempo oficial.
