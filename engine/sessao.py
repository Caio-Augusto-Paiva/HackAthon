"""Diálogo em memória; a API pode persistir entradas e reconstruir a sessão."""
from copy import deepcopy
from .modelos import Base, MODOS
from .memoria import Memoria
from .selecao import analisar
from .parada import motivo_parada
from .parecer import montar_parecer
from .explicacao import como
from .traco import evento, para_json
from .avaliacao import avaliar_condicao


class Sessao:
    def __init__(self, base, modo='produtor', ficha=None, limite_dinamico=None):
        self.base=Base.de_dict(base)
        if modo not in MODOS: raise ValueError('Modo inválido')
        if limite_dinamico is not None and (type(limite_dinamico) is not int or limite_dinamico<0):
            raise ValueError('Limite inválido')
        self.modo=modo
        self.limite_dinamico=limite_dinamico
        self.memoria=Memoria(self.base)
        self.traco=[]
        self.perguntas={}
        self.dinamicas=[]
        self.bandeiras_historicas={}
        self.reconhecidas=set()
        self.finalizada_por_alerta=False
        self.memoria.registrar(ficha or {},origem='ficha')
        self._calcular()

    @property
    def fatos(self): return dict(self.memoria.fatos)

    @property
    def resultado(self): return self.analise.resultado

    def _calcular(self):
        self.analise=analisar(self.base,self.memoria.fatos,self.modo)
        for e in self.resultado.traco:
            evento(self.traco,e['tipo'],**{k:v for k,v in e.items() if k not in ('id','tipo')})
        for id in self.resultado.bandeiras:
            if id not in self.bandeiras_historicas:
                self.bandeiras_historicas[id]=deepcopy(como(self.resultado,'chamar_agora'))

    def _ids_tela(self,tela):
        if 'simbolos_por_modo' in tela:
            return list(tela['simbolos_por_modo'].get(self.modo,[]))
        return [id for id in tela['simbolos'] if not self.base.simbolos[id].get('pergunta')
                or self.base.simbolos[id]['pergunta'].get(self.modo)]

    def _telas_pendentes(self):
        return [t for t in self.base.meta['triagem'] if any(id not in self.memoria.fatos for id in self._ids_tela(t))]

    def _pergunta(self,id,origem,motivo,**extras):
        if id not in self.perguntas:
            pergunta=evento(self.traco,'pergunta_feita',simbolo=id,origem=origem,motivo=motivo,**extras)
            self.perguntas[id]=pergunta

    def estado(self):
        pendentes=self._telas_pendentes()
        motivo=motivo_parada(self.analise,not pendentes,len(self.dinamicas),self.limite_dinamico)
        encerrada=bool(motivo) or self.finalizada_por_alerta
        pausa=self.modo=='produtor' and bool(set(self.bandeiras_historicas)-self.reconhecidas) and not self.finalizada_por_alerta
        proxima=None
        if not encerrada and not pausa:
            if pendentes:
                t=pendentes[0]; indice=self.base.meta['triagem'].index(t)+1
                ids=[id for id in self._ids_tela(t) if id not in self.memoria.fatos]
                proxima={'tipo':'tela_triagem','id':t['id'],'selecao':t['selecao'],'simbolos':ids,
                         'texto':t.get('texto',t.get('textos',{})).get(self.modo,t['id'])}
                for id in ids:
                    self._pergunta(id,'triagem',f'Triagem obrigatória, tela {indice} de {len(self.base.meta["triagem"])}',tela_id=t['id'])
            else:
                id=self.analise.proxima; s=self.base.simbolos[id]; candidato=self.analise.candidatos[id]
                serve=[]
                for d,regras in sorted(candidato['serve_a'].items()):
                    serve.append({'doenca':d,'nome':self.base.simbolos[d]['nome'],'gravidade':self.base.simbolos[d]['gravidade'],
                                  'cf_atual':self.resultado.cfs[d],'regras':sorted(regras)})
                motivo_pergunta=('Verificar bandeira vermelha parcialmente ativada.' if candidato['seguranca']
                                 else s.get('por_que',{}).get(self.modo,'Esclarecer hipóteses abertas: '+', '.join(x['doenca'] for x in serve)+'.'))
                proxima={'tipo':'pergunta','id':id,'pergunta':s['pergunta'][self.modo],'entrada':s['dominio']}
                self._pergunta(id,'fase_dinamica',motivo_pergunta,pergunta=s['pergunta'][self.modo],serve_a=serve)
        return para_json({'modo':self.modo,'versao_base':self.base.meta.get('versao'),
                          'fase':'encerrada' if encerrada else 'triagem' if pendentes else 'dinamica',
                          'pausa':pausa,'urgencia':'chamar_agora' if self.bandeiras_historicas else self.resultado.urgencia,
                          'bandeiras':sorted(self.bandeiras_historicas),'motivo_parada':motivo,'proxima':proxima,
                          'progresso':{'triagem_respondida':len(self.base.meta['triagem'])-len(pendentes),
                                       'triagem_total':len(self.base.meta['triagem']),
                                       'dinamicas_respondidas':len(self.dinamicas)}})

    def responder_triagem(self,tela_id,resposta,*,corrigir=False):
        telas={t['id']:t for t in self.base.meta['triagem']}
        if tela_id not in telas: raise ValueError('Tela inexistente')
        t=telas[tela_id]; ids=self._ids_tela(t)
        estado=self.estado()
        if corrigir:
            if not all(id in self.memoria.fatos for id in ids): raise ValueError('Tela ainda não respondida')
        elif estado['proxima'] is None or estado['proxima']['id']!=tela_id or estado['proxima']['tipo']!='tela_triagem':
            raise ValueError('Tela não é a próxima ou já foi respondida')
        else:
            ids=estado['proxima']['simbolos']
        if resposta is None or resposta in ('nao_sei','não sei'):
            entradas={id:None for id in ids}
        elif t['selecao']=='multipla':
            if not isinstance(resposta,list) or len(resposta)!=len(set(resposta)) or not set(resposta)<=set(ids):
                raise ValueError('Seleção múltipla inválida')
            entradas={id:id in resposta for id in ids}
        elif isinstance(resposta,dict):
            if set(resposta)!=set(ids): raise ValueError('Resposta não corresponde aos símbolos da tela')
            entradas=resposta
        elif len(ids)==1: entradas={ids[0]:resposta}
        else: raise ValueError('Informe os valores da tela por símbolo')
        self.memoria.registrar(entradas,tela_id=tela_id)
        self.finalizada_por_alerta=False
        self._calcular()
        return self.estado()

    def responder(self,simbolo,valor,*,corrigir=False):
        if corrigir:
            if simbolo not in self.dinamicas: raise ValueError('Pergunta ainda não respondida')
        else:
            proxima=self.estado()['proxima']
            if not proxima or proxima['tipo']!='pergunta' or proxima['id']!=simbolo:
                raise ValueError('Pergunta não aplicável neste momento/modo')
        self.memoria.registrar({simbolo:valor})
        if not corrigir: self.dinamicas.append(simbolo)
        self.finalizada_por_alerta=False
        self._calcular()
        return self.estado()

    def trocar_modo(self,modo):
        if modo not in MODOS: raise ValueError('Modo inválido')
        self.modo=modo
        self.finalizada_por_alerta=False
        self._calcular()
        return self.estado()

    def acao_bandeira(self,acao):
        if not self.bandeiras_historicas or acao not in ('continuar','ver_parecer'):
            raise ValueError('Ação de bandeira inválida')
        self.reconhecidas.update(self.bandeiras_historicas)
        self.finalizada_por_alerta=acao=='ver_parecer'
        return self.estado()

    def parecer(self):
        estado=self.estado()
        nao_verificadas=[]
        for regra in self.base.regras:
            if regra.get('classe')!='bandeira_vermelha' or regra['id'] in self.bandeiras_historicas:
                continue
            valores=[avaliar_condicao(c,self.resultado.fatos,self.base.simbolos) for c in regra['se']]
            if any(v==0 for v in valores) and all(v>=0 for v in valores):
                nao_verificadas.append(regra['id'])
        return montar_parecer(self.resultado,estado['motivo_parada'],estado['urgencia'],
                              sorted(self.bandeiras_historicas),sorted(nao_verificadas))

    def porque(self,simbolo):
        if simbolo not in self.perguntas: raise ValueError('Pergunta ainda não apresentada')
        return deepcopy(self.perguntas[simbolo])

    def como(self,simbolo):
        explicacao=como(self.resultado,simbolo)
        if simbolo=='chamar_agora': explicacao['bandeiras_historicas']=deepcopy(self.bandeiras_historicas)
        return explicacao
