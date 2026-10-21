"""Utilidades compartilhadas pelos serviços da API."""
from __future__ import annotations

import json


def texto_legivel(*valores: object) -> bool:
    r"""``False`` se algum texto (também dentro de dict e lista) tem um surrogate Unicode solto.

    O JSON aceita ``\ud800``; o banco e a resposta não o codificam em UTF-8, e sem esta checagem a gravação
    ou a resposta viraria 500.
    """
    try:
        json.dumps(valores, ensure_ascii=False).encode("utf-8")
    except ValueError:  # UnicodeEncodeError é um ValueError
        return False
    return True
