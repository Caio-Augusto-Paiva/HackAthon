"""Execução dos casos de teste por versão (4.5.3). Dados fictícios: a base mínima e ``casos_minima.json``."""
from __future__ import annotations

import codecs
import json
from contextlib import closing
from pathlib import Path

import pytest
from fastapi.testclient import TestClient

from api.config import Configuracao
from api.db.conexao import abrir
from api.servicos import casos_servico
from kb.carregador import Repositorio
from kb.modelos import carregar_base
from tests.api.apoio import validar_contrato


def _erro(resposta, status: int, codigo: str) -> dict:
    assert resposta.status_code == status, resposta.text
    erro = resposta.json()["erro"]
    assert erro["codigo"] == codigo
    return erro


def _executar(cliente: TestClient, versao: str = "v0001", casos: list[str] | None = None) -> dict:
    resposta = cliente.post(f"/api/base/versoes/{versao}/execucoes", json={"casos": casos})
    assert resposta.status_code == 201, resposta.text
    corpo = resposta.json()
    validar_contrato("executar_casos", corpo)
    return corpo


def _resultado(execucao: dict, caso_id: str) -> dict:
    return next(r for r in execucao["resultados"] if r["caso_id"] == caso_id)


def _acrescentar_caso(arquivo: Path, caso: dict) -> None:
    casos = json.loads(arquivo.read_text(encoding="utf-8"))
    casos.append(caso)
    arquivo.write_text(json.dumps(casos, ensure_ascii=False, indent=2), encoding="utf-8")


def _caso_extra(id: str, **mudancas) -> dict:
    """Um caso válido da base mínima (o do D1), com os campos de ``mudancas`` trocados."""
    caso = {
        "id": id,
        "descricao": "caso de teste",
        "modo": "produtor",
        "ficha": {"dias_em_lactacao": 10},
        "triagem": {"sinais": ["sinal_a"]},
        "respostas": {"pergunta_x": True},
        "esperado": {"top1": "d1"},
    }
    caso.update(mudancas)
    return caso


def _salvar_filha(config: Configuracao, cf_regra_d1: float) -> str:
    """Salva a v0002 (pai v0001) com o CF da regra R-D1-02 trocado; com 0,1 o D1 do C-D1-OK sai da faixa."""
    repo_kb = Repositorio(config.base_dir, hoje=config.hoje)
    dados = json.loads((config.base_dir / "versoes" / "v0001.json").read_text(encoding="utf-8"))
    regra = next(r for r in dados["regras"] if r["id"] == "R-D1-02")
    regra["entao"]["cf"] = cf_regra_d1
    return repo_kb.salvar_nova(carregar_base(dados), autor="teste", nota="filha", pai="v0001")


def _linhas(config: Configuracao, sql: str, *parametros) -> list:
    with closing(abrir(config.db_path)) as conn:
        return conn.execute(sql, parametros).fetchall()


# --- POST /base/versoes/{versao}/execucoes --------------------------------------------------


def test_executar_todos_grava_execucao(cliente: TestClient, com_casos: Path):
    resposta = cliente.post("/api/base/versoes/v0001/execucoes", json={"casos": None})
    assert resposta.status_code == 201, resposta.text
    corpo = resposta.json()
    validar_contrato("executar_casos", corpo)
    assert corpo["execucao_id"] == "ex_0001"
    assert corpo["versao"] == "v0001"
    assert corpo["executada_em"] == "2026-10-20T10:00:00"
    assert (corpo["total"], corpo["passou"], corpo["falhou"]) == (3, 2, 1)
    assert corpo["comparada_com"] is None
    assert corpo["mudancas"] == []
    assert [(r["caso_id"], r["status"]) for r in corpo["resultados"]] == [
        ("C-D1-OK", "passou"),
        ("C-BV-OK", "passou"),
        ("C-FALHA", "falhou"),
    ]
    assert _resultado(corpo, "C-D1-OK")["descricao"].startswith("D1 sobe com o sinal A")
    assert all(r["mudou_vs_pai"] is None and r["erro"] is None for r in corpo["resultados"])
    # o caso que pausa por bandeira vermelha vem do motor, não de um valor fixo
    assert _resultado(corpo, "C-BV-OK")["obtido"]["alerta"]["pausa"] is True
    assert _resultado(corpo, "C-D1-OK")["obtido"]["percentuais"] == {"d1": 80}


