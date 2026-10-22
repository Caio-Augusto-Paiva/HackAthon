"""OpenAPI versionado e teste de contrato (Task 12, 4.8).

``contratos/openapi.json`` é gerado pelo código (``python -m api.exportar_openapi``) e versionado: se uma rota ou um
schema mudar sem regenerar o arquivo, o primeiro teste falha. O resto confere que o documento descreve a API que existe:
os 27 ``operationId`` de ``CONTRATOS``, os erros no formato único da 4.4, os discriminadores e, num percurso real pela
API, que cada resposta segue o modelo registrado.
"""
from __future__ import annotations

import inspect
import json
import os
import subprocess
import sys
import tomllib
from pathlib import Path

import pydantic
import pytest
from pydantic import ValidationError

from api import exportar_openapi
from api.exportar_openapi import gerar_texto, main
from api.schemas.erro import ErroResposta
from api.schemas.registro import CONTRATOS
from api.schemas.sessao import EstadoSessao
from tests.api.apoio import validar_contrato

RAIZ = Path(__file__).resolve().parents[2]
OPENAPI_VERSIONADO = RAIZ / "contratos" / "openapi.json"
PASTA_EXEMPLOS = RAIZ / "contratos" / "exemplos"
# prontuário fictício: a base mínima só conhece a ficha `data_ultimo_parto`
PRONTUARIO_CSV = b"brinco,nome,data_ultimo_parto\nBR-0007,Estrela,2026-09-30\nBR-0001,Mimosa,2026-10-14\n"
METODOS = {"get", "post", "put", "patch", "delete"}
OPERACOES = sorted(CONTRATOS)

# Erros documentados por operação (Seção 4.4): 404 recurso inexistente, 409 conflito, 422 entrada recusada,
# 500 erro interno. ``saude`` e ``listar_versoes`` não recebem nada do cliente: só o 500 vale para elas.
ERROS_POR_OPERACAO: dict[str, set[str]] = {
    "saude": {"500"},
    "listar_versoes": {"500"},
    "listar_animais": {"422", "500"},
    "validar_base": {"422", "500"},
    "criar_animal": {"409", "422", "500"},
    "importar_animais": {"409", "422", "500"},
    "obter_animal": {"404", "422", "500"},
    "listar_sessoes_animal": {"404", "422", "500"},
    "criar_sessao": {"404", "409", "422", "500"},
    "obter_sessao": {"404", "422", "500"},
    "trocar_modo": {"404", "409", "422", "500"},
    "responder_triagem": {"404", "409", "422", "500"},
    "corrigir_triagem": {"404", "409", "422", "500"},
    "responder_pergunta": {"404", "409", "422", "500"},
    "corrigir_resposta": {"404", "409", "422", "500"},
    "acao_bandeira": {"404", "409", "422", "500"},
    "obter_parecer": {"404", "422", "500"},
    "obter_porque": {"404", "422", "500"},
    "obter_como": {"404", "422", "500"},
    "obter_traco": {"404", "422", "500"},
    "obter_versao": {"404", "422", "500"},
    "obter_grafo": {"404", "422", "500"},
    "salvar_versao": {"404", "409", "422", "500"},
    "ativar_versao": {"404", "409", "422", "500"},
    "executar_casos": {"404", "422", "500"},
    "listar_execucoes": {"404", "422", "500"},
    "obter_execucao": {"404", "422", "500"},
}


# --- apoio ---------------------------------------------------------------------------------------


@pytest.fixture(scope="module")
def openapi() -> dict:
    return json.loads(gerar_texto())


def _operacoes(documento: dict) -> dict[str, tuple[str, str, dict]]:
    """``operationId`` -> (método em minúsculas, rota, operação)."""
    return {
        op["operationId"]: (metodo, rota, op)
        for rota, itens in documento["paths"].items()
        for metodo, op in itens.items()
        if metodo in METODOS
    }


def _nome_do_schema(conteudo: dict) -> str:
    """O nome do schema referenciado no ``application/json`` de uma resposta ou corpo."""
    return conteudo["content"]["application/json"]["schema"]["$ref"].rsplit("/", 1)[-1]


