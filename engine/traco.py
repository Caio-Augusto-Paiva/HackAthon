"""Eventos sem relógio/UUID: entradas iguais produzem o mesmo traço."""
from fractions import Fraction


def para_json(valor):
    if isinstance(valor,Fraction): return float(valor)
    if isinstance(valor,dict): return {k:para_json(v) for k,v in valor.items()}
    if isinstance(valor,(tuple,list)): return [para_json(v) for v in valor]
    return valor


def evento(traco, tipo, **dados):
    item={'id':f'ev_{len(traco)+1:04d}', 'tipo':tipo, **para_json(dados)}
    traco.append(item)
    return item


def dados_fato(fato):
    return dict(simbolo=fato.simbolo,valor=fato.valor,cf=fato.cf,
                origem=fato.origem,tela_id=fato.tela_id)
