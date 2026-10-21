"""Salvar uma nova versão da base a partir do grafo e ativá-la (Task 11, 4.5.3).

Base mínima (``tests/fixtures/kb/base_minima.json``) e ``casos_minima.json``, dados fictícios. Os três casos da fixture:
``C-D1-OK`` e ``C-BV-OK`` passam; ``C-FALHA`` falha de propósito (o ``top1`` esperado não existe). Por isso a v0001 já
tem 1 caso falhando; os testes que precisam de uma versão "sem falhas" corrigem o ``C-FALHA`` antes.

Com o ``R-D1-01`` em 0,6 e o ``R-D1-02`` em 0,5 (premissa 0,99), o ``C-D1-OK`` dá ``d1`` = 0,798 (80 %, faixa 75-85).
Baixar o CF do ``R-D1-02`` para 0,1 tira o ``d1`` da faixa (0,64): o caso passa a falhar.
"""
from __future__ import annotations

import copy
import json
import re
from contextlib import closing
from pathlib import Path

import pytest
from fastapi.testclient import TestClient

from api.config import Configuracao
from api.db.conexao import abrir
from kb.carregador import Repositorio
from kb.modelos import carregar_base
from tests.api.apoio import criar_animal_teste, criar_sessao_teste, validar_contrato

PASTA_EXEMPLOS = Path(__file__).resolve().parents[2] / "contratos" / "exemplos"
SINAIS = {"valores": {"sinal_a": True, "sinal_b": False}}


def _cf_d1(parecer: dict) -> float:
    """O CF da doença ``d1`` no parecer, em qualquer bloco (o bloco muda com o CF)."""
    return next(i["cf"] for b in parecer["blocos"] for i in b["itens"] if i["doenca"] == "d1")


def _erro(resposta, status: int, codigo: str) -> dict:
    assert resposta.status_code == status, resposta.text
    erro = resposta.json()["erro"]
    assert erro["codigo"] == codigo
    return erro


def _exemplo(operacao: str) -> dict:
    return json.loads((PASTA_EXEMPLOS / f"{operacao}.json").read_text(encoding="utf-8"))


def _linhas(config: Configuracao, sql: str, *parametros) -> list:
    with closing(abrir(config.db_path)) as conn:
        return conn.execute(sql, parametros).fetchall()


def _versoes_no_disco(base_dir: Path) -> list[str]:
    return sorted(p.stem for p in (base_dir / "versoes").glob("v*.json"))


def _ativa_no_disco(base_dir: Path) -> str:
    return json.loads((base_dir / "ativa.json").read_text(encoding="utf-8"))["versao"]


def _grafo(cliente: TestClient, versao: str = "v0001") -> dict:
    resposta = cliente.get(f"/api/base/versoes/{versao}/grafo")
    assert resposta.status_code == 200, resposta.text
    return resposta.json()


def _com_cf(grafo: dict, aresta_id: str, cf: float) -> dict:
    """Uma cópia do grafo com o CF da aresta de conclusão trocado."""
    copia = copy.deepcopy(grafo)
    next(a for a in copia["arestas"] if a["id"] == aresta_id)["cf"] = cf
    return copia


def _edicao(grafo: dict, *, pai: str | None = "v0001", nota: str = "ajuste de CF", **extra) -> dict:
    """O corpo de ``POST /base/versoes`` a partir do que ``GET .../grafo`` devolve."""
    corpo = {
        "pai": pai,
        "nota": nota,
        "meta": grafo["meta"],
        "grafo": {"nos": grafo["nos"], "arestas": grafo["arestas"]},
        "layout": grafo["layout"],
    }
    corpo.update(extra)
    return corpo


def _salvar(cliente: TestClient, corpo: dict) -> dict:
    resposta = cliente.post("/api/base/versoes", json=corpo)
    assert resposta.status_code == 201, resposta.text
    resultado = resposta.json()
    validar_contrato("salvar_versao", resultado)
    return resultado


def _ativar(cliente: TestClient, versao: str, **extra):
    return cliente.put("/api/base/ativa", json={"versao": versao, **extra})


