import json
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest
from .apoio import modulo, base, simbolo, doenca, regra, condicao


class IntegracaoTests(unittest.TestCase):
    def test_exemplos_sinteticos_publicados_passam_no_motor(self):
        pasta=Path('tests/fixtures/motor')
        self.assertTrue((pasta/'base.json').is_file(),'Base sintética executável ausente')
        b=json.loads((pasta/'base.json').read_text(encoding='utf-8'))
        self.assertEqual(len([s for s in b['simbolos'] if s['tipo']=='doenca']),8)
        self.assertEqual(len(b['meta']['triagem']),6)
        for nome in ['confirmacao','bandeira']:
            c=json.loads((pasta/f'{nome}.json').read_text(encoding='utf-8'))
            r=modulo('casos').executar_caso(b,c)
            self.assertEqual(r['status'],'passou',r)

    def test_cli_executa_base_e_caso_json_com_codigo_saida(self):
        modulo('__main__')
        b=base([simbolo('x'),doenca()],[regra('r','d',0.9,condicao('x'))])
        caso={'id':'demo','modo':'produtor','respostas':{'x':True},'esperado':{'top1':'d','faixas':{'d':[90,90]}}}
        with tempfile.TemporaryDirectory(dir=Path.cwd()) as diretorio:
            pasta=Path(diretorio)
            (pasta/'base.json').write_text(json.dumps(b),encoding='utf-8')
            (pasta/'caso.json').write_text(json.dumps(caso),encoding='utf-8')
            comando=[sys.executable,'-m','engine',str(pasta/'base.json'),str(pasta/'caso.json')]
            r=subprocess.run(comando,capture_output=True,text=True,encoding='utf-8')
            self.assertEqual(r.returncode,0,r.stderr)
            self.assertEqual(json.loads(r.stdout)['status'],'passou')
            caso['esperado']['top1']='ausente'
            (pasta/'caso.json').write_text(json.dumps(caso),encoding='utf-8')
            r=subprocess.run(comando,capture_output=True,text=True,encoding='utf-8')
            self.assertEqual(r.returncode,1)
            self.assertEqual(json.loads(r.stdout)['status'],'falhou')

    def test_parecer_sinaliza_bandeira_nao_verificada_com_nao_sei(self):
        b=base([simbolo('x'),simbolo('y'),doenca(),simbolo('chamar_agora','urgencia')],
               [regra('d','d',0.5,condicao('x')),regra('bv','chamar_agora',0.9,condicao('x'),condicao('y'),classe='bandeira_vermelha')])
        s=modulo('sessao').Sessao(b,ficha={'x':True,'y':'nao_sei'},limite_dinamico=0)
        self.assertEqual(s.parecer()['bandeiras_nao_verificadas'],[])

    def test_limis_produtor_e_veterinario_contam_apenas_respostas_dinamicas(self):
        # Muitas evidências fracas mantêm hipótese aberta após responder não sei.
        ss=[simbolo(f'x{i:02d}') for i in range(50)]+[doenca()]
        rs=[regra(f'r{i}','d',0.1,condicao(f'x{i:02d}')) for i in range(50)]
        s=modulo('sessao').Sessao(base(ss,rs),'produtor')
        for i in range(12):
            estado=s.estado()
            if estado['fase']=='encerrada': break
            s.responder(estado['proxima']['id'],'nao_sei')
        self.assertEqual(s.estado()['motivo_parada'],'limite')
        self.assertEqual(s.estado()['progresso']['dinamicas_respondidas'],12)
        # O especialista não tem limite: pergunta até não restar o que mudar na hipótese.
        s=modulo('sessao').Sessao(base(ss,rs),'veterinario')
        while s.estado()['fase']!='encerrada':
            s.responder(s.estado()['proxima']['id'],'nao_sei')
        self.assertEqual(s.estado()['motivo_parada'],'sem_perguntas')
        self.assertEqual(s.estado()['progresso']['dinamicas_respondidas'],50)

