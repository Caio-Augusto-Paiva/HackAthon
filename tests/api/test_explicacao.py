"""Parecer, "por quê?", "como?" e traço (Task 8).

Base mínima (``tests/fixtures/kb/base_minima.json``), dados fictícios, ``hoje`` = 2026-10-20. O animal com parto em
``2026-10-14`` tem 6 dias em lactação: a tela ``dias`` já vem da ficha e a primeira pergunta é a tela ``sinais``.

Na base mínima, com ``sinal_a = sim`` o ``d1`` fica em CF 0,6 (``R-D1-01``). ``pergunta_x = sim`` acrescenta ``R-D1-02``
(premissa 0,99 de ``recente``, que vem dos dias em lactação): 0,6 combinado com 0,495 dá 0,798, que o parecer mostra
como 80 %, mas fica abaixo do limiar de confirmação (0,80): a sessão encerra por ``sem_perguntas``. No modo
veterinário, ``exame_v = sim`` (``R-D1-03``) leva o ``d1`` a 0,92 e encerra por ``confirmacao``.
"""
from __future__ import annotations

from contextlib import closing

import pytest

from api.config import Configuracao
from api.db.conexao import abrir
from api.servicos.textos import AVISO_PARECER, TEXTO_URGENCIA, texto_da_regra
from kb.modelos import Condicao, Conclusao, Regra, Simbolo
from tests.api.apoio import criar_animal_teste, criar_sessao_teste, validar_contrato

SINAIS = {"valores": {"sinal_a": True, "sinal_b": False}}
SINAIS_SEM_A = {"valores": {"sinal_a": False, "sinal_b": False}}
SINAIS_COM_BANDEIRA = {"valores": {"sinal_a": False, "sinal_b": True}}
BASE = "/api/sessoes/ses_0001"


def _erro(resposta, status: int, codigo: str) -> dict:
    assert resposta.status_code == status, resposta.text
    erro = resposta.json()["erro"]
    assert erro["codigo"] == codigo
    return erro


def _consultar(config: Configuracao, sql: str, *parametros):
    with closing(abrir(config.db_path)) as conn:
        return [tuple(linha) for linha in conn.execute(sql, parametros)]


def _triagem(cliente, tela_id: str, corpo: dict, *, metodo: str = "POST", sessao_id: str = "ses_0001"):
    return cliente.request(metodo, f"/api/sessoes/{sessao_id}/triagem/{tela_id}", json=corpo)


def _pergunta(cliente, simbolo: str, valor, *, sessao_id: str = "ses_0001"):
    return cliente.post(f"/api/sessoes/{sessao_id}/respostas", json={"simbolo": simbolo, "valor": valor})


def _ler(cliente, parte: str, *, sessao_id: str = "ses_0001"):
    return cliente.get(f"/api/sessoes/{sessao_id}/{parte}")


def _corpo(cliente, parte: str, operacao: str, *, sessao_id: str = "ses_0001") -> dict:
    """GET 200 que passa pelo contrato da operação."""
    resposta = _ler(cliente, parte, sessao_id=sessao_id)
    assert resposta.status_code == 200, resposta.text
    corpo = resposta.json()
    validar_contrato(operacao, corpo)
    return corpo


def _evidencia(corpo: dict, regra_id: str) -> dict:
    return next(e for e in corpo["evidencias"] if e["regra_id"] == regra_id)


def _entrada(evidencia: dict, simbolo: str) -> dict:
    return next(e for e in evidencia["entradas"] if e["simbolo"] == simbolo)


@pytest.fixture
def sessao(cliente) -> dict:
    """``ses_0001`` do produtor, com a tela ``sinais`` pela frente."""
    animal = criar_animal_teste(cliente)
    return criar_sessao_teste(cliente, animal["id"])


@pytest.fixture
def apos_sinais(cliente, sessao) -> dict:
    """``sinais`` com ``sinal_a = sim``: o ``d1`` está em 0,6 e a próxima é a pergunta dinâmica ``pergunta_x``."""
    resposta = _triagem(cliente, "sinais", SINAIS)
    assert resposta.status_code == 200, resposta.text
    return resposta.json()


