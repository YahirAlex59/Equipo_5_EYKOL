# -----------------------------------------------------------------------------
# Errores del compilador
# Todas las fases lanzan ErrorCompilacion en lugar de hacer print(), así el IDE
# puede mostrarlos en su panel de errores.
# -----------------------------------------------------------------------------


class ErrorCompilacion(Exception):
    """Error encontrado en alguna fase del compilador."""

    def __init__(self, fase, mensaje, linea=None, columna=None):
        self.fase = fase          # 'Léxico', 'Sintáctico', 'Semántico' o 'Ejecución'
        self.mensaje = mensaje
        self.linea = linea
        self.columna = columna    # opcional: columna (1 = primer carácter de la línea)
        super().__init__(str(self))

    def __str__(self):
        if self.linea is not None:
            return "Error %s (línea %d): %s" % (self.fase.lower(), self.linea, self.mensaje)
        return "Error %s: %s" % (self.fase.lower(), self.mensaje)


def calcular_columna(texto, posicion):
    """Convierte una posición absoluta (lexpos de PLY) en columna 1-based."""
    if texto is None or posicion is None:
        return None
    inicio_linea = texto.rfind("\n", 0, posicion) + 1
    return posicion - inicio_linea + 1
