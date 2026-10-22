"""Impede publicar base ativa inválida ou desenvolvimento divergente das regras oficiais."""
import json
from pathlib import Path

from engine.modelos import Base as BaseMotor
from kb import carregar_base, para_motor, validar, validar_dados

RAIZ = Path(__file__).resolve().parents[2]
DESENVOLVIMENTO = RAIZ / 'base/desenvolvimento/anamnese-bovinos-v3.1.0-revisao1.json'


def base_ativa():
    versao = json.loads((RAIZ / 'base/ativa.json').read_text(encoding='utf-8'))['versao']
    return carregar_base(RAIZ / 'base/versoes' / f'{versao}.json')


def test_base_ativa_valida_sem_erros_e_carrega_no_motor():
    base = base_ativa()
    relatorio = validar(base)
    assert not relatorio.erros, relatorio.erros
    motor = BaseMotor.de_dict(para_motor(base))
    assert motor.regras


def test_desenvolvimento_tambem_passa_no_contrato_kb():
    dados = json.loads(DESENVOLVIMENTO.read_text(encoding='utf-8'))
    relatorio = validar_dados(dados)
    assert not relatorio.erros, relatorio.erros


def test_desenvolvimento_preserva_simbolos_regras_e_triagem_da_ativa():
    desenvolvimento = carregar_base(DESENVOLVIMENTO)
    ativa = base_ativa()
    assert desenvolvimento.simbolos == ativa.simbolos
    assert desenvolvimento.regras == ativa.regras
    assert desenvolvimento.meta.triagem == ativa.meta.triagem
