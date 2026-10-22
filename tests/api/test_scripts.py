"""Execução em localhost (Task 13): sementes fictícias, reset do banco, frontend servido pela API e script de subida."""
from __future__ import annotations

import dataclasses
import os
import shutil
import subprocess
import sys
from contextlib import closing
from datetime import timedelta
from pathlib import Path

import pytest
from fastapi.testclient import TestClient

from api.config import Configuracao
from api.db import repositorios as repo
from api.db.conexao import abrir, inicializar
from api.frontend import _arquivo_no_dist, montar_frontend
from api.main import criar_app
from api.servicos.ficha import validar_ficha
from kb.carregador import Repositorio
from scripts import resetar_db, semear_ficticios
from scripts.semear_ficticios import semear

RAIZ = Path(__file__).resolve().parents[2]
NOMES_FICTICIOS = {"Mimosa", "Estrela", "Jurema", "Boneca"}
HTML = "<!doctype html><html><body><div id='raiz'>Anamnese fictícia</div></body></html>"
JS = "console.log('app');"


def _ajustar(dados: dict) -> None:
    """Acrescenta à base mínima os campos de ficha da Seção 3.2 (``campo_ficha`` igual ao id)."""
    booleano = {"tipo": "booleano"}
    campos = {
        "numero_lactacoes": {"tipo": "numerico", "min": 0, "max": 20},
        "raca_grupo": {"tipo": "categorico", "valores": ["europeia", "zebuina", "cruzada"]},
        "retencao_placenta": booleano,
        "parto_distocico": booleano,
        "historico_mastite_12m": booleano,
        "mudanca_dieta_recente": booleano,
        "casos_podais_no_rebanho": booleano,
    }
    dados["simbolos"] += [
        {"id": campo, "tipo": "ficha", "nome": campo, "campo_ficha": campo, "dominio": dominio}
        for campo, dominio in campos.items()
    ]


def _so_raca_europeia(dados: dict) -> None:
    """Uma base cujo único campo extra de ficha só aceita ``europeia``: o resto da semente fica inválido."""
    dados["simbolos"].append(
        {
            "id": "raca_grupo", "tipo": "ficha", "nome": "Grupo racial", "campo_ficha": "raca_grupo",
            "dominio": {"tipo": "categorico", "valores": ["europeia"]},
        }
    )


@pytest.fixture
def base_dir(tmp_path, fabrica_base_dir):
    """Sobrescreve a fixture do conftest: a base ativa tem os campos de ficha de ``_ajustar``."""
    return fabrica_base_dir(tmp_path / "base", _ajustar)


@pytest.fixture
def base(base_dir):
    return Repositorio(base_dir).carregar_ativa()


@pytest.fixture
def caminho_db(tmp_path) -> Path:
    return tmp_path / "dados" / "teste.db"


@pytest.fixture
def conn(caminho_db):
    inicializar(caminho_db)
    with closing(abrir(caminho_db)) as c:
        yield c


@pytest.fixture
def ambiente(monkeypatch, caminho_db, base_dir):
    """Aponta ``ANAMNESE_DB`` e ``ANAMNESE_BASE_DIR`` para o temporário (o que o ``rodar.ps1`` faria)."""
    monkeypatch.setenv("ANAMNESE_DB", str(caminho_db))
    monkeypatch.setenv("ANAMNESE_BASE_DIR", str(base_dir))
    return caminho_db


def _animais(conn) -> list[dict]:
    return repo.listar_animais(conn, None)


def _dist(raiz: Path) -> Path:
    dist = raiz / "web" / "dist"
    (dist / "assets").mkdir(parents=True)
    (dist / "index.html").write_text(HTML, encoding="utf-8")
    (dist / "assets" / "app.js").write_text(JS, encoding="utf-8")
    return dist


# --- semente ---------------------------------------------------------------------------------------------


def test_semear_idempotente(conn, agora, base):
    assert semear(conn, agora) == 4
    assert semear(conn, agora) == 0

    mimosa = repo.obter_animal_por_brinco(conn, "BR-0001")
    assert mimosa["id"] == "an_001"
    assert mimosa["nome"] == "Mimosa"
    assert mimosa["ficha"]["data_ultimo_parto"] == (agora.date() - timedelta(days=6)).isoformat()

    animais = _animais(conn)
    assert len(animais) == 4
    assert {a["nome"] for a in animais} == NOMES_FICTICIOS  # só nomes fictícios
    assert len({str(a["ficha"]) for a in animais}) == 4  # fichas diferentes
    for animal in animais:
        assert validar_ficha(base, animal["ficha"]) == [], animal["brinco"]


