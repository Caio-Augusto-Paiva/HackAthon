"""Diálogo em memória; a API pode persistir entradas e reconstruir a sessão."""
import re
from fractions import Fraction
from copy import deepcopy
from .modelos import Base, MODOS
from .memoria import Memoria
from .selecao import analisar, _fontes
from .inferencia import inferir
from .parada import limite_efetivo, motivo_parada
from .parecer import montar_parecer
from .explicacao import como
from .traco import evento, para_json, dados_fato
from .avaliacao import avaliar_condicao


def _racionais_do_snapshot(fatos, simbolos):
    """`exportar` grava números racionais como "a/b". Só no snapshot esse texto volta a Fraction; a
    entrada digitada nunca passa por aqui (`observar` recusa frações em texto). O domínio continua conferido."""
    saida = {}
    for id, entrada in fatos.items():
        bruto = entrada.get('valor') if isinstance(entrada, dict) else None
        if (isinstance(bruto, str) and id in simbolos and simbolos[id]['dominio']['tipo'] == 'numerico'
                and re.fullmatch(r'[0-9]+/[0-9]+', bruto, re.ASCII) and int(bruto.split('/')[1]) > 0):
            entrada = {**entrada, 'valor': Fraction(bruto)}
        saida[id] = entrada
    return saida


