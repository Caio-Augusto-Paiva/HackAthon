"""Responder triagem e perguntas dinâmicas, com correção (Task 6).

Base mínima (``tests/fixtures/kb/base_minima.json``), dados fictícios, ``hoje`` = 2026-10-20. O animal com parto em
``2026-10-14`` tem 6 dias em lactação: a tela ``dias`` já vem da ficha e a primeira pergunta é a tela ``sinais``.
"""
from __future__ import annotations

from contextlib import closing, contextmanager

import pytest
from fastapi.testclient import TestClient

from api.config import Configuracao
from api.contexto import Contexto
from api.db.conexao import abrir
from api.main import criar_app
from api.servicos.sessao_motor import aplicar, carregar
from kb.carregador import Repositorio
from tests.api.apoio import criar_animal_teste, criar_sessao_teste, validar_contrato

SINAIS = {"valores": {"sinal_a": True, "sinal_b": False}}


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


def _pergunta(cliente, simbolo: str, valor=None, *, nao_sei: bool = False, sessao_id: str = "ses_0001"):
    corpo = {"simbolo": simbolo, **({"nao_sei": True} if nao_sei else {"valor": valor})}
    return cliente.post(f"/api/sessoes/{sessao_id}/respostas", json=corpo)


def _corrigir_pergunta(cliente, simbolo: str, corpo: dict, *, sessao_id: str = "ses_0001"):
    return cliente.put(f"/api/sessoes/{sessao_id}/respostas/{simbolo}", json=corpo)


@pytest.fixture
def sessao(cliente) -> dict:
    """``ses_0001`` do animal de 6 dias em lactação (parto 2026-10-14): a próxima é a tela ``sinais``."""
    animal = criar_animal_teste(cliente)
    return criar_sessao_teste(cliente, animal["id"])


@pytest.fixture
def sessao_dinamica(cliente, sessao) -> dict:
    """A mesma sessão com ``sinais`` respondida: a próxima é a pergunta dinâmica ``pergunta_x``."""
    resposta = _triagem(cliente, "sinais", SINAIS)
    assert resposta.status_code == 200, resposta.text
    return resposta.json()


# --- triagem: POST ---------------------------------------------------------------------------


def test_triagem_multipla_avanca_para_dinamica(cliente, sessao):
    resposta = _triagem(cliente, "sinais", SINAIS)
    assert resposta.status_code == 200, resposta.text
    corpo = resposta.json()
    validar_contrato("responder_triagem", corpo)
    assert corpo["revisao"] == 2
    assert corpo["fase"] == "dinamica"
    assert corpo["proxima"]["tipo"] == "pergunta"
    assert corpo["proxima"]["simbolo"] == "pergunta_x"
    assert corpo["progresso"]["triagem_respondidas"] == 2
    assert corpo["progresso"]["dinamicas_feitas"] == 0
    assert cliente.get("/api/sessoes/ses_0001").json() == corpo  # o que o POST devolveu é o que ficou gravado


def test_triagem_multipla_aceita_so_as_marcadas(cliente, config, sessao):
    """O mapa pode trazer só as opções marcadas: as demais da tela contam como não marcadas."""
    corpo = _triagem(cliente, "sinais", {"valores": {"sinal_a": True}}).json()
    assert corpo["progresso"]["triagem_respondidas"] == 2
    respostas = dict(_consultar(config, "SELECT simbolo, valor_json FROM respostas"))
    assert (respostas["sinal_a"], respostas["sinal_b"]) == ("true", "false")


def test_triagem_nao_sei(cliente, config, sessao):
    resposta = _triagem(cliente, "sinais", {"nao_sei": True})
    assert resposta.status_code == 200, resposta.text
    corpo = resposta.json()
    validar_contrato("responder_triagem", corpo)
    assert corpo["urgencia"]["nivel"] == "sem_problema"
    assert corpo["progresso"]["triagem_respondidas"] == 2
    nao_sei = dict(_consultar(config, "SELECT simbolo, nao_sei FROM respostas WHERE tela_id = 'sinais'"))
    assert nao_sei == {"sinal_a": 1, "sinal_b": 1}