def test_semear_inclui_vaca_com_parto_recente(conn, agora):
    """O roteiro da demonstração (6.2.2) usa uma vaca com parto há 1 dia."""
    semear(conn, agora)
    partos = {a["ficha"]["data_ultimo_parto"] for a in _animais(conn)}
    assert (agora.date() - timedelta(days=1)).isoformat() in partos


def test_semear_com_base_pula_campo_invalido(tmp_path, fabrica_base_dir, conn, agora):
    """Com a base à mão, o campo que ela não aceita é pulado (ficha completa só com o que vale); nada quebra."""
    restrita = Repositorio(fabrica_base_dir(tmp_path / "base_restrita", _so_raca_europeia)).carregar_ativa()

    assert semear(conn, agora, restrita) == 4

    por_brinco = {a["brinco"]: a["ficha"] for a in _animais(conn)}
    assert list(por_brinco["BR-0001"]) == ["data_ultimo_parto", "raca_grupo"]  # completa: só os campos da base
    assert por_brinco["BR-0001"]["raca_grupo"] is None  # Mimosa é cruzada: o valor não cabe na base, pulado
    assert por_brinco["BR-0002"]["raca_grupo"] == "europeia"  # o que cabe fica
    for ficha in por_brinco.values():
        assert validar_ficha(restrita, ficha) == []


def test_main_da_semente_sem_base_ativa_nao_quebra(monkeypatch, tmp_path, caminho_db, capsys):
    monkeypatch.setenv("ANAMNESE_DB", str(caminho_db))
    monkeypatch.setenv("ANAMNESE_BASE_DIR", str(tmp_path / "vazia"))

    semear_ficticios.main()

    with closing(abrir(caminho_db)) as conn:
        assert len(_animais(conn)) == 4
    assert "Animais fictícios criados: 4" in capsys.readouterr().out


# --- reset do banco --------------------------------------------------------------------------------------


def test_resetar_apaga_e_recria(conn, caminho_db, agora):
    with conn:
        repo.inserir_animal(conn, brinco="BR-9999", nome="Fictícia", ficha={}, origens={}, agora=agora)
    assert len(_animais(conn)) == 1
    conn.close()

    resetar_db.resetar(caminho_db)

    with closing(abrir(caminho_db)) as novo:
        assert novo.execute("SELECT COUNT(*) FROM animais").fetchone()[0] == 0
        tabelas = {r[0] for r in novo.execute("SELECT name FROM sqlite_master WHERE type = 'table'")}
    assert {"animais", "sessoes", "respostas", "versoes_base"} <= tabelas


def test_resetar_recusa_arquivo_que_nao_e_sqlite(tmp_path):
    alvo = tmp_path / "importante.json"
    alvo.write_text('{"nao": "apague"}', encoding="utf-8")
    lateral = tmp_path / "importante.json-wal"  # nome parecido com o auxiliar do SQLite: também fica
    lateral.write_text("lateral", encoding="utf-8")

    with pytest.raises(resetar_db.RecusaDeReset, match="não é um banco SQLite; recuso apagar"):
        resetar_db.resetar(alvo)

    assert alvo.read_text(encoding="utf-8") == '{"nao": "apague"}'
    assert lateral.read_text(encoding="utf-8") == "lateral"


def test_resetar_recusa_pasta(tmp_path):
    pasta = tmp_path / "anamnese.db"
    pasta.mkdir()
    (pasta / "dentro.txt").write_text("fica", encoding="utf-8")

    with pytest.raises(resetar_db.RecusaDeReset, match="pasta"):
        resetar_db.resetar(pasta)

    assert (pasta / "dentro.txt").read_text(encoding="utf-8") == "fica"


def test_resetar_aceita_arquivo_vazio_e_apaga_os_auxiliares_do_sqlite(conn, caminho_db):
    conn.close()
    auxiliar = Path(f"{caminho_db}-journal")
    auxiliar.write_bytes(b"resto de uma sessao anterior")

    resetar_db.resetar(caminho_db)

    assert not auxiliar.exists()
    vazio = caminho_db.with_name("vazio.db")
    vazio.write_bytes(b"")  # arquivo vazio (um .db recém-criado e ainda sem tabelas) pode ser recriado
    resetar_db.resetar(vazio)
    with closing(abrir(vazio)) as novo:
        assert novo.execute("SELECT COUNT(*) FROM animais").fetchone()[0] == 0