def _status_de_sucesso(op: dict) -> int:
    return min(int(codigo) for codigo in op["responses"] if codigo.startswith("2"))


# --- o arquivo versionado ------------------------------------------------------------------------


def test_openapi_versionado_esta_atualizado():
    # read_text usa quebra de linha universal: um checkout com CRLF (core.autocrlf) não faz o teste falhar
    versionado = OPENAPI_VERSIONADO.read_text(encoding="utf-8")
    assert versionado == gerar_texto(), (
        "contratos/openapi.json está desatualizado: rode `python -m api.exportar_openapi` e faça commit"
    )


def test_gerar_texto_formato_estavel():
    texto = gerar_texto()
    documento = json.loads(texto)
    assert texto == json.dumps(documento, indent=2, sort_keys=True, ensure_ascii=False) + "\n"
    assert "Saúde do servidor" in texto  # UTF-8 direto, sem \uXXXX
    assert "\r" not in texto


def test_gerar_texto_igual_em_outro_processo():
    """A ordem das chaves e das listas não depende do hash aleatório do Python (PYTHONHASHSEED)."""
    codigo = "import sys; from api.exportar_openapi import gerar_texto; sys.stdout.buffer.write(gerar_texto().encode('utf-8'))"
    saida = subprocess.run(
        [sys.executable, "-c", codigo], cwd=RAIZ, env={**os.environ, "PYTHONHASHSEED": "12345"},
        capture_output=True, check=True, timeout=60,
    ).stdout
    assert saida.decode("utf-8") == gerar_texto()


def test_gerar_texto_nao_toca_no_disco(tmp_path: Path, monkeypatch: pytest.MonkeyPatch):
    """Sem lifespan e sem tocar nos caminhos do ambiente: nem o banco, nem a base, nem a pasta ``dados``."""
    monkeypatch.chdir(tmp_path)
    monkeypatch.setenv("ANAMNESE_DB", str(tmp_path / "dados" / "anamnese.db"))
    monkeypatch.setenv("ANAMNESE_BASE_DIR", str(tmp_path / "base"))
    chamadas: list = []
    monkeypatch.setattr("api.main.inicializar", lambda *a, **k: chamadas.append(a))  # o lifespan cria o esquema
    configs = []
    criar_app_real = exportar_openapi.criar_app
    monkeypatch.setattr(exportar_openapi, "criar_app", lambda config=None: configs.append(config) or criar_app_real(config))

    texto = gerar_texto()

    assert texto.startswith("{")
    assert chamadas == []
    assert list(tmp_path.iterdir()) == []
    [config] = configs
    assert config is not None  # configuração neutra, não a do ambiente
    for caminho in (config.db_path, config.db_path.parent, config.base_dir, config.web_dist):
        assert not caminho.exists()


def test_main_grava_utf8_com_lf(tmp_path: Path):
    destino = tmp_path / "pasta_nova" / "openapi.json"
    main(destino)
    bruto = destino.read_bytes()
    assert b"\r" not in bruto
    assert bruto.decode("utf-8") == gerar_texto()


def test_destino_padrao_e_o_arquivo_versionado():
    padrao = inspect.signature(main).parameters["destino"].default
    assert Path(padrao).resolve() == OPENAPI_VERSIONADO.resolve()  # vale de qualquer pasta de execução


# --- operações e schemas -------------------------------------------------------------------------


def test_operation_ids_batem_com_contratos(openapi):
    ids = [op["operationId"] for itens in openapi["paths"].values() for m, op in itens.items() if m in METODOS]
    assert len(ids) == len(set(ids)) == 27
    assert set(ids) == set(CONTRATOS)
    assert all(rota.startswith("/api/") for rota in openapi["paths"])


@pytest.mark.parametrize("operation_id", OPERACOES)
def test_modelos_do_openapi_batem_com_contratos(openapi, operation_id: str):
    modelo_corpo, modelo_resposta = CONTRATOS[operation_id]
    _, _, op = _operacoes(openapi)[operation_id]

    assert _nome_do_schema(op["responses"][str(_status_de_sucesso(op))]) == modelo_resposta.__name__
    corpo = op.get("requestBody")
    if modelo_corpo is None:  # GET, ou a importação, que é multipart
        assert corpo is None or "application/json" not in corpo["content"]
    else:
        assert _nome_do_schema(corpo) == modelo_corpo.__name__


