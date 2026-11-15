# -----------------------------------------------------------------------------
# Punto de entrada por consola (para probar mientras se hace el IDE).
#
#   python main.py                         -> usa ejemplos/ejemplo.txt
#   python main.py ejemplos/errores.txt    -> otro archivo
#   python main.py archivo.txt --todo      -> muestra también tokens, árbol, etc.
# -----------------------------------------------------------------------------
import sys
from pprint import pprint

from compilador import compilar


def titulo(texto):
    print('\n' + '=' * 20, texto, '=' * 20)


def main():
    args = [a for a in sys.argv[1:] if not a.startswith('--')]
    ver_todo = '--todo' in sys.argv
    ruta = args[0] if args else 'ejemplos/ejemplo.txt'

    with open(ruta, encoding='utf-8') as f:
        codigo = f.read()

    r = compilar(codigo)

    if ver_todo:
        titulo('TOKENS')
        for token in r.tokens:
            print(token)
        titulo('ÁRBOL')
        pprint(r.arbol)
        titulo('CÓDIGO INTERMEDIO')
        print('\n'.join(r.codigo_intermedio))
        titulo('TABLA DE SÍMBOLOS')
        for nombre, (tipo, valor) in r.tabla_simbolos.items():
            print('%-12s %-10s %s' % (nombre, tipo, valor))

    titulo('SALIDA')
    print('\n'.join(r.salida))

    if r.errores:
        titulo('ERRORES')
        for e in r.errores:
            print(e)
        sys.exit(1)


if __name__ == '__main__':
    main()
