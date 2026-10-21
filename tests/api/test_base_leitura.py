"""Base de conhecimento: leitura e validação (Task 9). Dados fictícios (a base mínima da fixture)."""
from __future__ import annotations

import json
from collections.abc import Iterator
from datetime import datetime, timedelta
from pathlib import Path

import pytest
from fastapi.testclient import TestClient

from api.config import Configuracao
from api.contexto import Contexto
from api.db import repositorios as repo
from api.db.conexao import abrir, inicializar
from api.schemas.base import EdicaoBase, GrafoEdicao
from api.servicos import base_servico
from kb import validar_edicao
from kb.carregador import Repositorio
from kb.grafo import Grafo, grafo_para_base
from kb.modelos import carregar_base
from tests.api.apoio import validar_contrato

PASTA_EXEMPLOS = Path(__file__).resolve().parents[2] / "contratos" / "exemplos"


def _erro(resposta, status: int, codigo: str) -> dict:
    assert resposta.status_code == status, resposta.text
    erro = resposta.json()["erro"]
    assert erro["codigo"] == codigo
    return erro


def _exemplo(operacao: str) -> dict:
    return json.loads((PASTA_EXEMPLOS / f"{operacao}.json").read_text(encoding="utf-8"))


def _edicao(grafo: dict, **extra) -> dict:
    """Corpo de ``POST /base/validar`` a partir do grafo devolvido por ``GET .../grafo`` (``nos`` e ``arestas``)."""
    corpo = {
        "pai": "v0001",
        "nota": "x",
        "meta": grafo["meta"],
        "grafo": {"nos": grafo["nos"], "arestas": grafo["arestas"]},
        "layout": grafo["layout"],
    }
    corpo.update(extra)
    return corpo


@pytest.fixture
def grafo(cliente: TestClient) -> dict:
    resposta = cliente.get("/api/base/versoes/v0001/grafo")
    assert resposta.status_code == 200, resposta.text
    return resposta.json()


@pytest.fixture
def ctx(config: Configuracao) -> Iterator[Contexto]:
    """Contexto montado à mão (sem HTTP) sobre o banco e a base do teste."""
    inicializar(config.db_path)
    conn = abrir(config.db_path)
    try:
        yield Contexto(config=config, conn=conn, repo=Repositorio(config.base_dir, hoje=config.hoje))
    finally:
        conn.close()


# --- GET /base/versoes ----------------------------------------------------------------------


def test_listar_versoes_marca_ativa(cliente: TestClient):
    resposta = cliente.get("/api/base/versoes")
    assert resposta.status_code == 200, resposta.text
    corpo = resposta.json()
    assert corpo["ativa"] == "v0001"
    assert [i["versao"] for i in corpo["itens"]] == ["v0001"]
    item = corpo["itens"][0]
    assert item["simbolos"] == 10
    assert item["regras"] == 6
    assert item["suposicao_a_validar"] == 0  # a base mínima tem status "validada"
    assert (item["pai"], item["autor"], item["data"], item["nota"]) == (None, "teste", "2026-10-20", "fixture")
    assert item["ultima_execucao"] is None
    validar_contrato("listar_versoes", corpo)


