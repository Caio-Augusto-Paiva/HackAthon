# Revisão técnica — Seção 6: entrega, apresentação e riscos

Data: 22/10/2026. Revisão com Codex, a partir de `docs/prompts/secao-6.md` e do checkout `codex-davi` em `d9eda27`. O prompt e a especificação são documentos aprovados de planejamento e foram preservados; as correções foram aplicadas aos documentos de entrega, que descrevem o estado executável. Não se trata de validação clínica, ensaio humano ou comprovante de envio.

## Fontes e critério

- [Apresentação oficial, transcrição A](../fontes/transcricao-apresentacao-rerum.md), slides 3, 5 e 8–15; [PDF original](../fontes/apresentacaoRerun.pdf). Os slides 10 e 15 também foram conferidos visualmente no PDF.
- [Documentário oficial, transcrição D](../fontes/transcricao-documentario-rerum.md), páginas 2–3; [PDF original](../fontes/DocumentárioRerun.pdf). A página 1 não está transcrita e não fundamenta afirmações desta revisão.
- [Seção 6 do desenho](../superpowers/specs/2026-10-20-anamnese-bovinos-design.md), [prompt revisado](../prompts/secao-6.md), documentos 01–06, diários, código/contrato e histórico Git. Para artefatos já indicados, a consulta foi direta, sem usar o grafo para inferir implementação.
- Conferência local: `v0002`, 51 símbolos, 56 regras, todas `suposicao_a_validar`, 34 casos JSON e 27 operações OpenAPI. `LICENSE` e `uv.lock` estão ausentes no checkout auditado.

Os campos abaixo distinguem erro verificável, lacuna de evidência, decisão externa e ressalva menor. Planos não são refutados só porque ainda não foram executados. Achados históricos sobre MYCIN não foram tratados como novas provas numéricas: permanecem históricos quando sua execução original não foi reproduzida nesta revisão.

## Atendimento às exigências dos organizadores

| Exigência | Evidência disponível | Resultado desta auditoria |
|---|---|---|
| Agente de IA no desenvolvimento — A3/A7 | Processo, commits e diários técnicos | Evidência disponível; atribuição pessoal e aprendizado precisam de complementação humana |
| Sem LLM na decisão; determinismo/auditoria — A8/A13 | Motor local, base explícita, traço e testes de arquitetura | Atendido no alcance testado; ordem de respostas também integra o estado |
| Ferramentas e código aberto — A3/A13, D2 | Código disponível e dependências declaradas | **Aberto:** ausência de licença do projeto e conferência final de atribuições |
| Documentar processo, arquitetura e regras — A10, D2 | Documentos 01/02/03; regras/casos gerados | Texto técnico disponível; relatos pessoais incompletos; formato final interno ainda não produzido |
| Apresentar processo da IA ao resultado — A10/A11 | Roteiro 05, decisões com evidência e limitações | Roteiro preparado; slides e ensaio não comprovados |
| Demonstrar sistema em localhost — A10/A15, D3 | SPA/API/motor locais e E2E com API real | Evidência de software disponível; ensaio físico e reserva pendentes |
| Trabalho em equipe, liderança e entendimento — A5/A11/A12 | Divisão informada e modelo de ensaio | Não é possível certificar desempenho humano por documentação ou teste |
| Envio até 22/10 às 20:00 com nome/telefone — A15 | Dados no índice, checklist e modelo de comprovante | Dados registrados; pacote, envio e recebimento ainda não comprovados |

ZIP, PDFs, vídeo, reserva e alvo de 18:30 são decisões internas, não novos requisitos oficiais. A duração oficial e o limite de anexo não estão informados nas fontes. A equipe confirmou **10 minutos de fala + 4 de demo como estimativas**, sem alterar esse caráter provisório.

## Achados sobre a seção fornecida

### S6-01 — Promessa de editor na apresentação

- **Veredito:** erro no roteiro se usado para representar a entrega atual.
- **Trecho exato (6.2.1, slide 5):** “o editor em grafo valida (ciclos, camadas, inalcançáveis) e só salva nova versão sem erros.”
- **Prova:** há validador e rotas de versões, mas a consulta em `web/` não implementa o editor. A10 pede o sistema produzido em funcionamento; apresentar uma interface inexistente não atende isso.
- **Correção mínima:** “A base JSON é versionada e validada; nesta entrega demonstramos a consulta web, sem editor gráfico.” Aplicada em 05/06; editor não passou a ser bloqueio artificial da entrega.

### S6-02 — Caso do abomaso promete coleta não demonstrada

