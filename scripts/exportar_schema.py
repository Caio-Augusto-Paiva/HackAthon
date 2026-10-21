"""Exporta os JSON Schemas do kb (``Base`` e ``Caso``) para ``kb/schema/``.

Uso, a partir da raiz do repositório:
    .venv/Scripts/python scripts/exportar_schema.py
"""
from __future__ import annotations

import json
import sys
from pathlib import Path

RAIZ = Path(__file__).resolve().parents[1]
if str(RAIZ) not in sys.path:  # permite rodar como script, sem instalar o pacote
    sys.path.insert(0, str(RAIZ))

from kb.modelos import Base, Caso  # noqa: E402

DESTINO_PADRAO = RAIZ / "kb" / "schema"


def main(destino: Path | None = None) -> None:
    destino = Path(destino) if destino is not None else DESTINO_PADRAO
    destino.mkdir(parents=True, exist_ok=True)
    for nome, modelo in (("base.schema.json", Base), ("caso.schema.json", Caso)):
        texto = json.dumps(modelo.model_json_schema(), ensure_ascii=False, indent=2) + "\n"
        (destino / nome).write_bytes(texto.encode("utf-8"))  # bytes: sem conversão de fim de linha


if __name__ == "__main__":
    main()