def _mudar_esperado(arquivo: Path, caso_id: str, esperado: dict) -> None:
    casos = json.loads(arquivo.read_text(encoding="utf-8"))
    next(c for c in casos if c["id"] == caso_id)["esperado"] = esperado
    arquivo.write_text(json.dumps(casos, ensure_ascii=False, indent=2), encoding="utf-8")


def _acrescentar_caso(arquivo: Path, caso: dict) -> None:
    casos = json.loads(arquivo.read_text(encoding="utf-8"))
    casos.append(caso)
    arquivo.write_text(json.dumps(casos, ensure_ascii=False, indent=2), encoding="utf-8")


def _consertar_c_falha(com_casos: Path) -> None:
    """O ``C-FALHA`` passa a esperar o ``top1`` que o motor devolve: nenhum caso da fixture falha mais."""
    _mudar_esperado(com_casos, "C-FALHA", {"top1": "d1"})


# --- POST /base/versoes ---------------------------------------------------------------------


def test_salvar_versao_valida_cria_v0002(cliente: TestClient, com_casos: Path, base_dir: Path):
    grafo = _grafo(cliente)
    resposta = cliente.post("/api/base/versoes", json=_edicao(_com_cf(grafo, "R-D1-01:entao", 0.65)))
    assert resposta.status_code == 201, resposta.text
    corpo = resposta.json()
    validar_contrato("salvar_versao", corpo)

    assert corpo["versao"] == "v0002"
    assert corpo["pai"] == "v0001"
    assert corpo["hash"].startswith("sha256:")
    assert corpo["validacao"]["valida"] is True
    assert corpo["validacao"]["erros"] == []
    assert corpo["execucao_nova"]["total"] == 3
    assert corpo["execucao_pai"]["total"] == 3
    # o pai nunca tinha sido executado: roda primeiro (ex_0001) para haver base de comparação; a nova vem depois
    assert corpo["execucao_pai"]["execucao_id"] == "ex_0001"
    assert corpo["execucao_nova"]["execucao_id"] == "ex_0002"
    assert (corpo["execucao_pai"]["passou"], corpo["execucao_pai"]["falhou"]) == (2, 1)
    assert (corpo["execucao_nova"]["passou"], corpo["execucao_nova"]["falhou"]) == (2, 1)
    assert corpo["mudancas"] == []  # o CF novo não tirou nenhum caso do lugar
    assert (base_dir / "versoes" / "v0002.json").is_file()
    assert _ativa_no_disco(base_dir) == "v0001"  # salvar não ativa
    assert cliente.get("/api/base/versoes").json()["ativa"] == "v0001"


def test_salvar_grava_arquivo_e_indice(cliente: TestClient, com_casos: Path, base_dir: Path, config: Configuracao):
    corpo = _salvar(cliente, _edicao(_com_cf(_grafo(cliente), "R-D1-01:entao", 0.65), nota="sobe o CF de R-D1-01"))

    gravada = json.loads((base_dir / "versoes" / "v0002.json").read_text(encoding="utf-8"))
    assert gravada["meta"]["versao"] == "v0002"
    assert gravada["meta"]["pai"] == "v0001"
    assert gravada["meta"]["autor"] == "equipe"
    assert gravada["meta"]["nota"] == "sobe o CF de R-D1-01"
    assert gravada["meta"]["data"] == "2026-10-20"
    assert next(r for r in gravada["regras"] if r["id"] == "R-D1-01")["entao"]["cf"] == 0.65
    assert next(r for r in gravada["regras"] if r["id"] == "R-D1-02")["entao"]["cf"] == 0.5  # o resto não mudou
    assert cliente.get("/api/base/versoes/v0002").json() == gravada

    # o hash da resposta é o do arquivo, e o índice do SQLite o guarda
    assert corpo["hash"] == Repositorio(base_dir).hash("v0002")
    indice = {l["versao"]: l for l in _linhas(config, "SELECT * FROM versoes_base")}
    assert sorted(indice) == ["v0001", "v0002"]
    assert indice["v0002"]["hash"] == corpo["hash"]
    assert (indice["v0002"]["pai"], indice["v0002"]["autor"], indice["v0002"]["nota"]) == (
        "v0001",
        "equipe",
        "sobe o CF de R-D1-01",
    )
    # as duas execuções estão no banco e a da nova aponta para a pai
    assert [l["versao"] for l in _linhas(config, "SELECT versao FROM execucoes_casos ORDER BY rowid")] == [
        "v0001",
        "v0002",
    ]
    nova = cliente.get(f"/api/base/versoes/v0002/execucoes/{corpo['execucao_nova']['execucao_id']}").json()
    assert nova["comparada_com"] == "v0001"