- **Veredito:** lacuna de evidência.
- **Trecho exato (6.2.2):** “apetite reduzido, queda de produção, costelas saltadas”.
- **Prova:** R15/R16 distinguem o caso com observação prévia de flanco do diálogo que não chega a perguntá-la. Um caso que injeta um fato não prova sua coleta na interface. O roteiro também não deve exigir símbolos ausentes da base ativa.
- **Correção mínima:** demonstrar o caminho mamário já coberto pelo E2E real de troca de modo e mostrar o parecer retornado, sem prometer CF ou pergunta específicos não alcançados. Aplicada em 05; R15/R16 permanecem abertos.

### S6-03 — Contagem histórica de casos

- **Veredito:** erro de atualização.
- **Trecho exato (6.2.1, slide 7):** “30 casos conhecidos rodam contra cada versão da base”.
- **Prova:** `base/casos/casos.json` contém 34 casos, documentados por execução em 04. São casos sintéticos; a contagem não demonstra assertividade clínica prevista em A3.
- **Correção mínima:** “Há 34 casos sintéticos de regressão na base ativa; testar uma versão nova antes de ativar.” Aplicada em 01/02/05, índice e README.

### S6-04 — Bandeira descrita como irreversível mesmo após correção

- **Veredito:** erro de semântica.
- **Trecho exato (6.2.3, pergunta 6):** “a urgência não desce mais”.
- **Prova:** testes do motor cobrem correção, remoção de reconhecimento e reprocessamento de gatilhos por ordem real. Novas respostas não apagam gatilhos históricos válidos; corrigir um fato que os sustenta pode removê-los. A8 exige explicação auditável dessa diferença.
- **Correção mínima:** “A bandeira preserva urgência com novas respostas; correções reprocessam os gatilhos e podem removê-la.” O documento 05 já expressava a distinção; mantida e ligada à continuidade da sessão.

### S6-05 — “Só texto e perguntas” omite limites do modo

- **Veredito:** ressalva menor de precisão.
- **Trecho exato (6.2.3, pergunta 8):** “mudam só o texto e as perguntas oferecidas”.
- **Prova:** o modo também altera o limite dinâmico de 12 para 25; a parada é recalculada e a sessão pode reabrir. `PATCH` preserva os fatos e o parecer continua único; não há segundo motor.
- **Correção mínima:** “Compartilham base, fatos e motor; mudam linguagem, perguntas disponíveis e limite dinâmico, com recálculo no mesmo histórico.” Incorporada em 02/05 e nos limites já documentados.

### S6-06 — Independência de família de modelo não demonstrada

- **Veredito:** lacuna, não prova de que as revisões não aconteceram.
- **Trecho exato (6.2.1, slide 8):** “revisão sempre por outra família de modelo”.
- **Prova:** planejamento de agentes não identifica o modelo real de toda revisão. Contexto separado não comprova outra família. A5/A11 avaliam uso de IA e organização; preencher atribuições fictícias enfraquece essa evidência.
- **Correção mínima:** “Mostrar revisões efetivamente registradas, identificando ferramenta e prova; distinguir revisão em contexto separado de revisão por outra família.” Aplicada em 01 e no log de revisões.

### S6-07 — Diários e prova de entendimento sem autores confirmados

- **Veredito:** lacuna de evidência humana.
- **Trecho exato (6.1.2):** “ao menos 8 a 10 entradas por pessoa”.
- **Prova:** B/C eram modelos de diário, A era registro técnico curado; não demonstravam interações e aprendizado dos três integrantes. A12, passo 8, pede estudo; A5/A11 pedem capacidades humanas, não uma quantidade de linhas.
- **Correção mínima:** manter os registros técnicos com proveniência e pedir a cada pessoa decisões, horários reais que possa comprovar e explicação de uma parte própria/alheia. Modelos atualizados, sem inventar entradas para atingir a meta interna; modelo 07 criado.

### S6-08 — Open source continua sem fechamento

- **Veredito:** lacuna frente a requisito obrigatório.
- **Trecho exato (restrições):** “3. Open source.”
- **Prova:** A3/A13 e D2 exigem ferramentas/códigos abertos; não há `LICENSE` do projeto. Disponibilizar código, por si só, não comprova uma licença declarada nem encerra a revisão dos materiais/dependências.
- **Correção mínima:** “A equipe deve escolher e registrar a licença do projeto e conferir as licenças/atribuições do pacote antes de declarar o requisito atendido.” R07 e checklist preservados como abertos; licença não escolhida em nome do grupo.

