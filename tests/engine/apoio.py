"""Mini-bases sintéticas; não contêm recomendações clínicas."""
import importlib
import unittest


def modulo(nome):
    try:
        return importlib.import_module('engine.' + nome)
    except ModuleNotFoundError as erro:
        if erro.name == 'engine' or erro.name == 'engine.' + nome:
            unittest.TestCase().fail(f'Comportamento ainda não implementado: engine.{nome}')
        raise


def simbolo(id, tipo='pergunta', dominio='booleano', **extras):
    return dict(id=id, tipo=tipo, dominio={'tipo': dominio}, nome=id,
                **({'pergunta': {'produtor': id, 'veterinario': id}} if tipo in ('pergunta', 'ficha') else {}), **extras)


def condicao(id, valor=True, op='=', **extras):
    return {'simbolo': id, 'op': op, 'valor': valor, 'negado': False, **extras}


def regra(id, destino, cf, *condicoes, classe='evidencia', prioridade=0):
    return dict(id=id, se=list(condicoes), entao={'simbolo': destino, 'cf': cf},
                prioridade=prioridade, classe=classe, fonte='Teste sintético', status='suposicao_a_validar')


def base(simbolos, regras, triagem=()):
    return dict(meta={'versao': 'teste', 'triagem': list(triagem)}, simbolos=simbolos, regras=regras)


def doenca(id='d', gravidade='media'):
    return simbolo(id, 'doenca', gravidade=gravidade)