@pytest.fixture
def apos_pergunta_x(cliente, apos_sinais) -> dict:
    """``pergunta_x = sim``: a sessão encerrou (``sem_perguntas``) com o ``d1`` em 0,798."""
    resposta = _pergunta(cliente, "pergunta_x", True)
    assert resposta.status_code == 200, resposta.text
    return resposta.json()


# --- parecer ---------------------------------------------------------------------------------


def test_parecer_parcial_final_false(cliente, apos_sinais):
    assert apos_sinais["fase"] == "dinamica"
    corpo = _corpo(cliente, "parecer", "obter_parecer")
    assert corpo["final"] is False
    assert corpo["motivo_parada"] is None
    assert (corpo["sessao_id"], corpo["versao_base"], corpo["modo"]) == ("ses_0001", "v0001", "produtor")
    assert [b["id"] for b in corpo["blocos"]] == ["hipoteses_principais", "diagnostico_diferencial", "pouco_provavel"]
    doencas = [i["doenca"] for b in corpo["blocos"] for i in b["itens"]]
    assert doencas == ["d1"]  # a base mínima tem uma só doença, e ela aparece uma única vez
    assert corpo["aviso"] == AVISO_PARECER
    assert "não uma probabilidade" in corpo["aviso"]
    assert corpo["inconclusivas"] == [] and corpo["bandeiras_nao_verificadas"] == []
    assert "bandeiras" not in corpo  # já estão em urgencia.regras


def test_parecer_final_apos_confirmacao(cliente, apos_pergunta_x):
    """O nome vem do plano; na base mínima a sessão encerra por ``sem_perguntas`` (0,798 < 0,80). Ver o veterinário."""
    assert apos_pergunta_x["fase"] == "encerrada"
    corpo = _corpo(cliente, "parecer", "obter_parecer")
    assert corpo["final"] is True
    assert corpo["motivo_parada"] == "sem_perguntas"
    principais = corpo["blocos"][0]
    assert principais["id"] == "hipoteses_principais"
    d1 = next(i for i in principais["itens"] if i["doenca"] == "d1")
    assert d1["percentual"] == 80
    assert d1["cf"] == pytest.approx(0.798)
    assert d1["situacao"] == "com_evidencia"
    assert (d1["nome"], d1["gravidade"]) == ("Doença D1", "alta")


def test_parecer_final_com_confirmacao_no_modo_veterinario(cliente):
    animal = criar_animal_teste(cliente)
    criar_sessao_teste(cliente, animal["id"], "veterinario")
    assert _triagem(cliente, "sinais", SINAIS).status_code == 200
    assert _pergunta(cliente, "exame_v", True).status_code == 200  # R-D1-03: 0,8 combinado com 0,6 = 0,92
    # O especialista não para na confirmação: segue enquanto alguma doença continua aberta e com pergunta.
    while (proxima := cliente.get("/api/sessoes/ses_0001").json()["proxima"]) is not None:
        assert _pergunta(cliente, proxima["simbolo"], False).status_code == 200
    corpo = _corpo(cliente, "parecer", "obter_parecer")
    assert (corpo["modo"], corpo["final"], corpo["motivo_parada"]) == ("veterinario", True, "sem_potencial")  # nenhuma doença aberta sobrou
    d1 = corpo["blocos"][0]["itens"][0]
    assert (d1["doenca"], d1["percentual"], d1["situacao"]) == ("d1", 92, "com_evidencia")


def test_parecer_urgencia_por_regra_de_urgencia(cliente, apos_pergunta_x):
    """Sem bandeira, a urgência vem de ``R-URG-d1`` (d1 em 0,6 ou mais): origem ``regra_urgencia``."""
    corpo = _corpo(cliente, "parecer", "obter_parecer")
    assert corpo["urgencia"] == {
        "nivel": "chamar_agora",
        "origem": "regra_urgencia",
        "regras": ["R-URG-d1"],
        "texto": TEXTO_URGENCIA[("chamar_agora", "produtor")],
    }


