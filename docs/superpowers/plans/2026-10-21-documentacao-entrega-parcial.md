# Plano de execução — documentação da entrega parcial

> Execução nesta sessão, conforme pedido para adiantar a documentação disponível. Aplicar `verification-before-completion`; usar TDD no gerador. O texto acompanha a evidência do checkout, sem assumir que API, interface ou validação clínica já existem.

**Objetivo:** produzir a documentação legível pela banca para o núcleo e a base de desenvolvimento existentes.

**Arquitetura:** documentos manuais descrevem processo, arquitetura, demonstração e pendências; regras e casos são gerados dos arquivos executáveis. A atualização do grafo e do Obsidian acompanha os novos documentos.

**Tecnologia:** Markdown e Python 3.12+, somente biblioteca padrão para geração e testes.

**Referência:** Seção 6 de `docs/superpowers/specs/2026-10-20-anamnese-bovinos-design.md`, confrontada com o prompt anexado e as transcrições oficiais em `docs/fontes/`.

## Restrições

- Português; sem inventar integrantes, telefones, revisões externas ou resultados clínicos.
- Preservar o motor, as regras da base e as assinaturas públicas.
- Usar explicitamente a base de desenvolvimento; não criar ponteiro de base ativa.
- Declarar licença ausente, validação clínica e aplicação web como pendências.
- Distinguir testes automatizados, casos sintéticos e validação clínica.

## Arquivos e etapas

1. `scripts/gerar_doc_regras.py` e `tests/documentacao/`: gerar `03-regras-de-producao.md` e `04-casos-de-teste.md`, com modo `--verificar`. Testar antes: limites de CF legíveis, escape de tabelas, base ativa ausente, entrada inválida, execução real dos casos e detecção de documento desatualizado.
2. `README.md`, `docs/entrega/README.md`, `01-processo.md`, `02-arquitetura.md`, `05-apresentacao-e-demo.md` e `06-riscos-e-pendencias.md`: escrever com base em commits, código, fontes oficiais e comandos executados.
3. `docs/processo/A.md`, `B.md`, `C.md` e `revisoes-cruzadas.md`: registrar o histórico verificável do núcleo e deixar os demais diários explicitamente a preencher pelas pessoas responsáveis.
4. Regenerar regras/casos; rodar a suíte inteira e os comandos de demonstração. Conferir links relativos, tempos do roteiro e cobertura das 56 regras.
5. Extrair semanticamente os documentos novos/alterados, atualizar `graphify-out/` e exportar `obsidian/01-conhecimento/`. Preservar o corpus anterior e a proveniência.
6. Conferir o diff, fazer commit e enviar para `origin/codex-davi`.

## Foco da revisão

- Arquivo gerado divergente da base deve ser detectado pelo modo de verificação e pelo teste de sincronismo.
- Fonte sem licença e fonte clínica contextual não devem aparecer como aprovação jurídica ou clínica.
- Valores `cf_minimo`/`cf_maximo` e negações precisam aparecer no texto gerado.
- Ordem de chegada das respostas afeta bandeiras históricas; determinismo da sessão considera essa ordem.
- Duração oficial, dados da equipe, PDFs finais, slides editáveis e envio continuam pendentes até evidência ou informação adicional.