@pytest.mark.parametrize("operation_id", OPERACOES)
def test_exemplo_descreve_a_rota_do_openapi(openapi, operation_id: str):
    exemplo = json.loads((PASTA_EXEMPLOS / f"{operation_id}.json").read_text(encoding="utf-8"))
    metodo, rota, op = _operacoes(openapi)[operation_id]
    assert (exemplo["metodo"].lower(), exemplo["rota"]) == (metodo, rota)
    assert exemplo["status"] == _status_de_sucesso(op)


def test_sem_schemas_input_output_duplicados(openapi):
    nomes = openapi["components"]["schemas"]
    assert not [n for n in nomes if n.endswith(("-Input", "-Output"))]


def test_discriminadores_literais(openapi):
    schemas = openapi["components"]["schemas"]

    # `proxima` é `X | None`: o discriminador fica na alternativa da união, não na propriedade
    proxima = schemas["EstadoSessao"]["properties"]["proxima"]
    alternativa = proxima["anyOf"][0]
    assert alternativa["discriminator"]["propertyName"] == "tipo"
    assert alternativa["discriminator"]["mapping"] == {
        "tela_triagem": "#/components/schemas/TelaTriagem",
        "pergunta": "#/components/schemas/PerguntaDinamica",
    }
    assert {"type": "null"} in proxima["anyOf"]
    assert schemas["TelaTriagem"]["properties"]["tipo"]["const"] == "tela_triagem"
    assert schemas["PerguntaDinamica"]["properties"]["tipo"]["const"] == "pergunta"

    # o nó do grafo é bipartido: `tipo_no` é um enum fechado, não um texto livre
    assert schemas["No"]["properties"]["tipo_no"]["enum"] == ["simbolo", "regra"]
    # a aresta tem papel fechado: `condicao` (símbolo -> regra) ou `conclusao` (regra -> símbolo)
    assert schemas["Aresta"]["properties"]["papel"]["enum"] == ["condicao", "conclusao"]

    # o discriminador está ligado no modelo (não é só uma união simples): tipo desconhecido é `union_tag_invalid`
    exemplo = json.loads((PASTA_EXEMPLOS / "obter_sessao.json").read_text(encoding="utf-8"))["resposta"]
    with pytest.raises(ValidationError) as erro:
        EstadoSessao.model_validate({**exemplo, "proxima": {**exemplo["proxima"], "tipo": "outra"}})
    assert [e["type"] for e in erro.value.errors()] == ["union_tag_invalid"]


def test_pydantic_fixado_na_versao_instalada():
    """Um patch do Pydantic pode mudar o texto do JSON Schema: o ``openapi.json`` versionado depende da versão exata."""
    dependencias = tomllib.loads((RAIZ / "pyproject.toml").read_text(encoding="utf-8"))["project"]["dependencies"]
    assert f"pydantic=={pydantic.VERSION}" in dependencias


# --- erros documentados --------------------------------------------------------------------------


def test_tabela_de_erros_cobre_as_27_operacoes():
    assert set(ERROS_POR_OPERACAO) == set(CONTRATOS)


@pytest.mark.parametrize("operation_id", OPERACOES)
def test_cada_rota_tem_resposta_de_erro_documentada(openapi, operation_id: str):
    _, _, op = _operacoes(openapi)[operation_id]
    erros = {codigo: resposta for codigo, resposta in op["responses"].items() if codigo[0] in "45"}

    assert set(erros) == ERROS_POR_OPERACAO[operation_id]
    # toda operação que recebe algo do cliente documenta o 422; o formato é sempre o único da 4.4
    if op.get("parameters") or op.get("requestBody"):
        assert "422" in erros
    for codigo, resposta in erros.items():
        assert _nome_do_schema(resposta) == ErroResposta.__name__, codigo
        assert resposta["description"]


