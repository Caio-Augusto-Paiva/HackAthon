# Riscos, lacunas e fechamento da entrega

Estado integrado da Seção 5, branch `codex-davi`, baseline `f46cd6e`. Responsáveis A/B/C são papéis do planejamento; nomes e responsabilidades informados constam do índice. Gravidade indica impacto para a entrega ou uso pretendido, não classificação clínica de um animal.

## Registro de riscos

| ID | Risco ou lacuna | Gravidade | Evidência atual | Mitigação e condição de encerramento | Papel |
|---|---|---|---|---|---|
| R01 | Conhecimento clínico e CF sem validação especializada | Alta | 56 regras como `suposicao_a_validar`; zero `validada` | Revisar com veterinário/RERUM; documentar quem revisou, escopo e critérios. Até lá, limitar a desenvolvimento/demonstração | A |
| R02 | Confiança excessiva por sinais correlacionados | Alta | Cetose pode chegar a CF 0,83086641 sem exame; claudicação/dor podem somar 0,65 para dermatite | Calibrar com casos representativos; não converter CF em probabilidade. Agrupamento leite/caneca já reduz um caso de duplicação | A |
| R03 | Falso entendimento de `sem_problema` | Alta | Fallback por ausência de gatilhos, inclusive dados incompletos | Explicar o alcance no parecer/apresentação; revisar mensagem e política com especialista antes de uso clínico | A/C |
| R04 | Interface final e editor gráfico em andamento | Alta | API FastAPI, `kb/`, SQLite e `scripts/rodar.ps1` já existem; frontend é trabalho paralelo | Equipe integrar e validar o navegador; até lá, demonstrar API/CLI e declarar a ausência de evidência E2E neste recorte | B/C |
| R05 | Regressão na restauração da sessão | Alta | API persiste snapshots e tem testes de troca de modo/correção; ordem e origens continuam essenciais | Manter a cobertura e repetir os fluxos após integrações do frontend | B |
| R06 | Divergência entre v0001 e especificação clínica | Alta | 56 regras ainda não validadas; sinais e estimativas da Seção 5 divergem (R15/R16) | Conciliar com especialista; alterações via nova versão e casos, nunca sobrescrever `v0001`. Ativação operacional não é aprovação clínica | A/B |
| R07 | Código entregue sem licença declarada | Alta | Arquivo `LICENSE` ausente | Equipe escolher e registrar licença; revisar materiais e dependências do pacote final antes de declarar requisito integralmente cumprido | Todos |
| R08 | Documentação manual divergir da implementação | Média | Processo/arquitetura precisam de revisão após novas integrações | Regras/casos já têm geração e teste de sincronismo; repetir testes e curadoria no fechamento | A/B |
| R09 | Contagem de testes ser confundida com validação clínica | Alta | 1006 testes aprovados, 1 ignorado, 110 subtestes; 34 casos sintéticos; zero validação clínica | Não somar as 125 execuções unittest (também coletadas por pytest); manter categorias separadas | Todos |
| R10 | Falha da máquina ou dependência externa na demo | Alta | Dependências Python instaladas; ensaios HTTP registrados separadamente; Swagger depende de CDN | Ensaio físico sem Wi-Fi e máquina reserva ainda obrigatórios; usar HTTP/CLI como roteiro offline | B/C |
| R11 | Tempo da fala e infraestrutura desconhecidos | Média | Materiais oficiais não informam duração nem infraestrutura | Confirmar com organização; ensaiar roteiros de 14 e 5 minutos, sem assumir projetor/rede | C |
| R12 | Equipe não dominar o que foi gerado com IA | Alta | Diários B/C e prova de entendimento ainda incompletos | Cada integrante explicar parte própria e alheia; registrar ensaio e corrigir dúvidas | Todos |
| R13 | Envio incompleto ou fora do prazo | Alta | PDFs, slides editáveis, contatos e pacote final pendentes | Checklist abaixo; alvo interno 22/10 às 18:30, prazo oficial às 20:00; confirmar recebimento pelo canal escolhido | C |
| R14 | Conflitos com trabalho paralelo de API/frontend | Média | Esta execução usa checkout isolado e baseline `f46cd6e`; pushes só em `codex-davi` | Não alterar `api/`, `web/`, `contratos/` ou `tests/api/`; equipe faz a integração na branch compartilhada | Todos |