def test_resultado_falho_traz_campo_esperado_obtido(cliente: TestClient, com_casos: Path):
    resultado = _resultado(_executar(cliente), "C-FALHA")
    assert resultado["status"] == "falhou"
    assert resultado["falhas"] == [{"campo": "top1", "esperado": "outra_doenca", "obtido": "d1"}]
    assert resultado["falhas"][0]["campo"] == "top1"
    assert resultado["falhas"][0]["obtido"] == "d1"
    assert "motivo_parada" in resultado["obtido"]
    assert resultado["erro"] is None


def test_executar_subconjunto(cliente: TestClient, com_casos: Path):
    corpo = _executar(cliente, casos=["C-D1-OK"])
    assert (corpo["total"], corpo["passou"], corpo["falhou"]) == (1, 1, 0)
    assert [r["caso_id"] for r in corpo["resultados"]] == ["C-D1-OK"]

    # a ordem dos resultados segue o arquivo de casos, não a do pedido, e um id repetido conta uma vez
    corpo = _executar(cliente, casos=["C-FALHA", "C-D1-OK", "C-FALHA"])
    assert [r["caso_id"] for r in corpo["resultados"]] == ["C-D1-OK", "C-FALHA"]


def test_id_de_caso_desconhecido_e_404_e_nada_e_gravado(cliente: TestClient, com_casos: Path, config: Configuracao):
    resposta = cliente.post("/api/base/versoes/v0001/execucoes", json={"casos": ["C-D1-OK", "C-NAO-EXISTE"]})
    erro = _erro(resposta, 404, "nao_encontrado")
    assert "C-NAO-EXISTE" in erro["mensagem"]
    assert _linhas(config, "SELECT id FROM execucoes_casos") == []


def test_lista_vazia_de_casos_executa_nenhum(cliente: TestClient, com_casos: Path):
    corpo = _executar(cliente, casos=[])
    assert (corpo["total"], corpo["passou"], corpo["falhou"], corpo["resultados"]) == (0, 0, 0, [])


def test_versao_inexistente_e_404(cliente: TestClient, com_casos: Path):
    for versao in ("v0009", "abc"):
        _erro(cliente.post(f"/api/base/versoes/{versao}/execucoes", json={"casos": None}), 404, "nao_encontrado")
        _erro(cliente.get(f"/api/base/versoes/{versao}/execucoes"), 404, "nao_encontrado")
        _erro(cliente.get(f"/api/base/versoes/{versao}/execucoes/ex_0001"), 404, "nao_encontrado")


def test_corpo_invalido_e_422(cliente: TestClient, com_casos: Path):
    _erro(cliente.post("/api/base/versoes/v0001/execucoes", json={"casos": "C-D1-OK"}), 422, "entrada_invalida")
    _erro(cliente.post("/api/base/versoes/v0001/execucoes", json={"casos": None, "x": 1}), 422, "entrada_invalida")


# --- GET .../execucoes e .../execucoes/{execucao_id} ----------------------------------------


def test_get_execucao_igual_ao_post(cliente: TestClient, com_casos: Path, config: Configuracao):
    postado = _executar(cliente)
    resposta = cliente.get(f"/api/base/versoes/v0001/execucoes/{postado['execucao_id']}")
    assert resposta.status_code == 200, resposta.text
    assert resposta.json() == postado
    validar_contrato("obter_execucao", resposta.json())

    # a execução de uma versão não aparece sob outra versão, nem existe com um id inventado
    _salvar_filha(config, 0.1)
    _erro(cliente.get(f"/api/base/versoes/v0002/execucoes/{postado['execucao_id']}"), 404, "nao_encontrado")
    _erro(cliente.get("/api/base/versoes/v0001/execucoes/ex_9999"), 404, "nao_encontrado")


