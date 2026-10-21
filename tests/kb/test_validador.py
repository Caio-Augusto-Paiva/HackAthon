import copy
import json
import random

import pytest

from kb.modelos import carregar_base
from kb.validador import Alvo, Problema, Relatorio, Resumo, validar, validar_dados
from tests.kb.apoio import CAMINHO_BASE_MOTOR, carregar_minima


# --- ajudantes de mutação -------------------------------------------------

def _regra(d, id_):
    return next(r for r in d["regras"] if r["id"] == id_)


def _simbolo(d, id_):
    return next(s for s in d["simbolos"] if s["id"] == id_)


def _nova_regra(d, id_, se, simbolo, cf, **extra):
    regra = {"id": id_, "se": se, "entao": {"simbolo": simbolo, "cf": cf}, "fonte": "teste", "status": "validada"}
    regra.update(extra)
    d["regras"].append(regra)


def _novo_simbolo(d, id_, tipo, **extra):
    simbolo = {"id": id_, "tipo": tipo, "nome": id_, "dominio": {"tipo": "booleano"}}
    simbolo.update(extra)
    d["simbolos"].append(simbolo)


def _remover_regras(d, *ids):
    d["regras"] = [r for r in d["regras"] if r["id"] not in ids]


def _renomear_simbolo(d, antigo, novo):
    _simbolo(d, antigo)["id"] = novo
    for regra in d["regras"]:
        for cond in regra["se"]:
            if cond["simbolo"] == antigo:
                cond["simbolo"] = novo
        if regra["entao"]["simbolo"] == antigo:
            regra["entao"]["simbolo"] = novo
    for tela in d["meta"]["triagem"]:
        tela["simbolos"] = [novo if i == antigo else i for i in tela["simbolos"]]
        if antigo in tela.get("opcoes", {}):
            tela["opcoes"][novo] = tela["opcoes"].pop(antigo)


# --- mutações de cada código ----------------------------------------------

def _m_e01(d):
    _regra(d, "R-D1-01")["se"][0]["simbolo"] = "nao_existe"


def _m_e02(d):
    _regra(d, "R-D1-01")["id"] = "d1"


def _m_e03(d):
    cond = _regra(d, "R-D1-01")["se"][0]
    cond["op"], cond["valor"] = "=", False


def _m_e03_valor_nulo(d):
    _regra(d, "R-D1-01")["se"][0]["valor"] = None


def _m_e03_fora_do_dominio(d):
    # numérico fora de [min, max]
    _regra(d, "R-REC-01")["se"][0]["valor"] = 500


def _m_e03_operador_incompativel(d):
    # operador de ordem sobre booleano
    cond = _regra(d, "R-D1-01")["se"][0]
    cond["op"], cond["valor"] = ">", 1


def _m_e03_categorico(d):
    _simbolo(d, "pergunta_x")["dominio"] = {"tipo": "categorico", "valores": ["a", "b"]}
    _regra(d, "R-D1-02")["se"][1] = {"simbolo": "pergunta_x", "op": "em", "valor": ["a", "c"]}


def _m_e03_valor_de_outro_tipo(d):
    # texto comparado com símbolo numérico
    _regra(d, "R-REC-01")["se"][0]["valor"] = "vinte"


def _m_e04(d):
    _regra(d, "R-D1-03")["entao"]["cf"] = 1.0


def _m_e05(d):
    _novo_simbolo(d, "x", "derivado")
    _novo_simbolo(d, "y", "derivado")
    _nova_regra(d, "R-X", [{"simbolo": "y"}], "x", 0.5)
    _nova_regra(d, "R-Y", [{"simbolo": "x"}], "y", 0.5)


def _m_e06(d):
    _nova_regra(d, "R-X", [{"simbolo": "recente", "negado": True}], "d1", 0.4)


def _m_e06_derivado_sem_regra(d):
    _novo_simbolo(d, "z", "derivado")
    _nova_regra(d, "R-X", [{"simbolo": "z"}], "d1", 0.4)


def _m_e06_pergunta_sem_texto(d):
    _novo_simbolo(d, "muda", "pergunta")
    _nova_regra(d, "R-X", [{"simbolo": "muda"}], "d1", 0.4)


def _m_e07(d):
    _regra(d, "R-BV-01")["entao"]["simbolo"] = "observar"


def _m_e08(d):
    _regra(d, "R-BV-01")["se"][0]["simbolo"] = "pergunta_x"


def _m_e09(d):
    _novo_simbolo(d, "d2", "doenca", gravidade="baixa")


