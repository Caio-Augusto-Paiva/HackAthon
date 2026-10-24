"""Propagação de CF nas três camadas; cada regra é aplicada uma vez."""
from dataclasses import dataclass
from fractions import Fraction
from .avaliacao import avaliar_condicao
from .cf import combinar, fracao
from .modelos import Base, CAMADAS, Fato, normalizar_fatos
from .traco import evento, dados_fato


@dataclass(frozen=True)
class Resultado:
    base: Base
    fatos: dict
    cfs: dict
    disparadas: tuple
    bandeiras: tuple
    urgencia: str
    traco: list
    excluidas: frozenset = frozenset()


def agenda(base):
    return sorted(base.regras, key=lambda r:(CAMADAS[base.simbolos[r['entao']['simbolo']]['tipo']],
                                           -r.get('prioridade',0),-len(r['se']),r['id']))


def aplicar_exclusoes(base, cfs, memoria, traco):
    """Rebaixa a doença mais fraca de cada par excludente; devolve os ids rebaixados.

    Os CFs de todos os pares são lidos antes de qualquer alteração, então a ordem
    dos pares não muda o resultado. Empate e vencedora abaixo do limiar não agem.
    """
    limiar=fracao(base.meta.get('limiares',{}).get('exclusao',0.5))
    originais=dict(cfs)
    novos={}
    for par in base.meta.get('exclusoes',[]):
        a,b=par['doencas']
        v,p=(a,b) if originais[a]>=originais[b] else (b,a)
        if originais[v]<limiar or originais[v]<=originais[p]: continue
        saida=combinar(originais[p],-originais[v])
        if p not in novos or saida<novos[p][0]:
            novos[p]=(saida,v,par)
    for p in sorted(novos):
        saida,v,par=novos[p]
        evento(traco,'exclusao_aplicada',simbolo=p,por=v,antes=originais[p],depois=saida,
               fonte=par.get('fonte'),nota=par.get('nota'))
        cfs[p]=saida
        memoria[p]=Fato(p,True,saida,'regra')
    return frozenset(novos)


def inferir(base, fatos):
    base=Base.de_dict(base)
    memoria=normalizar_fatos(base,fatos)
    traco=[]
    cfs={id:Fraction(0) for id in base.simbolos}
    for id,fato in memoria.items():
        cfs[id]=fato.cf
        evento(traco,'fato_adicionado',**dados_fato(fato))
    disparadas=[]
    urgencias=[]
    for r in agenda(base):
        condicoes=[avaliar_condicao(c,memoria,base.simbolos) for c in r['se']]
        premissa=min(condicoes)
        if premissa<=base.meta['limiares']['premissa']:
            continue
        id=r['entao']['simbolo']
        cf_regra=fracao(r['entao']['cf'])
        saida=premissa*cf_regra
        antes=cfs[id]
        depois=max(antes,saida) if base.simbolos[id].get('combinacao')=='max' else combinar(antes,saida)
        entradas=[{**dados_fato(memoria[c['simbolo']]),'cf_condicao':v,'condicao':c}
                  for c,v in zip(r['se'],condicoes)]
        evento(traco,'regra_disparada',regra_id=r['id'],simbolo=id,premissa=premissa,
               cf_regra=cf_regra,cf_saida=saida,entradas=entradas,fonte=r['fonte'],
               status=r.get('status','suposicao_a_validar'))
        evento(traco,'cf_combinado',simbolo=id,regra_id=r['id'],antes=antes,depois=depois)
        cfs[id]=depois
        memoria[id]=Fato(id,True,depois,'regra')
        evento(traco,'fato_adicionado',**dados_fato(memoria[id]),regra_id=r['id'])
        disparadas.append(r)
        if r.get('classe') in ('urgencia','bandeira_vermelha'): urgencias.append(id)
    excluidas=aplicar_exclusoes(base,cfs,memoria,traco)
    bandeiras=[r['id'] for r in disparadas if r.get('classe')=='bandeira_vermelha'
               and cfs[r['entao']['simbolo']]>0]
    urgencias={id for id in urgencias if cfs[id]>0}
    if 'chamar_agora' in urgencias:
        urgencia='chamar_agora'
    elif 'observar' in urgencias or any(cfs[id]>base.meta['limiares']['hipotese_relevante']
                                       for id,s in base.simbolos.items() if s['tipo']=='doenca'):
        urgencia='observar'
    else:
        urgencia='sem_problema'
    return Resultado(base,memoria,cfs,tuple(disparadas),tuple(bandeiras),urgencia,traco,excluidas)
