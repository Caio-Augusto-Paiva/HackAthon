# Riscos, lacunas e fechamento da entrega

Estado integrado das Seções 5 e 6, branch `codex-davi`, auditado até `d9eda27`. `f46cd6e` identifica o checkpoint histórico da Seção 5. A/B/C na coluna Papel são responsáveis propostos no planejamento original, não atribuições pessoais confirmadas; distribuir as ações conforme as responsabilidades reais do índice antes do ensaio. Gravidade indica impacto para a entrega ou uso pretendido, não classificação clínica de um animal.

## Registro de riscos

| ID | Risco ou lacuna | Gravidade | Evidência atual | Mitigação e condição de encerramento | Papel |
|---|---|---|---|---|---|
| R01 | Conhecimento clínico e CF sem validação especializada | Alta | 61 regras (v0003) como `suposicao_a_validar`; zero `validada`. As 5 regras de sinal isolado da v0003 (R-HIP-05/06, R-CET-06, R-DAB-04, R-ACI-05) são suposições novas, de peso baixo, sem validação clínica | Revisar com veterinário/RERUM; documentar quem revisou, escopo e critérios. Até lá, limitar a desenvolvimento/demonstração | A |
| R02 | Confiança excessiva por sinais correlacionados | Alta | Cetose pode chegar a CF 0,83086641 sem exame; claudicação/dor podem somar 0,65 para dermatite | Calibrar com casos representativos; não converter CF em probabilidade. Agrupamento leite/caneca já reduz um caso de duplicação | A |
| R03 | Falso entendimento de `sem_problema` | Alta | Fallback por ausência de gatilhos, inclusive dados incompletos | Explicar o alcance no parecer/apresentação; revisar mensagem e política com especialista antes de uso clínico | A/C |
| R04 | Prometer editor gráfico fora do escopo entregue | Média | Consulta React e 11 E2E no checkpoint da troca de modo; editor não faz parte desta implementação | Demonstrar a consulta web; retirar edição visual do roteiro principal. Editor não é exigência explícita dos organizadores | B/C |
| R05 | Regressão na restauração da sessão | Alta | API persiste snapshots e tem testes de troca de modo/correção; ordem e origens continuam essenciais | Manter a cobertura e repetir os fluxos após integrações do frontend | B |
| R06 | Divergência entre v0001 e especificação clínica | Alta | 61 regras ainda não validadas (as 5 da v0003 são suposições novas, de peso baixo); sinais e estimativas da Seção 5 divergem (R15/R16) | Conciliar com especialista; alterações via nova versão e casos, nunca sobrescrever `v0001`. Ativação operacional não é aprovação clínica | A/B |
| R07 | Código entregue sem licença declarada | Alta | Arquivo `LICENSE` ausente | Equipe escolher e registrar licença; revisar materiais e dependências do pacote final antes de declarar requisito integralmente cumprido | Todos |
| R08 | Documentação manual divergir da implementação | Média | Processo/arquitetura precisam de revisão após novas integrações | Regras/casos já têm geração e teste de sincronismo; repetir testes e curadoria no fechamento | A/B |
| R09 | Contagem de testes ser confundida com validação clínica | Alta | Estado atual: 1080 testes Python, 170 subtestes, 71 Vitest, 34 casos sintéticos (E2E não rodados). Histórico, baseline integrado: 1066 testes Python aprovados, 1 ignorado, 170 subtestes; 34 casos sintéticos; frontend verificado separadamente | Não somar as 132 execuções unittest (também coletadas por pytest); nenhum teste de software constitui validação clínica | Todos |
| R10 | Falha da máquina ou dependência externa na demo | Alta | SPA com recursos locais e E2E sem chamadas externas; ensaio HTTP histórico separado; Swagger depende de CDN | Ensaiar SPA na principal e na reserva, sem Wi-Fi; manter CLI como contingência. Esse preparo é decisão da equipe, não exigência adicional dos organizadores | B/C |
| R11 | Tempo da fala e infraestrutura desconhecidos | Média | Materiais oficiais não informam duração nem infraestrutura | Confirmar com organização; ensaiar roteiros de 14 e 5 minutos, sem assumir projetor/rede | C |
| R12 | Equipe não dominar o que foi gerado com IA | Alta | Diários B/C e prova de entendimento ainda incompletos | Cada integrante explicar parte própria e alheia; registrar ensaio e corrigir dúvidas | Todos |
| R13 | Envio incompleto ou fora do prazo | Alta | Contatos informados no índice; PDFs, slides editáveis e pacote final pendentes | Conferir dados e checklist; alvo interno 22/10 às 18:30, prazo oficial às 20:00; confirmar recebimento pelo canal escolhido | C |
| R14 | Conflitos com trabalho paralelo | Média | Frontend implementado no checkout isolado, com pushes em `codex-davi`; merge preservou a Seção 5 e trouxe a v0002 | Motor, API, kb, versões imutáveis e contratos preservados; alinhar futuras integrações sem reescrever versões | Todos |

