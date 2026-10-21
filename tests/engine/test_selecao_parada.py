from fractions import Fraction as F
from itertools import product
import unittest
from .apoio import modulo, base, simbolo, doenca, regra, condicao


class SelecaoTests(unittest.TestCase):
    def analisar(self,b,f=None,modo='produtor'):
        return modulo('selecao').analisar(b,f or {},modo)

    def test_regra_morta_e_exame_exclusivo_nao_selecionam(self):
        vet=simbolo('vet'); vet['pergunta'].pop('produtor')
        b=base([simbolo('x'),simbolo('morta'),simbolo('viva'),vet,doenca()],
               [regra('m','d',0.9,condicao('x'),condicao('morta')),
                regra('v','d',0.7,condicao('viva')),regra('vet','d',0.99,condicao('vet'),condicao('morta'))])
        a=self.analisar(b,{'x':False})
        self.assertEqual(a.proxima,'viva')
        self.assertEqual(set(a.viaveis),{'v'})
        self.assertNotIn('vet',a.candidatos)

    def test_vet_respondido_continua_valendo_no_produtor(self):
        vet=simbolo('vet'); vet['pergunta'].pop('produtor')
        b=base([vet,simbolo('x'),doenca()],[regra('r','d',0.8,condicao('vet'),condicao('x'))])
        self.assertEqual(self.analisar(b,{'vet':True}).proxima,'x')

    def test_peso_propagado_por_derivado_e_desempate_gravidade(self):
        b=base([simbolo('x'),simbolo('y'),simbolo('z','derivado'),doenca('a','baixa'),doenca('b','alta')],
               [regra('der','z',0.9,condicao('x')),regra('a','a',0.8,condicao('z')),
                regra('b','b',0.72,condicao('y'))])
        a=self.analisar(b)
        self.assertEqual(a.candidatos['x']['peso'],F(18,25))
        self.assertEqual(a.proxima,'y')
        b['simbolos'][-1]['gravidade']='baixa'
        self.assertEqual(self.analisar(b).proxima,'x')

    def test_pergunta_compartilhada_soma_pesos_hipoteses(self):
        b=base([simbolo('x'),simbolo('y'),doenca('a'),doenca('b')],
               [regra('r1','a',0.6,condicao('x')),regra('r2','b',0.6,condicao('x')),regra('r3','b',0.9,condicao('y'))])
        a=self.analisar(b)
        self.assertEqual(a.proxima,'x'); self.assertEqual(a.candidatos['x']['peso'],F(6,5))

    def test_nao_sei_nao_pergunta_de_novo_e_conjuncao_impossivel(self):
        b=base([simbolo('x',dominio='numerico'),simbolo('y'),doenca()],
               [regra('impossivel','d',0.9,condicao('x',10,'>'),condicao('x',2,'<')),
                regra('y','d',0.8,condicao('y'))])
        self.assertEqual(self.analisar(b).proxima,'y')
        self.assertIsNone(self.analisar(b,{'y':'nao_sei'}).proxima)

    def test_potencial_nao_conta_duas_vezes_regra_ja_disparada(self):
        b=base([simbolo('x'),doenca()],[regra('r','d',0.5,condicao('x'))])
        self.assertEqual(self.analisar(b,{'x':True}).potenciais['d'],F(1,2))

    def test_derivado_correlacionado_nao_torna_conjuncao_impossivel_viavel(self):
        b=base([simbolo('x'),simbolo('z','derivado'),doenca()],
               [regra('z','z',0.9,condicao('x')),regra('d','d',0.9,condicao('x',False),condicao('z'))])
        a=self.analisar(b)
        self.assertNotIn('d',a.viaveis)
        self.assertEqual(a.potenciais['d'],0)
        self.assertIsNone(a.proxima)

    def test_potencial_limita_todas_respostas_inclusive_derivado_negado(self):
        b=base([simbolo('x'),simbolo('y'),simbolo('z','derivado'),doenca()],
               [regra('pos','z',0.8,condicao('x')),regra('neg','z',-0.9,condicao('y')),
                regra('dpos','d',0.7,condicao('z')),regra('dneg','d',0.8,condicao('z',False))])
        inferir=modulo('inferencia').inferir
        for parcial in [{},{'x':True},{'x':False},{'y':True}]:
            limite=self.analisar(b,parcial).potenciais['d']
            for x,y in product([True,False,'nao_sei'],repeat=2):
                fatos={'x':x,'y':y,**parcial}
                self.assertGreaterEqual(limite,inferir(b,fatos).cfs['d'])

    def test_limiares_abertura_excluem_descartadas_e_confirmadas(self):
        b=base([simbolo('x'),simbolo('y'),doenca()],[regra('r','d',0.8,condicao('x')),regra('s','d',0.4,condicao('y'))])
        self.assertEqual(self.analisar(b,{'x':True}).abertas,())
        b['regras'][0]['entao']['cf']=-0.2
        self.assertEqual(self.analisar(b,{'x':True}).abertas,())


