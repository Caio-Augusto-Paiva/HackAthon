"""Animais, ficha e importação de prontuário (Task 4). Dados fictícios apenas."""
from __future__ import annotations

from contextlib import closing
from datetime import date, timedelta
from pathlib import Path

import pytest
from fastapi.testclient import TestClient

from api.config import Configuracao
from api.db import repositorios
from api.db.conexao import abrir
from api.db.repositorios import inserir_sessao
from api.main import criar_app
from api.servicos.ficha import dias_em_lactacao, ficha_para_motor, validar_ficha
from engine.sessao import Sessao
from kb.carregador import Repositorio
from kb.modelos import carregar_base, para_motor
from tests.api.apoio import criar_animal_teste, validar_contrato

FIXTURES = Path(__file__).resolve().parents[1] / "fixtures" / "api"

FICHA_MIMOSA = {"data_ultimo_parto": "2026-10-14", "raca_grupo": "cruzada", "historico_mastite_12m": True}


def _ajustar(dados: dict) -> None:
    """Acrescenta à base mínima os símbolos de ficha usados aqui (``campo_ficha`` igual ao id)."""
    dados["simbolos"] += [
        {
            "id": "raca_grupo", "tipo": "ficha", "nome": "Grupo racial", "campo_ficha": "raca_grupo",
            "dominio": {"tipo": "categorico", "valores": ["europeia", "zebuina", "cruzada"]},
        },
        {
            "id": "historico_mastite_12m", "tipo": "ficha", "nome": "Mastite nos últimos 12 meses",
            "campo_ficha": "historico_mastite_12m", "dominio": {"tipo": "booleano"},
        },
        {
            "id": "numero_lactacoes", "tipo": "ficha", "nome": "Número de lactações", "campo_ficha": "numero_lactacoes",
            "dominio": {"tipo": "numerico", "min": 0, "max": 20},
        },
    ]


@pytest.fixture
def base_dir(tmp_path, fabrica_base_dir):
    """Sobrescreve a fixture do conftest: a base ativa tem os símbolos de ficha de ``_ajustar``."""
    return fabrica_base_dir(tmp_path / "base", _ajustar)


@pytest.fixture
def base(base_dir):
    return Repositorio(base_dir).carregar_ativa()


def _criar(cliente: TestClient, brinco: str = "BR-0001", nome: str = "Mimosa", ficha: dict | None = None):
    return cliente.post("/api/animais", json={"brinco": brinco, "nome": nome, "ficha": ficha if ficha is not None else FICHA_MIMOSA})


def _enviar(cliente: TestClient, conteudo: bytes, nome: str = "prontuario.csv", gravar: bool | None = None):
    consulta = "" if gravar is None else f"?gravar={'true' if gravar else 'false'}"
    return cliente.post(f"/api/animais/importacao{consulta}", files={"arquivo": (nome, conteudo, "application/octet-stream")})


def _brincos(cliente: TestClient) -> list[str]:
    return [a["brinco"] for a in cliente.get("/api/animais").json()["itens"]]


def _erro(resposta, status: int, codigo: str) -> dict:
    assert resposta.status_code == status, resposta.text
    erro = resposta.json()["erro"]
    assert erro["codigo"] == codigo
    return erro


# --- ficha: funções puras --------------------------------------------------------------------


def test_dias_em_lactacao_calculo():
    hoje = date(2026, 10, 20)
    assert dias_em_lactacao("2026-10-14", hoje) == 6
    assert dias_em_lactacao("2026-10-20", hoje) == 0
    assert dias_em_lactacao(None, hoje) is None
    assert dias_em_lactacao("abc", hoje) is None
    assert dias_em_lactacao("2026-12-01", hoje) is None  # no futuro
    assert dias_em_lactacao("2026-02-30", hoje) is None  # data que não existe
    assert dias_em_lactacao("20261014", hoje) is None  # só AAAA-MM-DD
    assert dias_em_lactacao(20261014, hoje) is None  # não é texto


