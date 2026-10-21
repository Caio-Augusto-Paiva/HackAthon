from copy import deepcopy
from fractions import Fraction as F
import json
import unittest
from .apoio import modulo, base, simbolo, doenca, regra, condicao


def base_triagem():
    # Seis telas; sinais e doenças artificiais, sem significado clínico.
    ss=[simbolo('dias','ficha','numerico')]+[simbolo(f't{i}') for i in range(1,7)]
    ss += [simbolo('dinamica'),doenca(),simbolo('chamar_agora','urgencia')]
    telas=[{'id':'ficha','selecao':'unica','simbolos':['dias'],'texto':{'produtor':'Dias?','veterinario':'Dias?'}},
           {'id':'multipla','selecao':'multipla','simbolos':['t1','t2'],'texto':{'produtor':'Sinais?','veterinario':'Sinais?'}}]
    telas += [{'id':f'tela{i}','selecao':'unica','simbolos':[f't{i}'],'texto':{'produtor':f'T{i}?','veterinario':f'T{i}?'}} for i in range(3,7)]
    return base(ss,[regra('d','d',0.9,condicao('dinamica')),regra('bv','chamar_agora',0.9,condicao('t2'),classe='bandeira_vermelha')],telas)


class SessaoTests(unittest.TestCase):
    def criar(self,b=None,**kwargs): return modulo('sessao').Sessao(b or base_triagem(),**kwargs)

    def preencher(self,s,multipla=()):
        while s.estado()['fase']=='triagem':
            estado=s.estado()
            if estado['pausa']: s.acao_bandeira('continuar'); continue
            tela=estado['proxima']['id']
            s.responder_triagem(tela,list(multipla) if tela=='multipla' else 'nao_sei')

    def test_triagem_seis_telas_ficha_auto_e_multipla(self):
        s=self.criar(ficha={'dias':10})
        self.assertEqual(s.estado()['proxima']['id'],'multipla')
        s.responder_triagem('multipla',['t1'])
        self.assertEqual(s.fatos['t1'].cf,1); self.assertEqual(s.fatos['t2'].cf,-1)
        self.assertEqual(s.estado()['proxima']['id'],'tela3')
        self.assertEqual(s.estado()['progresso']['dinamicas_respondidas'],0)
        self.preencher(s)
        self.assertEqual(s.estado()['fase'],'dinamica')
        self.assertEqual(s.estado()['progresso']['triagem_respondida'],6)

    def test_nao_sei_multipla_grava_zero_e_nao_trava(self):
        s=self.criar(ficha={'dias':1})
        s.responder_triagem('multipla','nao_sei')
        self.assertEqual([s.fatos[x].cf for x in ('t1','t2')],[0,0])
        self.preencher(s)
        s.responder('dinamica','nao_sei')
        self.assertEqual(s.estado()['fase'],'encerrada')
        self.assertEqual(s.estado()['motivo_parada'],'sem_perguntas')

    def test_triagem_parcial_preserva_fato_preexistente_nao_exibido(self):
        for resposta in [['t2'],'nao_sei']:
            s=self.criar(ficha={'dias':1,'t1':True})
            self.assertEqual(s.estado()['proxima']['simbolos'],['t2'])
            s.responder_triagem('multipla',resposta)
            self.assertEqual(s.fatos['t1'].valor,True)
            self.assertEqual(s.fatos['t1'].origem,'ficha')

    def test_confirmacao_nao_pula_triagem(self):
        b=base_triagem(); b['regras'][0]['se']=[condicao('t1')]
        s=self.criar(b,ficha={'dias':10}); s.responder_triagem('multipla',['t1'])
        self.assertEqual(s.resultado.cfs['d'],F(9,10))
        self.assertEqual(s.estado()['fase'],'triagem')

    def test_bandeira_pausa_so_produtor_e_correcao_remove_bandeira(self):
        s=self.criar(ficha={'dias':10}); s.responder_triagem('multipla',['t2'])
        self.assertTrue(s.estado()['pausa']); self.assertEqual(s.estado()['urgencia'],'chamar_agora')
        s.acao_bandeira('continuar')
        s.responder_triagem('multipla',[],corrigir=True)
        self.assertFalse(s.estado()['pausa']); self.assertEqual(s.estado()['urgencia'],'sem_problema')
        self.assertEqual(s.estado()['bandeiras'],[])
        v=self.criar(modo='veterinario',ficha={'dias':10}); v.responder_triagem('multipla',['t2'])
        self.assertFalse(v.estado()['pausa']); self.assertEqual(v.estado()['urgencia'],'chamar_agora')

    def test_ver_parecer_apos_alerta_encerra_sem_exigir_resto_triagem(self):
        s=self.criar(ficha={'dias':10}); s.responder_triagem('multipla',['t2'])
        s.acao_bandeira('ver_parecer')
        self.assertEqual(s.estado()['fase'],'encerrada'); self.assertIsNone(s.estado()['proxima'])

    def test_correcao_nao_duplica_contagem_e_porque_original_e_preservado(self):
        s=self.criar(ficha={'dias':1}); self.preencher(s)
        motivo=deepcopy(s.porque('dinamica'))
        s.responder('dinamica',True)
        self.assertEqual(s.estado()['motivo_parada'],'confirmacao')
        s.responder('dinamica',False,corrigir=True)
        self.assertEqual(s.resultado.cfs['d'],0)
        self.assertEqual(s.estado()['progresso']['dinamicas_respondidas'],1)
        self.assertEqual(s.porque('dinamica'),motivo)

    def test_troca_modo_preserva_observacoes_e_pergunta_novo_exame(self):
        p=simbolo('prod'); p['pergunta']={'produtor':'Sinal?'}
        v=simbolo('vet',dominio='numerico'); v['pergunta']={'veterinario':'Temperatura?'}
        t={'id':'termico','selecao':'unica','simbolos':['prod','vet'],'texto':{'produtor':'Sinal?','veterinario':'Temperatura?'}}
        b=base([p,v,simbolo('extra'),doenca()], [regra('p','d',0.4,condicao('prod')),regra('v','d',0.9,condicao('vet',39,'>')),regra('e','d',0.5,condicao('extra'))],[t])
        s=self.criar(b); s.responder_triagem('termico',{'prod':True})
        s.trocar_modo('veterinario')
        self.assertIn('prod',s.fatos)
        self.assertEqual(s.estado()['proxima']['simbolos'],['vet'])
        s.responder_triagem('termico',{'vet':40})
        self.assertEqual(s.resultado.cfs['d'],F(47,50))
        s.trocar_modo('produtor'); self.assertIn('vet',s.fatos)

    def test_limite_dinamico_e_independente_da_triagem(self):
        s=self.criar(ficha={'dias':1},limite_dinamico=1); self.preencher(s)
        self.assertEqual(s.estado()['fase'],'dinamica')
        s.responder('dinamica','nao_sei')
        self.assertEqual(s.estado()['motivo_parada'],'limite')

    def test_resposta_invalida_e_transacao_atomica(self):
        s=self.criar(ficha={'dias':1}); antes=deepcopy(s.fatos)
        with self.assertRaises(ValueError): s.responder_triagem('multipla',['t1','nao_existe'])
        self.assertEqual(s.fatos,antes)
        with self.assertRaises(ValueError): s.responder('dinamica',True)
        s.responder_triagem('multipla',[])
        with self.assertRaises(ValueError): s.responder_triagem('multipla',[])

    def test_estado_e_traco_repetidos_sao_deterministas_e_json(self):
        a=self.criar(ficha={'dias':1}); b=self.criar(ficha={'dias':1})
        self.preencher(a); self.preencher(b)
        self.assertEqual(a.estado(),a.estado()); self.assertEqual(a.traco,b.traco)
        self.assertEqual({e['tipo'] for e in a.traco},{'pergunta_feita','fato_adicionado'})
        a.responder('dinamica',True)
        self.assertEqual({e['tipo'] for e in a.traco},{'pergunta_feita','fato_adicionado','regra_disparada','cf_combinado'})
        json.dumps(a.estado(),allow_nan=False); json.dumps(a.parecer(),allow_nan=False)

    def test_como_percorre_derivado_e_origem_importada(self):
        b=base([simbolo('x'),simbolo('z','derivado'),doenca()],[regra('der','z',0.9,condicao('x')),regra('d','d',0.8,condicao('z'))])
        s=self.criar(b,ficha={'x':{'valor':True,'origem':'importacao'}})
        como=s.como('d')
        self.assertEqual(como['evidencias'][0]['entradas'][0]['evidencias'][0]['regra_id'],'der')
        self.assertEqual(como['evidencias'][0]['entradas'][0]['evidencias'][0]['entradas'][0]['origem'],'importacao')