def test_parecer_com_bandeira_urgencia_objeto(cliente, sessao):
    assert _triagem(cliente, "sinais", SINAIS_COM_BANDEIRA).status_code == 200
    acao = cliente.post(f"{BASE}/acoes/bandeira", json={"acao": "ver_parecer"})
    assert acao.status_code == 200, acao.text
    corpo = _corpo(cliente, "parecer", "obter_parecer")
    assert corpo["final"] is True
    assert corpo["urgencia"] == {
        "nivel": "chamar_agora",
        "origem": "bandeira_vermelha",
        "regras": ["R-BV-01"],
        "texto": "Chame um veterinário o mais rápido possível.",
    }

    animal = criar_animal_teste(cliente, brinco="BR-0002")
    criar_sessao_teste(cliente, animal["id"], "veterinario")
    assert _triagem(cliente, "sinais", SINAIS_COM_BANDEIRA, sessao_id="ses_0002").status_code == 200
    tecnico = _corpo(cliente, "parecer", "obter_parecer", sessao_id="ses_0002")
    assert tecnico["modo"] == "veterinario"
    assert tecnico["urgencia"]["texto"] == TEXTO_URGENCIA[("chamar_agora", "veterinario")]
    assert tecnico["urgencia"]["texto"] != corpo["urgencia"]["texto"]
    assert (tecnico["urgencia"]["origem"], tecnico["urgencia"]["regras"]) == ("bandeira_vermelha", ["R-BV-01"])


def test_parecer_sem_urgencia_tem_origem_padrao(cliente, sessao):
    """Sem bandeira e sem hipótese: ``sem_problema``, sem regras e com o texto do modo."""
    assert _triagem(cliente, "sinais", SINAIS_SEM_A).status_code == 200
    corpo = _corpo(cliente, "parecer", "obter_parecer")
    assert corpo["urgencia"]["nivel"] == "sem_problema"
    assert (corpo["urgencia"]["origem"], corpo["urgencia"]["regras"]) == ("padrao", [])
    assert corpo["urgencia"]["texto"] == TEXTO_URGENCIA[("sem_problema", "produtor")]


# --- por quê? --------------------------------------------------------------------------------


def test_porque_dinamica(cliente, apos_sinais):
    corpo = _corpo(cliente, "porque/pergunta_x", "obter_porque")
    assert corpo["simbolo"] == "pergunta_x"
    assert corpo["origem"] == "fase_dinamica"
    assert corpo["pergunta"] == "Você notou o fato X?"
    assert corpo["motivo"] == "Ajuda a separar a hipótese D1 de outras."
    assert corpo["serve_a"][0]["doenca"] == "d1"
    assert corpo["serve_a"][0]["nome"] == "Doença D1"
    assert corpo["evento_traco"].startswith("ev_")
    # o evento do traço é este mesmo
    evento = next(e for e in _corpo(cliente, "traco", "obter_traco")["eventos"] if e["id"] == corpo["evento_traco"])
    assert (evento["tipo"], evento["simbolo"], evento["motivo"]) == ("pergunta_feita", "pergunta_x", corpo["motivo"])


def test_porque_triagem(cliente, apos_sinais):
    corpo = _corpo(cliente, "porque/sinal_a", "obter_porque")
    assert corpo["origem"] == "triagem"
    assert corpo["motivo"] == "Triagem obrigatória, tela 2 de 2"
    assert corpo["pergunta"] == "O animal apresenta o sinal A?"
    assert [(s["doenca"], s["regras"]) for s in corpo["serve_a"]] == [("d1", ["R-D1-01"])]
    assert corpo["evento_traco"].startswith("ev_")
    assert corpo["serve_a"][0]["sinais"] == ["sinal A"]