def test_422_padrao_do_fastapi_nao_aparece(openapi):
    """O 422 real usa o formato da 4.4 (``ErroResposta``), não o ``HTTPValidationError`` do FastAPI."""
    schemas = openapi["components"]["schemas"]
    assert "HTTPValidationError" not in schemas and "ValidationError" not in schemas
    assert "ErroResposta" in schemas


def test_erros_reais_seguem_o_schema_documentado(cliente):
    """Um 404, um 409 e um 422 de verdade têm o corpo de ``ErroResposta`` e o código esperado."""
    animal = {"brinco": "BR-0001", "nome": "Mimosa", "ficha": {"data_ultimo_parto": "2026-10-14"}}
    assert cliente.post("/api/animais", json=animal).status_code == 201
    casos = [
        (cliente.get("/api/animais/an_9999"), 404, "nao_encontrado"),
        (cliente.post("/api/animais", json=animal), 409, "conflito"),
        (cliente.post("/api/animais", json={"brinco": "BR-0002", "extra": 1}), 422, "entrada_invalida"),
    ]
    for resposta, status, codigo in casos:
        assert resposta.status_code == status, resposta.text
        assert ErroResposta.model_validate(resposta.json()).erro.codigo == codigo
        assert resposta.headers["X-Requisicao-Id"] == resposta.json()["erro"]["requisicao_id"]


# --- a API de verdade ----------------------------------------------------------------------------


class Percurso:
    """Chama a API pelas rotas que o OpenAPI descreve e valida cada resposta com o modelo de ``CONTRATOS``."""

    def __init__(self, cliente, documento: dict):
        self.cliente = cliente
        self.operacoes = _operacoes(documento)
        self.cobertas: set[str] = set()

    def chamar(self, operation_id: str, *, caminho: dict | None = None, **requisicao) -> dict:
        metodo, rota, op = self.operacoes[operation_id]
        resposta = self.cliente.request(metodo.upper(), rota.format(**(caminho or {})), **requisicao)
        assert resposta.status_code == _status_de_sucesso(op), f"{operation_id}: {resposta.status_code} {resposta.text}"
        corpo = resposta.json()
        validar_contrato(operation_id, corpo)
        self.cobertas.add(operation_id)
        return corpo


def _casos_sem_falha(arquivo: Path) -> None:
    """O ``C-FALHA`` da fixture falha de propósito; aqui passa a esperar o ``top1`` que o motor devolve."""
    casos = json.loads(arquivo.read_text(encoding="utf-8"))
    next(c for c in casos if c["id"] == "C-FALHA")["esperado"] = {"top1": "d1"}
    arquivo.write_text(json.dumps(casos, ensure_ascii=False, indent=2), encoding="utf-8")