def test_triagem_unica_numerica_sem_ficha(cliente, config):
    animal = criar_animal_teste(cliente, parto=None)
    criar_sessao_teste(cliente, animal["id"])
    resposta = _triagem(cliente, "dias", {"valores": {"dias_em_lactacao": 10}})  # o JSON 10 chega como 10.0
    assert resposta.status_code == 200, resposta.text
    corpo = resposta.json()
    validar_contrato("responder_triagem", corpo)
    assert corpo["proxima"]["tela_id"] == "sinais"
    assert _consultar(config, "SELECT valor_json, tela_id FROM respostas WHERE simbolo = 'dias_em_lactacao'") == [
        ("10", "dias")
    ]


def test_post_em_tela_respondida_409(cliente, sessao):
    assert _triagem(cliente, "sinais", SINAIS).status_code == 200
    antes = cliente.get("/api/sessoes/ses_0001").json()
    _erro(_triagem(cliente, "sinais", SINAIS), 409, "ja_respondida")
    assert cliente.get("/api/sessoes/ses_0001").json() == antes
    assert antes["revisao"] == 2


def test_post_em_tela_so_de_ficha_409(cliente, sessao):
    """A tela ``dias`` veio inteira da ficha: contar como respondida, não deixar o POST sobrescrever."""
    _erro(_triagem(cliente, "dias", {"valores": {"dias_em_lactacao": 30}}), 409, "ja_respondida")
    assert cliente.get("/api/sessoes/ses_0001").json()["revisao"] == 1


def test_triagem_fora_de_ordem_422(cliente):
    animal = criar_animal_teste(cliente, parto=None)  # sem ficha: a tela ``dias`` está pendente
    criar_sessao_teste(cliente, animal["id"])
    antes = cliente.get("/api/sessoes/ses_0001").json()
    _erro(_triagem(cliente, "sinais", SINAIS), 422, "resposta_invalida")
    assert cliente.get("/api/sessoes/ses_0001").json() == antes


# --- triagem: PUT ----------------------------------------------------------------------------


def test_put_em_tela_nao_respondida_409(cliente, sessao):
    _erro(_triagem(cliente, "sinais", SINAIS, metodo="PUT"), 409, "nao_respondida")
    assert cliente.get("/api/sessoes/ses_0001").json()["revisao"] == 1


def test_put_corrige_sem_perder_respostas(cliente, config, sessao):
    primeira = _triagem(cliente, "sinais", {"valores": {"sinal_a": True, "sinal_b": False}}).json()
    assert primeira["urgencia"]["nivel"] == "chamar_agora"
    resposta = _triagem(cliente, "sinais", {"valores": {"sinal_a": False, "sinal_b": False}}, metodo="PUT")
    assert resposta.status_code == 200, resposta.text
    corpo = resposta.json()
    validar_contrato("corrigir_triagem", corpo)
    assert corpo["revisao"] == 3
    assert corpo["progresso"]["triagem_respondidas"] == primeira["progresso"]["triagem_respondidas"] == 2
    assert corpo["urgencia"]["nivel"] != "chamar_agora"  # a hipótese de sinal_a sumiu com a correção
    assert _consultar(config, "SELECT valor_json FROM respostas WHERE simbolo = 'sinal_a'") == [("false",)]
    assert _consultar(config, "SELECT valor_json FROM respostas WHERE simbolo = 'dias_em_lactacao'") == [("6",)]
    assert cliente.get("/api/sessoes/ses_0001").json() == corpo


