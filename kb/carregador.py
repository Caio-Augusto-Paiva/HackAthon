"""Repositório de versões imutáveis da base de conhecimento (arquivos JSON).

Layout sob ``raiz``: ``versoes/vNNNN.json`` (nunca sobrescritas), ``ativa.json``
(ponteiro ``{"versao": "vNNNN"}``) e ``casos/casos.json``. Salvar sempre cria a
próxima versão; ativar apenas move o ponteiro.
"""
from __future__ import annotations

import hashlib
import json
import re
from collections.abc import Callable
from datetime import date
from pathlib import Path

from kb.modelos import Base, Caso, carregar_base
from kb.validador import Relatorio, validar

_NOME_VERSAO = re.compile(r"v(\d{4})\.json")


class BaseInvalida(Exception):
    """A base tem erros de validação; nada foi gravado."""

    def __init__(self, relatorio: Relatorio):
        self.relatorio = relatorio
        super().__init__(
            f"Base inválida: {len(relatorio.erros)} erro(s) de validação; nada foi gravado."
        )


def _json(dados) -> str:
    return json.dumps(dados, ensure_ascii=False, indent=2) + "\n"


class Repositorio:
    def __init__(self, raiz: Path, *, hoje: Callable[[], date] = date.today):
        self.raiz = Path(raiz)
        self._hoje = hoje

    # --- caminhos ---------------------------------------------------------

    def _arquivo(self, versao: str) -> Path:
        return self.raiz / "versoes" / f"{versao}.json"

    @property
    def _ativa(self) -> Path:
        return self.raiz / "ativa.json"

    # --- leitura ----------------------------------------------------------

    def listar_versoes(self) -> list[str]:
        pasta = self.raiz / "versoes"
        if not pasta.is_dir():
            return []
        return sorted(p.stem for p in pasta.iterdir() if p.is_file() and _NOME_VERSAO.fullmatch(p.name))

    def carregar(self, versao: str) -> Base:
        arquivo = self._arquivo(versao)
        if not arquivo.is_file():
            raise FileNotFoundError(f"Versão {versao} não encontrada em {arquivo.parent}.")
        return carregar_base(arquivo)

    def versao_ativa(self) -> str | None:
        if not self._ativa.is_file():
            return None
        return json.loads(self._ativa.read_text(encoding="utf-8"))["versao"]

    def carregar_ativa(self) -> Base:
        versao = self.versao_ativa()
        if versao is None:
            raise FileNotFoundError(f"Nenhuma versão ativa: {self._ativa} não existe.")
        try:
            return self.carregar(versao)
        except FileNotFoundError:
            raise FileNotFoundError(
                f"A versão ativa {versao} (apontada por {self._ativa.name}) não existe em versoes/."
            ) from None

    def hash(self, versao: str) -> str:
        arquivo = self._arquivo(versao)
        if not arquivo.is_file():
            raise FileNotFoundError(f"Versão {versao} não encontrada em {arquivo.parent}.")
        return "sha256:" + hashlib.sha256(arquivo.read_bytes()).hexdigest()

    def carregar_casos(self) -> list[Caso]:
        arquivo = self.raiz / "casos" / "casos.json"
        if not arquivo.is_file():
            return []
        return [Caso.model_validate(c) for c in json.loads(arquivo.read_text(encoding="utf-8"))]

    # --- escrita ----------------------------------------------------------

    def _proxima(self) -> str:
        numeros = [int(v[1:]) for v in self.listar_versoes()]
        return f"v{max(numeros, default=0) + 1:04d}"

    def salvar_nova(self, base: Base, *, autor: str, nota: str, pai: str | None = None) -> str:
        """Valida e grava a próxima versão (sem ativá-la); devolve o id da versão."""
        relatorio = validar(base)
        if not relatorio.valida:
            raise BaseInvalida(relatorio)
        versao = self._proxima()
        meta = base.meta.model_copy(
            update={
                "versao": versao,
                "pai": pai if pai is not None else self.versao_ativa(),
                "autor": autor,
                "nota": nota,
                "data": self._hoje().isoformat(),
            },
            deep=True,
        )
        nova = base.model_copy(update={"meta": meta})
        texto = _json(nova.model_dump(mode="json", exclude_none=True))
        arquivo = self._arquivo(versao)
        arquivo.parent.mkdir(parents=True, exist_ok=True)
        with open(arquivo, "x", encoding="utf-8", newline="\n") as f:
            f.write(texto)
        return versao

    def ativar(self, versao: str) -> None:
        if not self._arquivo(versao).is_file():
            raise FileNotFoundError(f"Não é possível ativar {versao}: versão não encontrada.")
        self.raiz.mkdir(parents=True, exist_ok=True)
        with open(self._ativa, "w", encoding="utf-8", newline="\n") as f:
            f.write(_json({"versao": versao}))
