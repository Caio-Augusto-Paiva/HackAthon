"""Esquema SQLite, conexão e repositórios (Task 2). Dados fictícios."""
from __future__ import annotations

import sqlite3
import threading
from collections.abc import Iterator
from datetime import datetime, timedelta
from pathlib import Path
from types import SimpleNamespace
from typing import Annotated

import pytest
from fastapi import Depends, FastAPI
from fastapi.testclient import TestClient

from api.config import Configuracao
from api.contexto import Contexto, obter_contexto
from api.db import repositorios as repo
from api.db.conexao import abrir, inicializar

TABELAS = {
    "animais",
    "sessoes",
    "respostas",
    "perguntas_feitas",
    "versoes_base",
    "execucoes_casos",
    "resultados_casos",
}


def _tabelas(conn: sqlite3.Connection) -> set[str]:
    linhas = conn.execute("select name from sqlite_master where type = 'table'").fetchall()
    return {linha["name"] for linha in linhas}


@pytest.fixture
def conn(tmp_path: Path) -> Iterator[sqlite3.Connection]:
    caminho = tmp_path / "dados" / "teste.db"
    inicializar(caminho)
    conexao = abrir(caminho)
    yield conexao
    conexao.close()


@pytest.fixture
def animal_id(conn: sqlite3.Connection, agora: datetime) -> str:
    return repo.inserir_animal(conn, brinco="BR-0001", nome="Mimosa", ficha={}, origens={}, agora=agora)


@pytest.fixture
def sessao_id(conn: sqlite3.Connection, animal_id: str, agora: datetime) -> str:
    return repo.inserir_sessao(
        conn,
        animal_id=animal_id,
        modo="produtor",
        versao_base="v0001",
        snapshot={"motor": {}},
        fase="triagem",
        agora=agora,
    )


def _fato(valor: object, cf: str = "1", origem: str = "resposta", tela_id: str | None = "sinais") -> dict:
    return {"valor": valor, "cf": cf, "origem": origem, "tela_id": tela_id}


def _resposta(conn: sqlite3.Connection, sessao_id: str, simbolo: str) -> sqlite3.Row:
    return conn.execute(
        "select * from respostas where sessao_id = ? and simbolo = ?", (sessao_id, simbolo)
    ).fetchone()


# --- conexão e esquema ----------------------------------------------------------------------


def test_inicializar_idempotente_cria_sete_tabelas(tmp_path: Path) -> None:
    caminho = tmp_path / "subpasta" / "anamnese.db"
    inicializar(caminho)
    inicializar(caminho)
    conexao = abrir(caminho)
    try:
        assert _tabelas(conexao) == TABELAS
    finally:
        conexao.close()


def test_inicializar_e_atomico_um_ddl_quebrado_nao_deixa_tabela_pela_metade(tmp_path: Path, monkeypatch) -> None:
    """O DDL roda numa transação só: se uma instrução falha, as anteriores também são desfeitas."""
    ddl = tmp_path / "quebrado.sql"
    ddl.write_text("CREATE TABLE IF NOT EXISTS a (x INTEGER);\nCREATE TABLE IF NOT EXISTS b (x INTEGER;\n", encoding="utf-8")
    monkeypatch.setattr("api.db.conexao.CAMINHO_ESQUEMA", ddl)
    caminho = tmp_path / "anamnese.db"
    with pytest.raises(sqlite3.OperationalError):
        inicializar(caminho)
    conexao = abrir(caminho)
    try:
        assert _tabelas(conexao) == set()
    finally:
        conexao.close()


def test_abrir_configura_conexao_e_serve_outra_thread(conn: sqlite3.Connection) -> None:
    assert conn.row_factory is sqlite3.Row
    assert conn.execute("pragma foreign_keys").fetchone()[0] == 1
    resultado: list[int] = []
    # o FastAPI roda setup, endpoint e teardown de uma dependência síncrona em threads do pool
    fio = threading.Thread(target=lambda: resultado.append(conn.execute("select 1").fetchone()[0]))
    fio.start()
    fio.join()
    assert resultado == [1]


