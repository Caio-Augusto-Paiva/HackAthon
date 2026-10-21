"""Executa casos sintéticos; não calibra nem valida conhecimento clínico."""
from .sessao import Sessao


def executar_caso(base, caso):
    try:
        sessao=Sessao(base,caso['modo'],caso.get('ficha'),caso.get('limite_dinamico'))
        fases=[caso]+([caso['continuacao']] if caso.get('continuacao') else [])
        for indice,fase in enumerate(fases):
            if indice: sessao.trocar_modo(fase['modo'])
            # Cada iteração responde um símbolo/tela ainda ausente ou reconhece pausa.
            for _ in range(len(sessao.base.simbolos)*3+len(sessao.base.regras)+10):
                estado=sessao.estado()
                if estado['pausa']:
                    sessao.acao_bandeira('continuar'); continue
                if estado['fase']=='encerrada': break
                proxima=estado['proxima']; id=proxima['id']
                if proxima['tipo']=='tela_triagem':
                    sessao.responder_triagem(id,fase.get('triagem',{}).get(id,'nao_sei'))
                else:
                    sessao.responder(id,fase.get('respostas',{}).get(id,'nao_sei'))
            else: raise ValueError('Caso não terminou dentro do limite de segurança')
        parecer=sessao.parecer()
        itens=[x for bloco in parecer['blocos'] for x in bloco['itens']]
        itens.sort(key=lambda x:(-x['cf'],x['doenca']))
        obtido={'urgencia':parecer['urgencia'],'top1':itens[0]['doenca'] if itens else None,
                'top3_contem':[x['doenca'] for x in itens[:3]],
                'percentuais':{x['doenca']:x['percentual'] for x in itens},
                'motivo_parada':parecer['motivo_parada'],'bandeiras':parecer['bandeiras']}
        falhas=[]
        for campo,esperado in caso.get('esperado',{}).items():
            if campo in ('faixas','faixas_porcentagem'):
                for id,(minimo,maximo) in esperado.items():
                    valor=obtido['percentuais'].get(id)
                    if valor is None or not minimo<=valor<=maximo:
                        falhas.append({'campo':'faixas.'+id,'esperado':[minimo,maximo],'obtido':valor})
            elif campo=='bandeira':
                if esperado not in obtido['bandeiras']: falhas.append({'campo':campo,'esperado':esperado,'obtido':obtido['bandeiras']})
            elif campo=='top3_contem':
                if not set(esperado)<=set(obtido[campo]): falhas.append({'campo':campo,'esperado':esperado,'obtido':obtido[campo]})
            elif campo not in obtido:
                raise ValueError('Critério de caso desconhecido: '+campo)
            elif obtido[campo]!=esperado:
                falhas.append({'campo':campo,'esperado':esperado,'obtido':obtido[campo]})
        return {'caso_id':caso.get('id'),'status':'falhou' if falhas else 'passou','falhas':falhas,
                'obtido':obtido,'respondidas':sorted(sessao.fatos)}
    except (KeyError,ValueError,TypeError) as erro:
        return {'caso_id':caso.get('id'),'status':'erro','erro':str(erro)}
