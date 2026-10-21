"""Bandeiras travadas dependem só das respostas finais e da ordem em que entraram."""
import json
import unittest
from unittest.mock import patch

from engine.sessao import Sessao
from .apoio import base, simbolo, doenca, regra, condicao


def regras_sonda():
    return [regra('z1','z',0.8,condicao('x')),regra('z2','z',-0.9,condicao('y')),
            regra('dy','d',0.4,condicao('y')),regra('dw','d',0.4,condicao('w')),
            regra('bv','chamar_agora',0.99,condicao('z'),classe='bandeira_vermelha')]


def base_sonda():
    return base([simbolo('x','ficha'),simbolo('y'),simbolo('w'),simbolo('z','derivado'),doenca(),
                 simbolo('chamar_agora','urgencia')],regras_sonda())


def sessao_sonda(y,corrigir_para=None):
    s=Sessao(base_sonda(),ficha={'x':True})
    s.acao_bandeira('continuar')
    s.responder('w',True)
    s.responder('y',y)
    if corrigir_para is not None: s.responder('y',corrigir_para,corrigir=True)
    return s


class ReprocessamentoTests(unittest.TestCase):
    def test_mesmas_respostas_finais_dao_mesma_bandeira(self):
        for nome,s in (('direto',sessao_sonda(True)),('falso_corrigido',sessao_sonda(False,True)),
                       ('mesmo_valor',sessao_sonda(True,True))):
            with self.subTest(nome):
                self.assertEqual(s.estado()['urgencia'],'chamar_agora')
                self.assertEqual(s.estado()['bandeiras'],['bv'])

    def test_corrigir_gatilho_remove_bandeira(self):
        b=base([simbolo('x'),simbolo('y'),simbolo('w'),simbolo('z','derivado'),doenca(),
                simbolo('chamar_agora','urgencia')],
               regras_sonda()+[regra('dx','d',0.4,condicao('x'))])
        s=Sessao(b)
        s.responder('w',True)
        s.responder('x',True)
        self.assertEqual(s.estado()['bandeiras'],['bv'])
        s.acao_bandeira('continuar')
        s.responder('y',True)
        s.responder('x',False,corrigir=True)
        self.assertNotIn('bv',s.estado()['bandeiras'])
        self.assertNotEqual(s.estado()['urgencia'],'chamar_agora')

    def test_correcao_parcial_de_tela_multipla_mantem_bandeira(self):
        b=base([simbolo('a'),simbolo('b'),simbolo('y'),simbolo('w'),simbolo('z','derivado'),doenca(),
                simbolo('chamar_agora','urgencia')],
               [regra('z1','z',0.8,condicao('a')),regra('z2','z',-0.9,condicao('y')),
                regra('dy','d',0.4,condicao('y')),regra('dw','d',0.4,condicao('w')),
                regra('bv','chamar_agora',0.99,condicao('z'),classe='bandeira_vermelha')],
               triagem=[{'id':'T','selecao':'multipla','simbolos':['a','b']}])
        s=Sessao(b)
        s.responder_triagem('T',['a'])
        self.assertEqual(s.estado()['bandeiras'],['bv'])
        s.acao_bandeira('continuar')
        s.responder('w',True)
        s.responder('y',True)
        self.assertEqual(s.resultado.bandeiras,())
        s.responder_triagem('T',['a','b'],corrigir=True)
        self.assertEqual(s.estado()['bandeiras'],['bv'])
        self.assertEqual(s.estado()['urgencia'],'chamar_agora')

    def test_reprocessamento_independe_do_historico_de_edicao(self):
        direto=Sessao(base_sonda(),ficha={'x':True})
        direto.acao_bandeira('continuar')
        direto.responder('w',True); direto.responder('y',True)
        editada=Sessao(base_sonda(),ficha={'x':True})
        editada.acao_bandeira('continuar')
        editada.responder('w',True); editada.responder('y',False)
        editada.responder('w',False,corrigir=True); editada.responder('y',True,corrigir=True)
        editada.responder('w',True,corrigir=True)
        for campo in ('urgencia','bandeiras','pausa','fase'):
            self.assertEqual(editada.estado()[campo],direto.estado()[campo],campo)

    def test_restaurar_deriva_bandeiras_sem_bandeiras_ativas(self):
        s=sessao_sonda(False,True)
        snap=json.loads(json.dumps(s.exportar()))
        snap.pop('bandeiras_ativas',None)
        r=Sessao.restaurar(s.base,**snap)
        self.assertEqual(r.estado(),s.estado())
        self.assertEqual(list(r.como('chamar_agora')['bandeiras_historicas']),['bv'])

    def test_restaurar_ignora_bandeiras_ativas_recebidas(self):
        s=sessao_sonda(False,True)
        snap=json.loads(json.dumps(s.exportar()))
        r=Sessao.restaurar(s.base,**{**snap,'bandeiras_ativas':{'inexistente':{}}})
        self.assertEqual(r.estado(),s.estado())

    def test_correcao_que_remove_gatilho_e_volta_a_disparar_pausa_de_novo(self):
        b=base([simbolo('x'),simbolo('w'),simbolo('chamar_agora','urgencia'),doenca()],
               [regra('dw','d',0.4,condicao('w')),regra('dx','d',0.4,condicao('x')),
                regra('bv','chamar_agora',0.99,condicao('x'),classe='bandeira_vermelha')])
        s=Sessao(b)
        s.responder('w',True)
        s.responder('x',True); s.acao_bandeira('continuar')
        s.responder('x',False,corrigir=True)
        self.assertEqual(s.estado()['bandeiras'],[])
        s.responder('x',True,corrigir=True)
        self.assertTrue(s.estado()['pausa'])


