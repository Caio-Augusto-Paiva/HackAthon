"""Semântica das condições, compartilhada pela propagação e pela seleção."""
from fractions import Fraction
from .cf import fracao
from .modelos import Fato, desconhecido


def satisfaz(valor, op, esperado):
    if op == '=': return valor == esperado
    if op == '≠': return valor != esperado
    if op == '<': return valor < esperado
    if op == '≤': return valor <= esperado
    if op == '>': return valor > esperado
    if op == '≥': return valor >= esperado
    if op == 'em': return valor in esperado
    raise ValueError('Operador inválido')


def avaliar_condicao(condicao, fatos, simbolos):
    fato = fatos.get(condicao['simbolo'])
    if fato is None: return Fraction(0)
    if isinstance(fato,Fato): valor,cf = fato.valor,fato.cf
    else: valor,cf = fato.get('valor'),fracao(fato.get('cf',0))
    if desconhecido(valor) or not cf: return Fraction(0)
    if 'cf_minimo' in condicao:
        resultado = cf if cf>=fracao(condicao['cf_minimo']) else Fraction(0)
    elif 'cf_maximo' in condicao:
        resultado = -cf if cf<=fracao(condicao['cf_maximo']) else Fraction(0)
    else:
        tipo = simbolos[condicao['simbolo']]['dominio']['tipo']
        op,esperado = condicao.get('op','='),condicao.get('valor',True)
        if tipo == 'booleano':
            if esperado in ('sim','não','nao'): esperado = esperado == 'sim'
            resultado = cf if satisfaz(True,op,esperado) else -cf
        else:
            if tipo == 'numerico':
                valor = Fraction(str(valor))
                esperado = [Fraction(str(x)) for x in esperado] if op=='em' else Fraction(str(esperado))
            resultado = cf if satisfaz(valor,op,esperado) else -cf
    return -resultado if condicao.get('negado',False) else resultado