As probabilidades de ocorrência não foram medidas; não atribuímos percentuais artificiais aos riscos. A prioridade deve ser revista pela equipe conforme avanço de API/web e disponibilidade de especialista.

## Achados da Camada 3 — Seção 5, branch codex-davi

- **R15 — Seleção e coleta de sinais com evidência inicial fraca (alta; A/B):** na `v0001`, `C-DAB-DIALOGO` termina com cetose 40% e abomaso 30%; `flanco_esquerdo_afundado` não é perguntado. O positivo `C-DAB-01` fornece esse achado como observação prévia fictícia na ficha do executor, alcançando 57%; não demonstra que a interface/API capture esse campo. `C-MET-03`, `C-TPB-03`, `C-HIP-03`, `C-DAB-03` e `C-ACI-03` podem encerrar em `sem_problema` sem solicitar os sinais adicionais. Os percentuais são confiança do sistema, não probabilidades. Equipe deve decidir política de coleta, limiares e mensagem; não houve alteração silenciosa em regra, motor ou API.
- **R16 — Os esperados históricos da Seção 5 não equivalem à base revisada (alta; A):** mastite com leite alterado + úbere tem CF 0,797, exibido como 80%, porém não alcança confirmação de 0,80 e encerra por `sem_perguntas`. Decúbito no periparto produz hipocalcemia 64%, não 80–100%; claudicação + dor produz dermatite 65%, não 80–100%. No caso de limite, só cetose excede 0,35; acidose=0,35 e dermatite=0,30 não entram nas inconclusivas. Metrite na comorbidade alcança 74%, abaixo do antigo 75%. A `v0001` não contém alguns sinais do roteiro (por exemplo, perda de condição corporal e lesão podal perguntável ao produtor); os cenários usam os símbolos disponíveis e registram os desvios. A `v0002` acrescenta limites e precisão numérica, sem alterar as evidências clínicas. Revisão clínica e novas regras exigem outra versão e decisão da equipe.
- **Correção de resposta:** o modelo `kb.Caso` não representa operações de correção. O cenário é exercitado diretamente com `Sessao` em `tests/casos/test_casos_conhecidos.py`: retirar decúbito remove R-BV-01 e a pausa, preservando dias em lactação e estado térmico. Não foi criado campo incompatível com o contrato em paralelo.
- **Contagens desta etapa:** 34 casos JSON (31 cenários adaptados, dois exemplos preservados e uma regressão explícita de diálogo), além do teste dedicado de correção. Cada esperado é literal e revisado contra as regras atuais; não é calculado pelo mesmo código que faz a asserção. Esses casos não são validação clínica.

## Ensaio HTTP e dependências de rede

- **Resultado observado:** `scripts/rodar.ps1 -Reset -SemNavegador` iniciou a API com `v0001` e banco fictício em `%LOCALAPPDATA%\anamnese\anamnese.db`, fora do OneDrive. Saúde e HTML do Swagger responderam 200; animal e sessão foram criados, o diálogo chegou ao parecer, `/porque` e `/como` responderam, e 34/34 casos passaram pela API. Os processos iniciados pelo ensaio foram encerrados e a porta 8000 ficou livre.
- O fluxo foi repetido bloqueando conexões TCP e resolução DNS externas nos processos Python do reset, semente e servidor; loopback permaneceu permitido. O bloqueio foi comprovado por tentativa interceptada para um endereço não loopback. Esse isolamento comprova o fluxo do backend nesse alcance, **não** um ensaio físico com Wi-Fi desligado nem um E2E de navegador. Adaptadores físicos permaneceram ativos; a conta não é administradora e outras sessões dependem da conexão. A equipe ainda deve ensaiar sem Wi-Fi na máquina principal e na reserva.
- **R17 — Swagger depende de recursos externos (média; B):** `/api/docs` retorna HTML 200, mas referencia JavaScript/CSS em `cdn.jsdelivr.net` e ícone em `fastapi.tiangolo.com`. Pedido à sessão da API: avaliar servir os recursos localmente ou documentar outro cliente offline. Não foi editado nenhum arquivo em `api/`, `web/`, `contratos/` ou `tests/api/`. Até a resolução, não apresentar HTML 200 como prova de Swagger interativo sem internet.
- Comandos, corpos de requisição, respostas e logs estão em [evidencias-verificacao.json](evidencias-verificacao.json). São dados fictícios de software; não há envio externo nem validação clínica.

