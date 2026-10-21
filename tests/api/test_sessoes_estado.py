"""Criar sessão, obter estado e a adaptação ``Sessao.estado()`` -> ``EstadoSessao`` (Task 5).

Base mínima (``tests/fixtures/kb/base_minima.json``), dados fictícios, ``hoje`` = 2026-10-20.
"""
from __future__ import annotations

import json
from contextlib import closing, contextmanager

import pytest
from fastapi.testclient import TestClient

from api.config import Configuracao
from api.contexto import Contexto
from api.db.conexao import abrir
from api.db.repositorios import inserir_animal, inserir_sessao
from api.erros import ErroApi
from api.servicos import sessao_motor
from api.servicos.sessao_motor import aplicar, carregar
from engine.sessao import Sessao
from kb.carregador import Repositorio
from kb.modelos import LimiteDinamico, para_motor
from tests.api.apoio import criar_animal_teste, validar_contrato


@pytest.fixture
def base(base_dir):
    return Repositorio(base_dir).carregar_ativa()


def _erro(resposta, status: int, codigo: str) -> dict:
    assert resposta.status_code == status, resposta.text
    erro = resposta.json()["erro"]
    assert erro["codigo"] == codigo
    return erro


def _criar(cliente: TestClient, animal_id: str, modo: str = "produtor", **extra):
    return cliente.post("/api/sessoes", json={"animal_id": animal_id, "modo": modo, **extra})


def _linha(config: Configuracao, sessao_id: str = "ses_0001") -> dict:
    """A linha da tabela ``sessoes``, direto do SQLite, com o snapshot decodificado."""
    with closing(abrir(config.db_path)) as conn:
        linha = dict(conn.execute("SELECT * FROM sessoes WHERE id = ?", (sessao_id,)).fetchone())
    linha["snapshot"] = json.loads(linha["snapshot_json"])
    return linha


def _consultar(config: Configuracao, sql: str, *parametros):
    with closing(abrir(config.db_path)) as conn:
        return [tuple(linha) for linha in conn.execute(sql, parametros)]


def _gravar_motor(config: Configuracao, animal_id: str, motor: Sessao) -> str:
    """Grava uma sessão feita pelo motor como a API a grava (snapshot D1, sem o ``resumo``: o GET o completa)."""
    estado = motor.estado()
    with closing(abrir(config.db_path)) as conn, conn:
        return inserir_sessao(
            conn, animal_id=animal_id, modo=estado["modo"], versao_base="v0001",
            snapshot={"motor": motor.exportar(), "origens_ficha": {}}, fase=estado["fase"], agora=config.agora(),
        )


# --- criar sessão ----------------------------------------------------------------------------


def test_criar_sessao_201_com_tela_dias_ja_respondida(cliente):
    animal = criar_animal_teste(cliente)  # parto 2026-10-14, hoje 2026-10-20: 6 dias
    resposta = _criar(cliente, animal["id"])
    assert resposta.status_code == 201, resposta.text
    corpo = resposta.json()
    validar_contrato("criar_sessao", corpo)
    assert corpo["sessao_id"] == "ses_0001"
    assert corpo["animal_id"] == animal["id"]
    assert corpo["modo"] == "produtor"
    assert corpo["versao_base"] == "v0001"
    assert corpo["revisao"] == 1
    assert corpo["fase"] == "triagem"
    assert corpo["progresso"] == {"triagem_respondidas": 1, "triagem_total": 2, "dinamicas_feitas": 0, "limite_dinamico": 12}
    proxima = corpo["proxima"]
    assert proxima["tipo"] == "tela_triagem"
    assert proxima["tela_id"] == "sinais"
    assert proxima["selecao"] == "multipla"
    assert proxima["permite_nao_sei"] is True
    assert proxima["titulo"] == "Marque o que você observa no animal."
    assert [c["simbolo"] for c in proxima["campos"]] == ["sinal_a", "sinal_b"]
    assert [(c["entrada"], c["rotulo"]) for c in proxima["campos"]] == [("booleano", "Sinal A"), ("booleano", "Sinal B")]


def test_criar_sessao_veterinario_limite_25(cliente):
    animal = criar_animal_teste(cliente)
    corpo = _criar(cliente, animal["id"], "veterinario").json()
    assert corpo["modo"] == "veterinario"
    assert corpo["progresso"]["limite_dinamico"] == 25
    assert corpo["proxima"]["titulo"] == "Sinais presentes ao exame."  # o texto do modo
    assert [c["rotulo"] for c in corpo["proxima"]["campos"]] == ["Sinal A (exame)", "Sinal B (exame)"]