def test_sinal_legivel_em_linguagem_comum():
    from api.servicos.textos import sinal_legivel
    simbolos = {
        "apetite": Simbolo(id="apetite", tipo="pergunta", nome="Apetite", dominio={"tipo": "categorico", "valores": ["normal", "reduzido", "ausente"]}),
        "decubito": Simbolo(id="decubito", tipo="pergunta", nome="Decúbito", dominio={"tipo": "booleano"}),
        "temp": Simbolo(id="temp", tipo="pergunta", nome="Temperatura retal", dominio={"tipo": "numerico", "unidade": "°C"}),
        "bhb": Simbolo(id="bhb", tipo="pergunta", nome="BHB sanguíneo", dominio={"tipo": "numerico", "unidade": "mmol/L"}),
    }
    assert sinal_legivel(Condicao(simbolo="apetite", op="em", valor=["reduzido", "ausente"]), simbolos) == "apetite reduzido ou ausente"
    assert sinal_legivel(Condicao(simbolo="decubito", op="=", valor=True), simbolos) == "decúbito"
    assert sinal_legivel(Condicao(simbolo="decubito", op="=", valor=True, negado=True), simbolos) == "ausência de decúbito"
    assert sinal_legivel(Condicao(simbolo="temp", op="≥", valor=39.5), simbolos) == "temperatura retal a partir de 39,5 °C"
    assert sinal_legivel(Condicao(simbolo="bhb", op=">", valor=1.2), simbolos) == "BHB sanguíneo acima de 1,2 mmol/L"


def test_porque_triagem_no_modo_veterinario_usa_a_pergunta_do_modo(cliente):
    animal = criar_animal_teste(cliente)
    criar_sessao_teste(cliente, animal["id"], "veterinario")
    corpo = _corpo(cliente, "porque/sinal_a", "obter_porque")
    assert corpo["pergunta"] == "Sinal A presente?"


def test_porque_sem_nenhuma_resposta_ainda_vale_para_a_tela_apresentada(cliente, sessao):
    """A tela ``sinais`` já foi apresentada ao abrir a sessão, mesmo sem resposta."""
    assert _corpo(cliente, "porque/sinal_b", "obter_porque")["origem"] == "triagem"


def test_porque_de_pergunta_nao_apresentada_404(cliente, apos_sinais):
    _erro(_ler(cliente, "porque/exame_v"), 404, "nao_encontrado")  # só existe no modo veterinário
    _erro(_ler(cliente, "porque/inexistente"), 404, "nao_encontrado")
    _erro(_ler(cliente, "porque/d1"), 404, "nao_encontrado")  # existe na base, mas não é pergunta
    _erro(_ler(cliente, "porque/dias_em_lactacao"), 404, "nao_encontrado")  # veio da ficha: ninguém perguntou


def test_porque_sobrevive_a_correcao(cliente, apos_sinais):
    """O motivo e o ``serve_a`` são os gravados na primeira apresentação (decisão 2 da 4.9), mesmo depois de corrigir."""
    antes = _corpo(cliente, "porque/pergunta_x", "obter_porque")
    assert antes["serve_a"][0]["cf_atual"] == pytest.approx(0.6)
    correcao = _triagem(cliente, "sinais", SINAIS_SEM_A, metodo="PUT")
    assert correcao.status_code == 200, correcao.text
    assert _corpo(cliente, "como/d1", "obter_como")["cf"] == 0.0  # o quadro mudou: sem o sinal A a regra deixa de disparar
    depois = _corpo(cliente, "porque/pergunta_x", "obter_porque")
    assert depois == antes


def test_porque_de_sessao_inexistente_404(cliente):
    _erro(_ler(cliente, "porque/sinal_a", sessao_id="ses_9999"), 404, "nao_encontrado")


# --- como? -----------------------------------------------------------------------------------


