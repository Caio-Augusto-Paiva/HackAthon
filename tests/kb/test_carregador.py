"""Testes do repositório de versões imutáveis da base (kb.carregador)."""
import json
from datetime import date

import pytest

from kb.carregador import BaseInvalida, Repositorio
from kb.modelos import carregar_base
from tests.kb.apoio import carregar_minima


def _repo(tmp_path):
    return Repositorio(tmp_path, hoje=lambda: date(2026, 10, 21))


def _base():
    return carregar_base(carregar_minima())


def test_salvar_cria_v0001_e_v0002_com_pai(tmp_path):
    repo = _repo(tmp_path)
    assert repo.listar_versoes() == []
    assert repo.versao_ativa() is None

    primeira = repo.salvar_nova(_base(), autor="ana", nota="primeira")
    assert primeira == "v0001"
    assert repo.carregar("v0001").meta.pai is None

    repo.ativar("v0001")
    segunda = repo.salvar_nova(_base(), autor="bia", nota="segunda")
    assert segunda == "v0002"
    assert repo.listar_versoes() == ["v0001", "v0002"]

    meta = repo.carregar("v0002").meta
    assert (meta.versao, meta.pai, meta.autor, meta.nota, meta.data) == (
        "v0002", "v0001", "bia", "segunda", "2026-10-21",
    )
    # salvar não ativa
    assert repo.versao_ativa() == "v0001"


def test_pai_explicito_e_proximo_numero_ignora_arquivos_estranhos(tmp_path):
    repo = _repo(tmp_path)
    repo.salvar_nova(_base(), autor="a", nota="n")
    (tmp_path / "versoes" / "rascunho.json").write_text("{}", encoding="utf-8")
    (tmp_path / "versoes" / "v7.json").write_text("{}", encoding="utf-8")
    (tmp_path / "versoes" / "v0005.json").write_text("{}", encoding="utf-8")
    assert repo.listar_versoes() == ["v0001", "v0005"]
    nova = repo.salvar_nova(_base(), autor="a", nota="n", pai="v0001")
    assert nova == "v0006"
    assert repo.carregar("v0006").meta.pai == "v0001"


def test_salvar_nao_altera_a_base_do_chamador(tmp_path):
    base = _base()
    antes = base.model_dump()
    _repo(tmp_path).salvar_nova(base, autor="ana", nota="x")
    assert base.model_dump() == antes


def test_nunca_sobrescreve(tmp_path):
    repo = _repo(tmp_path)
    repo.salvar_nova(_base(), autor="a", nota="n")
    # o próximo número seria v0002; criado à mão logo antes da gravação
    manual = tmp_path / "versoes" / "v0002.json"

    class Corrida(Repositorio):
        def _proxima(self):
            manual.write_text("conteudo manual", encoding="utf-8")
            return "v0002"

    with pytest.raises(FileExistsError):
        Corrida(tmp_path).salvar_nova(_base(), autor="a", nota="n")
    assert manual.read_text(encoding="utf-8") == "conteudo manual"


def test_base_invalida_nao_grava(tmp_path):
    dados = carregar_minima()
    dados["regras"][0]["entao"]["simbolo"] = "inexistente"
    repo = _repo(tmp_path)
    with pytest.raises(BaseInvalida) as exc:
        repo.salvar_nova(carregar_base(dados), autor="a", nota="n")
    assert not exc.value.relatorio.valida
    assert exc.value.relatorio.erros
    assert repo.listar_versoes() == []
    assert list(tmp_path.rglob("*.json")) == []


def test_ativar_e_carregar_ativa(tmp_path):
    repo = _repo(tmp_path)
    repo.salvar_nova(_base(), autor="a", nota="n")
    repo.salvar_nova(_base(), autor="a", nota="n")
    repo.ativar("v0001")
    assert repo.versao_ativa() == "v0001"
    repo.ativar("v0002")
    assert repo.versao_ativa() == "v0002"
    assert repo.carregar_ativa().meta.versao == "v0002"
    assert json.loads((tmp_path / "ativa.json").read_text(encoding="utf-8")) == {"versao": "v0002"}


def test_ativar_versao_inexistente_erro(tmp_path):
    repo = _repo(tmp_path)
    with pytest.raises(FileNotFoundError, match="v0009"):
        repo.ativar("v0009")
    assert repo.versao_ativa() is None


def test_ativa_inexistente_erro_claro(tmp_path):
    (tmp_path / "ativa.json").write_text('{"versao": "v0003"}', encoding="utf-8")
    repo = _repo(tmp_path)
    assert repo.versao_ativa() == "v0003"
    with pytest.raises(FileNotFoundError, match="v0003"):
        repo.carregar_ativa()
    with pytest.raises(FileNotFoundError, match="v0003"):
        repo.carregar("v0003")


def test_carregar_ativa_sem_ativa_erro(tmp_path):
    with pytest.raises(FileNotFoundError, match="ativa"):
        _repo(tmp_path).carregar_ativa()


def test_hash_estavel(tmp_path):
    repo = _repo(tmp_path)
    versao = repo.salvar_nova(_base(), autor="a", nota="n")
    h = repo.hash(versao)
    assert h.startswith("sha256:") and len(h) == len("sha256:") + 64
    assert repo.hash(versao) == h
    arquivo = tmp_path / "versoes" / f"{versao}.json"
    arquivo.write_text(arquivo.read_text(encoding="utf-8") + " ", encoding="utf-8")
    assert repo.hash(versao) != h


def test_hash_versao_inexistente(tmp_path):
    with pytest.raises(FileNotFoundError, match="v0001"):
        _repo(tmp_path).hash("v0001")


def test_json_utf8_indentado(tmp_path):
    dados = carregar_minima()
    dados["simbolos"][0]["nome"] = "Temperatura ≤ 39"
    repo = _repo(tmp_path)
    versao = repo.salvar_nova(carregar_base(dados), autor="a", nota="n")
    texto = (tmp_path / "versoes" / f"{versao}.json").read_bytes().decode("utf-8")
    assert "≤" in texto and "\\u" not in texto
    assert texto.endswith("\n") and not texto.endswith("\n\n")
    assert '\n  "meta": {' in texto
    assert "\r" not in texto


def test_casos_ausentes_lista_vazia(tmp_path):
    assert _repo(tmp_path).carregar_casos() == []


def test_carregar_casos(tmp_path):
    (tmp_path / "casos").mkdir()
    caso = {
        "id": "c1", "descricao": "d", "modo": "produtor",
        "esperado": {"urgencia": "observar"},
    }
    (tmp_path / "casos" / "casos.json").write_text(json.dumps([caso]), encoding="utf-8")
    casos = _repo(tmp_path).carregar_casos()
    assert [c.id for c in casos] == ["c1"]
    assert casos[0].esperado.urgencia == "observar"
