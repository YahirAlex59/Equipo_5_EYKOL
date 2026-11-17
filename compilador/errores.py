# -----------------------------------------------------------------------------
# Errores del compilador
# Todas las fases lanzan ErrorCompilacion en lugar de hacer print(), así el IDE
# puede mostrarlos en su panel de errores.
#
# Este archivo también decide QUÉ dice cada error: aquí están los nombres
# legibles de los tokens y las funciones que arman mensajes específicos
# (qué se esperaba, qué falta, cómo arreglarlo) para cada fase.
# -----------------------------------------------------------------------------
import difflib
import re


class ErrorCompilacion(Exception):
    """Error encontrado en alguna fase del compilador."""

    def __init__(self, fase, mensaje, linea=None, columna=None, sugerencia=None, simbolo=None):
        self.fase = fase              # 'Léxico', 'Sintáctico', 'Semántico' o 'Ejecución'
        self.mensaje = mensaje
        self.linea = linea
        self.columna = columna        # opcional: columna (1 = primer carácter de la línea)
        self.sugerencia = sugerencia  # opcional: cómo se puede corregir
        self.simbolo = simbolo        # opcional: nombre involucrado (sirve para ubicarlo)
        super().__init__(str(self))

    def __str__(self):
        if self.linea is not None and self.columna is not None:
            ubicacion = " (línea %d, columna %d)" % (self.linea, self.columna)
        elif self.linea is not None:
            ubicacion = " (línea %d)" % self.linea
        else:
            ubicacion = ""
        return "Error %s%s: %s" % (self.fase.lower(), ubicacion, self.mensaje)


# =============================================================================
# Utilidades de posición
# =============================================================================
def calcular_columna(texto, posicion):
    """Convierte una posición absoluta (lexpos de PLY) en columna 1-based."""
    if texto is None or posicion is None:
        return None
    inicio_linea = texto.rfind("\n", 0, posicion) + 1
    return posicion - inicio_linea + 1


def _quitar_comentarios_y_cadenas(linea):
    """Reemplaza cadenas y comentarios por espacios para no encontrar nombres dentro de ellos."""
    resultado = []
    dentro_cadena = False
    i = 0
    while i < len(linea):
        c = linea[i]
        if dentro_cadena:
            resultado.append(" ")
            if c == '"':
                dentro_cadena = False
        elif c == '"':
            dentro_cadena = True
            resultado.append(" ")
        elif linea.startswith("//", i) or c == "#":
            break
        else:
            resultado.append(c)
        i += 1
    return "".join(resultado)


def ubicar_simbolo(codigo, nombre):
    """Busca la primera aparición de `nombre` en el código (fuera de comentarios
    y cadenas). Regresa (linea, columna) o (None, None)."""
    if not codigo or not nombre:
        return None, None
    patron = re.compile(r"\b%s\b" % re.escape(nombre))
    en_comentario_multilinea = False
    for numero, linea in enumerate(codigo.split("\n"), start=1):
        if en_comentario_multilinea:
            fin = linea.find("*/")
            if fin == -1:
                continue
            linea = " " * (fin + 2) + linea[fin + 2:]
            en_comentario_multilinea = False
        inicio = linea.find("/*")
        if inicio != -1:
            fin = linea.find("*/", inicio + 2)
            if fin == -1:
                linea = linea[:inicio]
                en_comentario_multilinea = True
            else:
                linea = linea[:inicio] + " " * (fin + 2 - inicio) + linea[fin + 2:]
        m = patron.search(_quitar_comentarios_y_cadenas(linea))
        if m:
            return numero, m.start() + 1
    return None, None


# =============================================================================
# Nombres legibles de los tokens
# =============================================================================
NOMBRES_TOKENS = {
    'PARIZQ': "'('", 'PARDER': "')'",
    'LLAVIZQ': "'{'", 'LLAVDER': "'}'",
    'MAS': "'+'", 'MENOS': "'-'", 'POR': "'*'", 'DIVIDIDO': "'/'", 'MODULO': "'%'",
    'IGUAL': "'='", 'IGUALIGUAL': "'=='", 'DIFERENTE': "'!='",
    'MENORQUE': "'<'", 'MAYORQUE': "'>'", 'MENORIGUAL': "'<='", 'MAYORIGUAL': "'>='",
    'AND': "'&&'", 'OR': "'||'", 'NOT': "'!'",
    'PTCOMA': "';'",
    'ENTERO': "un número entero", 'DECIMAL': "un número decimal",
    'CADENA': "un texto entre comillas", 'ID': "un nombre de variable",
    '$end': "el final del programa",
}