def _m_e10(d):
    _remover_regras(d, "R-D1-01", "R-D1-02")


def _m_e11(d):
    _remover_regras(d, "R-D1-01")


def _m_e12(d):
    _nova_regra(d, "R-X", [{"simbolo": "chamar_agora"}], "d1", 0.5)


def _m_e13(d):
    del _simbolo(d, "d1")["gravidade"]


def _m_e14(d):
    _simbolo(d, "recente")["combinacao"] = "max"
    _nova_regra(d, "R-REC-02", [{"simbolo": "sinal_a"}], "recente", -0.3)


def _m_e14_max_em_nao_derivado(d):
    _simbolo(d, "d1")["combinacao"] = "max"


def _m_e14_max_com_cf_zero(d):
    _simbolo(d, "recente")["combinacao"] = "max"
    _nova_regra(d, "R-REC-02", [{"simbolo": "sinal_a"}], "recente", 0.0)


def _m_e21(d):
    tela = next(t for t in d["meta"]["triagem"] if t["id"] == "sinais")
    tela["simbolos"].append("recente")  # derivado não é pergunta nem ficha


def _m_e21_por_modo(d):
    tela = next(t for t in d["meta"]["triagem"] if t["id"] == "sinais")
    tela["simbolos_por_modo"] = {"produtor": ["sinal_a", "d1"]}


def _m_e02_tela(d):
    d["meta"]["triagem"].append(copy.deepcopy(d["meta"]["triagem"][1]))


def _m_e15(d):
    _regra(d, "R-URG-d1")["se"][0]["cf_minimo"] = 1.5
    _regra(d, "R-D1-01")["se"][0]["cf_minimo"] = 0.5  # sinal_a não é doença nem derivado


def _m_e15_minimo_e_maximo(d):
    cond = _regra(d, "R-URG-d1")["se"][0]
    cond["cf_maximo"] = 0.9


def _m_e16(d):
    tela = next(t for t in d["meta"]["triagem"] if t["id"] == "sinais")
    del tela["texto"]["veterinario"]


def _m_e17(d):
    d["meta"]["limiares"] = {"premissa": 0.4, "bloco_diferencial": 0.6}


def _m_e18(d):
    del _regra(d, "R-D1-03")["fonte"]


def _m_e19(d):
    _nova_regra(d, "R-X", [{"simbolo": "sinal_a"}], "sem_problema", 0.5, classe="urgencia")
    _nova_regra(d, "R-Y", [{"simbolo": "sinal_a"}], "observar", 0.3, classe="evidencia")


def _m_e20(d):
    _renomear_simbolo(d, "sinal_a", "Sinal-A")


def _m_e22_negativo(d):
    _regra(d, "R-URG-d1")["entao"]["cf"] = -0.9


def _m_e22_zero(d):
    _regra(d, "R-URG-d1")["entao"]["cf"] = 0.0


def _m_e22_bandeira(d):
    _regra(d, "R-BV-01")["entao"]["cf"] = -0.5


def _m_e19_urgencia_monitorar(d):
    _novo_simbolo(d, "monitorar", "urgencia")
    _nova_regra(d, "R-MON", [{"simbolo": "sinal_a"}], "monitorar", 0.5, classe="urgencia")


def _m_e19_bandeira_derivado(d):
    _simbolo(d, "chamar_agora")["tipo"] = "derivado"
    _remover_regras(d, "R-URG-d1")


def _m_e19_urgencia_em_doenca(d):
    _nova_regra(d, "R-X", [{"simbolo": "sinal_a"}], "d1", 0.5, classe="urgencia")


def _m_e23(d):
    _simbolo(d, "recente")["dominio"] = {"tipo": "numerico", "min": 0, "max": 1}


def _m_e23_doenca(d):
    _simbolo(d, "d1")["dominio"] = {"tipo": "categorico", "valores": ["a"]}


def _m_e21_multipla_numerica(d):
    tela = next(t for t in d["meta"]["triagem"] if t["id"] == "dias")
    tela["selecao"] = "multipla"


def _m_e21_multipla_por_modo(d):
    tela = next(t for t in d["meta"]["triagem"] if t["id"] == "sinais")
    tela["simbolos_por_modo"] = {"produtor": ["sinal_a"], "veterinario": ["sinal_a", "dias_em_lactacao"]}


def _m_e17_confirmacao(d):
    d["meta"]["limiares"] = {"confirmacao": 1.5}


def _m_e17_descarte(d):
    d["meta"]["limiares"] = {"descarte": -1.5}


