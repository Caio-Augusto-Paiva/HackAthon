"""Regressões da base revisada, executadas contra o motor público existente."""
import json
from pathlib import Path
import subprocess
import sys
import unittest

from engine.inferencia import inferir
from engine.modelos import Base
from engine.sessao import Sessao

PROJETO = Path(__file__).resolve().parents[2]
ARQUIVO = PROJETO / 'base/desenvolvimento/anamnese-bovinos-v3.1.0-revisao1.json'


def carregar():
    return json.loads(ARQUIVO.read_text(encoding='utf-8'))


class ContratoDaBase(unittest.TestCase):
    def test_carrega_diretamente_no_motor(self):
        try:
            base = Base.de_dict(carregar())
        except (OSError, KeyError, TypeError, ValueError) as erro:
            self.fail(f'A base precisa carregar sem adaptação: {erro!r}')
        self.assertEqual(sum(s['tipo'] == 'doenca' for s in base.simbolos.values()), 8)

    def test_triagem_tem_seis_telas_e_textos_nos_dois_modos(self):
        telas = carregar()['meta'].get('triagem', [])
        self.assertEqual(len(telas), 6)
        for modo in ('produtor', 'veterinario'):
            sessao = Sessao(carregar(), modo=modo)
            self.assertEqual(sessao.estado()['proxima']['id'], 'dias_em_lactacao')
            sessao.responder_triagem('dias_em_lactacao', 10)
            esperado = ['extremidades'] if modo == 'produtor' else ['temperatura_retal']
            self.assertEqual(sessao.estado()['proxima']['simbolos'], esperado)
            for tela in telas:
                self.assertTrue(tela['texto'][modo].strip())

    def test_cada_doenca_tem_caminho_positivo_exclusivo_da_triagem(self):
        dados = carregar()
        simbolos = {s['id']: s for s in dados['simbolos']}
        triagem = {id for tela in dados['meta']['triagem'] for id in tela['simbolos']}
        regras_por_alvo = {}
        for regra in dados['regras']:
            regras_por_alvo.setdefault(regra['entao']['simbolo'], []).append(regra)

        def so_triagem(id):
            if simbolos[id]['tipo'] in ('pergunta', 'ficha'):
                return id in triagem
            regras = regras_por_alvo.get(id, [])
            return bool(regras) and all(so_triagem(c['simbolo']) for r in regras for c in r['se'])

        for id, simbolo in simbolos.items():
            if simbolo['tipo'] == 'doenca':
                with self.subTest(doenca=id):
                    self.assertTrue(any(r['entao']['cf'] > 0 and all(so_triagem(c['simbolo']) for c in r['se'])
                                        for r in regras_por_alvo[id]))

    def test_cada_doenca_tem_caminho_positivo_no_modo_produtor(self):
        dados = carregar()
        simbolos = {s['id']: s for s in dados['simbolos']}
        regras_por_alvo = {}
        for regra in dados['regras']:
            regras_por_alvo.setdefault(regra['entao']['simbolo'], []).append(regra)

        def produtor(id):
            simbolo = simbolos[id]
            if simbolo['tipo'] in ('pergunta', 'ficha'):
                return bool(simbolo.get('pergunta', {}).get('produtor'))
            return any(r['entao']['cf'] > 0 and all(produtor(c['simbolo']) for c in r['se'])
                       for r in regras_por_alvo.get(id, []))

        for id, simbolo in simbolos.items():
            if simbolo['tipo'] == 'doenca':
                with self.subTest(doenca=id):
                    self.assertTrue(produtor(id))

    def test_toda_bandeira_depende_diretamente_da_triagem(self):
        dados = carregar()
        triagem = {id for tela in dados['meta']['triagem'] for id in tela['simbolos']}
        for regra in dados['regras']:
            if regra['classe'] == 'bandeira_vermelha':
                with self.subTest(regra=regra['id']):
                    self.assertTrue(any(c['simbolo'] in triagem for c in regra['se']))
                    self.assertEqual(regra['entao']['simbolo'], 'chamar_agora')

    def test_perguntas_e_campos_de_ficha_sao_acessiveis(self):
        for simbolo in carregar()['simbolos']:
            if simbolo['tipo'] in ('pergunta', 'ficha'):
                with self.subTest(simbolo=simbolo['id']):
                    self.assertTrue(simbolo['pergunta'])
                    self.assertTrue(simbolo['nome'])
                    if simbolo['tipo'] == 'ficha':
                        self.assertEqual(simbolo['campo_ficha'], simbolo['id'])

    def test_sessao_restaurada_preserva_estado_e_explicacao(self):
        for modo in ('produtor', 'veterinario'):
            with self.subTest(modo=modo):
                sessao = Sessao(carregar(), modo=modo, limite_dinamico=0)
                for tela, resposta in (('dias_em_lactacao', 10),
                                       ('estado_termico', 'normal' if modo == 'produtor' else 38.5),
                                       ('atitude_locomocao', []), ('apetite_ruminacao', 'normal'),
                                       ('producao_leite', []), ('excrecoes', [])):
                    sessao.responder_triagem(tela, resposta)
                estado = sessao.estado()
                self.assertEqual(estado['fase'], 'encerrada')
                self.assertEqual(estado['progresso']['triagem_respondida'], 6)
                snapshot = json.loads(json.dumps(sessao.exportar()))
                restaurada = Sessao.restaurar(carregar(), **snapshot)
                self.assertEqual(restaurada.estado(), estado)
                self.assertEqual(restaurada.porque('dias_em_lactacao'), sessao.porque('dias_em_lactacao'))

    def test_troca_de_modo_permite_acrescentar_a_medicao_retal(self):
        sessao = Sessao(carregar(), ficha={'dias_em_lactacao': 10})
        sessao.responder_triagem('estado_termico', 'normal')
        sessao.trocar_modo('veterinario')
        self.assertEqual(sessao.estado()['proxima']['simbolos'], ['temperatura_retal'])

    def test_numeros_invalidos_nao_entram_como_evidencia(self):
        for id, valor in (('dias_em_lactacao', -1), ('bhb_sanguineo', -0.1),
                          ('calcio_serico', -1), ('ph_ruminal', 15)):
            with self.subTest(simbolo=id, valor=valor):
                with self.assertRaises(ValueError):
                    inferir(carregar(), {id: valor})


