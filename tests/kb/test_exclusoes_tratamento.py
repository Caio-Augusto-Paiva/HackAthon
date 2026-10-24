import pytest

from kb.modelos import carregar_base
from kb.validador import validar
from tests.kb.apoio import carregar_minima


def _base_com_d2() -> dict:
    d = carregar_minima()
    d["simbolos"].append({"id": "d2", "tipo": "doenca", "nome": "Doença D2",
                          "dominio": {"tipo": "booleano"}, "gravidade": "media"})
    d["regras"].append({"id": "R-D2-01", "se": [{"simbolo": "sinal_a"}], "entao": {"simbolo": "d2", "cf": 0.5},
                        "fonte": "teste", "status": "validada"})
    return d


def _exclusao(a, b, nota="teste"):
    return {"doencas": [a, b], "fonte": "teste", "nota": nota}


def _simbolo(d, id_):
    return next(s for s in d["simbolos"] if s["id"] == id_)


def _codigos(d) -> list[str]:
    return [e.codigo for e in validar(carregar_base(d)).erros]


def test_base_minima_com_d2_valida():
    assert validar(carregar_base(_base_com_d2())).valida


def test_exclusao_valida_aceita():
    d = _base_com_d2()
    d["meta"]["exclusoes"] = [_exclusao("d1", "d2")]
    assert validar(carregar_base(d)).valida


def test_exclusao_doenca_inexistente():
    d = _base_com_d2()
    d["meta"]["exclusoes"] = [_exclusao("d1", "nao_existe")]
    r = validar(carregar_base(d))
    assert not r.valida
    assert "exclusao_doenca_inexistente" in [e.codigo for e in r.erros]


def test_exclusao_com_simbolo_que_nao_e_doenca_e_inexistente():
    d = _base_com_d2()
    d["meta"]["exclusoes"] = [_exclusao("d1", "sinal_a")]
    assert "exclusao_doenca_inexistente" in _codigos(d)


def test_exclusao_mesma_doenca():
    d = _base_com_d2()
    d["meta"]["exclusoes"] = [_exclusao("d1", "d1")]
    r = validar(carregar_base(d))
    assert not r.valida
    assert "exclusao_mesma_doenca" in [e.codigo for e in r.erros]


def test_exclusao_duplicada():
    d = _base_com_d2()
    d["meta"]["exclusoes"] = [_exclusao("d1", "d2"), _exclusao("d2", "d1")]
    r = validar(carregar_base(d))
    assert not r.valida
    assert "exclusao_duplicada" in [e.codigo for e in r.erros]


@pytest.mark.parametrize("url", [
    "javascript:alert(1)",
    "http://www.embrapa.br/x",
    "https://embrapa.br.evil.com/x",
    "https://exemplo.com",
])
def test_tratamento_url_fora_da_lista_recusada(url):
    d = _base_com_d2()
    _simbolo(d, "d1")["tratamento"] = {"titulo": "Tratamento", "url": url}
    r = validar(carregar_base(d))
    assert not r.valida
    assert "tratamento_url_invalida" in [e.codigo for e in r.erros]


@pytest.mark.parametrize("url", [
    "https://www.embrapa.br/x",
    "https://www.gov.br/agricultura/x",
    "https://www.msdvetmanual.com/pt/x",
])
def test_tratamento_url_permitida(url):
    d = _base_com_d2()
    _simbolo(d, "d1")["tratamento"] = {"titulo": "Tratamento", "url": url}
    assert validar(carregar_base(d)).valida


def test_tratamento_em_pergunta_recusado():
    d = _base_com_d2()
    _simbolo(d, "sinal_a")["tratamento"] = {"titulo": "Tratamento", "url": "https://www.embrapa.br/x"}
    r = validar(carregar_base(d))
    assert not r.valida
    assert "tratamento_fora_de_doenca" in [e.codigo for e in r.erros]