def test_put_em_tela_so_de_ficha_corrige(cliente, config, sessao):
    """A tela ``dias`` só tem símbolo da ficha: ela conta como respondida e o usuário pode corrigi-la."""
    resposta = _triagem(cliente, "dias", {"valores": {"dias_em_lactacao": 30}}, metodo="PUT")
    assert resposta.status_code == 200, resposta.text
    corpo = resposta.json()
    validar_contrato("corrigir_triagem", corpo)
    assert corpo["revisao"] == 2
    assert corpo["progresso"]["triagem_respondidas"] == 1
    assert corpo["proxima"]["tela_id"] == "sinais"
    assert _consultar(config, "SELECT valor_json, origem FROM respostas WHERE simbolo = 'dias_em_lactacao'") == [
        ("30", "resposta")
    ]


# --- triagem: 404 e respostas recusadas ------------------------------------------------------


@pytest.mark.parametrize("metodo", ["POST", "PUT"])
def test_tela_inexistente_404(cliente, sessao, metodo):
    _erro(_triagem(cliente, "nao_existe", SINAIS, metodo=metodo), 404, "nao_encontrado")


@pytest.mark.parametrize("corpo", [
    {"valores": {"sinal_z": True}},  # símbolo que não existe
    {"valores": {"sinal_z": False}},  # fora da tela, mesmo desmarcado, é erro
    {"valores": {"dias_em_lactacao": True}},  # existe, mas é de outra tela
    {"valores": {"sinal_a": "sim"}},  # texto não é booleano (o motor aceitaria "sim")
    {"valores": {"sinal_a": 1}},  # o JSON 1 chega como 1.0
    {"valores": {"sinal_a": 0}},
], ids=["simbolo_inexistente", "inexistente_desmarcado", "outra_tela", "texto_sim", "numero_1", "numero_0"])
def test_multipla_invalida_nao_altera_estado(cliente, config, sessao, corpo):
    antes = cliente.get("/api/sessoes/ses_0001").json()
    linhas = _consultar(config, "SELECT simbolo, valor_json FROM respostas ORDER BY simbolo")
    _erro(_triagem(cliente, "sinais", corpo), 422, "resposta_invalida")
    assert cliente.get("/api/sessoes/ses_0001").json() == antes  # revisão incluída
    assert _consultar(config, "SELECT simbolo, valor_json FROM respostas ORDER BY simbolo") == linhas
    assert _consultar(config, "SELECT revisao FROM sessoes") == [(1,)]


def test_multipla_com_surrogate_solto_na_chave_422(cliente, sessao):
    """O JSON aceita ``\\ud800``; a mensagem de erro não pode repeti-lo (viraria 500 ao codificar a resposta)."""
    resposta = cliente.post(
        "/api/sessoes/ses_0001/triagem/sinais",
        content=b'{"valores": {"\\ud800": true}}',
        headers={"content-type": "application/json"},
    )
    _erro(resposta, 422, "resposta_invalida")


@pytest.mark.parametrize("valor", ["abc", "1e1", True, 401, -1])
def test_triagem_numerica_fora_do_dominio_422(cliente, config, valor):
    animal = criar_animal_teste(cliente, parto=None)
    criar_sessao_teste(cliente, animal["id"])
    _erro(_triagem(cliente, "dias", {"valores": {"dias_em_lactacao": valor}}), 422, "resposta_invalida")
    assert _consultar(config, "SELECT COUNT(*) FROM respostas") == [(0,)]
    assert cliente.get("/api/sessoes/ses_0001").json()["revisao"] == 1


def test_triagem_unica_com_chaves_trocadas_422(cliente):
    animal = criar_animal_teste(cliente, parto=None)
    criar_sessao_teste(cliente, animal["id"])
    _erro(_triagem(cliente, "dias", {"valores": {"sinal_a": 10}}), 422, "resposta_invalida")


# --- perguntas dinâmicas ---------------------------------------------------------------------


