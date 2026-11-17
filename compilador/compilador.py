# -----------------------------------------------------------------------------
# Compilador: une todas las fases.
#
#   código ─► léxico ─► sintáctico ─► semántico ─► código intermedio ─► ejecución
#
# El IDE solo necesita llamar a compilar(texto) y mostrar el Resultado.
# -----------------------------------------------------------------------------
from dataclasses import dataclass, field

from .errores import ErrorCompilacion, ubicar_simbolo
from .lexico import analizar_lexico
from .sintactico import analizar_sintactico
from .semantico import analizar_semantico
from .generacion import generar_codigo
from .interprete import Interprete


@dataclass
class Resultado:
    tokens: list = field(default_factory=list)              # [(tipo, valor, línea)]
    arbol: list = field(default_factory=list)               # AST (tuplas)
    codigo_intermedio: list = field(default_factory=list)   # líneas de tres direcciones
    salida: list = field(default_factory=list)              # lo que mostró el programa
    tabla_simbolos: dict = field(default_factory=dict)      # nombre -> (tipo, valor)
    errores: list = field(default_factory=list)             # [ErrorCompilacion]

    @property
    def exito(self):
        return not self.errores


def _ubicar(error, codigo):
    """El árbol no guarda posiciones: si el error menciona una variable, se
    busca en el código para poder decir en qué línea y columna está."""
    if error.linea is None and getattr(error, 'simbolo', None):
        error.linea, error.columna = ubicar_simbolo(codigo, error.simbolo)
    return error


def compilar(codigo, ejecutar=True):
    """Pasa el código por todas las fases. Se detiene en la primera que falle."""
    r = Resultado()

    # 1. Léxico
    r.tokens, r.errores = analizar_lexico(codigo)
    if r.errores or not r.tokens:
        return r

    try:
        # 2. Sintáctico
        r.arbol = analizar_sintactico(codigo)
        # 3. Semántico
        analizar_semantico(r.arbol)
        # 4. Código intermedio
        r.codigo_intermedio = generar_codigo(r.arbol)
    except ErrorCompilacion as e:
        r.errores.append(_ubicar(e, codigo))
        return r

    # 5. Ejecución
    if ejecutar:
        interprete = Interprete()
        try:
            interprete.ejecutar(r.arbol)
        except ErrorCompilacion as e:
            r.errores.append(_ubicar(e, codigo))
        except RecursionError:
            r.errores.append(ErrorCompilacion(
                'Ejecución', 'el programa es demasiado anidado',
                sugerencia='Reduce la cantidad de bloques o paréntesis anidados.'))
        r.salida = interprete.salida          # se conserva lo que alcanzó a mostrar
        r.tabla_simbolos = interprete.tabla

    return r