def test_listar_execucoes_so_cabecalho_a_mais_nova_primeiro(cliente: TestClient, com_casos: Path, config: Configuracao):
    primeira = _executar(cliente)
    segunda = _executar(cliente, casos=["C-D1-OK"])
    _salvar_filha(config, 0.1)
    terceira = _executar(cliente, versao="v0002")

    resposta = cliente.get("/api/base/versoes/v0001/execucoes")
    assert resposta.status_code == 200, resposta.text
    corpo = resposta.json()
    validar_contrato("listar_execucoes", corpo)
    assert [i["execucao_id"] for i in corpo["itens"]] == [segunda["execucao_id"], primeira["execucao_id"]]
    assert corpo["itens"][0] == {
        "execucao_id": "ex_0002",
        "executada_em": "2026-10-20T10:00:00",
        "total": 1,
        "passou": 1,
        "falhou": 0,
    }
    assert all("resultados" not in item for item in corpo["itens"])
    # só as execuções da versão pedida
    assert [i["execucao_id"] for i in cliente.get("/api/base/versoes/v0002/execucoes").json()["itens"]] == [
        terceira["execucao_id"]
    ]


def test_listar_execucoes_sem_nenhuma(cliente: TestClient, com_casos: Path):
    resposta = cliente.get("/api/base/versoes/v0001/execucoes")
    assert resposta.status_code == 200, resposta.text
    assert resposta.json() == {"itens": []}


# --- casos sem condição de rodar ------------------------------------------------------------


def test_caso_mal_formado_vira_erro(cliente: TestClient, com_casos: Path):
    # critério que o esperado não conhece: o caso vira "erro" e os outros três rodam normalmente
    _acrescentar_caso(com_casos, _caso_extra("C-CRITERIO", esperado={"criterio_inventado": 1}))
    corpo = _executar(cliente)
    assert (corpo["total"], corpo["passou"], corpo["falhou"]) == (4, 2, 1)  # erro não conta em passou nem em falhou
    resultado = _resultado(corpo, "C-CRITERIO")
    assert resultado["status"] == "erro"
    assert resultado["erro"]
    assert "criterio_inventado" in resultado["erro"]
    assert "casos.json" not in resultado["erro"] and "\\" not in resultado["erro"] and "/" not in resultado["erro"]
    assert resultado["obtido"] is None and resultado["falhas"] == []
    assert resultado["descricao"] == "caso de teste"
    assert [r["status"] for r in corpo["resultados"] if r["caso_id"] != "C-CRITERIO"] == ["passou", "passou", "falhou"]


def test_caso_que_o_motor_recusa_vira_erro(cliente: TestClient, com_casos: Path):
    # o caso passa na validação do kb (respostas é um dict livre), mas o motor rejeita o valor da resposta
    _acrescentar_caso(com_casos, _caso_extra("C-TALVEZ", respostas={"pergunta_x": "talvez"}))
    corpo = _executar(cliente)
    resultado = _resultado(corpo, "C-TALVEZ")
    assert resultado["status"] == "erro"
    assert "pergunta_x" in resultado["erro"]
    assert resultado["obtido"] is None
    assert (corpo["total"], corpo["passou"], corpo["falhou"]) == (4, 2, 1)