def test_ficha_ausente_pergunta_dias(cliente):
    animal = criar_animal_teste(cliente, parto=None)
    corpo = _criar(cliente, animal["id"]).json()
    validar_contrato("criar_sessao", corpo)
    assert corpo["progresso"]["triagem_respondidas"] == 0
    assert corpo["proxima"]["tela_id"] == "dias"
    assert corpo["proxima"]["selecao"] == "unica"
    (campo,) = corpo["proxima"]["campos"]
    assert campo["simbolo"] == "dias_em_lactacao"
    assert campo["entrada"] == "numerico"
    assert (campo["min"], campo["max"], campo["unidade"]) == (0, 400, "dias")
    assert campo["opcoes"] is None
    assert campo["rotulo"] == "Dias em lactação"  # sem rótulo na tela: o nome do símbolo


@pytest.mark.parametrize("parto", ["2026-12-01", "1990-01-01"], ids=["no_futuro", "dias_fora_do_dominio"])
def test_parto_no_futuro_nao_quebra(cliente, parto):
    animal = criar_animal_teste(cliente, parto=parto)
    resposta = _criar(cliente, animal["id"])
    assert resposta.status_code == 201, resposta.text
    assert resposta.json()["proxima"]["tela_id"] == "dias"  # os dias não valem: a triagem pergunta


# --- obter estado ----------------------------------------------------------------------------


def test_get_estado_idempotente_nao_sobe_revisao(cliente, config):
    animal = criar_animal_teste(cliente)
    criada = _criar(cliente, animal["id"]).json()
    primeira = cliente.get("/api/sessoes/ses_0001")
    segunda = cliente.get("/api/sessoes/ses_0001")
    assert primeira.status_code == segunda.status_code == 200
    assert primeira.json() == segunda.json() == criada
    assert primeira.json()["revisao"] == 1
    validar_contrato("obter_sessao", primeira.json())
    assert _linha(config)["revisao"] == 1


def test_urgencia_padrao(cliente):
    animal = criar_animal_teste(cliente)
    corpo = _criar(cliente, animal["id"]).json()
    assert corpo["urgencia"] == {"nivel": "sem_problema", "provisoria": True, "origem": "padrao", "regras": []}
    assert corpo["alerta"] is None


def test_sessao_inexistente_404(cliente, config):
    _erro(cliente.get("/api/sessoes/ses_9999"), 404, "nao_encontrado")
    _erro(_criar(cliente, "an_999"), 404, "nao_encontrado")
    animal = criar_animal_teste(cliente)
    _erro(_criar(cliente, animal["id"], versao_base="v0099"), 404, "nao_encontrado")
    _erro(_criar(cliente, animal["id"], versao_base="abc"), 404, "nao_encontrado")  # nem é um id de versão
    _erro(_criar(cliente, animal["id"], modo="x"), 422, "entrada_invalida")
    assert _consultar(config, "SELECT COUNT(*) FROM sessoes") == [(0,)]  # nada foi criado


def test_texto_ilegivel_no_id_vira_422_e_nao_500(cliente, config):
    animal = criar_animal_teste(cliente)
    resposta = cliente.post(
        "/api/sessoes", content=b'{"animal_id": "\\ud800", "modo": "produtor"}', headers={"content-type": "application/json"}
    )
    _erro(resposta, 422, "entrada_invalida")
    resposta = cliente.post(
        "/api/sessoes",
        content=b'{"animal_id": "' + animal["id"].encode() + b'", "modo": "produtor", "versao_base": "\\ud800"}',
        headers={"content-type": "application/json"},
    )
    _erro(resposta, 422, "entrada_invalida")
    assert _consultar(config, "SELECT COUNT(*) FROM sessoes") == [(0,)]


def test_404_de_versao_nao_ecoa_o_valor_inteiro(cliente):
    animal = criar_animal_teste(cliente)
    erro = _erro(_criar(cliente, animal["id"], versao_base="v" + "9" * 5000), 404, "nao_encontrado")
    assert len(erro["mensagem"]) < 100
    assert "9" * 50 not in erro["mensagem"]
    erro = _erro(_criar(cliente, animal["id"], versao_base="v0099"), 404, "nao_encontrado")
    assert "'v0099'" in erro["mensagem"]  # o valor curto continua aparecendo


def test_sem_versao_ativa_409_mas_versao_explicita_funciona(cliente, base_dir):
    animal = criar_animal_teste(cliente)
    (base_dir / "ativa.json").unlink()  # a base continua em versoes/, só não há ponteiro
    erro = _erro(_criar(cliente, animal["id"]), 409, "conflito")
    assert "Nenhuma versão ativa" in erro["mensagem"]
    assert _criar(cliente, animal["id"], versao_base="v0001").status_code == 201


