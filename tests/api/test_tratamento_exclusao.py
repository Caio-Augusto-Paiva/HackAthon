"""Tratamento no parecer, frase de exclusão no "como?" e sessão presa à versão em que nasceu (Tarefa 3)."""
from __future__ import annotations

from tests.api.apoio import criar_animal_teste, criar_sessao_teste, validar_contrato

BASE = "/api/sessoes/ses_0001"
URL = "https://www.embrapa.br/busca-de-publicacoes/-/publicacao/d1"
SINAIS = {"valores": {"sinal_a": True, "sinal_b": False}}


def _com_tratamento(dados: dict) -> None:
    d1 = next(s for s in dados["simbolos"] if s["id"] == "d1")
    d1["tratamento"] = {"titulo": "Manejo da doença D1", "url": URL}


def _com_par_excludente(dados: dict) -> None:
    dados["simbolos"].append(
        {"id": "d2", "tipo": "doenca", "nome": "Doença D2", "dominio": {"tipo": "booleano"}, "gravidade": "media"}
    )
    dados["regras"].append(
        {"id": "R-D2-01", "se": [{"simbolo": "sinal_a"}], "entao": {"simbolo": "d2", "cf": 0.3},
         "fonte": "fixture de software", "status": "validada", "nota": "fixture de software"}
    )
    dados["meta"]["exclusoes"] = [{"doencas": ["d1", "d2"], "fonte": "fixture de software", "nota": "par de teste"}]


def _sessao(cliente) -> None:
    animal = criar_animal_teste(cliente)
    criar_sessao_teste(cliente, animal["id"])
    resposta = cliente.post(f"{BASE}/triagem/sinais", json=SINAIS)
    assert resposta.status_code == 200, resposta.text


def _itens(parecer: dict) -> dict:
    return {i["doenca"]: i for b in parecer["blocos"] for i in b["itens"]}


def test_parecer_traz_tratamento_da_base(cliente_com):
    _, cliente = cliente_com(_com_tratamento)
    _sessao(cliente)
    resposta = cliente.get(f"{BASE}/parecer")
    assert resposta.status_code == 200, resposta.text
    validar_contrato("obter_parecer", resposta.json())
    assert _itens(resposta.json())["d1"]["tratamento"] == {"titulo": "Manejo da doença D1", "url": URL}


def test_parecer_tratamento_nulo_sem_campo(cliente):
    _sessao(cliente)
    item = _itens(cliente.get(f"{BASE}/parecer").json())["d1"]
    assert "tratamento" in item and item["tratamento"] is None


def test_como_frase_exclusao(cliente_com):
    _, cliente = cliente_com(_com_par_excludente)
    _sessao(cliente)
    resposta = cliente.get(f"{BASE}/como/d2")
    assert resposta.status_code == 200, resposta.text
    corpo = resposta.json()
    validar_contrato("obter_como", corpo)
    assert len(corpo["exclusoes"]) == 1
    etapa = corpo["exclusoes"][0]
    assert etapa["tipo"] == "exclusao" and etapa["por"] == "d1"
    assert etapa["frase"] == "Ficou menos provável porque Doença D1 ficou mais forte, e as duas não costumam ocorrer juntas."
    assert etapa["depois"] < etapa["antes"]
    assert cliente.get(f"{BASE}/como/d1").json()["exclusoes"] == []


def test_sessao_v0004_restaura_apos_ativar_v0005(cliente):
    """A sessão fica presa à versão em que nasceu: ativar outra depois não a quebra."""
    _sessao(cliente)
    antes = cliente.get(f"{BASE}/parecer").json()
    grafo = cliente.get("/api/base/versoes/v0001/grafo").json()
    corpo = {"pai": "v0001", "nota": "nova versão", "meta": grafo["meta"],
             "grafo": {"nos": grafo["nos"], "arestas": grafo["arestas"]}, "layout": grafo["layout"]}
    salva = cliente.post("/api/base/versoes", json=corpo)
    assert salva.status_code == 201, salva.text
    nova = salva.json()["versao"]
    assert cliente.put("/api/base/ativa", json={"versao": nova, "confirmar_falhas": True}).status_code == 200
    resposta = cliente.get(f"{BASE}/parecer")
    assert resposta.status_code == 200, resposta.text
    assert resposta.json()["versao_base"] == "v0001"
    assert set(_itens(resposta.json())) == set(_itens(antes))