def test_salvar_com_erro_422_nada_gravado(cliente: TestClient, com_casos: Path, base_dir: Path, config: Configuracao):
    corpo = _edicao(copy.deepcopy(_grafo(cliente)))
    # a regra R-D1-03 passa a concluir uma pergunta (camada mais baixa que a do que ela lê): viola a camada
    next(a for a in corpo["grafo"]["arestas"] if a["id"] == "R-D1-03:entao")["destino"] = "sinal_a"

    resposta = cliente.post("/api/base/versoes", json=corpo)
    erro = _erro(resposta, 422, "base_invalida")
    assert erro["detalhes"][0]["codigo"] == "camada"
    assert erro["detalhes"][0]["severidade"] == "erro"
    assert erro["detalhes"][0]["alvo"] == {"tipo": "regra", "id": "R-D1-03"}
    assert all(d["severidade"] == "erro" for d in erro["detalhes"])  # os avisos não entram
    assert [i["versao"] for i in cliente.get("/api/base/versoes").json()["itens"]] == ["v0001"]
    assert _versoes_no_disco(base_dir) == ["v0001"]
    assert _linhas(config, "SELECT id FROM execucoes_casos") == []  # nenhuma execução nova
    assert _linhas(config, "SELECT versao FROM versoes_base") == []
    assert not list((base_dir / "versoes").glob(".*tmp*"))  # nem temporário esquecido


def test_salvar_estrutura_quebrada_422_base_invalida(cliente: TestClient, com_casos: Path, base_dir: Path):
    corpo = _edicao(copy.deepcopy(_grafo(cliente)), meta={})
    corpo["grafo"]["arestas"].append({"id": "solta", "papel": "condicao", "origem": "nao_existe", "destino": "R-D1-01"})

    erro = _erro(cliente.post("/api/base/versoes", json=corpo), 422, "base_invalida")
    assert [d["codigo"] for d in erro["detalhes"]] == ["estrutura"]  # o kb nem chega a montar a base
    assert erro["detalhes"][0]["severidade"] == "erro"
    assert "nao_existe" in erro["detalhes"][0]["mensagem"]
    assert _versoes_no_disco(base_dir) == ["v0001"]


def test_salvar_meta_vazia_422_base_invalida(cliente: TestClient, com_casos: Path, base_dir: Path):
    # a meta vazia monta uma base, mas sem triagem: o validador recusa (não é erro de estrutura)
    erro = _erro(cliente.post("/api/base/versoes", json=_edicao(_grafo(cliente), meta={})), 422, "base_invalida")
    assert erro["detalhes"] and all(d["severidade"] == "erro" for d in erro["detalhes"])
    assert _versoes_no_disco(base_dir) == ["v0001"]


def test_salvar_mudancas_listam_caso_que_passou_a_falhar(cliente: TestClient, com_casos: Path):
    corpo = _salvar(cliente, _edicao(_com_cf(_grafo(cliente), "R-D1-02:entao", 0.1)))

    assert corpo["mudancas"] == [{"caso_id": "C-D1-OK", "antes": "passou", "depois": "falhou"}]
    assert (corpo["execucao_pai"]["passou"], corpo["execucao_pai"]["falhou"]) == (2, 1)
    assert (corpo["execucao_nova"]["passou"], corpo["execucao_nova"]["falhou"]) == (1, 2)


@pytest.mark.parametrize("pai", ["v0099", "abc"])
def test_salvar_pai_inexistente_404(cliente: TestClient, com_casos: Path, base_dir: Path, config: Configuracao, pai):
    resposta = cliente.post("/api/base/versoes", json=_edicao(_grafo(cliente), pai=pai))
    erro = _erro(resposta, 404, "nao_encontrado")
    assert pai in erro["mensagem"]
    assert _versoes_no_disco(base_dir) == ["v0001"]
    assert _linhas(config, "SELECT id FROM execucoes_casos") == []


