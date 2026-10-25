# Grafo 2 — Dados das 20 doenças

Este cofre do Obsidian mostra a base de conhecimento do sistema separada por doença: cada doença (20 na v0006), as regras que a concluem e os sinais que essas regras usam. Os 2 pares excludentes da base (`deslocamento_abomaso_esquerda` × `deslocamento_abomaso_direita`, `timpanismo_espumoso` × `timpanismo_gasoso` e `retencao_placenta` × `metrite`) aparecem como ligações `exclui` entre as doenças. Os links de tratamento ficam na base (`tratamento` de cada doença), não neste grafo.

O grafo é **exato**: é gerado pelo conversor `kb/grafo.py` a partir dos arquivos em `base/fonte/`, sem inteligência artificial. Todas as ligações são EXTRACTED e o resultado é o mesmo a cada geração.

## Como regenerar

1. `.venv/Scripts/python -m kb.exportar_grafo` — lê `base/fonte/` e grava `graphify-out-dados/grafo_exato.json` e `graphify-out-dados/extracao.json`.
2. `<python do graphify> scripts/grafo_dados.py graphify-out-dados "obsidian/02-Dados de Treino"` — monta comunidades, relatório, HTML e as notas deste cofre (o caminho do Python do graphify está em `graphify-out/.graphify_python`).

## O motor pode ler este grafo?

Pode, pelo grafo exato: `kb.exportar_grafo.carregar_do_grafo("graphify-out-dados/grafo_exato.json")` devolve a mesma base, e os 60 casos clínicos dão o mesmo resultado. O motor **não** lê o `graph.json` de uma execução normal do graphify, porque aquele vem de extração por IA e pode variar — isso quebraria a decisão determinística e auditável.

“Dados de Treino” é só o nome da pasta: o sistema não usa aprendizado de máquina.