## Correções editoriais aplicadas na Seção 5

| Trecho do roteiro original | Veredito | Evidência integrada | Ajuste aplicado nesta documentação |
|---|---|---|---|
| “30/31 casos conhecidos” | Especificação histórica | 34 casos JSON executados na ativa, com desvios explícitos R15/R16 | Documentar o conjunto real e preservar as estimativas antigas como referência, não como validação clínica |
| “editor salvando versão e rodando casos” na demo | Editor em andamento | Rotas de versões e casos disponíveis; frontend fora desta sessão | Demonstrar a API; não alegar teste de navegador |
| `03-regras` gerado da base ativa | Implementado | Ponteiro `v0002` presente e válido | Gerador sem `--base` segue o ponteiro; documentos 03/04 e teste de sincronismo usam a ativa |
| “sem código nesta fase” no rascunho histórico | Desatualizado para a solicitação atual | Motor, testes e integração já implementados | Descrever o código existente e criar somente o utilitário necessário à documentação |
| Equipe e telefones no pacote | Dados parcialmente fornecidos | Nomes/responsabilidades informados em `fcdcea9`; telefones ausentes | Preservar os nomes fornecidos e solicitar os contatos no fechamento humano |
| Fontes e CF apresentados como conhecimento validado | Risco de extrapolação | Todas as regras continuam como suposição | Separar fonte contextual, comportamento de software e validação clínica |
| OpenAPI, SQLite e `rodar.ps1` tratados como futuros | Texto desatualizado | 27 operações no contrato, SQLite e scripts presentes | Documentos 02/05/06 descrevem o backend real; web/editor em andamento |

## Checklist de fechamento

- [x] Documentar processo, arquitetura e regras do escopo implementado.
- [x] Gerar regras e casos a partir de arquivos executáveis, com teste de sincronismo.
- [x] Preparar comandos de demonstração e perguntas prováveis da banca.
- [x] Explicitar o caráter sintético dos exemplos e a validação clínica pendente.
- [ ] Conferir os nomes/responsabilidades fornecidos e completar os telefones.
- [ ] Completar diários pessoais, revisões realmente realizadas e prova de entendimento.
- [ ] Registrar licença do projeto e revisar as licenças do material empacotado.
- [x] Integrar base ativa, `kb/`, API, persistência e casos conhecidos deste recorte.
- [ ] Concluir web/editor e executar E2E na sessão responsável; confirmar o escopo da apresentação.
- [ ] Conciliar a base com a especificação e obter revisão especializada, se viável; registrar as limitações remanescentes.
- [ ] Confirmar duração da fala, infraestrutura e limite/formato de anexos com a organização.
- [ ] Produzir e conferir PDFs dos documentos, slides em PDF e formato editável.
- [ ] Ensaiar na máquina principal e na reserva, com rede desligada; preparar captura/vídeo.
- [ ] Regenerar os documentos 03/04 e rodar a suíte completa depois da última mudança de código ou base.
- [ ] Preparar `.zip` sem caches, ambiente virtual, dados pessoais de teste ou dependências instaladas.
- [ ] Conferir contatos, abrir os arquivos em outra máquina, enviar e confirmar recebimento.

Os três últimos marcos são da entrega final. Este checkpoint não envia mensagens à organização nem publica um pacote final.

## Resumo do que falta resolver

A documentação técnica acompanha o motor, a base ativa, a API e o SQLite existentes.
Web/editor, política de coleta dos casos R15/R16, licença e validação clínica exigem trabalho ou decisão.
A equipe precisa completar seus dados, ensaiar e produzir os arquivos finais antes do envio de 22/10.