def _m_e17_bloco_principal(d):
    d["meta"]["limiares"] = {"bloco_principal": 1.5}


def _m_e17_bloco_diferencial_negativo(d):
    d["meta"]["limiares"] = {"bloco_diferencial": -0.1}


def _m_e17_blocos_invertidos(d):
    d["meta"]["limiares"] = {"bloco_diferencial": 0.6, "bloco_principal": 0.5}


def _d2_so_com_exame_t(d, tela_mutar):
    _novo_simbolo(d, "exame_t", "pergunta", pergunta={"veterinario": "Resultado do exame T é positivo?"})
    _novo_simbolo(d, "d2", "doenca", gravidade="baixa")
    _nova_regra(d, "R-D2-01", [{"simbolo": "exame_t"}], "d2", 0.5)
    tela = next(t for t in d["meta"]["triagem"] if t["id"] == "sinais")
    tela["simbolos"].append("exame_t")
    tela_mutar(tela)


def _m_e10_so_por_modo_veterinario(d):
    def mutar(tela):
        tela["simbolos_por_modo"] = {"produtor": ["sinal_a", "sinal_b"], "veterinario": ["sinal_a", "sinal_b", "exame_t"]}
    _d2_so_com_exame_t(d, mutar)


def _m_e10_tela_sem_texto_do_produtor(d):
    _d2_so_com_exame_t(d, lambda tela: None)  # exame_t só tem pergunta do veterinário


def _urgencia_le_d1(d, condicao):
    _nova_regra(d, "R-URG-x", [condicao, {"simbolo": "sinal_a"}], "observar", 0.5, classe="urgencia")


def _m_e06_cf_maximo_sem_regra_negativa(d):
    _urgencia_le_d1(d, {"simbolo": "d1", "cf_maximo": 0.1})


def _m_e06_negado_cf_minimo(d):
    _urgencia_le_d1(d, {"simbolo": "d1", "cf_minimo": 0.2, "negado": True})


def _m_e06_negado_cf_maximo_zero(d):
    _urgencia_le_d1(d, {"simbolo": "d1", "cf_maximo": 0.0, "negado": True})


def _m_e06_sem_regra_positiva(d):
    _novo_simbolo(d, "d3", "doenca", gravidade="baixa")
    _nova_regra(d, "R-D3-01", [{"simbolo": "sinal_a"}], "d3", -0.5)
    _urgencia_le_d1(d, {"simbolo": "d3", "cf_minimo": 0.3})


def _m_e06_derivado_max_negado(d):
    _simbolo(d, "recente")["combinacao"] = "max"
    _nova_regra(d, "R-X", [{"simbolo": "recente", "negado": True}], "d1", 0.4)


def _m_sem_e06_cf_maximo_com_regra_negativa(d):
    _nova_regra(d, "R-D1-neg", [{"simbolo": "sinal_b"}], "d1", -0.5)
    _urgencia_le_d1(d, {"simbolo": "d1", "cf_maximo": 0.1})


def _m_w01(d):
    _novo_simbolo(d, "nunca", "pergunta", pergunta={"produtor": "Pergunta nunca usada?"})


def _m_w02(d):
    copia = copy.deepcopy(_regra(d, "R-D1-01"))
    copia["id"] = "R-D1-01-contra"
    copia["entao"]["cf"] = -0.4
    d["regras"].append(copia)


def _m_w03(d):
    del _regra(d, "R-D1-01")["status"]