def test_resposta_dinamica_e_correcao(cliente, config, sessao_dinamica):
    resposta = _pergunta(cliente, "pergunta_x", True)
    assert resposta.status_code == 200, resposta.text
    corpo = resposta.json()
    validar_contrato("responder_pergunta", corpo)
    assert corpo["progresso"]["dinamicas_feitas"] == 1
    assert corpo["revisao"] == 3
    assert _consultar(config, "SELECT valor_json, tela_id FROM respostas WHERE simbolo = 'pergunta_x'") == [
        ("true", None)
    ]

    _erro(_pergunta(cliente, "pergunta_x", True), 409, "ja_respondida")
    assert cliente.get("/api/sessoes/ses_0001").json()["revisao"] == 3

    corrigida = _corrigir_pergunta(cliente, "pergunta_x", {"valor": False})
    assert corrigida.status_code == 200, corrigida.text
    validar_contrato("corrigir_resposta", corrigida.json())
    assert corrigida.json()["revisao"] == 4
    assert corrigida.json()["progresso"]["dinamicas_feitas"] == 1
    assert _consultar(config, "SELECT valor_json FROM respostas WHERE simbolo = 'pergunta_x'") == [("false",)]

    _erro(_corrigir_pergunta(cliente, "exame_v", {"valor": True}), 409, "nao_respondida")
    assert cliente.get("/api/sessoes/ses_0001").json() == corrigida.json()


def test_resposta_dinamica_nao_sei(cliente, config, sessao_dinamica):
    resposta = _pergunta(cliente, "pergunta_x", nao_sei=True)
    assert resposta.status_code == 200, resposta.text
    validar_contrato("responder_pergunta", resposta.json())
    assert resposta.json()["progresso"]["dinamicas_feitas"] == 1
    assert _consultar(config, "SELECT nao_sei FROM respostas WHERE simbolo = 'pergunta_x'") == [(1,)]
    corrigida = _corrigir_pergunta(cliente, "pergunta_x", {"nao_sei": True})
    assert corrigida.status_code == 200, corrigida.text
    validar_contrato("corrigir_resposta", corrigida.json())


def test_pergunta_do_triagem_nao_e_dinamica(cliente, sessao_dinamica):
    """``sinal_a`` já tem resposta (da triagem): o POST dinâmico é ``ja_respondida`` e o PUT dinâmico não a corrige."""
    _erro(_pergunta(cliente, "sinal_a", True), 409, "ja_respondida")
    _erro(_corrigir_pergunta(cliente, "sinal_a", {"valor": False}), 409, "nao_respondida")
    assert cliente.get("/api/sessoes/ses_0001").json() == sessao_dinamica


def test_pergunta_do_veterinario_no_produtor_422(cliente, sessao_dinamica):
    _erro(_pergunta(cliente, "exame_v", True), 422, "resposta_invalida")
    assert cliente.get("/api/sessoes/ses_0001").json() == sessao_dinamica


def test_pergunta_fora_de_hora_no_inicio_422(cliente, sessao):
    """A triagem ainda não acabou: a pergunta dinâmica não é a próxima."""
    _erro(_pergunta(cliente, "pergunta_x", True), 422, "resposta_invalida")


def test_simbolo_inexistente_404(cliente, sessao_dinamica):
    _erro(_pergunta(cliente, "nao_existe", True), 404, "nao_encontrado")
    _erro(_corrigir_pergunta(cliente, "nao_existe", {"valor": True}), 404, "nao_encontrado")


@pytest.mark.parametrize("valor", ["abc", "sim", 1, 0, 1.5], ids=["texto", "texto_sim", "numero_1", "numero_0", "decimal"])
def test_valor_fora_do_dominio_422(cliente, config, sessao_dinamica, valor):
    """Símbolo booleano só aceita ``true``/``false``: nem texto (o motor aceitaria "sim"), nem o JSON 1 virado 1.0."""
    _erro(_pergunta(cliente, "pergunta_x", valor), 422, "resposta_invalida")
    assert cliente.get("/api/sessoes/ses_0001").json() == sessao_dinamica
    assert _consultar(config, "SELECT COUNT(*) FROM respostas WHERE simbolo = 'pergunta_x'") == [(0,)]


