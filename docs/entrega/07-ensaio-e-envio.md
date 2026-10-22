# Registro de ensaio e conferência do envio

**Modelo não preenchido.** A existência deste arquivo não comprova ensaio, produção de PDFs, envio ou recebimento. Preencher com acontecimentos reais, sem reconstruir horários nem inventar decisões. Usar somente animais fictícios na demonstração.

## Referências e decisões

- Fonte oficial: [A, slides 10 e 15](../fontes/transcricao-apresentacao-rerum.md). Materiais: documentação, apresentação e código-fonte; solução demonstrada em localhost; nomes e telefones no envio.
- Prazo oficial: **22/10/2026 às 20:00**; apresentação em **23/10 às 09:00**. Alvo interno de envio: **18:30**.
- Estimativa escolhida pela equipe: **10 minutos de fala + 4 de demo**, sem perguntas. Tempo oficial, infraestrutura e limite de anexo: a confirmar com a organização.
- Três vozes, diários pessoais, ZIP + PDFs e reserva são decisões internas. A equipe deve confirmar a distribuição das falas; não se infere autoria por A/B/C ou por branch.
- Conteúdo da fala e passos executáveis: [roteiro 05](05-apresentacao-e-demo.md). Pendências com critérios de encerramento: [registro 06](06-riscos-e-pendencias.md).

## Antes do ensaio

- [ ] Confirmar que os três integrantes são alunos inscritos e estarão presentes na apresentação, conforme [A], slide 3; conferência humana pendente.
- [ ] Nomear operador e apresentadores, conferindo os [dados da equipe](README.md).
- [ ] Registrar commit, base ativa e versões das ferramentas nos dois computadores.
- [ ] Instalar dependências e compilar a SPA com internet antes de testar sem rede; não copiar `.venv` ou `node_modules` de outro computador.
- [ ] Usar banco SQLite fictício fora do OneDrive; preservar o banco existente, sem `-Reset` em banco que precise ser mantido.
- [ ] Fechar outro servidor na porta 8000 antes de iniciar o próprio, sem interromper processos de terceiros.
- [ ] Abrir `http://localhost:8000/` e conferir a mesma consulta na máquina principal e na reserva.
- [ ] Ensaiar a SPA sem internet depois do preparo. Não usar Swagger como requisito da demo offline, pois depende de CDN.
- [ ] Preparar capturas locais e, se produzido, vídeo da versão ensaiada; identificar gravação como gravação.

## Registro por computador

Duplicar a tabela para a máquina reserva. Não marcar “aprovado” com base apenas nos testes automatizados de outra máquina.

| Campo | Registro real |
|---|---|
| Máquina e operador | A preencher |
| Data, início e fim | A preencher |
| Commit / base ativa | A preencher |
| Sistema, Python, Node e navegador | A preencher |
| Banco fictício usado, fora de pasta sincronizada | A preencher |
| Instalação e build preparados | A preencher |
| Estado da rede no ensaio | A preencher |
| Dias inválidos, erro no campo e correção | A preencher |
| Produtor → especialista, resposta técnica e histórico mantido | A preencher |
| Voltar, corrigir resposta anterior e consultar o mesmo parecer | A preencher |
| Bandeira, pausa e explicação do raciocínio | A preencher |
| Erro observado / correção / nova tentativa | A preencher |
| Resultado e responsável pela conferência | A preencher |

## Cronometragem e entendimento

| Bloco | Estimativa | Tempo observado | Ajuste necessário |
|---|---:|---|---|
| Fala, incluindo transições entre três vozes | 10:00 | A medir | A preencher |
| Demo, incluindo cliques e respostas | 4:00 | A medir | A preencher |
| Perguntas da banca | Não informado | A medir no treino | Confirmar duração oficial |

Se a demo passar de quatro minutos, retirar a segunda consulta conforme o roteiro 05, mantendo a explicação da primeira. Capturas e vídeo são apoio; não substituem a demonstração em localhost. Vídeo depende de um meio de exibição funcional: falha de projetor exige alternativa de exibição combinada com a organização.

| Integrante | Parte própria explicada | Parte alheia explicada | Regra, teste ou commit mostrado | Dúvida e correção |
|---|---|---|---|---|
| Caio Augusto de Paiva Teixeira | A preencher | A preencher | A preencher | A preencher |
| Davi Monção Fernandes | A preencher | A preencher | A preencher | A preencher |
| Luis Henrique Poubel Buettel | A preencher | A preencher | A preencher | A preencher |

Explicar pelo menos um achado aceito ou ajustado e um rejeitado com evidência, sem atribuir a alguém um agente que não usou. Registrar por que CF não é probabilidade e por que software testado não é conhecimento clinicamente validado. Esse exercício operacionaliza o passo 8 de [A], slide 12; a quantidade sugerida de exemplos é interna.

## Conferência do pacote

- [ ] Licença escolhida pela equipe, arquivo correspondente e licenças/atribuições dos materiais e dependências conferidos; até lá, open source continua pendente.
- [ ] Documentos 01/02/03 presentes e revisados; 03/04 sincronizados pelo gerador, sem edição manual das tabelas.
- [ ] PDFs dos documentos produzidos e abertos; verificar páginas, tabelas, links e legibilidade.
- [ ] Slides em PDF e formato editável produzidos e abertos, incluindo tema/equipe, sumário, processo com IA, resultado, limitações e perguntas.
- [ ] Código, testes, casos sintéticos, `pyproject.toml`, `web/package-lock.json`, fontes e instruções de instalação incluídos.
- [ ] Ausência de `uv.lock` resolvida por decisão e instalação testada, ou limitação explicitada; não anunciar um arquivo inexistente no pacote.
- [ ] ZIP sem `.git`, caches, ambientes instalados, bancos SQLite de sessão e segredos; manter os contatos da equipe exigidos para o envio.
- [ ] Extrair o pacote em outra pasta/máquina e verificar os comandos documentados; registrar o resultado real.
- [ ] Medir o tamanho do anexo e confirmar canal/formato aceitos; ZIP e PDFs são formato interno, não uma extensão exigida por [A].
- [ ] Conferir nomes e telefones dos três na mensagem e nos materiais pertinentes.

## Comprovante de envio — preenchimento humano

| Campo | Registro real |
|---|---|
| Quem enviou / quem conferiu | A preencher |
| Data e horário | A preencher |
| Canal e destinatário conferidos no slide 15 original | A preencher |
| Commit, base ativa e identificação do pacote | A preencher |
| Arquivos enviados / tamanho | A preencher |
| Comprovante de envio | A preencher |
| Confirmação de recebimento | A preencher |
| Pendência e ação corretiva | A preencher |

Não enviar automaticamente a partir deste modelo. Conferir o destinatário no PDF oficial; o arquivo de transcrição omite o contato de suporte. Um comprovante de envio não equivale a confirmação de recebimento.
