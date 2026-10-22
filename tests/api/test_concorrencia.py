"""Concorrência: transação imediata, ids sem corrida e revisão otimista da sessão (dados fictícios).

Duas requisições simultâneas (threads + ``threading.Barrier``) no mesmo ``TestClient``. As corridas são
probabilísticas, por isso cada teste repete o par várias vezes.
"""
from __future__ import annotations

import sqlite3
import threading
from collections import Counter
from collections.abc import Callable
from contextlib import closing

import pytest

from api.contexto import Contexto
from api.db.conexao import abrir, transacao
from api.erros import ErroApi
from api.servicos.sessao_motor import aplicar, carregar
from kb.carregador import Repositorio
from tests.api.apoio import criar_animal_teste, criar_sessao_teste

REPETICOES = 15
SINAIS = {"valores": {"sinal_a": True, "sinal_b": False}}


def _em_par(a: Callable, b: Callable) -> list:
    """Roda ``a`` e ``b`` ao mesmo tempo (largam juntas numa ``Barrier``) e devolve ``[resultado_a, resultado_b]``."""
    barreira = threading.Barrier(2)
    saida: list = [None, None]
    erros: list = []

    def rodar(i: int, fazer: Callable) -> None:
        try:
            barreira.wait(timeout=10)
            saida[i] = fazer()
        except BaseException as erro:  # noqa: BLE001 - o teste reporta qualquer falha da thread
            erros.append(erro)

    threads = [threading.Thread(target=rodar, args=(i, f)) for i, f in enumerate((a, b))]
    for t in threads:
        t.start()
    for t in threads:
        t.join(timeout=60)
    assert not erros, erros
    return saida


# --- transacao() ------------------------------------------------------------------------------


@pytest.fixture
def conn(config):
    config.db_path.parent.mkdir(parents=True, exist_ok=True)
    from api.db.conexao import inicializar

    inicializar(config.db_path)
    with closing(abrir(config.db_path)) as c:
        yield c


def test_transacao_confirma_no_sucesso_e_desfaz_na_excecao(conn):
    with transacao(conn):
        conn.execute("INSERT INTO versoes_base (versao, hash, criada_em) VALUES ('v9001', 'h', 'x')")
    assert not conn.in_transaction
    assert conn.execute("SELECT COUNT(*) FROM versoes_base").fetchone()[0] == 1

    with pytest.raises(RuntimeError, match="falhou"):
        with transacao(conn):
            conn.execute("INSERT INTO versoes_base (versao, hash, criada_em) VALUES ('v9002', 'h', 'x')")
            raise RuntimeError("falhou")
    assert not conn.in_transaction
    assert conn.execute("SELECT COUNT(*) FROM versoes_base").fetchone()[0] == 1


def test_transacao_aninhada_falha_alto(conn):
    with transacao(conn):
        with pytest.raises(sqlite3.OperationalError):
            with transacao(conn):
                pass  # pragma: no cover
    assert not conn.in_transaction


def test_transacao_e_imediata_e_bloqueia_a_escrita_de_outra_conexao(conn, config):
    with transacao(conn):  # já tem a trava de escrita, antes de escrever qualquer coisa
        with closing(abrir(config.db_path)) as outra:
            outra.execute("PRAGMA busy_timeout = 0")
            with pytest.raises(sqlite3.OperationalError, match="locked"):
                outra.execute("BEGIN IMMEDIATE")


# --- I1: ids sem corrida ----------------------------------------------------------------------


def test_duas_sessoes_simultaneas_do_mesmo_animal_ganham_ids_diferentes(cliente):
    animal = criar_animal_teste(cliente)
    corpo = {"animal_id": animal["id"], "modo": "produtor"}
    for _ in range(REPETICOES):
        a, b = _em_par(lambda: cliente.post("/api/sessoes", json=corpo), lambda: cliente.post("/api/sessoes", json=corpo))
        assert (a.status_code, b.status_code) == (201, 201), (a.text, b.text)
        assert a.json()["sessao_id"] != b.json()["sessao_id"]


def test_dois_animais_simultaneos_com_brincos_diferentes_ganham_ids_diferentes(cliente):
    for i in range(REPETICOES):
        def novo(brinco: str):
            return lambda: cliente.post("/api/animais", json={"brinco": brinco, "nome": "Mimosa", "ficha": {}})

        a, b = _em_par(novo(f"BR-A{i}"), novo(f"BR-B{i}"))
        assert (a.status_code, b.status_code) == (201, 201), (a.text, b.text)
        assert a.json()["id"] != b.json()["id"]


def test_duas_execucoes_simultaneas_ganham_ids_diferentes(cliente, com_casos):
    url = "/api/base/versoes/v0001/execucoes"
    for _ in range(REPETICOES):
        a, b = _em_par(lambda: cliente.post(url, json={"casos": None}), lambda: cliente.post(url, json={"casos": None}))
        assert (a.status_code, b.status_code) == (201, 201), (a.text, b.text)
        assert a.json()["execucao_id"] != b.json()["execucao_id"]