def test_excecao_inesperada_do_motor_vira_erro_sem_vazar_detalhe(
    cliente: TestClient, com_casos: Path, monkeypatch: pytest.MonkeyPatch
):
    original = casos_servico.executar_caso

    def com_defeito(base, caso):
        if caso["id"] == "C-D1-OK":
            raise RuntimeError(r"falha em C:\segredo\engine\sessao.py")
        return original(base, caso)

    monkeypatch.setattr(casos_servico, "executar_caso", com_defeito)
    corpo = _executar(cliente)
    resultado = _resultado(corpo, "C-D1-OK")
    assert resultado["status"] == "erro"
    assert resultado["erro"]
    assert "segredo" not in resultado["erro"] and "sessao.py" not in resultado["erro"]
    assert [r["status"] for r in corpo["resultados"]] == ["erro", "passou", "falhou"]


def test_entrada_que_nao_e_caso_nem_derruba_nem_repete_id(cliente: TestClient, com_casos: Path):
    _acrescentar_caso(com_casos, _caso_extra("C-D1-OK"))  # id repetido
    _acrescentar_caso(com_casos, {"descricao": "sem id e sem modo"})
    casos = json.loads(com_casos.read_text(encoding="utf-8"))
    casos.append(7)  # nem objeto é
    com_casos.write_text(json.dumps(casos), encoding="utf-8")

    corpo = _executar(cliente)
    assert corpo["total"] == 6
    ids = [r["caso_id"] for r in corpo["resultados"]]
    assert len(set(ids)) == 6  # nenhum id se repete, senão o banco recusaria a gravação
    assert ids[:3] == ["C-D1-OK", "C-BV-OK", "C-FALHA"]
    assert [r["status"] for r in corpo["resultados"]] == ["passou", "passou", "falhou", "erro", "erro", "erro"]
    assert "repetido" in corpo["resultados"][3]["erro"]
    assert corpo["resultados"][4]["descricao"] == "sem id e sem modo"
    assert corpo["resultados"][5]["descricao"] == ""


def test_sem_casos_total_zero(cliente: TestClient):
    corpo = _executar(cliente)  # sem a fixture com_casos: não há casos/casos.json
    assert (corpo["total"], corpo["passou"], corpo["falhou"]) == (0, 0, 0)
    assert corpo["resultados"] == [] and corpo["mudancas"] == [] and corpo["comparada_com"] is None


def test_arquivo_de_casos_corrompido_e_erro_do_servidor(cliente: TestClient, com_casos: Path):
    com_casos.write_text("{ isto não é JSON", encoding="utf-8")
    resposta = cliente.post("/api/base/versoes/v0001/execucoes", json={"casos": None})
    erro = _erro(resposta, 500, "erro_interno")
    assert "casos" not in erro["mensagem"].lower()


def test_casos_com_bom_utf8_sao_lidos_como_no_carregador(cliente: TestClient, com_casos: Path, config: Configuracao):
    texto = com_casos.read_text(encoding="utf-8")
    com_casos.write_text(texto, encoding="utf-8-sig")  # o editor do Windows grava o BOM
    assert com_casos.read_bytes().startswith(codecs.BOM_UTF8)

    corpo = _executar(cliente)
    assert (corpo["total"], corpo["passou"], corpo["falhou"]) == (3, 2, 1)
    # o mesmo arquivo e os mesmos ids que o kb.carregador entrega
    ids_do_kb = [c.id for c in Repositorio(config.base_dir, hoje=config.hoje).carregar_casos()]
    assert [r["caso_id"] for r in corpo["resultados"]] == ids_do_kb


@pytest.mark.parametrize("conteudo", ["{}", '{"id": "C-1"}', "null", '"casos"', "7"])
def test_casos_json_valido_que_nao_e_lista_e_erro_do_servidor(
    cliente: TestClient, com_casos: Path, config: Configuracao, caplog: pytest.LogCaptureFixture, conteudo: str
):
    # igual ao JSON quebrado: 500 erro_interno de corpo fixo, o motivo só no log, nada gravado
    com_casos.write_text(conteudo, encoding="utf-8")
    resposta = cliente.post("/api/base/versoes/v0001/execucoes", json={"casos": None})
    erro = _erro(resposta, 500, "erro_interno")
    assert erro["mensagem"] == "Erro interno. Tente novamente."
    assert "lista" not in resposta.text and "casos.json" not in resposta.text
    assert "casos.json deve conter uma lista" in caplog.text
    assert _linhas(config, "SELECT id FROM execucoes_casos") == []