def test_salvar_valida_antes_de_checar_o_pai(cliente: TestClient, com_casos: Path):
    # a ordem do serviço: primeiro a validação (422), depois o pai (404)
    _erro(cliente.post("/api/base/versoes", json=_edicao(_grafo(cliente), pai="v0099", meta={})), 422, "base_invalida")


def test_salvar_sem_pai_usa_a_versao_ativa(cliente: TestClient, com_casos: Path, base_dir: Path):
    grafo = _grafo(cliente)
    primeira = _salvar(cliente, _edicao(_com_cf(grafo, "R-D1-01:entao", 0.65), pai=None))
    assert (primeira["versao"], primeira["pai"]) == ("v0002", "v0001")  # a ativa era a v0001

    assert _ativar(cliente, "v0002", confirmar_falhas=True).status_code == 200
    segunda = _salvar(cliente, _edicao(_com_cf(grafo, "R-D1-01:entao", 0.7), pai=None))
    assert (segunda["versao"], segunda["pai"]) == ("v0003", "v0002")  # agora a ativa é a v0002

    # um pai explícito vence a ativa
    terceira = _salvar(cliente, _edicao(_com_cf(grafo, "R-D1-01:entao", 0.75), pai="v0001"))
    assert (terceira["versao"], terceira["pai"]) == ("v0004", "v0001")
    assert json.loads((base_dir / "versoes" / "v0004.json").read_text(encoding="utf-8"))["meta"]["pai"] == "v0001"


def test_salvar_sem_pai_e_sem_versao_ativa(cliente: TestClient, com_casos: Path, base_dir: Path):
    (base_dir / "ativa.json").unlink()
    corpo = _salvar(cliente, _edicao(_grafo(cliente), pai=None))

    assert (corpo["versao"], corpo["pai"]) == ("v0002", None)
    assert corpo["execucao_pai"] is None  # sem pai não há o que comparar
    assert corpo["mudancas"] == []
    assert corpo["execucao_nova"]["total"] == 3


def test_salvar_nao_reexecuta_o_pai_que_ja_tem_execucao(cliente: TestClient, com_casos: Path, config: Configuracao):
    antes = cliente.post("/api/base/versoes/v0001/execucoes", json={"casos": None}).json()
    assert antes["execucao_id"] == "ex_0001"

    corpo = _salvar(cliente, _edicao(_com_cf(_grafo(cliente), "R-D1-01:entao", 0.65)))

    assert corpo["execucao_pai"] == {"execucao_id": "ex_0001", "total": 3, "passou": 2, "falhou": 1}
    assert corpo["execucao_nova"]["execucao_id"] == "ex_0002"
    assert [l["versao"] for l in _linhas(config, "SELECT versao FROM execucoes_casos ORDER BY rowid")] == [
        "v0001",
        "v0002",
    ]


def test_salvar_sem_casos_roda_zero_casos(cliente: TestClient):
    corpo = _salvar(cliente, _edicao(_grafo(cliente)))  # sem a fixture com_casos: não há casos/casos.json

    assert corpo["execucao_nova"]["total"] == 0 and corpo["execucao_pai"]["total"] == 0
    assert corpo["mudancas"] == []


def test_salvar_conflito_de_versao_409_nada_sobrescrito(
    cliente: TestClient, com_casos: Path, base_dir: Path, config: Configuracao, monkeypatch: pytest.MonkeyPatch
):
    original = (base_dir / "versoes" / "v0001.json").read_bytes()
    # outra gravação chegou antes: o repositório escolhe um número que já existe e o kb recusa sobrescrever
    monkeypatch.setattr(Repositorio, "_proxima", lambda self: "v0001")

    erro = _erro(cliente.post("/api/base/versoes", json=_edicao(_grafo(cliente))), 409, "conflito")
    assert "v0001.json" not in erro["mensagem"] and str(base_dir) not in erro["mensagem"]
    assert (base_dir / "versoes" / "v0001.json").read_bytes() == original
    assert _versoes_no_disco(base_dir) == ["v0001"]
    assert _linhas(config, "SELECT id FROM execucoes_casos") == []


