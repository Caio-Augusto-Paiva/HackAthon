"""Esqueleto do app, configuração e formato único de erro (Task 1)."""
import logging
from datetime import date
from pathlib import Path
from typing import Literal
from uuid import UUID

import pytest
from fastapi import FastAPI, HTTPException, Request
from pydantic import BaseModel, ConfigDict, Field

from api.config import carregar_configuracao
from api.erros import (
    base_invalida,
    conflito,
    importacao_invalida,
    nao_encontrado,
    resposta_invalida,
    simbolo_invalido,
)
from api.main import criar_app
from kb.validador import Alvo, Problema


class _Corpo(BaseModel):
    n: int


class _ComPadrao(BaseModel):
    # sem este config o Pydantic não distingue entrada e saída e o teste não discriminaria
    model_config = ConfigDict(json_schema_serialization_defaults_required=True)
    x: int = 0


class _ComUuid(BaseModel):
    u: UUID


class _Restrito(BaseModel):
    model_config = ConfigDict(extra="forbid")
    curto: str = Field(min_length=3)
    longo: str = Field(max_length=2)
    maior: int = Field(gt=10)
    maior_igual: int = Field(ge=10)
    menor: int = Field(lt=10)
    menor_igual: int = Field(le=10)
    data: date
    poucos: list[int] = Field(min_length=2)
    muitos: list[int] = Field(max_length=1)
    modo: Literal["a", "b"]


def _problema() -> dict:
    """Um item como o relatório do validador da base o entrega (com ``numero``, que não vai ao cliente)."""
    return Problema(
        codigo="camada",
        numero="E07",
        severidade="erro",
        alvo=Alvo(tipo="regra", id="R-MAS-99"),
        mensagem="Regra de doença lê outra doença.",
    ).model_dump(mode="json")


# nome -> (fábrica, status, código), conforme a tabela da 4.4
FABRICAS = {
    "nao_encontrado": (lambda: nao_encontrado("Sessão não encontrada."), 404, "nao_encontrado"),
    "conflito": (lambda: conflito("Brinco já cadastrado."), 409, "conflito"),
    "conflito_ja_respondida": (
        lambda: conflito("Tela já respondida.", codigo="ja_respondida"),
        409,
        "ja_respondida",
    ),
    "resposta_invalida": (lambda: resposta_invalida("Valor fora do domínio."), 422, "resposta_invalida"),
    "base_invalida": (lambda: base_invalida("A base tem 1 erro.", [_problema()]), 422, "base_invalida"),
    "simbolo_invalido": (lambda: simbolo_invalido("Símbolo sem explicação."), 422, "simbolo_invalido"),
    "importacao_invalida": (lambda: importacao_invalida("Arquivo ilegível."), 422, "importacao_invalida"),
}


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

    def com_uuid(dados: _ComUuid) -> dict:
        return {}

    def restrito(dados: _Restrito) -> dict:
        return {}

    def http(codigo: int) -> None:
        raise HTTPException(status_code=codigo, detail="detalhe_http", headers={"X-Extra": "1"})

    def fabrica(nome: str) -> None:
        raise FABRICAS[nome][0]()

    app.add_api_route("/api/teste/corpo", com_corpo, methods=["POST"])
    app.add_api_route("/api/teste/padrao", com_padrao, methods=["POST"])
    app.add_api_route("/api/teste/uuid", com_uuid, methods=["POST"])
    app.add_api_route("/api/teste/restrito", restrito, methods=["POST"])
    app.add_api_route("/api/teste/http/{codigo}", http, methods=["GET"])
    app.add_api_route("/api/teste/fabrica/{nome}", fabrica, methods=["GET"])
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


def test_422_json_malformado_em_portugues_sem_ecoar_o_corpo(cliente):
    resposta = cliente.post(
        "/api/teste/corpo", content='{"enviado_secreto": ', headers={"Content-Type": "application/json"}
    )
    assert resposta.status_code == 422
    detalhes = resposta.json()["erro"]["detalhes"]
    assert [(d["codigo"], d["mensagem"]) for d in detalhes] == [
        ("json_invalid", "corpo: O corpo não é um JSON válido.")
    ]
    assert "enviado_secreto" not in resposta.text


def test_422_tipo_nao_mapeado_vira_valor_invalido_sem_ecoar_o_valor(cliente):
    resposta = cliente.post("/api/teste/uuid", json={"u": "valor_enviado"})
    assert resposta.status_code == 422
    assert resposta.json()["erro"]["detalhes"] == [
        {"codigo": "uuid_parsing", "severidade": "erro", "mensagem": "corpo.u: Valor inválido."}
    ]
    assert "valor_enviado" not in resposta.text


