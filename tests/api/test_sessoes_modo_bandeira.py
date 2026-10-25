"""Troca de modo (PATCH) e ação da bandeira vermelha (POST) (Task 7).

Base mínima (``tests/fixtures/kb/base_minima.json``), dados fictícios, ``hoje`` = 2026-10-20. O animal com parto em
``2026-10-14`` tem 6 dias em lactação: a primeira pergunta é a tela ``sinais``.

Na base mínima a triagem acaba em ``sinais``: ``sinal_b`` dispara ``R-BV-01`` e a sessão encerra na hora
(``sem_potencial``). Para ter uma bandeira com algo ainda aberto, os testes de pausa usam a base com uma tela
``extra`` depois de ``sinais``.
"""
from __future__ import annotations

from contextlib import closing

import pytest

from api.config import Configuracao
from api.db.conexao import abrir
from tests.api.apoio import criar_animal_teste, criar_sessao_teste, validar_contrato

SINAIS = {"valores": {"sinal_a": True, "sinal_b": False}}
SINAIS_COM_BANDEIRA = {"valores": {"sinal_a": False, "sinal_b": True}}
SINAIS_SEM_BANDEIRA = {"valores": {"sinal_a": False, "sinal_b": False}}
URGENCIA_BANDEIRA = {"nivel": "chamar_agora", "provisoria": True, "origem": "bandeira_vermelha", "regras": ["R-BV-01"]}
RESPOSTAS = "SELECT simbolo, valor_json, nao_sei, origem, tela_id, ordem FROM respostas ORDER BY simbolo"


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


def _modo(cliente, modo, *, sessao_id: str = "ses_0001"):
    return cliente.patch(f"/api/sessoes/{sessao_id}", json={"modo": modo})


def _bandeira(cliente, acao, *, sessao_id: str = "ses_0001"):
    return cliente.post(f"/api/sessoes/{sessao_id}/acoes/bandeira", json={"acao": acao})


def _ajustar_tela_no_fim(dados: dict) -> None:
    """Uma terceira tela depois de ``sinais``: a triagem continua aberta quando a bandeira dispara."""
    dados["meta"]["triagem"].append(
        {
            "id": "extra", "selecao": "unica", "simbolos": ["pergunta_x"],
            "texto": {"produtor": "Notou o fato X?", "veterinario": "Fato X?"},
        }
    )


@pytest.fixture
def sessao_dinamica_produtor(cliente) -> dict:
    """``ses_0001`` do produtor com ``sinais`` e ``pergunta_x`` respondidas: a fase dinâmica do produtor acabou."""
    animal = criar_animal_teste(cliente)
    criar_sessao_teste(cliente, animal["id"])
    assert _triagem(cliente, "sinais", SINAIS).status_code == 200
    resposta = _pergunta(cliente, "pergunta_x", True)
    assert resposta.status_code == 200, resposta.text
    return resposta.json()


@pytest.fixture
def pausada(cliente_com):
    """``(config, cliente, estado)``: produtor com ``sinal_b`` marcado e a tela ``extra`` aberta (sessão pausada)."""
    config, cliente = cliente_com(_ajustar_tela_no_fim)
    animal = criar_animal_teste(cliente)
    criar_sessao_teste(cliente, animal["id"])
    resposta = _triagem(cliente, "sinais", SINAIS_COM_BANDEIRA)
    assert resposta.status_code == 200, resposta.text
    return config, cliente, resposta.json()


# --- PATCH /sessoes/{id}: troca de modo ----------------------------------------------------------


def test_patch_modo_preserva_respostas_e_muda_limite(cliente, config, sessao_dinamica_produtor):
    anterior = sessao_dinamica_produtor
    assert (anterior["modo"], anterior["revisao"], anterior["progresso"]["limite_dinamico"]) == ("produtor", 3, 12)
    respostas = _consultar(config, RESPOSTAS)

    resposta = _modo(cliente, "veterinario")
    assert resposta.status_code == 200, resposta.text
    corpo = resposta.json()
    validar_contrato("trocar_modo", corpo)
    assert corpo["modo"] == "veterinario"
    assert corpo["revisao"] == 4  # a troca é uma mudança do usuário: sobe a revisão
    assert corpo["progresso"]["limite_dinamico"] is None  # o especialista não tem limite
    assert corpo["progresso"]["dinamicas_feitas"] == 1  # a pergunta_x já respondida continua contando
    assert corpo["proxima"]["tipo"] == "pergunta"
    assert corpo["proxima"]["simbolo"] == "exame_v"  # a pergunta que só existe no modo veterinário
    assert _consultar(config, RESPOSTAS) == respostas  # nenhuma resposta se perde nem muda
    assert _consultar(config, "SELECT modo, revisao FROM sessoes") == [("veterinario", 4)]
    assert cliente.get("/api/sessoes/ses_0001").json() == corpo  # o que o PATCH devolveu é o que ficou gravado