def test_salvar_conflito_e_pelo_tipo_da_excecao(
    cliente: TestClient, com_casos: Path, monkeypatch: pytest.MonkeyPatch
):
    def ja_existe(self, base, *, autor, nota, pai=None):
        raise FileExistsError("qualquer texto, sem a palavra que um casamento de mensagem esperaria")

    monkeypatch.setattr(Repositorio, "salvar_nova", ja_existe)
    _erro(cliente.post("/api/base/versoes", json=_edicao(_grafo(cliente))), 409, "conflito")


def test_salvar_texto_com_surrogate_solto_422(cliente: TestClient, com_casos: Path, base_dir: Path):
    texto = json.dumps(_edicao(_grafo(cliente), nota="x\ud800"))  # ensure_ascii: o surrogate segue como \ud800
    assert "\\ud800" in texto
    resposta = cliente.post("/api/base/versoes", content=texto, headers={"Content-Type": "application/json"})
    _erro(resposta, 422, "entrada_invalida")
    assert _versoes_no_disco(base_dir) == ["v0001"]


def test_salvar_campo_extra_fora_do_grafo_422(cliente: TestClient, com_casos: Path, base_dir: Path):
    resposta = cliente.post("/api/base/versoes", json=_edicao(_grafo(cliente), autor="outra pessoa"))
    _erro(resposta, 422, "entrada_invalida")
    assert _versoes_no_disco(base_dir) == ["v0001"]


# --- PUT /base/ativa ------------------------------------------------------------------------


def test_ativar_sem_falhas_200(cliente: TestClient, com_casos: Path, base_dir: Path):
    _consertar_c_falha(com_casos)
    salva = _salvar(cliente, _edicao(_com_cf(_grafo(cliente), "R-D1-01:entao", 0.65)))
    assert salva["execucao_nova"]["falhou"] == 0

    resposta = _ativar(cliente, "v0002")
    assert resposta.status_code == 200, resposta.text
    assert resposta.json() == {"versao": "v0002", "anterior": "v0001"}
    validar_contrato("ativar_versao", resposta.json())
    assert _ativa_no_disco(base_dir) == "v0002"  # ativa.json mudou
    assert cliente.get("/api/base/versoes").json()["ativa"] == "v0002"


def test_ativar_com_casos_falhando_409(cliente: TestClient, com_casos: Path, base_dir: Path):
    salva = _salvar(cliente, _edicao(_com_cf(_grafo(cliente), "R-D1-01:entao", 0.65)))
    assert salva["execucao_nova"]["falhou"] == 1  # o C-FALHA da fixture

    erro = _erro(_ativar(cliente, "v0002"), 409, "casos_falhando")
    assert "v0002" in erro["mensagem"]
    assert _ativa_no_disco(base_dir) == "v0001"  # nada mudou
    _erro(_ativar(cliente, "v0002", confirmar_falhas=False), 409, "casos_falhando")
    assert _ativa_no_disco(base_dir) == "v0001"

    resposta = _ativar(cliente, "v0002", confirmar_falhas=True)
    assert resposta.status_code == 200, resposta.text
    assert resposta.json() == {"versao": "v0002", "anterior": "v0001"}
    assert _ativa_no_disco(base_dir) == "v0002"


def test_ativar_conta_caso_com_erro_como_falhando(cliente: TestClient, com_casos: Path, base_dir: Path):
    # o motor recusa o valor da resposta: o caso vira "erro", que o cabeçalho não conta em `falhou` (ruling 7)
    _consertar_c_falha(com_casos)
    _acrescentar_caso(
        com_casos,
        {"id": "C-TALVEZ", "descricao": "valor que o motor recusa", "modo": "produtor", "ficha": {"dias_em_lactacao": 10},
         "triagem": {"sinais": ["sinal_a"]}, "respostas": {"pergunta_x": "talvez"}, "esperado": {"top1": "d1"}},
    )
    salva = _salvar(cliente, _edicao(_com_cf(_grafo(cliente), "R-D1-01:entao", 0.65)))
    assert (salva["execucao_nova"]["total"], salva["execucao_nova"]["falhou"]) == (4, 0)

    erro = _erro(_ativar(cliente, "v0002"), 409, "casos_falhando")
    assert "erro" in erro["mensagem"]
    assert _ativa_no_disco(base_dir) == "v0001"
    assert _ativar(cliente, "v0002", confirmar_falhas=True).status_code == 200