def test_validar_ficha_pelo_dominio(base):
    assert validar_ficha(base, {}) == []
    assert validar_ficha(base, {**FICHA_MIMOSA, "numero_lactacoes": 3, "raca_grupo": None}) == []  # null = ausente
    erros = {e.campo: e.mensagem for e in validar_ficha(
        base,
        {
            "raca_grupo": "nelore", "historico_mastite_12m": "sim", "numero_lactacoes": 21,
            "data_ultimo_parto": "14/10/2026", "cor": "malhada",
        },
    )}
    assert erros["raca_grupo"] == "Valor 'nelore' fora de europeia/zebuina/cruzada."
    assert "verdadeiro ou falso" in erros["historico_mastite_12m"]
    assert "0" in erros["numero_lactacoes"] and "20" in erros["numero_lactacoes"]
    assert "AAAA-MM-DD" in erros["data_ultimo_parto"]
    assert erros["cor"] == "Campo desconhecido."
    assert validar_ficha(base, {"numero_lactacoes": True})  # booleano não é número
    assert validar_ficha(base, {"historico_mastite_12m": 1})  # nem número é booleano


@pytest.mark.parametrize("valor", [float("nan"), float("inf"), float("-inf")])
def test_validar_ficha_rejeita_numero_nao_finito(base, valor):
    erros = validar_ficha(base, {"numero_lactacoes": valor})
    assert [e.campo for e in erros] == ["numero_lactacoes"]
    assert "finito" in erros[0].mensagem


def test_dias_em_lactacao_e_calculado_nao_informado(base):
    erros = validar_ficha(base, {"dias_em_lactacao": 30})
    assert [e.campo for e in erros] == ["dias_em_lactacao"]
    assert "data_ultimo_parto" in erros[0].mensagem


def test_ficha_para_motor(base):
    hoje = date(2026, 10, 20)
    assert ficha_para_motor(base, {}, hoje) == {}
    ficha = {**FICHA_MIMOSA, "numero_lactacoes": None}
    # chaves = id do símbolo; o símbolo de campo_ficha "dias_em_lactacao" vem da data do parto; null é filtrado
    assert ficha_para_motor(base, ficha, hoje) == {
        "dias_em_lactacao": 6, "raca_grupo": "cruzada", "historico_mastite_12m": True,
    }
    # data ausente, inválida ou no futuro: o símbolo é omitido (a pergunta será feita), nunca erro
    for parto in (None, "abc", "2026-12-01"):
        assert "dias_em_lactacao" not in ficha_para_motor(base, {"data_ultimo_parto": parto}, hoje)
    # valor gravado que a base atual não aceita mais também é omitido
    assert ficha_para_motor(base, {"raca_grupo": "nelore"}, hoje) == {}
    # dias fora do domínio da base (0 a 400)
    assert "dias_em_lactacao" not in ficha_para_motor(base, {"data_ultimo_parto": "2024-01-01"}, hoje)


# --- animais: rotas --------------------------------------------------------------------------


def test_criar_animal_201_e_valida_contrato(cliente):
    resposta = _criar(cliente)
    assert resposta.status_code == 201, resposta.text
    corpo = resposta.json()
    assert corpo["id"] == "an_001"
    assert corpo["brinco"] == "BR-0001"
    assert corpo["dias_em_lactacao"] == 6  # a data de "hoje" vem da configuração, não do relógio
    assert corpo["origens"] == {}
    # a ficha sai completa: o que não foi informado fica null
    assert corpo["ficha"] == {**FICHA_MIMOSA, "numero_lactacoes": None}
    validar_contrato("criar_animal", corpo)


def test_brinco_duplicado_409_conflito(cliente):
    assert _criar(cliente).status_code == 201
    _erro(_criar(cliente), 409, "conflito")
    assert len(cliente.get("/api/animais").json()["itens"]) == 1


def test_ficha_invalida_422(cliente):
    erro = _erro(_criar(cliente, ficha={"raca_grupo": "nelore"}), 422, "entrada_invalida")
    assert "nelore" in erro["mensagem"]
    assert erro["detalhes"] == [
        {
            "codigo": "ficha_invalida",
            "severidade": "erro",
            "mensagem": "corpo.ficha.raca_grupo: Valor 'nelore' fora de europeia/zebuina/cruzada.",
        }
    ]
    erro = _erro(_criar(cliente, ficha={"cor": "malhada"}), 422, "entrada_invalida")
    assert "cor" in erro["detalhes"][0]["mensagem"]
    assert _brincos(cliente) == []  # nada foi gravado


def test_ficha_com_varios_erros_lista_todos(cliente):
    erro = _erro(_criar(cliente, ficha={"raca_grupo": "nelore", "numero_lactacoes": 99}), 422, "entrada_invalida")
    assert [d["mensagem"].split(":")[0] for d in erro["detalhes"]] == ["corpo.ficha.raca_grupo", "corpo.ficha.numero_lactacoes"]