def base_troca_de_modo():
    v=simbolo('v'); v['pergunta']={'veterinario':'v'}
    return base([simbolo('a'),v,simbolo('y'),simbolo('z','derivado'),doenca(),simbolo('chamar_agora','urgencia')],
                [regra('z1','z',0.8,condicao('v')),regra('z2','z',-0.9,condicao('y')),
                 regra('da','d',0.4,condicao('a')),regra('dy','d',0.4,condicao('y')),
                 regra('bv','chamar_agora',0.99,condicao('z'),classe='bandeira_vermelha')],
                triagem=[{'id':'T1','selecao':'multipla','simbolos':['a','v'],
                          'simbolos_por_modo':{'produtor':['a'],'veterinario':['a','v']}}])


def sessao_troca_de_modo(verificar=lambda s:None):
    s=Sessao(base_troca_de_modo())
    s.responder_triagem('T1',['a']); verificar(s)
    s.responder('y',True); verificar(s)
    s.trocar_modo('veterinario'); verificar(s)
    s.responder_triagem('T1',['v']); verificar(s)
    return s


class OrdemRealDeEntradaTests(unittest.TestCase):
    def confere(self,s):
        self.assertEqual(set(s.bandeiras_historicas),set(s._reprocessar_bandeiras()))

    def test_tela_reaberta_pela_troca_de_modo_respeita_a_ordem_de_entrada(self):
        s=sessao_troca_de_modo(self.confere)
        self.assertNotIn('bv',s.estado()['bandeiras'])
        r=Sessao.restaurar(s.base,**json.loads(json.dumps(s.exportar())))
        self.assertNotIn('bv',r.estado()['bandeiras'])
        s.responder('y',True,corrigir=True)
        self.assertNotIn('bv',s.estado()['bandeiras'])

    def test_correcao_nao_move_simbolo_na_ordem(self):
        s=sessao_troca_de_modo()
        antes=json.loads(json.dumps(s.exportar()['ordem_respostas']))
        s.responder('y',False,corrigir=True)
        self.assertEqual(s.exportar()['ordem_respostas'],antes)

    def test_ordem_respostas_invalida_e_recusada(self):
        s=sessao_troca_de_modo()
        snap=json.loads(json.dumps(s.exportar()))
        for ordem in ([['a'],['a']],[['inexistente']]):
            with self.assertRaises(ValueError):
                Sessao.restaurar(s.base,**{**snap,'ordem_respostas':ordem})

    def test_propriedade_bandeiras_iguais_ao_reprocessamento_completo_na_sonda(self):
        s=Sessao(base_sonda(),ficha={'x':True})
        passos=[lambda:s.acao_bandeira('continuar'),lambda:s.responder('w',True),lambda:s.responder('y',False),
                lambda:s.responder('y',True,corrigir=True),lambda:s.responder('w',False,corrigir=True),
                lambda:s.responder('y',False,corrigir=True)]
        for passo in passos:
            passo()
            self.assertEqual(set(s.bandeiras_historicas),set(s._reprocessar_bandeiras()))


class CorrecaoDeTelaComFichaTests(unittest.TestCase):
    def sessao(self):
        b=base([simbolo('a','ficha'),simbolo('b'),doenca()],[regra('r','d',0.8,condicao('b'))],
               triagem=[{'id':'T','selecao':'multipla','simbolos':['a','b']}])
        s=Sessao(b,ficha={'a':True})
        s.responder_triagem('T',['b'])
        return s

    def test_correcao_preserva_fato_da_ficha(self):
        s=self.sessao()
        s.responder_triagem('T',[],corrigir=True)
        self.assertEqual(s.fatos['a'].origem,'ficha')
        self.assertIs(s.fatos['a'].valor,True)
        self.assertIs(s.fatos['b'].valor,False)

    def test_correcao_nao_aceita_simbolo_da_ficha_na_lista(self):
        with self.assertRaises(ValueError):
            self.sessao().responder_triagem('T',['a'],corrigir=True)

    def test_restaurar_com_triagem_preserva_estado_e_tela_id(self):
        s=self.sessao()
        r=Sessao.restaurar(s.base,**json.loads(json.dumps(s.exportar())))
        self.assertEqual(r.estado(),s.estado())
        self.assertEqual(r.fatos['b'].tela_id,'T')
        self.assertEqual(r.fatos['a'].origem,'ficha')


class AjustesMenoresTests(unittest.TestCase):
    def test_calcular_inicial_nao_e_mais_parametro(self):
        with self.assertRaises(TypeError):
            Sessao(base_sonda(),_calcular_inicial=False)

    def test_estado_na_triagem_calcula_serve_a_uma_vez_por_simbolo(self):
        b=base([simbolo('a'),simbolo('b'),doenca()],[regra('r','d',0.8,condicao('a'))],
               triagem=[{'id':'T','selecao':'multipla','simbolos':['a','b']}])
        s=Sessao(b)
        with patch.object(Sessao,'_serve_a_triagem',autospec=True,side_effect=Sessao._serve_a_triagem) as contador:
            for _ in range(3): s.estado()
            self.assertEqual(contador.call_count,2)


if __name__=='__main__':
    unittest.main()
