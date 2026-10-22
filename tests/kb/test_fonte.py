"""Base separada por doença (``base/fonte/``) e junção exata de volta."""
import json
from pathlib import Path

import pytest

from kb import carregar_base, validar
from kb.carregador import _json
from kb.fonte import FonteInvalida, gravar_fonte, ler_fonte

RAIZ = Path(__file__).resolve().parents[2]
ARQUIVO_V0002 = RAIZ / "base/versoes/v0002.json"


@pytest.fixture
def v0002():
    return carregar_base(ARQUIVO_V0002)


@pytest.fixture
def fonte(tmp_path, v0002):
    gravar_fonte(v0002, tmp_path)
    return tmp_path


def _ler(caminho):
    return json.loads(caminho.read_text(encoding="utf-8"))


def _gravar(caminho, dados):
    caminho.write_text(json.dumps(dados, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def test_ida_e_volta_identica(fonte, v0002):
    juntada = ler_fonte(fonte)
    assert juntada == v0002
    assert _json(juntada.model_dump(mode="json", exclude_none=True)) == ARQUIVO_V0002.read_text(encoding="utf-8")


def test_oito_doencas_com_suas_regras(fonte, v0002):
    arquivos = sorted((fonte / "doencas").glob("*.json"))
    doencas = sorted(s.id for s in v0002.simbolos if s.tipo == "doenca")
    assert [a.stem for a in arquivos] == doencas
    for arquivo in arquivos:
        dados = _ler(arquivo)
        d = arquivo.stem
        assert dados["doenca"] == d
        assert any(s["id"] == d and s["tipo"] == "doenca" for s in dados["simbolos"])
        ids = {r["id"] for r in dados["regras"]}
        assert {r.id for r in v0002.regras if r.entao.simbolo == d} <= ids
        assert any(r.classe == "urgencia" and any(c.simbolo == d for c in r.se) and r.id in ids for r in v0002.regras)


def test_ids_unicos_entre_arquivos(fonte):
    vistos: dict[str, str] = {}
    for arquivo in [fonte / "comum.json", *sorted((fonte / "doencas").glob("*.json"))]:
        dados = _ler(arquivo)
        for item in dados["simbolos"] + dados["regras"]:
            assert item["id"] not in vistos, (item["id"], vistos.get(item["id"]), arquivo.name)
            vistos[item["id"]] = arquivo.name


def test_id_duplicado_entre_arquivos(fonte):
    mastite, cetose = fonte / "doencas/mastite.json", fonte / "doencas/cetose.json"
    regra = _ler(mastite)["regras"][0]
    dados = _ler(cetose)
    dados["regras"].append(regra)
    _gravar(cetose, dados)
    with pytest.raises(FonteInvalida) as erro:
        ler_fonte(fonte)
    texto = str(erro.value)
    assert regra["id"] in texto and "mastite.json" in texto and "cetose.json" in texto


def test_doenca_sem_simbolo(fonte):
    arquivo = fonte / "doencas/mastite.json"
    dados = _ler(arquivo)
    dados["simbolos"] = [s for s in dados["simbolos"] if s["id"] != "mastite"]
    _gravar(arquivo, dados)
    with pytest.raises(FonteInvalida, match="mastite"):
        ler_fonte(fonte)


def test_json_invalido(fonte):
    (fonte / "doencas/tpb.json").write_text("{", encoding="utf-8")
    with pytest.raises(FonteInvalida, match="tpb.json"):
        ler_fonte(fonte)


def test_regra_nova_entra_e_valida(fonte, v0002):
    arquivo = fonte / "doencas/mastite.json"
    dados = _ler(arquivo)
    dados["regras"].append({
        "id": "R-MAS-99", "se": [{"simbolo": "febre", "op": "=", "valor": True, "negado": False}],
        "entao": {"simbolo": "mastite", "cf": 0.2}, "classe": "evidencia", "prioridade": 10,
        "fonte": "teste", "status": "suposicao_a_validar",
    })
    _gravar(arquivo, dados)
    juntada = ler_fonte(fonte)
    ids = [r.id for r in juntada.regras]
    assert ids[-1] == "R-MAS-99" and len(ids) == len(v0002.regras) + 1
    assert validar(juntada).valida
    (fonte / "indice.json").unlink()
    sem_indice = ler_fonte(fonte)
    assert {r.id for r in sem_indice.regras} == set(ids) and validar(sem_indice).valida
