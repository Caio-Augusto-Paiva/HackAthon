"""Esqueleto do app, configuração e formato único de erro (Task 1)."""
from pathlib import Path

import pytest
from fastapi import FastAPI, Request
from pydantic import BaseModel, ConfigDict

from api.config import carregar_configuracao
from api.erros import conflito
from api.main import criar_app


class _Corpo(BaseModel):
    n: int


class _ComPadrao(BaseModel):
    # sem este config o Pydantic não distingue entrada e saída e o teste não discriminaria
    model_config = ConfigDict(json_schema_serialization_defaults_required=True)
    x: int = 0


@pytest.fixture
def app(config) -> FastAPI:
    """O app real mais rotas de teste que exercitam cada caminho de erro."""
    app = criar_app(config)

    def com_corpo(dados: _Corpo) -> dict:
        return {"n": dados.n}

    app.state.ids_vistos = []  # ids que o middleware pôs em request.state nas rotas que quebram

    def quebra(request: Request) -> None:
        app.state.ids_vistos.append(request.state.requisicao_id)
        raise RuntimeError("segredo")

    def duplicada() -> None:
        raise conflito("x", codigo="ja_respondida")

    def com_padrao(dados: _ComPadrao) -> _ComPadrao:
        return dados

    app.add_api_route("/api/teste/corpo", com_corpo, methods=["POST"])
    app.add_api_route("/api/teste/padrao", com_padrao, methods=["POST"])
    app.add_api_route("/api/teste/quebra", quebra, methods=["GET"])
    app.add_api_route("/api/teste/conflito", duplicada, methods=["GET"])
    return app


def test_saude_ok(cliente):
    resposta = cliente.get("/api/saude")
    assert resposta.status_code == 200
    assert resposta.json() == {"status": "ok", "versao_api": "0.1.0"}
    assert resposta.headers["X-Requisicao-Id"].startswith("rq_")


def test_404_rota_inexistente_formato_unico(cliente):
    resposta = cliente.get("/api/nao_existe")
    assert resposta.status_code == 404
    corpo = resposta.json()
    assert set(corpo) == {"erro"}
    assert corpo["erro"]["codigo"] == "nao_encontrado"
    assert corpo["erro"]["requisicao_id"].startswith("rq_")
    assert "detalhes" not in corpo["erro"]


def test_405_metodo_nao_permitido(cliente):
    resposta = cliente.post("/api/saude")
    assert resposta.status_code == 405
    assert resposta.json()["erro"]["codigo"] == "metodo_nao_permitido"
    assert "GET" in resposta.headers["Allow"]


def test_422_entrada_invalida_substitui_padrao(cliente):
    resposta = cliente.post("/api/teste/corpo", json={"n": "valor_enviado"})
    assert resposta.status_code == 422
    corpo = resposta.json()
    assert "detail" not in corpo
    assert corpo["erro"]["codigo"] == "entrada_invalida"
    detalhes = corpo["erro"]["detalhes"]
    assert detalhes[0]["severidade"] == "erro"
    assert detalhes[0]["mensagem"].startswith("corpo.n: ")  # campo por detalhe
    assert "valor_enviado" not in resposta.text  # o valor enviado não volta na resposta


def test_500_sem_detalhe_tecnico(cliente):
    resposta = cliente.get("/api/teste/quebra")
    assert resposta.status_code == 500
    corpo = resposta.json()
    assert corpo["erro"]["codigo"] == "erro_interno"
    assert corpo["erro"]["mensagem"] == "Erro interno. Tente novamente."
    assert "detalhes" not in corpo["erro"]
    assert "segredo" not in resposta.text
    assert "RuntimeError" not in resposta.text


def test_requisicao_id_no_cabecalho_igual_ao_corpo(cliente):
    respostas = [
        cliente.get("/api/nao_existe"),
        cliente.post("/api/teste/corpo", json={"n": "x"}),
        cliente.get("/api/teste/conflito"),
        cliente.get("/api/teste/quebra"),
    ]
    ids = set()
    for resposta in respostas:
        id_corpo = resposta.json()["erro"]["requisicao_id"]
        assert resposta.headers["X-Requisicao-Id"] == id_corpo
        assert len(id_corpo) == len("rq_") + 4 and int(id_corpo[3:], 16) >= 0
        ids.add(id_corpo)
    assert len(ids) > 1  # um id por requisição
    # o handler do 500 roda fora do middleware, mas reaproveita o id que ele pôs no estado
    assert cliente.app.state.ids_vistos == [respostas[-1].json()["erro"]["requisicao_id"]]


def test_erro_api_dominio(cliente):
    resposta = cliente.get("/api/teste/conflito")
    assert resposta.status_code == 409
    corpo = resposta.json()
    assert corpo["erro"]["codigo"] == "ja_respondida"
    assert corpo["erro"]["mensagem"] == "x"


def test_docs_e_openapi_sob_o_prefixo_api(cliente):
    assert cliente.get("/api/docs").status_code == 200
    esquema = cliente.get("/api/openapi.json").json()
    assert esquema["paths"]["/api/saude"]["get"]["operationId"] == "saude"
    assert cliente.get("/docs").status_code == 404


def test_openapi_sem_esquemas_separados_de_entrada_e_saida(cliente):
    esquemas = cliente.get("/api/openapi.json").json()["components"]["schemas"]
    assert "_ComPadrao" in esquemas
    assert not [nome for nome in esquemas if nome.endswith(("-Input", "-Output"))]


def test_config_le_ambiente(monkeypatch, tmp_path):
    destino = tmp_path / "outro.db"
    monkeypatch.setenv("ANAMNESE_DB", str(destino))
    monkeypatch.setenv("ANAMNESE_BASE_DIR", str(tmp_path / "minha_base"))
    config = carregar_configuracao()
    assert config.db_path == destino
    assert config.base_dir == tmp_path / "minha_base"

    monkeypatch.delenv("ANAMNESE_DB")
    monkeypatch.delenv("ANAMNESE_BASE_DIR")
    padrao = carregar_configuracao()
    assert padrao.db_path == Path("dados/anamnese.db")
    assert padrao.base_dir == Path("base")
    assert padrao.web_dist == Path("web/dist")
