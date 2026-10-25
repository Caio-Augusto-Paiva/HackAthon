"""Grafo exato da base (``grafo_exato.json``) e extração no esquema do graphify (``extracao.json``).

``kb`` não depende do graphify: ``extracao.json`` só segue o formato que ele lê.
"""
from __future__ import annotations

import argparse
import json
from pathlib import Path

from kb.fonte import COMUM, PASTA_DOENCAS, ler_fonte
from kb.grafo import Grafo, base_para_grafo, grafo_para_base
from kb.modelos import Base


def _origens(origem: Path) -> dict[str, str]:
    """Id de símbolo/regra -> caminho do arquivo da fonte onde está."""
    arquivos = [COMUM] + [f"{PASTA_DOENCAS}/{c.name}" for c in sorted((origem / PASTA_DOENCAS).glob("*.json"))]
    achados: dict[str, str] = {}
    for relativo in arquivos:
        dados = json.loads((origem / relativo).read_text(encoding="utf-8"))
        for item in [*dados.get("simbolos", []), *dados.get("regras", [])]:
            achados[item["id"]] = f"{origem.as_posix()}/{relativo}"
    achados["__comum__"] = f"{origem.as_posix()}/{COMUM}"
    return achados


def extracao(base: Base, origem_por_id: dict[str, str]) -> dict:
    nomes = {s.id: s.nome for s in base.simbolos}
    nodes: list[dict] = [
        {"id": f"sim:{s.id}", "label": s.nome, "file_type": "concept",
         "source_file": origem_por_id[s.id], "tipo": s.tipo}
        for s in base.simbolos
    ]
    edges: list[dict] = []
    for r in base.regras:
        arquivo = origem_por_id[r.id]
        condicoes = " E ".join(nomes[c.simbolo] for c in r.se)
        nodes.append({"id": f"regra:{r.id}",
                      "label": f"{r.id}: SE {condicoes} ENTÃO {nomes[r.entao.simbolo]}",
                      "file_type": "concept", "source_file": arquivo, "classe": r.classe})
        for c in r.se:
            edges.append({"source": f"sim:{c.simbolo}", "target": f"regra:{r.id}", "relation": "condicao_de",
                          "confidence": "EXTRACTED", "source_file": arquivo})
        edges.append({"source": f"regra:{r.id}", "target": f"sim:{r.entao.simbolo}", "relation": "conclui",
                      "confidence": "EXTRACTED", "source_file": arquivo, "cf": r.entao.cf})
    comum = f"{origem_por_id['__comum__']}"
    for e in base.meta.exclusoes:
        a, b = e.doencas
        edges.append({"source": f"sim:{a}", "target": f"sim:{b}", "relation": "exclui",
                      "confidence": "EXTRACTED", "source_file": comum})
    return {"nodes": nodes, "edges": edges, "hyperedges": [], "input_tokens": 0, "output_tokens": 0}


def _gravar(caminho: Path, dados) -> None:
    caminho.write_text(json.dumps(dados, ensure_ascii=False, indent=2) + "\n", encoding="utf-8", newline="\n")


def exportar(origem: Path, saida: Path) -> tuple[Path, Path]:
    origem, saida = Path(origem), Path(saida)
    base = ler_fonte(origem)
    saida.mkdir(parents=True, exist_ok=True)
    exato, ext = saida / "grafo_exato.json", saida / "extracao.json"
    _gravar(exato, base_para_grafo(base).model_dump(mode="json", exclude_none=True))
    _gravar(ext, extracao(base, _origens(origem)))
    return exato, ext


def carregar_do_grafo(caminho: Path) -> Base:
    grafo = Grafo.model_validate(json.loads(Path(caminho).read_text(encoding="utf-8")))
    return grafo_para_base(grafo)


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(prog="python -m kb.exportar_grafo",
                                     description="Exporta a base da fonte como grafo.")
    parser.add_argument("--origem", default="base/fonte")
    parser.add_argument("--saida", default="graphify-out-dados")
    args = parser.parse_args(argv)
    exato, ext = exportar(Path(args.origem), Path(args.saida))
    dados = json.loads(ext.read_text(encoding="utf-8"))
    print(f"{len(dados['nodes'])} nós e {len(dados['edges'])} arestas gravados em {args.saida}.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