As probabilidades de ocorrência não foram medidas; não atribuímos percentuais artificiais aos riscos. A prioridade deve ser revista pela equipe conforme fechamento da entrega e disponibilidade de especialista. O requisito open source continua aberto enquanto a licença do projeto não for decidida e registrada; código acessível não encerra R07.

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
| “editor salvando versão e rodando casos” na demo | Editor pendente | Rotas de versões e casos disponíveis; consulta web implementada sem editor | Demonstrar a consulta no navegador; não alegar conclusão do editor |
| `03-regras` gerado da base ativa | Implementado | Ponteiro `v0003` presente e válido | Gerador sem `--base` segue o ponteiro; documentos 03/04 e teste de sincronismo usam a ativa |
| “sem código nesta fase” no rascunho histórico | Desatualizado para a solicitação atual | Motor, testes e integração já implementados | Descrever o código existente e criar somente o utilitário necessário à documentação |
| Equipe e telefones no pacote | Situação atualizada na Seção 6 | Contatos já informados no índice; grafia de Davi Monção Fernandes confirmada nesta revisão | Conferir dados e incluí-los no envio; não manter a falsa pendência de coleta |
| Fontes e CF apresentados como conhecimento validado | Risco de extrapolação | Todas as regras continuam como suposição | Separar fonte contextual, comportamento de software e validação clínica |
| OpenAPI, SQLite e `rodar.ps1` tratados como futuros | Texto desatualizado | 27 operações no contrato, SQLite, scripts e SPA presentes | Documentos 02/05/06 descrevem consulta web integrada; editor pendente |

## Checklist de fechamento

- [x] Documentar processo, arquitetura e regras do escopo implementado.
- [x] Gerar regras e casos a partir de arquivos executáveis, com teste de sincronismo.
- [x] Preparar comandos de demonstração e perguntas prováveis da banca.
- [x] Explicitar o caráter sintético dos exemplos e a validação clínica pendente.
- [x] Registrar nomes, responsabilidades e telefones fornecidos; corrigir a grafia confirmada de Davi Monção Fernandes.
- [ ] Conferir com os três integrantes os dados já registrados e incluí-los na mensagem de envio.
- [ ] Confirmar inscrição dos três alunos e presença na apresentação, conforme [A], slide 3.
- [ ] Completar diários pessoais, revisões realmente realizadas e prova de entendimento.
- [ ] Registrar licença do projeto e revisar as licenças do material empacotado.
- [x] Integrar base ativa, `kb/`, API, persistência e casos conhecidos deste recorte.
- [x] Integrar a consulta web e executar E2E com API real e base v0002 (a ativa na época; hoje `v0003`).
- [x] Definir o recorte da apresentação como consulta web integrada; manter editor gráfico fora da promessa atual.
- [ ] Conciliar a base com a especificação e obter revisão especializada, se viável; registrar as limitações remanescentes.
- [ ] Confirmar duração da fala, infraestrutura e limite/formato de anexos com a organização.
- [ ] Produzir e conferir PDFs dos documentos, slides em PDF e formato editável, conforme formato interno escolhido; os organizadores exigem os materiais, mas não especificam essas extensões.
- [ ] Ensaiar na máquina principal e na reserva, com rede desligada; preparar captura/vídeo.
- [ ] Regenerar os documentos 03/04 e rodar a suíte completa depois da última mudança de código ou base.
- [ ] Preparar `.zip` sem `.git`, caches, `.venv`, `node_modules`, bancos SQLite de sessão ou dados de teste; conservar código, casos sintéticos, lockfile npm, documentação e os contatos de entrega exigidos.
- [ ] Conferir contatos, abrir os arquivos em outra máquina, enviar e confirmar recebimento.

O [modelo de ensaio e envio](07-ensaio-e-envio.md) torna esses marcos registráveis, sem marcá-los como executados. Esta revisão não envia mensagens à organização nem publica um pacote final.

## Resumo do que falta resolver

A documentação técnica acompanha motor, base ativa, API, SQLite, consulta React e troca de modo.
Licença, política de coleta R15/R16 e validação clínica permanecem abertas; editor não integra a promessa atual.
A equipe precisa conferir os dados fornecidos, completar relatos pessoais, ensaiar e produzir os arquivos finais antes do envio.

## Integração da interface — 22/10/2026

React 19, TypeScript e Vite 8 estão conectados à API e ao motor. A SPA usa o protótipo do Figma, fontes empacotadas e SVGs originais. O ensaio `rodar.ps1 -SemNavegador` serviu a SPA, uma rota interna e `/api/docs` com HTTP 200. O checkpoint inicial tinha oito cenários Chromium; a troca de modo ampliou para **11 E2E e 60 testes Vitest**. Usam SQLite temporário e a base ativa (`v0002` no checkpoint; hoje `v0003`): produtor completo, bandeira, especialista, número inválido, seis telas em quatro larguras e continuidade/correção após troca. A análise axe nas telas exercitadas não encontrou violações das regras WCAG A/AA selecionadas; isso não certifica acessibilidade nem substitui leitor de tela e dispositivo físico. Detalhes e capturas estão em [QUALIDADE.md](../../web/QUALIDADE.md) e [capturas/](capturas/).