def test_obter_contexto_abre_e_fecha_a_conexao(config: Configuracao) -> None:
    inicializar(config.db_path)
    requisicao = SimpleNamespace(app=SimpleNamespace(state=SimpleNamespace(config=config)))
    gerador = obter_contexto(requisicao)
    ctx = next(gerador)
    assert isinstance(ctx.conn, sqlite3.Connection)
    assert ctx.conn.execute("select count(*) from animais").fetchone()[0] == 0
    gerador.close()
    with pytest.raises(sqlite3.ProgrammingError):
        ctx.conn.execute("select 1")


def test_ciclo_de_vida_inicializa_o_esquema(cliente: TestClient, config: Configuracao) -> None:
    conexao = abrir(config.db_path)
    try:
        assert _tabelas(conexao) == TABELAS
    finally:
        conexao.close()


def test_dependencia_do_fastapi_entrega_contexto_com_conexao(app: FastAPI, cliente: TestClient) -> None:
    # integração com o pool de threads do FastAPI; quem prova o check_same_thread é o teste da outra thread
    @app.get("/api/_teste_contexto")
    def tabelas(ctx: Annotated[Contexto, Depends(obter_contexto)]) -> dict:
        return {"tabelas": sorted(_tabelas(ctx.conn))}

    for _ in range(20):
        resposta = cliente.get("/api/_teste_contexto")
        assert resposta.status_code == 200, resposta.text
        assert set(resposta.json()["tabelas"]) == TABELAS


def test_chave_estrangeira_exige_animal(conn: sqlite3.Connection, agora: datetime) -> None:
    with pytest.raises(sqlite3.IntegrityError):
        repo.inserir_sessao(
            conn,
            animal_id="an_999",
            modo="produtor",
            versao_base="v0001",
            snapshot={},
            fase="triagem",
            agora=agora,
        )


# --- ids ------------------------------------------------------------------------------------


def test_proximo_id_sequencial(conn: sqlite3.Connection, agora: datetime) -> None:
    assert repo.proximo_id(conn, "animais", "an", 3) == "an_001"
    primeiro = repo.inserir_animal(conn, brinco="BR-0001", nome="Mimosa", ficha={}, origens={}, agora=agora)
    assert primeiro == "an_001"
    assert repo.proximo_id(conn, "animais", "an", 3) == "an_002"
    assert repo.proximo_id(conn, "sessoes", "ses", 4) == "ses_0001"
    assert repo.proximo_id(conn, "execucoes_casos", "ex", 4) == "ex_0001"


def test_proximo_id_so_aceita_tabela_com_id(conn: sqlite3.Connection) -> None:
    with pytest.raises(ValueError):
        repo.proximo_id(conn, "respostas; drop table animais", "x", 3)


# --- animais --------------------------------------------------------------------------------


def test_brinco_unico(conn: sqlite3.Connection, agora: datetime) -> None:
    repo.inserir_animal(conn, brinco="BR-0001", nome="Mimosa", ficha={}, origens={}, agora=agora)
    with pytest.raises(sqlite3.IntegrityError):
        repo.inserir_animal(conn, brinco="BR-0001", nome="Estrela", ficha={}, origens={}, agora=agora)


def test_animal_ida_e_volta_json_e_atualizacao(conn: sqlite3.Connection, agora: datetime) -> None:
    ficha = {"data_ultimo_parto": "2026-10-14", "raca_grupo": "cruzada", "obs": "calma e dócil"}
    origens = {"raca_grupo": "manual"}
    animal_id = repo.inserir_animal(conn, brinco="BR-0001", nome="Mimosa", ficha=ficha, origens=origens, agora=agora)
    animal = repo.obter_animal(conn, animal_id)
    assert animal == {
        "id": "an_001",
        "brinco": "BR-0001",
        "nome": "Mimosa",
        "ficha": ficha,
        "origens": origens,
        "criado_em": "2026-10-20T10:00:00",
        "atualizado_em": "2026-10-20T10:00:00",
    }
    assert "dócil" in conn.execute("select ficha_json from animais").fetchone()[0]  # ensure_ascii=False
    assert repo.obter_animal_por_brinco(conn, "BR-0001") == animal
    assert repo.obter_animal(conn, "an_999") is None
    assert repo.obter_animal_por_brinco(conn, "BR-9999") is None

    depois = agora + timedelta(hours=1)
    repo.atualizar_animal(conn, animal_id, ficha={"raca_grupo": "zebuina"}, origens={"raca_grupo": "importacao"}, agora=depois)
    animal = repo.obter_animal(conn, animal_id)
    assert animal["ficha"] == {"raca_grupo": "zebuina"}
    assert animal["origens"] == {"raca_grupo": "importacao"}
    assert animal["criado_em"] == "2026-10-20T10:00:00"
    assert animal["atualizado_em"] == "2026-10-20T11:00:00"