class ParecerTests(unittest.TestCase):
    def test_oito_doencas_ordem_percentuais_situacao_e_blocos(self):
        ss=[]; rs=[]; fatos={}
        pesos=[0.8,0.5,0.499,0.205,0.2,-0.2,-0.201,0]
        for i,peso in enumerate(pesos):
            ss += [simbolo(f'x{i}'),doenca(f'd{i}')]
            rs += [regra(f'r{i}',f'd{i}',peso,condicao(f'x{i}'))]; fatos[f'x{i}']=True
        s=modulo('sessao').Sessao(base(ss,rs),ficha=fatos)
        p=s.parecer()
        itens=[item for bloco in p['blocos'] for item in bloco['itens']]
        self.assertEqual(len(itens),8)
        self.assertEqual([x['doenca'] for x in itens],['d0','d1','d2','d3','d4','d7','d5','d6'])
        self.assertEqual([x['percentual'] for x in itens],[80,50,50,21,20,0,0,0])
        self.assertEqual([x['situacao'] for x in itens[-3:]],['sem_evidencia','sem_evidencia','descartada'])
        self.assertEqual([len(x['itens']) for x in p['blocos']],[2,2,4])
        self.assertIn('não probabilidade',p['aviso'])

    def test_desempate_id_fallback_urgencia_e_inconclusivas(self):
        b=base([simbolo('x'),doenca('b'),doenca('a')],[regra('b','b',0.4,condicao('x')),regra('a','a',0.4,condicao('x'))])
        s=modulo('sessao').Sessao(b,ficha={'x':True},limite_dinamico=0)
        p=s.parecer()
        self.assertEqual(p['urgencia'],'observar'); self.assertEqual(p['inconclusivas'],['a','b'])
        self.assertEqual([x['doenca'] for x in p['blocos'][1]['itens']],['a','b'])


