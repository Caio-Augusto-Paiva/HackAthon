"""Serve o build do frontend (``web/dist``) pela própria API, só se ele existir (Seção 5.2).

``/assets`` entrega os arquivos do build; qualquer outro ``GET`` fora de ``/api`` devolve ``index.html`` (ou o
arquivo de mesmo nome na raiz do ``dist``, como ``favicon.svg``), para o React funcionar ao recarregar a página
numa rota como ``/animais/an_001``. Sob ``/api`` nada disso vale: uma rota inexistente continua sendo o 404 do
formato único (``{"erro": ...}``), nunca o HTML.

Usa uma rota coringa própria, e não ``FastAPI.frontend()``, porque o fallback do FastAPI só vale para ``GET`` com
``Accept: text/html``; aqui o contrato (``/api`` sempre JSON, o resto sempre HTML) precisa ser o mesmo para todo cliente.
Efeito colateral aceito: só ``GET`` casa a rota coringa, então ``POST`` numa rota desconhecida e ``HEAD /`` dão 405.
"""
from __future__ import annotations

from pathlib import Path, PurePosixPath, PureWindowsPath

from fastapi import FastAPI
from fastapi.responses import FileResponse
from starlette.exceptions import HTTPException
from starlette.staticfiles import StaticFiles

PREFIXO_API = "api"
_PROIBIDOS_NO_CAMINHO = (chr(92), ":", chr(0))  # separador do Windows, unidade (C:) e byte nulo


def _caminho_seguro(caminho: str) -> bool:
    """Só olha o texto, sem tocar o disco: relativo, com ``/`` como separador, sem unidade, UNC nem ``..``.

    Um caminho de rede (``barra-invertida`` dupla, servidor, compartilhamento) ou ``C:/x`` levaria o Windows a abrir
    outro recurso já no ``resolve``; por isso a rejeição vem antes de qualquer acesso ao disco.
    """
    if not caminho or caminho.startswith("/") or any(c in caminho for c in _PROIBIDOS_NO_CAMINHO):
        return False
    janela = PureWindowsPath(caminho)
    if janela.drive or janela.is_absolute() or PurePosixPath(caminho).is_absolute():
        return False
    return ".." not in PurePosixPath(caminho).parts


def _arquivo_no_dist(dist: Path, caminho: str) -> Path | None:
    """O arquivo ``caminho`` dentro de ``dist``; ``None`` se não existe, é pasta ou escapa de ``dist``.

    O caminho é rejeitado pelo texto, antes de qualquer ``resolve`` ou ``is_file``; só o que passa chega ao disco.
    """
    if not _caminho_seguro(caminho):
        return None
    raiz = dist.resolve()
    try:
        alvo = (raiz / caminho).resolve()
    except (OSError, ValueError):  # nome que o sistema de arquivos recusa
        return None
    return alvo if alvo.is_file() and alvo.is_relative_to(raiz) else None


def montar_frontend(app: FastAPI, dist: Path) -> bool:
    """Monta ``dist`` no ``app`` e devolve ``True``; sem ``dist/index.html``, não monta nada e devolve ``False``.

    Chame depois de registrar todas as rotas da API: a rota coringa só pega o que nenhuma outra pegou.
    """
    indice = dist / "index.html"
    if not indice.is_file():
        return False
    if (dist / "assets").is_dir():
        app.mount("/assets", StaticFiles(directory=dist / "assets"), name="assets")

    @app.get("/{caminho:path}", include_in_schema=False)
    def pagina(caminho: str) -> FileResponse:
        caminho = caminho.lstrip("/")  # "//api/x" (barras a mais) também é /api
        if caminho == PREFIXO_API or caminho.startswith(PREFIXO_API + "/"):
            raise HTTPException(status_code=404)  # o handler devolve o formato único
        return FileResponse(_arquivo_no_dist(dist, caminho) or indice)

    return True
