"""Grafo exato da base e extração para o graphify."""
import json
from pathlib import Path

import pytest

from engine.casos import executar_caso
from kb import carregar_base, para_motor
from kb.exportar_grafo import carregar_do_grafo, exportar
from kb.fonte import gravar_fonte

RAIZ = Path(__file__).resolve().parents[2]


@pytest.fixture
def v0002():
    return carregar_base(RAIZ / "base/versoes/v0002.json")


@pytest.fixture
def saida(tmp_path, v0002):
    gravar_fonte(v0002, tmp_path / "fonte")
    return exportar(tmp_path / "fonte", tmp_path / "saida")


def test_carregar_do_grafo_igual_v0002(saida, v0002):
    assert carregar_do_grafo(saida[0]) == v0002


def test_casos_iguais_lendo_do_grafo(saida, v0002):
    do_grafo = carregar_do_grafo(saida[0])
    casos = json.loads((RAIZ / "base/casos/casos.json").read_text(encoding="utf-8"))
    assert casos
    motor_a, motor_b = para_motor(v0002), para_motor(do_grafo)
    for caso in casos:
        assert executar_caso(motor_b, caso) == executar_caso(motor_a, caso)


def test_extracao_no_esquema_do_graphify(saida):
    dados = json.loads(saida[1].read_text(encoding="utf-8"))
    assert dados["hyperedges"] == []
    ids = {n["id"] for n in dados["nodes"]}
    for no in dados["nodes"]:
        assert {"id", "label", "file_type", "source_file"} <= no.keys()
        assert no["source_file"].endswith(".json")
    assert dados["edges"]
    for a in dados["edges"]:
        assert {"source", "target", "relation", "confidence", "source_file"} <= a.keys()
        assert a["source"] in ids and a["target"] in ids
        assert a["confidence"] == "EXTRACTED"
    assert sum(i.startswith("sim:") for i in ids) == 51
    assert sum(i.startswith("regra:") for i in ids) == 56