def test_patch_volta_ao_produtor_e_pergunta_do_vet_some(cliente, config, sessao_dinamica_produtor):
    respostas = _consultar(config, RESPOSTAS)
    assert _modo(cliente, "veterinario").json()["proxima"]["simbolo"] == "exame_v"

    resposta = _modo(cliente, "produtor")
    assert resposta.status_code == 200, resposta.text
    corpo = resposta.json()
    validar_contrato("trocar_modo", corpo)
    assert corpo["modo"] == "produtor"
    assert corpo["revisao"] == 5
    assert corpo["progresso"]["limite_dinamico"] == 12
    assert corpo["proxima"] is None  # a pergunta exame_v não vale no produtor e não restou outra
    assert corpo["fase"] == "encerrada"
    assert _consultar(config, RESPOSTAS) == respostas


def test_patch_para_o_mesmo_modo_e_aceito_e_conta_como_mudanca(cliente, sessao_dinamica_produtor):
    corpo = _modo(cliente, "produtor").json()
    assert corpo["modo"] == "produtor"
    assert corpo["revisao"] == sessao_dinamica_produtor["revisao"] + 1


def test_patch_modo_invalido_422(cliente, config, sessao_dinamica_produtor):
    for corpo in ({"modo": "x"}, {"modo": None}, {}, {"modo": "veterinario", "extra": 1}):
        _erro(cliente.patch("/api/sessoes/ses_0001", json=corpo), 422, "entrada_invalida")
    assert cliente.get("/api/sessoes/ses_0001").json() == sessao_dinamica_produtor
    assert _consultar(config, "SELECT modo, revisao FROM sessoes") == [("produtor", 3)]


def test_patch_sessao_inexistente_404(cliente):
    _erro(_modo(cliente, "veterinario", sessao_id="ses_9999"), 404, "nao_encontrado")


# --- POST /sessoes/{id}/acoes/bandeira -------------------------------------------------------------


def test_bandeira_pausa_so_no_produtor(pausada):
    _, cliente, produtor = pausada
    validar_contrato("responder_triagem", produtor)
    assert produtor["alerta"]["pausa"] is True
    assert produtor["alerta"]["acoes"] == ["ver_parecer", "continuar"]
    assert produtor["alerta"]["regras"] == ["R-BV-01"]
    assert produtor["urgencia"] == URGENCIA_BANDEIRA
    assert produtor["proxima"] is None  # pausada: o frontend mostra o alerta, não uma tela
    assert produtor["fase"] == "triagem"

    animal = criar_animal_teste(cliente, brinco="BR-0002")
    criar_sessao_teste(cliente, animal["id"], "veterinario")
    veterinario = _triagem(cliente, "sinais", SINAIS_COM_BANDEIRA, sessao_id="ses_0002").json()
    assert veterinario["alerta"]["pausa"] is False  # o veterinário vê a bandeira, mas a anamnese não para
    assert veterinario["alerta"]["acoes"] == []
    assert veterinario["urgencia"] == URGENCIA_BANDEIRA
    assert veterinario["proxima"]["tela_id"] == "extra"


def test_alerta_traz_os_sinais_da_bandeira_em_linguagem_simples(pausada):
    _, _, produtor = pausada
    assert produtor["alerta"]["sinais"] == ["sinal B"]


def test_bandeira_com_a_sessao_encerrada_oferece_so_ver_parecer(cliente):
    """Na base mínima não há o que continuar: a bandeira encerra a sessão e a única ação é ver o parecer."""
    animal = criar_animal_teste(cliente)
    criar_sessao_teste(cliente, animal["id"])
    corpo = _triagem(cliente, "sinais", SINAIS_COM_BANDEIRA).json()
    assert corpo["fase"] == "encerrada" and corpo["proxima"] is None
    assert corpo["alerta"]["pausa"] is True
    assert corpo["alerta"]["acoes"] == ["ver_parecer"]


def test_continuar_tira_pausa_e_mantem_quadro(pausada):
    config, cliente, _ = pausada
    resposta = _bandeira(cliente, "continuar")
    assert resposta.status_code == 200, resposta.text
    corpo = resposta.json()
    validar_contrato("acao_bandeira", corpo)
    assert corpo["revisao"] == 3  # criar, sinais, continuar
    assert corpo["alerta"]["pausa"] is False
    assert corpo["alerta"]["acoes"] == []
    assert corpo["alerta"]["regras"] == ["R-BV-01"]  # o alerta continua à vista, só deixa de pausar
    assert corpo["urgencia"] == URGENCIA_BANDEIRA  # o quadro urgente continua no topo, provisório
    assert corpo["fase"] == "triagem"
    assert corpo["proxima"]["tipo"] == "tela_triagem"
    assert corpo["proxima"]["tela_id"] == "extra"  # a anamnese segue de onde parou
    assert _consultar(config, "SELECT bandeiras_reconhecidas_json, fase FROM sessoes") == [('["R-BV-01"]', "triagem")]
    assert cliente.get("/api/sessoes/ses_0001").json() == corpo


