"""Compilador de nuestro lenguaje, hecho con PLY.

Uso:
    from compilador import compilar
    resultado = compilar(texto)
"""
from .compilador import compilar, Resultado
from .errores import ErrorCompilacion

__all__ = ['compilar', 'Resultado', 'ErrorCompilacion']
