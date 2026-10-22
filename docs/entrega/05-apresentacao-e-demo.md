# Roteiro de apresentação e demonstração — versão disponível

Este roteiro acompanha a integração em `codex-davi`: interface React, motor, `kb/`, base ativa `v0002`, API FastAPI com 27 operações e persistência SQLite. Há testes de navegador com API real; o editor gráfico permanece pendente. Nomes e responsabilidades informados pela equipe estão no [índice](README.md); as transições e a participação humana precisam de ensaio.

A duração oficial não consta dos materiais fornecidos. **10 minutos de fala mais 4 de demonstração** e a alternativa de **5 minutos incluindo demo** são hipóteses de preparação, sujeitas à confirmação com a organização. O conteúdo abaixo é um roteiro editorial; slides finais e PDFs ainda precisam ser produzidos/revisados.

## Fala principal — 10 minutos

| Slide | Mensagem e evidência visual sugerida | Papel | Tempo |
|---|---|---|---|
| 1. Problema e T1 Anamnese | Coletar sinais e tornar o raciocínio de triagem explicável; citar [A], slide 9 | C | 0:45 |
| 2. O que é sistema especialista | Mostrar fato → regra → conclusão; IA auxiliou a construção, motor faz a consulta | A | 1:00 |
| 3. Arquitetura disponível | Diagrama do documento 02: React, API FastAPI, SQLite, `kb`, versão ativa, motor e explicação; editor pendente | B | 1:15 |
| 4. Raciocínio e segurança | Três camadas, premissa mínima, combinação MYCIN, seis telas e bandeiras; um único exemplo numérico | A | 1:45 |
| 5. Base e limites clínicos | 8 doenças, 56 regras, todas como suposição; fontes contextuais não calibram CF | C | 1:00 |
| 6. Evidência de funcionamento | Baseline integrado: 1066 testes Python aprovados, 1 ignorado, 170 subtestes e 34 casos sintéticos; testes de interface e navegador registrados no relatório web; não confundir com validação clínica | B | 1:00 |
| 7. IA e julgamento da equipe | Três exemplos comprovados: restauração direta, regra de TPB sem febre e rejeição de aprovação clínica automática; 40 s por papel | A/B/C | 2:00 |
| 8. Riscos e próximos passos | Revisão especializada, licença, editor, limitações de coleta R15/R16, Swagger offline e ensaio físico sem rede | A | 0:45 |
| 9. Encerramento | A decisão é reproduzível a partir da base, fatos e ordem; mostrar repositório e limitações | C | 0:30 |

Total: **600 segundos (10:00)**. A demo soma **240 segundos (4:00)**; total de preparação: **14:00**, sem perguntas da banca. Não acrescentar uma demonstração de componente planejado para preencher o tempo.

Um exemplo de CF pode usar dois apoios positivos independentes de 0,60 e 0,50: `0,60 + 0,50 × (1 − 0,60) = 0,80`. É uma ilustração aritmética, não calibração clínica. Explique que sinais duplicados não devem ser considerados independentes; a base agrupa leite/caneca com `max`.

## Demonstração principal — interface em localhost, 4 minutos

Instalar o ambiente Python uma vez seguindo [api/README.md](../../api/README.md) e Node.js 24 para compilar a interface. Antes da demo, conferir a versão ativa e o banco fora do OneDrive. O script compila `web/` quando o build está ausente; após alterações, executar `npm.cmd run build` em `web/`. Instalações iniciais precisam de internet. O `-Reset` apaga o SQLite escolhido: usá-lo apenas no banco fictício destinado ao ensaio.

```powershell
$env:ANAMNESE_DB = "$env:LOCALAPPDATA\anamnese\anamnese.db"
powershell -ExecutionPolicy Bypass -File scripts\rodar.ps1 -SemNavegador
```

