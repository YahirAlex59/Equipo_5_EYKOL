from PyQt6.QtCore import QRegularExpression
from PyQt6.QtGui import QColor, QFont, QSyntaxHighlighter, QTextCharFormat


class ResaltadorEYKOL(QSyntaxHighlighter):
    """Resaltador de sintaxis para el lenguaje EYKOL."""

    PALABRAS_RESERVADAS = [
        "ent", "deci", "txt", "boli", "si", "osi",
        "durante", "repetir", "impt", "vrd", "fals", "raiz",
    ]

    def __init__(self, documento):
        super().__init__(documento)
        self.reglas = []

        formato_reservadas = QTextCharFormat()
        formato_reservadas.setForeground(QColor("#569CD6"))
        formato_reservadas.setFontWeight(QFont.Weight.Bold)

        for palabra in self.PALABRAS_RESERVADAS:
            patron = QRegularExpression(rf"\b{palabra}\b")
            self.reglas.append((patron, formato_reservadas))

    def highlightBlock(self, texto):
        for patron, formato in self.reglas:
            iterador = patron.globalMatch(texto)
            while iterador.hasNext():
                m = iterador.next()
                self.setFormat(m.capturedStart(), m.capturedLength(), formato)