MUTACOES_ERRO = {
    "E01": (_m_e01, {"E01"}),
    "E02": (_m_e02, {"E02"}),
    "E03": (_m_e03, {"E03"}),
    "E03-nulo": (_m_e03_valor_nulo, {"E03"}),
    "E03-fora-do-dominio": (_m_e03_fora_do_dominio, {"E03"}),
    "E03-operador": (_m_e03_operador_incompativel, {"E03"}),
    "E03-categorico": (_m_e03_categorico, {"E03"}),
    "E03-tipo": (_m_e03_valor_de_outro_tipo, {"E03"}),
    "E04": (_m_e04, {"E04"}),
    "E05": (_m_e05, {"E05", "E12"}),
    "E06": (_m_e06, {"E06"}),
    "E06-derivado-sem-regra": (_m_e06_derivado_sem_regra, {"E06"}),
    "E06-pergunta-sem-texto": (_m_e06_pergunta_sem_texto, {"E06"}),
    "E07": (_m_e07, {"E07"}),
    "E08": (_m_e08, {"E08"}),
    "E09": (_m_e09, {"E09"}),
    "E10": (_m_e10, {"E10", "E11"}),
    "E11": (_m_e11, {"E11"}),
    "E12": (_m_e12, {"E12", "E05"}),
    "E13": (_m_e13, {"E13"}),
    "E14": (_m_e14, {"E14"}),
    "E14-max-em-nao-derivado": (_m_e14_max_em_nao_derivado, {"E14"}),
    "E14-max-com-cf-zero": (_m_e14_max_com_cf_zero, {"E14"}),
    "E02-tela": (_m_e02_tela, {"E02"}),
    "E21": (_m_e21, {"E21"}),
    "E21-por-modo": (_m_e21_por_modo, {"E21"}),
    "E15": (_m_e15, {"E15"}),
    "E15-minimo-e-maximo": (_m_e15_minimo_e_maximo, {"E15"}),
    "E16": (_m_e16, {"E16"}),
    "E17": (_m_e17, {"E17"}),
    "E18": (_m_e18, {"E18"}),
    "E19": (_m_e19, {"E19"}),
    "E20": (_m_e20, {"E20"}),
    "E06-cf-maximo": (_m_e06_cf_maximo_sem_regra_negativa, {"E06"}),
    "E06-negado-cf-minimo": (_m_e06_negado_cf_minimo, {"E06"}),
    "E06-negado-cf-maximo-zero": (_m_e06_negado_cf_maximo_zero, {"E06"}),
    "E06-sem-regra-positiva": (_m_e06_sem_regra_positiva, {"E06"}),
    "E06-derivado-max-negado": (_m_e06_derivado_max_negado, {"E06"}),
    "E10-por-modo-veterinario": (_m_e10_so_por_modo_veterinario, {"E10"}),
    "E10-sem-pergunta-do-produtor": (_m_e10_tela_sem_texto_do_produtor, {"E10"}),
    "E22-negativo": (_m_e22_negativo, {"E22"}),
    "E22-zero": (_m_e22_zero, {"E22"}),
    "E22-bandeira": (_m_e22_bandeira, {"E22"}),
    "E19-urgencia-monitorar": (_m_e19_urgencia_monitorar, {"E19"}),
    "E19-bandeira-derivado": (_m_e19_bandeira_derivado, {"E19"}),
    "E19-urgencia-em-doenca": (_m_e19_urgencia_em_doenca, {"E19"}),
    "E23": (_m_e23, {"E23"}),
    "E23-doenca": (_m_e23_doenca, {"E23"}),
    "E21-multipla-numerica": (_m_e21_multipla_numerica, {"E21"}),
    "E21-multipla-por-modo": (_m_e21_multipla_por_modo, {"E21"}),
    "E17-confirmacao": (_m_e17_confirmacao, {"E17"}),
    "E17-descarte": (_m_e17_descarte, {"E17"}),
    "E17-bloco-principal": (_m_e17_bloco_principal, {"E17"}),
    "E17-bloco-diferencial-negativo": (_m_e17_bloco_diferencial_negativo, {"E17"}),
    "E17-blocos-invertidos": (_m_e17_blocos_invertidos, {"E17"}),
}

MUTACOES_AVISO = {"W01": _m_w01, "W02": _m_w02, "W03": _m_w03}


def _relatorio(mutacao=None):
    dados = carregar_minima()
    if mutacao:
        mutacao(dados)
    return validar_dados(dados)


def _numeros(problemas):
    return {p.numero for p in problemas}


# --- testes ---------------------------------------------------------------

def test_base_minima_valida_sem_avisos():
    rel = _relatorio()
    assert isinstance(rel, Relatorio)
    assert rel.valida is True
    assert rel.erros == []
    assert rel.avisos == []


def test_validar_aceita_base_ja_carregada():
    rel = validar(carregar_base(carregar_minima()))
    assert rel.valida and not rel.avisos


@pytest.mark.parametrize("nome", list(MUTACOES_ERRO))
def test_codigo_erro(nome):
    mutacao, esperado = MUTACOES_ERRO[nome]
    rel = _relatorio(mutacao)
    assert _numeros(rel.erros) == esperado, [(p.numero, p.mensagem) for p in rel.erros]
    assert rel.valida is False
    assert all(p.severidade == "erro" and p.mensagem for p in rel.erros)


@pytest.mark.parametrize("numero", list(MUTACOES_AVISO))
def test_codigo_aviso(numero):
    rel = _relatorio(MUTACOES_AVISO[numero])
    assert rel.erros == [], [(p.numero, p.mensagem) for p in rel.erros]
    assert rel.valida is True
    assert numero in _numeros(rel.avisos)
    assert all(p.severidade == "aviso" for p in rel.avisos)


