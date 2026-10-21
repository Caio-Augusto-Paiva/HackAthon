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
    assert "prioridade" not in dados  # padrão por classe não é gravado


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


def _minima_com_valor_none():
    base = _minima()
    regra = next(r for r in base.regras if r.id == "R-D1-01")
    regra.se[0] = regra.se[0].model_copy(update={"valor": None})
    assert regra.se[0].valor is None
    return base


def test_valor_none_explicito_ida_e_volta_em_memoria():
    base = _minima_com_valor_none()
    nova = grafo_para_base(base_para_grafo(base))
    assert nova == base
    assert next(r for r in nova.regras if r.id == "R-D1-01").se[0].valor is None


def test_valor_none_explicito_ida_e_volta_por_json():
    base = _minima_com_valor_none()
    texto = base_para_grafo(base).model_dump_json()  # sem exclude_none: escreve "valor": null
    nova = grafo_para_base(Grafo.model_validate_json(texto))
    assert nova == base
    assert next(r for r in nova.regras if r.id == "R-D1-01").se[0].valor is None


def test_valor_ausente_continua_default_true():
    grafo = base_para_grafo(_minima())
    alvo = next(a for a in grafo.arestas if a.id == "R-D1-01:se:0")
    sem_valor = Aresta.model_validate({k: v for k, v in alvo.model_dump(exclude_none=True).items()
                                       if k != "valor"})
    grafo.arestas = [sem_valor if a.id == alvo.id else a for a in grafo.arestas]
    regra = next(r for r in grafo_para_base(grafo).regras if r.id == "R-D1-01")
    assert regra.se[0].valor is True


def test_id_do_no_de_simbolo_difere_dos_dados():
    grafo = base_para_grafo(_minima())
    _no(grafo, "sinal_a").id = "sinal_renomeado"
    with pytest.raises(ValueError, match="sinal_renomeado.*sinal_a"):
        grafo_para_base(grafo)


def test_id_do_no_de_regra_difere_dos_dados():
    grafo = base_para_grafo(_minima())
    _no(grafo, "R-D1-01").id = "R-NOVA"
    with pytest.raises(ValueError, match="R-NOVA.*R-D1-01"):
        grafo_para_base(grafo)


def test_no_duplicado_rejeitado():
    grafo = base_para_grafo(_minima())
    grafo.nos.append(_no(grafo, "sinal_a").model_copy(deep=True))
    with pytest.raises(ValueError, match="duplicado.*sinal_a"):
        grafo_para_base(grafo)


# --- contrato da API: arestas sem ``ordem`` (spec 4.5.3) ------------------------

def _grafo_sem_ordem(base=None):
    """Grafo no formato do contrato do editor: arestas sem ``ordem``."""
    grafo = base_para_grafo(base or _minima())
    dados = grafo.model_dump(mode="json", exclude_none=True)
    for aresta in dados["arestas"]:
        aresta.pop("ordem", None)
    return Grafo.model_validate(dados)


def test_aresta_sem_ordem_tem_ordem_none():
    assert all(a.ordem is None for a in _grafo_sem_ordem().arestas if a.papel == "condicao")


def test_grafo_sem_ordem_converte_e_preserva_ordem_da_lista():
    base = _minima()
    regra = next(r for r in base.regras if r.id == "R-D1-02")
    regra.se.append(regra.se[0].model_copy(update={"simbolo": "sinal_a"}))
    regra.se.append(regra.se[0].model_copy(update={"simbolo": "sinal_b"}))
    assert len(regra.se) == 4
    assert grafo_para_base(_grafo_sem_ordem(base)) == base


def test_base_para_grafo_continua_emitindo_ordem():
    grafo = base_para_grafo(_minima())
    ordens = {a.id: a.ordem for a in grafo.arestas if a.papel == "condicao"}
    assert ordens["R-D1-02:se:0"] == 0 and ordens["R-D1-02:se:1"] == 1


def test_ordem_explicita_vem_antes_das_sem_ordem_e_desempata_pela_posicao():
    grafo = _grafo_sem_ordem()
    a0, a1 = (a for a in grafo.arestas if a.id in ("R-D1-02:se:0", "R-D1-02:se:1"))
    a1.ordem = 0  # só a segunda tem ordem: vem primeiro; a sem ordem fica por último
    regra = next(r for r in grafo_para_base(grafo).regras if r.id == "R-D1-02")
    assert [c.simbolo for c in regra.se] == ["pergunta_x", "recente"]


def test_ordem_duplicada_so_vale_entre_explicitas():
    grafo = _grafo_sem_ordem()
    grafo_para_base(grafo)  # várias sem ordem: sem erro
    a0, a1 = (a for a in grafo.arestas if a.id in ("R-D1-02:se:0", "R-D1-02:se:1"))
    a0.ordem = a1.ordem = 3
    with pytest.raises(ValueError, match="R-D1-02"):
        grafo_para_base(grafo)


# --- nó sem ``id`` nos dados ------------------------------------------------------

def test_dados_do_no_sem_id_recebem_o_id_do_no():
    base = _minima()
    grafo = base_para_grafo(base)
    for no in grafo.nos:
        no.dados.pop("id")
    assert grafo_para_base(grafo) == base


def test_dados_com_id_diferente_continuam_rejeitados():
    grafo = base_para_grafo(_minima())
    _no(grafo, "sinal_a").dados["id"] = "outro"
    with pytest.raises(ValueError, match="sinal_a.*outro"):
        grafo_para_base(grafo)


# --- campos de papel errado -------------------------------------------------------

def _aresta(grafo, id_):
    return next(a for a in grafo.arestas if a.id == id_)


def test_cf_em_aresta_de_condicao_rejeitado():
    grafo = base_para_grafo(_minima())
    _aresta(grafo, "R-D1-01:se:0").cf = 0.3
    with pytest.raises(ValueError, match=r"R-D1-01:se:0.*cf"):
        grafo_para_base(grafo)


@pytest.mark.parametrize("campo,valor", [
    ("op", "="), ("valor", True), ("negado", False), ("cf_minimo", 0.5), ("cf_maximo", 0.5),
])
def test_campo_de_condicao_em_aresta_de_conclusao_rejeitado(campo, valor):
    grafo = base_para_grafo(_minima())
    setattr(_aresta(grafo, "R-D1-01:entao"), campo, valor)
    with pytest.raises(ValueError, match=rf"R-D1-01:entao.*{campo}"):
        grafo_para_base(grafo)
