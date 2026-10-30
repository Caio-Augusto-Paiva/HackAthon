"""Empacota o backend Python para rodar no navegador (Pyodide): ``web/public/py/app.zip``.

Leva ``engine/``, ``kb/``, ``api/`` e a base (``ativa.json``, versões e casos). O site publicado na Cloudflare
carrega esse zip e roda a mesma API FastAPI dentro do navegador de quem acessa; nada é calculado em servidor.
Uso: ``python scripts/empacotar_navegador.py`` (depois ``npm run build:navegador`` em ``web/``).
"""
from __future__ import annotations

import zipfile
from pathlib import Path

RAIZ = Path(__file__).resolve().parents[1]
DESTINO = RAIZ / 'web/public/py/app.zip'
PASTAS = ('engine', 'kb', 'api')
BASE = ('base/ativa.json', 'base/versoes', 'base/casos')


def _arquivos():
    for pasta in PASTAS:
        for caminho in sorted((RAIZ / pasta).rglob('*')):
            if caminho.is_file() and '__pycache__' not in caminho.parts and caminho.suffix != '.pyc':
                yield caminho
    for item in BASE:
        caminho = RAIZ / item
        yield from (sorted(p for p in caminho.rglob('*') if p.is_file()) if caminho.is_dir() else [caminho])


def main() -> None:
    DESTINO.parent.mkdir(parents=True, exist_ok=True)
    with zipfile.ZipFile(DESTINO, 'w', zipfile.ZIP_DEFLATED) as zf:
        for caminho in _arquivos():
            zf.write(caminho, caminho.relative_to(RAIZ).as_posix())
    print(f'Gerado: {DESTINO.relative_to(RAIZ)} ({DESTINO.stat().st_size // 1024} KB)')


if __name__ == '__main__':
    main()
