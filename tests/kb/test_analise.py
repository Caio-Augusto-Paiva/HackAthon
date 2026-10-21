from kb.analise import (
    CAMADA,
    dependencias,
    derivados_com_cf_negativo,
    derivados_de_triagem,
    encontrar_ciclo,
    ordem_topologica,
    perguntavel,
    regras_que_concluem,
    simbolos_por_id,
    simbolos_triagem,
)
from kb.modelos import carregar_base
from tests.kb.apoio import carregar_minima


def _minima():
    return carregar_base(carregar_minima())


def _base_com_regras(*arestas):
    """Base de símbolos booleanos 'derivado' e uma regra por aresta (lê -> conclui)."""
    ids = sorted({i for a in arestas for i in a})
    return carregar_base({
        "meta": {},
        "simbolos": [
            {"id": i, "tipo": "derivado", "nome": i, "dominio": {"tipo": "booleano"}}
            for i in ids
        ],
        "regras": [
            {"id": f"R-{n}", "se": [{"simbolo": lido}], "entao": {"simbolo": concluido, "cf": 0.5}}
            for n, (lido, concluido) in enumerate(arestas)
        ],
    })


def test_camadas():
    assert CAMADA == {"pergunta": 0, "ficha": 0, "derivado": 1, "doenca": 2, "urgencia": 3}


def test_simbolos_por_id_e_dependencias_da_minima():
    base = _minima()
    assert set(simbolos_por_id(base)) == {s.id for s in base.simbolos}
    deps = dependencias(base)
    assert deps == {
        "recente": {"dias_em_lactacao"},
        "d1": {"sinal_a", "recente", "pergunta_x", "exame_v"},
        "chamar_agora": {"d1", "sinal_b"},
    }


def test_regras_que_concluem():
    base = _minima()
    assert [r.id for r in regras_que_concluem(base, "d1")] == ["R-D1-01", "R-D1-02", "R-D1-03"]
    assert regras_que_concluem(base, "observar") == []
    assert regras_que_concluem(base, "inexistente") == []


def test_ordem_topologica_da_minima():
    ordem = ordem_topologica(_minima())
    assert sorted(ordem) == sorted(s.id for s in _minima().simbolos)
    assert ordem.index("dias_em_lactacao") < ordem.index("recente") < ordem.index("d1")
    assert ordem.index("d1") < ordem.index("chamar_agora")
    assert ordem == ordem_topologica(_minima())


def test_ciclo_direto_e_indireto():
    direto = encontrar_ciclo(_base_com_regras(("a", "b"), ("b", "a")))
    assert direto[0] == direto[-1]
    assert set(direto) == {"a", "b"}
    indireto = encontrar_ciclo(_base_com_regras(("a", "b"), ("b", "c"), ("c", "a")))
    assert indireto[0] == indireto[-1]
    assert set(indireto) == {"a", "b", "c"}
    assert len(indireto) == 4


def test_auto_ciclo():
    assert encontrar_ciclo(_base_com_regras(("a", "a"))) == ["a", "a"]


def test_ordem_topologica_com_ciclo_levanta_erro():
    import pytest

    with pytest.raises(ValueError):
        ordem_topologica(_base_com_regras(("a", "b"), ("b", "a")))


def test_sem_ciclo_retorna_none():
    assert encontrar_ciclo(_minima()) is None


def test_perguntavel_por_modo():
    simbolos = simbolos_por_id(_minima())
    assert perguntavel(simbolos["exame_v"], "veterinario") is True
    assert perguntavel(simbolos["exame_v"], "produtor") is False
    assert perguntavel(simbolos["sinal_a"], "produtor") is True
    assert perguntavel(simbolos["dias_em_lactacao"], "veterinario") is True
    assert perguntavel(simbolos["d1"], "produtor") is False
    assert perguntavel(simbolos["d1"], "veterinario") is False
    assert perguntavel(simbolos["recente"], "veterinario") is False


def test_perguntavel_ignora_texto_em_branco():
    dados = carregar_minima()
    dados["simbolos"][1]["pergunta"]["produtor"] = "   "
    simbolo = simbolos_por_id(carregar_base(dados))["sinal_a"]
    assert perguntavel(simbolo, "produtor") is False
    assert perguntavel(simbolo, "veterinario") is True


def test_simbolos_triagem_inclui_por_modo():
    assert simbolos_triagem(_minima()) == {"dias_em_lactacao", "sinal_a", "sinal_b"}
    dados = carregar_minima()
    dados["meta"]["triagem"][0]["simbolos_por_modo"] = {"veterinario": ["exame_v"]}
    assert "exame_v" in simbolos_triagem(carregar_base(dados))


def test_derivados_de_triagem():
    assert "recente" in derivados_de_triagem(_minima())
    # derivado sem regra não conta
    dados = carregar_minima()
    dados["regras"] = [r for r in dados["regras"] if r["id"] != "R-REC-01"]
    assert derivados_de_triagem(carregar_base(dados)) == set()


def test_derivados_de_triagem_exclui_quem_le_fora_da_triagem():
    dados = carregar_minima()
    dados["regras"][0]["se"].append({"simbolo": "pergunta_x"})
    assert derivados_de_triagem(carregar_base(dados)) == set()


def test_derivados_com_cf_negativo():
    assert derivados_com_cf_negativo(_minima()) == set()
    dados = carregar_minima()
    dados["regras"].append({
        "id": "R-REC-02",
        "se": [{"simbolo": "sinal_a"}],
        "entao": {"simbolo": "recente", "cf": -0.5},
    })
    assert derivados_com_cf_negativo(carregar_base(dados)) == {"recente"}


def test_referencias_pendentes_sao_ignoradas():
    dados = carregar_minima()
    dados["regras"].append({
        "id": "R-X",
        "se": [{"simbolo": "fantasma"}],
        "entao": {"simbolo": "recente", "cf": -0.3},
    })
    dados["regras"].append({
        "id": "R-Y",
        "se": [{"simbolo": "sinal_a"}],
        "entao": {"simbolo": "outro_fantasma", "cf": 0.3},
    })
    base = carregar_base(dados)
    assert "fantasma" not in dependencias(base)["recente"]
    assert "outro_fantasma" not in dependencias(base)
    assert encontrar_ciclo(base) is None
    assert len(ordem_topologica(base)) == len(base.simbolos)
    assert "recente" not in derivados_de_triagem(base)
    assert derivados_com_cf_negativo(base) == {"recente"}
