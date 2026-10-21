"""Apoio dos testes do pacote kb: leitura das fixtures (dados fictícios)."""
import json
from pathlib import Path

RAIZ = Path(__file__).resolve().parents[2]
FIXTURES = RAIZ / "tests" / "fixtures"
CAMINHO_MINIMA = FIXTURES / "kb" / "base_minima.json"
CAMINHO_BASE_MOTOR = FIXTURES / "motor" / "base.json"


def carregar_minima() -> dict:
    """Devolve uma cópia nova (dict) da base mínima válida."""
    return json.loads(CAMINHO_MINIMA.read_text(encoding="utf-8"))