def test_cada_sessao_guarda_a_versao_em_que_nasceu(cliente, base_dir, hoje):
    """Ativar outra versão não muda o texto da tela nem o limite de uma sessão já criada; a nova pega os da ativa."""
    repo = Repositorio(base_dir, hoje=lambda: hoje)
    segunda = repo.carregar("v0001").model_copy(deep=True)
    next(t for t in segunda.meta.triagem if t.id == "sinais").texto["produtor"] = "Marque os sinais (segunda versão)."
    segunda.meta.limite_dinamico = LimiteDinamico(produtor=7, veterinario=9)

    animal = criar_animal_teste(cliente)
    antiga = _criar(cliente, animal["id"]).json()  # nasce na v0001, a ativa
    assert antiga["versao_base"] == "v0001"
    assert antiga["proxima"]["titulo"] == "Marque o que você observa no animal."
    assert antiga["progresso"]["limite_dinamico"] == 12

    assert repo.salvar_nova(segunda, autor="teste", nota="segunda versão") == "v0002"
    repo.ativar("v0002")
    assert cliente.get("/api/sessoes/ses_0001").json() == antiga  # presa à v0001: mesmo texto, limite e revisão

    nova = _criar(cliente, animal["id"]).json()  # a ativa agora é a v0002
    assert nova["versao_base"] == "v0002"
    assert nova["proxima"]["titulo"] == "Marque os sinais (segunda versão)."
    assert nova["progresso"]["limite_dinamico"] == 7
    assert _criar(cliente, animal["id"], "veterinario").json()["progresso"]["limite_dinamico"] == 9

    explicita = _criar(cliente, animal["id"], "veterinario", versao_base="v0001").json()  # pede a v0001 com a v0002 ativa
    assert explicita["versao_base"] == "v0001"
    assert explicita["proxima"]["titulo"] == "Sinais presentes ao exame."
    assert explicita["progresso"]["limite_dinamico"] == 25
    assert cliente.get("/api/sessoes/ses_0001").json() == antiga  # e a primeira continua igual


# --- persistência: snapshot (D1/D2), resumo e projeções --------------------------------------


def test_snapshot_persistido_restaura_igual(cliente, config, base):
    animal = criar_animal_teste(cliente)
    _criar(cliente, animal["id"])
    corpo = cliente.get("/api/sessoes/ses_0001").json()
    snapshot = _linha(config)["snapshot"]
    restaurada = Sessao.restaurar(para_motor(base), **snapshot["motor"])
    estado = restaurada.estado()
    assert estado["fase"] == corpo["fase"]
    assert estado["proxima"]["id"] == corpo["proxima"]["tela_id"]
    assert estado["urgencia"] == corpo["urgencia"]["nivel"]
    assert estado["progresso"]["triagem_respondida"] == corpo["progresso"]["triagem_respondidas"]
    # D2: o snapshot já tinha os eventos de pergunta feita; restaurar e chamar estado() não acrescenta nenhum
    assert json.loads(json.dumps(restaurada.exportar())) == snapshot["motor"]
    assert set(snapshot["motor"]["perguntas_feitas"]) == {"sinal_a", "sinal_b"}


def test_get_completa_snapshot_exportado_antes_de_estado(cliente, config, base, monkeypatch):
    """D2: snapshot sem ``perguntas_feitas``. O 1º GET o completa (snapshot e projeção) sem subir a revisão; o 2º não regrava."""
    animal = criar_animal_teste(cliente)
    motor = Sessao(para_motor(base), "produtor", {"dias_em_lactacao": 6})
    snapshot = {"motor": motor.exportar(), "origens_ficha": {"dias_em_lactacao": "manual"}}  # antes de estado()
    assert snapshot["motor"]["perguntas_feitas"] == {}  # premissa do teste
    with closing(abrir(config.db_path)) as conn, conn:
        sessao_id = inserir_sessao(
            conn, animal_id=animal["id"], modo="produtor", versao_base="v0001", snapshot=snapshot, fase="triagem",
            agora=config.agora(),
        )
    assert _consultar(config, "SELECT COUNT(*) FROM perguntas_feitas") == [(0,)]

    chamadas: list[dict] = []
    original = sessao_motor.persistir

    def espiao(*args, **kwargs):
        chamadas.append(kwargs)
        return original(*args, **kwargs)

    monkeypatch.setattr(sessao_motor, "persistir", espiao)
    primeiro = cliente.get(f"/api/sessoes/{sessao_id}").json()
    assert primeiro["revisao"] == 1
    assert [c["subir_revisao"] for c in chamadas] == [False]  # regravou uma vez, sem contar como mudança
    linha = _linha(config, sessao_id)
    assert linha["revisao"] == 1
    assert set(linha["snapshot"]["motor"]["perguntas_feitas"]) == {"sinal_a", "sinal_b"}
    assert [p[0] for p in _consultar(config, "SELECT simbolo FROM perguntas_feitas ORDER BY ordem")] == [
        "sinal_a", "sinal_b",
    ]

    segundo = cliente.get(f"/api/sessoes/{sessao_id}").json()
    assert segundo == primeiro
    assert len(chamadas) == 1  # nada novo: o segundo GET não chamou persistir


