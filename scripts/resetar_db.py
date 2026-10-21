"""Apaga o banco SQLite local e recria o esquema (``--semear`` também grava os animais fictícios).

Uso, a partir da raiz do repositório (``ANAMNESE_DB`` vale como na API; padrão ``dados/anamnese.db``):
    .venv/Scripts/python scripts/resetar_db.py [--semear]
Só o banco é tocado: a pasta da base (``ANAMNESE_BASE_DIR``) nunca é alterada.
"""
from __future__ import annotations

import argparse
import sys
from pathlib import Path

RAIZ = Path(__file__).resolve().parents[1]
if str(RAIZ) not in sys.path:  # permite rodar como script, sem instalar o pacote
    sys.path.insert(0, str(RAIZ))

from api.config import carregar_configuracao  # noqa: E402
from api.db.conexao import inicializar  # noqa: E402
from scripts import semear_ficticios  # noqa: E402

_SUFIXOS_DO_SQLITE = ("", "-wal", "-shm", "-journal")


def resetar(db_path: Path) -> None:
    """Apaga o arquivo do banco (e os auxiliares do SQLite, se houver) e recria o esquema vazio."""
    for sufixo in _SUFIXOS_DO_SQLITE:
        Path(f"{db_path}{sufixo}").unlink(missing_ok=True)
    inicializar(db_path)


def main(argv: list[str] | None = None) -> None:
    analisador = argparse.ArgumentParser(description="Apaga o banco local e recria o esquema.")
    analisador.add_argument("--semear", action="store_true", help="grava também os animais fictícios")
    args = analisador.parse_args(argv)

    config = carregar_configuracao()
    try:
        resetar(config.db_path)
    except PermissionError:  # no Windows, o arquivo aberto por outro processo não pode ser apagado
        sys.exit(f"Não foi possível apagar {config.db_path}: feche o servidor que o está usando e tente de novo.")
    print(f"Banco recriado: {config.db_path}")
    if args.semear:
        semear_ficticios.main()


if __name__ == "__main__":
    main()
