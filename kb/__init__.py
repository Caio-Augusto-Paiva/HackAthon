"""Base de conhecimento do sistema especialista de anamnese (ver ``kb/README.md``)."""
from kb.modelos import Base, Caso, carregar_base, para_motor
from kb.validador import validar, validar_dados, validar_edicao

__all__ = [
    "Base", "Caso", "carregar_base", "para_motor", "validar", "validar_dados", "validar_edicao",
]