def test_snapshot_grava_resumo_e_origens(cliente, config):
    animal = criar_animal_teste(cliente)
    _criar(cliente, animal["id"])
    snapshot = _linha(config)["snapshot"]
    assert set(snapshot) == {"motor", "origens_ficha", "resumo"}
    assert snapshot["resumo"] == {"urgencia": "sem_problema", "top1": None}
    assert snapshot["origens_ficha"] == {"dias_em_lactacao": "manual"}


def test_projecoes_na_criacao(cliente, config):
    animal = criar_animal_teste(cliente)
    _criar(cliente, animal["id"])
    respostas = _consultar(config, "SELECT simbolo, valor_json, nao_sei, origem, tela_id, ordem FROM respostas")
    assert respostas == [("dias_em_lactacao", "6", 0, "ficha", None, 1)]
    perguntas = _consultar(config, "SELECT simbolo, ordem, motivo_json FROM perguntas_feitas ORDER BY ordem")
    assert [(p[0], p[1], json.loads(p[2])) for p in perguntas] == [
        ("sinal_a", 1, "Triagem obrigatória, tela 2 de 2"),
        ("sinal_b", 2, "Triagem obrigatória, tela 2 de 2"),
    ]
    linha = _linha(config)
    assert (linha["fase"], linha["motivo_parada"], linha["modo"], linha["bandeiras_reconhecidas_json"]) == (
        "triagem", None, "produtor", "[]",
    )


def _ajustar_base_completa(dados: dict) -> None:
    """Acrescenta à base mínima um símbolo de ficha (``raca_grupo``) e uma tela categórica de triagem (``apetite``)."""
    dados["simbolos"] += [
        {
            "id": "raca_grupo", "tipo": "ficha", "nome": "Grupo racial", "campo_ficha": "raca_grupo",
            "dominio": {"tipo": "categorico", "valores": ["europeia", "zebuina", "cruzada"]},
        },
        {
            "id": "apetite", "tipo": "pergunta", "nome": "Apetite",
            "dominio": {"tipo": "categorico", "valores": ["normal", "reduzido", "ausente"]},
            "pergunta": {"produtor": "Como está o apetite?", "veterinario": "Apetite?"},
        },
    ]
    dados["regras"].append(
        {
            "id": "R-D1-04", "se": [{"simbolo": "apetite", "op": "=", "valor": "ausente"}],
            "entao": {"simbolo": "d1", "cf": 0.3}, "fonte": "fixture de software", "status": "validada",
        }
    )
    dados["meta"]["triagem"].insert(
        0,
        {
            "id": "apetite_tela", "selecao": "unica", "simbolos": ["apetite"],
            "texto": {"produtor": "Como está o apetite?", "veterinario": "Apetite do animal?"},
            "opcoes": {
                "apetite": {"produtor": "Apetite"},  # sem rótulo no modo veterinário: cai no nome do símbolo
                "apetite.reduzido": {"produtor": "Reduzido", "veterinario": "Apetite reduzido"},
                "apetite.ausente": {"produtor": "Ausente"},  # "normal" sem rótulo: cai no próprio valor
            },
        },
    )


def _regra(dados: dict, id: str) -> dict:
    return next(r for r in dados["regras"] if r["id"] == id)


def _ajustar_bandeira_dinamica(dados: dict) -> None:
    """Uma bandeira na fase dinâmica (``pergunta_x``), com outra pergunta (``pergunta_y``) ainda a fazer."""
    _regra(dados, "R-D1-01")["entao"]["cf"] = 0.3
    dados["simbolos"].append(
        {
            "id": "pergunta_y", "tipo": "pergunta", "nome": "Pergunta Y", "dominio": {"tipo": "booleano"},
            "pergunta": {"produtor": "Você notou o fato Y?", "veterinario": "Fato Y presente?"},
        }
    )
    dados["regras"] += [
        {
            "id": "R-D1-05", "se": [{"simbolo": "pergunta_y"}], "entao": {"simbolo": "d1", "cf": 0.3},
            "fonte": "fixture de software", "status": "validada",
        },
        {
            "id": "R-BV-02", "se": [{"simbolo": "sinal_a"}, {"simbolo": "pergunta_x"}],  # a validação exige um símbolo da triagem
            "entao": {"simbolo": "chamar_agora", "cf": 0.99},
            "classe": "bandeira_vermelha", "fonte": "fixture de software", "status": "validada",
        },
    ]