### S6-09 — Lockfile prometido não existe

- **Veredito:** erro na descrição do pacote atual.
- **Trecho exato (6.1.4):** “com `uv.lock` e `package-lock.json`”.
- **Prova:** existe `web/package-lock.json`; `uv.lock` está ausente. `pyproject.toml` não trava todas as dependências transitivas e deixa faixas de desenvolvimento. Não há base para prometer `uv sync --frozen --offline` a partir desse checkout.
- **Correção mínima:** documentar a instalação atual e registrar decisão/teste de reprodutibilidade Python como pendente antes do pacote final. R22 criado; não gerar lockfile sem testar instalação.

### S6-10 — Ensaio e vídeo tratados como se já existissem

- **Veredito:** lacuna de execução, embora o plano marque suposições.
- **Trecho exato (6.2.2):** “vídeo gravado da demonstração” e “gravado na quinta 16–18 durante o ensaio 1”.
- **Prova:** o checkout auditado contém roteiro, capturas e testes; não comprova essa gravação nem ensaio físico nas duas máquinas. E2E sem chamadas externas e bloqueio de rede em processos Python têm alcance distinto de Wi-Fi desligado num ensaio humano.
- **Correção mínima:** “Produzir e conferir vídeo e reserva, registrando data, versão e resultado; até lá, são pendências.” Aplicada em 05/06 e modelo 07; R10/R20/R23 continuam explícitos.

### S6-11 — Limites de tempo e envio dependem da organização

- **Veredito:** decisão em aberto, não erro numérico.
- **Trecho exato (6.2.1):** “14:00 (suposição; ajustar quando a organização informar a duração)”.
- **Prova:** a soma da fala original é 600 s; demo prevista de 240 s resulta em 840 s, antes de perguntas/montagem. O roteiro vigente também soma 600 + 240 s. A15 dá data/horário da apresentação, não duração, tamanho de anexo ou obrigação de usar dois canais.
- **Correção mínima:** manter 10 + 4 como estimativas e cronometrar; confirmar duração, infraestrutura e anexos. ZIP/PDF e e-mail com aviso adicional continuam escolhas internas. Perguntas necessárias: “Qual o tempo total com perguntas? Qual canal/formato e tamanho de anexo serão aceitos?”

### S6-12 — Fontes clínicas e CF continuam provisórios

- **Veredito:** lacuna de validação reconhecida pelo plano.
- **Trecho exato (6.3.2):** “ler integralmente antes de citar na documentação”.
- **Prova:** 56/56 regras permanecem `suposicao_a_validar`. Fontes contextuais e testes sintéticos não calibram CF nem comprovam revisão por veterinário. Esta auditoria documental não supre a leitura clínica ou a calibração pendentes.
- **Correção mínima:** preservar o aviso e registrar fonte/trecho e revisor de cada validação futura. Não atribuir CF estimado a uma publicação como se fosse um valor extraído dela. Pergunta necessária: “Quem revisou quais regras, com quais critérios e evidências?” R01/R02 permanecem abertos.

## Problemas adicionais encontrados no material atual

### AD-01 — Documentos de processo negavam a integração existente

- **Veredito:** erro de atualização, fora da lista histórica de achados de IA da seção.
- **Trechos exatos antes da correção:** 01: “A ausência de API e web neste checkpoint”; B: “A implementação desses componentes não está presente”; C: “Não há implementação web ou execução E2E registrada”.
- **Prova:** código/contratos presentes e commits de integração/troca de modo. A10 exige documentar o processo real, não apenas o estágio inicial.
- **Correção mínima:** preservar a data do checkpoint e acrescentar o estado integrado de 22/10, sem atribuir commits a pessoas por inferência. Aplicada em 01 e nos três diários.

### AD-02 — Contatos presentes, pendência falsa e grafia divergente

- **Veredito:** erro editorial.
- **Trechos exatos antes da correção:** README raiz: “os telefones para o envio continuam pendentes”; índice: “Davi Monção Fernades”.
- **Prova:** os três telefones já constavam do índice. O usuário confirmou nesta revisão a opção “Davi Monção Fernandes”. A15 exige identificação correta de todos no envio.
- **Correção mínima:** corrigir grafia, manter contatos fornecidos e trocar “coletar” por “conferir e incluir no envio”. Aplicada em índice/README/06, sem repetir telefones neste relatório.

### AD-03 — Contagens e mapa do pacote desatualizados