def test_listar_versoes_traz_a_ultima_execucao_de_cada_versao(
    cliente: TestClient, config: Configuracao, agora: datetime
):
    # a segunda versão vem do disco; só a primeira tem execuções (a mais nova vale)
    repo_kb = Repositorio(config.base_dir, hoje=config.hoje)
    repo_kb.salvar_nova(repo_kb.carregar("v0001"), autor="ana", nota="segunda", pai="v0001")
    conn = abrir(config.db_path)
    try:
        with conn:
            for versao in ("v0001", "v0002"):
                repo.sincronizar_versao(
                    conn, versao=versao, pai=None, autor=None, data=None, nota=None, hash=f"sha256:{versao}", agora=agora
                )
            resultado = {"caso_id": "C-1", "status": "passou"}
            repo.inserir_execucao(conn, versao="v0001", comparada_com=None, resultados=[resultado], agora=agora)
            falho = {"caso_id": "C-2", "status": "falhou"}
            repo.inserir_execucao(
                conn, versao="v0001", comparada_com=None, resultados=[resultado, falho], agora=agora + timedelta(hours=1)
            )
    finally:
        conn.close()

    corpo = cliente.get("/api/base/versoes").json()
    assert [i["versao"] for i in corpo["itens"]] == ["v0001", "v0002"]
    assert corpo["itens"][0]["ultima_execucao"] == {"execucao_id": "ex_0002", "passou": 1, "falhou": 1}
    assert corpo["itens"][1]["ultima_execucao"] is None
    assert corpo["itens"][1]["pai"] == "v0001"
    assert corpo["itens"][1]["autor"] == "ana"
    validar_contrato("listar_versoes", corpo)


def test_listar_versoes_sem_versao_ativa(cliente: TestClient, base_dir: Path):
    (base_dir / "ativa.json").unlink()
    corpo = cliente.get("/api/base/versoes").json()
    assert corpo["ativa"] is None
    assert [i["versao"] for i in corpo["itens"]] == ["v0001"]


# --- GET /base/versoes/{versao} -------------------------------------------------------------


def test_obter_versao_devolve_arquivo_inteiro(cliente: TestClient, base_dir: Path):
    resposta = cliente.get("/api/base/versoes/v0001")
    assert resposta.status_code == 200, resposta.text
    corpo = resposta.json()
    assert set(corpo) == {"meta", "simbolos", "regras", "layout"}
    assert corpo["meta"]["versao"] == "v0001"
    # é o arquivo gravado: sem os null que o modelo acrescentaria
    assert corpo == json.loads((base_dir / "versoes" / "v0001.json").read_text(encoding="utf-8"))
    validar_contrato("obter_versao", corpo)


@pytest.mark.parametrize("versao", ["v0099", "abc", "v1", "V0001", "v0001.json"])
def test_obter_versao_inexistente_ou_id_invalido_404(cliente: TestClient, versao: str):
    _erro(cliente.get(f"/api/base/versoes/{versao}"), 404, "nao_encontrado")
    _erro(cliente.get(f"/api/base/versoes/{versao}/grafo"), 404, "nao_encontrado")


def test_404_de_versao_cita_o_id_curto(cliente: TestClient):
    assert "'v0099'" in _erro(cliente.get("/api/base/versoes/v0099"), 404, "nao_encontrado")["mensagem"]
    longo = _erro(cliente.get("/api/base/versoes/" + "x" * 500), 404, "nao_encontrado")["mensagem"]
    assert len(longo) < 100  # o id enviado não volta inteiro


# --- GET /base/versoes/{versao}/grafo -------------------------------------------------------


def test_grafo_ida_e_volta(cliente: TestClient, base_dir: Path, grafo: dict):
    assert grafo["versao"] == "v0001"
    assert grafo["nos"] and grafo["arestas"]
    nos = {no["id"]: no for no in grafo["nos"]}
    assert nos["sinal_a"]["triagem"] is True
    assert nos["sinal_a"]["tipo_no"] == "simbolo"
    assert nos["R-D1-01"]["tipo_no"] == "regra"
    assert nos["pergunta_x"]["triagem"] is False
    assert grafo_para_base(Grafo.model_validate(grafo)) == carregar_base(base_dir / "versoes" / "v0001.json")
    validar_contrato("obter_grafo", grafo)


def test_get_nao_escreve_nada(cliente: TestClient, base_dir: Path, config: Configuracao):
    antes = sorted(p.name for p in (base_dir / "versoes").iterdir())
    for rota in ("/api/base/versoes", "/api/base/versoes/v0001", "/api/base/versoes/v0001/grafo"):
        assert cliente.get(rota).status_code == 200
    assert sorted(p.name for p in (base_dir / "versoes").iterdir()) == antes
    conn = abrir(config.db_path)
    try:
        assert repo.listar_versoes_base(conn) == []  # só quem grava execução sincroniza o índice
    finally:
        conn.close()


