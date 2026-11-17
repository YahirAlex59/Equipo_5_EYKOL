from PyQt6.QtCore import QRegularExpression
from PyQt6.QtGui import QColor, QFont, QSyntaxHighlighter, QTextCharFormat


def _formato(color, negrita=False, cursiva=False):
    f = QTextCharFormat()
    f.setForeground(QColor(color))
    if negrita:
        f.setFontWeight(QFont.Weight.Bold)
    f.setFontItalic(cursiva)
    return f


class ResaltadorEYKOL(QSyntaxHighlighter):
    """Resaltador de sintaxis para el lenguaje EYKOL."""

    PALABRAS_RESERVADAS = [
        "ent", "deci", "txt", "boli", "si", "osi",
        "durante", "repetir", "impt", "vrd", "fals", "raiz",
    ]

    def __init__(self, documento):
        super().__init__(documento)

        self.formato_comentario = _formato("#5FD38D")
        self.reglas = []

        # Palabras reservadas
        formato_reservadas = _formato("#4FC3FF", negrita=True)
        for palabra in self.PALABRAS_RESERVADAS:
            self.reglas.append((QRegularExpression(rf"\b{palabra}\b"), formato_reservadas))

        # Numeros enteros y decimales
        self.reglas.append(
            (QRegularExpression(r"\b\d+(\.\d+)?\b"), _formato("#B5F58A"))
        )

        # Cadenas entre comillas
        self.reglas.append(
            (QRegularExpression(r'"[^"\n]*"'), _formato("#FFB08A"))
        )

        # Comentarios de una linea (va al final para que tenga prioridad)
        self.reglas.append(
            (QRegularExpression(r"(//|#)[^\n]*"), self.formato_comentario)
        )

        # Comentario de varias lineas /* ... */
        self.inicio_comentario = QRegularExpression(r"/\*")
        self.fin_comentario = QRegularExpression(r"\*/")

    def highlightBlock(self, texto):
        for patron, formato in self.reglas:
            iterador = patron.globalMatch(texto)
            while iterador.hasNext():
                m = iterador.next()
                self.setFormat(m.capturedStart(), m.capturedLength(), formato)

        # Comentarios multilinea (usa el estado del bloque anterior)
        self.setCurrentBlockState(0)

        if self.previousBlockState() == 1:
            inicio = 0
            desde = 0
        else:
            m = self.inicio_comentario.match(texto)
            inicio = m.capturedStart() if m.hasMatch() else -1
            desde = inicio + 2

        while inicio >= 0:
            m_fin = self.fin_comentario.match(texto, desde)
            if m_fin.hasMatch():
                longitud = m_fin.capturedEnd() - inicio
                self.setFormat(inicio, longitud, self.formato_comentario)
                m = self.inicio_comentario.match(texto, inicio + longitud)
                inicio = m.capturedStart() if m.hasMatch() else -1
                desde = inicio + 2
            else:
                self.setCurrentBlockState(1)
                self.setFormat(inicio, len(texto) - inicio, self.formato_comentario)
                break