def test_cf_maximo_com_regra_negativa_nao_e_inalcancavel():
    rel = _relatorio(_m_sem_e06_cf_maximo_com_regra_negativa)
    assert "E06" not in _numeros(rel.erros), [(p.numero, p.mensagem) for p in rel.erros]


def test_codigos_textuais_por_numero():
    esperados = {
        "E01": "simbolo_indefinido", "E02": "id_duplicado", "E03": "valor_invalido",
        "E04": "cf_fora_do_limite", "E05": "ciclo", "E06": "regra_inalcancavel",
        "E07": "bandeira_sem_chamar_agora", "E08": "bandeira_sem_triagem",
        "E09": "doenca_sem_regra", "E10": "doenca_sem_regra_produtor",
        "E11": "cobertura_triagem", "E12": "camada", "E13": "doenca_sem_gravidade",
        "E14": "derivado_max_negativo", "E15": "limite_cf_invalido",
        "E16": "tela_sem_texto", "E17": "limiares_fora_de_ordem",
        "E18": "regra_sem_fonte", "E19": "classe_incompativel", "E20": "id_invalido",
        "E21": "tela_simbolo_invalido", "E22": "cf_urgencia_nao_positivo",
        "E23": "dominio_conceito_nao_booleano",
    }
    obtidos = {}
    for nome, (mutacao, _) in MUTACOES_ERRO.items():
        for p in _relatorio(mutacao).erros:
            obtidos[p.numero] = p.codigo
    assert {n: obtidos[n] for n in esperados} == esperados
    avisos = {}
    for mutacao in MUTACOES_AVISO.values():
        for p in _relatorio(mutacao).avisos:
            avisos[p.numero] = p.codigo
    assert avisos == {
        "W01": "simbolo_nao_usado", "W02": "regras_contraditorias", "W03": "suposicoes_pendentes",
    }


# --- alvos e mensagens ------------------------------------------------------

def test_alvo_e_mensagem_citam_os_ids():
    rel = _relatorio(_m_e01)
    (erro,) = rel.erros
    assert erro.alvo == Alvo(tipo="regra", id="R-D1-01")
    assert "R-D1-01" in erro.mensagem and "nao_existe" in erro.mensagem


def test_alvos_de_simbolo_tela_e_meta():
    assert _relatorio(_m_e13).erros[0].alvo == Alvo(tipo="simbolo", id="d1")
    assert _relatorio(_m_e16).erros[0].alvo == Alvo(tipo="tela", id="sinais")
    for erro in _relatorio(_m_e17).erros:
        assert erro.alvo == Alvo(tipo="meta", id="limiares")
    (aviso,) = _relatorio(_m_w03).avisos
    assert aviso.alvo is None
    assert "1" in aviso.mensagem


def test_ciclo_na_ordem_do_fluxo_de_dados():
    erro = next(p for p in _relatorio(_m_e05).erros if p.numero == "E05")
    # R-X: y -> x ; R-Y: x -> y  (lê -> conclui); o ciclo é achado a partir de 'x'
    assert erro.alvo == Alvo(tipo="simbolo", id="x")
    assert erro.mensagem == (
        "Ciclo: x -> y -> x. Um símbolo não pode depender, direta ou indiretamente, de si mesmo."
    )


def test_e02_cobre_simbolo_e_regra_com_mesmo_id():
    erro = _relatorio(_m_e02).erros[0]
    assert "d1" in erro.mensagem


def test_e02_cobre_dois_simbolos_com_mesmo_id():
    def duplicar(d):
        d["simbolos"].append(copy.deepcopy(_simbolo(d, "sinal_a")))
    assert _numeros(_relatorio(duplicar).erros) == {"E02"}


def test_e03_nao_dispara_para_derivado_com_cf_minimo():
    # a base mínima já tem cond. d1 com cf_minimo; derivado com cf_maximo também vale
    def m(d):
        # cf_maximo só é alcançável se alguma regra conclui 'recente' com cf negativo (E06)
        _nova_regra(d, "R-REC-02", [{"simbolo": "sinal_a"}], "recente", -0.3)
        _nova_regra(d, "R-X", [{"simbolo": "recente", "cf_maximo": 0.5}], "d1", 0.3)
    assert _relatorio(m).erros == []


