"""Resposta numérica digitada: a API repassa número JSON ou texto e o motor decide; nada é gravado se recusar."""
import json
import shutil
from contextlib import closing
from datetime import date, datetime
from pathlib import Path

import pytest
from fastapi.testclient import TestClient

from api.config import Configuracao
from api.db.conexao import abrir
from api.main import criar_app
from tests.api.apoio import criar_animal_teste, criar_sessao_teste

RAIZ = Path(__file__).resolve().parents[2]

MALICIOSOS = [
    "12.5", "-3", "+3", " 12", "12 ", "1e3", "1_000", "3/2", "0x10", "١٢", "12abc",
    "12; DROP TABLE sessoes", "' OR 1=1 --", "<script>", "", "1001", "12,5",
]


def _codigo(valor):
    return "entrada_invalida" if isinstance(valor, str) and len(valor) > 16 else "resposta_invalida"


def _erro(resposta, status, codigo):
    assert resposta.status_code == status, resposta.text
    assert resposta.json()["erro"]["codigo"] == codigo


def _estado_gravado(config):
    with closing(abrir(config.db_path)) as conn:
        return [tuple(l) for l in conn.execute("SELECT revisao, snapshot_json FROM sessoes")]


def _cliente(tmp_path, base_dir):
    config = Configuracao(
        base_dir=base_dir, db_path=tmp_path / "dados" / "anamnese.db", web_dist=tmp_path / "web",
        hoje=lambda: date(2026, 10, 20), agora=lambda: datetime(2026, 10, 20, 10, 0),
    )
    return config, TestClient(criar_app(config), raise_server_exceptions=False)


@pytest.fixture
def real(tmp_path):
    """A base real copiada (versão ativa) e uma sessão cuja primeira tela é ``dias_em_lactacao``."""
    destino = tmp_path / "base_real"
    shutil.copytree(RAIZ / "base" / "versoes", destino / "versoes")
    shutil.copyfile(RAIZ / "base" / "ativa.json", destino / "ativa.json")
    config, cliente = _cliente(tmp_path, destino)
    with cliente:
        resposta = cliente.post("/api/animais", json={"brinco": "BR-0009", "nome": "Teste", "ficha": {}})
        assert resposta.status_code == 201, resposta.text
        sessao = criar_sessao_teste(cliente, resposta.json()["id"])
        assert sessao["versao_base"] == json.loads((RAIZ / "base" / "ativa.json").read_text(encoding="utf-8"))["versao"]
        assert sessao["proxima"]["tela_id"] == "dias_em_lactacao"
        yield config, cliente


@pytest.mark.parametrize("valor", MALICIOSOS)
def test_triagem_recusa_valor_malicioso_sem_gravar(real, valor):
    config, cliente = real
    antes = _estado_gravado(config)
    resposta = cliente.post("/api/sessoes/ses_0001/triagem/dias_em_lactacao", json={"valores": {"dias_em_lactacao": valor}})
    _erro(resposta, 422, _codigo(valor))
    assert valor not in resposta.text or valor == ""
    assert _estado_gravado(config) == antes


def test_triagem_recusa_texto_longo_e_mapa_grande(real):
    config, cliente = real
    antes = _estado_gravado(config)
    _erro(cliente.post("/api/sessoes/ses_0001/triagem/dias_em_lactacao", json={"valores": {"dias_em_lactacao": "1" * 17}}), 422, "entrada_invalida")
    grande = {f"s{i}": True for i in range(21)}
    _erro(cliente.post("/api/sessoes/ses_0001/triagem/dias_em_lactacao", json={"valores": grande}), 422, "entrada_invalida")
    assert _estado_gravado(config) == antes


@pytest.mark.parametrize("valor", ["12", 12, 12.0])
def test_triagem_aceita_numero_ou_texto(real, valor):
    config, cliente = real
    resposta = cliente.post("/api/sessoes/ses_0001/triagem/dias_em_lactacao", json={"valores": {"dias_em_lactacao": valor}})
    assert resposta.status_code == 200, resposta.text


def test_triagem_recusa_infinito_e_booleano(real):
    config, cliente = real
    antes = _estado_gravado(config)
    for bruto in ("true", "1e999", "Infinity", "NaN"):
        resposta = cliente.post(
            "/api/sessoes/ses_0001/triagem/dias_em_lactacao",
            content='{"valores": {"dias_em_lactacao": %s}}' % bruto, headers={"Content-Type": "application/json"},
        )
        assert resposta.status_code == 422, (bruto, resposta.text)
    assert _estado_gravado(config) == antes


# --- POST /respostas: pergunta dinâmica numérica ---------------------------------------------


def _numerica(dados):
    for s in dados["simbolos"]:
        if s["id"] == "pergunta_x":
            s["dominio"] = {"tipo": "numerico", "min": 0, "max": 1000, "casas_decimais": 0}
    for r in dados["regras"]:
        for c in r["se"]:
            if c["simbolo"] == "pergunta_x":
                c.update(op="≥", valor=1)


@pytest.fixture
def dinamica(cliente_com):
    config, cliente = cliente_com(_numerica)
    animal = criar_animal_teste(cliente)
    criar_sessao_teste(cliente, animal["id"])
    resposta = cliente.post("/api/sessoes/ses_0001/triagem/sinais", json={"valores": {"sinal_a": True, "sinal_b": False}})
    assert resposta.status_code == 200, resposta.text
    assert resposta.json()["proxima"]["simbolo"] == "pergunta_x"
    return config, cliente


@pytest.mark.parametrize("valor", MALICIOSOS)
def test_respostas_recusa_valor_malicioso_sem_gravar(dinamica, valor):
    config, cliente = dinamica
    antes = _estado_gravado(config)
    resposta = cliente.post("/api/sessoes/ses_0001/respostas", json={"simbolo": "pergunta_x", "valor": valor})
    _erro(resposta, 422, _codigo(valor))
    assert _estado_gravado(config) == antes


def test_respostas_texto_longo_e_entrada_invalida(dinamica):
    config, cliente = dinamica
    antes = _estado_gravado(config)
    _erro(cliente.post("/api/sessoes/ses_0001/respostas", json={"simbolo": "pergunta_x", "valor": "1" * 17}), 422, "entrada_invalida")
    _erro(cliente.put("/api/sessoes/ses_0001/respostas/pergunta_x", json={"valor": "1" * 17}), 422, "entrada_invalida")
    assert _estado_gravado(config) == antes


@pytest.mark.parametrize("valor", ["12", 12])
def test_respostas_aceita_numero_ou_texto(dinamica, valor):
    config, cliente = dinamica
    resposta = cliente.post("/api/sessoes/ses_0001/respostas", json={"simbolo": "pergunta_x", "valor": valor})
    assert resposta.status_code == 200, resposta.text