# Grupos de tokens que se resumen en una sola palabra en los mensajes
INICIO_EXPRESION = {'ENTERO', 'DECIMAL', 'CADENA', 'ID', 'PARIZQ', 'MENOS', 'NOT',
                    'RRAIZ', 'RVERDADERO', 'RFALSO'}
INICIO_INSTRUCCION = {'RENTERO', 'RDECIMAL', 'RCADENA', 'RBOOLEANO', 'ID',
                      'RMOSTRAR', 'RSI', 'RMIENTRAS', 'RPARA'}
OPERADORES = {'MAS', 'MENOS', 'POR', 'DIVIDIDO', 'MODULO', 'IGUALIGUAL', 'DIFERENTE',
              'MENORQUE', 'MAYORQUE', 'MENORIGUAL', 'MAYORIGUAL', 'AND', 'OR'}
TIPOS_DATO = {'RENTERO', 'RDECIMAL', 'RCADENA', 'RBOOLEANO'}


def _palabra_reservada(tipo):
    """Texto en el lenguaje de un token de palabra reservada (ej. RMOSTRAR -> 'impt')."""
    from .lexico import reservadas   # import tardío para evitar import circular
    for palabra, token in reservadas.items():
        if token == tipo:
            return palabra
    return None


def describir_token(tipo):
    """Nombre legible de un tipo de token."""
    if tipo in NOMBRES_TOKENS:
        return NOMBRES_TOKENS[tipo]
    palabra = _palabra_reservada(tipo)
    if palabra:
        return "la palabra '%s'" % palabra
    return tipo


def describir_encontrado(token):
    """Cómo se nombra en el mensaje el token que causó el error."""
    if token is None:
        return "el final del programa"
    if token.type == 'ID':
        return "la variable '%s'" % token.value
    if token.type == 'CADENA':
        return 'el texto "%s"' % token.value
    if token.type in ('ENTERO', 'DECIMAL'):
        return "el número %s" % token.value
    palabra = _palabra_reservada(token.type)
    if palabra:
        return "la palabra '%s'" % palabra
    return "'%s'" % token.value


def describir_esperados(esperados):
    """Convierte un conjunto de tokens esperados en una frase corta."""
    esperados = set(esperados)
    partes = []
    if len(esperados & INICIO_INSTRUCCION) >= 4:
        partes.append("una instrucción")
        esperados -= INICIO_INSTRUCCION
    if len(esperados & INICIO_EXPRESION) >= 3:
        partes.append("un valor o una expresión")
        esperados -= INICIO_EXPRESION
    if len(esperados & OPERADORES) >= 3:
        partes.append("un operador")
        esperados -= OPERADORES
    if len(esperados & TIPOS_DATO) >= 3:
        partes.append("un tipo de dato (ent, deci, txt, boli)")
        esperados -= TIPOS_DATO
    partes.extend(describir_token(t) for t in sorted(esperados))
    if not partes:
        return ""
    if len(partes) == 1:
        return partes[0]
    return ", ".join(partes[:-1]) + " o " + partes[-1]


# =============================================================================
# Errores léxicos
# =============================================================================
_CARACTERES_CONOCIDOS = {
    '"': ("texto sin cerrar: falta la comilla de cierre '\"'",
          'Cierra el texto en la misma línea, por ejemplo: "hola".'),
    "'": ("las comillas simples no son válidas",
          'Los textos van entre comillas dobles, por ejemplo: "hola".'),
    '&': ("operador incompleto '&'",
          "Para el Y lógico usa '&&'."),
    '|': ("operador incompleto '|'",
          "Para el O lógico usa '||'."),
    '.': ("punto fuera de lugar",
          "Los decimales llevan dígitos a ambos lados del punto, por ejemplo: 0.5"),
    ',': ("la coma no es un símbolo válido",
          "Separa instrucciones con ';'. Para decimales usa punto: 3.14"),
    '[': ("los corchetes '[' no existen en EYKOL",
          "Usa '(' para agrupar expresiones."),
    ']': ("los corchetes ']' no existen en EYKOL",
          "Usa ')' para cerrar la agrupación."),
    ':': ("el símbolo ':' no existe en EYKOL",
          "Para asignar usa '=' y termina la instrucción con ';'."),
    '^': ("el símbolo '^' no existe en EYKOL",
          "Para potencias multiplica, por ejemplo: x * x"),
}