def _ajustar_d1_fraco(dados: dict) -> None:
    """``R-D1-01`` com cf 0,4: d1 passa de 0,35 (hipótese relevante) e fica abaixo do ``cf_minimo`` 0,5 de ``R-URG-d1``."""
    _regra(dados, "R-D1-01")["entao"]["cf"] = 0.4


def _ajustar_regra_observar(dados: dict) -> None:
    """Além de ``_ajustar_d1_fraco``, uma regra de urgência que conclui ``observar`` (a base mínima não tem)."""
    _ajustar_d1_fraco(dados)
    dados["regras"].append(
        {
            "id": "R-URG-obs", "se": [{"simbolo": "d1", "cf_minimo": 0.3}], "entao": {"simbolo": "observar", "cf": 0.7},
            "classe": "urgencia", "fonte": "fixture de software", "status": "validada",
        }
    )


def _ajustar_tela_no_fim(dados: dict) -> None:
    """Uma terceira tela depois de ``sinais``: a triagem continua aberta quando a bandeira dispara."""
    dados["meta"]["triagem"].append(
        {
            "id": "extra", "selecao": "unica", "simbolos": ["pergunta_x"],
            "texto": {"produtor": "Notou o fato X?", "veterinario": "Fato X?"},
        }
    )


def _motor(config: Configuracao, modo: str = "produtor") -> Sessao:
    """Um motor novo sobre a base ativa de ``config``, com a ficha de 6 dias em lactação."""
    return Sessao(para_motor(Repositorio(config.base_dir).carregar_ativa()), modo, {"dias_em_lactacao": 6})


def test_origens_ficha_por_simbolo(cliente_com, agora):
    """``animal.origens`` é por campo da ficha; o snapshot guarda por id de símbolo, e os dias herdam o parto."""
    config, cliente = cliente_com(_ajustar_base_completa)
    with closing(abrir(config.db_path)) as conn, conn:
        inserir_animal(
            conn, brinco="BR-0007", nome=None, ficha={"data_ultimo_parto": "2026-10-14", "raca_grupo": "zebuina"},
            origens={"data_ultimo_parto": "importacao"}, agora=agora,
        )
    assert _criar(cliente, "an_001").status_code == 201
    snapshot = _linha(config)["snapshot"]
    assert snapshot["origens_ficha"] == {"dias_em_lactacao": "importacao", "raca_grupo": "manual"}
    assert snapshot["motor"]["fatos"]["raca_grupo"]["valor"] == "zebuina"  # a ficha inteira vai para o motor


def test_tela_categorica_com_opcoes_rotuladas(cliente_com):
    _, cliente = cliente_com(_ajustar_base_completa)
    animal = criar_animal_teste(cliente)
    produtor = _criar(cliente, animal["id"]).json()
    validar_contrato("criar_sessao", produtor)
    assert produtor["proxima"]["tela_id"] == "apetite_tela"
    (campo,) = produtor["proxima"]["campos"]
    assert (campo["simbolo"], campo["entrada"], campo["rotulo"]) == ("apetite", "categorico", "Apetite")
    assert campo["opcoes"] == [
        {"valor": "normal", "rotulo": "normal"},
        {"valor": "reduzido", "rotulo": "Reduzido"},
        {"valor": "ausente", "rotulo": "Ausente"},
    ]
    assert (campo["unidade"], campo["min"], campo["max"]) == (None, None, None)

    veterinario = _criar(cliente, animal["id"], "veterinario").json()
    (campo,) = veterinario["proxima"]["campos"]
    assert campo["rotulo"] == "Apetite"  # o nome do símbolo
    assert [o["rotulo"] for o in campo["opcoes"]] == ["normal", "Apetite reduzido", "ausente"]


# --- adaptação do estado do motor (sessões feitas pelo motor e lidas pela API) ---------------


