"""Guardas de execução; validação editorial completa pertence ao kb."""
from .cf import fracao
from .modelos import CAMADAS, GRAVIDADES, LIMIARES, MODOS, CORTES

OPS = {'=', '≠', '<', '≤', '>', '≥', 'em'}


def validar(dados):
    simbolos = dados['simbolos']
    ids = [s['id'] for s in simbolos]
    regras = dados['regras']
    if len(ids) != len(set(ids)) or len({r['id'] for r in regras}) != len(regras):
        raise ValueError('Id duplicado')
    por_id = {s['id']:s for s in simbolos}
    for s in simbolos:
        if s['tipo'] not in CAMADAS or s['dominio']['tipo'] not in ('booleano','numerico','categorico'):
            raise ValueError('Tipo de símbolo/domínio inválido')
        if s['tipo'] == 'doenca' and s.get('gravidade') not in GRAVIDADES:
            raise ValueError('Doença sem gravidade válida')
        if s.get('combinacao','mycin') not in ('mycin','max') or (s.get('combinacao') == 'max' and s['tipo'] != 'derivado'):
            raise ValueError('Combinação max permitida somente em derivados')
    for r in regras:
        alvo = r['entao']['simbolo']
        if alvo not in por_id or not r.get('fonte') or not r.get('se'):
            raise ValueError('Regra sem símbolo, fonte ou condições')
        destino = por_id[alvo]
        cf = fracao(r['entao']['cf'])
        if abs(cf) > fracao(0.99) or (destino.get('combinacao') == 'max' and cf <= 0):
            raise ValueError('CF de regra inválido')
        classe = r.get('classe','evidencia')
        if classe not in ('evidencia','urgencia','bandeira_vermelha'):
            raise ValueError('Classe inválida')
        if (classe == 'evidencia') != (destino['tipo'] in ('doenca','derivado')):
            raise ValueError('Classe incompatível com a camada da conclusão')
        if classe == 'bandeira_vermelha' and alvo != 'chamar_agora':
            raise ValueError('Bandeira deve concluir chamar_agora')
        if classe == 'urgencia' and alvo not in ('observar','chamar_agora'):
            raise ValueError('Urgência inválida; sem_problema é calculado')
        for c in r['se']:
            if c['simbolo'] not in por_id:
                raise ValueError('Condição com símbolo indefinido')
            origem = por_id[c['simbolo']]
            if CAMADAS[origem['tipo']] >= CAMADAS[destino['tipo']]:
                raise ValueError('Violação de camada estrita')
            if c.get('op','=') not in OPS:
                raise ValueError('Operador inválido')
            limites = [c[k] for k in ('cf_minimo','cf_maximo') if k in c]
            if limites and (origem['tipo'] not in ('doenca','derivado') or len(limites)>1 or any(not 0<=fracao(v)<=1 for v in limites)):
                raise ValueError('Limite de CF inválido')
            if origem['dominio']['tipo'] != 'numerico' and c.get('op','=') in ('<','≤','>','≥'):
                raise ValueError('Operador incompatível com domínio')
    meta = dados.get('meta',{})
    limiares = {k:fracao(meta.get('limiares',{}).get(k,v)) for k,v in LIMIARES.items()}
    ordem = [limiares[k] for k in LIMIARES]
    if not (ordem[0]<0<ordem[1] and all(a<b for a,b in zip(ordem,ordem[1:]))):
        raise ValueError('Limiares fora de ordem')
    cortes={k:fracao(meta.get('limiares',{}).get(k,v)) for k,v in CORTES.items()}
    if not 0<=cortes['bloco_diferencial']<cortes['bloco_principal']<=1:
        raise ValueError('Cortes de exibição fora de ordem')
    for modo,limite in meta.get('limite_dinamico',{}).items():
        if modo not in MODOS or type(limite) is not int or limite<0:
            raise ValueError('Limite dinâmico inválido')
    telas=meta.get('triagem',[])
    if len({t['id'] for t in telas}) != len(telas):
        raise ValueError('Tela duplicada')
    for t in telas:
        if not t.get('simbolos') or any(id not in por_id or por_id[id]['tipo'] not in ('pergunta','ficha') for id in t['simbolos']):
            raise ValueError('Triagem com símbolo inválido')