def error_lexico(caracter, linea, columna):
    """Arma un error léxico específico para el carácter no reconocido."""
    if caracter in _CARACTERES_CONOCIDOS:
        mensaje, sugerencia = _CARACTERES_CONOCIDOS[caracter]
    elif caracter.isalpha():
        mensaje = "la letra '%s' no es válida en nombres ni palabras clave" % caracter
        sugerencia = "Usa solo letras sin acentos (a-z), dígitos y '_'. Por ejemplo, 'año' -> 'anio'."
    else:
        mensaje = "carácter no válido '%s'" % caracter
        sugerencia = "Bórralo o reemplázalo por un operador válido: + - * / % == != < > <= >= && || !"
    return ErrorCompilacion('Léxico', mensaje, linea, columna, sugerencia)


# =============================================================================
# Errores sintácticos
# =============================================================================
def _fin_de_token(token):
    """(linea, columna) justo después del token (donde 'falta' algo)."""
    if token is None:
        return None, None
    datos = getattr(token.lexer, 'lexdata', None)
    columna = calcular_columna(datos, token.lexpos)
    largo = len(str(token.value))
    if token.type == 'CADENA':
        largo += 2   # las comillas
    if columna is not None and datos is not None:
        # el valor de números puede diferir del texto original (ej. 1.50 -> 1.5)
        fin = token.lexpos
        while fin < len(datos) and not datos[fin].isspace() and datos[fin] not in ";(){}":
            fin += 1
        largo = max(largo if token.type == 'CADENA' else 1, fin - token.lexpos)
        return token.lineno, columna + largo
    return token.lineno, None


def error_sintactico(token, esperados, anterior=None):
    """Arma un error sintáctico específico.

    token:     token donde falló el parser (None si se acabó el programa)
    esperados: conjunto de tipos de token que el parser aceptaba en ese punto
    anterior:  último token leído antes de `token` (para ubicar lo que falta)
    """
    esperados = set(esperados or ())
    encontrado = describir_encontrado(token)

    # ---- Se acabó el programa antes de tiempo ----
    if token is None:
        linea, columna = _fin_de_token(anterior)
        if 'LLAVDER' in esperados:
            return ErrorCompilacion('Sintáctico', "falta '}' para cerrar un bloque",
                                    linea, columna, "Agrega '}' al final del bloque que abriste con '{'.")
        if 'PTCOMA' in esperados:
            return ErrorCompilacion('Sintáctico', "falta ';' al final de la última instrucción",
                                    linea, columna, "Toda instrucción termina en ';'.")
        if 'PARDER' in esperados:
            return ErrorCompilacion('Sintáctico', "falta ')' para cerrar un paréntesis",
                                    linea, columna, "Revisa que cada '(' tenga su ')'.")
        return ErrorCompilacion('Sintáctico', "el programa terminó incompleto: se esperaba %s"
                                % describir_esperados(esperados), linea, columna)

    datos = getattr(token.lexer, 'lexdata', None)
    linea, columna = token.lineno, calcular_columna(datos, token.lexpos)

    # ---- Falta ';' al final de la línea anterior ----
    if 'PTCOMA' in esperados and anterior is not None and token.lineno > anterior.lineno:
        linea_ant, columna_ant = _fin_de_token(anterior)
        return ErrorCompilacion('Sintáctico', "falta ';' al final de la línea %d" % anterior.lineno,
                                linea_ant, columna_ant, "Agrega ';' al final de esa instrucción.")

    # ---- '=' donde se esperaba comparar ----
    if token.type == 'IGUAL' and 'IGUALIGUAL' in esperados:
        return ErrorCompilacion('Sintáctico', "se usó '=' dentro de una condición",
                                linea, columna, "Para comparar usa '=='. El '=' solo sirve para asignar.")

    # ---- Paréntesis sin cerrar ----
    if 'PARDER' in esperados and token.type in ('PTCOMA', 'LLAVIZQ', 'LLAVDER'):
        return ErrorCompilacion('Sintáctico', "falta ')' antes de %s" % encontrado,
                                linea, columna, "Revisa que cada '(' tenga su ')'.")

    # ---- Falta '{' para abrir el bloque ----
    if esperados == {'LLAVIZQ'}:
        return ErrorCompilacion('Sintáctico', "falta '{' para abrir el bloque; se encontró %s" % encontrado,
                                linea, columna, "Después de la condición va un bloque: { ... }")

    # ---- Llave de cierre que sobra ----
    if token.type == 'LLAVDER' and 'LLAVDER' not in esperados:
        return ErrorCompilacion('Sintáctico', "sobra '}': no hay ningún bloque abierto",
                                linea, columna, "Borra esta llave o revisa dónde abriste el bloque.")

    # ---- 'osi' sin 'si' ----
    if token.type == 'RSINO':
        return ErrorCompilacion('Sintáctico', "'osi' sin un 'si' antes",
                                linea, columna, "'osi' debe ir justo después del bloque '}' de un 'si'.")

    # ---- Falta '(' después de impt / si / durante / repetir / raiz ----
    if esperados == {'PARIZQ'} and anterior is not None:
        palabra = _palabra_reservada(anterior.type) or anterior.value
        return ErrorCompilacion('Sintáctico', "falta '(' después de '%s'" % palabra,
                                linea, columna, "Escribe por ejemplo: %s(...)" % palabra)

    # ---- Falta el nombre de la variable en una declaración ----
    if esperados == {'ID'} and anterior is not None and anterior.type in TIPOS_DATO:
        return ErrorCompilacion('Sintáctico', "falta el nombre de la variable después de '%s'" % anterior.value,
                                linea, columna, "Por ejemplo: %s x = ...;" % anterior.value)

    # ---- Dos valores seguidos sin operador ----
    if token.type in INICIO_EXPRESION and esperados & OPERADORES:
        return ErrorCompilacion('Sintáctico', "falta un operador antes de %s" % encontrado,
                                linea, columna, "Une los valores con un operador (+, -, *, /, ==, &&, ...) "
                                                "o termina la instrucción con ';'.")

    # ---- Falta un valor después de un operador o de '=' ----
    if esperados >= {'ENTERO', 'ID'} and token.type not in INICIO_EXPRESION:
        antes = ("después de '%s' " % anterior.value) if anterior is not None else ""
        return ErrorCompilacion('Sintáctico', "falta un valor %santes de %s" % (antes, encontrado),
                                linea, columna, "Escribe un número, un texto, una variable o una expresión.")

    # ---- Caso general ----
    esperado = describir_esperados(esperados)
    mensaje = "no se esperaba %s" % encontrado
    if esperado:
        mensaje += "; se esperaba %s" % esperado
    return ErrorCompilacion('Sintáctico', mensaje, linea, columna)