def test_continuar_com_a_sessao_encerrada_e_aceito_e_inocuo(cliente):
    """O motor aceita ``continuar`` numa sessão já encerrada: só tira a pausa; não vira 422."""
    animal = criar_animal_teste(cliente)
    criar_sessao_teste(cliente, animal["id"])
    assert _triagem(cliente, "sinais", SINAIS_COM_BANDEIRA).json()["fase"] == "encerrada"
    resposta = _bandeira(cliente, "continuar")
    assert resposta.status_code == 200, resposta.text
    corpo = resposta.json()
    validar_contrato("acao_bandeira", corpo)
    assert corpo["fase"] == "encerrada" and corpo["proxima"] is None
    assert corpo["alerta"]["pausa"] is False and corpo["alerta"]["acoes"] == []


def test_ver_parecer_encerra(pausada):
    config, cliente, _ = pausada
    resposta = _bandeira(cliente, "ver_parecer")
    assert resposta.status_code == 200, resposta.text
    corpo = resposta.json()
    validar_contrato("acao_bandeira", corpo)
    assert corpo["revisao"] == 3
    assert corpo["fase"] == "encerrada"
    assert corpo["proxima"] is None
    assert corpo["urgencia"]["provisoria"] is False
    assert corpo["urgencia"]["nivel"] == "chamar_agora"
    assert corpo["alerta"]["pausa"] is False and corpo["alerta"]["acoes"] == []
    assert _consultar(config, "SELECT fase, bandeiras_reconhecidas_json FROM sessoes") == [("encerrada", '["R-BV-01"]')]
    assert cliente.get("/api/sessoes/ses_0001").json() == corpo


def test_continuar_sem_bandeira_e_sem_encerrar_422(cliente, config):
    animal = criar_animal_teste(cliente)
    criar_sessao_teste(cliente, animal["id"])
    antes = cliente.get("/api/sessoes/ses_0001").json()
    assert antes["alerta"] is None
    _erro(_bandeira(cliente, "continuar"), 422, "resposta_invalida")  # nada a reconhecer nem a retomar
    assert cliente.get("/api/sessoes/ses_0001").json() == antes  # nada foi gravado, a revisão não subiu
    assert _consultar(config, "SELECT revisao FROM sessoes") == [(1,)]


def test_ver_resultado_agora_sem_bandeira_encerra_e_continuar_retoma(cliente):
    animal = criar_animal_teste(cliente)
    criar_sessao_teste(cliente, animal["id"])
    encerrada = _bandeira(cliente, "ver_parecer")
    assert encerrada.status_code == 200, encerrada.text
    assert (encerrada.json()["fase"], encerrada.json()["proxima"], encerrada.json()["alerta"]) == ("encerrada", None, None)
    parecer = cliente.get("/api/sessoes/ses_0001/parecer").json()
    assert parecer["final"] is True and parecer["motivo_parada"] is None
    retomada = _bandeira(cliente, "continuar")
    assert retomada.status_code == 200, retomada.text
    assert retomada.json()["fase"] != "encerrada" and retomada.json()["proxima"] is not None


@pytest.mark.parametrize("corpo", [{"acao": "x"}, {"acao": None}, {}, {"acao": "continuar", "extra": 1}])
def test_acao_invalida_422(cliente, corpo):
    animal = criar_animal_teste(cliente)
    criar_sessao_teste(cliente, animal["id"])
    _erro(cliente.post("/api/sessoes/ses_0001/acoes/bandeira", json=corpo), 422, "entrada_invalida")


def test_acao_de_bandeira_em_sessao_inexistente_404(cliente):
    _erro(_bandeira(cliente, "continuar", sessao_id="ses_9999"), 404, "nao_encontrado")


# --- a bandeira e a revisão da resposta ----------------------------------------------------------