@pytest.mark.parametrize("literal", ["NaN", "Infinity", "-Infinity"])
def test_ficha_com_numero_nao_finito_422(cliente, literal):
    # o json do Python aceita NaN e Infinity; o cliente (httpx) não os emite, por isso o corpo vai cru
    corpo = f'{{"brinco": "BR-0001", "nome": "Mimosa", "ficha": {{"numero_lactacoes": {literal}}}}}'.encode()
    resposta = cliente.post("/api/animais", content=corpo, headers={"content-type": "application/json"})
    erro = _erro(resposta, 422, "entrada_invalida")
    assert "numero_lactacoes" in erro["detalhes"][0]["mensagem"]
    assert _brincos(cliente) == []


@pytest.mark.parametrize(
    "corpo",
    [
        rb'{"brinco": "BR-0001", "nome": "\ud800"}',
        rb'{"brinco": "BR-0001", "nome": "Mimosa", "ficha": {"\ud800": 1}}',
        rb'{"brinco": "BR-0001", "nome": "Mimosa", "ficha": {"raca_grupo": "\ud800"}}',
    ],
    ids=["nome", "chave_da_ficha", "valor_da_ficha"],
)
def test_surrogate_solto_no_json_422_nunca_500(cliente, corpo):
    # o JSON aceita "\ud800" solto; sem a checagem, o SQLite ou a resposta não o codificariam (500)
    resposta = cliente.post("/api/animais", content=corpo, headers={"content-type": "application/json"})
    assert resposta.status_code == 422, resposta.text
    assert resposta.json()["erro"]["codigo"] == "entrada_invalida"
    assert _brincos(cliente) == []


def test_campo_fora_do_schema_do_corpo_422(cliente):
    resposta = cliente.post("/api/animais", json={"brinco": "BR-0001", "nome": "Mimosa", "cf": 1})
    _erro(resposta, 422, "entrada_invalida")
    resposta = cliente.post("/api/animais", json={"brinco": "BR-0001"})  # sem nome
    _erro(resposta, 422, "entrada_invalida")


def test_brinco_so_com_espacos_422(cliente):
    _erro(cliente.post("/api/animais", json={"brinco": "   ", "nome": "Mimosa"}), 422, "entrada_invalida")


def test_corrida_do_brinco_na_criacao_409_conflito(cliente, monkeypatch):
    assert _criar(cliente).status_code == 201
    # outra requisição gravou o brinco entre a pré-checagem e o insert: a pré-checagem "não acha", o UNIQUE acha
    monkeypatch.setattr(repositorios, "obter_animal_por_brinco", lambda conn, brinco: None)
    erro = _erro(_criar(cliente), 409, "conflito")
    assert "BR-0001" in erro["mensagem"]
    monkeypatch.undo()
    assert _brincos(cliente) == ["BR-0001"]


def test_brinco_e_nome_sem_espacos_nas_pontas(cliente):
    corpo = cliente.post("/api/animais", json={"brinco": " BR-0005 ", "nome": " Estrela "}).json()
    assert (corpo["brinco"], corpo["nome"]) == ("BR-0005", "Estrela")
    _erro(cliente.post("/api/animais", json={"brinco": "BR-0005", "nome": "Outra"}), 409, "conflito")


@pytest.mark.parametrize("nome", ["", "   "])
def test_nome_em_branco_na_criacao_manual_vira_none(cliente, nome):
    corpo = cliente.post("/api/animais", json={"brinco": "BR-0070", "nome": nome}).json()
    assert corpo["nome"] is None
    validar_contrato("obter_animal", corpo)


def test_obter_e_listar_animais(cliente):
    _criar(cliente)
    cliente.post("/api/animais", json={"brinco": "BR-0002", "nome": "Estrela"})
    lista = cliente.get("/api/animais", params={"busca": "mim"}).json()
    assert lista["total"] == 1
    assert lista["itens"][0] == {
        "id": "an_001", "brinco": "BR-0001", "nome": "Mimosa", "dias_em_lactacao": 6, "ultima_sessao_id": None,
    }
    validar_contrato("listar_animais", lista)
    assert cliente.get("/api/animais").json()["total"] == 2
    assert cliente.get("/api/animais", params={"busca": "br-0002"}).json()["total"] == 1  # brinco, sem diferenciar caixa
    assert cliente.get("/api/animais", params={"busca": "zzz"}).json() == {"total": 0, "itens": []}

    animal = cliente.get("/api/animais/an_001").json()
    assert animal["nome"] == "Mimosa" and animal["dias_em_lactacao"] == 6
    validar_contrato("obter_animal", animal)
    assert cliente.get("/api/animais/an_002").json()["dias_em_lactacao"] is None  # sem data de parto

    _erro(cliente.get("/api/animais/an_999"), 404, "nao_encontrado")