def test_get_completa_snapshot_antigo_sem_subir_revisao(cliente, config, base):
    """Snapshot sem ``resumo`` (gravado por fora): o GET o completa uma vez e a revisão não muda."""
    animal = criar_animal_teste(cliente)
    sessao_id = _gravar_motor(config, animal["id"], Sessao(para_motor(base), "produtor", {"dias_em_lactacao": 6}))
    assert "resumo" not in _linha(config, sessao_id)["snapshot"]
    primeiro = cliente.get(f"/api/sessoes/{sessao_id}").json()
    assert primeiro["revisao"] == 1
    assert _linha(config, sessao_id)["snapshot"]["resumo"] == {"urgencia": "sem_problema", "top1": None}
    assert cliente.get(f"/api/sessoes/{sessao_id}").json() == primeiro
    assert _linha(config, sessao_id)["revisao"] == 1


def test_estado_pergunta_dinamica_e_urgencia_por_regra(cliente, config, base):
    animal = criar_animal_teste(cliente)
    motor = Sessao(para_motor(base), "produtor", {"dias_em_lactacao": 6})
    motor.responder_triagem("sinais", {"sinal_a": True, "sinal_b": False})  # d1 = 0,6: dispara R-URG-d1
    sessao_id = _gravar_motor(config, animal["id"], motor)
    corpo = cliente.get(f"/api/sessoes/{sessao_id}").json()
    validar_contrato("obter_sessao", corpo)
    assert corpo["fase"] == "dinamica"
    assert corpo["progresso"] == {"triagem_respondidas": 2, "triagem_total": 2, "dinamicas_feitas": 0, "limite_dinamico": 12}
    assert corpo["proxima"] == {
        "tipo": "pergunta", "simbolo": "pergunta_x", "entrada": "booleano", "permite_nao_sei": True,
        "texto": "Você notou o fato X?", "motivo_resumo": "Ajuda a separar a hipótese D1 de outras.",
        "porque_disponivel": True, "opcoes": None, "unidade": None, "min": None, "max": None,
    }
    assert corpo["urgencia"] == {"nivel": "chamar_agora", "provisoria": True, "origem": "regra_urgencia", "regras": ["R-URG-d1"]}
    assert corpo["alerta"] is None  # urgência por regra não é bandeira vermelha


def test_observar_por_limiar_sem_regra_e_origem_padrao(cliente_com):
    """d1 acima de 0,35 sem regra de urgência disparada: o motor devolve ``observar`` e a origem é ``padrao``."""
    config, cliente = cliente_com(_ajustar_d1_fraco)
    animal = criar_animal_teste(cliente)
    motor = _motor(config)
    motor.responder_triagem("sinais", {"sinal_a": True, "sinal_b": False})
    corpo = cliente.get(f"/api/sessoes/{_gravar_motor(config, animal['id'], motor)}").json()
    validar_contrato("obter_sessao", corpo)
    assert corpo["urgencia"] == {"nivel": "observar", "provisoria": True, "origem": "padrao", "regras": []}
    assert corpo["alerta"] is None


def test_observar_com_regra_de_urgencia_e_origem_regra_urgencia(cliente_com):
    config, cliente = cliente_com(_ajustar_regra_observar)
    animal = criar_animal_teste(cliente)
    motor = _motor(config)
    motor.responder_triagem("sinais", {"sinal_a": True, "sinal_b": False})
    corpo = cliente.get(f"/api/sessoes/{_gravar_motor(config, animal['id'], motor)}").json()
    validar_contrato("obter_sessao", corpo)
    assert corpo["urgencia"] == {"nivel": "observar", "provisoria": True, "origem": "regra_urgencia", "regras": ["R-URG-obs"]}
    assert corpo["alerta"] is None


def test_bandeira_pausa_no_produtor_e_encerra_sem_potencial(cliente, config, base):
    """Na base mínima a triagem acaba em ``sinais``; com a bandeira, o motor encerra (``sem_potencial``) e pausa."""
    animal = criar_animal_teste(cliente)
    motor = Sessao(para_motor(base), "produtor", {"dias_em_lactacao": 6})
    motor.responder_triagem("sinais", {"sinal_a": False, "sinal_b": True})
    corpo = cliente.get(f"/api/sessoes/{_gravar_motor(config, animal['id'], motor)}").json()
    validar_contrato("obter_sessao", corpo)
    assert corpo["fase"] == "encerrada" and corpo["proxima"] is None
    assert corpo["urgencia"] == {"nivel": "chamar_agora", "provisoria": False, "origem": "bandeira_vermelha", "regras": ["R-BV-01"]}
    assert corpo["alerta"] == {
        "nivel": "chamar_agora", "regras": ["R-BV-01"], "pausa": True, "acoes": ["ver_parecer"],  # não há o que continuar
        "texto": "Sintoma grave: chame um veterinário o mais rápido possível.",
    }