def test_resposta_real_valida_pelo_contrato(cliente, com_casos: Path, openapi):
    """Do animal aos casos de teste: cada resposta da API real passa pelo modelo da sua operação (os 27)."""
    p = Percurso(cliente, openapi)
    _casos_sem_falha(com_casos)

    # sistema e animais
    assert p.chamar("saude")["status"] == "ok"
    animal = p.chamar(
        "criar_animal", json={"brinco": "BR-0001", "nome": "Mimosa", "ficha": {"data_ultimo_parto": "2026-10-14"}}
    )
    importacao = p.chamar(
        "importar_animais", files={"arquivo": ("prontuario.csv", PRONTUARIO_CSV, "text/csv")}
    )
    assert importacao["gravado"] is True and len(importacao["criados"]) == 1
    assert p.chamar("listar_animais")["total"] == 2
    assert p.chamar("obter_animal", caminho={"animal_id": animal["id"]})["brinco"] == "BR-0001"

    # sessão do produtor: triagem, pergunta dinâmica e correções
    estado = p.chamar("criar_sessao", json={"animal_id": animal["id"], "modo": "produtor"})
    sessao = {"sessao_id": estado["sessao_id"]}
    assert estado["proxima"]["tipo"] == "tela_triagem"
    assert p.chamar("obter_sessao", caminho=sessao) == estado
    tela = {**sessao, "tela_id": estado["proxima"]["tela_id"]}
    sinais = {"valores": {"sinal_a": True, "sinal_b": False}}
    estado = p.chamar("responder_triagem", caminho=tela, json=sinais)
    assert estado["proxima"]["tipo"] == "pergunta"
    pergunta = estado["proxima"]["simbolo"]
    assert p.chamar("obter_porque", caminho={**sessao, "simbolo": pergunta})["simbolo"] == pergunta
    p.chamar("corrigir_triagem", caminho=tela, json={"valores": {"sinal_a": False, "sinal_b": False}})
    p.chamar("corrigir_triagem", caminho=tela, json=sinais)
    p.chamar("responder_pergunta", caminho=sessao, json={"simbolo": pergunta, "valor": True})
    p.chamar("corrigir_resposta", caminho={**sessao, "simbolo": pergunta}, json={"valor": True})

    # modo veterinário: aparece a pergunta que só ele faz
    estado = p.chamar("trocar_modo", caminho=sessao, json={"modo": "veterinario"})
    assert estado["modo"] == "veterinario" and estado["proxima"]["tipo"] == "pergunta"
    p.chamar("responder_pergunta", caminho=sessao, json={"simbolo": estado["proxima"]["simbolo"], "valor": True})

    # parecer e explicações
    parecer = p.chamar("obter_parecer", caminho=sessao)
    assert parecer["final"] is True
    doenca = parecer["blocos"][0]["itens"][0]["doenca"]
    assert p.chamar("obter_como", caminho={**sessao, "simbolo": doenca})["simbolo"] == doenca
    assert p.chamar("obter_traco", caminho=sessao)["eventos"]  # há traço: a sessão disparou regras

    # bandeira vermelha numa segunda sessão do mesmo animal
    segunda = p.chamar("criar_sessao", json={"animal_id": animal["id"], "modo": "produtor"})
    alerta = p.chamar(
        "responder_triagem",
        caminho={"sessao_id": segunda["sessao_id"], "tela_id": segunda["proxima"]["tela_id"]},
        json={"valores": {"sinal_a": False, "sinal_b": True}},
    )
    assert alerta["alerta"]["nivel"] == "chamar_agora"
    p.chamar("acao_bandeira", caminho={"sessao_id": segunda["sessao_id"]}, json={"acao": "ver_parecer"})
    assert len(p.chamar("listar_sessoes_animal", caminho={"animal_id": animal["id"]})["itens"]) == 2

    # base: leitura, edição, execução dos casos e ativação
    versoes = p.chamar("listar_versoes")
    ativa = versoes["ativa"]
    base = p.chamar("obter_versao", caminho={"versao": ativa})
    assert base["meta"]["versao"] == ativa
    grafo = p.chamar("obter_grafo", caminho={"versao": ativa})
    edicao = {
        "pai": ativa,
        "nota": "sem mudança de CF: só exercita a rota",
        "meta": grafo["meta"],
        "grafo": {"nos": grafo["nos"], "arestas": grafo["arestas"]},
        "layout": grafo["layout"],
    }
    assert p.chamar("validar_base", json=edicao)["valida"] is True
    salva = p.chamar("salvar_versao", json=edicao)
    nova = {"versao": salva["versao"]}
    execucao = p.chamar("executar_casos", caminho=nova, json={"casos": None})
    listadas = p.chamar("listar_execucoes", caminho=nova)
    assert execucao["execucao_id"] in [e["execucao_id"] for e in listadas["itens"]]
    lida = p.chamar("obter_execucao", caminho={**nova, "execucao_id": execucao["execucao_id"]})
    assert lida["execucao_id"] == execucao["execucao_id"]
    assert p.chamar("ativar_versao", json={"versao": salva["versao"]})["anterior"] == ativa

    assert p.cobertas == set(CONTRATOS), f"sem cobertura: {sorted(set(CONTRATOS) - p.cobertas)}"


# --- documentação interativa ---------------------------------------------------------------------


def test_docs_em_api_docs(cliente, openapi):
    docs = cliente.get("/api/docs")
    assert docs.status_code == 200
    assert "text/html" in docs.headers["content-type"]
    assert "/api/openapi.json" in docs.text

    esquema = cliente.get("/api/openapi.json")
    assert esquema.status_code == 200
    assert esquema.json() == openapi  # o que a API serve é o que se versiona