def test_correcao_com_valor_fora_do_dominio_422(cliente, sessao_dinamica):
    assert _pergunta(cliente, "pergunta_x", True).status_code == 200
    antes = cliente.get("/api/sessoes/ses_0001").json()
    _erro(_corrigir_pergunta(cliente, "pergunta_x", {"valor": "sim"}), 422, "resposta_invalida")
    _erro(_corrigir_pergunta(cliente, "pergunta_x", {"valor": 1}), 422, "resposta_invalida")
    assert cliente.get("/api/sessoes/ses_0001").json() == antes


# --- corpo, sessão inexistente ---------------------------------------------------------------


@pytest.mark.parametrize("corpo", [
    {"valores": {"sinal_a": True, "sinal_b": False}, "cf": 0.9},
    {"valores": {"sinal_a": True, "sinal_b": False}, "nao_sei": True},
    {},
    {"cf": 0.9, "nao_sei": True},
], ids=["cf_no_corpo", "valores_e_nao_sei", "vazio", "so_cf"])
def test_triagem_corpo_invalido_422(cliente, sessao, corpo):
    _erro(_triagem(cliente, "sinais", corpo), 422, "entrada_invalida")
    _erro(_triagem(cliente, "sinais", corpo, metodo="PUT"), 422, "entrada_invalida")
    assert cliente.get("/api/sessoes/ses_0001").json()["revisao"] == 1


def test_cliente_nao_envia_cf(cliente, sessao_dinamica):
    """Nenhuma rota de resposta aceita ``cf``: o servidor é quem mapeia sim, não e não sei em certeza."""
    _erro(cliente.post("/api/sessoes/ses_0001/respostas", json={"simbolo": "pergunta_x", "valor": True, "cf": 0.9}),
          422, "entrada_invalida")
    _erro(_corrigir_pergunta(cliente, "pergunta_x", {"valor": True, "cf": 0.9}), 422, "entrada_invalida")
    _erro(cliente.post("/api/sessoes/ses_0001/respostas", json={"simbolo": "pergunta_x"}), 422, "entrada_invalida")
    assert cliente.get("/api/sessoes/ses_0001").json() == sessao_dinamica


def test_sessao_inexistente_404(cliente):
    _erro(_triagem(cliente, "sinais", SINAIS, sessao_id="ses_9999"), 404, "nao_encontrado")
    _erro(_triagem(cliente, "sinais", SINAIS, metodo="PUT", sessao_id="ses_9999"), 404, "nao_encontrado")
    _erro(_pergunta(cliente, "pergunta_x", True, sessao_id="ses_9999"), 404, "nao_encontrado")
    _erro(_corrigir_pergunta(cliente, "pergunta_x", {"valor": True}, sessao_id="ses_9999"), 404, "nao_encontrado")


# --- a tela muda com o modo --------------------------------------------------------------------


@pytest.fixture
def cliente_tela_por_modo(tmp_path, fabrica_base_dir, hoje, agora):
    """Base em que a tela ``sinais`` pede ``exame_v`` a mais no modo veterinário (``simbolos_por_modo``)."""

    def ajustar(dados: dict) -> None:
        dados["meta"]["triagem"][1]["simbolos_por_modo"] = {
            "produtor": ["sinal_a", "sinal_b"],
            "veterinario": ["sinal_a", "sinal_b", "exame_v"],
        }

    config = Configuracao(
        base_dir=fabrica_base_dir(tmp_path / "base_modo", ajustar),
        db_path=tmp_path / "dados_modo" / "anamnese.db", web_dist=tmp_path / "web",
        hoje=lambda: hoje, agora=lambda: agora,
    )
    with TestClient(criar_app(config), raise_server_exceptions=False) as cliente:
        yield config, cliente