def test_listar_sessoes_do_animal_vazio(cliente):
    animal = criar_animal_teste(cliente)
    resposta = cliente.get(f"/api/animais/{animal['id']}/sessoes")
    assert resposta.status_code == 200
    assert resposta.json() == {"itens": []}
    validar_contrato("listar_sessoes_animal", resposta.json())
    _erro(cliente.get("/api/animais/an_999/sessoes"), 404, "nao_encontrado")


def test_listar_sessoes_do_animal_com_sessao(cliente, config, base):
    animal = criar_animal_teste(cliente)
    # a sessão nasce como a Task 5 a grava: snapshot = {"motor": Sessao.exportar(), "origens_ficha": {...}}
    motor = Sessao(para_motor(base), "produtor", {"dias_em_lactacao": 6})
    with closing(abrir(config.db_path)) as conn, conn:
        inserir_sessao(
            conn, animal_id=animal["id"], modo="produtor", versao_base="v0001",
            snapshot={"motor": motor.exportar(), "origens_ficha": {}}, fase="triagem", agora=config.agora(),
        )
    corpo = cliente.get(f"/api/animais/{animal['id']}/sessoes").json()
    assert corpo == {
        "itens": [
            {
                "sessao_id": "ses_0001", "modo": "produtor", "versao_base": "v0001", "fase": "triagem",
                "urgencia": "sem_problema", "top1": None, "criada_em": "2026-10-20T10:00:00",
            }
        ]
    }
    validar_contrato("listar_sessoes_animal", corpo)
    assert cliente.get("/api/animais").json()["itens"][0]["ultima_sessao_id"] == "ses_0001"


def test_listar_sessoes_do_animal_duas_sessoes_mais_nova_primeiro(cliente, config, base):
    animal = criar_animal_teste(cliente)
    motor_base = para_motor(base)
    # snapshots feitos pelo próprio motor (Sessao + exportar), como a Task 5 os grava
    antiga = Sessao(motor_base, "produtor", {"dias_em_lactacao": 6})
    antiga.responder_triagem("sinais", {"sinal_a": True, "sinal_b": False})  # d1 com evidência (cf 0,6)
    nova = Sessao(motor_base, "veterinario", {"dias_em_lactacao": 6})  # sem nada marcado
    antiga_estado, nova_estado = antiga.estado(), nova.estado()
    assert antiga.parecer()["blocos"][0]["itens"][0]["situacao"] == "com_evidencia"  # premissa do teste
    assert (antiga_estado["fase"], nova_estado["fase"]) == ("dinamica", "triagem")
    with closing(abrir(config.db_path)) as conn, conn:
        for motor, estado, agora in (
            (antiga, antiga_estado, config.agora()),
            (nova, nova_estado, config.agora() + timedelta(hours=1)),
        ):
            inserir_sessao(
                conn, animal_id=animal["id"], modo=estado["modo"], versao_base="v0001",
                snapshot={"motor": motor.exportar(), "origens_ficha": {}}, fase=estado["fase"], agora=agora,
            )

    corpo = cliente.get(f"/api/animais/{animal['id']}/sessoes").json()
    validar_contrato("listar_sessoes_animal", corpo)
    assert [i["sessao_id"] for i in corpo["itens"]] == ["ses_0002", "ses_0001"]  # a mais nova primeiro
    segunda, primeira = corpo["itens"]
    assert segunda["criada_em"] > primeira["criada_em"]
    assert (primeira["modo"], primeira["fase"], primeira["versao_base"]) == ("produtor", "dinamica", "v0001")
    assert primeira["top1"] == "d1"  # a com evidência
    assert primeira["urgencia"] == antiga.parecer()["urgencia"] == "chamar_agora"
    assert (segunda["modo"], segunda["fase"]) == ("veterinario", "triagem")
    assert segunda["top1"] is None  # sem evidência não há hipótese a destacar
    assert segunda["urgencia"] == nova.parecer()["urgencia"] == "sem_problema"
    assert cliente.get("/api/animais").json()["itens"][0]["ultima_sessao_id"] == "ses_0002"


