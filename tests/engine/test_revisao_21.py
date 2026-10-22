"""Regressões dos contratos revistos em ce6874b (21/10/2026)."""
import ast
from copy import deepcopy
from fractions import Fraction as F
import json
from pathlib import Path
import unittest
from engine.sessao import Sessao
from engine.inferencia import inferir, agenda
from engine.modelos import Base
from engine.casos import executar_caso
from engine.parecer import percentual
from .apoio import base, simbolo, doenca, regra, condicao
from .test_sessao import base_triagem


def base_dinamica():
    return base([simbolo('x'),simbolo('y'),simbolo('z'),doenca()],
                [regra('x','d',0.5,condicao('x')),regra('y','d',0.5,condicao('y')),regra('z','d',0.5,condicao('z'))])


class RestauracaoTests(unittest.TestCase):
    def test_restauracao_nao_repete_respostas_com_ordem_ja_alterada_por_correcao(self):
        s=Sessao(base_dinamica())
        s.responder('x',True); s.responder('y',True)
        porque=deepcopy(s.porque('y'))
        s.responder('x',False,corrigir=True)
        self.assertTrue(hasattr(Sessao,'restaurar'),'Falta Sessao.restaurar para a API')
        restaurada=Sessao.restaurar(base_dinamica(),modo='produtor',fatos=s.fatos,
                                  perguntas_dinamicas=s.dinamicas,perguntas_feitas=s.perguntas)
        self.assertEqual(restaurada.fatos,s.fatos)
        self.assertEqual(restaurada.estado(),s.estado())
        self.assertEqual(restaurada.porque('y'),porque)
        self.assertEqual(restaurada.estado()['progresso']['dinamicas_respondidas'],2)

    def test_roundtrip_json_preserva_nao_sei_fatos_fracionarios_traco_e_pausa(self):
        s=Sessao(base_triagem(),ficha={'dias':F(1,2)})
        s.responder_triagem('multipla',['t2'])
        s.acao_bandeira('continuar')
        s.responder_triagem('multipla',['t1'],corrigir=True)
        s.responder_triagem('multipla',['t2'],corrigir=True)
        self.assertTrue(hasattr(s,'exportar'),'Falta exportação de estado restaurável')
        dados=json.loads(json.dumps(s.exportar()))
        r=Sessao.restaurar(base_triagem(),**dados)
        self.assertEqual(r.estado(),s.estado()); self.assertEqual(r.traco,s.traco)
        self.assertEqual(r.fatos,s.fatos)
        self.assertTrue(r.estado()['pausa'])

    def test_restauracao_preserva_encerramento_por_alerta_e_reconhecimento(self):
        s=Sessao(base_triagem(),ficha={'dias':1})
        s.responder_triagem('multipla',['t2']); s.acao_bandeira('ver_parecer')
        self.assertTrue(hasattr(s,'exportar'),'Falta exportação de estado restaurável')
        r=Sessao.restaurar(base_triagem(),**s.exportar())
        self.assertEqual(r.estado(),s.estado()); self.assertIsNone(r.estado()['proxima'])

    def test_restauracao_rejeita_contagem_duplicada_e_conclusao_injetada(self):
        self.assertTrue(hasattr(Sessao,'restaurar'),'Falta restauração validada')
        for fatos,ordem in [({'x':True},['x','x']),({'d':True},[])]:
            with self.assertRaises(ValueError):
                Sessao.restaurar(base_dinamica(),modo='produtor',fatos=fatos,
                                perguntas_dinamicas=ordem,perguntas_feitas={})


class BandeiraFichaTracoTests(unittest.TestCase):
    def test_correcao_remove_reconhecimento_e_bandeira_volta_a_pausar(self):
        s=Sessao(base_triagem(),ficha={'dias':1})
        s.responder_triagem('multipla',['t2']); s.acao_bandeira('continuar')
        s.responder_triagem('multipla',[],corrigir=True)
        self.assertEqual(s.estado()['bandeiras'],[])
        self.assertEqual(s.reconhecidas,set())
        s.responder_triagem('multipla',['t2'],corrigir=True)
        self.assertTrue(s.estado()['pausa'])

    def test_nova_resposta_nao_rebaixa_bandeira_ativada_por_derivado(self):
        b=base([simbolo('x'),simbolo('y'),simbolo('z','derivado'),doenca(),simbolo('chamar_agora','urgencia')],
               [regra('z1','z',0.8,condicao('x')),regra('z2','z',-0.9,condicao('y')),
                regra('d','d',0.9,condicao('y')),regra('bv','chamar_agora',0.99,condicao('z'),classe='bandeira_vermelha')])
        s=Sessao(b,ficha={'x':True}); s.acao_bandeira('continuar')
        s.responder('y',True)
        self.assertEqual(s.resultado.bandeiras,())
        self.assertEqual(s.estado()['urgencia'],'chamar_agora')

    def test_ficha_null_ou_valor_null_nao_e_resposta_mas_nao_sei_explicito_e(self):
        for entrada in [None,{'valor':None}]:
            s=Sessao(base_triagem(),ficha={'dias':entrada})
            self.assertEqual(s.estado()['proxima']['id'],'ficha')
            self.assertNotIn('dias',s.fatos)
        s=Sessao(base_triagem(),ficha={'dias':'nao_sei'})
        self.assertEqual(s.estado()['proxima']['id'],'multipla')

    def test_traco_contem_apenas_ultimo_calculo_e_historico_de_correcao(self):
        s=Sessao(base_dinamica()); s.responder('x',True); s.responder('y',False)
        s.responder('x',False,corrigir=True)
        traco=s.traco
        observados=[e for e in traco if e['tipo']=='fato_adicionado' and e.get('origem')!='regra' and not e.get('correcao')]
        self.assertEqual(len(observados),2)
        corrigidos=[e for e in traco if e.get('correcao')]
        self.assertEqual(len(corrigidos),1)
        self.assertEqual(corrigidos[0]['anterior']['valor'],True)
        self.assertEqual(corrigidos[0]['valor'],False)
        self.assertEqual(len({e['id'] for e in traco}),len(traco))
        self.assertEqual(s.traco,traco)

    def test_conclusoes_emitem_fato_adicionado_origem_regra(self):
        r=inferir(base_dinamica(),{'x':True})
        eventos=[e for e in r.traco if e['tipo']=='fato_adicionado' and e.get('origem')=='regra']
        self.assertEqual(len(eventos),1); self.assertEqual(eventos[0]['simbolo'],'d')

    def test_multipla_aceita_mapa_booleano_sem_apagar_ficha(self):
        s=Sessao(base_triagem(),ficha={'dias':1,'t1':True})
        try:
            s.responder_triagem('multipla',{'t2':False})
        except ValueError as erro:
            self.fail(f'Mapa booleano válido foi rejeitado: {erro}')
        self.assertEqual(s.fatos['t1'].origem,'ficha'); self.assertEqual(s.fatos['t2'].cf,-1)
        with self.assertRaises(ValueError): s.responder_triagem('multipla',{'t1':1,'t2':False},corrigir=True)