def test_como_doenca(cliente, apos_pergunta_x):
    corpo = _corpo(cliente, "como/d1", "obter_como")
    assert (corpo["simbolo"], corpo["nome"]) == ("d1", "Doença D1")
    assert corpo["cf"] == pytest.approx(0.798)  # 0,495 (R-D1-02) combinado com 0,6 (R-D1-01); o motor não arredonda
    assert corpo["percentual"] == 80
    # a combinação segue a ordem em que o motor disparou as regras
    assert [c["apos_regra"] for c in corpo["combinacao"]] == ["R-D1-02", "R-D1-01"]
    assert [(c["antes"], c["depois"]) for c in corpo["combinacao"]] == [(0.0, 0.495), (0.495, 0.798)]
    assert sorted(e["regra_id"] for e in corpo["evidencias"]) == ["R-D1-01", "R-D1-02"]
    r01 = _evidencia(corpo, "R-D1-01")
    assert (r01["premissa"], r01["cf_regra"], r01["cf_saida"]) == (1.0, 0.6, 0.6)
    assert (r01["fonte"], r01["status"]) == ("fixture de software", "validada")
    assert r01["entradas"][0]["simbolo"] == "sinal_a"
    assert r01["entradas"][0]["origem"] == "resposta"
    assert r01["entradas"][0]["tela_id"] == "sinais"
    assert r01["entradas"][0]["valor"] is True
    # linguagem comum para a tela: condições da regra como frase e o nome legível de cada fato
    assert r01["frase"] == "sinal A"
    assert r01["entradas"][0]["nome"] == "Sinal A"


def test_como_traz_o_texto_legivel_de_cada_regra(cliente, apos_pergunta_x):
    corpo = _corpo(cliente, "como/d1", "obter_como")
    assert _evidencia(corpo, "R-D1-01")["texto"] == "R-D1-01: SE Sinal A = sim ENTÃO Doença D1 (CF 0,6)"
    assert (
        _evidencia(corpo, "R-D1-02")["texto"]
        == "R-D1-02: SE Lactação recente = sim E Pergunta X = sim ENTÃO Doença D1 (CF 0,5)"
    )
    urgencia = _corpo(cliente, "como/chamar_agora", "obter_como")
    assert (
        _evidencia(urgencia, "R-URG-d1")["texto"]
        == "R-URG-d1: SE Doença D1 com CF ≥ 0,5 ENTÃO Chamar o veterinário agora (CF 0,9)"
    )


def test_como_derivado_traz_evidencias_aninhadas(cliente, apos_pergunta_x):
    d1 = _corpo(cliente, "como/d1", "obter_como")
    via_recente = _entrada(_evidencia(d1, "R-D1-02"), "recente")
    assert via_recente["origem"] == "regra"
    assert via_recente["evidencias"][0]["regra_id"] == "R-REC-01"
    assert via_recente["evidencias"][0]["texto"] == "R-REC-01: SE Dias em lactação ≤ 21 ENTÃO Lactação recente (CF 0,99)"
    # as aninhadas são as do "como?" do próprio derivado
    recente = _corpo(cliente, "como/recente", "obter_como")
    assert (recente["simbolo"], recente["nome"], recente["cf"]) == ("recente", "Lactação recente", pytest.approx(0.99))
    assert via_recente["evidencias"] == recente["evidencias"]
    # a ficha cadastrada à mão continua "ficha"
    dias = _entrada(recente["evidencias"][0], "dias_em_lactacao")
    assert (dias["origem"], dias["valor"], dias["tela_id"]) == ("ficha", 6.0, None)
    # e quem foi respondido continua "resposta"
    assert _entrada(_evidencia(d1, "R-D1-02"), "pergunta_x")["origem"] == "resposta"


def test_como_urgencia_percorre_ate_as_respostas(cliente, apos_pergunta_x):
    corpo = _corpo(cliente, "como/chamar_agora", "obter_como")
    entrada = _entrada(_evidencia(corpo, "R-URG-d1"), "d1")
    assert entrada["origem"] == "regra"
    assert sorted(e["regra_id"] for e in entrada["evidencias"]) == ["R-D1-01", "R-D1-02"]
    # dois níveis abaixo: o derivado ``recente`` e os dias em lactação
    via_recente = _entrada(next(e for e in entrada["evidencias"] if e["regra_id"] == "R-D1-02"), "recente")
    assert _entrada(via_recente["evidencias"][0], "dias_em_lactacao")["origem"] == "ficha"