def test_sem_base_ativa_409(tmp_path, config, hoje, agora):
    vazia = Configuracao(
        base_dir=tmp_path / "sem_base", db_path=tmp_path / "outro" / "anamnese.db",
        web_dist=config.web_dist, hoje=lambda: hoje, agora=lambda: agora,
    )
    with TestClient(criar_app(vazia), raise_server_exceptions=False) as cliente:
        erro = _erro(_criar(cliente), 409, "conflito")
        assert "Nenhuma versão ativa" in erro["mensagem"]
        _erro(_enviar(cliente, b"brinco\nBR-0001\n"), 409, "conflito")
        assert cliente.get("/api/animais").json() == {"total": 0, "itens": []}  # ler não exige base


# --- importação de prontuário ----------------------------------------------------------------


@pytest.fixture
def mimosa(cliente):
    """BR-0001 já cadastrada; o prontuário só muda o histórico de mastite dela."""
    resposta = _criar(cliente, ficha={**FICHA_MIMOSA, "historico_mastite_12m": False})
    assert resposta.status_code == 201
    return resposta.json()


def test_importacao_csv_simulada_nao_grava(cliente, mimosa):
    resposta = _enviar(cliente, (FIXTURES / "prontuario.csv").read_bytes(), gravar=False)
    assert resposta.status_code == 200, resposta.text
    corpo = resposta.json()
    validar_contrato("importar_animais", corpo)
    assert corpo["formato"] == "csv"
    assert corpo["gravado"] is False
    assert corpo["criados"] == [{"linha": 2, "brinco": "BR-0007"}]
    assert corpo["atualizados"] == [{"linha": 3, "brinco": "BR-0001", "campos": ["historico_mastite_12m"]}]
    assert corpo["rejeitados"][0]["linha"] == 4
    assert corpo["rejeitados"][0]["erros"][0]["campo"] == "raca_grupo"
    assert "nelore" in corpo["rejeitados"][0]["erros"][0]["mensagem"]
    # simular não grava nada: nem o animal novo, nem a mudança no existente
    assert _brincos(cliente) == ["BR-0001"]
    animal = cliente.get(f"/api/animais/{mimosa['id']}").json()
    assert animal["ficha"]["historico_mastite_12m"] is False and animal["origens"] == {}


def test_importacao_grava_e_marca_origem(cliente, mimosa):
    resposta = _enviar(cliente, (FIXTURES / "prontuario.csv").read_bytes())  # gravar é o padrão
    assert resposta.status_code == 200, resposta.text
    corpo = resposta.json()
    assert corpo["gravado"] is True
    assert [c["brinco"] for c in corpo["criados"]] == ["BR-0007"]

    assert _brincos(cliente) == ["BR-0001", "BR-0007"]  # BR-0009 foi rejeitada
    atualizado = cliente.get(f"/api/animais/{mimosa['id']}").json()
    assert atualizado["ficha"]["historico_mastite_12m"] is True
    assert atualizado["origens"] == {"historico_mastite_12m": "importacao"}  # só o campo que mudou
    assert atualizado["ficha"]["raca_grupo"] == "cruzada"

    novo = cliente.get("/api/animais/an_002").json()
    assert (novo["brinco"], novo["nome"]) == ("BR-0007", "Estrela")
    assert novo["ficha"] == {
        "data_ultimo_parto": "2026-09-30", "raca_grupo": "europeia", "historico_mastite_12m": False, "numero_lactacoes": None,
    }
    assert novo["dias_em_lactacao"] == 20
    assert novo["origens"] == {"data_ultimo_parto": "importacao", "raca_grupo": "importacao", "historico_mastite_12m": "importacao"}
    validar_contrato("obter_animal", novo)


def test_corrida_do_brinco_na_importacao_409_e_nada_gravado(cliente, mimosa, monkeypatch):
    # a pré-checagem não vê BR-0001 (gravado "por outra requisição"): o insert falha e a transação inteira volta,
    # inclusive BR-0007, que foi inserido antes dele
    monkeypatch.setattr(repositorios, "obter_animal_por_brinco", lambda conn, brinco: None)
    erro = _erro(_enviar(cliente, (FIXTURES / "prontuario.csv").read_bytes()), 409, "conflito")
    assert "Nada foi gravado" in erro["mensagem"]
    monkeypatch.undo()
    assert _brincos(cliente) == ["BR-0001"]
    assert cliente.get(f"/api/animais/{mimosa['id']}").json()["ficha"]["historico_mastite_12m"] is False


