"""Critérios de encerramento independentes da interface."""
def motivo_parada(analise, triagem_completa, perguntas_dinamicas, limite=None):
    if not triagem_completa: return None
    r=analise.resultado
    lim=r.base.meta['limiares']
    confirmadas=[id for id in analise.potenciais if r.cfs[id]>=lim['confirmacao']]
    concorrentes=[id for id in analise.abertas if r.cfs[id]>lim['hipotese_relevante']
                  and analise.potenciais[id]>=lim['potencial']]
    if confirmadas and not concorrentes and not analise.bandeiras_pendentes:
        return 'confirmacao'
    limite=r.base.meta['limite_dinamico'][analise.modo] if limite is None else limite
    if type(limite) is not int or limite<0: raise ValueError('Limite inválido')
    if perguntas_dinamicas>=limite: return 'limite'
    if analise.proxima is None: return 'sem_perguntas'
    if analise.bandeiras_pendentes: return None
    if not any(analise.potenciais[id]>=lim['exaustao'] for id in analise.abertas):
        return 'sem_potencial'
    return None