# --- POST /base/validar ---------------------------------------------------------------------


def test_validar_edicao_valida(cliente: TestClient, grafo: dict):
    resposta = cliente.post("/api/base/validar", json=_edicao(grafo))
    assert resposta.status_code == 200, resposta.text
    corpo = resposta.json()
    assert corpo["valida"] is True
    assert corpo["erros"] == []
    assert corpo["resumo"] == {"simbolos": 10, "regras": 6, "suposicao_a_validar": 0}
    validar_contrato("validar_base", corpo)


def test_validar_aceita_o_grafo_inteiro_do_editor(cliente: TestClient, grafo: dict):
    """O editor devolve o ``Grafo`` todo (``versao``, ``meta`` e ``layout`` junto de ``nos`` e ``arestas``) em ``grafo``."""
    corpo = _edicao(grafo)
    corpo["grafo"] = grafo  # sobra: versao, meta e layout, que o envelope já traz por fora
    assert {"versao", "meta", "layout"} <= set(corpo["grafo"])

    resposta = cliente.post("/api/base/validar", json=corpo)
    assert resposta.status_code == 200, resposta.text
    assert resposta.json()["valida"] is True


def test_validar_usa_a_meta_e_o_layout_do_envelope_nao_os_de_dentro_do_grafo(cliente: TestClient, grafo: dict):
    corpo = _edicao(grafo, layout={"sinal_a": {"x": 1.0, "y": 2.0}})
    corpo["grafo"] = {**grafo, "layout": {"sinal_a": "lixo"}, "meta": {"limiares": "lixo"}}
    resposta = cliente.post("/api/base/validar", json=corpo)
    assert resposta.status_code == 200, resposta.text
    assert resposta.json()["valida"] is True  # o lixo de dentro de grafo.* foi ignorado


def test_so_o_envelope_do_grafo_ignora_campos_extras():
    # decisão (Ruling 9): extra="ignore" só em GrafoEdicao; o envelope e os demais corpos seguem fechados
    assert GrafoEdicao.model_config["extra"] == "ignore"
    assert GrafoEdicao.model_config["allow_inf_nan"] is False
    assert EdicaoBase.model_config["extra"] == "forbid"
    assert GrafoEdicao.model_validate({"nos": [], "arestas": [], "versao": "v1", "meta": {}}).model_dump() == {
        "nos": [],
        "arestas": [],
    }


def test_campo_extra_fora_do_grafo_continua_422(cliente: TestClient, grafo: dict):
    resposta = cliente.post("/api/base/validar", json=_edicao(grafo, cf=0.9))
    erro = _erro(resposta, 422, "entrada_invalida")
    assert any("corpo.cf" in d["mensagem"] for d in erro["detalhes"])


def test_validar_sem_nos_ou_arestas_422(cliente: TestClient, grafo: dict):
    corpo = _edicao(grafo)
    del corpo["grafo"]["arestas"]
    _erro(cliente.post("/api/base/validar", json=corpo), 422, "entrada_invalida")


def test_validar_edicao_com_erro_camada(cliente: TestClient, base_dir: Path, grafo: dict):
    antes = sorted(p.name for p in (base_dir / "versoes").iterdir())
    corpo = _edicao(grafo)
    corpo["grafo"]["arestas"].append(
        {"id": "extra", "papel": "condicao", "origem": "chamar_agora", "destino": "R-D1-01", "op": "=",
         "valor": True, "negado": False}
    )

    resposta = cliente.post("/api/base/validar", json=corpo)
    assert resposta.status_code == 200, resposta.text
    relatorio = resposta.json()
    assert relatorio["valida"] is False
    assert {e["codigo"] for e in relatorio["erros"]} >= {"camada"}
    camada = next(e for e in relatorio["erros"] if e["codigo"] == "camada")
    assert camada["numero"] == "E12"
    assert camada["alvo"] == {"tipo": "regra", "id": "R-D1-01"}
    validar_contrato("validar_base", relatorio)
    assert sorted(p.name for p in (base_dir / "versoes").iterdir()) == antes  # validar nunca grava