class ParecerCasosTests(unittest.TestCase):
    def test_percentuais_positivos_neutros_nao_sao_zerados(self):
        for cf,esperado in [(F(3,20),15),(F(1,5),20),(F(1,200),1),(-F(1,5),0)]:
            self.assertEqual(percentual(cf),esperado)

    def test_blocos_leem_cortes_da_base_e_ids_da_api(self):
        b=base([simbolo('x'),doenca()],[regra('r','d',0.6,condicao('x'))])
        b['meta']['limiares']={'bloco_principal':0.7,'bloco_diferencial':0.3}
        p=Sessao(b,ficha={'x':True}).parecer()
        self.assertEqual([b['id'] for b in p['blocos']],['hipoteses_principais','diagnostico_diferencial','pouco_provavel'])
        self.assertEqual(p['blocos'][1]['itens'][0]['doenca'],'d')
        b['meta']['limiares']['bloco_principal']=0.6
        self.assertEqual(Sessao(b,ficha={'x':True}).parecer()['blocos'][0]['itens'][0]['doenca'],'d')

    def test_prioridades_padrao_preservam_override_zero(self):
        b=base([simbolo('x'),doenca(),simbolo('observar','urgencia'),simbolo('chamar_agora','urgencia')],
               [regra('d','d',0.8,condicao('x')),regra('a_urg','observar',0.9,condicao('x'),classe='urgencia'),
                regra('z_bv','chamar_agora',0.9,condicao('x'),classe='bandeira_vermelha')])
        for r in b['regras']: r.pop('prioridade')
        normal=Base.de_dict(b)
        self.assertEqual([r.get('prioridade') for r in normal.regras],[10,50,100])
        self.assertEqual([r['id'] for r in agenda(normal)],['d','z_bv','a_urg'])
        b['regras'][2]['prioridade']=0
        self.assertEqual(Base.de_dict(b).regras[2]['prioridade'],0)

    def test_sem_hipotese_aberta_informa_sem_potencial(self):
        b=base([simbolo('x'),doenca()],[regra('r','d',-0.8,condicao('x'))])
        self.assertEqual(Sessao(b,ficha={'x':True}).estado()['motivo_parada'],'sem_potencial')

    def test_executor_confere_inconclusivas_e_pausa_ocorrida(self):
        b=base_dinamica()
        c={'modo':'produtor','ficha':{'x':True},'limite_dinamico':0,
           'esperado':{'inconclusivas':['d'],'alerta.pausa':False}}
        r=executar_caso(b,c); self.assertEqual(r['status'],'passou',r)
        c={'modo':'produtor','ficha':{'dias':1},'triagem':{'multipla':['t2']},'esperado':{'alerta':{'pausa':True}}}
        r=executar_caso(base_triagem(),c); self.assertEqual(r['status'],'passou',r)
        c['esperado']['alerta']['pausa']=False
        self.assertEqual(executar_caso(base_triagem(),c)['status'],'falhou')

    def test_bandeiras_nao_verificadas_so_viaveis_no_limite(self):
        vet=simbolo('vet'); vet['pergunta'].pop('produtor')
        b=base([simbolo('x'),simbolo('y'),vet,doenca(),simbolo('chamar_agora','urgencia')],
               [regra('d','d',0.5,condicao('x')),regra('bv','chamar_agora',0.9,condicao('x'),condicao('y'),classe='bandeira_vermelha'),
                regra('vet','chamar_agora',0.9,condicao('x'),condicao('vet'),classe='bandeira_vermelha')])
        s=Sessao(b,ficha={'x':True})
        self.assertEqual(s.parecer()['bandeiras_nao_verificadas'],[])
        limitado=Sessao(b,ficha={'x':True},limite_dinamico=0)
        self.assertEqual(limitado.parecer()['bandeiras_nao_verificadas'],['bv'])

    def test_engine_independe_de_api_web_banco_e_kb(self):
        proibidos={'api','web','sqlite3','kb'}
        for arquivo in Path('engine').glob('*.py'):
            arvore=ast.parse(arquivo.read_text(encoding='utf-8'))
            for no in ast.walk(arvore):
                if isinstance(no,ast.Import): nomes=[a.name.split('.')[0] for a in no.names]
                elif isinstance(no,ast.ImportFrom) and no.level==0: nomes=[(no.module or '').split('.')[0]]
                else: continue
                self.assertFalse(proibidos.intersection(nomes),arquivo)
