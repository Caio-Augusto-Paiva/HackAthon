"""Monta o grafo 2 (dados das doenças) com o graphify, sem IA.

Uso (com o Python onde o graphify está instalado; ver ``graphify-out/.graphify_python``):

    <python do graphify> scripts/grafo_dados.py graphify-out-dados "obsidian/02-Dados de Treino"

Lê ``<saida>/extracao.json`` (gerado por ``python -m kb.exportar_grafo``), monta o grafo
dirigido e grava ``graph.json``, ``GRAPH_REPORT.md`` e ``graph.html`` em ``<saida>`` e as
notas do cofre em ``<cofre>``. As comunidades não vêm do agrupamento automático: cada
arquivo de ``base/fonte/`` é uma comunidade (uma por doença e a “Comum”), o que deixa o
resultado idêntico a cada geração.
"""
from __future__ import annotations

import json
import sys
from pathlib import Path

from graphify.analyze import god_nodes, surprising_connections
from graphify.build import build_from_json
from graphify.cluster import score_all
from graphify.export import to_html, to_json, to_obsidian
from graphify.report import generate


def comunidades_por_arquivo(extracao: dict) -> tuple[dict[int, list[str]], dict[int, str]]:
    """Uma comunidade por arquivo de origem; rótulo = nome da doença ou “Comum”."""
    nomes = {n["id"].removeprefix("sim:"): n["label"] for n in extracao["nodes"] if n.get("tipo") == "doenca"}
    grupos: dict[str, list[str]] = {}
    for no in extracao["nodes"]:
        grupos.setdefault(no["source_file"], []).append(no["id"])
    comunidades, rotulos = {}, {}
    for i, arquivo in enumerate(sorted(grupos, key=lambda a: (not a.endswith("comum.json"), a))):
        comunidades[i] = grupos[arquivo]
        doenca = Path(arquivo).stem
        rotulos[i] = nomes.get(doenca, "Comum: bandeiras, triagem e sinais compartilhados")
    return comunidades, rotulos


def main(saida: str, cofre: str) -> int:
    pasta = Path(saida)
    extracao = json.loads((pasta / "extracao.json").read_text(encoding="utf-8"))
    G = build_from_json(extracao, directed=True, dedup=False)
    comunidades, rotulos = comunidades_por_arquivo(extracao)
    coesao = score_all(G, comunidades)

    if not to_json(G, comunidades, str(pasta / "graph.json"), force=True, community_labels=rotulos):
        print("Erro: o graphify recusou gravar graph.json.", file=sys.stderr)
        return 1
    deteccao = {"total_files": len(comunidades), "total_words": 0, "files": {"document": sorted({n["source_file"] for n in extracao["nodes"]})}}
    relatorio = generate(G, comunidades, coesao, rotulos, god_nodes(G), surprising_connections(G, comunidades),
                         deteccao, {"input": 0, "output": 0}, "base/fonte", suggested_questions=[])
    (pasta / "GRAPH_REPORT.md").write_text(relatorio, encoding="utf-8", newline="\n")
    to_html(G, comunidades, str(pasta / "graph.html"), community_labels=rotulos)
    # O cofre lista as ligações de cada nota pelos vizinhos; no grafo dirigido, uma doença
    # mostraria só as regras que ela dispara, e não as que a concluem.
    notas = to_obsidian(G.to_undirected(), comunidades, cofre, community_labels=rotulos, cohesion=coesao)
    print(f"Grafo 2: {G.number_of_nodes()} nós, {G.number_of_edges()} arestas, {len(comunidades)} comunidades; "
          f"{notas} notas em {cofre}.")
    return 0


if __name__ == "__main__":
    if len(sys.argv) != 3:
        print(__doc__)
        raise SystemExit(2)
    raise SystemExit(main(sys.argv[1], sys.argv[2]))
