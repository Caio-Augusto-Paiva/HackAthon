"""Semeia animais fictícios no banco local. Dados fictícios apenas: nenhum animal ou propriedade real.

Idempotente por ``brinco``: o que já existe não é tocado. O primeiro animal (``BR-0001``, "Mimosa") é o da
anamnese do produtor do roteiro da demonstração (parto há 6 dias); "Estrela" tem parto há 1 dia (6.2.2).

Uso, a partir da raiz do repositório (``ANAMNESE_DB`` e ``ANAMNESE_BASE_DIR`` valem como na API):
    .venv/Scripts/python scripts/semear_ficticios.py
"""
from __future__ import annotations

import sqlite3
import sys
from contextlib import closing
from datetime import datetime, timedelta
from pathlib import Path

RAIZ = Path(__file__).resolve().parents[1]
if str(RAIZ) not in sys.path:  # permite rodar como script, sem instalar o pacote
    sys.path.insert(0, str(RAIZ))

from api.config import carregar_configuracao  # noqa: E402
from api.db import repositorios as repo  # noqa: E402
from api.db.conexao import abrir, inicializar  # noqa: E402
from api.servicos.ficha import CAMPO_DATA_PARTO, completar_ficha, validar_ficha  # noqa: E402
from kb.carregador import Repositorio  # noqa: E402
from kb.modelos import Base  # noqa: E402

# (brinco, nome, dias desde o parto, demais campos da ficha da Seção 3.2). Campo ausente = a pergunta é feita.
ANIMAIS: tuple[tuple[str, str, int, dict], ...] = (
    (
        "BR-0001", "Mimosa", 6,
        {"numero_lactacoes": 3, "raca_grupo": "cruzada", "historico_retencao_placenta": False, "parto_distocico": False,
         "historico_mastite_12m": True, "mudanca_dieta_recente": False, "casos_podais_no_rebanho": False},
    ),
    (
        "BR-0002", "Estrela", 1,
        {"numero_lactacoes": 4, "raca_grupo": "europeia", "historico_retencao_placenta": False, "parto_distocico": False,
         "historico_mastite_12m": False},
    ),
    (
        "BR-0003", "Jurema", 100,
        {"numero_lactacoes": 2, "raca_grupo": "europeia", "historico_retencao_placenta": False, "parto_distocico": False,
         "historico_mastite_12m": False, "casos_podais_no_rebanho": False},
    ),
    (
        "BR-0004", "Boneca", 45,
        {"numero_lactacoes": 1, "raca_grupo": "zebuina", "historico_retencao_placenta": True, "parto_distocico": True,
         "historico_mastite_12m": False, "mudanca_dieta_recente": True},
    ),
)


def base_ativa_ou_none(base_dir: Path) -> Base | None:
    """A base ativa, ou ``None`` se ainda não existe ou não carrega: a semente nunca depende dela para rodar."""
    try:
        return Repositorio(base_dir).carregar_ativa()
    except Exception as erro:  # sem ativa.json, versão faltando, JSON ou base inválidos
        print(f"Aviso: sem base ativa utilizável em {base_dir} ({type(erro).__name__}); fichas semeadas sem validação.")
        return None


def _ficha(dias: int, campos: dict, agora: datetime, base: Base | None) -> dict:
    ficha = {CAMPO_DATA_PARTO: (agora.date() - timedelta(days=dias)).isoformat(), **campos}
    if base is None:
        return ficha
    invalidos = {erro.campo for erro in validar_ficha(base, ficha)}  # campo que a base não tem ou não aceita
    return completar_ficha(base, {c: v for c, v in ficha.items() if c not in invalidos})


def semear(conn: sqlite3.Connection, agora: datetime, base: Base | None = None) -> int:
    """Grava os animais fictícios que ainda não existem (por ``brinco``) e devolve quantos criou.

    Com ``base``, cada ficha é validada por ela: o campo inválido ou desconhecido é pulado (nunca quebra) e a
    ficha sai completa, com ``null`` onde falta. Sem ``base``, a ficha é gravada como está. Uma transação só.
    """
    criados = 0
    with conn:
        for brinco, nome, dias, campos in ANIMAIS:
            if repo.obter_animal_por_brinco(conn, brinco) is not None:
                continue
            repo.inserir_animal(
                conn, brinco=brinco, nome=nome, ficha=_ficha(dias, campos, agora, base), origens={}, agora=agora
            )
            criados += 1
    return criados


def main() -> None:
    config = carregar_configuracao()
    inicializar(config.db_path)  # cria a pasta e o esquema se faltar (não toca no que já existe)
    base = base_ativa_ou_none(config.base_dir)
    with closing(abrir(config.db_path)) as conn:
        criados = semear(conn, config.agora(), base)
    print(f"Animais fictícios criados: {criados} (banco: {config.db_path}).")


if __name__ == "__main__":
    main()