def test_busca_animais_ignora_caixa(conn: sqlite3.Connection, agora: datetime) -> None:
    repo.inserir_animal(conn, brinco="BR-0001", nome="Mimosa", ficha={}, origens={}, agora=agora)
    repo.inserir_animal(conn, brinco="BR-0002", nome="Estrela", ficha={}, origens={}, agora=agora)
    repo.inserir_animal(conn, brinco="MIM-77", nome=None, ficha={}, origens={}, agora=agora)
    assert [a["brinco"] for a in repo.listar_animais(conn, "mim")] == ["BR-0001", "MIM-77"]
    assert [a["nome"] for a in repo.listar_animais(conn, "ESTR")] == ["Estrela"]
    assert [a["brinco"] for a in repo.listar_animais(conn, "br-0002")] == ["BR-0002"]
    assert repo.listar_animais(conn, "zzz") == []
    assert len(repo.listar_animais(conn, None)) == 3
    assert len(repo.listar_animais(conn, "")) == 3


def test_listar_animais_traz_ultima_sessao(conn: sqlite3.Connection, animal_id: str, agora: datetime) -> None:
    outro = repo.inserir_animal(conn, brinco="BR-0002", nome="Estrela", ficha={}, origens={}, agora=agora)
    for _ in range(2):
        ultima = repo.inserir_sessao(
            conn, animal_id=animal_id, modo="produtor", versao_base="v0001", snapshot={}, fase="triagem", agora=agora
        )
    por_brinco = {a["brinco"]: a for a in repo.listar_animais(conn, None)}
    assert por_brinco["BR-0001"]["ultima_sessao_id"] == ultima == "ses_0002"
    assert por_brinco["BR-0002"]["ultima_sessao_id"] is None
    assert outro == "an_002"


# --- sessões --------------------------------------------------------------------------------


def test_sessao_snapshot_ida_e_volta_e_revisao(
    conn: sqlite3.Connection, animal_id: str, agora: datetime
) -> None:
    inicial = {"motor": {"modo": "produtor", "fatos": {}}, "origens_ficha": {}}
    sessao_id = repo.inserir_sessao(
        conn, animal_id=animal_id, modo="produtor", versao_base="v0001", snapshot=inicial, fase="triagem", agora=agora
    )
    assert sessao_id == "ses_0001"
    sessao = repo.obter_sessao(conn, sessao_id)
    assert sessao["revisao"] == 1
    assert sessao["snapshot"] == inicial
    assert sessao["bandeiras_reconhecidas"] == []
    assert sessao["motivo_parada"] is None

    novo = {"motor": {"modo": "veterinario", "fatos": {"sinal_a": {"valor": True}}, "texto": "não sei"}}
    depois = agora + timedelta(minutes=5)
    assert (
        repo.salvar_sessao(
            conn, sessao_id, snapshot=novo, fase="dinamica", motivo_parada=None, modo="veterinario",
            reconhecidas=["R-BV-01"], agora=depois, subir_revisao=True,
        )
        == 2
    )
    assert (
        repo.salvar_sessao(
            conn, sessao_id, snapshot=novo, fase="encerrada", motivo_parada="limite", modo="veterinario",
            reconhecidas=["R-BV-01"], agora=depois, subir_revisao=False,
        )
        == 2
    )
    sessao = repo.obter_sessao(conn, sessao_id)
    assert sessao["snapshot"] == novo
    assert sessao["revisao"] == 2
    assert sessao["fase"] == "encerrada"
    assert sessao["motivo_parada"] == "limite"
    assert sessao["modo"] == "veterinario"
    assert sessao["bandeiras_reconhecidas"] == ["R-BV-01"]
    assert sessao["criada_em"] == "2026-10-20T10:00:00"
    assert sessao["atualizada_em"] == "2026-10-20T10:05:00"
    assert sessao["versao_base"] == "v0001"
    assert "não sei" in conn.execute("select snapshot_json from sessoes").fetchone()[0]  # ensure_ascii=False