def test_e06_negado_vale_quando_ha_regra_de_cf_negativo():
    def m(d):
        _nova_regra(d, "R-REC-02", [{"simbolo": "sinal_a"}], "recente", -0.3)
        _nova_regra(d, "R-X", [{"simbolo": "recente", "negado": True}], "d1", 0.4)
    assert _relatorio(m).erros == []


def test_e06_pergunta_com_campo_ficha_ou_na_triagem_e_alcancavel():
    def m(d):
        _novo_simbolo(d, "so_ficha", "ficha", campo_ficha="so_ficha")
        _nova_regra(d, "R-X", [{"simbolo": "so_ficha"}], "d1", 0.4)
    assert "E06" not in _numeros(_relatorio(m).erros)


def test_e09_nao_acumula_e10_e11():
    assert _numeros(_relatorio(_m_e09).erros) == {"E09"}


def test_e16_tela_so_de_ficha_dispensa_texto():
    def m(d):
        tela = next(t for t in d["meta"]["triagem"] if t["id"] == "dias")
        tela["texto"] = {}
    assert _relatorio(m).erros == []


def test_e17_ordem_completa():
    def m(d):
        d["meta"]["limiares"] = {"descarte": 0.5}
    assert _numeros(_relatorio(m).erros) == {"E17"}


@pytest.mark.parametrize("limiares", [
    {"premissa": 0.35},                       # premissa == hipotese_relevante
    {"hipotese_relevante": 0.6},              # == exaustao
    {"exaustao": 0.7},                        # == potencial
    {"potencial": 0.8},                       # == confirmacao
    {"bloco_diferencial": 0.5},               # == bloco_principal
    {"descarte": 0.1},                        # descarte deve ser negativo
    {"descarte": 0.0},
    {"premissa": -0.1},                       # premissa deve ser positiva
    {"premissa": 0.0},
])
def test_e17_ordem_estrita_com_zero_como_pivo(limiares):
    def m(d):
        d["meta"]["limiares"] = limiares
    rel = _relatorio(m)
    assert _numeros(rel.erros) == {"E17"}, limiares


def test_e17_limiares_padrao_validos():
    assert _relatorio().erros == []


def test_e08_basta_uma_condicao_da_triagem():
    def m(d):
        _regra(d, "R-BV-01")["se"].append({"simbolo": "pergunta_x"})  # sinal_b (triagem) + pergunta_x
    assert "E08" not in _numeros(_relatorio(m).erros)


def test_e08_aceita_derivado_de_triagem():
    def m(d):
        _regra(d, "R-BV-01")["se"] = [{"simbolo": "recente"}, {"simbolo": "pergunta_x"}]
    assert "E08" not in _numeros(_relatorio(m).erros)


def test_e08_so_condicoes_fora_da_triagem():
    def m(d):
        _regra(d, "R-BV-01")["se"] = [{"simbolo": "pergunta_x"}, {"simbolo": "exame_v"}]
    assert _numeros(_relatorio(m).erros) == {"E08"}


def test_w02_exige_mesmas_condicoes():
    def m(d):
        copia = copy.deepcopy(_regra(d, "R-D1-01"))
        copia["id"] = "R-OUTRA"
        copia["se"][0]["negado"] = True
        copia["entao"]["cf"] = -0.4
        d["regras"].append(copia)
    rel = _relatorio(m)
    assert "W02" not in _numeros(rel.avisos)


def test_ordenacao_por_numero_e_depois_por_alvo():
    def m(d):
        _m_e18(d)
        del _regra(d, "R-D1-02")["fonte"]
        _m_e04(d)
    rel = _relatorio(m)
    chaves = [(p.numero, p.alvo.id if p.alvo else "") for p in rel.erros]
    assert chaves == sorted(chaves)
    assert [p.numero for p in rel.erros] == ["E04", "E18", "E18"]


# --- resumo e dados inválidos ------------------------------------------------

def test_resumo_conta_suposicoes():
    assert _relatorio().resumo == Resumo(simbolos=10, regras=6, suposicao_a_validar=0)

    def m(d):
        del _regra(d, "R-D1-01")["status"]
        _regra(d, "R-D1-02")["status"] = "suposicao_a_validar"
    rel = _relatorio(m)
    assert rel.resumo.suposicao_a_validar == 2
    assert rel.resumo.regras == 6


def test_validar_dados_nunca_levanta():
    rel = validar_dados({})
    assert rel.valida is False and rel.erros and all(p.codigo == "estrutura" for p in rel.erros)

    rel = validar_dados({"meta": {}})
    assert rel.valida is False and _numeros(rel.erros) == {"E00"}

    dados = carregar_minima()
    _regra(dados, "R-D1-01")["entao"]["cf"] = "0,7"
    rel = validar_dados(dados)
    assert rel.valida is False
    (erro,) = rel.erros
    assert (erro.codigo, erro.numero, erro.severidade) == ("estrutura", "E00", "erro")
    assert "entao.cf" in erro.mensagem