def test_bandeira_na_fase_dinamica_pausa_com_as_duas_acoes(cliente_com):
    config, cliente = cliente_com(_ajustar_bandeira_dinamica)
    animal = criar_animal_teste(cliente)
    motor = _motor(config)
    motor.responder_triagem("sinais", {"sinal_a": True, "sinal_b": False})
    assert motor.estado()["proxima"]["id"] == "pergunta_x"  # premissa do teste
    motor.responder("pergunta_x", True)  # dispara R-BV-02 com a pergunta_y ainda aberta
    corpo = cliente.get(f"/api/sessoes/{_gravar_motor(config, animal['id'], motor)}").json()
    validar_contrato("obter_sessao", corpo)
    assert corpo["fase"] == "dinamica"
    assert corpo["proxima"] is None  # pausada pela bandeira
    assert corpo["alerta"]["pausa"] is True
    assert corpo["alerta"]["acoes"] == ["ver_parecer", "continuar"]
    assert corpo["urgencia"] == {"nivel": "chamar_agora", "provisoria": True, "origem": "bandeira_vermelha", "regras": ["R-BV-02"]}


def test_bandeira_com_triagem_aberta_pausa_o_produtor(cliente_com):
    config, cliente = cliente_com(_ajustar_tela_no_fim)
    animal = criar_animal_teste(cliente)
    motor = _motor(config)
    motor.responder_triagem("sinais", {"sinal_a": False, "sinal_b": True})
    corpo = cliente.get(f"/api/sessoes/{_gravar_motor(config, animal['id'], motor)}").json()
    validar_contrato("obter_sessao", corpo)
    assert corpo["fase"] == "triagem"
    assert corpo["proxima"] is None  # pausada pela bandeira: o frontend mostra o alerta, não uma tela
    assert corpo["urgencia"] == {"nivel": "chamar_agora", "provisoria": True, "origem": "bandeira_vermelha", "regras": ["R-BV-01"]}
    assert corpo["alerta"]["pausa"] is True
    assert corpo["alerta"]["acoes"] == ["ver_parecer", "continuar"]


def test_bandeira_nao_pausa_o_veterinario(cliente_com):
    config, cliente = cliente_com(_ajustar_tela_no_fim)
    animal = criar_animal_teste(cliente)
    motor = _motor(config, "veterinario")
    motor.responder_triagem("sinais", {"sinal_a": False, "sinal_b": True})
    corpo = cliente.get(f"/api/sessoes/{_gravar_motor(config, animal['id'], motor)}").json()
    assert corpo["alerta"]["pausa"] is False
    assert corpo["alerta"]["acoes"] == []
    assert corpo["alerta"]["regras"] == ["R-BV-01"]
    assert corpo["alerta"]["texto"] == "Bandeira vermelha: sinal de gravidade presente nos dados informados."
    assert corpo["urgencia"]["origem"] == "bandeira_vermelha"
    assert corpo["proxima"]["tela_id"] == "extra"  # o veterinário segue a triagem


def test_continuar_e_ver_parecer_no_estado(cliente_com):
    config, cliente = cliente_com(_ajustar_tela_no_fim)
    animal = criar_animal_teste(cliente)
    motor = _motor(config)
    motor.responder_triagem("sinais", {"sinal_a": False, "sinal_b": True})
    motor.acao_bandeira("continuar")
    corpo = cliente.get(f"/api/sessoes/{_gravar_motor(config, animal['id'], motor)}").json()
    assert corpo["alerta"]["pausa"] is False and corpo["alerta"]["acoes"] == []
    assert corpo["urgencia"]["nivel"] == "chamar_agora"  # o quadro urgente continua no topo
    assert corpo["proxima"]["tela_id"] == "extra" and corpo["urgencia"]["provisoria"] is True

    motor.acao_bandeira("ver_parecer")
    corpo = cliente.get(f"/api/sessoes/{_gravar_motor(config, animal['id'], motor)}").json()
    assert corpo["fase"] == "encerrada"
    assert corpo["proxima"] is None
    assert corpo["urgencia"]["provisoria"] is False
    assert corpo["alerta"]["pausa"] is False


# --- aplicar: o contrato que as Tasks 6 a 8 usam ---------------------------------------------


@contextmanager
def _contexto(config: Configuracao):
    """Um ``Contexto`` como o de uma requisição: conexão própria, fechada ao sair."""
    with closing(abrir(config.db_path)) as conn:
        yield Contexto(config=config, conn=conn, repo=Repositorio(config.base_dir, hoje=config.hoje))