# =============================================================================
# Errores semánticos
# =============================================================================
def error_variable_no_declarada(nombre, declaradas, fase='Semántico'):
    """La variable se usa sin haberse declarado. Sugiere nombres parecidos."""
    parecidas = difflib.get_close_matches(nombre, list(declaradas), n=1, cutoff=0.6)
    if parecidas:
        sugerencia = "¿Quisiste decir '%s'?" % parecidas[0]
    else:
        sugerencia = "Declárala antes de usarla, por ejemplo: ent %s = 0;" % nombre
    return ErrorCompilacion(fase, "la variable '%s' no está declarada" % nombre,
                            sugerencia=sugerencia, simbolo=nombre)


# =============================================================================
# Errores de ejecución
# =============================================================================
NOMBRES_TIPOS = {int: 'ent', float: 'deci', str: 'txt', bool: 'boli'}


def tipo_de(valor):
    """Nombre del tipo EYKOL de un valor de Python."""
    return NOMBRES_TIPOS.get(type(valor), type(valor).__name__)


def error_division_cero(operador):
    accion = "módulo" if operador == '%' else "división"
    return ErrorCompilacion('Ejecución', "%s entre cero" % accion,
                            sugerencia="Revisa con un 'si' que el divisor no sea 0 antes de dividir.")


def error_tipo_asignacion(valor, nombre, tipo):
    return ErrorCompilacion('Ejecución',
                            "no se puede guardar %r (%s) en la variable '%s' de tipo %s"
                            % (valor, tipo_de(valor), nombre, tipo),
                            sugerencia="Asigna un valor de tipo %s o declara la variable con otro tipo." % tipo,
                            simbolo=nombre)


def error_operacion(operador, izq, der, texto):
    return ErrorCompilacion('Ejecución',
                            "no se puede aplicar '%s' a %s (%s) y %s (%s)"
                            % (operador, texto(izq), tipo_de(izq), texto(der), tipo_de(der)),
                            sugerencia="Ambos lados deben ser de un tipo compatible (por ejemplo, dos números).")


def error_raiz_tipo(valor, texto):
    return ErrorCompilacion('Ejecución', "raiz() requiere un número, se recibió %s (%s)"
                            % (texto(valor), tipo_de(valor)),
                            sugerencia="Pásale un ent o un deci, por ejemplo: raiz(16)")


def error_raiz_negativa(valor):
    return ErrorCompilacion('Ejecución', "no se puede calcular la raíz cuadrada de un número negativo (%s)" % valor,
                            sugerencia="Verifica que el valor sea mayor o igual a 0.")


def error_ciclo_infinito(maximo):
    return ErrorCompilacion('Ejecución', "el ciclo superó %d vueltas (¿ciclo infinito?)" % maximo,
                            sugerencia="Asegúrate de que la condición del ciclo cambie en cada vuelta "
                                       "(por ejemplo, incrementando el contador).")