def test_422_tipos_comuns_do_pydantic_em_portugues(cliente):
    resposta = cliente.post(
        "/api/teste/restrito",
        json={
            "curto": "a", "longo": "abc", "maior": 5, "maior_igual": 5, "menor": 50, "menor_igual": 50,
            "data": "nao_e_data", "poucos": [1], "muitos": [1, 2], "modo": "c", "intruso": 1,
        },
    )
    assert resposta.status_code == 422
    obtido = {d["codigo"]: d["mensagem"] for d in resposta.json()["erro"]["detalhes"]}
    abaixo, acima = "Valor abaixo do mínimo permitido.", "Valor acima do máximo permitido."
    mensagem_data = obtido.pop("date_parsing", None) or obtido.pop("date_from_datetime_parsing")
    assert mensagem_data == "corpo.data: Deve ser uma data válida (AAAA-MM-DD)."
    assert obtido == {
        "string_too_short": "corpo.curto: Texto curto demais.",
        "string_too_long": "corpo.longo: Texto longo demais.",
        "greater_than": f"corpo.maior: {abaixo}",
        "greater_than_equal": f"corpo.maior_igual: {abaixo}",
        "less_than": f"corpo.menor: {acima}",
        "less_than_equal": f"corpo.menor_igual: {acima}",
        "too_short": "corpo.poucos: Lista com poucos itens.",
        "too_long": "corpo.muitos: Lista com itens demais.",
        "literal_error": "corpo.modo: Valor fora das opções permitidas.",
        "extra_forbidden": "corpo.intruso: Campo não permitido.",
    }
    assert "Input should" not in resposta.text and "nao_e_data" not in resposta.text


@pytest.mark.parametrize(
    ("codigo_http", "status", "codigo"),
    [(400, 422, "entrada_invalida"), (413, 422, "entrada_invalida"), (503, 503, "erro_interno")],
)
def test_http_exception_de_outro_status_segue_a_tabela_da_4_4(cliente, codigo_http, status, codigo):
    resposta = cliente.get(f"/api/teste/http/{codigo_http}")
    assert resposta.status_code == status
    assert resposta.json()["erro"]["codigo"] == codigo
    assert "detalhe_http" not in resposta.text


def test_500_sem_detalhe_tecnico(cliente):
    resposta = cliente.get("/api/teste/quebra")
    assert resposta.status_code == 500
    corpo = resposta.json()
    assert corpo["erro"]["codigo"] == "erro_interno"
    assert corpo["erro"]["mensagem"] == "Erro interno. Tente novamente."
    assert "detalhes" not in corpo["erro"]
    assert "segredo" not in resposta.text
    assert "RuntimeError" not in resposta.text


def test_500_registra_o_id_e_a_excecao_no_log(cliente, caplog):
    with caplog.at_level(logging.ERROR, logger="api"):
        resposta = cliente.get("/api/teste/quebra")
    requisicao_id = resposta.json()["erro"]["requisicao_id"]
    registros = [r for r in caplog.records if r.name == "api"]
    assert len(registros) == 1
    assert requisicao_id in registros[0].getMessage()
    assert registros[0].exc_info[0] is RuntimeError  # o detalhe fica no servidor, nunca na resposta
    assert "segredo" not in resposta.text


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


@pytest.mark.parametrize("nome", FABRICAS)
def test_fabricas_de_erro_seguem_a_tabela_da_4_4(cliente, nome):
    _, status, codigo = FABRICAS[nome]
    resposta = cliente.get(f"/api/teste/fabrica/{nome}")
    assert resposta.status_code == status
    erro = resposta.json()["erro"]
    assert erro["codigo"] == codigo
    assert erro["mensagem"] and erro["requisicao_id"].startswith("rq_")
    if nome == "base_invalida":
        assert erro["detalhes"] == [
            {
                "codigo": "camada",
                "severidade": "erro",
                "alvo": {"tipo": "regra", "id": "R-MAS-99"},
                "mensagem": "Regra de doença lê outra doença.",
            }
        ]  # sem o "numero" do Problema
    else:
        assert "detalhes" not in erro


def test_docs_e_openapi_sob_o_prefixo_api(cliente):
    assert cliente.get("/api/docs").status_code == 200
    esquema = cliente.get("/api/openapi.json").json()
    assert esquema["paths"]["/api/saude"]["get"]["operationId"] == "saude"


@pytest.mark.parametrize("rota", ["/docs", "/redoc", "/docs/oauth2-redirect"])
def test_documentacao_fora_do_prefixo_api_da_404_no_formato_unico(cliente, rota):
    resposta = cliente.get(rota)
    assert resposta.status_code == 404
    assert resposta.json()["erro"]["codigo"] == "nao_encontrado"


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