def _importar_animal(cliente) -> dict:
    csv = "brinco,nome,data_ultimo_parto\nBR-0007,Estrela,2026-10-14\n".encode()
    resposta = cliente.post("/api/animais/importacao", files={"arquivo": ("prontuario.csv", csv, "text/csv")})
    assert resposta.status_code == 200, resposta.text
    assert [c["brinco"] for c in resposta.json()["criados"]] == ["BR-0007"]
    animal = cliente.get("/api/animais/an_001").json()
    assert animal["origens"] == {"data_ultimo_parto": "importacao"}
    return animal


def test_como_origem_importacao(cliente):
    animal = _importar_animal(cliente)
    criar_sessao_teste(cliente, animal["id"])
    assert _triagem(cliente, "sinais", SINAIS).status_code == 200
    assert _pergunta(cliente, "pergunta_x", True).status_code == 200
    recente = _corpo(cliente, "como/recente", "obter_como")
    dias = _entrada(recente["evidencias"][0], "dias_em_lactacao")
    assert dias["origem"] == "importacao"  # o motor só conhece "ficha"; a API sabe que veio do prontuário
    # recursivo: o mesmo vale no "como?" de quem usa o derivado
    d1 = _corpo(cliente, "como/d1", "obter_como")
    aninhado = _entrada(_entrada(_evidencia(d1, "R-D1-02"), "recente")["evidencias"][0], "dias_em_lactacao")
    assert aninhado["origem"] == "importacao"
    # o que foi respondido nunca vira importação
    assert _entrada(_evidencia(d1, "R-D1-01"), "sinal_a")["origem"] == "resposta"


def test_como_ficha_corrigida_pela_tela_deixa_de_ser_importacao(cliente):
    """Depois do PUT na tela só de ficha, o fato é uma resposta do usuário (``origem = resposta``) e não se reescreve."""
    animal = _importar_animal(cliente)
    criar_sessao_teste(cliente, animal["id"])
    assert _triagem(cliente, "sinais", SINAIS).status_code == 200
    antes = _entrada(_corpo(cliente, "como/recente", "obter_como")["evidencias"][0], "dias_em_lactacao")
    assert (antes["origem"], antes["valor"]) == ("importacao", 6.0)
    correcao = _triagem(cliente, "dias", {"valores": {"dias_em_lactacao": 10}}, metodo="PUT")
    assert correcao.status_code == 200, correcao.text
    depois = _entrada(_corpo(cliente, "como/recente", "obter_como")["evidencias"][0], "dias_em_lactacao")
    assert (depois["origem"], depois["valor"], depois["tela_id"]) == ("resposta", 10.0, "dias")


def _origens_do_traco(corpo: dict, simbolo: str) -> set[str]:
    """As origens do ``simbolo`` no traço: nos ``fato_adicionado`` e nas entradas de cada ``regra_disparada``."""
    origens = {e["origem"] for e in corpo["eventos"] if e["tipo"] == "fato_adicionado" and e["simbolo"] == simbolo}
    for evento in corpo["eventos"]:
        if evento["tipo"] == "regra_disparada":
            origens |= {e["origem"] for e in evento["entradas"] if e["simbolo"] == simbolo}
    return origens


def test_traco_origem_importacao_concorda_com_o_como(cliente):
    animal = _importar_animal(cliente)
    criar_sessao_teste(cliente, animal["id"])
    assert _triagem(cliente, "sinais", SINAIS).status_code == 200
    assert _pergunta(cliente, "pergunta_x", True).status_code == 200
    traco = _corpo(cliente, "traco", "obter_traco")
    assert _origens_do_traco(traco, "dias_em_lactacao") == {"importacao"}  # no fato e na entrada da R-REC-01
    como = _corpo(cliente, "como/recente", "obter_como")
    assert _entrada(como["evidencias"][0], "dias_em_lactacao")["origem"] == "importacao"
    assert _origens_do_traco(traco, "sinal_a") == {"resposta"}  # o que foi respondido nunca vira importação