def test_ativar_versao_sem_execucao_nao_exige_confirmacao(
    cliente: TestClient, com_casos: Path, base_dir: Path, config: Configuracao
):
    # decisão: sem execução não há falha conhecida a confirmar. A v0002 é gravada direto no repositório (fora da API),
    # logo nunca foi executada, embora os casos da fixture tenham um que falha.
    dados = json.loads((base_dir / "versoes" / "v0001.json").read_text(encoding="utf-8"))
    Repositorio(base_dir, hoje=config.hoje).salvar_nova(carregar_base(dados), autor="teste", nota="fora da API")
    assert cliente.get("/api/base/versoes/v0002/execucoes").json() == {"itens": []}

    resposta = _ativar(cliente, "v0002")
    assert resposta.status_code == 200, resposta.text
    assert resposta.json() == {"versao": "v0002", "anterior": "v0001"}
    assert _ativa_no_disco(base_dir) == "v0002"


def test_ativar_olha_a_ultima_execucao(cliente: TestClient, com_casos: Path, base_dir: Path):
    _salvar(cliente, _edicao(_com_cf(_grafo(cliente), "R-D1-01:entao", 0.65)))
    _erro(_ativar(cliente, "v0002"), 409, "casos_falhando")  # a execução da gravação tem o C-FALHA falhando

    _consertar_c_falha(com_casos)  # os casos foram corrigidos: uma nova execução passa
    nova = cliente.post("/api/base/versoes/v0002/execucoes", json={"casos": None}).json()
    assert nova["falhou"] == 0

    resposta = _ativar(cliente, "v0002")  # a mais recente manda; a antiga, com falha, não conta mais
    assert resposta.status_code == 200, resposta.text
    assert _ativa_no_disco(base_dir) == "v0002"


@pytest.mark.parametrize("versao", ["v0099", "abc", "", "\ud800"])
def test_ativar_inexistente_404(cliente: TestClient, com_casos: Path, base_dir: Path, versao: str):
    texto = json.dumps({"versao": versao})  # o surrogate segue como \ud800
    resposta = cliente.put("/api/base/ativa", content=texto, headers={"Content-Type": "application/json"})
    erro = _erro(resposta, 404, "nao_encontrado")
    assert erro["mensagem"].startswith("Versão ")  # o 404 da versão, não o "Recurso não encontrado" de rota inexistente
    assert _ativa_no_disco(base_dir) == "v0001"


@pytest.mark.parametrize("corpo", [{}, {"versao": 1}, {"versao": "v0001", "forcar": True}, {"versao": "v0001", "confirmar_falhas": "talvez"}])
def test_ativar_corpo_invalido_422(cliente: TestClient, base_dir: Path, corpo: dict):
    _erro(cliente.put("/api/base/ativa", json=corpo), 422, "entrada_invalida")
    assert _ativa_no_disco(base_dir) == "v0001"


def test_ativar_sem_ponteiro_anterior(cliente: TestClient, base_dir: Path):
    (base_dir / "ativa.json").unlink()
    resposta = _ativar(cliente, "v0001")
    assert resposta.status_code == 200, resposta.text
    assert resposta.json() == {"versao": "v0001", "anterior": None}
    validar_contrato("ativar_versao", resposta.json())
    assert _ativa_no_disco(base_dir) == "v0001"


def test_exemplos_do_contrato_tem_a_forma_das_respostas_reais(cliente: TestClient, com_casos: Path):
    real = _salvar(cliente, _edicao(_com_cf(_grafo(cliente), "R-D1-01:entao", 0.65)))
    exemplo = _exemplo("salvar_versao")["resposta"]

    assert set(exemplo) == set(real)
    assert set(exemplo["validacao"]) == set(real["validacao"])
    for chave in ("execucao_nova", "execucao_pai"):
        assert set(exemplo[chave]) == set(real[chave])
        assert exemplo[chave]["passou"] + exemplo[chave]["falhou"] == exemplo[chave]["total"]  # as contas fecham
        assert real[chave]["passou"] + real[chave]["falhou"] == real[chave]["total"]
    assert re.fullmatch(r"sha256:[0-9a-f]{64}", exemplo["hash"])
    assert re.fullmatch(r"sha256:[0-9a-f]{64}", real["hash"])
    assert set(exemplo["mudancas"][0]) == {"caso_id", "antes", "depois"}

    ativar = _exemplo("ativar_versao")
    resposta = _ativar(cliente, "v0002", **{k: v for k, v in ativar["requisicao"].items() if k != "versao"})
    assert resposta.status_code == ativar["status"]
    assert set(resposta.json()) == set(ativar["resposta"])