def test_main_do_reset_recusa_com_mensagem_e_saida_diferente_de_zero(monkeypatch, tmp_path):
    alvo = tmp_path / "config.json"
    alvo.write_text("{}", encoding="utf-8")
    monkeypatch.setenv("ANAMNESE_DB", str(alvo))

    with pytest.raises(SystemExit) as saida:
        resetar_db.main([])

    assert isinstance(saida.value.code, str) and "não é um banco SQLite; recuso apagar" in saida.value.code
    assert alvo.read_text(encoding="utf-8") == "{}"


def test_resetar_cria_banco_que_nao_existe(tmp_path):
    caminho = tmp_path / "pasta" / "nova" / "anamnese.db"
    resetar_db.resetar(caminho)
    assert caminho.is_file()


def test_main_do_reset_com_semear(ambiente, base):
    resetar_db.main(["--semear"])

    with closing(abrir(ambiente)) as conn:
        animais = _animais(conn)
        assert len(animais) == 4
        assert all(validar_ficha(base, a["ficha"]) == [] for a in animais)

    resetar_db.main([])  # sem --semear: banco vazio de novo
    with closing(abrir(ambiente)) as conn:
        assert _animais(conn) == []


# --- frontend servido pela API -----------------------------------------------------------------------------


def test_frontend_serve_index_e_coringa(config, tmp_path):
    dist = _dist(tmp_path)
    app = criar_app(dataclasses.replace(config, web_dist=dist))

    with TestClient(app, raise_server_exceptions=False) as cliente:
        raiz = cliente.get("/")
        assert raiz.status_code == 200
        assert raiz.headers["content-type"].startswith("text/html")
        assert raiz.text == HTML

        rota_do_react = cliente.get("/animais/an_001")  # recarregar a página numa rota do React
        assert rota_do_react.status_code == 200
        assert rota_do_react.text == HTML

        asset = cliente.get("/assets/app.js")
        assert asset.status_code == 200
        assert asset.text == JS

        ausente = cliente.get("/assets/nao_existe.js")  # arquivo que não existe não vira HTML
        assert ausente.status_code == 404
        assert ausente.json()["erro"]["codigo"] == "nao_encontrado"

        inexistente = cliente.get("/api/inexistente")  # a API nunca devolve o HTML
        assert inexistente.status_code == 404
        assert inexistente.headers["content-type"].startswith("application/json")
        assert inexistente.json()["erro"]["codigo"] == "nao_encontrado"
        assert "erro" in cliente.get("/api").json()

        assert cliente.get("/api/saude").json() == {"status": "ok", "versao_api": "0.1.0"}
        assert cliente.get("/api/docs").status_code == 200


def test_frontend_nao_entra_no_openapi(config, tmp_path):
    com = criar_app(dataclasses.replace(config, web_dist=_dist(tmp_path))).openapi()
    sem = criar_app(config).openapi()
    assert com == sem
    assert not [rota for rota in com["paths"] if not rota.startswith("/api")]


def test_frontend_serve_arquivo_da_raiz_do_dist(config, tmp_path):
    dist = _dist(tmp_path)
    (dist / "favicon.svg").write_text("<svg/>", encoding="utf-8")
    app = criar_app(dataclasses.replace(config, web_dist=dist))

    with TestClient(app, raise_server_exceptions=False) as cliente:
        assert cliente.get("/favicon.svg").text == "<svg/>"
        assert cliente.get("/qualquer/coisa").text == HTML


def test_arquivo_no_dist_nao_sai_da_pasta(tmp_path):
    dist = _dist(tmp_path)
    (tmp_path / "web" / "segredo.txt").write_text("SEGREDO", encoding="utf-8")

    assert _arquivo_no_dist(dist, "assets/app.js") == (dist / "assets" / "app.js").resolve()
    assert _arquivo_no_dist(dist, "") is None  # a própria pasta não é arquivo
    assert _arquivo_no_dist(dist, "nao_existe.txt") is None
    assert _arquivo_no_dist(dist, "../segredo.txt") is None
    assert _arquivo_no_dist(dist, "assets/../../segredo.txt") is None
    assert _arquivo_no_dist(dist, str(tmp_path / "web" / "segredo.txt")) is None  # caminho absoluto
    assert _arquivo_no_dist(dist, "a\x00b") is None  # byte nulo não derruba (nem vira 500)