@contextmanager
def _contexto(config: Configuracao):
    with closing(abrir(config.db_path)) as conn:
        yield Contexto(config=config, conn=conn, repo=Repositorio(config.base_dir, hoje=config.hoje))


def test_tela_respondida_no_produtor_volta_pendente_no_veterinario(cliente_tela_por_modo):
    """Tela com fato gravado, mas com símbolo novo no outro modo, ainda não está respondida: o POST é aceito."""
    config, cliente = cliente_tela_por_modo
    animal = criar_animal_teste(cliente)
    criar_sessao_teste(cliente, animal["id"])
    assert _triagem(cliente, "sinais", SINAIS).status_code == 200
    with _contexto(config) as ctx:  # a troca de modo é a rota da Task 7; aqui só se precisa do efeito dela
        aplicar(ctx, carregar(ctx, "ses_0001"), lambda motor: motor.trocar_modo("veterinario"), muda=True)
    estado = cliente.get("/api/sessoes/ses_0001").json()
    assert estado["fase"] == "triagem"
    assert [c["simbolo"] for c in estado["proxima"]["campos"]] == ["exame_v"]

    _erro(_triagem(cliente, "sinais", {"valores": {"sinal_a": True}}), 422, "resposta_invalida")  # já respondido
    resposta = _triagem(cliente, "sinais", {"valores": {"exame_v": True}})
    assert resposta.status_code == 200, resposta.text
    validar_contrato("responder_triagem", resposta.json())
    assert resposta.json()["fase"] != "triagem"
    _erro(_triagem(cliente, "sinais", {"valores": {"exame_v": True}}), 409, "ja_respondida")


# --- pergunta dinâmica numérica e categórica ---------------------------------------------------------


def _pergunta_x_numerica(dados: dict) -> None:
    """``pergunta_x`` vira a temperatura (numérica, 30 a 45 °C); a regra R-D1-02 passa a pedir ``>= 39``."""
    simbolo = next(s for s in dados["simbolos"] if s["id"] == "pergunta_x")
    simbolo["dominio"] = {"tipo": "numerico", "min": 30, "max": 45, "unidade": "°C"}
    regra = next(r for r in dados["regras"] if r["id"] == "R-D1-02")
    regra["se"] = [{"simbolo": "recente"}, {"simbolo": "pergunta_x", "op": "≥", "valor": 39}]


def _pergunta_x_categorica(dados: dict) -> None:
    """``pergunta_x`` vira o apetite (categórica); a regra R-D1-02 passa a pedir ``= reduzido``."""
    simbolo = next(s for s in dados["simbolos"] if s["id"] == "pergunta_x")
    simbolo["dominio"] = {"tipo": "categorico", "valores": ["normal", "reduzido", "ausente"]}
    regra = next(r for r in dados["regras"] if r["id"] == "R-D1-02")
    regra["se"] = [{"simbolo": "recente"}, {"simbolo": "pergunta_x", "op": "=", "valor": "reduzido"}]


def _sessao_dinamica(cliente_com, ajustar) -> tuple[TestClient, dict]:
    """``(cliente, estado)`` com ``sinais`` respondida: a próxima é a pergunta dinâmica ``pergunta_x``."""
    _, cliente = cliente_com(ajustar)
    criar_sessao_teste(cliente, criar_animal_teste(cliente)["id"])
    resposta = _triagem(cliente, "sinais", SINAIS)
    assert resposta.status_code == 200, resposta.text
    estado = resposta.json()
    assert estado["proxima"]["tipo"] == "pergunta" and estado["proxima"]["simbolo"] == "pergunta_x"
    return cliente, estado


def _responder_x(cliente, valor) -> object:
    return cliente.post("/api/sessoes/ses_0001/respostas", json={"simbolo": "pergunta_x", "valor": valor})