class Sessao:
    def __init__(self, base, modo='produtor', ficha=None, limite_dinamico=None):
        self._iniciar(base,modo,ficha,limite_dinamico)
        self._calcular()

    def _iniciar(self, base, modo, ficha, limite_dinamico):
        self.base=Base.de_dict(base)
        if modo not in MODOS: raise ValueError('Modo inválido')
        if limite_dinamico is not None and (type(limite_dinamico) is not int or limite_dinamico<0):
            raise ValueError('Limite inválido')
        self.modo=modo
        self.limite_dinamico=limite_dinamico
        self.memoria=Memoria(self.base)
        self._historico=[]
        self.perguntas={}
        self.dinamicas=[]
        self.bandeiras_historicas={}
        self.reconhecidas=set()
        self.finalizada_por_alerta=False
        preenchidos={id:valor for id,valor in (ficha or {}).items()
                     if valor is not None and not (isinstance(valor,dict) and valor.get('valor') is None
                                                  and not valor.get('nao_sei',False))}
        self.memoria.registrar(preenchidos,origem='ficha')
        self._ordem=[list(preenchidos)] if preenchidos else []

    @classmethod
    def restaurar(cls, base, *, modo='produtor', fatos, perguntas_dinamicas=(),
                  perguntas_feitas=None, bandeiras_reconhecidas=(),
                  finalizada_por_alerta=False, limite_dinamico=None,
                  correcoes=(), bandeiras_ativas=None, ordem_respostas=None):  # bandeiras_ativas: só compatibilidade, ignorado
        """Reconstrói dados persistidos diretamente, sem repetir o diálogo.

        A API decodifica suas colunas JSON e fornece os fatos por símbolo,
        ids dinâmicos em ordem e eventos de perguntas com o motivo original.
        Dados são validados como observações; não se exige que cada resposta
        antiga ainda seja a próxima pergunta após uma correção. As bandeiras
        travadas são derivadas reprocessando as respostas em ordem. Sem
        `ordem_respostas`, a ordem é derivada (ficha, telas, dinâmicas).
        """
        sessao=cls.__new__(cls)
        sessao._iniciar(base,modo,None,limite_dinamico)
        sessao.memoria.registrar(_racionais_do_snapshot(fatos, sessao.base.simbolos))
        dinamicas=list(perguntas_dinamicas)
        if len(dinamicas)!=len(set(dinamicas)) or any(id not in sessao.fatos for id in dinamicas):
            raise ValueError('Perguntas dinâmicas duplicadas ou sem resposta persistida')
        sessao.dinamicas=dinamicas
        perguntas=(list(perguntas_feitas.values()) if isinstance(perguntas_feitas,dict)
                   else list(perguntas_feitas or ()))
        historico=deepcopy(perguntas+list(correcoes))
        if historico and all('id' in e for e in historico):
            historico.sort(key=lambda e:e['id'])
        sessao.perguntas={}
        for e in historico:
            id=e.get('simbolo')
            if id not in sessao.base.simbolos or sessao.base.simbolos[id]['tipo'] not in ('pergunta','ficha'):
                raise ValueError('Evento persistido com símbolo inválido')
            if e.get('tipo')=='pergunta_feita':
                if id in sessao.perguntas or not e.get('motivo'):
                    raise ValueError('Pergunta persistida duplicada ou sem motivo')
            elif e.get('tipo')!='fato_adicionado' or not e.get('correcao'):
                raise ValueError('Somente perguntas e correções pertencem ao histórico')
            item=evento(sessao._historico,e['tipo'],**{k:v for k,v in e.items() if k not in ('id','tipo')})
            if item['tipo']=='pergunta_feita': sessao.perguntas[id]=item
        sessao._ordem=sessao._validar_ordem(ordem_respostas) if ordem_respostas is not None else sessao._ordem_derivada()
        sessao.reconhecidas=set(bandeiras_reconhecidas)
        sessao._calcular(reprocessar=True)
        if type(finalizada_por_alerta) is not bool:  # também vale para "ver resultado agora", sem bandeira
            raise ValueError('Encerramento por alerta inválido')
        sessao.finalizada_por_alerta=finalizada_por_alerta
        return sessao

    def exportar(self):
        """Snapshot JSON aceito por restaurar(base, **snapshot), sem banco."""
        from fractions import Fraction
        fatos={id:{'valor':str(f.valor) if isinstance(f.valor,Fraction) else f.valor,
                   'cf':str(f.cf),'origem':f.origem,'tela_id':f.tela_id} for id,f in self.fatos.items()}
        return deepcopy({'modo':self.modo,'fatos':fatos,'perguntas_dinamicas':self.dinamicas,
                         'perguntas_feitas':self.perguntas,'bandeiras_reconhecidas':sorted(self.reconhecidas),
                         'finalizada_por_alerta':self.finalizada_por_alerta,'limite_dinamico':self.limite_dinamico,
                         'correcoes':[e for e in self._historico if e.get('correcao')],
                         'ordem_respostas':self._ordem})

    @property
    def traco(self):
        """Histórico de perguntas/correções e somente o cálculo atual."""
        traco=deepcopy(self._historico)
        for e in self.resultado.traco:
            evento(traco,e['tipo'],**{k:v for k,v in e.items() if k not in ('id','tipo')})
        return traco

    @property
    def fatos(self): return dict(self.memoria.fatos)

    @property
    def resultado(self): return self.analise.resultado

    def _validar_ordem(self, ordem):
        if not isinstance(ordem,(list,tuple)) or not all(isinstance(l,(list,tuple)) for l in ordem):
            raise ValueError('Ordem das respostas inválida')
        ids=[id for lote in ordem for id in lote]
        if len(ids)!=len(set(ids)) or any(id not in self.memoria.fatos for id in ids):
            raise ValueError('Ordem das respostas com símbolos duplicados ou sem resposta persistida')
        return [list(l) for l in ordem if l]

    def _ordem_derivada(self):
        """Ordem aproximada: ficha, telas na ordem da base, perguntas dinâmicas."""
        fatos=self.memoria.fatos
        telas=[[id for id,f in fatos.items() if f.tela_id==t['id'] and f.origem!='ficha']
               for t in self.base.meta['triagem']]
        dinamicas=[[id] for id in self.dinamicas if id in fatos]
        usados={id for lote in telas+dinamicas for id in lote}
        return [lote for lote in [[id for id in fatos if id not in usados]]+telas+dinamicas if lote]

    def _registrar_ordem(self, ids):
        conhecidos={id for lote in self._ordem for id in lote}
        novos=[id for id in ids if id not in conhecidos]
        if novos: self._ordem.append(novos)

    def _lotes(self):
        """Respostas atuais, em lotes, na ordem real de entrada."""
        fatos=self.memoria.fatos
        conhecidos={id for lote in self._ordem for id in lote}
        lotes=[{id:fatos[id] for id in lote if id in fatos} for lote in self._ordem]
        soltos={id:f for id,f in fatos.items() if id not in conhecidos}
        if soltos:
            if lotes: lotes[0]={**soltos,**lotes[0]}
            else: lotes=[soltos]
        return [lote for lote in lotes if lote]

    def _reprocessar_bandeiras(self):
        """União das bandeiras de cada prefixo de lotes, na ordem de entrada."""
        historicas={}
        acumulado={}
        for lote in self._lotes():
            acumulado.update(lote)
            resultado=inferir(self.base,acumulado)
            for id in resultado.bandeiras:
                if id not in historicas: historicas[id]=deepcopy(como(resultado,'chamar_agora'))
        return historicas

    def _calcular(self, *, reprocessar=False):
        self.analise=analisar(self.base,self.memoria.fatos,self.modo)
        if reprocessar:
            self.bandeiras_historicas=self._reprocessar_bandeiras()
        else:
            for id in self.resultado.bandeiras:
                if id not in self.bandeiras_historicas:
                    self.bandeiras_historicas[id]=deepcopy(como(self.resultado,'chamar_agora'))
        self.reconhecidas.intersection_update(self.bandeiras_historicas)

    def _registrar_correcao(self, anteriores):
        for id,anterior in anteriores.items():
            evento(self._historico,'fato_adicionado',**dados_fato(self.memoria.fatos[id]),
                   correcao=True,anterior=para_json(dados_fato(anterior)))

    def _ids_tela(self,tela):
        if 'simbolos_por_modo' in tela:
            return list(tela['simbolos_por_modo'].get(self.modo,[]))
        return [id for id in tela['simbolos'] if not self.base.simbolos[id].get('pergunta')
                or self.base.simbolos[id]['pergunta'].get(self.modo)]

    def _telas_pendentes(self):
        return [t for t in self.base.meta['triagem'] if any(id not in self.memoria.fatos for id in self._ids_tela(t))]

    def _pergunta(self,id,origem,motivo,**extras):
        if id not in self.perguntas:
            pergunta=evento(self._historico,'pergunta_feita',simbolo=id,origem=origem,motivo=motivo,**extras)
            self.perguntas[id]=pergunta

    def _formatar_serve_a(self,regras_por_doenca):
        return [{'doenca':d,'nome':self.base.simbolos[d]['nome'],'gravidade':self.base.simbolos[d]['gravidade'],
                 'cf_atual':self.resultado.cfs[d],'regras':sorted(regras)}
                for d,regras in sorted(regras_por_doenca.items())]

    def _serve_a_triagem(self,id):
        regras_por_doenca={}
        for r in self.base.regras:
            d=r['entao']['simbolo']
            if self.base.simbolos[d]['tipo']=='doenca' and any(id in _fontes(c['simbolo'],self.base) for c in r['se']):
                regras_por_doenca.setdefault(d,set()).add(r['id'])
        return self._formatar_serve_a(regras_por_doenca)

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
                    if id not in self.perguntas:
                        self._pergunta(id,'triagem',f'Triagem obrigatória, tela {indice} de {len(self.base.meta["triagem"])}',
                                       tela_id=t['id'],serve_a=self._serve_a_triagem(id))
            else:
                id=self.analise.proxima; s=self.base.simbolos[id]; candidato=self.analise.candidatos[id]
                serve=self._formatar_serve_a(candidato['serve_a'])
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
            ids=[id for id in ids if self.memoria.fatos[id].origem!='ficha'] or ids  # tela só de ficha: correção explícita
        elif estado['proxima'] is None or estado['proxima']['id']!=tela_id or estado['proxima']['tipo']!='tela_triagem':
            raise ValueError('Tela não é a próxima ou já foi respondida')
        else:
            ids=estado['proxima']['simbolos']
        if resposta is None or resposta in ('nao_sei','não sei'):
            entradas={id:None for id in ids}
        elif t['selecao']=='multipla':
            if isinstance(resposta,dict):
                if set(resposta)!=set(ids) or any(type(v) is not bool for v in resposta.values()):
                    raise ValueError('Mapa de seleção múltipla inválido')
                entradas=resposta
            elif isinstance(resposta,list) and len(resposta)==len(set(resposta)) and set(resposta)<=set(ids):
                entradas={id:id in resposta for id in ids}
            else:
                raise ValueError('Seleção múltipla inválida')
        elif isinstance(resposta,dict):
            if set(resposta)!=set(ids): raise ValueError('Resposta não corresponde aos símbolos da tela')
            entradas=resposta
        elif len(ids)==1: entradas={ids[0]:resposta}
        else: raise ValueError('Informe os valores da tela por símbolo')
        anteriores={id:self.memoria.fatos[id] for id in ids} if corrigir else {}
        self.memoria.registrar(entradas,tela_id=tela_id)
        if corrigir: self._registrar_correcao(anteriores)
        else: self._registrar_ordem(entradas)
        self.finalizada_por_alerta=False
        self._calcular(reprocessar=corrigir)
        return self.estado()

    def responder(self,simbolo,valor,*,corrigir=False):
        if corrigir:
            if simbolo not in self.dinamicas: raise ValueError('Pergunta ainda não respondida')
        else:
            proxima=self.estado()['proxima']
            if not proxima or proxima['tipo']!='pergunta' or proxima['id']!=simbolo:
                raise ValueError('Pergunta não aplicável neste momento/modo')
        anteriores={simbolo:self.memoria.fatos[simbolo]} if corrigir else {}
        self.memoria.registrar({simbolo:valor})
        if corrigir: self._registrar_correcao(anteriores)
        if not corrigir: self.dinamicas.append(simbolo); self._registrar_ordem([simbolo])
        self.finalizada_por_alerta=False
        self._calcular(reprocessar=corrigir)
        return self.estado()

    def trocar_modo(self,modo):
        if modo not in MODOS: raise ValueError('Modo inválido')
        self.modo=modo
        self.finalizada_por_alerta=False
        self._calcular()
        return self.estado()

    def limite_efetivo(self):
        return limite_efetivo(self.base,self.modo,self.limite_dinamico)

    def acao_bandeira(self,acao):
        """``ver_parecer`` encerra a qualquer momento (com ou sem bandeira) e guarda o cálculo daquela hora;
        ``continuar`` reconhece a bandeira ou retoma uma sessão encerrada pelo usuário."""
        if acao not in ('continuar','ver_parecer') or (acao=='continuar' and not self.bandeiras_historicas
                                                         and not self.finalizada_por_alerta):
            raise ValueError('Ação de bandeira inválida')
        self.reconhecidas.update(self.bandeiras_historicas)
        self.finalizada_por_alerta=acao=='ver_parecer'
        return self.estado()

    def parecer(self):
        estado=self.estado()
        nao_verificadas=[]
        for regra in self.analise.viaveis.values() if estado['motivo_parada']=='limite' else ():
            if regra.get('classe')!='bandeira_vermelha' or regra['id'] in self.bandeiras_historicas:
                continue
            valores=[avaliar_condicao(c,self.resultado.fatos,self.base.simbolos) for c in regra['se']]
            if any(v==0 for v in valores) and all(v>=0 for v in valores):
                nao_verificadas.append(regra['id'])
        return montar_parecer(self.resultado,estado['motivo_parada'],estado['urgencia'],
                              sorted(self.bandeiras_historicas),sorted(nao_verificadas),self.analise.potenciais)

    def porque(self,simbolo):
        if simbolo not in self.perguntas: raise ValueError('Pergunta ainda não apresentada')
        return deepcopy(self.perguntas[simbolo])

    def como(self,simbolo):
        explicacao=como(self.resultado,simbolo)
        if simbolo=='chamar_agora': explicacao['bandeiras_historicas']=deepcopy(self.bandeiras_historicas)
        return explicacao