class ParadaTests(unittest.TestCase):
    def parar(self,b,f=None,triagem=True,contagem=0,modo='produtor',limite=None):
        a=modulo('selecao').analisar(b,f or {},modo)
        return modulo('parada').motivo_parada(a,triagem,contagem,limite)

    def duas(self,peso=0.5):
        return base([simbolo('x'),simbolo('y'),simbolo('z'),doenca('a'),doenca('b')],
                    [regra('a','a',0.85,condicao('x')),regra('b','b',0.5,condicao('y')),regra('c','b',peso,condicao('z'))])

    def test_triagem_incompleta_nunca_encerra(self):
        self.assertIsNone(self.parar(self.duas(),{'x':True},triagem=False,contagem=99))

    def test_lider_e_concorrente_potencial_alto_ou_baixo(self):
        self.assertIsNone(self.parar(self.duas(),{'x':True,'y':True}))
        self.assertEqual(self.parar(self.duas(0.2),{'x':True,'y':True}),'confirmacao')

    def test_comorbidade_confirmada_nao_se_bloqueia(self):
        self.assertEqual(self.parar(self.duas(0.8),{'x':True,'y':True,'z':True}),'confirmacao')

    def test_bandeira_parcial_bloqueia_confirmacao(self):
        b=self.duas(0.1)
        b['simbolos'] += [simbolo('chamar_agora','urgencia')]
        b['regras'] += [regra('bv','chamar_agora',0.9,condicao('x'),condicao('z'),classe='bandeira_vermelha')]
        self.assertIsNone(self.parar(b,{'x':True,'y':True}))

    def test_bandeira_parcial_ganha_pergunta_mesmo_sem_hipotese_aberta(self):
        b=base([simbolo('x'),simbolo('y'),doenca(),simbolo('chamar_agora','urgencia')],
               [regra('d','d',0.9,condicao('x')),regra('bv','chamar_agora',0.9,condicao('x'),condicao('y'),classe='bandeira_vermelha')])
        a=modulo('selecao').analisar(b,{'x':True},'produtor')
        self.assertEqual(a.proxima,'y')
        self.assertIsNone(modulo('parada').motivo_parada(a,True,0))

    def test_exclusiva_vet_nao_bloqueia_confirmacao_no_produtor(self):
        b=self.duas(); b['simbolos'][2]['pergunta'].pop('produtor')
        self.assertEqual(self.parar(b,{'x':True,'y':True}),'confirmacao')

    def test_baixa_confianca_continua_se_ha_potencial(self):
        b=base([simbolo('x'),simbolo('y'),doenca()],
               [regra('atual','d',0.3,condicao('x')),regra('futura','d',0.6,condicao('y'))])
        self.assertIsNone(self.parar(b,{'x':True}))

    def test_limite_e_sem_perguntas_sem_potencial(self):
        b=base([simbolo('x'),doenca()],[regra('r','d',0.8,condicao('x'))])
        self.assertEqual(self.parar(b,contagem=12),'limite')
        self.assertEqual(self.parar(b,contagem=3,limite=3),'limite')
        self.assertEqual(self.parar(b,{'x':'nao_sei'}),'sem_perguntas')
        b['regras'][0]['entao']['cf']=0.4
        self.assertEqual(self.parar(b),'sem_potencial')