def test_corrigir_bandeira_remove_alerta(pausada):
    """O motor refaz o quadro a cada correção: sem ``sinal_b``, a bandeira some e não resta ação a tomar."""
    _, cliente, _ = pausada
    resposta = _triagem(cliente, "sinais", SINAIS_SEM_BANDEIRA, metodo="PUT")
    assert resposta.status_code == 200, resposta.text
    corpo = resposta.json()
    validar_contrato("corrigir_triagem", corpo)
    assert corpo["alerta"] is None
    assert corpo["urgencia"]["origem"] != "bandeira_vermelha"
    assert corpo["proxima"]["tela_id"] == "extra"  # a pausa acabou junto com a bandeira
    _erro(_bandeira(cliente, "continuar"), 422, "resposta_invalida")  # e a ação deixou de existir
    assert cliente.get("/api/sessoes/ses_0001").json() == corpo


def test_trocar_para_veterinario_levanta_a_pausa(pausada):
    """A pausa é do produtor: no modo veterinário a bandeira continua visível, mas a anamnese segue."""
    _, cliente, _ = pausada
    corpo = _modo(cliente, "veterinario").json()
    validar_contrato("trocar_modo", corpo)
    assert corpo["alerta"]["pausa"] is False
    assert corpo["alerta"]["acoes"] == []
    assert corpo["urgencia"] == URGENCIA_BANDEIRA
    assert corpo["proxima"]["tela_id"] == "extra"


# --- depois de ver_parecer ---------------------------------------------------------------------------


def _depois_de_ver_parecer(pausada) -> tuple:
    config, cliente, _ = pausada
    resposta = _bandeira(cliente, "ver_parecer")
    assert resposta.status_code == 200, resposta.text
    encerrada = resposta.json()
    assert (encerrada["fase"], encerrada["proxima"], encerrada["alerta"]["pausa"]) == ("encerrada", None, False)
    assert cliente.get("/api/sessoes/ses_0001/parecer").json()["final"] is True
    return config, cliente, encerrada


def _reaberta(corpo: dict) -> None:
    """O estado de uma sessão reaberta: de volta à triagem, com a tela ``extra`` pela frente e sem pausa."""
    assert corpo["fase"] == "triagem" and corpo["proxima"]["tela_id"] == "extra"
    assert corpo["alerta"]["pausa"] is False and corpo["alerta"]["acoes"] == []
    assert corpo["urgencia"]["provisoria"] is True  # voltou a ser o quadro em andamento


def test_continuar_depois_de_ver_parecer_reabre_a_sessao(pausada):
    config, cliente, encerrada = _depois_de_ver_parecer(pausada)
    resposta = _bandeira(cliente, "continuar")
    assert resposta.status_code == 200, resposta.text
    corpo = resposta.json()
    validar_contrato("acao_bandeira", corpo)
    _reaberta(corpo)
    assert corpo["revisao"] == encerrada["revisao"] + 1
    assert cliente.get("/api/sessoes/ses_0001/parecer").json()["final"] is False  # o parecer voltou a ser parcial
    assert _consultar(config, "SELECT fase FROM sessoes") == [("triagem",)]
    assert cliente.get("/api/sessoes/ses_0001").json() == corpo


@pytest.mark.parametrize("modo", ["produtor", "veterinario"])
def test_patch_de_modo_depois_de_ver_parecer_reabre_a_sessao(pausada, modo):
    """Até o PATCH para o mesmo modo reabre: o motor refaz o quadro e a sessão já não está encerrada."""
    _, cliente, encerrada = _depois_de_ver_parecer(pausada)
    resposta = _modo(cliente, modo)
    assert resposta.status_code == 200, resposta.text
    corpo = resposta.json()
    validar_contrato("trocar_modo", corpo)
    assert corpo["fase"] == "triagem" and corpo["proxima"]["tela_id"] == "extra"
    assert corpo["modo"] == modo and corpo["revisao"] == encerrada["revisao"] + 1


def test_correcao_depois_de_ver_parecer_reabre_a_sessao(pausada):
    _, cliente, encerrada = _depois_de_ver_parecer(pausada)
    resposta = _triagem(cliente, "sinais", SINAIS_COM_BANDEIRA, metodo="PUT")  # a mesma resposta, só reenviada
    assert resposta.status_code == 200, resposta.text
    corpo = resposta.json()
    validar_contrato("corrigir_triagem", corpo)
    assert corpo["fase"] == "triagem" and corpo["proxima"]["tela_id"] == "extra"
    assert corpo["revisao"] == encerrada["revisao"] + 1


def test_resposta_nova_depois_de_ver_parecer_422_e_nada_muda(pausada):
    """Responder (POST) a uma sessão encerrada é recusado pelo motor: a tela já não é a próxima."""
    _, cliente, encerrada = _depois_de_ver_parecer(pausada)
    _erro(_triagem(cliente, "extra", {"valores": {"pergunta_x": True}}), 422, "resposta_invalida")
    assert cliente.get("/api/sessoes/ses_0001").json() == encerrada