def test_sessao_inexistente(conn: sqlite3.Connection, agora: datetime) -> None:
    assert repo.obter_sessao(conn, "ses_9999") is None
    with pytest.raises(LookupError):
        repo.salvar_sessao(
            conn, "ses_9999", snapshot={}, fase="triagem", motivo_parada=None, modo="produtor",
            reconhecidas=[], agora=agora, subir_revisao=True,
        )


def test_listar_sessoes_do_animal_mais_nova_primeiro(conn: sqlite3.Connection, animal_id: str, agora: datetime) -> None:
    outro = repo.inserir_animal(conn, brinco="BR-0002", nome="Estrela", ficha={}, origens={}, agora=agora)
    for aid in (animal_id, outro, animal_id):
        repo.inserir_sessao(
            conn, animal_id=aid, modo="produtor", versao_base="v0001", snapshot={"n": aid}, fase="triagem", agora=agora
        )
    sessoes = repo.listar_sessoes_do_animal(conn, animal_id)
    assert [s["id"] for s in sessoes] == ["ses_0003", "ses_0001"]
    assert sessoes[0]["snapshot"] == {"n": animal_id}
    assert repo.listar_sessoes_do_animal(conn, "an_999") == []


# --- projeções ------------------------------------------------------------------------------


def test_projetar_respostas_upsert(conn: sqlite3.Connection, sessao_id: str, agora: datetime) -> None:
    ordem = [["sinal_a", "sinal_b"]]
    repo.projetar_respostas(conn, sessao_id, {"sinal_a": _fato(True), "sinal_b": _fato(None, cf="0")}, ordem, "produtor", agora)
    repo.projetar_respostas(conn, sessao_id, {"sinal_a": _fato(False), "sinal_b": _fato(None, cf="0")}, ordem, "produtor", agora)
    linhas = conn.execute("select * from respostas where simbolo = 'sinal_a'").fetchall()
    assert len(linhas) == 1
    assert linhas[0]["valor_json"] == "false"
    assert conn.execute("select count(*) from respostas").fetchone()[0] == 2
    assert not _resposta(conn, sessao_id, "sinal_a")["nao_sei"]
    assert _resposta(conn, sessao_id, "sinal_b")["nao_sei"]
    assert _resposta(conn, sessao_id, "sinal_b")["valor_json"] == "null"


def test_projetar_respostas_campos(conn: sqlite3.Connection, sessao_id: str, agora: datetime) -> None:
    fatos = {
        "dias": _fato(6, origem="ficha", tela_id=None),
        "sinal_a": _fato(True),
        "cor": _fato("avermelhado", cf="4/5", tela_id=None),
    }
    ordem = [["dias"], ["sinal_a"]]
    repo.projetar_respostas(conn, sessao_id, fatos, ordem, "veterinario", agora)
    dias, sinal, cor = (_resposta(conn, sessao_id, s) for s in ("dias", "sinal_a", "cor"))
    assert (dias["valor_json"], dias["origem"], dias["tela_id"], dias["ordem"]) == ("6", "ficha", None, 1)
    assert (sinal["valor_json"], sinal["tela_id"], sinal["ordem"], sinal["nao_sei"]) == ("true", "sinais", 2, 0)
    assert (cor["valor_json"], cor["ordem"]) == ('"avermelhado"', 1)  # fora de qualquer lote: como o motor, no primeiro
    assert {r["modo_na_resposta"] for r in (dias, sinal, cor)} == {"veterinario"}
    assert {r["respondida_em"] for r in (dias, sinal, cor)} == {"2026-10-20T10:00:00"}