CAMINHOS_QUE_NAO_TOCAM_O_DISCO = (
    "\\\\host\\share\\x",  # UNC: o Windows tentaria abrir \\host\share
    "C:/Windows/win.ini",
    "C:\\Windows\\win.ini",
    "/etc/passwd",
    "../segredo.txt",
    "assets/../../segredo.txt",
    "a\x00b",
)


def _proibir_disco(monkeypatch):
    def proibido(*_args, **_kwargs):
        raise AssertionError("tocou o disco antes de rejeitar o caminho")

    monkeypatch.setattr(Path, "resolve", proibido)
    monkeypatch.setattr(Path, "is_file", proibido)


def test_arquivo_no_dist_rejeita_antes_de_tocar_o_disco(tmp_path, monkeypatch):
    dist = _dist(tmp_path)
    with monkeypatch.context() as m:
        _proibir_disco(m)
        for caminho in CAMINHOS_QUE_NAO_TOCAM_O_DISCO:
            assert _arquivo_no_dist(dist, caminho) is None, caminho


def test_get_com_caminho_de_rede_ou_unidade_cai_no_index_sem_tocar_o_disco(config, tmp_path, monkeypatch):
    app = criar_app(dataclasses.replace(config, web_dist=_dist(tmp_path)))
    with TestClient(app, raise_server_exceptions=False) as cliente:
        with monkeypatch.context() as m:
            _proibir_disco(m)
            unc = cliente.get("/%5C%5Chost%5Cshare%5Cx")
            unidade = cliente.get("/C:/Windows/win.ini")
        assert (unc.status_code, unc.text) == (200, HTML)
        assert (unidade.status_code, unidade.text) == (200, HTML)


def test_barras_a_mais_nao_escapam_do_prefixo_api(config, tmp_path):
    app = criar_app(dataclasses.replace(config, web_dist=_dist(tmp_path)))
    with TestClient(app, raise_server_exceptions=False) as cliente:
        for caminho in ("//api/x", "///api/x", "//api"):
            resposta = cliente.get("http://testserver" + caminho)  # URL inteira: "//api/x" sozinho seria um host
            assert resposta.status_code == 404, caminho
            assert resposta.headers["content-type"].startswith("application/json"), caminho
            assert resposta.json()["erro"]["codigo"] == "nao_encontrado", caminho
        com_barra = cliente.get("/api/x/")  # barra final sob /api: também o 404 JSON
        assert com_barra.status_code == 404
        assert com_barra.json()["erro"]["codigo"] == "nao_encontrado"


def test_sem_dist_nao_monta_frontend(config, tmp_path):
    app = criar_app(config)  # `config.web_dist` aponta para uma pasta que não existe
    assert montar_frontend(app, tmp_path / "nao_existe") is False

    dist_sem_index = tmp_path / "vazio"
    (dist_sem_index / "assets").mkdir(parents=True)
    assert montar_frontend(app, dist_sem_index) is False

    with TestClient(app, raise_server_exceptions=False) as cliente:
        resposta = cliente.get("/")
        assert resposta.status_code == 404
        assert resposta.json()["erro"]["codigo"] == "nao_encontrado"
        assert cliente.get("/assets/app.js").status_code == 404


# --- sobe sem a base -------------------------------------------------------------------------------------


def test_app_sobe_sem_base_ativa(tmp_path, agora, hoje):
    """A base real pode não existir ainda: a API sobe e responde 409 (nunca 500) onde precisa dela."""
    config = Configuracao(
        base_dir=tmp_path / "base_vazia",
        db_path=tmp_path / "dados" / "anamnese.db",
        web_dist=tmp_path / "web" / "dist",
        hoje=lambda: hoje,
        agora=lambda: agora,
    )
    with TestClient(criar_app(config), raise_server_exceptions=False) as cliente:
        assert cliente.get("/api/saude").status_code == 200

        with closing(abrir(config.db_path)) as conn:  # o lifespan já criou o esquema
            semear(conn, agora)

        resposta = cliente.post("/api/sessoes", json={"animal_id": "an_001", "modo": "produtor"})
        assert resposta.status_code == 409, resposta.text
        erro = resposta.json()["erro"]
        assert erro["codigo"] == "conflito"
        assert "Nenhuma versão ativa" in erro["mensagem"]

        assert cliente.get("/api/base/versoes").status_code == 200  # a listagem também não quebra
        assert cliente.get("/api/animais").status_code == 200


