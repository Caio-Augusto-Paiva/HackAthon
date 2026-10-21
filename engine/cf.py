"""Aritmética MYCIN exata: decimais de entrada viram frações."""
from fractions import Fraction


def fracao(valor):
    """Valida um CF finito no intervalo fechado [-1, 1]."""
    try:
        if isinstance(valor, bool):
            raise ValueError('CF não é booleano')
        resultado = valor if isinstance(valor, Fraction) else Fraction(str(valor))
        if not -1 <= resultado <= 1:
            raise ValueError('CF fora de [-1, 1]')
        return resultado
    except (ValueError, TypeError, ZeroDivisionError) as erro:
        raise ValueError(f'CF inválido: {valor!r}') from erro


def combinar(a, b):
    """Combina evidências; ±1 conflitantes têm a guarda defensiva 0."""
    a, b = fracao(a), fracao(b)
    if a >= 0 and b >= 0:
        return a + b * (1-a)
    if a <= 0 and b <= 0:
        return a + b * (1+a)
    denominador = 1-min(abs(a), abs(b))
    return (a+b)/denominador if denominador else Fraction(0)


def combinar_todas(valores):
    resultado = Fraction(0)
    for valor in valores:
        resultado = combinar(resultado, valor)
    return resultado
