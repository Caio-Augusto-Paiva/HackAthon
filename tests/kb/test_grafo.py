import random

import pytest
from hypothesis import HealthCheck, given, settings
from hypothesis import strategies as st

from kb.grafo import Aresta, Grafo, base_para_grafo, grafo_para_base
from kb.modelos import Posicao, carregar_base
from tests.kb.apoio import CAMINHO_BASE_MOTOR, carregar_minima


def _minima():
    return carregar_base(carregar_minima())


def _no(grafo, id_):
    return next(n for n in grafo.nos if n.id == id_)


def test_ida_e_volta_minima():
    base = _minima()
    assert grafo_para_base(base_para_grafo(base)) == base


def test_ida_e_volta_fixture_motor():
    base = carregar_base(CAMINHO_BASE_MOTOR)
    assert grafo_para_base(base_para_grafo(base)) == base


def test_ida_e_volta_passando_por_json():
    base = carregar_base(CAMINHO_BASE_MOTOR)
    grafo = base_para_grafo(base)
    texto = grafo.model_dump_json(exclude_none=True)
    assert grafo_para_base(Grafo.model_validate_json(texto)) == base


def test_nos_na_ordem_simbolos_depois_regras():
    base = _minima()
    grafo = base_para_grafo(base)
    esperado = [s.id for s in base.simbolos] + [r.id for r in base.regras]
    assert [n.id for n in grafo.nos] == esperado
    assert {n.tipo_no for n in grafo.nos[: len(base.simbolos)]} == {"simbolo"}
    assert {n.tipo_no for n in grafo.nos[len(base.simbolos):]} == {"regra"}
    assert grafo.versao == base.meta.versao


def test_arestas_ids_papeis_e_campos():
    grafo = base_para_grafo(_minima())
    por_id = {a.id: a for a in grafo.arestas}
    cond = por_id["R-D1-02:se:1"]
    assert (cond.papel, cond.origem, cond.destino, cond.ordem) == ("condicao", "pergunta_x", "R-D1-02", 1)
    assert cond.cf is None
    concl = por_id["R-D1-02:entao"]
    assert (concl.papel, concl.origem, concl.destino) == ("conclusao", "R-D1-02", "d1")
    assert concl.cf is not None
    assert (concl.op, concl.valor, concl.negado, concl.cf_minimo, concl.cf_maximo) == (None,) * 5


def test_dados_da_regra_sem_se_e_entao():
    grafo = base_para_grafo(_minima())
    dados = _no(grafo, "R-D1-02").dados
    assert "se" not in dados and "entao" not in dados
    assert dados["id"] == "R-D1-02"
    assert dados["prioridade"] == 10


def test_ordem_das_condicoes_preservada():
    base = _minima()
    regra = next(r for r in base.regras if r.id == "R-D1-02")
    regra.se.append(regra.se[0].model_copy(update={"simbolo": "sinal_a"}))
    regra.se.append(regra.se[0].model_copy(update={"simbolo": "sinal_b"}))
    assert len(regra.se) == 4
    grafo = base_para_grafo(base)
    random.Random(7).shuffle(grafo.arestas)
    assert grafo_para_base(grafo) == base
    reconstruida = next(r for r in grafo_para_base(grafo).regras if r.id == "R-D1-02")
    assert [c.simbolo for c in reconstruida.se] == [c.simbolo for c in regra.se]


def test_ordem_das_condicoes_segue_o_campo_ordem():
    grafo = base_para_grafo(_minima())
    a0, a1 = (a for a in grafo.arestas if a.id in ("R-D1-02:se:0", "R-D1-02:se:1"))
    a0.ordem, a1.ordem = 1, 0
    regra = next(r for r in grafo_para_base(grafo).regras if r.id == "R-D1-02")
    assert [c.simbolo for c in regra.se] == ["pergunta_x", "recente"]


def test_empate_de_ordem_rejeitado():
    grafo = base_para_grafo(_minima())
    for a in grafo.arestas:
        if a.id == "R-D1-02:se:1":
            a.ordem = 0
    with pytest.raises(ValueError, match="R-D1-02"):
        grafo_para_base(grafo)