# --- script de subida ------------------------------------------------------------------------------------


@pytest.mark.lento
@pytest.mark.skipif(sys.platform != "win32" or shutil.which("powershell") is None, reason="só no Windows PowerShell")
def test_rodar_ps1_e_valido_no_powershell_5():
    """O parser do Windows PowerShell aceita o roteiro (sem ``&&`` nem ``?:``) e ele expõe só as duas chaves."""
    comando = (
        "$e = $null; $t = $null; "
        "$a = [System.Management.Automation.Language.Parser]::ParseFile($env:ROTEIRO, [ref]$t, [ref]$e); "
        "'ERROS=' + $e.Count; "
        "'PARAMETROS=' + (($a.ParamBlock.Parameters | ForEach-Object { $_.Name.VariablePath.UserPath }) -join ',')"
    )
    ambiente = {**os.environ, "ROTEIRO": str(RAIZ / "scripts" / "rodar.ps1")}
    saida = subprocess.run(
        ["powershell", "-NoProfile", "-NonInteractive", "-Command", comando],
        capture_output=True, text=True, env=ambiente, timeout=60, check=True,
    ).stdout.splitlines()
    assert "ERROS=0" in saida
    assert "PARAMETROS=SoPreparar,Reset,SemNavegador" in saida


def _bash() -> str | None:
    caminho = shutil.which("bash")
    if caminho is None or "system32" in caminho.lower():  # bash.exe de System32 é o lançador do WSL, não um bash
        return None
    return caminho


@pytest.mark.lento
@pytest.mark.skipif(_bash() is None, reason="sem bash")
def test_rodar_sh_tem_sintaxe_valida():
    resultado = subprocess.run(
        [_bash(), "-n", (RAIZ / "scripts" / "rodar.sh").as_posix()], capture_output=True, text=True, timeout=60
    )
    assert resultado.returncode == 0, resultado.stderr


# --- aviso do OneDrive -----------------------------------------------------------------------------------


def _preparar(comando: list[str], banco: Path, base_dir: Path) -> subprocess.CompletedProcess:
    ambiente = {**os.environ, "ANAMNESE_DB": str(banco), "ANAMNESE_BASE_DIR": str(base_dir), "PYTHONIOENCODING": "utf-8"}
    return subprocess.run(comando, capture_output=True, text=True, encoding="utf-8", errors="replace", env=ambiente, timeout=120, cwd=RAIZ)


def _roteiros_de_preparo(tmp_path: Path, base_dir: Path):
    """``(comando, aviso)`` de cada roteiro disponível neste computador, rodando só o preparo do banco."""
    roteiros = []
    if sys.platform == "win32" and shutil.which("powershell") is not None:
        roteiros.append(
            ["powershell", "-NoProfile", "-NonInteractive", "-ExecutionPolicy", "Bypass", "-File",
             str(RAIZ / "scripts" / "rodar.ps1"), "-SoPreparar"]
        )
    if _bash() is not None:
        roteiros.append([_bash(), (RAIZ / "scripts" / "rodar.sh").as_posix(), "--so-preparar"])
    return roteiros


@pytest.mark.lento
def test_roteiros_avisam_quando_o_banco_esta_no_onedrive(tmp_path, base_dir):
    roteiros = _roteiros_de_preparo(tmp_path, base_dir)
    if not roteiros:
        pytest.skip("sem PowerShell nem bash")
    for i, comando in enumerate(roteiros):
        no_onedrive = tmp_path / f"r{i}" / "OneDrive" / "Desktop" / "anamnese.db"
        resultado = _preparar(comando, no_onedrive, base_dir)
        assert resultado.returncode == 0, resultado.stdout + resultado.stderr
        avisos = [l for l in resultado.stdout.splitlines() if l.startswith("Aviso") and "OneDrive" in l]
        assert avisos, resultado.stdout  # a linha de "Criando o banco ..." também traz o caminho; o que conta é o aviso
        assert "ANAMNESE_DB" in avisos[0]  # diz o que fazer
        fora = tmp_path / f"f{i}" / "dados" / "anamnese.db"
        resultado = _preparar(comando, fora, base_dir)
        assert resultado.returncode == 0, resultado.stdout + resultado.stderr
        assert "OneDrive" not in resultado.stdout, resultado.stdout
