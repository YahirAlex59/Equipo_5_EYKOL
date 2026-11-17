
# -----------------------------------------------------------------------------
# Punto de entrada de EYKOL.
#
#   python main.py                         -> abre el IDE
#   python main.py ejemplos/errores.txt    -> ejecuta un archivo
#   python main.py archivo.txt --todo      -> muestra tokens, arbol, etc.
# -----------------------------------------------------------------------------

import sys
from pprint import pprint

from compilador import compilar


def titulo(texto):
    print('\n' + '=' * 20, texto, '=' * 20)


def abrir_ide():
    from PyQt6.QtWidgets import QApplication
    from ide.prueba_ventana import VentanaIDE

    app = QApplication(sys.argv)

    ventana = VentanaIDE()
    ventana.show()

    sys.exit(app.exec())


def main():
    # Sin argumentos: abrir el IDE
    if len(sys.argv) == 1:
        abrir_ide()
        return

    # Con argumentos: conservar la ejecución por consola
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

        titulo('ARBOL')
        pprint(r.arbol)

        titulo('CODIGO INTERMEDIO')
        print('\n'.join(r.codigo_intermedio))

        titulo('TABLA DE SIMBOLOS')
        for nombre, (tipo, valor) in r.tabla_simbolos.items():
            print('%-12s %-10s %s' % (nombre, tipo, valor))

    titulo('SALIDA')
    print('\n'.join(r.salida))

    if r.errores:
        titulo('ERRORES')
        for e in r.errores:
            print(e)
            if getattr(e, 'sugerencia', None):
                print('    Sugerencia:', e.sugerencia)

        sys.exit(1)


if __name__ == '__main__':
    main()