def test_traco_ficha_a_mao_continua_ficha_e_corrigida_vira_resposta(cliente, sessao):
    assert _triagem(cliente, "sinais", SINAIS).status_code == 200
    assert _origens_do_traco(_corpo(cliente, "traco", "obter_traco"), "dias_em_lactacao") == {"ficha"}
    animal = _importar_animal_com_brinco(cliente)
    criar_sessao_teste(cliente, animal["id"])
    assert _triagem(cliente, "sinais", SINAIS, sessao_id="ses_0002").status_code == 200
    correcao = _triagem(cliente, "dias", {"valores": {"dias_em_lactacao": 10}}, metodo="PUT", sessao_id="ses_0002")
    assert correcao.status_code == 200, correcao.text
    traco = _corpo(cliente, "traco", "obter_traco", sessao_id="ses_0002")
    assert _origens_do_traco(traco, "dias_em_lactacao") == {"resposta"}


def _importar_animal_com_brinco(cliente) -> dict:
    csv = "brinco,nome,data_ultimo_parto\nBR-0008,Aurora,2026-10-14\n".encode()
    resposta = cliente.post("/api/animais/importacao", files={"arquivo": ("prontuario.csv", csv, "text/csv")})
    assert resposta.status_code == 200, resposta.text
    return cliente.get("/api/animais?busca=BR-0008").json()["itens"][0]


def test_como_de_simbolo_sem_conclusao_devolve_cf_zero_e_nada_a_explicar(cliente, apos_sinais):
    corpo = _corpo(cliente, "como/recente", "obter_como")  # dias_em_lactacao = 6: R-REC-01 já disparou
    assert corpo["cf"] == pytest.approx(0.99)
    urgencia = _corpo(cliente, "como/observar", "obter_como")  # nenhuma regra concluiu "observar"
    assert (urgencia["cf"], urgencia["percentual"], urgencia["combinacao"], urgencia["evidencias"]) == (0.0, 0, [], [])


def test_como_simbolo_de_pergunta_422(cliente, apos_sinais):
    erro = _erro(_ler(cliente, "como/sinal_a"), 422, "simbolo_invalido")
    assert "sinal_a" in erro["mensagem"]
    _erro(_ler(cliente, "como/dias_em_lactacao"), 422, "simbolo_invalido")  # símbolo de ficha também não se explica
    _erro(_ler(cliente, "como/inexistente"), 404, "nao_encontrado")


def test_como_de_sessao_inexistente_404(cliente):
    _erro(_ler(cliente, "como/d1", sessao_id="ses_9999"), 404, "nao_encontrado")


# --- traço -----------------------------------------------------------------------------------


def test_traco_tem_quatro_tipos(cliente, apos_pergunta_x):
    corpo = _corpo(cliente, "traco", "obter_traco")
    eventos = corpo["eventos"]
    tipos = {e["tipo"] for e in eventos}
    assert tipos <= {"pergunta_feita", "fato_adicionado", "regra_disparada", "cf_combinado"}
    assert tipos == {"pergunta_feita", "fato_adicionado", "regra_disparada", "cf_combinado"}
    assert [e["id"] for e in eventos] == [f"ev_{n:04d}" for n in range(1, len(eventos) + 1)]  # ids em ordem, sem furo
    disparadas = {e["regra_id"] for e in eventos if e["tipo"] == "regra_disparada"}
    assert {"R-REC-01", "R-D1-01", "R-D1-02", "R-URG-d1"} <= disparadas


def test_traco_de_sessao_inexistente_404(cliente):
    _erro(_ler(cliente, "traco", sessao_id="ses_9999"), 404, "nao_encontrado")


def test_parecer_de_sessao_inexistente_404(cliente):
    _erro(_ler(cliente, "parecer", sessao_id="ses_9999"), 404, "nao_encontrado")


# --- leitura pura ----------------------------------------------------------------------------


