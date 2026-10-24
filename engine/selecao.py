"""Busca dirigida a objetivos e limites conservadores de potencial."""
from dataclasses import dataclass
from fractions import Fraction
from .avaliacao import avaliar_condicao
from .cf import combinar, fracao
from .inferencia import inferir, agenda
from .modelos import Fato, GRAVIDADES, MODOS


def perguntavel(simbolo, modo):
    return simbolo['tipo'] in ('pergunta','ficha') and bool(simbolo.get('pergunta',{}).get(modo))


def _valores_numericos(condicoes, dominio):
    pontos=set()
    for c in condicoes:
        valores=c.get('valor',0) if c.get('op')=='em' else [c.get('valor',0)]
        pontos.update(Fraction(str(x)) for x in valores)
    for k in ('min','max'):
        if k in dominio: pontos.add(Fraction(str(dominio[k])))
    pontos=sorted(pontos or {Fraction(0)})
    candidatos=set(pontos)
    candidatos.update((a+b)/2 for a,b in zip(pontos,pontos[1:]))
    candidatos.update((pontos[0]-1,pontos[-1]+1))
    return [x for x in sorted(candidatos) if ('min' not in dominio or x>=Fraction(str(dominio['min'])))
            and ('max' not in dominio or x<=Fraction(str(dominio['max'])))]


def _limites_grupo(id, condicoes, intervalos, resultado, modo, fixos=None):
    """Condições da mesma variável compartilham um valor possível."""
    s=resultado.base.simbolos[id]
    if s['tipo'] in ('pergunta','ficha'):
        if id in resultado.fatos or not perguntavel(s,modo):
            valor=min(avaliar_condicao(c,resultado.fatos,resultado.base.simbolos) for c in condicoes)
            return valor,valor
        dominio=s['dominio']
        if dominio['tipo']=='booleano': valores=[False,True]
        elif dominio['tipo']=='numerico': valores=_valores_numericos(condicoes,dominio)
        else:
            valores=dominio.get('valores')
            if valores is None:
                valores=['__outro__']
                for c in condicoes:
                    valores.extend(c.get('valor',[]) if c.get('op')=='em' else [c.get('valor')])
        if fixos is not None and id in fixos: valores=[fixos[id]]
        possiveis=[Fraction(0)]  # responder não sei também é possível
        for valor in valores:
            cf=-Fraction(1) if valor is False else Fraction(1)
            memoria={id:Fato(id,valor,cf)}
            possiveis.append(min(avaliar_condicao(c,memoria,resultado.base.simbolos) for c in condicoes))
    else:
        baixo,alto=intervalos[id]
        pontos={baixo,alto}
        if baixo<=0<=alto: pontos.add(Fraction(0))
        for c in condicoes:
            for k in ('cf_minimo','cf_maximo'):
                if k in c:
                    valor=fracao(c[k])
                    if baixo<=valor<=alto: pontos.add(valor)
        pontos=sorted(pontos)
        pontos+= [(a+b)/2 for a,b in zip(pontos,pontos[1:])]
        possiveis=[min(avaliar_condicao(c,{id:Fato(id,True,x,'regra')},resultado.base.simbolos)
                       for c in condicoes) for x in pontos]
    return min(possiveis),max(possiveis)


def _premissa(r, intervalos, resultado, modo, fixos=None):
    grupos={}
    for c in r['se']: grupos.setdefault(c['simbolo'],[]).append(c)
    limites=[_limites_grupo(id,cs,intervalos,resultado,modo,fixos) for id,cs in grupos.items()]
    return min(x[0] for x in limites),min(x[1] for x in limites)


def _fontes(id,base):
    if base.simbolos[id]['tipo'] in ('pergunta','ficha'): return [id]
    return [folha for r in base.regras_para(id) for c in r['se'] for folha in _fontes(c['simbolo'],base)]


def _compartilhadas(regra,base,resultado,modo):
    # Repetição em caminhos diferentes exige o mesmo valor da observação.
    folhas=[id for c in regra['se'] for id in _fontes(c['simbolo'],base)]
    return sorted(id for id in set(folhas) if folhas.count(id)>1 and id not in resultado.fatos
                  and perguntavel(base.simbolos[id],modo))


def _valores_folha(id,base):
    dominio=base.simbolos[id]['dominio']
    condicoes=[c for r in base.regras for c in r['se'] if c['simbolo']==id]
    if dominio['tipo']=='booleano': return [False,True]
    if dominio['tipo']=='numerico': return _valores_numericos(condicoes,dominio)
    if 'valores' in dominio: return dominio['valores']
    valores=['__outro__']
    for c in condicoes: valores.extend(c.get('valor',[]) if c.get('op')=='em' else [c.get('valor')])
    return list(dict.fromkeys(valores))


