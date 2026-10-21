from fractions import Fraction as F
import unittest
from .apoio import modulo, base, simbolo, doenca, regra, condicao


class InferenciaTests(unittest.TestCase):
    def inferir(self,b,f): return modulo('inferencia').inferir(b,f)

    def test_premissa_minima_e_limiar_estrito(self):
        b=base([simbolo('x'),simbolo('y'),doenca()], [regra('r','d',0.8,condicao('x'),condicao('y'))])
        for cf,esperado in [(0.2,0),(0.21,F(21,125)),(0.5,F(2,5))]:
            resultado=self.inferir(b,{'x':True,'y':{'valor':True,'cf':cf}})
            self.assertEqual(resultado.cfs['d'],esperado)

    def test_camadas_agenda_e_trace_determinista(self):
        b=base([simbolo('x'),simbolo('z','derivado'),doenca(),simbolo('observar','urgencia')],
               [regra('a_urg','observar',0.9,condicao('d',cf_minimo=0.5),classe='urgencia',prioridade=100),
                regra('a_d','d',0.8,condicao('z')),regra('z_der','z',0.9,condicao('x'))])
        r=self.inferir(b,{'x':True})
        self.assertEqual(r.cfs['d'],F(18,25))
        self.assertEqual([x['id'] for x in r.disparadas],['z_der','a_d','a_urg'])
        self.assertEqual(r.urgencia,'observar')
        self.assertEqual({e['tipo'] for e in r.traco},{'fato_adicionado','regra_disparada','cf_combinado'})
        b['regras'].reverse()
        self.assertEqual(self.inferir(b,{'x':True}).traco,r.traco)

    def test_agenda_prioridade_especificidade_id(self):
        b=base([simbolo('x'),simbolo('y'),doenca()],
               [regra('z','d',0.1,condicao('x'),prioridade=2),
                regra('a','d',0.1,condicao('x')),
                regra('b','d',0.1,condicao('x'),condicao('y'))])
        self.assertEqual([r['id'] for r in self.inferir(b,{'x':True,'y':True}).disparadas],['z','b','a'])

    def test_redundancia_max_e_negacao_derivada(self):
        b=base([simbolo('x'),simbolo('y'),simbolo('z','derivado',combinacao='max'),doenca()],
               [regra('r1','z',0.9,condicao('x')),regra('r2','z',0.9,condicao('y')),regra('r3','d',0.8,condicao('z'))])
        self.assertEqual(self.inferir(b,{'x':True,'y':True}).cfs['z'],F(9,10))
        b['simbolos'][2]['combinacao']='mycin'; b['regras'][0]['entao']['cf']=-0.9
        b['regras'][2]['se'][0]['valor']=False
        self.assertEqual(self.inferir(b,{'x':True,'y':False}).cfs['d'],F(18,25))

    def test_corrigir_recalcula_sem_duplicar_evidencia(self):
        b=base([simbolo('x'),doenca()],[regra('r','d',0.8,condicao('x'))])
        self.assertEqual(self.inferir(b,{'x':True}).cfs['d'],F(4,5))
        self.assertEqual(self.inferir(b,{'x':False}).cfs['d'],0)
        self.assertEqual(self.inferir(b,{'x':True}).cfs['d'],F(4,5))

    def test_negativos_e_guardas_urgencia(self):
        b=base([simbolo('x'),simbolo('y'),doenca(),simbolo('chamar_agora','urgencia')],
               [regra('r1','d',0.5,condicao('x')),regra('r2','d',-0.8,condicao('y')),
                regra('u','chamar_agora',0.9,condicao('d',cf_minimo=0.5),classe='urgencia')])
        self.assertEqual(self.inferir(b,{'x':True}).urgencia,'chamar_agora')
        self.assertEqual(self.inferir(b,{'x':True,'y':True}).cfs['d'],-F(3,5))
        self.assertEqual(self.inferir(b,{'x':True,'y':True}).urgencia,'sem_problema')

    def test_bandeira_independe_da_doenca_e_mantem_mais_urgente(self):
        b=base([simbolo('x'),doenca(),simbolo('chamar_agora','urgencia'),simbolo('observar','urgencia')],
               [regra('bv','chamar_agora',0.1,condicao('x'),classe='bandeira_vermelha'),
                regra('u','observar',0.9,condicao('x'),classe='urgencia')])
        r=self.inferir(b,{'x':True})
        self.assertEqual(r.urgencia,'chamar_agora'); self.assertEqual(r.bandeiras,('bv',))
        self.assertEqual(r.cfs['d'],0)

    def test_rejeita_injecao_de_conclusao_e_numero_nao_finito(self):
        b=base([simbolo('x',dominio='numerico'),doenca()],[regra('r','d',0.8,condicao('x',2,'>'))])
        for fatos in [{'d':True},{'x':float('nan')},{'x':True},{'ausente':1}]:
            with self.assertRaises((ValueError,KeyError)): self.inferir(b,fatos)