def test_dinamica_numerica_expoe_limites_e_aceita_numero(cliente_com):
    cliente, estado = _sessao_dinamica(cliente_com, _pergunta_x_numerica)
    proxima = estado["proxima"]
    validar_contrato("responder_triagem", estado)
    assert (proxima["entrada"], proxima["unidade"], proxima["min"], proxima["max"], proxima["opcoes"]) == (
        "numerico", "°C", 30, 45, None,
    )
    resposta = _responder_x(cliente, 39)  # o JSON 39 chega como 39.0: é número, não texto
    assert resposta.status_code == 200, resposta.text
    corpo = resposta.json()
    validar_contrato("responder_pergunta", corpo)
    assert corpo["revisao"] == 3 and corpo["progresso"]["dinamicas_feitas"] == 1
    como = cliente.get("/api/sessoes/ses_0001/como/d1").json()
    assert "R-D1-02" in [e["regra_id"] for e in como["evidencias"]]  # 39 >= 39: a regra com o limiar disparou


@pytest.mark.parametrize("valor", ["39.5.1", "39e0", True, "alto"], ids=["dois_pontos", "expoente", "booleano", "palavra"])
def test_dinamica_numerica_recusa_texto_que_nao_e_numero_estrito(cliente_com, valor):
    cliente, estado = _sessao_dinamica(cliente_com, _pergunta_x_numerica)
    _erro(_responder_x(cliente, valor), 422, "resposta_invalida")
    assert cliente.get("/api/sessoes/ses_0001").json() == estado  # nada foi gravado


@pytest.mark.parametrize("valor", [29.9, 45.1, 1000], ids=["abaixo", "acima", "absurdo"])
def test_dinamica_numerica_fora_dos_limites_422(cliente_com, valor):
    cliente, estado = _sessao_dinamica(cliente_com, _pergunta_x_numerica)
    _erro(_responder_x(cliente, valor), 422, "resposta_invalida")
    assert cliente.get("/api/sessoes/ses_0001").json() == estado


def test_dinamica_categorica_expoe_opcoes_e_aceita_uma_valida(cliente_com):
    cliente, estado = _sessao_dinamica(cliente_com, _pergunta_x_categorica)
    proxima = estado["proxima"]
    validar_contrato("responder_triagem", estado)
    assert proxima["entrada"] == "categorico"
    assert [o["valor"] for o in proxima["opcoes"]] == ["normal", "reduzido", "ausente"]
    assert (proxima["unidade"], proxima["min"], proxima["max"]) == (None, None, None)
    resposta = _responder_x(cliente, "reduzido")
    assert resposta.status_code == 200, resposta.text
    validar_contrato("responder_pergunta", resposta.json())
    como = cliente.get("/api/sessoes/ses_0001/como/d1").json()
    assert "R-D1-02" in [e["regra_id"] for e in como["evidencias"]]


@pytest.mark.parametrize("valor", ["inexistente", "Reduzido ", 3, True], ids=["fora_da_lista", "caixa_e_espaco", "numero", "booleano"])
def test_dinamica_categorica_opcao_invalida_422(cliente_com, valor):
    cliente, estado = _sessao_dinamica(cliente_com, _pergunta_x_categorica)
    _erro(_responder_x(cliente, valor), 422, "resposta_invalida")
    assert cliente.get("/api/sessoes/ses_0001").json() == estado


def test_dinamica_numerica_e_categorica_aceitam_nao_sei(cliente_com):
    for ajustar in (_pergunta_x_numerica, _pergunta_x_categorica):
        cliente, _ = _sessao_dinamica(cliente_com, ajustar)
        resposta = _pergunta(cliente, "pergunta_x", nao_sei=True)
        assert resposta.status_code == 200, resposta.text
        assert resposta.json()["progresso"]["dinamicas_feitas"] == 1
