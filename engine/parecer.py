"""Apresentação sem interpretação probabilística ou recomendação clínica."""
from fractions import Fraction

BLOCOS=(('hipoteses_principais','Hipóteses principais'),
        ('diagnostico_diferencial','Diagnóstico diferencial / sinais inespecíficos'),
        ('pouco_provavel','Pouco provável ou descartada'))


def percentual(cf):
    """max(0, CF) × 100, arredondado meio para cima, inclusive CF neutro."""
    numero=max(Fraction(0),cf)*100+Fraction(1,2)
    return numero.numerator//numero.denominator


def montar_parecer(resultado, motivo=None, urgencia=None, bandeiras=(), pendentes=(), potenciais=None):
    base=resultado.base
    blocos=[{'id':id,'titulo':titulo,'itens':[]} for id,titulo in BLOCOS]
    doencas=sorted((id for id,s in base.simbolos.items() if s['tipo']=='doenca'),
                   key=lambda id:(-resultado.cfs[id],id))
    for id in doencas:
        cf=resultado.cfs[id]; s=base.simbolos[id]
        situacao='descartada' if cf < -Fraction(1,5) else 'sem_evidencia' if cf<=Fraction(1,5) else 'com_evidencia'
        item={'doenca':id,'nome':s['nome'],'gravidade':s['gravidade'],'cf':float(cf),
              'percentual':percentual(cf),'situacao':situacao}
        item['potencial']=max(item['percentual'],percentual(potenciais[id])) if potenciais and id in potenciais else item['percentual']
        lim=base.meta['limiares']
        indice=0 if cf>=lim['bloco_principal'] else 1 if cf>lim['bloco_diferencial'] else 2
        blocos[indice]['itens'].append(item)
    lim=base.meta['limiares']
    return {'versao_base':base.meta.get('versao'), 'urgencia':urgencia or resultado.urgencia,
            'motivo_parada':motivo,'blocos':blocos,'bandeiras':list(bandeiras),
            'inconclusivas':[id for id in doencas if motivo=='limite' and lim['hipotese_relevante']<resultado.cfs[id]<lim['confirmacao']],
            'bandeiras_nao_verificadas':list(pendentes),
            'aviso':'Grau de confiança do sistema, não probabilidade. Conhecimento veterinário: suposição a validar.'}