def test_layout_separado():
    base = _minima()
    base.layout = {"sinal_a": Posicao(x=1, y=2)}
    grafo = base_para_grafo(base)
    assert grafo.layout == {"sinal_a": Posicao(x=1, y=2)}
    grafo.layout["sinal_a"] = Posicao(x=99, y=-5)
    grafo.layout["R-D1-01"] = Posicao(x=3, y=4)
    nova = grafo_para_base(grafo)
    assert nova.simbolos == base.simbolos
    assert nova.regras == base.regras
    assert nova.layout == grafo.layout
    assert base.layout == {"sinal_a": Posicao(x=1, y=2)}  # a base original não mudou


def test_triagem_marcada():
    grafo = base_para_grafo(_minima())
    assert _no(grafo, "sinal_a").triagem is True
    assert _no(grafo, "dias_em_lactacao").triagem is True
    assert _no(grafo, "pergunta_x").triagem is False
    assert _no(grafo, "R-D1-01").triagem is False


def test_regra_sem_conclusao_rejeitada():
    grafo = base_para_grafo(_minima())
    grafo.arestas = [a for a in grafo.arestas if a.id != "R-D1-01:entao"]
    with pytest.raises(ValueError, match="R-D1-01"):
        grafo_para_base(grafo)


def test_regra_com_duas_conclusoes_rejeitada():
    grafo = base_para_grafo(_minima())
    grafo.arestas.append(Aresta(id="R-D1-01:entao2", papel="conclusao", origem="R-D1-01",
                                destino="observar", cf=0.5))
    with pytest.raises(ValueError, match="R-D1-01"):
        grafo_para_base(grafo)


@pytest.mark.parametrize("campo", ["origem", "destino"])
def test_aresta_com_no_inexistente_rejeitada(campo):
    grafo = base_para_grafo(_minima())
    alvo = next(a for a in grafo.arestas if a.id == "R-D1-01:se:0")
    setattr(alvo, campo, "fantasma")
    with pytest.raises(ValueError, match="fantasma"):
        grafo_para_base(grafo)


def test_condicao_regra_para_simbolo_rejeitada():
    grafo = base_para_grafo(_minima())
    alvo = next(a for a in grafo.arestas if a.id == "R-D1-01:se:0")
    alvo.origem, alvo.destino = alvo.destino, alvo.origem
    with pytest.raises(ValueError, match="R-D1-01:se:0"):
        grafo_para_base(grafo)


def test_conclusao_simbolo_para_regra_rejeitada():
    grafo = base_para_grafo(_minima())
    alvo = next(a for a in grafo.arestas if a.id == "R-D1-01:entao")
    alvo.origem, alvo.destino = alvo.destino, alvo.origem
    with pytest.raises(ValueError, match="R-D1-01:entao"):
        grafo_para_base(grafo)


def test_reconstroi_so_de_nos_e_arestas():
    """A base reconstruída não pode depender de nenhuma cópia guardada no grafo."""
    base = _minima()
    grafo = base_para_grafo(base)
    grafo.arestas = [a for a in grafo.arestas if a.id != "R-D1-01:se:0"] + [
        Aresta(id="R-D1-01:se:0", papel="condicao", origem="sinal_b", destino="R-D1-01", ordem=0)]
    regra = next(r for r in grafo_para_base(grafo).regras if r.id == "R-D1-01")
    assert regra.se[0].simbolo == "sinal_b"


@settings(max_examples=50, deadline=None, suppress_health_check=[HealthCheck.function_scoped_fixture])
@given(cf=st.floats(min_value=-0.99, max_value=0.99, allow_nan=False), negado=st.booleans())
def test_propriedade_cf_e_negado(cf, negado):
    base = _minima()
    regra = next(r for r in base.regras if r.id == "R-D1-01")
    regra.entao.cf = cf
    regra.se[0].negado = negado
    grafo = Grafo.model_validate_json(base_para_grafo(base).model_dump_json(exclude_none=True))
    nova = grafo_para_base(grafo)
    assert nova == base
    refeita = next(r for r in nova.regras if r.id == "R-D1-01")
    assert refeita.entao.cf == cf and refeita.se[0].negado is negado