def test_projetar_respostas_so_regrava_o_que_mudou(conn: sqlite3.Connection, sessao_id: str, agora: datetime) -> None:
    repo.projetar_respostas(conn, sessao_id, {"sinal_a": _fato(True)}, [["sinal_a"]], "produtor", agora)

    # mesmo valor, outro modo e outro instante: a resposta continua sendo a do modo e da hora originais
    depois = agora + timedelta(minutes=10)
    repo.projetar_respostas(conn, sessao_id, {"sinal_a": _fato(True)}, [["sinal_a"]], "veterinario", depois)
    linha = _resposta(conn, sessao_id, "sinal_a")
    assert (linha["modo_na_resposta"], linha["respondida_em"]) == ("produtor", "2026-10-20T10:00:00")

    # só a posição mudou (a ordem não é o valor): atualiza a posição, mantém modo e hora
    repo.projetar_respostas(conn, sessao_id, {"sinal_a": _fato(True)}, [["x"], ["sinal_a"]], "veterinario", depois)
    linha = _resposta(conn, sessao_id, "sinal_a")
    assert (linha["ordem"], linha["modo_na_resposta"], linha["respondida_em"]) == (2, "produtor", "2026-10-20T10:00:00")

    # valor novo: modo e hora passam a ser os de agora
    repo.projetar_respostas(conn, sessao_id, {"sinal_a": _fato(False)}, [["sinal_a"]], "veterinario", depois)
    linha = _resposta(conn, sessao_id, "sinal_a")
    assert linha["valor_json"] == "false"
    assert (linha["modo_na_resposta"], linha["respondida_em"]) == ("veterinario", "2026-10-20T10:10:00")


def test_projetar_perguntas_insere_so_as_novas(conn: sqlite3.Connection, sessao_id: str, agora: datetime) -> None:
    perguntas = {"febre": {"id": 3, "tipo": "pergunta_feita", "simbolo": "febre", "motivo": {"resumo": "porque sim"}}}
    repo.projetar_perguntas(conn, sessao_id, perguntas, agora)

    depois = agora + timedelta(minutes=1)
    perguntas["febre"] = {**perguntas["febre"], "motivo": {"resumo": "alterado depois"}}
    perguntas["apetite"] = {"id": 5, "tipo": "pergunta_feita", "simbolo": "apetite", "motivo": {"resumo": "não comeu"}}
    repo.projetar_perguntas(conn, sessao_id, perguntas, depois)

    linhas = conn.execute("select * from perguntas_feitas order by ordem").fetchall()
    assert [(l["simbolo"], l["ordem"], l["feita_em"]) for l in linhas] == [
        ("febre", 1, "2026-10-20T10:00:00"),
        ("apetite", 2, "2026-10-20T10:01:00"),
    ]
    assert linhas[0]["motivo_json"] == '{"resumo": "porque sim"}'
    assert linhas[1]["motivo_json"] == '{"resumo": "não comeu"}'


# --- versões da base ------------------------------------------------------------------------


def _versao(conn: sqlite3.Connection, versao: str, agora: datetime, **extra: object) -> None:
    dados = {"pai": None, "autor": "teste", "data": "2026-10-20", "nota": "fixture", "hash": f"sha256:{versao}"}
    dados.update(extra)
    repo.sincronizar_versao(conn, versao=versao, agora=agora, **dados)


def test_sincronizar_versao_insere_so_se_faltar(conn: sqlite3.Connection, agora: datetime) -> None:
    _versao(conn, "v0002", agora, pai="v0001", nota="segunda")
    _versao(conn, "v0001", agora)
    _versao(conn, "v0001", agora + timedelta(hours=1), nota="repetida", hash="sha256:outro")
    versoes = repo.listar_versoes_base(conn)
    assert [v["versao"] for v in versoes] == ["v0001", "v0002"]
    assert versoes[0] == {
        "versao": "v0001",
        "pai": None,
        "autor": "teste",
        "data": "2026-10-20",
        "nota": "fixture",
        "hash": "sha256:v0001",
        "criada_em": "2026-10-20T10:00:00",
    }
    assert versoes[1]["pai"] == "v0001"


def test_sincronizar_versao_ignora_so_o_conflito_de_chave(conn: sqlite3.Connection, agora: datetime) -> None:
    # `INSERT OR IGNORE` engoliria também a violação de NOT NULL e a versão nunca seria registrada, sem aviso
    with pytest.raises(sqlite3.IntegrityError, match="NOT NULL"):
        _versao(conn, "v0001", agora, hash=None)
    assert repo.listar_versoes_base(conn) == []


