"""Apaga o banco SQLite local e recria o esquema (``--semear`` também grava os animais fictícios).

Uso, a partir da raiz do repositório (``ANAMNESE_DB`` vale como na API; padrão ``dados/anamnese.db``):
    .venv/Scripts/python scripts/resetar_db.py [--semear]
Só o banco é tocado: a pasta da base (``ANAMNESE_BASE_DIR``) nunca é alterada. Antes de apagar, o alvo é conferido:
só vale arquivo SQLite (cabeçalho ``SQLite format 3``) ou arquivo vazio; um ``ANAMNESE_DB`` apontado por engano para
um JSON, uma pasta ou qualquer outro arquivo é recusado, e nada é apagado.
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

CABECALHO_SQLITE = b"SQLite format 3\x00"  # os 16 primeiros bytes de todo arquivo SQLite
_SUFIXOS_AUXILIARES = ("-wal", "-shm", "-journal")


class RecusaDeReset(Exception):
    """O alvo existe e não é um banco SQLite (nem arquivo vazio): nada é apagado."""


def _conferir_alvo(db_path: Path) -> None:
    """Levanta ``RecusaDeReset`` se ``db_path`` existe e não é arquivo SQLite nem arquivo vazio."""
    if db_path.is_dir():
        raise RecusaDeReset(f"{db_path} é uma pasta, não um arquivo de banco; recuso apagar.")
    if not db_path.exists():
        return
    if not db_path.is_file():
        raise RecusaDeReset(f"{db_path} não é um arquivo comum; recuso apagar.")
    with db_path.open("rb") as arquivo:
        inicio = arquivo.read(len(CABECALHO_SQLITE))
    if inicio and inicio != CABECALHO_SQLITE:
        raise RecusaDeReset(f"{db_path} não é um banco SQLite; recuso apagar.")


def resetar(db_path: Path) -> None:
    """Apaga o arquivo do banco (e os auxiliares do SQLite, se houver) e recria o esquema vazio.

    Só apaga se o alvo não existe, é arquivo vazio ou é um SQLite; senão levanta ``RecusaDeReset`` antes de apagar
    qualquer coisa (os auxiliares ``-wal``/``-shm``/``-journal`` também só caem depois dessa conferência).
    """
    _conferir_alvo(db_path)
    db_path.unlink(missing_ok=True)
    for sufixo in _SUFIXOS_AUXILIARES:
        auxiliar = Path(f"{db_path}{sufixo}")
        if auxiliar.is_file():
            auxiliar.unlink()
    inicializar(db_path)


def main(argv: list[str] | None = None) -> None:
    analisador = argparse.ArgumentParser(description="Apaga o banco local e recria o esquema.")
    analisador.add_argument("--semear", action="store_true", help="grava também os animais fictícios")
    args = analisador.parse_args(argv)

    config = carregar_configuracao()
    try:
        resetar(config.db_path)
    except RecusaDeReset as recusa:
        sys.exit(str(recusa))  # mensagem no stderr e saída 1
    except PermissionError:  # no Windows, o arquivo aberto por outro processo não pode ser apagado
        sys.exit(f"Não foi possível apagar {config.db_path}: feche o servidor que o está usando e tente de novo.")
    print(f"Banco recriado: {config.db_path}")
    if args.semear:
        semear_ficticios.main()


if __name__ == "__main__":
    main()
