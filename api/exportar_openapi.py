"""Exporta o OpenAPI da API para ``contratos/openapi.json`` (versionado; o teste de contrato o confere).

Uso: ``python -m api.exportar_openapi``. Monta o app sem subir servidor e sem tocar no disco: o ``lifespan`` (que
cria o banco) só roda quando o app sobe, e a configuração usada aqui aponta para caminhos que nunca são criados,
sem ler ``ANAMNESE_BASE_DIR`` nem ``ANAMNESE_DB``.
"""
from __future__ import annotations

import json
import tempfile
from datetime import date, datetime
from pathlib import Path

from api.config import Configuracao
from api.main import criar_app

DESTINO_PADRAO = Path(__file__).resolve().parents[1] / "contratos" / "openapi.json"

# caminhos de mentira: o OpenAPI não os lê, e nada neste módulo os cria
_NEUTRO = Path(tempfile.gettempdir()) / "anamnese-openapi-sem-io"


def _config_neutra() -> Configuracao:
    return Configuracao(
        base_dir=_NEUTRO / "base",
        db_path=_NEUTRO / "dados" / "anamnese.db",
        web_dist=_NEUTRO / "web" / "dist",
        hoje=date.today,
        agora=datetime.now,
    )


def gerar_texto() -> str:
    """O OpenAPI como texto estável: chaves ordenadas, recuo de 2, UTF-8 direto e quebra de linha final."""
    documento = criar_app(_config_neutra()).openapi()
    return json.dumps(documento, indent=2, sort_keys=True, ensure_ascii=False) + "\n"


def main(destino: Path = DESTINO_PADRAO) -> None:
    """Grava o OpenAPI em ``destino`` (UTF-8, quebra de linha ``\\n`` em qualquer sistema)."""
    destino = Path(destino)
    destino.parent.mkdir(parents=True, exist_ok=True)
    destino.write_text(gerar_texto(), encoding="utf-8", newline="\n")


if __name__ == "__main__":
    main()
