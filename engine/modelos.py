"""Fronteira de dados do motor, compatível com JSON e model_dump do kb."""
from copy import deepcopy
from dataclasses import dataclass
from fractions import Fraction
from .cf import fracao

LIMIARES = {'descarte': -0.2, 'premissa': 0.2, 'hipotese_relevante': 0.35,
            'exaustao': 0.6, 'potencial': 0.7, 'confirmacao': 0.8}
CORTES = {'bloco_principal': 0.5, 'bloco_diferencial': 0.2}
PRIORIDADES = {'bandeira_vermelha': 100, 'urgencia': 50, 'evidencia': 10}
CAMADAS = {'pergunta': 0, 'ficha': 0, 'derivado': 1, 'doenca': 2, 'urgencia': 3}
GRAVIDADES = {'baixa': 0, 'media': 1, 'alta': 2}
MODOS = ('produtor', 'veterinario')


def desconhecido(valor):
    return valor is None or (isinstance(valor, str) and valor in ('nao_sei', 'não sei'))


@dataclass(frozen=True)
class Fato:
    simbolo: str
    valor: object
    cf: Fraction
    origem: str = 'resposta'
    tela_id: str | None = None


@dataclass(frozen=True)
class Base:
    simbolos: dict
    regras: tuple
    meta: dict

    @classmethod
    def de_dict(cls, dados):
        if isinstance(dados, cls):
            return dados
        if hasattr(dados, 'model_dump'):
            dados = dados.model_dump(mode='json')
        dados = deepcopy(dados)
        from .validacao import validar
        validar(dados)
        meta = dados.get('meta', {})
        meta['limiares'] = {k: fracao(meta.get('limiares', {}).get(k,v)) for k,v in {**LIMIARES,**CORTES}.items()}
        meta['limite_dinamico'] = {'produtor': 12, 'veterinario': 25, **meta.get('limite_dinamico', {})}
        meta.setdefault('triagem', [])
        for regra in dados['regras']:
            regra.setdefault('prioridade',PRIORIDADES[regra.get('classe','evidencia')])
        return cls({s['id']:s for s in dados['simbolos']}, tuple(dados['regras']), meta)

    def regras_para(self, id):
        return tuple(r for r in self.regras if r['entao']['simbolo'] == id)


def observar(id, entrada, simbolos, *, origem='resposta', tela_id=None):
    """Normaliza valor/certeza sem confundir intensidade com certeza."""
    simbolo = simbolos[id]
    if simbolo['tipo'] not in ('pergunta', 'ficha'):
        raise ValueError('Somente fatos observados podem ser fornecidos')
    if isinstance(entrada, Fato):
        if entrada.simbolo != id:
            raise ValueError('Identidade do fato incompatível')
        valor, cf, origem, tela_id = entrada.valor, entrada.cf, entrada.origem, entrada.tela_id
    elif isinstance(entrada, dict):
        valor, cf = entrada.get('valor'), entrada.get('cf', 1)
        origem, tela_id = entrada.get('origem',origem), entrada.get('tela_id',tela_id)
    else:
        valor, cf = entrada, 1
    if origem not in ('resposta','ficha','importacao'):
        raise ValueError('Origem de observação inválida')
    cf = fracao(cf)
    if desconhecido(valor):
        return Fato(id,None,Fraction(0),origem,tela_id)
    dominio = simbolo['dominio']
    tipo = dominio['tipo']
    if tipo == 'booleano':
        if valor in ('sim','não','nao'):
            valor = valor == 'sim'
        if not isinstance(valor,bool):
            raise ValueError(f'{id}: esperado booleano')
        cf = abs(cf) if valor else -abs(cf)
    else:
        if cf < 0:
            raise ValueError('Certeza de valor numérico/categórico deve ser não negativa')
        if tipo == 'categorico' and 'valores' in dominio and valor not in dominio['valores']:
            raise ValueError(f'{id}: valor fora do domínio')
        if tipo == 'numerico':
            try:
                if isinstance(valor,bool): raise ValueError()
                numero = Fraction(str(valor))
                if ('min' in dominio and numero < Fraction(str(dominio['min']))) or ('max' in dominio and numero > Fraction(str(dominio['max']))):
                    raise ValueError()
            except (ValueError,TypeError,ZeroDivisionError) as erro:
                raise ValueError(f'{id}: número fora do domínio') from erro
            valor = numero
    return Fato(id,valor,cf,origem,tela_id)


def normalizar_fatos(base, fatos):
    return {id:observar(id,entrada,base.simbolos) for id,entrada in sorted(fatos.items())}