def test_aplicar_grava_snapshot_projecoes_e_sobe_revisao(cliente, config):
    animal = criar_animal_teste(cliente)
    _criar(cliente, animal["id"])
    with _contexto(config) as ctx:
        carregada = carregar(ctx, "ses_0001")
        estado = aplicar(
            ctx, carregada, lambda m: m.responder_triagem("sinais", {"sinal_a": True, "sinal_b": False}), muda=True
        )
    assert estado.revisao == 2
    assert estado.fase == "dinamica"
    assert estado.proxima.simbolo == "pergunta_x"
    assert cliente.get("/api/sessoes/ses_0001").json() == estado.model_dump(mode="json")  # o GET lê o que foi gravado
    linha = _linha(config)
    assert (linha["revisao"], linha["fase"], linha["modo"]) == (2, "dinamica", "produtor")
    assert linha["snapshot"]["resumo"] == {"urgencia": "chamar_agora", "top1": "d1"}
    respostas = dict(_consultar(config, "SELECT simbolo, valor_json FROM respostas"))
    assert respostas == {"dias_em_lactacao": "6", "sinal_a": "true", "sinal_b": "false"}
    assert [p[0] for p in _consultar(config, "SELECT simbolo FROM perguntas_feitas ORDER BY ordem")] == [
        "sinal_a", "sinal_b", "pergunta_x",
    ]


def test_aplicar_sem_mudar_nao_sobe_revisao(cliente, config):
    animal = criar_animal_teste(cliente)
    _criar(cliente, animal["id"])
    with _contexto(config) as ctx:
        estado = aplicar(ctx, carregar(ctx, "ses_0001"), lambda m: m.trocar_modo("veterinario"), muda=False)
    assert estado.revisao == 1
    assert estado.modo == "veterinario"  # gravou o que o motor fez, só não contou como mudança do usuário
    assert _linha(config)["modo"] == "veterinario"


def test_aplicar_valor_invalido_vira_422_sem_escrever(cliente, config):
    animal = criar_animal_teste(cliente)
    _criar(cliente, animal["id"])
    antes = _linha(config)
    with _contexto(config) as ctx:
        carregada = carregar(ctx, "ses_0001")
        with pytest.raises(ErroApi) as excecao:
            aplicar(ctx, carregada, lambda m: m.responder_triagem("sinais", {"sinal_z": True}), muda=True)
    assert (excecao.value.status, excecao.value.codigo) == (422, "resposta_invalida")
    assert _linha(config) == antes  # nada escrito
    assert [p for p in _consultar(config, "SELECT simbolo FROM respostas")] == [("dias_em_lactacao",)]


def test_carregar_inexistente_404(cliente, config):
    with _contexto(config) as ctx:
        with pytest.raises(ErroApi) as excecao:
            carregar(ctx, "ses_9999")
    assert (excecao.value.status, excecao.value.codigo) == (404, "nao_encontrado")


# --- histórico do animal lê o resumo, sem rodar o motor --------------------------------------


def test_listar_sessoes_do_animal_le_o_resumo_sem_rodar_o_motor(cliente, monkeypatch):
    animal = criar_animal_teste(cliente)
    _criar(cliente, animal["id"])

    def proibido(*args, **kwargs):
        raise AssertionError("o motor não deve rodar quando o snapshot tem o resumo")

    monkeypatch.setattr(sessao_motor.Sessao, "restaurar", proibido)
    corpo = cliente.get(f"/api/animais/{animal['id']}/sessoes").json()
    validar_contrato("listar_sessoes_animal", corpo)
    assert [(i["sessao_id"], i["urgencia"], i["top1"], i["fase"]) for i in corpo["itens"]] == [
        ("ses_0001", "sem_problema", None, "triagem")
    ]


def test_listar_sessoes_do_animal_usa_o_resumo_gravado(cliente, config, base):
    """O resumo gravado no snapshot é o que o histórico mostra (``top1`` só com evidência)."""
    animal = criar_animal_teste(cliente)
    motor = Sessao(para_motor(base), "produtor", {"dias_em_lactacao": 6})
    motor.responder_triagem("sinais", {"sinal_a": True, "sinal_b": False})
    sessao_id = _gravar_motor(config, animal["id"], motor)
    cliente.get(f"/api/sessoes/{sessao_id}")  # completa o snapshot com o resumo
    assert _linha(config, sessao_id)["snapshot"]["resumo"] == {"urgencia": "chamar_agora", "top1": "d1"}
    (item,) = cliente.get(f"/api/animais/{animal['id']}/sessoes").json()["itens"]
    assert (item["urgencia"], item["top1"]) == ("chamar_agora", "d1")