# --- I2: última escrita vence -----------------------------------------------------------------


@pytest.fixture
def animal(cliente) -> dict:
    return criar_animal_teste(cliente)


def test_duplo_post_na_mesma_tela_da_um_200_e_um_409_e_a_revisao_sobe_uma_vez(cliente, animal):
    for _ in range(REPETICOES):
        sessao_id = criar_sessao_teste(cliente, animal["id"])["sessao_id"]
        url = f"/api/sessoes/{sessao_id}/triagem/sinais"
        a, b = _em_par(lambda: cliente.post(url, json=SINAIS), lambda: cliente.post(url, json=SINAIS))
        assert sorted((a.status_code, b.status_code)) == [200, 409], (a.text, b.text)
        perdedora = a if a.status_code == 409 else b
        assert perdedora.json()["erro"]["codigo"] == "ja_respondida"
        assert cliente.get(f"/api/sessoes/{sessao_id}").json()["revisao"] == 2


def test_aplicar_sobre_sessao_desatualizada_e_409_conflito(cliente, config, animal):
    sessao_id = criar_sessao_teste(cliente, animal["id"])["sessao_id"]
    with closing(abrir(config.db_path)) as conn:
        ctx = Contexto(config=config, conn=conn, repo=Repositorio(config.base_dir, hoje=config.hoje))
        velha = carregar(ctx, sessao_id)  # lida antes da mutação abaixo
        assert cliente.post(f"/api/sessoes/{sessao_id}/triagem/sinais", json=SINAIS).status_code == 200
        with pytest.raises(ErroApi) as erro:
            with transacao(conn):
                aplicar(ctx, velha, lambda m: m.responder_triagem("sinais", ["sinal_a"], corrigir=False), muda=True)
        assert (erro.value.status, erro.value.codigo) == (409, "conflito")
        assert "recarregue" in erro.value.mensagem
        assert not conn.in_transaction
    estado = cliente.get(f"/api/sessoes/{sessao_id}").json()
    assert estado["revisao"] == 2  # a gravação da sessão velha não aconteceu


def test_leitura_desatualizada_nao_regrava_nem_falha(cliente, config, animal):
    sessao_id = criar_sessao_teste(cliente, animal["id"])["sessao_id"]
    with closing(abrir(config.db_path)) as conn:
        ctx = Contexto(config=config, conn=conn, repo=Repositorio(config.base_dir, hoje=config.hoje))
        velha = carregar(ctx, sessao_id)
        velha.linha["snapshot"] = {**velha.linha["snapshot"], "resumo": {"urgencia": "x", "top1": None}}  # força "regravar"
        assert cliente.post(f"/api/sessoes/{sessao_id}/triagem/sinais", json=SINAIS).status_code == 200
        estado = aplicar(ctx, velha, lambda m: None, muda=False)  # sem erro; devolve o que calculou
        assert estado.sessao_id == sessao_id
    assert cliente.get(f"/api/sessoes/{sessao_id}").json()["revisao"] == 2
    assert cliente.get(f"/api/sessoes/{sessao_id}").json()["fase"] == "dinamica"  # a resposta não foi desfeita


def test_resposta_e_troca_de_modo_simultaneas_nao_perdem_nenhuma(cliente, animal):
    """Cada requisição aceita (200) está no estado final; a recusada é explícita (409 ou 422), nunca perdida em silêncio.

    Com a trava, a segunda relê o estado da primeira: se o PATCH vem antes, ``pergunta_x`` não vale mais no modo
    veterinário (422 ``resposta_invalida``); se a resposta vem antes, as duas passam.
    """
    resultados = Counter()
    for _ in range(REPETICOES):
        sessao_id = criar_sessao_teste(cliente, animal["id"])["sessao_id"]
        assert cliente.post(f"/api/sessoes/{sessao_id}/triagem/sinais", json=SINAIS).status_code == 200
        corpo = {"simbolo": "pergunta_x", "valor": True}
        responder = lambda: cliente.post(f"/api/sessoes/{sessao_id}/respostas", json=corpo)  # noqa: E731
        trocar = lambda: cliente.patch(f"/api/sessoes/{sessao_id}", json={"modo": "veterinario"})  # noqa: E731
        resposta, patch = _em_par(responder, trocar)
        estado = cliente.get(f"/api/sessoes/{sessao_id}").json()
        assert resposta.status_code in (200, 409, 422), resposta.text
        assert patch.status_code in (200, 409), patch.text
        if resposta.status_code != 200:
            assert resposta.json()["erro"]["codigo"] in ("conflito", "resposta_invalida")
        if patch.status_code != 200:
            assert patch.json()["erro"]["codigo"] == "conflito"
        assert (estado["modo"] == "veterinario") == (patch.status_code == 200)  # a troca aceita está lá
        assert (estado["progresso"]["dinamicas_feitas"] == 1) == (resposta.status_code == 200)  # a resposta aceita também
        resultados[(resposta.status_code, patch.status_code)] += 1
    assert sum(resultados.values()) == REPETICOES