# --- execuções de casos ---------------------------------------------------------------------


def _resultado(caso_id: str, status: str, **extra: object) -> dict:
    return {
        "caso_id": caso_id,
        "status": status,
        "obtido": {"top1": "d1", "motivo_parada": "limite"},
        "falhas": [] if status == "passou" else [{"campo": "top1", "esperado": "d2", "obtido": "d1"}],
        "extra": {"descricao": f"caso {caso_id}", "mudou_vs_pai": None},
        **extra,
    }


def test_execucao_conta_resultados(conn: sqlite3.Connection, agora: datetime) -> None:
    _versao(conn, "v0001", agora)
    primeira = repo.inserir_execucao(
        conn, versao="v0001", comparada_com=None, resultados=[_resultado("C-1", "passou")], agora=agora
    )
    depois = agora + timedelta(minutes=30)
    resultados = [_resultado("C-1", "passou"), _resultado("C-2", "falhou"), _resultado("C-3", "passou")]
    segunda = repo.inserir_execucao(conn, versao="v0001", comparada_com="v0000", resultados=resultados, agora=depois)
    assert (primeira, segunda) == ("ex_0001", "ex_0002")

    execucao = repo.obter_execucao(conn, segunda)
    assert (execucao["total"], execucao["passou"], execucao["falhou"]) == (3, 2, 1)
    assert execucao["versao"] == "v0001"
    assert execucao["comparada_com"] == "v0000"
    assert execucao["executada_em"] == "2026-10-20T10:30:00"
    assert [r["caso_id"] for r in execucao["resultados"]] == ["C-1", "C-2", "C-3"]
    assert execucao["resultados"][1] == resultados[1]
    assert repo.ultima_execucao(conn, "v0001") == execucao


def test_execucao_listagens(conn: sqlite3.Connection, agora: datetime) -> None:
    _versao(conn, "v0001", agora)
    _versao(conn, "v0002", agora, pai="v0001")
    assert repo.obter_execucao(conn, "ex_9999") is None
    assert repo.ultima_execucao(conn, "v0001") is None
    assert repo.listar_execucoes(conn, "v0001") == []
    for versao in ("v0001", "v0001", "v0002"):
        repo.inserir_execucao(conn, versao=versao, comparada_com=None, resultados=[_resultado("C-1", "passou")], agora=agora)

    cabecalhos = repo.listar_execucoes(conn, "v0001")
    assert [c["id"] for c in cabecalhos] == ["ex_0002", "ex_0001"]  # mais nova primeiro, mesmo no mesmo instante
    assert all("resultados" not in c for c in cabecalhos)
    assert repo.ultima_execucao(conn, "v0001")["id"] == "ex_0002"
    assert repo.ultima_execucao(conn, "v0002")["id"] == "ex_0003"


def test_execucao_sem_resultados_e_status_erro(conn: sqlite3.Connection, agora: datetime) -> None:
    _versao(conn, "v0001", agora)
    vazia = repo.inserir_execucao(conn, versao="v0001", comparada_com=None, resultados=[], agora=agora)
    assert {k: repo.obter_execucao(conn, vazia)[k] for k in ("total", "passou", "falhou", "resultados")} == {
        "total": 0, "passou": 0, "falhou": 0, "resultados": [],
    }
    malformado = {"caso_id": "C-X", "status": "erro", "obtido": None, "falhas": [], "extra": {"erro": "critério desconhecido"}}
    com_erro = repo.inserir_execucao(
        conn, versao="v0001", comparada_com=None, resultados=[malformado, _resultado("C-1", "passou")], agora=agora
    )
    execucao = repo.obter_execucao(conn, com_erro)
    assert execucao["total"] == 2 and execucao["passou"] == 1 and execucao["falhou"] == 0  # erro não é falha
    assert execucao["resultados"][0] == malformado


def test_execucao_exige_versao_sincronizada(conn: sqlite3.Connection, agora: datetime) -> None:
    with pytest.raises(sqlite3.IntegrityError):
        repo.inserir_execucao(conn, versao="v0099", comparada_com=None, resultados=[], agora=agora)
