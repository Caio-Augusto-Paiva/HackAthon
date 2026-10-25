"""Critérios de encerramento independentes da interface."""
def limite_efetivo(base, modo, limite=None):
    """O limite explícito da sessão; sem ele, o da base no produtor e nenhum no especialista (pergunta até esgotar)."""
    if limite is None and modo=='veterinario': return None
    limite=base.meta['limite_dinamico'][modo] if limite is None else limite
    if type(limite) is not int or limite<0: raise ValueError('Limite inválido')
    return limite


def motivo_parada(analise, triagem_completa, perguntas_dinamicas, limite=None):
    if not triagem_completa: return None
    r=analise.resultado
    lim=r.base.meta['limiares']
    exaustivo=analise.modo=='veterinario'
    if not exaustivo:
        confirmadas=[id for id in analise.potenciais if r.cfs[id]>=lim['confirmacao']]
        concorrentes=[id for id in analise.abertas if r.cfs[id]>lim['hipotese_relevante']
                      and analise.potenciais[id]>=lim['potencial']]
        if confirmadas and not concorrentes and not analise.bandeiras_pendentes:
            return 'confirmacao'
    limite=limite_efetivo(r.base,analise.modo,limite)
    if limite is not None and perguntas_dinamicas>=limite: return 'limite'
    if analise.bandeiras_pendentes: return None
    if not analise.abertas: return 'sem_potencial'
    if analise.proxima is None: return 'sem_perguntas'
    # O especialista só para quando nenhuma pergunta muda mais nenhuma doença aberta.
    if not exaustivo and not any(analise.potenciais[id]>=lim['exaustao'] for id in analise.abertas):
        return 'sem_potencial'
    return None
