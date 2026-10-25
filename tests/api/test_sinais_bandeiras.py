"""Bandeiras em linguagem simples: os sinais que acenderam o alerta e os que ainda faltam verificar."""
from __future__ import annotations

from pathlib import Path

import pytest

from api.servicos.textos import sinais_das_regras
from kb.carregador import Repositorio

RAIZ = Path(__file__).resolve().parents[2]


@pytest.fixture(scope="module")
def base_ativa():
    repo = Repositorio(RAIZ / "base")
    return repo.carregar(repo.versao_ativa())


def test_sinais_das_regras_sem_repetir(base_ativa):
    # R-BV-03 (apetite ausente e apatia) e R-BV-04 (hipotermia e apatia) compartilham a apatia.
    assert sinais_das_regras(base_ativa, ["R-BV-03", "R-BV-04"]) == ["apetite ausente", "apatia", "hipotermia"]


def test_sinais_pendentes_deixam_de_fora_o_que_ja_foi_respondido(base_ativa):
    assert sinais_das_regras(base_ativa, ["R-BV-05"], conhecidos={"ubere_inflamado"}) == ["febre", "apatia"]


def test_regra_desconhecida_nao_quebra(base_ativa):
    assert sinais_das_regras(base_ativa, ["R-NAO-EXISTE"]) == []