def test_explicacao_nao_sobe_revisao(cliente, config, apos_pergunta_x):
    revisao = apos_pergunta_x["revisao"]
    assert cliente.get(BASE).json()["revisao"] == revisao
    for parte in ("parecer", "porque/sinal_a", "porque/pergunta_x", "como/d1", "como/recente", "traco"):
        assert _ler(cliente, parte).status_code == 200, parte
    assert cliente.get(BASE).json()["revisao"] == revisao
    assert _consultar(config, "SELECT revisao FROM sessoes") == [(revisao,)]


def test_explicacao_nao_muda_o_estado_gravado(cliente, config, apos_sinais):
    estado = cliente.get(BASE).json()
    gravado = _consultar(config, "SELECT snapshot_json, fase, modo, revisao FROM sessoes")
    for parte in ("parecer", "porque/pergunta_x", "como/d1", "traco"):
        assert _ler(cliente, parte).status_code == 200, parte
    assert cliente.get(BASE).json() == estado
    assert _consultar(config, "SELECT snapshot_json, fase, modo, revisao FROM sessoes") == gravado


# --- texto da regra (puro) -------------------------------------------------------------------


def _simbolo(id: str, nome: str, tipo: str = "pergunta", dominio: dict | None = None) -> Simbolo:
    return Simbolo.model_validate({"id": id, "tipo": tipo, "nome": nome, "dominio": dominio or {"tipo": "booleano"}})


SIMBOLOS = {
    s.id: s
    for s in (
        _simbolo("temperatura", "Temperatura", dominio={"tipo": "numerico", "unidade": "°C"}),
        _simbolo("raca", "Raça", dominio={"tipo": "categorico", "valores": ["europeia", "zebuina"]}),
        _simbolo("sinal_a", "Sinal A"),
        _simbolo("d1", "Doença D1", "doenca"),
    )
}


def _regra(se: list[dict], conclusao: str = "d1", cf: float = 0.6, id: str = "R-1") -> Regra:
    return Regra(id=id, se=[Condicao(**c) for c in se], entao=Conclusao(simbolo=conclusao, cf=cf))


@pytest.mark.parametrize(
    "se, cf, esperado",
    [
        ([{"simbolo": "sinal_a"}], 0.6, "R-1: SE Sinal A = sim ENTÃO Doença D1 (CF 0,6)"),
        ([{"simbolo": "sinal_a", "valor": False}], 0.6, "R-1: SE Sinal A = não ENTÃO Doença D1 (CF 0,6)"),
        ([{"simbolo": "sinal_a", "negado": True}], -0.35, "R-1: SE NÃO (Sinal A = sim) ENTÃO Doença D1 (CF -0,35)"),
        ([{"simbolo": "temperatura", "op": ">=", "valor": 39.5}], 0.99, "R-1: SE Temperatura ≥ 39,5 ENTÃO Doença D1 (CF 0,99)"),
        ([{"simbolo": "temperatura", "op": "<", "valor": 21}], 1, "R-1: SE Temperatura < 21 ENTÃO Doença D1 (CF 1)"),
        ([{"simbolo": "raca", "op": "em", "valor": ["europeia", "zebuina"]}], 0.2,
         "R-1: SE Raça em {europeia, zebuina} ENTÃO Doença D1 (CF 0,2)"),
        ([{"simbolo": "raca", "op": "!=", "valor": "zebuina"}, {"simbolo": "sinal_a"}], 0.5,
         "R-1: SE Raça ≠ zebuina E Sinal A = sim ENTÃO Doença D1 (CF 0,5)"),
        ([{"simbolo": "d1", "cf_minimo": 0.5}], 0.9, "R-1: SE Doença D1 com CF ≥ 0,5 ENTÃO Doença D1 (CF 0,9)"),
        ([{"simbolo": "d1", "cf_maximo": -0.2}], 0.9, "R-1: SE Doença D1 com CF ≤ -0,2 ENTÃO Doença D1 (CF 0,9)"),
        ([{"simbolo": "fantasma"}], 0.1, "R-1: SE fantasma = sim ENTÃO Doença D1 (CF 0,1)"),  # sem nome: usa o id
    ],
)
def test_texto_da_regra(se, cf, esperado):
    assert texto_da_regra(_regra(se, cf=cf), SIMBOLOS) == esperado
