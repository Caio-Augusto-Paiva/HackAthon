"""Contrato kb -> motor: tudo que o kb declara válido, o motor precisa conseguir carregar."""
import copy
import json

import pytest

from engine.modelos import Base as BaseMotor
from kb.modelos import carregar_base, para_motor
from kb.validador import validar, validar_dados
from tests.kb import test_validador as tv
from tests.kb.apoio import CAMINHO_BASE_MOTOR, carregar_minima


def _m_tela_com_derivado(d):
    tela = next(t for t in d["meta"]["triagem"] if t["id"] == "sinais")
    tela["simbolos"].append("recente")


def _m_tela_duplicada(d):
    d["meta"]["triagem"].append(copy.deepcopy(d["meta"]["triagem"][1]))


def _m_max_em_doenca(d):
    tv._simbolo(d, "d1")["combinacao"] = "max"


def _m_max_com_cf_zero(d):
    tv._simbolo(d, "recente")["combinacao"] = "max"
    tv._nova_regra(d, "R-REC-02", [{"simbolo": "sinal_a"}], "recente", 0.0)


def _m_limite_negativo(d):
    d["meta"]["limite_dinamico"] = {"produtor": -1, "veterinario": 25}


def _m_limiar_nan(d):
    d["meta"]["limiares"] = {"exaustao": float("nan")}


def _m_cf_infinito(d):
    tv._regra(d, "R-D1-03")["entao"]["cf"] = float("inf")


def _m_limite_dinamico_nan(d):
    d["meta"]["limite_dinamico"] = {"produtor": 12, "veterinario": float("nan")}


def _carrega(nome_mut):
    from tests.kb.test_validador import MUTACOES_ERRO
    dados = carregar_minima()
    MUTACOES_ERRO[nome_mut][0](dados)
    return dados


CASOS_QUE_O_MOTOR_RECUSA = {
    "tela-com-derivado": (_m_tela_com_derivado, "E21"),
    "tela-duplicada": (_m_tela_duplicada, "E02"),
    "max-em-doenca": (_m_max_em_doenca, "E14"),
    "max-com-cf-zero": (_m_max_com_cf_zero, "E14"),
    "limite-dinamico-negativo": (_m_limite_negativo, "E00"),
    "limiar-nan": (_m_limiar_nan, "E00"),
    "cf-infinito": (_m_cf_infinito, "E00"),
    "limite-dinamico-nan": (_m_limite_dinamico_nan, "E00"),
}

# mutações (de tests/kb/test_validador.py) que o motor recusa e o kb precisa recusar também
MUTACOES_QUE_O_MOTOR_RECUSA = {
    "E22-negativo": "E22", "E22-zero": "E22", "E22-bandeira": "E22",
    "E19-urgencia-monitorar": "E19", "E19-bandeira-derivado": "E19", "E19-urgencia-em-doenca": "E19",
    "E17-confirmacao": "E17", "E17-descarte": "E17", "E17-bloco-principal": "E17",
    "E17-bloco-diferencial-negativo": "E17", "E17-blocos-invertidos": "E17",
}


@pytest.mark.parametrize("nome", list(MUTACOES_QUE_O_MOTOR_RECUSA))
def test_motor_recusa_o_que_o_kb_recusa(nome):
    dados = _carrega(nome)
    assert MUTACOES_QUE_O_MOTOR_RECUSA[nome] in {p.numero for p in validar_dados(dados).erros}
    with pytest.raises(ValueError):
        BaseMotor.de_dict(para_motor(carregar_base(dados)))


@pytest.mark.parametrize("nome", list(CASOS_QUE_O_MOTOR_RECUSA))
def test_kb_reporta_erro_onde_o_motor_recusa(nome):
    mutacao, numero = CASOS_QUE_O_MOTOR_RECUSA[nome]
    dados = carregar_minima()
    mutacao(dados)
    rel = validar_dados(dados)
    assert rel.valida is False
    assert numero in {p.numero for p in rel.erros}, [(p.numero, p.mensagem) for p in rel.erros]


def _bases_validas():
    yield "minima", carregar_minima()
    yield "motor", json.loads(CAMINHO_BASE_MOTOR.read_text(encoding="utf-8"))
    for nome, mutacao in tv.MUTACOES_AVISO.items():  # só avisos: continuam válidas
        dados = carregar_minima()
        mutacao(dados)
        yield f"aviso-{nome}", dados


@pytest.mark.parametrize("nome,dados", list(_bases_validas()), ids=lambda v: v if isinstance(v, str) else "")
def test_valida_implica_motor_carrega(nome, dados):
    base = carregar_base(dados)
    assert validar(base).valida
    BaseMotor.de_dict(base.model_dump(mode="json", exclude_none=True))
    BaseMotor.de_dict(para_motor(base))


def test_para_motor_e_o_dump_sem_none():
    base = carregar_base(carregar_minima())
    assert para_motor(base) == base.model_dump(mode="json", exclude_none=True)


def test_motor_quebra_na_inferencia_com_derivado_nao_booleano():
    """O motor avalia a condição pelo domínio declarado: derivado numérico quebra (E23 evita isso)."""
    from engine.inferencia import inferir

    dados = _carrega("E23")
    assert "E23" in {p.numero for p in validar_dados(dados).erros}
    motor = para_motor(carregar_base(dados))
    BaseMotor.de_dict(motor)  # carrega; o problema só aparece ao inferir
    with pytest.raises(ValueError):
        inferir(motor, {"dias_em_lactacao": 10, "pergunta_x": True})
