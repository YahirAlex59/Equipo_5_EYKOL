# -----------------------------------------------------------------------------
# Fase 2: análisis sintáctico
# Revisa que los tokens sigan la gramática y arma el árbol (AST).
# No ejecuta nada: el cuerpo de un ciclo se reduce una sola vez, por eso la
# ejecución se hace después en interprete.py.
#
# Forma de los nodos del árbol (tuplas):
#   ('declarar', tipo, nombre, expresion | None)
#   ('asignar',  nombre, expresion)
#   ('mostrar',  expresion)
#   ('si',       condicion, [instrucciones], [instrucciones del sino])
#   ('mientras', condicion, [instrucciones])
#   ('para',     inicio, condicion, paso, [instrucciones])
#   ('binaria',  operador, izquierda, derecha)
#   ('negativo', expresion)   ('not', expresion)
#   ('valor',    valor)       ('id', nombre)
# -----------------------------------------------------------------------------
import ply.yacc as yacc

from .errores import ErrorCompilacion
from .lexico import tokens, lexer   # PLY necesita `tokens` en este módulo

# Asociación de operadores y precedencia (de menor a mayor, como en C)
precedence = (
    ('left', 'OR'),
    ('left', 'AND'),
    ('left', 'IGUALIGUAL', 'DIFERENTE'),
    ('left', 'MENORQUE', 'MAYORQUE', 'MENORIGUAL', 'MAYORIGUAL'),
    ('left', 'MAS', 'MENOS'),
    ('left', 'POR', 'DIVIDIDO', 'MODULO'),
    ('right', 'NOT', 'UMENOS'),
)


# ---------------------------- Instrucciones ----------------------------------
def p_instrucciones_lista(t):
    'instrucciones : instrucciones instruccion'
    t[1].append(t[2])
    t[0] = t[1]


def p_instrucciones_una(t):
    'instrucciones : instruccion'
    t[0] = [t[1]]


def p_instruccion(t):
    '''instruccion : declaracion PTCOMA
                   | asignacion PTCOMA
                   | mostrar
                   | si
                   | mientras
                   | para'''
    t[0] = t[1]


def p_tipo(t):
    '''tipo : RENTERO
            | RDECIMAL
            | RCADENA
            | RBOOLEANO'''
    t[0] = t[1]


def p_declaracion(t):
    'declaracion : tipo ID'
    t[0] = ('declarar', t[1], t[2], None)


def p_declaracion_valor(t):
    'declaracion : tipo ID IGUAL expresion'
    t[0] = ('declarar', t[1], t[2], t[4])


def p_asignacion(t):
    'asignacion : ID IGUAL expresion'
    t[0] = ('asignar', t[1], t[3])


def p_mostrar(t):
    'mostrar : RMOSTRAR PARIZQ expresion PARDER PTCOMA'
    t[0] = ('mostrar', t[3])


# ---------------------------- Control de flujo -------------------------------
def p_si(t):
    'si : RSI PARIZQ expresion PARDER bloque'
    t[0] = ('si', t[3], t[5], [])


def p_si_sino(t):
    'si : RSI PARIZQ expresion PARDER bloque RSINO bloque'
    t[0] = ('si', t[3], t[5], t[7])


def p_si_sino_si(t):
    'si : RSI PARIZQ expresion PARDER bloque RSINO si'
    t[0] = ('si', t[3], t[5], [t[7]])


def p_mientras(t):
    'mientras : RMIENTRAS PARIZQ expresion PARDER bloque'
    t[0] = ('mientras', t[3], t[5])


def p_para(t):
    '''para : RPARA PARIZQ declaracion PTCOMA expresion PTCOMA asignacion PARDER bloque
            | RPARA PARIZQ asignacion PTCOMA expresion PTCOMA asignacion PARDER bloque'''
    t[0] = ('para', t[3], t[5], t[7], t[9])


def p_bloque(t):
    'bloque : LLAVIZQ instrucciones LLAVDER'
    t[0] = t[2]


def p_bloque_vacio(t):
    'bloque : LLAVIZQ LLAVDER'
    t[0] = []


# ---------------------------- Expresiones ------------------------------------
def p_expresion_binaria(t):
    '''expresion : expresion MAS expresion
                 | expresion MENOS expresion
                 | expresion POR expresion
                 | expresion DIVIDIDO expresion
                 | expresion MODULO expresion
                 | expresion MENORQUE expresion
                 | expresion MAYORQUE expresion
                 | expresion MENORIGUAL expresion
                 | expresion MAYORIGUAL expresion
                 | expresion IGUALIGUAL expresion
                 | expresion DIFERENTE expresion
                 | expresion AND expresion
                 | expresion OR expresion'''
    t[0] = ('binaria', t[2], t[1], t[3])


def p_expresion_unaria(t):
    'expresion : MENOS expresion %prec UMENOS'
    t[0] = ('negativo', t[2])


def p_expresion_not(t):
    'expresion : NOT expresion'
    t[0] = ('not', t[2])


def p_expresion_agrupacion(t):
    'expresion : PARIZQ expresion PARDER'
    t[0] = t[2]


def p_expresion_valor(t):
    '''expresion : ENTERO
                 | DECIMAL
                 | CADENA'''
    t[0] = ('valor', t[1])


def p_expresion_booleano(t):
    '''expresion : RVERDADERO
                 | RFALSO'''
    t[0] = ('valor', t[1] == 'verdadero')


def p_expresion_id(t):
    'expresion : ID'
    t[0] = ('id', t[1])


# ---------------------------- Errores ----------------------------------------
def p_error(t):
    if t:
        raise ErrorCompilacion('Sintáctico', "símbolo inesperado '%s'" % t.value, t.lineno)
    raise ErrorCompilacion('Sintáctico', 'el programa terminó antes de tiempo (¿falta un ; o una } ?)')


# Construye el parser. Genera parsetab.py y parser.out dentro de esta carpeta;
# en parser.out se pueden revisar los conflictos de la gramática.
parser = yacc.yacc()


def analizar_sintactico(codigo):
    """Regresa el árbol (lista de instrucciones). Lanza ErrorCompilacion si hay error."""
    lexer.lineno = 1
    arbol = parser.parse(codigo, lexer=lexer)
    return arbol or []