# --- comparação com a versão pai ------------------------------------------------------------


def test_comparacao_com_pai(cliente: TestClient, com_casos: Path, config: Configuracao):
    pai = _executar(cliente)
    assert _salvar_filha(config, 0.1) == "v0002"

    filha = _executar(cliente, versao="v0002")
    validar_contrato("executar_casos", filha)
    assert filha["versao"] == "v0002"
    assert filha["comparada_com"] == "v0001"
    assert (filha["passou"], filha["falhou"]) == (1, 2)
    assert filha["mudancas"] == [{"caso_id": "C-D1-OK", "antes": "passou", "depois": "falhou"}]
    assert _resultado(filha, "C-D1-OK")["mudou_vs_pai"] == "passou->falhou"
    assert _resultado(filha, "C-D1-OK")["falhas"][0]["campo"] == "faixas.d1"
    assert _resultado(filha, "C-BV-OK")["mudou_vs_pai"] is None  # igual ao pai: nada a dizer
    assert _resultado(filha, "C-FALHA")["mudou_vs_pai"] is None
    # a execução do pai não foi tocada
    assert cliente.get(f"/api/base/versoes/v0001/execucoes/{pai['execucao_id']}").json() == pai
    # e o GET da filha traz a mesma comparação
    lida = cliente.get(f"/api/base/versoes/v0002/execucoes/{filha['execucao_id']}").json()
    assert lida == filha


def _mudar_esperado(arquivo: Path, caso_id: str, esperado: dict) -> None:
    casos = json.loads(arquivo.read_text(encoding="utf-8"))
    next(c for c in casos if c["id"] == caso_id)["esperado"] = esperado
    arquivo.write_text(json.dumps(casos, ensure_ascii=False, indent=2), encoding="utf-8")


def test_comparacao_e_por_caso_na_execucao_mais_recente_que_o_contem(
    cliente: TestClient, com_casos: Path, config: Configuracao
):
    # ex_0001: execução completa do pai (D1-OK passou, BV-OK passou, FALHA falhou)
    _executar(cliente)
    # ex_0002: execução parcial, só o C-FALHA, que agora passa (esperado corrigido para o top1 real)
    _mudar_esperado(com_casos, "C-FALHA", {"top1": "d1"})
    parcial = _executar(cliente, casos=["C-FALHA"])
    assert _resultado(parcial, "C-FALHA")["status"] == "passou"
    # na filha o C-FALHA volta a falhar (esperado errado outra vez) e o C-D1-OK sai da faixa
    _mudar_esperado(com_casos, "C-FALHA", {"top1": "outra_doenca"})
    _salvar_filha(config, 0.1)

    filha = _executar(cliente, versao="v0002")
    assert filha["comparada_com"] == "v0001"
    # nenhum caso é "ausente": o C-D1-OK e o C-BV-OK vêm da ex_0001; o C-FALHA, da ex_0002 (a mais recente com ele)
    assert filha["mudancas"] == [
        {"caso_id": "C-D1-OK", "antes": "passou", "depois": "falhou"},
        {"caso_id": "C-FALHA", "antes": "passou", "depois": "falhou"},
    ]
    assert [r["mudou_vs_pai"] for r in filha["resultados"]] == ["passou->falhou", None, "passou->falhou"]
    assert "ausente" not in json.dumps(filha)


