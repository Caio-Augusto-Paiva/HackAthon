"""Superfície pública do pacote ``kb``."""


def test_reexporta_a_api_publica():
    import kb
    from kb.modelos import Base, Caso, carregar_base, para_motor
    from kb.validador import validar, validar_dados, validar_edicao

    assert kb.Base is Base and kb.Caso is Caso
    assert kb.carregar_base is carregar_base and kb.para_motor is para_motor
    assert kb.validar is validar and kb.validar_dados is validar_dados
    assert kb.validar_edicao is validar_edicao


def test_import_direto_dos_nomes():
    from kb import Base, Caso, carregar_base, para_motor, validar, validar_dados, validar_edicao
    assert all((Base, Caso, carregar_base, para_motor, validar, validar_dados, validar_edicao))


def test_all_lista_so_nomes_existentes():
    import kb
    assert set(kb.__all__) == {
        "Base", "Caso", "carregar_base", "validar", "validar_dados", "validar_edicao", "para_motor",
    }
    assert all(hasattr(kb, nome) for nome in kb.__all__)


def test_kb_continua_pacote_folha():
    import subprocess
    import sys
    codigo = "import sys, kb; sys.exit(1 if 'engine' in sys.modules else 0)"
    assert subprocess.run([sys.executable, "-c", codigo]).returncode == 0