# --- Review Focus 5: a sessão fica na versão em que nasceu ----------------------------------


def test_sessao_em_andamento_continua_na_versao_antiga(cliente: TestClient):
    antiga = criar_sessao_teste(cliente, criar_animal_teste(cliente)["id"])
    assert antiga["versao_base"] == "v0001"
    resposta = cliente.post("/api/sessoes/ses_0001/triagem/sinais", json=SINAIS)
    assert resposta.status_code == 200, resposta.text
    assert resposta.json()["versao_base"] == "v0001"
    assert _cf_d1(cliente.get("/api/sessoes/ses_0001/parecer").json()) == pytest.approx(0.6)

    # a base muda e é ativada com o CF de R-D1-01 de 0,6 para 0,3, com a sessão ainda no meio
    salva = _salvar(cliente, _edicao(_com_cf(_grafo(cliente), "R-D1-01:entao", 0.3)))
    assert salva["versao"] == "v0002"
    assert _ativar(cliente, "v0002").status_code == 200
    assert cliente.get("/api/base/versoes").json()["ativa"] == "v0002"

    # a sessão antiga segue na v0001: ler, responder mais uma tela e pedir o parecer usam os CF da v0001
    lida = cliente.get("/api/sessoes/ses_0001")
    assert lida.status_code == 200 and lida.json()["versao_base"] == "v0001"
    parcial = cliente.get("/api/sessoes/ses_0001/parecer").json()
    assert parcial["versao_base"] == "v0001"
    assert _cf_d1(parcial) == pytest.approx(0.6)  # na v0002 seria 0,3

    resposta = cliente.post("/api/sessoes/ses_0001/respostas", json={"simbolo": "pergunta_x", "valor": True})
    assert resposta.status_code == 200, resposta.text
    validar_contrato("responder_pergunta", resposta.json())
    assert resposta.json()["versao_base"] == "v0001"
    final = cliente.get("/api/sessoes/ses_0001/parecer").json()
    assert final["versao_base"] == "v0001" and final["final"] is True
    assert _cf_d1(final) == pytest.approx(0.798)  # 0,6 + 0,495 * 0,4 (v0002 daria 0,6465)

    # uma sessão nova nasce na versão ativa
    nova = criar_sessao_teste(cliente, criar_animal_teste(cliente, brinco="BR-0002")["id"])
    assert nova["versao_base"] == "v0002"
    assert cliente.post("/api/sessoes/ses_0002/triagem/sinais", json=SINAIS).json()["versao_base"] == "v0002"
    parecer = cliente.get("/api/sessoes/ses_0002/parecer").json()
    assert parecer["versao_base"] == "v0002"
    assert _cf_d1(parecer) == pytest.approx(0.3)


def test_sessao_so_le_versao_gravada_no_disco(cliente: TestClient, base_dir: Path):
    criar_sessao_teste(cliente, criar_animal_teste(cliente)["id"])
    _salvar(cliente, _edicao(_com_cf(_grafo(cliente), "R-D1-01:entao", 0.3)))
    assert _ativar(cliente, "v0002").status_code == 200

    arquivo = base_dir / "versoes" / "v0001.json"
    conteudo = arquivo.read_bytes()
    arquivo.unlink()  # simula a perda do arquivo da versão antiga
    resposta = cliente.get("/api/sessoes/ses_0001")
    erro = _erro(resposta, 500, "erro_interno")
    assert erro["mensagem"] == "Erro interno. Tente novamente."
    for pista in ("v0001.json", str(base_dir), "versoes", "Versão v0001 não encontrada"):
        assert pista not in resposta.text

    # nada fica em memória: com o arquivo de volta, a mesma sessão responde de novo
    arquivo.write_bytes(conteudo)
    restaurada = cliente.get("/api/sessoes/ses_0001")
    assert restaurada.status_code == 200 and restaurada.json()["versao_base"] == "v0001"
