"""Os exemplos de animal do contrato usam só campos de ficha que a base ativa conhece."""
from __future__ import annotations

import json
from pathlib import Path

import pytest

from api.servicos.ficha import campos_da_ficha, validar_ficha
from kb.carregador import Repositorio

RAIZ = Path(__file__).resolve().parents[2]
PASTA_EXEMPLOS = RAIZ / "contratos" / "exemplos"


@pytest.fixture(scope="module")
def base_ativa():
    repo = Repositorio(RAIZ / "base")
    return repo.carregar(repo.versao_ativa())


def _exemplo(nome: str) -> dict:
    return json.loads((PASTA_EXEMPLOS / f"{nome}.json").read_text(encoding="utf-8"))


def test_criar_animal_requisicao_e_valida_na_base_ativa(base_ativa):
    ficha = _exemplo("criar_animal")["requisicao"]["ficha"]
    assert validar_ficha(base_ativa, ficha) == []


@pytest.mark.parametrize("nome", ["criar_animal", "obter_animal"])
def test_ficha_da_resposta_tem_exatamente_os_campos_da_base_ativa(base_ativa, nome):
    ficha = _exemplo(nome)["resposta"]["ficha"]
    assert list(ficha) == list(campos_da_ficha(base_ativa))


def test_importacao_cita_apenas_campos_da_base_ativa(base_ativa):
    resposta = _exemplo("importar_animais")["resposta"]
    citados = {c for a in resposta["atualizados"] for c in a["campos"]}
    citados |= {e["campo"] for r in resposta["rejeitados"] for e in r["erros"]}
    assert citados <= set(campos_da_ficha(base_ativa))