class ExemplosDaBase(unittest.TestCase):
    def executar(self, nome):
        processo = subprocess.run(
            [sys.executable, '-m', 'engine', str(ARQUIVO),
             str(ARQUIVO.parent / 'casos' / nome)],
            cwd=PROJETO, capture_output=True, text=True, encoding='utf-8', check=False,
            timeout=30,
        )
        self.assertEqual(processo.returncode, 0, processo.stdout + processo.stderr)
        resultado = json.loads(processo.stdout)
        self.assertEqual(resultado['status'], 'passou', resultado)
        return resultado['obtido']

    def test_exemplo_de_decubito_passa_pela_cli(self):
        resultado = self.executar('alerta-decubito.json')
        self.assertEqual(resultado['urgencia'], 'chamar_agora')
        self.assertIn('R-BV-01', resultado['bandeiras'])
        self.assertTrue(resultado['alerta']['pausa'])

    def test_exemplo_mamario_passa_pela_cli(self):
        resultado = self.executar('sinais-mamarios.json')
        self.assertEqual(resultado['urgencia'], 'observar')
        self.assertEqual(resultado['top1'], 'mastite')


class RegrasDaBase(unittest.TestCase):
    def calcular(self, **fatos):
        return inferir(carregar(), fatos)

    def test_tpb_com_mucosas_alteradas_nao_exige_febre(self):
        resultado = self.calcular(temperatura_retal=38.5, **{'mucosas_palidas_ou_ictericas': True})
        self.assertGreaterEqual(resultado.cfs['tpb'], 0.5)
        self.assertEqual(resultado.urgencia, 'chamar_agora')

    def test_esfregaco_positivo_sem_febre_alimenta_tpb(self):
        resultado = self.calcular(temperatura_retal=38.5, esfregaco_hemoparasitas=True)
        self.assertGreaterEqual(resultado.cfs['tpb'], 0.5)
        self.assertEqual(resultado.urgencia, 'chamar_agora')

    def test_extremidades_frias_com_temperatura_alta_nao_confirmam_hipotermia(self):
        resultado = self.calcular(temperatura_retal=40, extremidades='fria', apatia=True)
        self.assertLessEqual(resultado.cfs['hipotermia'], 0)
        self.assertNotIn('R-BV-04', resultado.bandeiras)

    def test_extremidades_quentes_com_temperatura_normal_nao_confirmam_febre(self):
        resultado = self.calcular(temperatura_retal=38.5, extremidades='quente')
        self.assertLessEqual(resultado.cfs['febre'], 0)

    def test_metrite_nao_vira_urgencia_apenas_por_risco_e_tamanho_uterino(self):
        resultado = self.calcular(dias_em_lactacao=8, retencao_placenta=True,
                                  utero_aumentado_palpacao=True, corrimento_vaginal=False,
                                  corrimento_fetido=False, temperatura_retal=38.5)
        self.assertLess(resultado.cfs['metrite'], 0.5)
        self.assertNotEqual(resultado.urgencia, 'chamar_agora')

    def test_caneca_nao_duplica_a_mesma_alteracao_do_leite(self):
        isolada = self.calcular(teste_caneca_grumos=True)
        repetida = self.calcular(teste_caneca_grumos=True, leite_alterado=True)
        self.assertEqual(repetida.cfs['mastite'], isolada.cfs['mastite'])
        self.assertGreater(isolada.cfs['mastite'], 0.5)

    def test_inicio_da_lactacao_termina_na_janela_aprovada(self):
        self.assertGreater(self.calcular(dias_em_lactacao=42).cfs['inicio_lactacao'], 0)
        self.assertEqual(self.calcular(dias_em_lactacao=43).cfs['inicio_lactacao'], 0)

    def test_alertas_brutos_continuam_independentes_do_diagnostico(self):
        for fatos, bandeira in (({'decubito': True}, 'R-BV-01'),
                                ({'urina_escura': True}, 'R-BV-02'),
                                ({'temperatura_retal': 41}, 'R-BV-06')):
            with self.subTest(fatos=fatos):
                resultado = self.calcular(**fatos)
                self.assertIn(bandeira, resultado.bandeiras)
                self.assertEqual(resultado.urgencia, 'chamar_agora')

    def test_exame_bioquimico_negativo_nao_e_confundido_com_positivo(self):
        self.assertEqual(self.calcular(bhb_sanguineo=1.19).cfs['cetose'], 0)
        self.assertGreater(self.calcular(bhb_sanguineo=1.2).cfs['cetose'], 0.8)

    def test_limite_da_urgencia_e_aplicado_ao_cf(self):
        abaixo = self.calcular(ubere_inflamado={'valor': True, 'cf': 0.98})
        no_limite = self.calcular(ubere_inflamado=True)
        self.assertNotIn('R-URG-05', {r['id'] for r in abaixo.disparadas})
        self.assertIn('R-URG-05', {r['id'] for r in no_limite.disparadas})

    def test_desconhecimento_nao_dispara_bandeira(self):
        resultado = self.calcular(decubito=None, urina_escura=None, apatia=None,
                                  temperatura_retal=None, extremidades=None)
        self.assertEqual(resultado.bandeiras, ())
        self.assertTrue(all(cf == 0 for cf in resultado.cfs.values()))

    def test_limiar_da_premissa_e_estrito_e_bandeira_independe_do_cf_da_doenca(self):
        no_limite = self.calcular(temperatura_retal={'valor': 41, 'cf': 0.2})
        acima = self.calcular(temperatura_retal={'valor': 41, 'cf': 0.21})
        self.assertNotIn('R-BV-06', no_limite.bandeiras)
        self.assertIn('R-BV-06', acima.bandeiras)
        self.assertEqual(acima.urgencia, 'chamar_agora')

    def test_mastite_e_hipocalcemia_podem_coexistir(self):
        resultado = self.calcular(dias_em_lactacao=2, calcio_serico=1.0,
                                  leite_alterado=True, teste_caneca_grumos=True)
        self.assertGreater(resultado.cfs['hipocalcemia'], 0.8)
        self.assertGreater(resultado.cfs['mastite'], 0.5)

    def test_bandeira_do_produtor_pausa_e_correcao_remove_alerta(self):
        sessao = Sessao(carregar(), ficha={'dias_em_lactacao': 2}, limite_dinamico=0)
        sessao.responder_triagem('estado_termico', 'normal')
        estado = sessao.responder_triagem('atitude_locomocao', ['decubito'])
        self.assertTrue(estado['pausa'])
        self.assertIn('R-BV-01', estado['bandeiras'])
        estado = sessao.responder_triagem('atitude_locomocao', [], corrigir=True)
        self.assertFalse(estado['pausa'])
        self.assertNotIn('R-BV-01', estado['bandeiras'])


if __name__ == '__main__':
    unittest.main(verbosity=2)