class CasosTests(unittest.TestCase):
    def test_executor_ignora_resposta_nao_pedida_e_nao_sei_ausente(self):
        b=base([simbolo('x'),simbolo('y'),doenca()],[regra('r','d',0.9,condicao('x'))])
        executar=modulo('casos').executar_caso
        c={'id':'c','modo':'produtor','respostas':{'x':True,'y':True},'esperado':{'top1':'d','urgencia':'observar','faixas':{'d':[90,90]},'motivo_parada':'confirmacao'}}
        r=executar(b,c)
        self.assertEqual(r['status'],'passou'); self.assertNotIn('y',r['respondidas'])
        c['respostas']={}; c['esperado']={'motivo_parada':'sem_perguntas','faixas':{'d':[0,0]}}
        self.assertEqual(executar(b,c)['status'],'passou')

    def test_executor_triagem_bandeira_continuacao_e_falhas(self):
        c={'id':'c','modo':'produtor','ficha':{'dias':1},'triagem':{'multipla':['t2']},'respostas':{},
           'continuacao':{'modo':'veterinario','respostas':{}},'esperado':{'urgencia':'chamar_agora','bandeira':'bv'}}
        executar=modulo('casos').executar_caso
        self.assertEqual(executar(base_triagem(),c)['status'],'passou')
        c['esperado']['urgencia']='sem_problema'
        self.assertEqual(executar(base_triagem(),c)['status'],'falhou')
        c['modo']='invalido'; self.assertEqual(executar(base_triagem(),c)['status'],'erro')