def test_caso_que_nenhuma_execucao_do_pai_rodou_e_ausente(cliente: TestClient, com_casos: Path, config: Configuracao):
    _executar(cliente, casos=["C-FALHA"])  # a única execução do pai rodou só o C-FALHA
    _salvar_filha(config, 0.1)
    filha = _executar(cliente, versao="v0002")
    assert filha["comparada_com"] == "v0001"
    assert filha["mudancas"] == [
        {"caso_id": "C-D1-OK", "antes": "ausente", "depois": "falhou"},
        {"caso_id": "C-BV-OK", "antes": "ausente", "depois": "passou"},
    ]
    assert _resultado(filha, "C-D1-OK")["mudou_vs_pai"] == "ausente->falhou"
    assert _resultado(filha, "C-FALHA")["mudou_vs_pai"] is None  # falhou no pai e falha na filha


def test_pai_sem_execucao_nao_compara(cliente: TestClient, com_casos: Path, config: Configuracao):
    _salvar_filha(config, 0.1)  # o pai v0001 nunca foi executado
    filha = _executar(cliente, versao="v0002")
    assert filha["comparada_com"] is None
    assert filha["mudancas"] == []
    assert all(r["mudou_vs_pai"] is None for r in filha["resultados"])


def test_versao_sem_pai_nao_compara(cliente: TestClient, com_casos: Path):
    _executar(cliente)
    segunda = _executar(cliente)  # v0001 não tem pai: a execução anterior dela mesma não conta
    assert segunda["execucao_id"] == "ex_0002"
    assert segunda["comparada_com"] is None and segunda["mudancas"] == []


# --- projeção no SQLite ---------------------------------------------------------------------


def test_projecao_no_sqlite(cliente: TestClient, com_casos: Path, config: Configuracao):
    _acrescentar_caso(com_casos, _caso_extra("C-TALVEZ", respostas={"pergunta_x": "talvez"}))
    _executar(cliente)

    cabecalho = _linhas(config, "SELECT * FROM execucoes_casos WHERE id = 'ex_0001'")
    assert len(cabecalho) == 1
    assert (cabecalho[0]["versao"], cabecalho[0]["total"], cabecalho[0]["passou"], cabecalho[0]["falhou"]) == (
        "v0001",
        4,
        2,
        1,
    )
    assert cabecalho[0]["comparada_com"] is None
    linhas = _linhas(config, "SELECT * FROM resultados_casos WHERE execucao_id = 'ex_0001' ORDER BY rowid")
    assert [(l["caso_id"], l["status"]) for l in linhas] == [
        ("C-D1-OK", "passou"),
        ("C-BV-OK", "passou"),
        ("C-FALHA", "falhou"),
        ("C-TALVEZ", "erro"),
    ]
    extra = json.loads(linhas[3]["extra_json"])
    assert extra["descricao"] == "caso de teste" and extra["erro"] and extra["mudou_vs_pai"] is None
    assert json.loads(linhas[3]["obtido_json"]) is None
    assert json.loads(linhas[2]["falhas_json"])[0]["campo"] == "top1"
    # a versão passou a constar do índice (a chave estrangeira da execução exige)
    assert [l["versao"] for l in _linhas(config, "SELECT versao FROM versoes_base")] == ["v0001"]


def test_gravacao_e_atomica(
    cliente: TestClient, com_casos: Path, config: Configuracao, monkeypatch: pytest.MonkeyPatch
):
    original = casos_servico.repo.inserir_execucao

    def grava_e_falha(*args, **kwargs):
        original(*args, **kwargs)  # o cabeçalho e os resultados já estão no banco, ainda sem commit
        raise RuntimeError("falha depois de gravar")

    monkeypatch.setattr(casos_servico.repo, "inserir_execucao", grava_e_falha)
    _erro(cliente.post("/api/base/versoes/v0001/execucoes", json={"casos": None}), 500, "erro_interno")
    assert _linhas(config, "SELECT id FROM execucoes_casos") == []
    assert _linhas(config, "SELECT caso_id FROM resultados_casos") == []