def test_importacao_json_equivalente(cliente, mimosa):
    csv = _enviar(cliente, (FIXTURES / "prontuario.csv").read_bytes(), gravar=False).json()
    resposta = _enviar(cliente, (FIXTURES / "prontuario.json").read_bytes(), nome="prontuario.json", gravar=False)
    assert resposta.status_code == 200, resposta.text
    corpo = resposta.json()
    validar_contrato("importar_animais", corpo)
    assert corpo["formato"] == "json"
    assert corpo["gravado"] is False
    # mesmo resumo; a linha do JSON é o índice + 1 (a do CSV conta o cabeçalho)
    assert corpo["criados"] == [{"linha": 1, "brinco": "BR-0007"}]
    assert corpo["atualizados"] == [{"linha": 2, "brinco": "BR-0001", "campos": ["historico_mastite_12m"]}]
    assert corpo["rejeitados"] == [{"linha": 3, "erros": csv["rejeitados"][0]["erros"]}]
    assert _brincos(cliente) == ["BR-0001"]

    gravado = _enviar(cliente, (FIXTURES / "prontuario.json").read_bytes(), nome="PRONTUARIO.JSON").json()
    assert gravado["gravado"] is True and gravado["formato"] == "json"
    assert _brincos(cliente) == ["BR-0001", "BR-0007"]


def test_importacao_casos_de_borda(cliente):
    # BOM, separador ";", vírgula decimal e booleano em português
    texto = (
        "brinco;nome;data_ultimo_parto;raca_grupo;historico_mastite_12m;numero_lactacoes\n"
        "BR-0020;Bonita;2026-10-01;Cruzada;SIM;2\n"
        ";Sem Brinco;2026-10-01;cruzada;não;1\n"
        "BR-0020;Repetida;2026-10-02;cruzada;não;1\n"
        "BR-0021;Rosa;;;;3,0\n"
    )
    resposta = _enviar(cliente, texto.encode("utf-8-sig"))
    assert resposta.status_code == 200, resposta.text
    corpo = resposta.json()
    assert corpo["criados"] == [{"linha": 2, "brinco": "BR-0020"}, {"linha": 5, "brinco": "BR-0021"}]
    assert [(r["linha"], r["erros"][0]["campo"]) for r in corpo["rejeitados"]] == [(3, "brinco"), (4, "brinco")]
    assert "obrigatório" in corpo["rejeitados"][0]["erros"][0]["mensagem"]
    assert "linha 2" in corpo["rejeitados"][1]["erros"][0]["mensagem"]
    bonita = cliente.get("/api/animais/an_001").json()
    assert bonita["ficha"]["raca_grupo"] == "cruzada"  # "Cruzada" casa com o valor do domínio
    assert bonita["ficha"]["historico_mastite_12m"] is True
    assert bonita["ficha"]["numero_lactacoes"] == 2 and type(bonita["ficha"]["numero_lactacoes"]) is int
    rosa = cliente.get("/api/animais/an_002").json()
    assert rosa["ficha"]["numero_lactacoes"] == 3 and rosa["dias_em_lactacao"] is None  # vazio = ausente
    assert rosa["origens"] == {"numero_lactacoes": "importacao"}


def test_importacao_linha_do_csv_conta_a_do_arquivo(cliente):
    texto = 'brinco,nome\n\nBR-0030,"Maria\nda Silva"\nBR-0031,Flor\n'
    corpo = _enviar(cliente, texto.encode(), gravar=False).json()
    # linha em branco conta; o registro de duas linhas começa na 3; o seguinte está na 5
    assert corpo["criados"] == [{"linha": 3, "brinco": "BR-0030"}, {"linha": 5, "brinco": "BR-0031"}]