def _consistente(regra,resultado,modo,excluidas):
    ids=_compartilhadas(regra,resultado.base,resultado,modo)
    if not ids: return True

    def buscar(indice,fixos):
        intervalos,_=_calcular_intervalos(resultado,modo,fixos,excluidas,verificar=False)
        if _premissa(regra,intervalos,resultado,modo,fixos)[1]<=resultado.base.meta['limiares']['premissa']:
            return False
        if indice==len(ids): return True
        id=ids[indice]
        for valor in _valores_folha(id,resultado.base):
            if buscar(indice+1,{**fixos,id:valor}): return True
        return False

    return buscar(0,{})


def _calcular_intervalos(resultado,modo,fixos=None,excluidas=None,verificar=True):
    base=resultado.base
    excluidas=set(excluidas or ())
    intervalos={id:(resultado.cfs[id],resultado.cfs[id]) if s['tipo'] in ('pergunta','ficha') else (Fraction(0),Fraction(0))
                for id,s in base.simbolos.items()}
    viaveis={}
    for r in agenda(base):
        if r['id'] in excluidas: continue
        baixo,alto=_premissa(r,intervalos,resultado,modo,fixos)
        if alto<=base.meta['limiares']['premissa']: continue
        if verificar and not _consistente(r,resultado,modo,excluidas):
            excluidas.add(r['id'])
            continue
        viaveis[r['id']]=r
        peso=fracao(r['entao']['cf'])
        contribuicoes=[alto*peso, baixo*peso if baixo>base.meta['limiares']['premissa'] else Fraction(0)]
        id=r['entao']['simbolo']
        anterior=intervalos[id]
        if base.simbolos[id].get('combinacao')=='max':
            intervalos[id]=(max(anterior[0],min(contribuicoes)),max(anterior[1],max(contribuicoes)))
        else:
            intervalos[id]=(combinar(anterior[0],min(contribuicoes)),combinar(anterior[1],max(contribuicoes)))
    return intervalos,viaveis


@dataclass(frozen=True)
class Analise:
    resultado: object
    modo: str
    potenciais: dict
    intervalos: dict
    viaveis: dict
    abertas: tuple
    candidatos: dict
    proxima: str | None
    bandeiras_pendentes: tuple


def analisar(base, fatos, modo):
    if modo not in MODOS: raise ValueError('Modo inválido')
    resultado=inferir(base,fatos)
    base=resultado.base
    lim=base.meta['limiares']
    intervalos,viaveis=_calcular_intervalos(resultado,modo)
    potenciais={id:intervalos[id][1] for id,s in base.simbolos.items() if s['tipo']=='doenca'}
    abertas=tuple(sorted(id for id in potenciais if id not in resultado.excluidas and lim['descarte']<resultado.cfs[id]<lim['confirmacao']))
    candidatos={}

    def folhas(id, fator):
        s=base.simbolos[id]
        if s['tipo'] in ('pergunta','ficha'):
            return [(id,fator)] if id not in resultado.fatos and perguntavel(s,modo) else []
        saida=[]
        if s['tipo']=='derivado':
            for r in base.regras_para(id):
                if r['id'] in viaveis:
                    for entrada in sorted({c['simbolo'] for c in r['se']}):
                        saida.extend(folhas(entrada,fator*abs(fracao(r['entao']['cf']))))
        return saida

    def adicionar(id,peso,doenca,regra,seguranca=False):
        item=candidatos.setdefault(id,{'peso':Fraction(0),'gravidade':-1,'serve_a':{},'seguranca':False})
        item['peso']+=peso
        item['seguranca'] |= seguranca
        if doenca:
            item['gravidade']=max(item['gravidade'],GRAVIDADES[base.simbolos[doenca]['gravidade']])
            item['serve_a'].setdefault(doenca,set()).add(regra)

    for id in abertas:
        for r in base.regras_para(id):
            if r['id'] not in viaveis: continue
            for entrada in sorted({c['simbolo'] for c in r['se']}):
                for folha,peso in folhas(entrada,abs(fracao(r['entao']['cf']))):
                    adicionar(folha,peso,id,r['id'])
    pendentes=[]
    for r in base.regras:
        if r.get('classe')!='bandeira_vermelha' or r['id'] not in viaveis or r in resultado.disparadas:
            continue
        ativada=any(avaliar_condicao(c,resultado.fatos,base.simbolos)>lim['premissa'] for c in r['se'])
        faltantes=[]
        for entrada in sorted({c['simbolo'] for c in r['se']}):
            faltantes.extend(folhas(entrada,abs(fracao(r['entao']['cf']))))
        if ativada and faltantes:
            pendentes.append(r['id'])
            for id,peso in faltantes: adicionar(id,peso,None,r['id'],True)
    ordem=sorted(candidatos,key=lambda id:(not candidatos[id]['seguranca'],-candidatos[id]['peso'],-candidatos[id]['gravidade'],id))
    return Analise(resultado,modo,potenciais,intervalos,viaveis,abertas,candidatos,
                   ordem[0] if ordem else None,tuple(sorted(pendentes)))