def test_validar_dados_caminho_do_erro_na_mensagem():
    dados = carregar_minima()
    indice = next(i for i, r in enumerate(dados["regras"]) if r["id"] == "R-D1-01")
    dados["regras"][indice]["entao"]["cf"] = "0,7"
    (erro,) = validar_dados(dados).erros
    assert f"regras.{indice}.entao.cf" in erro.mensagem


def test_validar_dados_se_vazio_e_meta_ausente():
    dados = carregar_minima()
    dados["regras"][0]["se"] = []
    assert _numeros(validar_dados(dados).erros) == {"E00"}
    dados = carregar_minima()
    del dados["meta"]
    assert _numeros(validar_dados(dados).erros) == {"E00"}


@pytest.mark.parametrize("entrada", [None, [], "texto", 5, 1.5, True, [{"meta": {}}]])
def test_validar_dados_entrada_que_nao_e_dict(entrada):
    rel = validar_dados(entrada)
    assert rel.valida is False
    assert len(rel.erros) == 1
    assert (rel.erros[0].codigo, rel.erros[0].numero) == ("estrutura", "E00")
    assert rel.resumo == Resumo(simbolos=0, regras=0, suposicao_a_validar=0)


def test_validar_dados_nunca_levanta_com_dados_corrompidos():
    """Corrompe campos ao acaso (semente fixa); nenhuma entrada pode levantar."""
    azar = random.Random(20261021)
    lixo = [None, "", "x", 0, -1, 1.5, True, [], {}, ["a"], {"a": 1}, "≠", "em"]

    def folhas(obj, caminho=()):
        if isinstance(obj, dict):
            for k, v in obj.items():
                yield from folhas(v, caminho + (k,))
        elif isinstance(obj, list):
            for i, v in enumerate(obj):
                yield from folhas(v, caminho + (i,))
        yield caminho

    base = carregar_minima()
    caminhos = [c for c in folhas(base) if c]
    for _ in range(400):
        dados = copy.deepcopy(base)
        for _ in range(azar.randint(1, 3)):
            caminho = azar.choice(caminhos)
            try:
                alvo = dados
                for chave in caminho[:-1]:
                    alvo = alvo[chave]
                alvo[caminho[-1]] = azar.choice(lixo)
            except (KeyError, IndexError, TypeError):
                continue
        rel = validar_dados(dados)
        assert isinstance(rel, Relatorio)
        assert rel.valida == (not rel.erros)


def test_fixture_motor_sem_erro_estrutural():
    dados = json.loads(CAMINHO_BASE_MOTOR.read_text(encoding="utf-8"))
    rel = validar_dados(dados)
    assert "E00" not in _numeros(rel.erros)
    assert all(p.codigo != "estrutura" for p in rel.erros)


def test_problema_e_modelos_publicos():
    p = Problema(codigo="x", numero="E99", severidade="erro", alvo=None, mensagem="m")
    assert p.alvo is None


# --- validar_edicao: payload do editor (Grafo) ------------------------------------

def _payload_do_editor(mutacao=None) -> dict:
    from kb.grafo import base_para_grafo
    dados = base_para_grafo(carregar_base(carregar_minima())).model_dump(mode="json", exclude_none=True)
    if mutacao:
        mutacao(dados)
    return dados


def test_validar_edicao_payload_valido():
    from kb.validador import validar_edicao
    base, rel = validar_edicao(_payload_do_editor())
    assert base == carregar_base(carregar_minima())
    assert rel.valida and rel.erros == []


def test_validar_edicao_payload_com_erro_semantico_devolve_base_e_relatorio():
    from kb.validador import validar_edicao

    def m(dados):
        next(a for a in dados["arestas"] if a["id"] == "R-D1-03:entao")["cf"] = 1.0
    base, rel = validar_edicao(_payload_do_editor(m))
    assert base is not None
    assert rel.valida is False
    assert _numeros(rel.erros) == {"E04"}


@pytest.mark.parametrize("payload", [
    None, "texto", 42, [], {},
    {"meta": {}, "nos": "não é lista", "arestas": []},
    {"meta": {}, "nos": [], "arestas": [], "extra": 1},
])
def test_validar_edicao_payload_malformado_vira_e00(payload):
    from kb.validador import validar_edicao
    base, rel = validar_edicao(payload)
    assert base is None
    assert rel.valida is False
    assert rel.erros and {p.numero for p in rel.erros} == {"E00"}
    assert all(p.mensagem for p in rel.erros)


