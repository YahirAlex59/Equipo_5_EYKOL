# -----------------------------------------------------------------------------
# Fase 1: análisis léxico
# Convierte el texto del programa en una lista de tokens.
#
# >>> AQUÍ SE PERSONALIZAN LAS PALABRAS CLAVE DEL LENGUAJE <<<
# Para cambiar, por ejemplo, 'entero' por 'ent', basta con cambiar la llave
# del diccionario `reservadas`. El nombre del token (RENTERO) no cambia, así
# que la gramática sigue funcionando.
# -----------------------------------------------------------------------------
import ply.lex as lex

from .errores import ErrorCompilacion

# Palabras reservadas: se reconocen primero como ID y luego se reclasifican
#   'texto en el lenguaje' : 'NOMBRE_DEL_TOKEN'
reservadas = {
    'entero'    : 'RENTERO',
    'decimal'   : 'RDECIMAL',
    'cadena'    : 'RCADENA',
    'booleano'  : 'RBOOLEANO',
    'si'        : 'RSI',
    'sino'      : 'RSINO',
    'mientras'  : 'RMIENTRAS',
    'para'      : 'RPARA',
    'mostrar'   : 'RMOSTRAR',
    'verdadero' : 'RVERDADERO',
    'falso'     : 'RFALSO',
}

tokens = [
    'PARIZQ', 'PARDER', 'LLAVIZQ', 'LLAVDER',
    'MAS', 'MENOS', 'POR', 'DIVIDIDO', 'MODULO',
    'IGUAL', 'IGUALIGUAL', 'DIFERENTE',
    'MENORQUE', 'MAYORQUE', 'MENORIGUAL', 'MAYORIGUAL',
    'AND', 'OR', 'NOT',
    'PTCOMA',
    'DECIMAL', 'ENTERO', 'CADENA', 'ID',
] + list(reservadas.values())

# Símbolos (PLY ordena estas reglas de la expresión más larga a la más corta,
# por eso '==' se reconoce antes que '=')
t_PARIZQ     = r'\('
t_PARDER     = r'\)'
t_LLAVIZQ    = r'\{'
t_LLAVDER    = r'\}'
t_MAS        = r'\+'
t_MENOS      = r'-'
t_POR        = r'\*'
t_DIVIDIDO   = r'/'
t_MODULO     = r'%'
t_IGUAL      = r'='
t_IGUALIGUAL = r'=='
t_DIFERENTE  = r'!='
t_MENORQUE   = r'<'
t_MAYORQUE   = r'>'
t_MENORIGUAL = r'<='
t_MAYORIGUAL = r'>='
t_AND        = r'&&'
t_OR         = r'\|\|'
t_NOT        = r'!'
t_PTCOMA     = r';'

# Caracteres ignorados
t_ignore = ' \t\r'

# Lista donde se acumulan los errores léxicos de la última ejecución
errores = []


# Las reglas definidas como función se prueban en el orden en que aparecen,
# por eso los comentarios van antes que DIVIDIDO y DECIMAL antes que ENTERO.
def t_COMENTARIO_MULTILINEA(t):
    r'/\*(.|\n)*?\*/'
    t.lexer.lineno += t.value.count('\n')     # no regresa token: se descarta


def t_COMENTARIO_SIMPLE(t):
    r'//.*'


def t_DECIMAL(t):
    r'\d+\.\d+'
    t.value = float(t.value)
    return t


def t_ENTERO(t):
    r'\d+'
    t.value = int(t.value)
    return t


def t_CADENA(t):
    r'"[^"\n]*"'
    t.value = t.value[1:-1]     # quita las comillas
    return t


def t_ID(t):
    r'[a-zA-Z_][a-zA-Z_0-9]*'
    t.type = reservadas.get(t.value, 'ID')     # distingue mayúsculas, como C
    return t


def t_newline(t):
    r'\n+'
    t.lexer.lineno += len(t.value)


def t_error(t):
    errores.append(ErrorCompilacion('Léxico', "carácter no válido '%s'" % t.value[0], t.lexer.lineno))
    t.lexer.skip(1)


# Construyendo el analizador léxico
lexer = lex.lex()


def analizar_lexico(codigo):
    """Regresa (tokens, errores). Cada token es una tupla (tipo, valor, línea)."""
    errores.clear()
    lexer.lineno = 1
    lexer.input(codigo)
    lista = [(t.type, t.value, t.lineno) for t in lexer]
    return lista, list(errores)