def test_importacao_valores_invalidos_por_linha(cliente):
    texto = (
        "brinco,nome,raca_grupo,historico_mastite_12m,numero_lactacoes,data_ultimo_parto,cor,dias_em_lactacao\n"
        "BR-0040,A,,talvez,muitas,14/10/2026,malhada,30\n"
        "BR-0041,B,,,99,,,\n"
        "BR-0042,C,,,nan,,,\n"
        "BR-0043,D,zebuina,não,1,,,\n"
    )
    corpo = _enviar(cliente, texto.encode()).json()
    assert [c["brinco"] for c in corpo["criados"]] == ["BR-0043"]
    erros = {r["linha"]: {e["campo"] for e in r["erros"]} for r in corpo["rejeitados"]}
    assert erros == {
        2: {"historico_mastite_12m", "numero_lactacoes", "data_ultimo_parto", "cor", "dias_em_lactacao"},
        3: {"numero_lactacoes"},
        4: {"numero_lactacoes"},
    }
    assert _brincos(cliente) == ["BR-0043"]  # linha com erro não grava nada, nem parcialmente


@pytest.mark.parametrize(
    "celula",
    ["9" * 5000, "-" + "9" * 5000, "9" * 5000 + ".5", "9" * 4300, "9" * 20, "9" * 15],
    ids=["inteiro_5000", "negativo_5000", "decimal_5000", "inteiro_4300", "inteiro_20", "inteiro_15"],
)
def test_importacao_numero_gigante_e_rejeitado_nunca_500(cliente, celula):
    # int() de texto com mais de 4300 dígitos levanta ValueError no Python 3.12: a linha vira rejeitada, o resto segue
    resposta = _enviar(cliente, f"brinco,numero_lactacoes\nBR-0060,{celula}\nBR-0061,2\n".encode())
    assert resposta.status_code == 200, resposta.text[:300]
    corpo = resposta.json()
    assert [(r["linha"], r["erros"][0]["campo"]) for r in corpo["rejeitados"]] == [(2, "numero_lactacoes")]
    assert corpo["criados"] == [{"linha": 3, "brinco": "BR-0061"}]
    assert _brincos(cliente) == ["BR-0061"]


def test_importacao_so_atualiza_o_que_mudou(cliente, mimosa):
    # nada novo para BR-0001: continua na lista, sem campos, e nada é gravado
    iguais = "brinco,nome,raca_grupo,historico_mastite_12m\nBR-0001,Outro Nome,cruzada,não\n"
    corpo = _enviar(cliente, iguais.encode()).json()
    assert corpo["atualizados"] == [{"linha": 2, "brinco": "BR-0001", "campos": []}]
    animal = cliente.get(f"/api/animais/{mimosa['id']}").json()
    assert animal["origens"] == {} and animal["nome"] == "Mimosa"  # o nome só vale na criação

    # célula vazia não apaga o que já existe; o campo novo e o que mudou entram
    parcial = "brinco,raca_grupo,historico_mastite_12m,numero_lactacoes\nBR-0001,,sim,4\n"
    corpo = _enviar(cliente, parcial.encode()).json()
    assert corpo["atualizados"][0]["campos"] == ["historico_mastite_12m", "numero_lactacoes"]
    animal = cliente.get(f"/api/animais/{mimosa['id']}").json()
    assert animal["ficha"] == {**FICHA_MIMOSA, "numero_lactacoes": 4}
    assert animal["origens"] == {"historico_mastite_12m": "importacao", "numero_lactacoes": "importacao"}


def test_importacao_json_com_itens_invalidos(cliente):
    dados = (
        '{"animais": [42, {"brinco": 7}, {"brinco": "BR-0050", "ficha": []}, {"brinco": "BR-0051", "raca_grupo": "cruzada"},'
        ' {"brinco": "BR-0052", "ficha": {"numero_lactacoes": NaN}}, {"brinco": "BR-0053", "nome": null, "ficha": null}]}'
    )
    corpo = _enviar(cliente, dados.encode(), nome="p.json").json()
    assert corpo["criados"] == [{"linha": 6, "brinco": "BR-0053"}]
    assert {r["linha"]: r["erros"][0]["campo"] for r in corpo["rejeitados"]} == {
        1: "animal", 2: "brinco", 3: "ficha", 4: "raca_grupo", 5: "numero_lactacoes",
    }
    assert cliente.get("/api/animais/an_001").json()["nome"] is None  # a importação aceita linha sem nome


