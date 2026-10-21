"""Integração do kb com o motor e com os JSON Schemas versionados."""
import importlib.util
import json

from engine.inferencia import inferir
from engine.modelos import Base as BaseMotor
from kb.modelos import carregar_base, para_motor
from tests.kb.apoio import CAMINHO_BASE_MOTOR, RAIZ, carregar_minima

SCHEMAS = ("base.schema.json", "caso.schema.json")


def _dump_kb(dados: dict) -> dict:
    return para_motor(carregar_base(dados))


def test_motor_aceita_dump_do_kb():
    BaseMotor.de_dict(_dump_kb(carregar_minima()))


def test_motor_mesmo_resultado_com_e_sem_kb():
    crua = json.loads(CAMINHO_BASE_MOTOR.read_text(encoding="utf-8"))
    fatos = {"sinal1": True, "dias": 120}

    direto = inferir(crua, fatos)
    via_kb = inferir(_dump_kb(crua), fatos)

    assert direto.cfs == via_kb.cfs
    assert direto.urgencia == via_kb.urgencia
    assert [r["id"] for r in direto.disparadas] == [r["id"] for r in via_kb.disparadas]
    assert direto.disparadas, "o cenário deve disparar ao menos uma regra"


def _carregar_script():
    caminho = RAIZ / "scripts" / "exportar_schema.py"
    spec = importlib.util.spec_from_file_location("exportar_schema", caminho)
    modulo = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(modulo)
    return modulo


def test_schema_sincronizado(tmp_path):
    _carregar_script().main(tmp_path)
    for nome in SCHEMAS:
        gerado = (tmp_path / nome).read_bytes()
        versionado = (RAIZ / "kb" / "schema" / nome).read_bytes()
        assert gerado == versionado, f"{nome} desatualizado: rode scripts/exportar_schema.py"
        assert gerado.endswith(b"\n") and b"\r" not in gerado


def test_motor_aplica_a_prioridade_efetiva_do_kb():
    """Sem prioridade gravada, o motor preenche exatamente o que o kb chama de efetiva."""
    base = carregar_base(carregar_minima())
    assert all(r.prioridade is None for r in base.regras)
    do_motor = [r["prioridade"] for r in BaseMotor.de_dict(para_motor(base)).regras]
    assert do_motor == [r.prioridade_efetiva for r in base.regras]


def test_prioridades_padrao_iguais_no_kb_e_no_motor():
    from engine.modelos import PRIORIDADES
    from kb.modelos import PRIORIDADE_POR_CLASSE
    assert PRIORIDADE_POR_CLASSE == PRIORIDADES
