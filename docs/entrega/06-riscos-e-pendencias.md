# Riscos, lacunas e fechamento da entrega

Estado em 21/10/2026. Este registro descreve o checkout auditado; responsáveis A/B/C são papéis do planejamento, com nomes ainda a confirmar. Gravidade indica impacto para a entrega ou uso pretendido, não classificação clínica de um animal.

## Registro de riscos

| ID | Risco ou lacuna | Gravidade | Evidência atual | Mitigação e condição de encerramento | Papel |
|---|---|---|---|---|---|
| R01 | Conhecimento clínico e CF sem validação especializada | Alta | 56 regras como `suposicao_a_validar`; zero `validada` | Revisar com veterinário/RERUM; documentar quem revisou, escopo e critérios. Até lá, limitar a desenvolvimento/demonstração | A |
| R02 | Confiança excessiva por sinais correlacionados | Alta | Cetose pode chegar a CF 0,83086641 sem exame; claudicação/dor podem somar 0,65 para dermatite | Calibrar com casos representativos; não converter CF em probabilidade. Agrupamento leite/caneca já reduz um caso de duplicação | A |
| R03 | Falso entendimento de `sem_problema` | Alta | Fallback por ausência de gatilhos, inclusive dados incompletos | Explicar o alcance no parecer/apresentação; revisar mensagem e política com especialista antes de uso clínico | A/C |
| R04 | Aplicação final em localhost incompleta | Alta | Não há `api/`, `web/`, `kb/`, banco ou `rodar.ps1` | Integrar os componentes; enquanto isso, demonstrar somente o núcleo por terminal e declarar o escopo parcial | B/C |
| R05 | Uso de snapshot incompleto na integração | Alta | Restauração exata depende de `ordem_respostas`, origens e tela | API deve persistir `exportar()` integralmente e testar ida e volta com troca de modo/correção | B |
| R06 | Divergência entre base de desenvolvimento e especificação clínica | Alta | Base revisada tem 56 regras; alguns sinais da especificação não constam do anexo original | Conciliar versões e critérios, incluindo cobertura de abomaso à direita e sinais ausentes. Não ativar silenciosamente como base canônica | A/B |
| R07 | Código entregue sem licença declarada | Alta | Arquivo `LICENSE` ausente | Equipe escolher e registrar licença; revisar materiais e dependências do pacote final antes de declarar requisito integralmente cumprido | Todos |
| R08 | Documentação manual divergir da implementação | Média | Processo/arquitetura precisam de revisão após novas integrações | Regras/casos já têm geração e teste de sincronismo; repetir testes e curadoria no fechamento | A/B |
| R09 | Contagem de testes ser confundida com validação clínica | Alta | 135 testes de software e dois casos sintéticos | Manter contagens separadas; retirar alegações de acurácia/diagnóstico definitivo | Todos |
| R10 | Falha da máquina ou dependência inesperada na demo | Alta | Núcleo usa Python padrão; ensaio offline ainda sem registro | Preparar Python, máquina reserva, comandos e captura; testar sem rede no equipamento da apresentação | B/C |
| R11 | Tempo da fala e infraestrutura desconhecidos | Média | Materiais oficiais não informam duração nem infraestrutura | Confirmar com organização; ensaiar roteiros de 14 e 5 minutos, sem assumir projetor/rede | C |
| R12 | Equipe não dominar o que foi gerado com IA | Alta | Diários B/C e prova de entendimento ainda incompletos | Cada integrante explicar parte própria e alheia; registrar ensaio e corrigir dúvidas | Todos |
| R13 | Envio incompleto ou fora do prazo | Alta | PDFs, slides editáveis, contatos e pacote final pendentes | Checklist abaixo; alvo interno 22/10 às 18:30, prazo oficial às 20:00; confirmar recebimento pelo canal escolhido | C |
| R14 | Regressão após contribuições paralelas | Média | Branch recebe correções de outras sessões, como as de reprocessamento | Atualizar por fast-forward, revisar diff, rodar suíte inteira e regenerar documentação antes do envio | Todos |

As probabilidades de ocorrência não foram medidas; não atribuímos percentuais artificiais aos riscos. A prioridade deve ser revista pela equipe conforme avanço de API/web e disponibilidade de especialista.

## Correções editoriais da Seção 6 que já podem ser aplicadas

| Trecho do roteiro original | Veredito | Prova no checkpoint | Ajuste aplicado nesta documentação |
|---|---|---|---|
| “30 casos conhecidos rodam contra cada versão” | Lacuna/inconsistência com outros trechos que falam em 31 | Só dois casos de desenvolvimento estão integrados | Documentar dois exemplos; manter expansão como pendência, sem alegar 30/31 aprovados |
| “editor salvando versão e rodando casos” na demo | Ação ainda indisponível | Editor e API ausentes | Substituir por CLI, traço e snapshot disponíveis |
| `03-regras` gerado exclusivamente da base ativa | Lacuna para o estado atual | Não há `base/ativa.json` | Usar `--base` explícito e rotular desenvolvimento; manter leitura do ponteiro para quando existir |
| “sem código nesta fase” no rascunho histórico | Desatualizado para a solicitação atual | Motor, testes e integração já implementados | Descrever o código existente e criar somente o utilitário necessário à documentação |
| Equipe e telefones no pacote | Lacuna de informação | Dados não fornecidos | Campos a preencher, sem inferir identidade pelos commits |
| Fontes e CF apresentados como conhecimento validado | Risco de extrapolação | Todas as regras continuam como suposição | Separar fonte contextual, comportamento de software e validação clínica |
| Contratos OpenAPI, locks e `rodar.ps1` tratados como disponíveis | Trabalho planejado | Arquivos não encontrados no checkout | Apresentar como pendência; comandos atuais usam somente Python |

## Checklist de fechamento

- [x] Documentar processo, arquitetura e regras do escopo implementado.
- [x] Gerar regras e casos a partir de arquivos executáveis, com teste de sincronismo.
- [x] Preparar comandos de demonstração e perguntas prováveis da banca.
- [x] Explicitar o caráter sintético dos exemplos e a validação clínica pendente.
- [ ] Completar nomes, telefones e associação das pessoas aos papéis A/B/C.
- [ ] Completar diários pessoais, revisões realmente realizadas e prova de entendimento.
- [ ] Registrar licença do projeto e revisar as licenças do material empacotado.
- [ ] Concluir API/web/editor ou acordar com a equipe o escopo que será apresentado como parcial.
- [ ] Conciliar a base com a especificação e obter revisão especializada, se viável; registrar as limitações remanescentes.
- [ ] Confirmar duração da fala, infraestrutura e limite/formato de anexos com a organização.
- [ ] Produzir e conferir PDFs dos documentos, slides em PDF e formato editável.
- [ ] Ensaiar na máquina principal e na reserva, com rede desligada; preparar captura/vídeo.
- [ ] Regenerar os documentos 03/04 e rodar a suíte completa depois da última mudança de código ou base.
- [ ] Preparar `.zip` sem caches, ambiente virtual, dados pessoais de teste ou dependências instaladas.
- [ ] Conferir contatos, abrir os arquivos em outra máquina, enviar e confirmar recebimento.

Os três últimos marcos são da entrega final. Este checkpoint não envia mensagens à organização nem publica um pacote final.

## Resumo do que falta resolver

A documentação técnica do núcleo já pode acompanhar uma demonstração local por terminal.
A base clínica continua como suposição, e API, web, licença e validação exigem trabalho ou confirmação.
A equipe precisa completar seus dados, ensaiar e produzir os arquivos finais antes do envio de 22/10.
