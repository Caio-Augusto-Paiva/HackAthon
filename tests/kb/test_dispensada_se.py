from kb.modelos import carregar_base
from kb.validador import validar
from tests.kb.apoio import carregar_minima


def _com_dispensa(alvos) -> dict:
    d = carregar_minima()
    next(s for s in d["simbolos"] if s["id"] == "sinal_a")["dispensada_se"] = alvos
    return d


def _codigos(d) -> list[str]:
    return [e.codigo for e in validar(carregar_base(d)).erros]


def test_dispensada_se_com_pergunta_existente_valida():
    assert _codigos(_com_dispensa(["exame_v"])) == []


def test_dispensada_se_com_simbolo_inexistente_recusada():
    assert "dispensada_se_invalida" in _codigos(_com_dispensa(["nao_existe"]))


def test_dispensada_se_com_conceito_recusada():
    assert "dispensada_se_invalida" in _codigos(_com_dispensa(["d1"]))


def test_dispensada_se_com_o_proprio_simbolo_recusada():
    assert "dispensada_se_invalida" in _codigos(_com_dispensa(["sinal_a"]))


def test_simbolo_sem_dispensa_continua_sem_o_campo_no_json():
    base = carregar_base(carregar_minima())
    assert all("dispensada_se" not in s for s in base.model_dump(mode="json", exclude_none=True)["simbolos"])
