"""Explica somente regras efetivamente disparadas e respostas observadas."""
from copy import deepcopy
from .parecer import percentual
from .traco import para_json


def como(resultado, simbolo):
    if simbolo not in resultado.base.simbolos: raise ValueError('Símbolo inexistente')
    evidencias=[]
    combinacoes=[]
    exclusoes=[]
    for e in resultado.traco:
        if e.get('simbolo')!=simbolo: continue
        if e['tipo']=='cf_combinado':
            combinacoes.append({'apos_regra':e['regra_id'],'antes':e['antes'],'depois':e['depois']})
        if e['tipo']=='exclusao_aplicada':
            exclusoes.append({'tipo':'exclusao','por':e['por'],'antes':e['antes'],'depois':e['depois'],
                              'fonte':e['fonte'],'nota':e['nota']})
        if e['tipo']=='regra_disparada':
            evidencia=deepcopy(e)
            evidencia.pop('id'); evidencia.pop('tipo')
            for entrada in evidencia['entradas']:
                if entrada['origem']=='regra':
                    entrada['evidencias']=como(resultado,entrada['simbolo'])['evidencias']
            evidencias.append(evidencia)
    cf=resultado.cfs[simbolo]
    return para_json({'simbolo':simbolo,'nome':resultado.base.simbolos[simbolo]['nome'],
                      'cf':cf,'percentual':percentual(cf),'combinacao':combinacoes,'exclusoes':exclusoes,'evidencias':evidencias})
