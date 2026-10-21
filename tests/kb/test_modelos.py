import json

import pytest
from pydantic import ValidationError

from kb.modelos import Base, Caso, Condicao, Regra, carregar_base
from tests.kb.apoio import CAMINHO_BASE_MOTOR, CAMINHO_MINIMA, carregar_minima


def _regra(**extras):
    dados = {"id": "R-X", "se": [{"simbolo": "a"}], "entao": {"simbolo": "b", "cf": 0.5}}
    dados.update(extras)
    return dados


def test_base_minima_carrega():
    base = carregar_base(carregar_minima())
    assert isinstance(base, Base)
    assert len(base.meta.triagem) == 2
    assert base.meta.limiares.confirmacao == 0.8
    assert base.meta.limite_dinamico.produtor == 12
    assert base.meta.limite_dinamico.veterinario == 25


@pytest.mark.parametrize("classe,esperada", [
    ("bandeira_vermelha", 100), ("urgencia", 50), ("evidencia", 10)])
def test_prioridade_default_por_classe(classe, esperada):
    assert Regra.model_validate(_regra(classe=classe)).prioridade == esperada


def test_prioridade_default_e_evidencia_sem_classe():
    assert Regra.model_validate(_regra()).prioridade == 10


def test_prioridade_explicita_mantida():
    assert Regra.model_validate(_regra(classe="bandeira_vermelha", prioridade=0)).prioridade == 0
    assert Regra.model_validate(_regra(prioridade=7)).prioridade == 7


@pytest.mark.parametrize("ascii_,canonico", [("!=", "≠"), ("<=", "≤"), (">=", "≥")])
def test_operador_ascii_normalizado(ascii_, canonico):
    assert Condicao(simbolo="x", op=ascii_, valor=1).op == canonico


def test_operador_ascii_normalizado_na_carga():
    dados = carregar_minima()
    dados["regras"][0]["se"][0]["op"] = "<="
    assert carregar_base(dados).regras[0].se[0].op == "≤"


def test_operador_invalido_rejeitado():
    with pytest.raises(ValidationError):
        Condicao(simbolo="x", op="~", valor=1)


def test_condicao_defaults():
    c = Condicao(simbolo="x")
    assert (c.op, c.valor, c.negado, c.cf_minimo, c.cf_maximo) == ("=", True, False, None, None)


def test_campo_desconhecido_rejeitado():
    with pytest.raises(ValidationError):
        Regra.model_validate(_regra(campo_inventado=1))
    dados = carregar_minima()
    dados["regras"][0]["campo_inventado"] = 1
    with pytest.raises(ValidationError):
        carregar_base(dados)


def test_dominio_discriminado():
    dados = carregar_minima()
    dados["simbolos"][1]["dominio"] = {"tipo": "categorico"}
    with pytest.raises(ValidationError):
        carregar_base(dados)
    dados["simbolos"][1]["dominio"] = {"tipo": "categorico", "valores": []}
    with pytest.raises(ValidationError):
        carregar_base(dados)
    dados["simbolos"][1]["dominio"] = {"tipo": "categorico", "valores": ["a", "b"]}
    assert carregar_base(dados).simbolos[1].dominio.valores == ["a", "b"]


def test_dominio_desconhecido_rejeitado():
    dados = carregar_minima()
    dados["simbolos"][1]["dominio"] = {"tipo": "inventado"}
    with pytest.raises(ValidationError):
        carregar_base(dados)


def test_simbolo_defaults():
    simbolo = carregar_base(carregar_minima()).simbolos[1]
    assert simbolo.combinacao == "mycin"
    assert simbolo.por_que == {}


def test_regra_sem_condicoes_rejeitada():
    with pytest.raises(ValidationError):
        Regra.model_validate(_regra(se=[]))


def test_regra_status_default():
    assert Regra.model_validate(_regra()).status == "suposicao_a_validar"


def test_carrega_fixture_do_motor():
    base = carregar_base(CAMINHO_BASE_MOTOR)
    assert base.meta.triagem and base.regras
    assert all(r.prioridade == 0 for r in base.regras)  # explícita, mantida


def test_carregar_base_aceita_dict_texto_e_caminho():
    dados = carregar_minima()
    de_dict = carregar_base(dados)
    de_texto = carregar_base(json.dumps(dados, ensure_ascii=False))
    de_path = carregar_base(CAMINHO_MINIMA)
    de_str = carregar_base(str(CAMINHO_MINIMA))
    assert de_dict == de_texto == de_path == de_str


def test_caso_com_continuacao():
    caso = Caso.model_validate({
        "id": "C-01",
        "descricao": "caso com continuação",
        "modo": "produtor",
        "ficha": {"dias_em_lactacao": 10},
        "triagem": {"sinais": ["sinal_a"]},
        "continuacao": {"modo": "veterinario", "respostas": {"exame_v": True}},
        "limite_dinamico": 5,
        "esperado": {
            "urgencia": "chamar_agora",
            "top3_contem": ["d1"],
            "faixas": {"d1": [70, 100]},
            "alerta": {"pausa": True},
        },
    })
    assert caso.continuacao.modo == "veterinario"
    assert caso.esperado.faixas["d1"] == (70.0, 100.0)
    assert caso.esperado.alerta.pausa is True


def test_caso_minimo_e_extra_proibido():
    caso = Caso.model_validate({"id": "C", "descricao": "d", "modo": "produtor", "esperado": {}})
    assert caso.continuacao is None and caso.ficha == {}
    with pytest.raises(ValidationError):
        Caso.model_validate({"id": "C", "descricao": "d", "modo": "produtor",
                             "esperado": {"inventado": 1}})
    with pytest.raises(ValidationError):
        Caso.model_validate({"id": "C", "descricao": "d", "modo": "produtor",
                             "esperado": {"faixas": {"d1": [1, 2, 3]}}})