def test_validar_edicao_falha_de_conversao_vira_e00_em_portugues():
    from kb.validador import validar_edicao

    def m(dados):
        dados["arestas"] = [a for a in dados["arestas"] if a["id"] != "R-D1-01:entao"]
    base, rel = validar_edicao(_payload_do_editor(m))
    assert base is None and rel.valida is False
    (erro,) = rel.erros
    assert erro.numero == "E00" and "R-D1-01" in erro.mensagem and "conclusão" in erro.mensagem


def test_validar_edicao_erro_pydantic_na_conversao_vira_e00():
    from kb.validador import validar_edicao

    def m(dados):
        next(n for n in dados["nos"] if n["id"] == "sinal_a")["dados"]["tipo"] = "inexistente"
    base, rel = validar_edicao(_payload_do_editor(m))
    assert base is None
    assert {p.numero for p in rel.erros} == {"E00"}
    assert "tipo" in rel.erros[0].mensagem


def test_validar_edicao_nunca_levanta_com_lixo():
    from kb.validador import validar_edicao
    azar = random.Random(7)
    lixo = [None, "", "x", 0, -1, 1.5, True, [], {}, ["a"], {"a": 1}]
    for _ in range(200):
        dados = _payload_do_editor()
        alvo = azar.choice([dados, dados["nos"][azar.randrange(len(dados["nos"]))],
                            dados["arestas"][azar.randrange(len(dados["arestas"]))]])
        chave = azar.choice(list(alvo))
        alvo[chave] = azar.choice(lixo)
        base, rel = validar_edicao(dados)
        assert isinstance(rel, Relatorio) and rel.valida == (not rel.erros)


# --- desempenho de _produtor_ok ----------------------------------------------------

def test_cadeia_longa_de_derivados_valida_rapido():
    """Cada derivado é lido por duas regras: sem memoização, 2**40 chamadas em E10."""
    import time
    d = carregar_minima()
    n = 40
    _novo_simbolo(d, "c0", "derivado")
    _nova_regra(d, "R-C0-a", [{"simbolo": "sinal_a"}], "c0", 0.5)
    _nova_regra(d, "R-C0-b", [{"simbolo": "sinal_b"}], "c0", 0.5)
    for i in range(1, n):
        _novo_simbolo(d, f"c{i}", "derivado")
        _nova_regra(d, f"R-C{i}-a", [{"simbolo": f"c{i - 1}"}], f"c{i}", 0.5)
        _nova_regra(d, f"R-C{i}-b", [{"simbolo": f"c{i - 1}", "cf_minimo": 0.2}], f"c{i}", 0.4)
    # a doença d2 só tem regras que entram na cadeia pelo fim
    _novo_simbolo(d, "d2", "doenca", gravidade="baixa")
    _nova_regra(d, "R-D2-a", [{"simbolo": f"c{n - 1}"}], "d2", 0.3)
    _nova_regra(d, "R-D2-b", [{"simbolo": f"c{n - 1}", "cf_minimo": 0.5}], "d2", 0.2)
    inicio = time.perf_counter()
    rel = validar_dados(d)
    assert time.perf_counter() - inicio < 2
    # derivado lendo derivado é E12 (camadas estritas), mas a cadeia é obtida do produtor: sem E10
    assert "E10" not in _numeros(rel.erros)


def test_e10_derivado_em_ciclo_nao_conta_como_produtor():
    def m(d):
        _novo_simbolo(d, "x", "derivado")
        _novo_simbolo(d, "y", "derivado")
        _nova_regra(d, "R-X", [{"simbolo": "y"}], "x", 0.5)
        _nova_regra(d, "R-Y", [{"simbolo": "x"}], "y", 0.5)
        _novo_simbolo(d, "d2", "doenca", gravidade="baixa")
        _nova_regra(d, "R-D2", [{"simbolo": "x"}], "d2", 0.5)
    rel = _relatorio(m)
    assert any(p.numero == "E10" and p.alvo.id == "d2" for p in rel.erros)


def test_limite_dinamico_booleano_e_recusado():
    dados = carregar_minima()
    dados["meta"]["limite_dinamico"] = {"produtor": True, "veterinario": 25}
    rel = validar_dados(dados)
    assert not rel.valida and {p.numero for p in rel.erros} == {"E00"}