@pytest.mark.parametrize(
    ("nome", "conteudo"),
    [
        pytest.param("prontuario.xlsx", b"PK\x03\x04\x14\x00\x06\x00", id="extensao_desconhecida"),
        pytest.param("prontuario", b"brinco\nBR-0001\n", id="sem_extensao"),
        pytest.param("prontuario.csv", b"\x89PNG\r\n\x1a\n\x00\x00\x00\rIHDR\xff\xfe", id="binario_nao_utf8"),
        pytest.param("prontuario.csv", b"brinco\x00\nBR-0001\x00\n", id="binario_que_decodifica"),
        pytest.param("prontuario.json", b"\xff\xfe{\x00}\x00", id="utf16"),
        pytest.param("prontuario.csv", b"", id="vazio"),
        pytest.param("prontuario.csv", b"\n\n", id="so_linhas_em_branco"),
        pytest.param("prontuario.csv", b"nome,raca_grupo\nMimosa,cruzada\n", id="sem_coluna_brinco"),
        pytest.param("prontuario.csv", b"brinco,nome,brinco\nBR-0001,A,BR-0002\n", id="coluna_repetida"),
        pytest.param("prontuario.json", b'{"animais": [', id="json_quebrado"),
        pytest.param("prontuario.json", b"[]", id="json_fora_do_formato"),
        pytest.param("prontuario.json", b'{"animais": {"brinco": "BR-0001"}}', id="animais_nao_e_lista"),
        pytest.param("prontuario.json", b"[" * 100000, id="json_aninhado_demais"),
    ],
)
def test_importacao_arquivo_ilegivel_422(cliente, nome, conteudo):
    _erro(_enviar(cliente, conteudo, nome=nome), 422, "importacao_invalida")
    assert _brincos(cliente) == []


def test_importacao_json_com_surrogate_solto_422(cliente):
    conteudo = rb'{"animais": [{"brinco": "BR-0001", "nome": "\ud800"}]}'
    _erro(_enviar(cliente, conteudo, nome="p.json"), 422, "importacao_invalida")
    assert _brincos(cliente) == []


def test_importacao_arquivo_grande_demais_422(cliente):
    from api.servicos.importacao import LIMITE_BYTES

    _erro(_enviar(cliente, b"brinco\n" + b"x" * LIMITE_BYTES), 422, "importacao_invalida")


def test_importacao_sem_arquivo_ou_com_parametro_invalido_422(cliente):
    _erro(cliente.post("/api/animais/importacao"), 422, "entrada_invalida")
    resposta = cliente.post("/api/animais/importacao?gravar=talvez", files={"arquivo": ("p.csv", b"brinco\nBR-0001\n")})
    _erro(resposta, 422, "entrada_invalida")
    assert _brincos(cliente) == []


def test_nome_em_branco_na_importacao_vira_none(cliente):
    _enviar(cliente, b"brinco,nome\nBR-0072,   \nBR-0073,\nBR-0074\n")
    dados = b'{"animais": [{"brinco": "BR-0075", "nome": "   "}, {"brinco": "BR-0076", "nome": ""}, {"brinco": "BR-0077"}]}'
    _enviar(cliente, dados, nome="p.json")
    itens = cliente.get("/api/animais").json()["itens"]
    assert [i["brinco"] for i in itens] == [f"BR-00{n}" for n in range(72, 78)]
    assert [i["nome"] for i in itens] == [None] * 6


def test_importacao_so_cabecalho_nao_cria_nada(cliente):
    corpo = _enviar(cliente, b"brinco,nome\n").json()
    assert corpo == {"formato": "csv", "gravado": True, "criados": [], "atualizados": [], "rejeitados": []}


def test_busca_de_animais_com_acento_ignora_a_caixa(cliente):
    """O filtro é feito em Python com ``casefold`` (o ``lower()`` do SQLite só trata ASCII)."""
    for brinco, nome in (("BR-0801", "Ângela"), ("BR-0802", "ÊNIO"), ("BR-0803", "Mimosa")):
        assert cliente.post("/api/animais", json={"brinco": brinco, "nome": nome}).status_code == 201

    def brincos(busca: str) -> list[str]:
        return [a["brinco"] for a in cliente.get("/api/animais", params={"busca": busca}).json()["itens"]]

    assert brincos("âng") == ["BR-0801"]  # minúscula acentuada acha a maiúscula acentuada
    assert brincos("ÂNG") == ["BR-0801"]
    assert brincos("ênio") == ["BR-0802"]  # e o nome todo em maiúsculas acha pela minúscula
    assert brincos("ÊNIO") == ["BR-0802"]
    assert brincos("ela") == ["BR-0801"]  # no meio do nome
