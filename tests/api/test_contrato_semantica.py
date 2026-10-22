"""Semântica do contrato para o frontend: descrições no OpenAPI, campos obrigatórios na resposta e o README.

O frontend gera tipos do ``contratos/openapi.json``: um campo que o servidor sempre envia (mesmo ``null``) tem de
ser obrigatório no schema de resposta, senão vira ``campo?: T`` e esconde um erro de digitação. Corpos de
requisição não mudam: o cliente continua podendo omitir o que tem padrão.
"""
from __future__ import annotations

import json
from pathlib import Path

import pytest

RAIZ = Path(__file__).resolve().parents[2]
PASTA_EXEMPLOS = RAIZ / "contratos" / "exemplos"
README = RAIZ / "api" / "README.md"


@pytest.fixture(scope="module")
def schemas() -> dict:
    from api.exportar_openapi import gerar_texto

    return json.loads(gerar_texto())["components"]["schemas"]


# --- descrições ---------------------------------------------------------------------------------

DESCRICOES = {
    ("EstadoSessao", "proxima"): ["null", "encerrada", "pausada"],
    ("EstadoSessao", "fase"): ["ver_parecer", "reabre"],
    ("Alerta", "pausa"): ["ver_parecer", "false"],
    ("Alerta", "acoes"): ["ver_parecer", "[]"],
    ("Parecer", "final"): ["motivo_parada", "null", "ver_parecer"],
    ("Parecer", "motivo_parada"): ["null", "ver_parecer"],
    ("ServeA", "cf_atual"): ["momento", "pergunta"],
    ("PerguntaDinamica", "motivo_resumo"): ["congelado", "primeira"],
}


@pytest.mark.parametrize(("modelo", "campo"), sorted(DESCRICOES))
def test_campo_semantico_tem_descricao_em_portugues(schemas, modelo, campo):
    descricao = schemas[modelo]["properties"][campo].get("description", "")
    assert descricao, f"{modelo}.{campo} sem description"
    for trecho in DESCRICOES[(modelo, campo)]:
        assert trecho in descricao, f"{modelo}.{campo}: faltou '{trecho}' em {descricao!r}"


# --- obrigatórios na resposta -----------------------------------------------------------------

OBRIGATORIOS = {
    "UrgenciaEstado": ["regras"],
    "Campo": ["rotulo", "opcoes", "unidade", "min", "max"],
    "PerguntaDinamica": ["opcoes", "unidade", "min", "max"],
    "SalvarResposta": ["execucao_pai"],
    "ResultadoCaso": ["mudou_vs_pai", "obtido", "erro"],
    "Entrada": ["evidencias"],
}


@pytest.mark.parametrize("modelo", sorted(OBRIGATORIOS))
def test_campos_que_o_servidor_sempre_envia_sao_obrigatorios_na_resposta(schemas, modelo):
    obrigatorios = set(schemas[modelo]["required"])
    assert set(OBRIGATORIOS[modelo]) <= obrigatorios
    assert obrigatorios == set(schemas[modelo]["properties"])  # o servidor envia todos, inclusive os null


REQUISICOES = {
    "NovaSessao": {"animal_id", "modo"},  # versao_base continua opcional
    "RespostaTriagem": set(),
    "RespostaPergunta": {"simbolo"},
    "CorrecaoPergunta": set(),
    "AcaoBandeira": {"acao"},
    "TrocaModo": {"modo"},
    "NovoAnimal": {"brinco", "nome"},  # ficha continua opcional
    "EdicaoBase": {"pai", "nota", "meta", "grafo"},  # layout continua opcional
    "AtivarBody": {"versao"},
    "ExecutarBody": set(),
}


@pytest.mark.parametrize("modelo", sorted(REQUISICOES))
def test_corpos_de_requisicao_nao_mudam(schemas, modelo):
    assert set(schemas[modelo].get("required", [])) == REQUISICOES[modelo]


def _faltas(schemas: dict, schema: dict, valor, caminho: str = "") -> list[str]:
    """As chaves ``required`` que faltam no ``valor``, descendo pelos objetos, listas e uniões."""
    if "$ref" in schema:
        return _faltas(schemas, schemas[schema["$ref"].rsplit("/", 1)[1]], valor, caminho)
    for uniao in ("anyOf", "oneOf"):
        if uniao in schema:
            todas = [_faltas(schemas, ramo, valor, caminho) for ramo in schema[uniao]]
            return min(todas, key=len) if todas else []
    if isinstance(valor, dict):
        faltas = [f"{caminho}.{chave}" for chave in schema.get("required", []) if chave not in valor]
        for chave, filho in schema.get("properties", {}).items():
            if chave in valor:
                faltas += _faltas(schemas, filho, valor[chave], f"{caminho}.{chave}")
        return faltas
    if isinstance(valor, list) and "items" in schema:
        return [f for i, v in enumerate(valor) for f in _faltas(schemas, schema["items"], v, f"{caminho}[{i}]")]
    return []


def test_exemplos_trazem_todos_os_campos_obrigatorios(schemas):
    from api.schemas.registro import CONTRATOS

    for operacao, (_, modelo) in sorted(CONTRATOS.items()):
        exemplo = json.loads((PASTA_EXEMPLOS / f"{operacao}.json").read_text(encoding="utf-8"))
        nome = modelo.__name__
        if nome not in schemas:
            continue
        assert _faltas(schemas, {"$ref": f"#/components/schemas/{nome}"}, exemplo["resposta"]) == [], operacao


def test_respostas_reais_trazem_todos_os_campos_obrigatorios(schemas, cliente):
    from tests.api.apoio import criar_animal_teste, criar_sessao_teste

    animal = criar_animal_teste(cliente)
    estado = criar_sessao_teste(cliente, animal["id"])
    assert _faltas(schemas, {"$ref": "#/components/schemas/EstadoSessao"}, estado) == []
    cliente.post(f"/api/sessoes/{estado['sessao_id']}/triagem/sinais", json={"valores": {"sinal_a": True, "sinal_b": False}})
    cliente.post(f"/api/sessoes/{estado['sessao_id']}/respostas", json={"simbolo": "pergunta_x", "valor": True})
    como = cliente.get(f"/api/sessoes/{estado['sessao_id']}/como/d1").json()
    assert _faltas(schemas, {"$ref": "#/components/schemas/Como"}, como) == []
    atual = cliente.get(f"/api/sessoes/{estado['sessao_id']}").json()
    assert _faltas(schemas, {"$ref": "#/components/schemas/EstadoSessao"}, atual) == []


# --- README -----------------------------------------------------------------------------------


def test_readme_tem_a_secao_para_o_frontend():
    texto = README.read_text(encoding="utf-8")
    assert "## Para o frontend" in texto
    secao = texto.split("## Para o frontend", 1)[1]
    for trecho in (
        "proxima",
        "ver_parecer",
        "conflito",
        "GET",
        "POST /animais/importacao",
        "vNNNN.json",
    ):
        assert trecho in secao, trecho