- **R18 — Precisão não exposta na pergunta (baixa; B):** `Campo`/`PerguntaDinamica` no OpenAPI expõem mínimo, máximo e unidade, mas não `casas_decimais`. A interface não deduz regras por nomes clínicos: envia o texto bruto e exibe o 422 do backend. Pedido futuro à API: expor precisão na próxima pergunta para orientar melhor o teclado e a ajuda. Não bloqueia a validação atual.
- **R19 — Histórico de correção desta navegação (baixa; B/C):** Voltar permite editar respostas enviadas durante a navegação atual por PUT. Recarregar retoma o estado persistido, mas não repovoa esse histórico de edição. Uma lista completa de respostas anteriores requer contrato próprio ou produto definido; nenhum endpoint foi inventado.
- **R20 — Cobertura de dispositivos (média; C):** houve Chromium e viewports emulados de 375/768/1024/1440 px, com análise automática, foco e revisão de capturas. Faltam Safari, Firefox, leitor de tela e dispositivos físicos, além do ensaio humano na máquina reserva com Wi-Fi desligado.
- **R21 — Continuidade após parada automática (média; B):** o Review Focus 5 do plano prevê voltar às perguntas após encerrar. Depois de escolher Ver parecer no alerta, a interface oferece Continuar respondendo e chama a ação `continuar`, suportada pela API para esse encerramento manual (`final: true`, `motivo_parada: null`). Quando o motor já encerrou por confirmação, limite, falta de perguntas ou potencial, a mesma ação não remove a regra de parada; sem bandeira histórica, ela é recusada com 422. Pedido à API: definir capacidade explícita e semântica de retomada após parada automática, caso esse comportamento seja desejado. Até lá, a interface não promete reabrir esse caso; oferece Nova verificação e registra o desvio do plano, sem alterar o motor/contrato.
- **Rede:** os E2E das seis telas verificam ausência de requisições externas. Isso se refere à SPA já compilada; instalação npm/Playwright exige internet. R17 continua válido para Swagger, cuja implementação foi preservada.
- **Escopo:** nenhuma regra clínica, versão imutável, contrato ou arquivo de API/motor/kb foi alterado para adaptar o frontend. A exceção autorizada de alinhamento em desenvolvimento e regeneração de documentos foi feita antes da UI. Os riscos clínicos R01–R03/R15/R16 permanecem.

## Fechamento da Seção 6 — 22/10/2026

- **R22 — Reprodutibilidade Python sem lockfile (média; B):** a Seção 6 prevê `uv.lock`, mas ele não existe no checkout auditado. `pyproject.toml` fixa dependências diretas de runtime e deixa faixas em desenvolvimento; isso não equivale a travar todas as transitivas. Decidir e testar o mecanismo de instalação reproduzível em uma máquina limpa antes de prometer `uv sync --frozen --offline`. Esta revisão não cria um lockfile sem validar a instalação.
- **R23 — Material editorial tratado como entrega concluída (alta; todos):** os roteiros e o modelo de conferência estão escritos, mas não há PDFs/slides finais, ZIP ou comprovante de envio no checkout. Não marcar esses itens como entregues apenas por existir Markdown. Arquivos visuais e pacote devem ser produzidos, abertos e conferidos separadamente.
- **R24 — Elegibilidade e presença sem confirmação (alta; todos):** [A], slide 3, exige grupo de até três participantes, alunos inscritos e presentes na apresentação. Há três nomes informados, mas inscrição e presença não podem ser verificadas no código. Cada integrante deve confirmar essas condições com a equipe/organização antes da apresentação; não se presume conformidade nem irregularidade.
- **Estimativas de tempo:** a equipe confirmou 10 minutos de fala + 4 de demo, sem alegar duração oficial. As tabelas somam 600 + 240 segundos; cliques, transições e respostas ainda precisam de cronometragem humana. Cortar a segunda consulta antes de sacrificar a explicação do raciocínio.
- **Dependências externas:** perguntar à organização a duração oficial, infraestrutura e limite/formato de anexos; perguntar aos integrantes qual licença autorizam e quem encerra cada ação. Não é necessário aguardar essas respostas para corrigir os documentos existentes.
- **Perguntas de encerramento:** quem revisou clinicamente a base e com qual escopo? Quem assumirá cada ação pendente? Os três conseguem explicar uma parte própria e uma alheia? A máquina reserva abriu os arquivos e executou a mesma consulta sem rede? Registrar resposta e evidência no modelo 07.
- **Revisão formal:** achados, trechos, provas e correções estão em [2026-10-22-revisao-secao-6.md](../revisoes/2026-10-22-revisao-secao-6.md). A documentação de conhecimento será atualizada no grafo em um único bloco após o fechamento desta revisão.