def test_validar_estrutura_quebrada_nunca_500(cliente: TestClient, grafo: dict):
    corpo = _edicao(grafo, meta={})
    corpo["grafo"]["arestas"].append(
        {"id": "solta", "papel": "condicao", "origem": "nao_existe", "destino": "R-D1-01"}
    )

    resposta = cliente.post("/api/base/validar", json=corpo)
    assert resposta.status_code == 200, resposta.text
    relatorio = resposta.json()
    assert relatorio["valida"] is False
    assert [(e["codigo"], e["numero"]) for e in relatorio["erros"]] == [("estrutura", "E00")]
    assert "nao_existe" in relatorio["erros"][0]["mensagem"]
    validar_contrato("validar_base", relatorio)


@pytest.mark.parametrize(
    "grafo_quebrado",
    [
        {"nos": [{}], "arestas": []},
        {"nos": [{"id": "a", "tipo_no": "simbolo", "dados": {}}], "arestas": []},
        {"nos": [{"id": "a", "tipo_no": "regra", "dados": {"id": "b"}}], "arestas": []},
        {"nos": [], "arestas": [{"id": "e", "papel": "condicao", "origem": "a", "destino": "b"}]},
    ],
)
def test_validar_estrutura_quebrada_em_varias_formas(cliente: TestClient, grafo: dict, grafo_quebrado: dict):
    corpo = _edicao(grafo)
    corpo["grafo"] = grafo_quebrado
    resposta = cliente.post("/api/base/validar", json=corpo)
    assert resposta.status_code == 200, resposta.text
    relatorio = resposta.json()
    assert relatorio["valida"] is False
    assert {e["codigo"] for e in relatorio["erros"]} == {"estrutura"}
    assert relatorio["resumo"] == {"simbolos": 0, "regras": 0, "suposicao_a_validar": 0}


@pytest.mark.parametrize("corpo", [[], [1, 2], "texto", 7, None])
def test_corpo_que_nao_e_objeto_422(cliente: TestClient, corpo):
    _erro(cliente.post("/api/base/validar", json=corpo), 422, "entrada_invalida")


def test_validar_texto_com_surrogate_solto_422_nunca_500(cliente: TestClient, grafo: dict):
    """O JSON aceita ``\\ud800``, mas a resposta não o codificaria em UTF-8 (a mensagem cita ids do corpo)."""
    corpo = _edicao(grafo)
    corpo["meta"]["triagem"][0]["simbolos"] = ["sinal_\ud800"]  # a mensagem E01 cita o símbolo sem escapar
    texto = json.dumps(corpo)  # ensure_ascii: o surrogate segue como a sequência \ud800
    assert "\\ud800" in texto
    resposta = cliente.post("/api/base/validar", content=texto, headers={"Content-Type": "application/json"})
    _erro(resposta, 422, "entrada_invalida")


# --- exemplos do contrato -------------------------------------------------------------------


def _relatorio_do_validador(requisicao: dict) -> dict:
    dados = {
        "meta": requisicao["meta"],
        "nos": requisicao["grafo"]["nos"],
        "arestas": requisicao["grafo"]["arestas"],
        "layout": requisicao["layout"],
    }
    return validar_edicao(dados)[1].model_dump(mode="json")


def test_exemplo_validar_base_e_a_resposta_real_do_validador(cliente: TestClient):
    exemplo = _exemplo("validar_base")
    assert exemplo["resposta"] == _relatorio_do_validador(exemplo["requisicao"])

    resposta = cliente.post("/api/base/validar", json=exemplo["requisicao"])  # e a rota serializa do mesmo jeito
    assert resposta.status_code == exemplo["status"]
    assert resposta.json() == exemplo["resposta"]