- **Veredito:** erro editorial.
- **Trechos exatos antes da correção:** README raiz: “Resultados dos dois casos sintéticos”; 02: “39 testes Vitest” e “8 cenários Playwright”.
- **Prova:** 04 contém 34 casos; o checkpoint `09f5754` ampliou a interface para 60 testes e 11 E2E. São categorias distintas e datadas; os unittest do motor também são coletados pelo pytest.
- **Correção mínima:** apontar para os 34 casos e registrar 60/11 como checkpoint, preservando 39/8 como histórico no relatório web. Aplicada no README, índice, 01/02/05/06.

### AD-04 — Matriz de pessoas difere da divisão A/B/C original

- **Veredito:** lacuna de atribuição.
- **Trecho exato (prompt, siglas):** “A = motor/base”, enquanto o índice informado põe motor/documentação na linha B e base/banco na C.
- **Prova:** as letras do planejamento não comprovam autoria real dos registros pessoais nem concordância de cada pessoa com o papel de apresentação proposto.
- **Correção mínima:** usar nomes/responsabilidades fornecidos no índice e tratar letras de diários, riscos e fala como referências históricas ou propostas até confirmação no ensaio. Aplicada em 01/05/06/índice/diários, sem redistribuir responsabilidades em nome do grupo.

### AD-05 — Vídeo não resolve falha de todo meio de exibição

- **Veredito:** ressalva menor de contingência.
- **Trecho exato (6.2.2):** “O vídeo cobre falha de projetor ou de máquina”.
- **Prova:** vídeo ainda precisa de tela/projetor funcional; o próprio plano depende de infraestrutura desconhecida. Uma máquina reserva mitiga falha da principal, mas não prova a disponibilidade de exibição para a banca.
- **Correção mínima:** “Vídeo e capturas ajudam se houver exibição disponível; combinar alternativa de tela com a organização e oferecer localhost.” Registrada no modelo 07.

## Correções aplicadas e limites desta entrega

Atualizados: processo, arquitetura, roteiro, riscos/checklist, índice, README e diários técnicos; acrescentado o modelo 07 e este relatório. Nenhum arquivo de `engine/`, `api/`, `kb/`, `base/`, `contratos/`, `web/` ou teste foi modificado nesta revisão. Documentos 03/04 continuam gerados, sem edição manual. O grafo/Obsidian é atualizado uma única vez ao fechar o bloco documental, com commit separado.

Não foram produzidos slides/PDFs/ZIP, escolhido licenciamento, enviados contatos a terceiros, realizados ensaios humanos ou validado conhecimento clínico: o arquivo solicitado é um prompt de revisão e explicitamente delimita “só estrutura, roteiros e tabelas”. As pendências materiais permanecem abertas, com critérios de conferência no modelo 07. A aprovação desta revisão não significa que o pacote final está pronto para envio.

## Verificação executada nesta revisão

| Verificação | Resultado observado |
|---|---|
| `pytest -q tests/documentacao tests/casos` | 20 aprovados e 34 subtestes; baseline antes da edição |
| `scripts/gerar_doc_regras.py --casos base/casos/casos.json --verificar` | Regras e 34 casos sincronizados; 03/04 não foram editados |
| `pytest -q` | 1066 aprovados, 1 ignorado e 170 subtestes aprovados, em 100,08 s |
| Dois comandos CLI do roteiro 05 | `alerta-decubito` e `sinais-mamarios`: `status: passou`, saída 0 |
| Trecho Python do roteiro 05 | Executado; snapshot restaurado com estado equivalente (`True`) |
| Links locais de README, entrega, processo e deste relatório | Nenhum destino inexistente na conferência automática |
| Durações extraídas das tabelas vigentes | Fala 600 s, demo 240 s com intervalos contíguos, reserva curta 300 s |
| Escopo de arquivos e `git diff --check` | Sem alteração do runtime, contratos, base, testes ou tabelas geradas; sem erros de espaços |

60 Vitest e 11 E2E são evidências do checkpoint `09f5754`, não execuções novas desta revisão documental. A suíte Python foi repetida; nenhum resultado de teste foi usado para preencher campos de ensaio humano. A conferência de links verifica existência de destinos locais, não a disponibilidade de sites externos ou a navegação de todos os fragmentos Markdown.

## Resumo — exatamente três linhas

O roteiro foi alinhado à consulta real, aos 34 casos e à troca de modo com histórico e parecer únicos.
Fala de 10 minutos e demo de 4 são estimativas; licença, validação clínica, ensaio humano e arquivos finais continuam pendentes.
Equipe e evidências foram atualizadas sem inventar autoria, aprendizado, recebimento ou conclusão de itens planejados.
