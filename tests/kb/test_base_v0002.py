"""A v0002 da base real limita os domínios numéricos e só muda isso em relação à v0001."""
from pathlib import Path

from engine.modelos import Base as BaseMotor
from kb import para_motor
from kb.carregador import Repositorio
from kb.validador import validar

RAIZ = Path(__file__).resolve().parents[2] / "base"
LIMITES = {
    "dias_em_lactacao": {"max": 1000, "casas_decimais": 0},
    "temperatura_retal": {"min": 30, "max": 45, "casas_decimais": 1},
    "ph_ruminal": {"casas_decimais": 1},
    "bhb_sanguineo": {"max": 20, "casas_decimais": 2},
    "calcio_serico": {"max": 20, "casas_decimais": 2},
}


def test_v0002_valida_tem_pai_e_carrega_no_motor():
    repo = Repositorio(RAIZ)
    base = repo.carregar("v0002")
    assert base.meta.pai == "v0001"
    assert not validar(base).erros
    BaseMotor.de_dict(para_motor(base))


def test_v0002_so_muda_dominios_numericos():
    repo = Repositorio(RAIZ)
    antiga, nova = (repo.carregar(v).model_dump(mode="json", exclude_none=True) for v in ("v0001", "v0002"))
    for s in antiga["simbolos"]:
        s["dominio"] = {k: v for k, v in s["dominio"].items() if s["id"] not in LIMITES or k not in LIMITES[s["id"]]}
    for s in nova["simbolos"]:
        if s["id"] in LIMITES:
            assert {k: s["dominio"][k] for k in LIMITES[s["id"]]} == LIMITES[s["id"]]
            s["dominio"] = {k: v for k, v in s["dominio"].items() if k not in LIMITES[s["id"]]}
    antiga["meta"], nova["meta"] = {}, {}
    assert antiga == nova