def test_exemplo_salvar_versao_traz_a_validacao_real_do_validador():
    exemplo = _exemplo("salvar_versao")
    assert exemplo["resposta"]["validacao"] == _relatorio_do_validador(exemplo["requisicao"])


# --- serviço: sincronizar_indice e grafo_da_edicao ------------------------------------------


def test_sincronizar_indice_registra_as_versoes_do_disco(ctx: Contexto):
    base_servico.sincronizar_indice(ctx)

    assert repo.listar_versoes_base(ctx.conn) == [
        {
            "versao": "v0001",
            "pai": None,
            "autor": "teste",
            "data": "2026-10-20",
            "nota": "fixture",
            "hash": ctx.repo.hash("v0001"),
            "criada_em": "2026-10-20T10:00:00",
        }
    ]
    assert not ctx.conn.in_transaction  # a escrita fechou a própria transação (with ctx.conn)
    # a FK de execucoes_casos.versao agora é satisfeita (é o que as Tasks 10 e 11 precisam)
    resultado = {"caso_id": "C-1", "status": "passou"}
    execucao = repo.inserir_execucao(
        ctx.conn, versao="v0001", comparada_com=None, resultados=[resultado], agora=ctx.config.agora()
    )
    assert execucao == "ex_0001"


def test_sincronizar_indice_so_acrescenta_o_que_falta(ctx: Contexto):
    base_servico.sincronizar_indice(ctx)
    ctx.repo.salvar_nova(ctx.repo.carregar("v0001"), autor="ana", nota="segunda", pai="v0001")
    base_servico.sincronizar_indice(ctx)
    base_servico.sincronizar_indice(ctx)  # idempotente

    versoes = repo.listar_versoes_base(ctx.conn)
    assert [v["versao"] for v in versoes] == ["v0001", "v0002"]
    assert (versoes[1]["pai"], versoes[1]["autor"], versoes[1]["nota"]) == ("v0001", "ana", "segunda")
    assert versoes[1]["hash"] == ctx.repo.hash("v0002") != versoes[0]["hash"]


def test_sincronizar_indice_nao_altera_versao_ja_registrada(ctx: Contexto):
    with ctx.conn:
        repo.sincronizar_versao(
            ctx.conn, versao="v0001", pai=None, autor="outro", data=None, nota="antiga", hash="sha256:antigo",
            agora=ctx.config.agora(),
        )
    base_servico.sincronizar_indice(ctx)

    (linha,) = repo.listar_versoes_base(ctx.conn)
    assert (linha["autor"], linha["nota"], linha["hash"]) == ("outro", "antiga", "sha256:antigo")


def test_sincronizar_indice_grava_de_verdade_no_banco(ctx: Contexto, config: Configuracao):
    base_servico.sincronizar_indice(ctx)
    outra = abrir(config.db_path)  # outra conexão só enxerga o que foi confirmado
    try:
        assert [v["versao"] for v in repo.listar_versoes_base(outra)] == ["v0001"]
    finally:
        outra.close()


def test_sincronizar_indice_sem_versoes_no_disco(ctx: Contexto, base_dir: Path):
    (base_dir / "versoes" / "v0001.json").unlink()
    base_servico.sincronizar_indice(ctx)
    assert repo.listar_versoes_base(ctx.conn) == []


def test_grafo_da_edicao_monta_o_dict_que_o_kb_espera(grafo: dict):
    corpo = EdicaoBase.model_validate(_edicao(grafo, layout={"sinal_a": {"x": 1.0, "y": 2.0}}))
    dados = base_servico.grafo_da_edicao(corpo)
    assert set(dados) == {"meta", "nos", "arestas", "layout"}
    assert dados["meta"] == grafo["meta"]
    assert dados["nos"] == grafo["nos"]
    assert dados["arestas"] == grafo["arestas"]
    assert dados["layout"] == {"sinal_a": {"x": 1.0, "y": 2.0}}
    assert validar_edicao(dados)[1].valida is True