| Intervalo | Ação | Evidência a mostrar |
|---|---|---|
| 0:00–0:30 | Abrir http://localhost:8000/ e clicar em Iniciar verificação | Tela inicial com os dois modos; API cria animal fictício e sessão na `v0002` |
| 0:30–1:00 | Digitar `12,5` em dias, enviar e corrigir para `90` | Mensagem 422 junto ao campo, sem avanço; após corrigir, aparece a lateral de hipóteses |
| 1:00–2:00 | Começar C-MAS-01 no produtor: estado térmico normal, nenhuma alteração de postura, apetite normal, leite alterado + úbere inflamado + queda de produção; abrir o por quê antes de responder | Opções fechadas e sinais mamários registrados antes da troca, na mesma sessão |
| 2:00–2:40 | Clicar Mudar para modo especialista, ler o aviso e confirmar. Responder à temperatura retal (38,5 °C no caso fictício, digitando `38.5`) e às excreções; responder Não sei aos exames sem observação | PATCH usa `veterinario`; próxima pergunta e limite vêm da API. Os sinais anteriores permanecem; Voltar permite corrigi-los. Mudar para modo produtor faz o caminho inverso sem confirmação |
| 2:40–3:10 | Examinar o parecer e abrir Como cheguei aqui? | Um único parecer combina as respostas de antes e depois da troca; mastite continua sustentada pelos sinais mamários. Exibir o percentual retornado pela API, sem fixar valor após exames adicionais |
| 3:10–3:40 | Nova verificação: caso C-HIP-01, 1 dia, extremidades frias, decúbito; mostrar a troca dentro do alerta ou abrir o parecer | Pausa e urgência chamar_agora preservadas; trocar para especialista não apaga a bandeira. Esc e clique no fundo não dispensam o alerta |
| 3:40–4:00 | Mostrar o relatório web e declarar limitações | Casos sintéticos, editor pendente e revisão clínica não realizada; não apresentar teste automatizado como ensaio humano |

`/api/docs` serve o HTML do Swagger, mas usa recursos externos de CDN na configuração atual. A SPA usa fontes e ilustrações locais e os E2E verificam que não há requisições externas. O ensaio automatizado HTTP histórico está em [evidencias-verificacao.json](evidencias-verificacao.json); a verificação atual de navegador está em [web/QUALIDADE.md](../../web/QUALIDADE.md), com [capturas das telas](capturas/). Nenhum deles substitui o ensaio humano com Wi-Fi desligado. Encerrar o servidor com Ctrl+C ao terminar.

### Troca de modo sem reiniciar a análise

O controle do cabeçalho mostra o modo atual e permite produtor ↔ especialista. Entrar no especialista exige confirmação com o aviso de complexidade; voltar ao produtor é direto. Durante a chamada, envio de resposta e outra troca ficam bloqueados. Há anúncio para leitores de tela, foco na pergunta retornada e recuperação de conflito por leitura da sessão. O parecer parcial oferece a mesma troca e retorna à anamnese.

As respostas anteriores não são reenviadas ao mudar de modo. O histórico permanece acessível por Voltar, e as correções são recalculadas pelo servidor. A tela térmica tem símbolos diferentes em cada modo: para corrigir o fato original, a interface muda temporariamente ao modo da resposta, envia o PUT e restaura o modo escolhido sob a mesma trava, mostrando apenas o resultado final. Se houver falha, relê o estado, conserva o histórico e informa se a correção foi gravada ou se o modo não pôde ser restaurado. Não converte observação de extremidades em temperatura nem calcula CF no navegador.

O teste `web/e2e/troca-modo.spec.ts` usa a API real e cobre sinais mamários informados no produtor, termometria no especialista, correção de dias e da observação térmica anterior, pausa, volta ao produtor e parecer parcial. O parecer final conserva o mesmo identificador de sessão e a evidência dos sinais anteriores. Esses testes são sintéticos, não validação clínica.

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
| O sistema roda sem internet? | Motor, base, API, fontes e imagens da interface executam localmente após instalar e compilar. E2E não emitem chamadas externas; Wi-Fi fisicamente desligado e máquina reserva ainda exigem ensaio da equipe. Swagger usa CDN. |
| Onde está o editor? | Em andamento em outra sessão. Neste recorte, JSON, validador, conversão de grafo e rotas de versões estão disponíveis; não se afirma conclusão da edição visual. |
| Por que essas oito doenças? | São o recorte definido pela equipe na especificação. Não representam todos os diagnósticos diferenciais da clínica bovina. |
| O que significa `sem_problema`? | Ausência de um gatilho de urgência pelos critérios atuais; não é comprovação de saúde ou segurança clínica. |
| Como mudam a base sem perder rastreabilidade? | `kb.Repositorio` grava versões imutáveis; a API executa casos, controla a ativação e prende a sessão à versão. Alteração de regra exige nova versão; `v0002` foi preservada. |
| O projeto atende integralmente a open source? | O código está disponível; falta registrar a licença do projeto e revisar o pacote final. Não declarar essa pendência resolvida. |

## Ensaio e reserva

Cada pessoa deve explicar uma regra e uma parte que não escreveu, identificar uma limitação e demonstrar o trecho sob sua responsabilidade. Registrar resultado, dúvida e correção no diário correspondente. Preparar captura ou vídeo da execução atual como reserva, sem substituir a demonstração real exigida. Ainda faltam registro de ensaio, arquivos visuais e confirmação do tempo oficial.
