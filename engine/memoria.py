"""Memória de observações por símbolo; conclusões não são entradas."""
from .modelos import observar


class Memoria:
    def __init__(self, base):
        self.base=base
        self.fatos={}

    def registrar(self, entradas, *, origem='resposta', tela_id=None):
        novos={id:observar(id,valor,self.base.simbolos,origem=origem,tela_id=tela_id)
               for id,valor in entradas.items()}
        self.fatos.update(novos)
