# HackAtom — anamnese explicável de bovinos leiteiros

Prova de conceito do tema T1 do Hackathon UFJF 2026. O núcleo executa regras explícitas, combina fatores de certeza pelo modelo MYCIN e explica as conclusões. A IA auxilia o desenvolvimento; a decisão em execução sai da base e do motor.

**Estado em 21/10/2026, após a integração em `sessao-pair-programming`:** motor local, base de desenvolvimento, módulo `kb/` e API FastAPI com persistência SQLite disponíveis. A interface web e o editor gráfico continuam pendentes. Todo conhecimento veterinário e todo CF permanecem como suposição a validar. O resultado não constitui diagnóstico nem recomendação terapêutica.

## Executar a demonstração do motor

Requer Python 3.12 ou superior. Abra um terminal na raiz deste repositório. O motor e os utilitários desta entrega usam somente a biblioteca padrão, sem instalação de pacotes.

```powershell
python -m unittest discover -s tests/engine -t .
python -m engine base/desenvolvimento/anamnese-bovinos-v3.1.0-revisao1.json base/desenvolvimento/casos/alerta-decubito.json
```

O primeiro comando executa os testes do motor e da base de desenvolvimento. O segundo executa um caso sintético, imprime JSON com `status: "passou"` e código de saída 0. Veja o [exemplo mamário e o uso Python](base/desenvolvimento/LEIA-ME.txt).

Para instalar as dependências, executar a API em `localhost:8000` e preparar o banco com dados fictícios, siga o [README da API](api/README.md). O contrato e a validação da base estão no [README de `kb/`](kb/README.md). Após instalar `.[dev]` no ambiente virtual, execute a suíte completa com `.venv\Scripts\python -m pytest`.

## Documentação

- [Índice da entrega parcial e atendimento às exigências](docs/entrega/README.md).
- [Processo de desenvolvimento](docs/entrega/01-processo.md).
- [Arquitetura implementada e integração planejada](docs/entrega/02-arquitetura.md).
- [56 regras de produção geradas da base](docs/entrega/03-regras-de-producao.md).
- [Resultados dos dois casos sintéticos](docs/entrega/04-casos-de-teste.md).
- [Roteiro de apresentação, demonstração e perguntas](docs/entrega/05-apresentacao-e-demo.md).
- [Riscos, pendências e checklist de envio](docs/entrega/06-riscos-e-pendencias.md).
- [Contrato detalhado do motor](engine/README.md).

## Manter as tabelas sincronizadas

```powershell
python scripts/gerar_doc_regras.py --base base/desenvolvimento/anamnese-bovinos-v3.1.0-revisao1.json --casos base/desenvolvimento/casos
python scripts/gerar_doc_regras.py --base base/desenvolvimento/anamnese-bovinos-v3.1.0-revisao1.json --casos base/desenvolvimento/casos --verificar
```

O segundo comando retorna 1 se o conteúdo gerado divergir do arquivo versionado. A suíte também verifica esse sincronismo. A base atual está em desenvolvimento; não há `base/ativa.json` nem ativação clínica aprovada.

## Equipe e licença

Os nomes e as responsabilidades informados pela equipe estão no [índice da entrega](docs/entrega/README.md); os telefones para o envio continuam pendentes. A licença do código do projeto ainda não foi declarada em um arquivo `LICENSE`; essa decisão continua pendente para atender integralmente à exigência de código aberto.
