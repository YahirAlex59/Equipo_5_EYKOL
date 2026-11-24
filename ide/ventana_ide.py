import sys
from pathlib import Path

from PyQt6.QtCore import QPointF, QPoint, QRect, QRectF, QRegularExpression, QSize, Qt
from PyQt6.QtGui import (
    QAction,
    QColor,
    QFont,
    QIcon,
    QKeySequence,
    QPainter,
    QPainterPath,
    QPalette,
    QPen,
    QPixmap,
    QPolygon,
    QRegion,
    QSyntaxHighlighter,
    QTextCharFormat,
    QTextCursor,
    QTextDocument,
    QTextFormat,
)
from PyQt6.QtWidgets import (
    QApplication,
    QDialog,
    QFileDialog,
    QFrame,
    QHBoxLayout,
    QLabel,
    QInputDialog,
    QLineEdit,
    QMainWindow,
    QMessageBox,
    QPlainTextEdit,
    QSizePolicy,
    QSplitter,
    QStackedWidget,
    QTabBar,
    QTableWidgetItem,
    QTabWidget,
    QTextEdit,
    QToolBar,
    QToolButton,
    QTreeWidget,
    QTreeWidgetItem,
    QVBoxLayout,
    QWidget,
)

RUTA_PROYECTO = Path(__file__).resolve().parent.parent
RUTA_EJEMPLOS = RUTA_PROYECTO / "ejemplos"

if str(RUTA_PROYECTO) not in sys.path:
    sys.path.insert(0, str(RUTA_PROYECTO))

from compilador.compilador import compilar
from ide.paneles import (
    crear_tabla_simbolos,
    crear_tabla_tokens,
    llenar_tabla_simbolos,
    llenar_tabla_tokens,
)
from ide.resaltador import ResaltadorEYKOL

# ------------------------------- Paleta ---------------------------------------
# Son los mismos colores que ya usaba el IDE; aqui solo se les pone nombre.
FONDO = "#12131A"
FONDO_BARRA = "#181924"
FONDO_LATERAL = "#14151E"
FONDO_EXPLORADOR = "#161722"
BORDE = "#262837"
TEXTO = "#E5E7EB"
TEXTO_SUAVE = "#D1D5DB"
TEXTO_GRIS = "#9CA3AF"
TEXTO_APAGADO = "#6B7280"
MORADO = "#8B5CF6"
AZUL = "#60A5FA"
VERDE = "#22C55E"
VERDE_SUAVE = "#34D399"
ROJO = "#F87171"
AMARILLO = "#EAB308"

# Colores del codigo (mismos que en ide/resaltador.py)
CODIGO_PALABRA = "#4FC3FF"
CODIGO_NUMERO = "#B5F58A"
CODIGO_CADENA = "#E490F8"

FUENTE_MONO = "'Consolas', 'Cascadia Mono', monospace"

ESTILO_OSCURO = f"""
QMainWindow, QWidget {{
    background-color: {FONDO};
    color: {TEXTO};
    font-family: "Segoe UI", sans-serif;
    font-size: 13px;
}}
QToolTip {{
    background-color: {FONDO_BARRA};
    color: {TEXTO};
    border: 1px solid #2E3044;
    padding: 4px 8px;
}}
QMenu {{
    background-color: {FONDO_BARRA};
    color: {TEXTO};
    border: 1px solid #2E3044;
    border-radius: 8px;
    padding: 5px;
}}
QMenu::item {{
    /* El fondo explicito evita que el estilo de Windows 11 pinte las opciones de negro */
    background-color: transparent;
    padding: 6px 28px 6px 10px;
    border-radius: 5px;
}}
QMenu::item:selected {{
    background-color: #252338;
    color: #FFFFFF;
}}
QMenu::item:disabled {{
    color: {TEXTO_APAGADO};
}}
QMenu::separator {{
    height: 1px;
    background: {BORDE};
    margin: 4px 8px;
}}
QMenu::icon {{
    padding-left: 6px;
}}

/* ---------- Barra superior ---------- */
QToolBar#barraSuperior {{
    background-color: {FONDO_BARRA};
    border: none;
    border-bottom: 1px solid {BORDE};
    spacing: 2px;
    padding: 4px 10px;
}}
QToolBar#barraSuperior QWidget {{
    background: transparent;
}}
QToolButton {{
    background: transparent;
    border: none;
    border-radius: 5px;
    padding: 5px;
}}
QToolButton:hover {{
    background-color: #25273A;
}}
QToolButton::menu-indicator {{
    image: none;
}}
QToolButton#btnEjecutar {{
    background-color: #232A27;
    border: 1px solid #232A27;
    border-radius: 6px;
}}
QToolButton#btnEjecutar:hover {{
    border: 1px solid {VERDE};
}}
QFrame#separadorBarra {{
    background-color: {BORDE};
}}
QLineEdit#campoBuscar {{
    background-color: {FONDO};
    color: {TEXTO};
    border: 1px solid #2E3044;
    border-radius: 6px;
    padding: 5px 10px;
}}
QLineEdit#campoBuscar:focus {{
    border: 1px solid {MORADO};
}}

/* ---------- Franja lateral y explorador ---------- */
QFrame#railLateral {{
    background-color: {FONDO_LATERAL};
    border-right: 1px solid {BORDE};
}}
QFrame#railLateral QToolButton:checked {{
    background-color: #252338;
}}
QFrame#panelExplorador {{
    background-color: {FONDO_EXPLORADOR};
    border: none;
}}
QLabel#tituloExplorador {{
    background-color: {FONDO_EXPLORADOR};
    color: {TEXTO_GRIS};
    font-weight: 600;
    font-size: 12px;
    padding: 10px 12px 6px 12px;
}}
QTreeWidget {{
    background-color: {FONDO_EXPLORADOR};
    color: {TEXTO_SUAVE};
    border: none;
    outline: none;
    padding: 2px 6px;
    show-decoration-selected: 0;
}}
QTreeWidget::item {{
    padding: 5px 6px;
    border-radius: 5px;
}}
QTreeWidget::item:hover {{
    background-color: #1F2130;
}}
QTreeWidget::item:selected {{
    background-color: #252338;
    color: #FFFFFF;
}}

/* ---------- Pestana del editor ---------- */
QFrame#barraTabEditor {{
    background-color: {FONDO};
    border-bottom: 1px solid {BORDE};
}}
QTabBar#pestanasEditor {{
    background: transparent;
}}
/* Pestañas tipo PyCharm: recuadros redondeados, la activa con fondo y borde */
QTabBar#pestanasEditor::tab {{
    background-color: transparent;
    color: {TEXTO_GRIS};
    font-size: 13px;
    height: 28px;
    padding: 0px 4px 0px 10px;
    margin: 0px 3px 0px 0px;
    border: 1px solid transparent;
    border-radius: 7px;
}}
QTabBar#pestanasEditor::tab:selected {{
    background-color: #25273A;
    color: #FFFFFF;
    border: 1px solid #32354E;
}}
QTabBar#pestanasEditor::tab:hover:!selected {{
    background-color: #1F2130;
    color: {TEXTO};
}}
QTabBar#pestanasEditor > QToolButton {{
    background-color: {FONDO};
    border: none;
}}
QWidget#ladoPestana, QWidget#ladoPestana QLabel {{
    background: transparent;
}}
QToolButton#btnNuevaPestana {{
    color: {TEXTO_GRIS};
    font-size: 17px;
    border-radius: 6px;
    padding: 0px 0px 2px 0px;
}}
QToolButton#btnNuevaPestana:hover {{
    background-color: #25273A;
    color: #FFFFFF;
}}
QToolButton#btnCerrarTab {{
    background: transparent;
    color: {TEXTO_APAGADO};
    font-size: 14px;
    border-radius: 4px;
    padding: 0px 0px 1px 0px;
}}
QToolButton#btnCerrarTab:hover {{
    background-color: #32354E;
    color: #FFFFFF;
}}

/* ---------- Editores de texto ---------- */
QPlainTextEdit {{
    background-color: {FONDO};
    color: {TEXTO};
    border: none;
    selection-background-color: #3730A3;
}}
QPlainTextEdit#codigoIntermedio {{
    font-family: {FUENTE_MONO};
    font-size: 10pt;
    padding: 6px 4px;
}}
QPlainTextEdit#salidaTerminal {{
    font-family: {FUENTE_MONO};
    font-size: 10.5pt;
    padding: 10px 14px;
}}

/* ---------- Barras de desplazamiento delgadas (mismos colores del tema) ---------- */
QScrollBar:vertical {{
    background: transparent;
    width: 10px;
    margin: 2px;
}}
QScrollBar:horizontal {{
    background: transparent;
    height: 10px;
    margin: 2px;
}}
QScrollBar::handle:vertical {{
    background: #2E3044;
    border-radius: 3px;
    min-height: 30px;
}}
QScrollBar::handle:horizontal {{
    background: #2E3044;
    border-radius: 3px;
    min-width: 30px;
}}
QScrollBar::handle:hover {{
    background: #32354E;
}}
QScrollBar::add-line, QScrollBar::sub-line {{
    width: 0px;
    height: 0px;
}}
QScrollBar::add-page, QScrollBar::sub-page {{
    background: transparent;
}}
QAbstractScrollArea::corner {{
    background: transparent;
}}

/* ---------- Islas: editor y consola separados (estilo PyCharm) ---------- */
QWidget#zonaIslas {{
    background-color: {FONDO_LATERAL};
}}
QSplitter#divisorIslas {{
    background-color: {FONDO_LATERAL};
}}
QSplitter#divisorIslas::handle {{
    background-color: {FONDO_LATERAL};
}}
QFrame#isla {{
    background-color: {FONDO};
    border: 1px solid {BORDE};
    border-radius: 8px;
}}

/* ---------- Panel inferior ---------- */
QTabWidget#panelInferior::pane {{
    border: none;
    border-top: 1px solid {BORDE};
    background-color: {FONDO};
}}
QTabWidget#panelInferior > QTabBar {{
    background-color: {FONDO_BARRA};
}}
QTabWidget#panelInferior > QTabBar::tab {{
    background-color: {FONDO_BARRA};
    color: {TEXTO_GRIS};
    font-size: 12px;
    font-weight: 500;
    padding: 7px 14px;
    border: none;
    border-right: 1px solid {BORDE};
    border-top: 2px solid transparent;
}}
QTabWidget#panelInferior > QTabBar::tab:selected {{
    background-color: {FONDO};
    color: {TEXTO};
    border-top: 2px solid {MORADO};
}}
QTabWidget#panelInferior > QTabBar::tab:hover:!selected {{
    color: #FFFFFF;
}}
QTreeWidget#arbolSintactico {{
    background-color: {FONDO};
    font-family: {FUENTE_MONO};
    font-size: 10pt;
    padding: 4px;
}}
QTreeWidget#arbolSintactico::item {{
    padding: 2px 4px;
}}
QHeaderView::section {{
    background-color: {FONDO_BARRA};
    color: {TEXTO_GRIS};
    border: none;
    border-bottom: 1px solid {BORDE};
    border-right: 1px solid {BORDE};
    padding: 6px;
    font-weight: bold;
}}
QSplitter::handle {{
    background-color: {BORDE};
}}
QMessageBox QLabel {{
    background: transparent;
}}
QMessageBox QPushButton {{
    background-color: #25273A;
    color: {TEXTO};
    border: 1px solid #2E3044;
    border-radius: 5px;
    padding: 5px 14px;
    min-width: 70px;
}}
QMessageBox QPushButton:hover {{
    background-color: #32354E;
}}

/* ---------- Barra de estado ---------- */
QStatusBar {{
    background-color: {FONDO_BARRA};
    color: {TEXTO_GRIS};
    border-top: 1px solid {BORDE};
    font-size: 12px;
}}
QStatusBar::item {{
    border: none;
}}
QStatusBar QLabel {{
    background: transparent;
}}
"""


# =============================================================================
# Iconos de la franja lateral y del explorador (los mismos de siempre)
# =============================================================================
def _crear_icono(tipo):
    """Iconos de la ventana y del explorador (logo, carpeta y archivo)."""
    pixmap = QPixmap(24, 24)
    pixmap.fill(Qt.GlobalColor.transparent)

    p = QPainter(pixmap)
    p.setRenderHint(QPainter.RenderHint.Antialiasing)

    if tipo == "logo":
        p.setPen(Qt.PenStyle.NoPen)
        p.setBrush(QColor(MORADO))
        p.drawRoundedRect(2, 2, 20, 20, 5, 5)
        p.setPen(QColor("#FFFFFF"))
        p.setFont(QFont("Segoe UI", 12, QFont.Weight.Bold))
        p.drawText(pixmap.rect(), Qt.AlignmentFlag.AlignCenter, "E")

    elif tipo == "folder":
        p.setPen(QPen(QColor(TEXTO_GRIS), 1.6))
        p.setBrush(Qt.BrushStyle.NoBrush)
        carpeta = QPolygon([
            QPoint(3, 6), QPoint(9, 6), QPoint(11, 8),
            QPoint(21, 8), QPoint(21, 18), QPoint(3, 18),
        ])
        p.drawPolygon(carpeta)

    elif tipo == "file":
        p.setPen(QPen(QColor(TEXTO_GRIS), 1.5))
        p.setBrush(Qt.BrushStyle.NoBrush)
        p.drawRect(6, 4, 12, 16)
        p.drawLine(9, 9, 15, 9)
        p.drawLine(9, 13, 15, 13)

    p.end()
    return QIcon(pixmap)


# =============================================================================
# Iconos de la barra superior y de la consola (estilo de contorno, nitidos 2x)
# =============================================================================
def _dibujar_icono(tipo, color=TEXTO_SUAVE, tamano=24):
    escala = 2
    pixmap = QPixmap(tamano * escala, tamano * escala)
    pixmap.setDevicePixelRatio(escala)
    pixmap.fill(Qt.GlobalColor.transparent)

    p = QPainter(pixmap)
    p.setRenderHint(QPainter.RenderHint.Antialiasing)
    p.scale(tamano / 24, tamano / 24)

    lapiz = QPen(QColor(color), 1.7, Qt.PenStyle.SolidLine, Qt.PenCapStyle.RoundCap, Qt.PenJoinStyle.RoundJoin)
    p.setPen(lapiz)
    p.setBrush(Qt.BrushStyle.NoBrush)

    def ruta(*puntos, cerrar=False):
        camino = QPainterPath(QPointF(*puntos[0]))
        for punto in puntos[1:]:
            camino.lineTo(QPointF(*punto))
        if cerrar:
            camino.closeSubpath()
        p.drawPath(camino)

    if tipo == "abrir":
        ruta((3, 6), (9, 6), (11, 8.5), (21, 8.5), (21, 19), (3, 19), cerrar=True)

    elif tipo == "guardar":
        ruta((4, 4), (16.5, 4), (20, 7.5), (20, 20), (4, 20), cerrar=True)
        ruta((8, 4), (8, 9), (15, 9), (15, 4))
        p.drawRoundedRect(QRectF(7.5, 13, 9, 7), 1, 1)

    elif tipo == "buscar":
        p.drawEllipse(QRectF(4, 4, 11, 11))
        p.drawLine(QPointF(13.5, 13.5), QPointF(20, 20))

    elif tipo == "limpiar":
        p.drawLine(QPointF(4, 7), QPointF(20, 7))
        ruta((9, 7), (9, 4.5), (15, 4.5), (15, 7))
        ruta((6, 7), (7, 20), (17, 20), (18, 7))
        p.drawLine(QPointF(10, 10.5), QPointF(10, 16.5))
        p.drawLine(QPointF(14, 10.5), QPointF(14, 16.5))

    elif tipo == "ejecutar":
        p.setPen(QPen(QColor(VERDE), 1.5, Qt.PenStyle.SolidLine, Qt.PenCapStyle.RoundCap, Qt.PenJoinStyle.RoundJoin))
        p.setBrush(QColor(VERDE))
        ruta((7.5, 5), (19, 12), (7.5, 19), cerrar=True)

    elif tipo == "archivo":
        ruta((6, 3), (14, 3), (18, 7), (18, 21), (6, 21), cerrar=True)
        p.drawLine(QPointF(9, 12), QPointF(15, 12))
        p.drawLine(QPointF(9, 16), QPointF(15, 16))

    elif tipo == "nuevo":
        ruta((6, 3), (14, 3), (19, 8), (19, 21), (6, 21), cerrar=True)
        ruta((14, 3), (14, 8), (19, 8))
        p.drawLine(QPointF(12.5, 11.5), QPointF(12.5, 17.5))
        p.drawLine(QPointF(9.5, 14.5), QPointF(15.5, 14.5))

    elif tipo == "pegar":
        ruta((8.5, 5), (6, 5), (6, 21), (18, 21), (18, 5), (15.5, 5))
        p.drawRoundedRect(QRectF(8.5, 3, 7, 4), 1, 1)

    elif tipo == "cortar":
        p.drawEllipse(QRectF(4, 14, 5.5, 5.5))
        p.drawEllipse(QRectF(14.5, 14, 5.5, 5.5))
        p.drawLine(QPointF(8.5, 14.5), QPointF(17, 4))
        p.drawLine(QPointF(15.5, 14.5), QPointF(7, 4))

    elif tipo == "acerca":
        p.drawEllipse(QRectF(3.5, 3.5, 17, 17))
        p.drawLine(QPointF(12, 11), QPointF(12, 16.5))
        p.setPen(Qt.PenStyle.NoPen)
        p.setBrush(QColor(color))
        p.drawEllipse(QPointF(12, 8), 1.2, 1.2)

    elif tipo == "menu":
        for y in (7, 12, 17):
            p.drawLine(QPointF(4, y), QPointF(20, y))

    elif tipo == "analizar":
        p.setPen(QPen(QColor(VERDE), 1.7, Qt.PenStyle.SolidLine, Qt.PenCapStyle.RoundCap, Qt.PenJoinStyle.RoundJoin))
        p.drawEllipse(QRectF(4, 4, 16, 16))
        ruta((8.5, 12.5), (11, 15), (15.8, 9.5))

    elif tipo == "consola":
        ruta((5, 8), (9, 12), (5, 16))
        p.drawLine(QPointF(11, 17), QPointF(19, 17))

    elif tipo == "intermedio":
        p.drawLine(QPointF(4, 6), QPointF(13, 6))
        p.drawLine(QPointF(7, 11), QPointF(20, 11))
        p.drawLine(QPointF(7, 16), QPointF(16, 16))
        p.drawLine(QPointF(4, 21), QPointF(11, 21))

    elif tipo == "arbol":
        p.drawRoundedRect(QRectF(9, 3, 6, 5), 1, 1)
        p.drawRoundedRect(QRectF(3, 16, 6, 5), 1, 1)
        p.drawRoundedRect(QRectF(15, 16, 6, 5), 1, 1)
        ruta((12, 8), (12, 12), (6, 12), (6, 16))
        ruta((12, 12), (18, 12), (18, 16))

    elif tipo == "tokens":
        ruta((4, 4), (12, 4), (20, 12), (12, 20), (4, 12), cerrar=True)
        p.drawEllipse(QPointF(8.5, 8.5), 1.4, 1.4)

    elif tipo == "simbolos":
        p.drawRoundedRect(QRectF(4, 5, 16, 14), 1.5, 1.5)
        p.drawLine(QPointF(4, 10), QPointF(20, 10))
        p.drawLine(QPointF(10, 5), QPointF(10, 19))

    elif tipo == "palabras":
        p.drawRoundedRect(QRectF(4, 4, 16, 16), 3, 3)
        ruta((15, 8), (9.5, 8), (9.5, 16), (15, 16))
        p.drawLine(QPointF(9.5, 12), QPointF(14, 12))

    elif tipo == "copiar":
        p.drawRoundedRect(QRectF(9, 9, 11, 11), 2, 2)
        ruta((15, 5.5), (15, 5), (5, 5), (5, 15), (5.5, 15))

    p.end()
    return pixmap


def _icono_barra(tipo, color=TEXTO_SUAVE):
    return QIcon(_dibujar_icono(tipo, color))


def _separador_vertical():
    linea = QFrame()
    linea.setObjectName("separadorBarra")
    linea.setFixedSize(1, 20)
    return linea


def _espaciador():
    espacio = QWidget()
    espacio.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Preferred)
    return espacio


# =============================================================================
# Editor de codigo
# =============================================================================
class _AreaNumerosLinea(QWidget):
    """Margen izquierdo con el numero de cada linea del editor."""

    def __init__(self, editor):
        super().__init__(editor)
        self.editor = editor

    def sizeHint(self):
        return QSize(self.editor.ancho_numeros_linea(), 0)

    def paintEvent(self, event):
        self.editor.pintar_numeros_linea(event)

    def mousePressEvent(self, event):
        # Clic en el numero: selecciona la linea completa
        cursor = self.editor.cursorForPosition(QPointF(0, event.position().y()).toPoint())
        cursor.movePosition(QTextCursor.MoveOperation.StartOfBlock)
        cursor.movePosition(QTextCursor.MoveOperation.EndOfBlock, QTextCursor.MoveMode.KeepAnchor)
        self.editor.setTextCursor(cursor)
        self.editor.setFocus()


class EditorCodigo(QPlainTextEdit):
    """Editor con numeros de linea, linea actual resaltada, parentesis emparejados,
    sangria automatica, autocierre de (), [], {}, "" y marcas de error."""

    PARES = {"(": ")", "[": "]", "{": "}", '"': '"'}
    CIERRES = {")", "]", "}", '"'}
    SANGRIA = "    "
    TAMANO_BASE = 11

    def __init__(self, solo_lectura=False, tamano=TAMANO_BASE):
        super().__init__()
        self.tamano_fuente = tamano
        self._marcas_error = []        # [(linea, columna)] 1-based
        self._lineas_error = set()     # numeros de bloque (0-based)

        self.area_numeros = _AreaNumerosLinea(self)
        self.setLineWrapMode(QPlainTextEdit.LineWrapMode.NoWrap)
        self.setReadOnly(solo_lectura)
        if not solo_lectura:
            self.setPlaceholderText("Escribe tu código EYKOL aquí...")

        self.blockCountChanged.connect(self._actualizar_margen)
        self.updateRequest.connect(self._actualizar_area_numeros)
        self.cursorPositionChanged.connect(self._actualizar_selecciones)
        self.textChanged.connect(self._al_cambiar_texto)

        self.aplicar_tamano(tamano)
        self._actualizar_selecciones()

    # ------------------------------ Fuente y zoom ----------------------------
    def aplicar_tamano(self, tamano):
        self.tamano_fuente = max(7, min(32, tamano))
        self.setStyleSheet(
            f"QPlainTextEdit {{ font-family: {FUENTE_MONO}; font-size: {self.tamano_fuente}pt; }}"
        )
        self.ensurePolished()
        self.setTabStopDistance(self.fontMetrics().horizontalAdvance(" ") * 4)
        self._actualizar_margen(0)
        self._reubicar_area_numeros()
        self.area_numeros.update()

    def acercar(self):
        self.aplicar_tamano(self.tamano_fuente + 1)

    def alejar(self):
        self.aplicar_tamano(self.tamano_fuente - 1)

    def wheelEvent(self, event):
        if event.modifiers() & Qt.KeyboardModifier.ControlModifier:
            if event.angleDelta().y() > 0:
                self.acercar()
            elif event.angleDelta().y() < 0:
                self.alejar()
            event.accept()
            return
        super().wheelEvent(event)

    # ------------------------------ Numeros de linea -------------------------
    def ancho_numeros_linea(self):
        digitos = len(str(max(1, self.blockCount())))
        return 24 + self.fontMetrics().horizontalAdvance("9") * max(2, digitos)

    def _actualizar_margen(self, _):
        self.setViewportMargins(self.ancho_numeros_linea(), 0, 0, 0)

    def _actualizar_area_numeros(self, rect, dy):
        if dy:
            self.area_numeros.scroll(0, dy)
        else:
            self.area_numeros.update(0, rect.y(), self.area_numeros.width(), rect.height())
        if rect.contains(self.viewport().rect()):
            self._actualizar_margen(0)

    def _reubicar_area_numeros(self):
        contenido = self.contentsRect()
        self.area_numeros.setGeometry(
            QRect(contenido.left(), contenido.top(), self.ancho_numeros_linea(), contenido.height())
        )

    def resizeEvent(self, event):
        super().resizeEvent(event)
        self._reubicar_area_numeros()

    def pintar_numeros_linea(self, event):
        painter = QPainter(self.area_numeros)
        painter.fillRect(event.rect(), QColor(FONDO))
        painter.setFont(self.font())

        bloque = self.firstVisibleBlock()
        numero = bloque.blockNumber()
        linea_actual = self.textCursor().blockNumber()
        top = round(self.blockBoundingGeometry(bloque).translated(self.contentOffset()).top())
        bottom = top + round(self.blockBoundingRect(bloque).height())
        alto = self.fontMetrics().height()

        while bloque.isValid() and top <= event.rect().bottom():
            if bloque.isVisible() and bottom >= event.rect().top():
                if numero in self._lineas_error:
                    painter.setPen(QPen(QColor(ROJO)))
                    painter.setBrush(QColor(ROJO))
                    painter.drawEllipse(QPointF(7, top + alto / 2), 2.5, 2.5)
                elif numero == linea_actual and not self.isReadOnly():
                    painter.setPen(QColor(TEXTO))
                else:
                    painter.setPen(QColor(TEXTO_APAGADO))
                painter.drawText(
                    0, top, self.area_numeros.width() - 10, alto,
                    Qt.AlignmentFlag.AlignRight | Qt.AlignmentFlag.AlignVCenter,
                    str(numero + 1),
                )
            bloque = bloque.next()
            top = bottom
            bottom = top + round(self.blockBoundingRect(bloque).height())
            numero += 1

    # ------------------------------ Resaltados -------------------------------
    def marcar_errores(self, marcas):
        """marcas: lista de (linea, columna) 1-based; columna puede ser None."""
        self._marcas_error = [(l, c) for l, c in marcas if l]
        self._lineas_error = {l - 1 for l, _ in self._marcas_error}
        self._actualizar_selecciones()

    def limpiar_errores(self):
        if self._marcas_error:
            self._marcas_error = []
            self._lineas_error = set()
            self._actualizar_selecciones()

    def _al_cambiar_texto(self):
        # Al editar, las marcas de la compilacion anterior ya no son validas
        self.limpiar_errores()

    def _seleccion(self, cursor, fondo=None, texto=None, negrita=False, linea_completa=False):
        sel = QTextEdit.ExtraSelection()
        if fondo is not None:
            sel.format.setBackground(QColor(fondo))
        if texto is not None:
            sel.format.setForeground(QColor(texto))
        if negrita:
            sel.format.setFontWeight(QFont.Weight.Bold)
        if linea_completa:
            sel.format.setProperty(QTextFormat.Property.FullWidthSelection, True)
        sel.cursor = cursor
        return sel

    def _actualizar_selecciones(self):
        selecciones = []

        if not self.isReadOnly():
            cursor = self.textCursor()
            cursor.clearSelection()
            selecciones.append(self._seleccion(cursor, fondo="#202235", linea_completa=True))

        documento = self.document()
        for linea, columna in self._marcas_error:
            bloque = documento.findBlockByNumber(linea - 1)
            if not bloque.isValid():
                continue
            cursor = QTextCursor(bloque)
            selecciones.append(self._seleccion(cursor, fondo=QColor(248, 113, 113, 34), linea_completa=True))
            if columna:
                texto = bloque.text()
                inicio = min(max(columna - 1, 0), len(texto))
                fin = inicio + 1
                while fin < len(texto) and (texto[fin].isalnum() or texto[fin] == "_") and texto[inicio].isalnum():
                    fin += 1
                if inicio < len(texto):
                    subrayado = QTextCursor(bloque)
                    subrayado.setPosition(bloque.position() + inicio)
                    subrayado.setPosition(bloque.position() + fin, QTextCursor.MoveMode.KeepAnchor)
                    sel = QTextEdit.ExtraSelection()
                    sel.format.setUnderlineStyle(QTextCharFormat.UnderlineStyle.WaveUnderline)
                    sel.format.setUnderlineColor(QColor(ROJO))
                    sel.cursor = subrayado
                    selecciones.append(sel)

        if not self.isReadOnly():
            selecciones.extend(self._selecciones_parentesis())

        self.setExtraSelections(selecciones)
        self.area_numeros.update()

    def _selecciones_parentesis(self):
        texto = self.toPlainText()
        posicion = self.textCursor().position()
        abre, cierra = "([{", ")]}"
        for p in (posicion, posicion - 1):
            if not (0 <= p < len(texto)) or texto[p] not in abre + cierra:
                continue
            caracter = texto[p]
            if caracter in abre:
                pareja, paso = cierra[abre.index(caracter)], 1
            else:
                pareja, paso = abre[cierra.index(caracter)], -1
            nivel, i = 0, p
            while 0 <= i < len(texto):
                if texto[i] == caracter:
                    nivel += 1
                elif texto[i] == pareja:
                    nivel -= 1
                    if nivel == 0:
                        return [self._marcar_caracter(p, "#2E3044", "#FFFFFF"),
                                self._marcar_caracter(i, "#2E3044", "#FFFFFF")]
                i += paso
            return [self._marcar_caracter(p, None, ROJO)]
        return []

    def _marcar_caracter(self, posicion, fondo, color):
        cursor = QTextCursor(self.document())
        cursor.setPosition(posicion)
        cursor.setPosition(posicion + 1, QTextCursor.MoveMode.KeepAnchor)
        return self._seleccion(cursor, fondo=fondo, texto=color, negrita=True)

    def ir_a(self, linea, columna=None):
        bloque = self.document().findBlockByNumber(max(linea - 1, 0))
        if not bloque.isValid():
            return
        cursor = QTextCursor(bloque)
        if columna:
            cursor.setPosition(bloque.position() + min(columna - 1, len(bloque.text())))
        self.setTextCursor(cursor)
        self.centerCursor()
        self.setFocus()

    # ------------------------------ Escritura asistida -----------------------
    def _caracter(self, desplazamiento):
        posicion = self.textCursor().position() + desplazamiento
        documento = self.document()
        if 0 <= posicion < documento.characterCount() - 1:
            return documento.characterAt(posicion)
        return ""

    def keyPressEvent(self, event):
        if self.isReadOnly():
            super().keyPressEvent(event)
            return

        tecla = event.key()
        texto = event.text()
        cursor = self.textCursor()

        if tecla in (Qt.Key.Key_Return, Qt.Key.Key_Enter):
            self._nueva_linea_con_sangria()
            return

        if tecla == Qt.Key.Key_Tab:
            if cursor.hasSelection() and " " in cursor.selectedText():
                self.cambiar_sangria(True)
            else:
                cursor.insertText(self.SANGRIA)
            return

        if tecla == Qt.Key.Key_Backtab:
            self.cambiar_sangria(False)
            return

        if tecla == Qt.Key.Key_Backspace and not cursor.hasSelection():
            antes, despues = self._caracter(-1), self._caracter(0)
            if antes in self.PARES and self.PARES[antes] == despues:
                cursor.beginEditBlock()
                cursor.deletePreviousChar()
                cursor.deleteChar()
                cursor.endEditBlock()
                return
            previo = cursor.block().text()[:cursor.positionInBlock()]
            if previo and previo.strip(" ") == "":
                cantidad = len(previo) % 4 or 4
                cursor.beginEditBlock()
                for _ in range(cantidad):
                    cursor.deletePreviousChar()
                cursor.endEditBlock()
                return

        if texto and texto in self.CIERRES and not cursor.hasSelection() and self._caracter(0) == texto:
            cursor.movePosition(QTextCursor.MoveOperation.Right)
            self.setTextCursor(cursor)
            return

        if texto and texto in self.PARES:
            if cursor.hasSelection():
                seleccionado = cursor.selectedText()
                cursor.insertText(texto + seleccionado + self.PARES[texto])
                return
            siguiente = self._caracter(0)
            if siguiente in ("", " ", "\t", " ", ")", "]", "}", ";", ","):
                cursor.insertText(texto + self.PARES[texto])
                cursor.movePosition(QTextCursor.MoveOperation.Left)
                self.setTextCursor(cursor)
                return

        if texto == "}":
            previo = cursor.block().text()[:cursor.positionInBlock()]
            if previo.strip() == "" and len(previo) >= len(self.SANGRIA):
                cursor.beginEditBlock()
                for _ in range(len(self.SANGRIA)):
                    cursor.deletePreviousChar()
                cursor.insertText("}")
                cursor.endEditBlock()
                return

        super().keyPressEvent(event)

    def _nueva_linea_con_sangria(self):
        cursor = self.textCursor()
        previo = cursor.block().text()[:cursor.positionInBlock()]
        sangria = previo[:len(previo) - len(previo.lstrip())]
        extra = self.SANGRIA if previo.rstrip().endswith("{") else ""

        cursor.beginEditBlock()
        cursor.insertText("\n" + sangria + extra)
        if extra and self._caracter(0) == "}":
            posicion = cursor.position()
            cursor.insertText("\n" + sangria)
            cursor.setPosition(posicion)
        cursor.endEditBlock()
        self.setTextCursor(cursor)
        self.ensureCursorVisible()

    def _bloques_seleccionados(self):
        cursor = self.textCursor()
        documento = self.document()
        inicio = documento.findBlock(cursor.selectionStart())
        fin = documento.findBlock(cursor.selectionEnd())
        if cursor.hasSelection() and fin.blockNumber() > inicio.blockNumber() and cursor.selectionEnd() == fin.position():
            fin = fin.previous()
        bloques = []
        bloque = inicio
        while bloque.isValid() and bloque.blockNumber() <= fin.blockNumber():
            bloques.append(bloque)
            bloque = bloque.next()
        return bloques

    def cambiar_sangria(self, aumentar):
        cursor = self.textCursor()
        cursor.beginEditBlock()
        for bloque in self._bloques_seleccionados():
            c = QTextCursor(bloque)
            if aumentar:
                c.insertText(self.SANGRIA)
            else:
                texto = bloque.text()
                cantidad = min(len(texto) - len(texto.lstrip(" ")), len(self.SANGRIA))
                if cantidad:
                    c.movePosition(QTextCursor.MoveOperation.Right, QTextCursor.MoveMode.KeepAnchor, cantidad)
                    c.removeSelectedText()
        cursor.endEditBlock()

    def alternar_comentario(self):
        bloques = [b for b in self._bloques_seleccionados() if b.text().strip()]
        if not bloques or self.isReadOnly():
            return
        todos_comentados = all(b.text().lstrip().startswith("//") for b in bloques)
        sangria_min = min(len(b.text()) - len(b.text().lstrip()) for b in bloques)

        cursor = self.textCursor()
        cursor.beginEditBlock()
        for bloque in bloques:
            texto = bloque.text()
            c = QTextCursor(bloque)
            if todos_comentados:
                inicio = texto.index("//")
                largo = 3 if texto[inicio:inicio + 3] == "// " else 2
                c.setPosition(bloque.position() + inicio)
                c.setPosition(bloque.position() + inicio + largo, QTextCursor.MoveMode.KeepAnchor)
                c.removeSelectedText()
            else:
                c.setPosition(bloque.position() + sangria_min)
                c.insertText("// ")
        cursor.endEditBlock()


class ResaltadorIntermedio(QSyntaxHighlighter):
    """Colorea el codigo de tres direcciones (etiquetas, saltos, temporales)."""

    def __init__(self, documento):
        super().__init__(documento)

        def fmt(color, negrita=False):
            f = QTextCharFormat()
            f.setForeground(QColor(color))
            if negrita:
                f.setFontWeight(QFont.Weight.Bold)
            return f

        self.reglas = [
            (QRegularExpression(r"\b\d+(\.\d+)?\b"), fmt(CODIGO_NUMERO)),
            (QRegularExpression(r"\bt\d+\b"), fmt(MORADO)),
            (QRegularExpression(r"\b(if_false|if|goto|impt|param|call|return)\b"), fmt(CODIGO_PALABRA, True)),
            (QRegularExpression(r"^\s*L\d+:"), fmt(AMARILLO, True)),
            (QRegularExpression(r"\bL\d+\b"), fmt(AMARILLO)),
            (QRegularExpression(r'"[^"\n]*"'), fmt(CODIGO_CADENA)),
        ]

    def highlightBlock(self, texto):
        for patron, formato in self.reglas:
            iterador = patron.globalMatch(texto)
            while iterador.hasNext():
                m = iterador.next()
                self.setFormat(m.capturedStart(), m.capturedLength(), formato)


# =============================================================================
# Ventana principal
# =============================================================================
class _Documento:
    """Una pestaña del editor: su propio editor y su archivo."""

    def __init__(self, nombre_nuevo):
        self.editor = EditorCodigo()
        self.resaltador = ResaltadorEYKOL(self.editor.document())
        self.archivo = None                 # Path del archivo, o None si no se ha guardado
        self.nombre_nuevo = nombre_nuevo    # "Sin título 2.txt" mientras no tenga archivo
        self.punto = QLabel("●")            # indicador de cambios sin guardar en la pestaña
        self.punto.setStyleSheet(f"color: {AMARILLO}; font-size: 10px;")
        self.punto.setToolTip("Cambios sin guardar")
        politica = self.punto.sizePolicy()
        politica.setRetainSizeWhenHidden(True)   # la × no se mueve al aparecer el punto
        self.punto.setSizePolicy(politica)

    @property
    def nombre(self):
        return self.archivo.name if self.archivo else self.nombre_nuevo

    @property
    def modificado(self):
        return self.editor.document().isModified()

    def esta_vacio(self):
        """Pestaña nueva sin tocar: se puede reutilizar al abrir un archivo."""
        return self.archivo is None and not self.modificado and not self.editor.toPlainText()


class _Isla(QFrame):
    """Panel con esquinas redondeadas y separado de los demas (estilo PyCharm)."""

    RADIO = 8

    def __init__(self, contenido):
        super().__init__()
        self.setObjectName("isla")
        layout = QVBoxLayout(self)
        layout.setContentsMargins(1, 1, 1, 1)
        layout.setSpacing(0)
        layout.addWidget(contenido)

    def resizeEvent(self, event):
        super().resizeEvent(event)
        # La mascara recorta tambien a los hijos, asi las esquinas quedan redondas
        camino = QPainterPath()
        camino.addRoundedRect(QRectF(self.rect()), self.RADIO, self.RADIO)
        self.setMask(QRegion(camino.toFillPolygon().toPolygon()))


class VentanaIDE(QMainWindow):

    def __init__(self):
        super().__init__()

        self.setMinimumSize(900, 560)
        self._centrar_en_pantalla()
        self.setStyleSheet(ESTILO_OSCURO)
        self.setWindowIcon(_crear_icono("logo"))

        self._documentos = []                 # pestañas abiertas (_Documento)
        self._documento_ejecutado = None      # pestaña cuya salida esta en la consola
        self._tamano_editor = EditorCodigo.TAMANO_BASE
        self._enlaces_consola = {}    # bloque de la consola -> (linea, columna) del error

        self._crear_acciones()
        self._crear_barra_superior()
        self._construir_interfaz()
        self._crear_barra_estado()

        self._cargar_explorador()
        self._mensaje_inicial_consola()
        self._actualizar_titulo()
        self._abrir_archivo_inicial()

    def _centrar_en_pantalla(self):
        """Tamaño proporcional a la pantalla y ventana centrada (no pegada arriba)."""
        pantalla = QApplication.primaryScreen()
        if pantalla is None:
            self.resize(1240, 800)
            return
        area = pantalla.availableGeometry()
        ancho = min(1400, int(area.width() * 0.88))
        alto = min(880, int(area.height() * 0.88))
        self.resize(ancho, alto)
        # Se descuenta la barra de titulo de Windows (~32 px) para que quede centrada a la vista
        x = area.x() + (area.width() - ancho) // 2
        y = area.y() + max(0, (area.height() - alto - 32) // 2)
        self.move(x, y)

    # ---------------------------- Pestaña actual -----------------------------
    # El resto del IDE usa self.editor / self.archivo_actual como antes; ahora
    # siempre se refieren a la pestaña que esta abierta.
    @property
    def documento(self):
        return self.barra_pestanas.tabData(self.barra_pestanas.currentIndex())

    @property
    def editor(self):
        return self.documento.editor

    @property
    def archivo_actual(self):
        return self.documento.archivo

    @archivo_actual.setter
    def archivo_actual(self, valor):
        doc = self.documento
        doc.archivo = valor
        if valor is None and not doc.nombre_nuevo:
            doc.nombre_nuevo = self._nombre_libre(excepto=doc)

    # ---------------------------- Acciones -----------------------------------
    def _accion(self, icono, texto, atajo, funcion, en_ventana=True):
        """Crea una accion con icono, tooltip (con su atajo) y conexion."""
        accion = QAction(icono or QIcon(), texto, self)
        if atajo:
            secuencia = QKeySequence(atajo)
            texto_atajo = secuencia.toString(QKeySequence.SequenceFormat.NativeText)
            accion.setToolTip(f"{texto} ({texto_atajo})")
            accion.setShortcut(secuencia)
            if en_ventana:
                self.addAction(accion)
            else:
                # El atajo solo se muestra en los menus; lo atiende el propio editor
                # (asi Ctrl+C / Ctrl+V siguen funcionando tambien en el buscador)
                accion.setShortcutContext(Qt.ShortcutContext.WidgetShortcut)
        else:
            accion.setToolTip(texto)
        accion.triggered.connect(funcion)
        return accion

    def _crear_acciones(self):
        # --- Barra izquierda (iconos de contorno) ---
        self.accion_nuevo = self._accion(_icono_barra("nuevo"), "Nuevo documento", "Ctrl+N", self.nuevo_documento)
        self.accion_explorador = self._accion(_icono_barra("abrir"), "Explorador", "Ctrl+B",
                                              self.alternar_explorador)
        self.accion_explorador.setCheckable(True)
        self.accion_explorador.setChecked(True)
        self.accion_guardar = self._accion(_icono_barra("guardar"), "Guardar archivo", "Ctrl+S", self.guardar_archivo)
        # Copiar / pegar / cortar usan el teclado propio del editor (asi tambien
        # funcionan dentro del buscador); el boton solo actua sobre el editor.
        self.accion_copiar = self._accion(_icono_barra("copiar"), "Copiar texto seleccionado", "Ctrl+C",
                                          self.editor_copiar, en_ventana=False)
        self.accion_pegar = self._accion(_icono_barra("pegar"), "Pegar texto", "Ctrl+V",
                                         self.editor_pegar, en_ventana=False)
        self.accion_cortar = self._accion(_icono_barra("cortar"), "Cortar texto seleccionado", "Ctrl+X",
                                          self.editor_cortar, en_ventana=False)
        self.accion_acerca = self._accion(_icono_barra("acerca"), "Acerca de EYKOL IDE", "F1", self.mostrar_acerca)
        self.accion_palabras = self._accion(_icono_barra("palabras"), "Palabras reservadas de EYKOL", None,
                                            self.mostrar_palabras_reservadas)

        # --- Barra superior ---
        self.accion_abrir = self._accion(_icono_barra("abrir"), "Abrir archivo", "Ctrl+O", self.abrir_archivo)
        self.accion_limpiar = self._accion(_icono_barra("limpiar"), "Limpiar editor y resultados", None,
                                           self.limpiar_editor)
        self.accion_ejecutar = self._accion(_icono_barra("ejecutar"), "Ejecutar código", "F5", self.ejecutar_codigo)
        self.accion_analizar = self._accion(_icono_barra("analizar"), "Analizar sin ejecutar", "Shift+F5",
                                            self.analizar_codigo)
        self.accion_guardar_como = self._accion(None, "Guardar como", "Ctrl+Shift+S", self.guardar_como)
        self.accion_comentar = self._accion(None, "Comentar / descomentar", "Ctrl+/",
                                            lambda: self.editor.alternar_comentario())
        self.accion_buscar = self._accion(None, "Buscar", "Ctrl+F", self._enfocar_buscador)
        self.accion_consola = self._accion(None, "Mostrar / ocultar consola", "Ctrl+J", self.alternar_panel)
        self.accion_limpiar_consola = self._accion(None, "Limpiar consola", "Ctrl+L", self._mensaje_inicial_consola)
        self.accion_acercar = self._accion(None, "Aumentar zoom", "Ctrl++", lambda: self._zoom(1))
        self.accion_alejar = self._accion(None, "Reducir zoom", "Ctrl+-", lambda: self._zoom(-1))
        self.accion_zoom_base = self._accion(None, "Restablecer zoom", "Ctrl+0", lambda: self._zoom(0))
        self.accion_nueva_pestana = self._accion(None, "Nueva pestaña", "Ctrl+T", self.nuevo_documento)
        self.accion_cerrar_pestana = self._accion(None, "Cerrar pestaña", "Ctrl+W", lambda: self.cerrar_pestana())
        self.accion_salir = self._accion(None, "Salir", "Ctrl+Q", self.close)

        # --- Editor (los atajos los maneja el propio editor; aqui solo se muestran) ---
        self.accion_deshacer = self._accion(None, "Deshacer", "Ctrl+Z", lambda: self.editor.undo(), en_ventana=False)
        self.accion_rehacer = self._accion(None, "Rehacer", "Ctrl+Y", lambda: self.editor.redo(), en_ventana=False)
        self.accion_seleccionar = self._accion(None, "Seleccionar todo", "Ctrl+A",
                                               lambda: self.editor.selectAll(), en_ventana=False)
        self.accion_sangria_mas = self._accion(None, "Aumentar sangría", "Tab",
                                               lambda: self.editor.cambiar_sangria(True), en_ventana=False)
        self.accion_sangria_menos = self._accion(None, "Reducir sangría", "Shift+Tab",
                                                 lambda: self.editor.cambiar_sangria(False), en_ventana=False)

        # --- Navegacion ---
        self.accion_ir_linea = self._accion(None, "Ir a línea…", "Ctrl+G", self.ir_a_linea)
        self.accion_buscar_sig = self._accion(None, "Buscar siguiente", "F3", self.buscar_texto)
        self.accion_buscar_ant = self._accion(None, "Buscar anterior", "Shift+F3", lambda: self.buscar_texto(atras=True))
        self.accion_pestana_sig = self._accion(None, "Pestaña siguiente", "Ctrl+Tab", lambda: self._cambiar_pestana(1))
        self.accion_pestana_ant = self._accion(None, "Pestaña anterior", "Ctrl+Shift+Tab",
                                               lambda: self._cambiar_pestana(-1))
        self.accion_error = self._accion(None, "Ir al primer error", "F2", self.ir_al_primer_error)

        # --- Solo atajos de teclado ---
        self._accion(None, "Ejecutar código", "Ctrl+Return", self.ejecutar_codigo)
        self._accion(None, "Aumentar zoom", "Ctrl+=", lambda: self._zoom(1))

    # ---------------------------- Barra superior -----------------------------
    def _crear_barra_superior(self):
        barra = QToolBar("Herramientas", self)
        barra.setObjectName("barraSuperior")
        barra.setMovable(False)
        barra.setFloatable(False)
        barra.setIconSize(QSize(18, 18))
        barra.setContextMenuPolicy(Qt.ContextMenuPolicy.PreventContextMenu)
        self.addToolBar(barra)

        # ----- Izquierda: insignia [E] + EYKOL -----
        marca = QWidget()
        layout_marca = QHBoxLayout(marca)
        layout_marca.setContentsMargins(2, 0, 8, 0)
        layout_marca.setSpacing(8)

        icono_e = QLabel()
        icono_e.setPixmap(_crear_icono("logo").pixmap(22, 22))
        texto_eykol = QLabel("EYKOL")
        texto_eykol.setStyleSheet("font-weight: bold; font-size: 13px; color: #FFFFFF; background: transparent;")
        layout_marca.addWidget(icono_e)
        layout_marca.addWidget(texto_eykol)
        barra.addWidget(marca)

        barra.addWidget(_espaciador())

        # Buscador al centro
        self.campo_buscar = QLineEdit()
        self.campo_buscar.setObjectName("campoBuscar")
        self.campo_buscar.setFixedWidth(300)
        self.campo_buscar.setPlaceholderText("Buscar en el código...  (Ctrl+F)")
        self.campo_buscar.addAction(_icono_barra("buscar", TEXTO_APAGADO), QLineEdit.ActionPosition.LeadingPosition)
        self.campo_buscar.setClearButtonEnabled(True)
        self.campo_buscar.returnPressed.connect(self.buscar_texto)
        self.campo_buscar.textChanged.connect(self._contar_coincidencias)
        self.campo_buscar.installEventFilter(self)
        barra.addWidget(self.campo_buscar)

        barra.addWidget(_espaciador())

        # Derecha: Limpiar (bote de basura) | ▶ Ejecutar
        boton_limpiar = QToolButton()
        boton_limpiar.setDefaultAction(self.accion_limpiar)
        boton_limpiar.setIconSize(QSize(18, 18))
        boton_limpiar.setFixedSize(32, 32)
        boton_limpiar.setCursor(Qt.CursorShape.PointingHandCursor)
        barra.addWidget(boton_limpiar)

        barra.addWidget(_separador_vertical())

        self.boton_ejecutar = QToolButton()
        self.boton_ejecutar.setObjectName("btnEjecutar")
        self.boton_ejecutar.setDefaultAction(self.accion_ejecutar)
        self.boton_ejecutar.setIconSize(QSize(18, 18))
        self.boton_ejecutar.setFixedSize(34, 32)
        self.boton_ejecutar.setCursor(Qt.CursorShape.PointingHandCursor)
        barra.addWidget(self.boton_ejecutar)

    def ir_a_linea(self):
        total = self.editor.blockCount()
        actual = self.editor.textCursor().blockNumber() + 1
        dialogo = QInputDialog(self)
        dialogo.setWindowTitle("Ir a línea")
        dialogo.setLabelText(f"Línea (1 – {total}):")
        dialogo.setInputMode(QInputDialog.InputMode.IntInput)
        dialogo.setIntRange(1, total)
        dialogo.setIntValue(actual)
        dialogo.setOkButtonText("Aceptar")
        dialogo.setCancelButtonText("Cancelar")
        if dialogo.exec():
            self.editor.ir_a(dialogo.intValue())

    def ir_al_primer_error(self):
        """Lleva al primer error de la ultima ejecucion (en su pestaña)."""
        if not self._enlaces_consola:
            self._poner_estado("No hay errores con ubicación en la última ejecución.", TEXTO_GRIS)
            return
        indice = self._indice_de(self._documento_ejecutado)
        if indice >= 0:
            self.barra_pestanas.setCurrentIndex(indice)
        bloque = min(self._enlaces_consola)
        self.editor.ir_a(*self._enlaces_consola[bloque])

    def eventFilter(self, objeto, evento):
        # Esc en el buscador regresa al editor
        if objeto is self.campo_buscar and evento.type() == evento.Type.KeyPress:
            if evento.key() == Qt.Key.Key_Escape:
                self.editor.setFocus()
                return True

        # Consola: las ubicaciones de error son enlaces que llevan a la linea
        if hasattr(self, "salida") and objeto is self.salida.viewport():
            tipo = evento.type()
            if tipo in (evento.Type.MouseMove, evento.Type.MouseButtonRelease):
                bloque = self.salida.cursorForPosition(evento.position().toPoint()).blockNumber()
                enlace = self._enlaces_consola.get(bloque)
                if tipo == evento.Type.MouseMove:
                    forma = Qt.CursorShape.PointingHandCursor if enlace else Qt.CursorShape.IBeamCursor
                    self.salida.viewport().setCursor(forma)
                elif (enlace and evento.button() == Qt.MouseButton.LeftButton
                      and not self.salida.textCursor().hasSelection()):
                    # El error es de la pestaña que se ejecuto: primero se cambia a ella
                    indice = self._indice_de(self._documento_ejecutado)
                    if indice >= 0:
                        self.barra_pestanas.setCurrentIndex(indice)
                    self.editor.ir_a(*enlace)
        return super().eventFilter(objeto, evento)

    # ---------------------------- Interfaz principal -------------------------
    def _construir_interfaz(self):
        central = QWidget()
        self.setCentralWidget(central)

        layout_principal = QHBoxLayout(central)
        layout_principal.setContentsMargins(0, 0, 0, 0)
        layout_principal.setSpacing(0)

        layout_principal.addWidget(self._crear_rail())

        # Explorador, editor y consola como "islas" separadas
        zona_islas = QWidget()
        zona_islas.setObjectName("zonaIslas")
        layout_islas = QVBoxLayout(zona_islas)
        layout_islas.setContentsMargins(6, 6, 6, 6)
        layout_islas.setSpacing(0)

        # Explorador a la izquierda (toda la altura); editor + consola apilados a la derecha
        self.divisor_v = QSplitter(Qt.Orientation.Vertical)
        self.divisor_v.setObjectName("divisorIslas")
        self.divisor_v.setHandleWidth(6)
        self.divisor_v.setChildrenCollapsible(False)
        self.divisor_v.addWidget(_Isla(self._crear_panel_editor()))
        self.isla_consola = _Isla(self._crear_panel_inferior())
        self.divisor_v.addWidget(self.isla_consola)
        self.divisor_v.setStretchFactor(0, 3)
        self.divisor_v.setStretchFactor(1, 2)
        self.divisor_v.setSizes([460, 260])

        self.divisor_h = QSplitter(Qt.Orientation.Horizontal)
        self.divisor_h.setObjectName("divisorIslas")
        self.divisor_h.setHandleWidth(6)
        self.divisor_h.setChildrenCollapsible(False)
        self.isla_explorador = _Isla(self._crear_explorador())
        self.divisor_h.addWidget(self.isla_explorador)
        self.divisor_h.addWidget(self.divisor_v)
        self.divisor_h.setStretchFactor(1, 1)
        self.divisor_h.setSizes([235, 965])
        layout_islas.addWidget(self.divisor_h)

        layout_principal.addWidget(zona_islas)

    # Herramientas de EYKOL accesibles desde el menu ☰ -> Herramientas:
    # (icono, nombre, pestaña del panel inferior que abren)
    HERRAMIENTAS_EYKOL = (
        ("consola", "Terminal", 0),
        ("tokens", "Tokens", 1),
        ("simbolos", "Tabla de símbolos", 2),
        ("intermedio", "Código intermedio", 3),
        ("arbol", "Árbol sintáctico", 4),
    )

    def _crear_rail(self):
        """Barra izquierda con los 7 botones principales: Nuevo, Explorador, Guardar |
        Copiar, Pegar, Cortar | Acerca de."""
        rail = QFrame()
        rail.setObjectName("railLateral")
        rail.setFixedWidth(44)
        layout_rail = QVBoxLayout(rail)
        layout_rail.setContentsMargins(6, 10, 6, 10)
        layout_rail.setSpacing(6)

        def separador():
            linea = QFrame()
            linea.setFixedHeight(1)
            linea.setStyleSheet(f"background-color: {BORDE};")
            layout_rail.addWidget(linea)

        def boton_de(accion):
            boton = QToolButton(rail)
            boton.setDefaultAction(accion)
            boton.setFixedSize(32, 32)
            boton.setIconSize(QSize(18, 18))
            boton.setCursor(Qt.CursorShape.PointingHandCursor)
            layout_rail.addWidget(boton)
            return boton

        for accion in (self.accion_nuevo, self.accion_explorador, self.accion_guardar):
            boton_de(accion)
        separador()
        for accion in (self.accion_copiar, self.accion_pegar, self.accion_cortar):
            boton_de(accion)
        separador()
        boton_de(self.accion_acerca)

        layout_rail.addStretch()
        return rail

    def _mostrar_herramienta(self, indice):
        self.isla_consola.setVisible(True)
        self.pestanas.setCurrentIndex(indice)

    def mostrar_palabras_reservadas(self):
        """Ventana con las palabras reservadas de EYKOL. Doble clic: la inserta en el editor."""
        from compilador.lexico import reservadas
        significados = {
            "ent": "Tipo entero", "deci": "Tipo decimal", "txt": "Tipo texto", "boli": "Tipo booleano",
            "si": "Condición (if)", "osi": "Si no (else)", "durante": "Ciclo mientras (while)",
            "repetir": "Ciclo para (for)", "impt": "Imprimir en la consola", "vrd": "Valor verdadero",
            "fals": "Valor falso", "raiz": "Raíz cuadrada",
        }
        dialogo = QDialog(self)
        dialogo.setWindowTitle("Palabras reservadas de EYKOL")
        dialogo.resize(460, 420)
        layout = QVBoxLayout(dialogo)
        layout.setContentsMargins(0, 0, 0, 0)
        tabla = crear_tabla_tokens()          # misma tabla oscura que el panel de tokens
        tabla.setHorizontalHeaderLabels(["Palabra", "Token", "Significado"])
        tabla.setRowCount(len(reservadas))
        for fila, (palabra, token) in enumerate(reservadas.items()):
            for columna, valor in enumerate((palabra, token, significados.get(palabra, ""))):
                tabla.setItem(fila, columna, QTableWidgetItem(valor))
        tabla.setToolTip("Doble clic para insertar la palabra en el editor")

        def insertar(fila, _columna):
            self.editor.insertPlainText(tabla.item(fila, 0).text())
            self.editor.setFocus()
            dialogo.accept()

        tabla.cellDoubleClicked.connect(insertar)
        layout.addWidget(tabla)
        dialogo.exec()

    def _crear_explorador(self):
        """Panel izquierdo: Explorador (igual que antes)."""
        self.panel_explorador = QFrame()
        self.panel_explorador.setObjectName("panelExplorador")
        self.panel_explorador.setMinimumWidth(215)
        self.panel_explorador.setMaximumWidth(300)
        layout_exp = QVBoxLayout(self.panel_explorador)
        layout_exp.setContentsMargins(0, 0, 0, 0)
        layout_exp.setSpacing(0)

        titulo_exp = QLabel("Explorador")
        titulo_exp.setObjectName("tituloExplorador")
        layout_exp.addWidget(titulo_exp)

        self.explorador = QTreeWidget()
        self.explorador.setHeaderHidden(True)
        self.explorador.setIconSize(QSize(16, 16))
        self.explorador.setIndentation(14)
        # Mismo color de seleccion en la zona de la flecha que en el nombre (una sola franja)
        paleta = self.explorador.palette()
        for grupo in (QPalette.ColorGroup.Active, QPalette.ColorGroup.Inactive):
            paleta.setColor(grupo, QPalette.ColorRole.Highlight, QColor("#252338"))
        self.explorador.setPalette(paleta)
        self.explorador.itemClicked.connect(self._al_seleccionar_archivo)
        layout_exp.addWidget(self.explorador)
        return self.panel_explorador

    def _crear_panel_editor(self):
        panel = QWidget()
        layout = QVBoxLayout(panel)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)

        barra_tab = QFrame()
        barra_tab.setObjectName("barraTabEditor")
        barra_tab.setFixedHeight(40)
        layout_tab = QHBoxLayout(barra_tab)
        layout_tab.setContentsMargins(8, 0, 12, 0)
        layout_tab.setSpacing(4)

        # Pestañas de archivos abiertos (se pueden arrastrar para reordenarlas)
        self.barra_pestanas = QTabBar()
        self.barra_pestanas.setObjectName("pestanasEditor")
        self.barra_pestanas.setExpanding(False)
        self.barra_pestanas.setMovable(True)
        self.barra_pestanas.setDrawBase(False)
        self.barra_pestanas.setUsesScrollButtons(True)
        self.barra_pestanas.setElideMode(Qt.TextElideMode.ElideNone)
        self.barra_pestanas.setIconSize(QSize(15, 15))
        self.barra_pestanas.currentChanged.connect(self._al_cambiar_pestana)
        layout_tab.addWidget(self.barra_pestanas, 0, Qt.AlignmentFlag.AlignVCenter)

        # "+": nueva pestaña en blanco
        boton_nueva = QToolButton()
        boton_nueva.setObjectName("btnNuevaPestana")
        boton_nueva.setText("+")
        boton_nueva.setFixedSize(28, 28)
        boton_nueva.setToolTip("Nueva pestaña (Ctrl+T)")
        boton_nueva.setCursor(Qt.CursorShape.PointingHandCursor)
        boton_nueva.clicked.connect(self.nuevo_documento)
        layout_tab.addWidget(boton_nueva)
        layout_tab.addStretch()

        layout.addWidget(barra_tab)
        self.pila_editores = QStackedWidget()   # un editor por pestaña
        layout.addWidget(self.pila_editores)
        self._crear_documento()                 # primera pestaña, en blanco
        return panel

    # ---------------------------- Pestañas -----------------------------------
    def _nombre_libre(self, excepto=None):
        """Primer nombre 'Sin título', 'Sin título 2'... que no este en uso."""
        usados = {d.nombre_nuevo for d in self._documentos if d.archivo is None and d is not excepto}
        n = 1
        while True:
            nombre = "Sin título.txt" if n == 1 else f"Sin título {n}.txt"
            if nombre not in usados:
                return nombre
            n += 1

    def _crear_documento(self, sin_titulo=True):
        """Crea una pestaña nueva con su propio editor y la deja activa."""
        doc = _Documento(self._nombre_libre() if sin_titulo else "")
        doc.editor.aplicar_tamano(self._tamano_editor)
        doc.editor.document().modificationChanged.connect(self._actualizar_titulo)
        doc.editor.cursorPositionChanged.connect(self._actualizar_posicion_cursor)
        self._documentos.append(doc)
        self.pila_editores.addWidget(doc.editor)

        # Lado derecho de la pestaña: punto de cambios + boton cerrar
        lado = QWidget()
        lado.setObjectName("ladoPestana")
        layout_lado = QHBoxLayout(lado)
        layout_lado.setContentsMargins(4, 0, 2, 0)
        layout_lado.setSpacing(2)
        layout_lado.addWidget(doc.punto)
        doc.punto.setVisible(False)
        boton_cerrar = QToolButton()
        boton_cerrar.setObjectName("btnCerrarTab")
        boton_cerrar.setText("×")
        boton_cerrar.setFixedSize(20, 20)
        boton_cerrar.setCursor(Qt.CursorShape.PointingHandCursor)
        boton_cerrar.setToolTip("Cerrar pestaña (Ctrl+W)")
        boton_cerrar.clicked.connect(lambda: self.cerrar_pestana(doc))
        layout_lado.addWidget(boton_cerrar)

        self.barra_pestanas.blockSignals(True)
        indice = self.barra_pestanas.addTab(_icono_barra("archivo", TEXTO_GRIS), doc.nombre)
        self.barra_pestanas.setTabData(indice, doc)
        self.barra_pestanas.setTabButton(indice, QTabBar.ButtonPosition.RightSide, lado)
        self.barra_pestanas.blockSignals(False)
        self.barra_pestanas.setCurrentIndex(indice)
        self._al_cambiar_pestana(indice)
        return doc

    def _indice_de(self, doc):
        for i in range(self.barra_pestanas.count()):
            if self.barra_pestanas.tabData(i) is doc:
                return i
        return -1

    def _al_cambiar_pestana(self, indice):
        doc = self.barra_pestanas.tabData(indice) if indice >= 0 else None
        if doc is None:
            return
        self.pila_editores.setCurrentWidget(doc.editor)
        self._actualizar_titulo()
        self._actualizar_posicion_cursor()
        if hasattr(self, "explorador"):
            if doc.archivo:
                self._seleccionar_en_explorador(doc.archivo)
            else:
                self.explorador.clearSelection()
        doc.editor.setFocus()

    def _cambiar_pestana(self, paso):
        total = self.barra_pestanas.count()
        if total > 1:
            self.barra_pestanas.setCurrentIndex((self.barra_pestanas.currentIndex() + paso) % total)

    def cerrar_pestana(self, doc=None):
        """Cierra una pestaña (pregunta si tiene cambios). Siempre queda al menos una."""
        doc = doc or self.documento
        indice = self._indice_de(doc)
        if indice < 0:
            return False
        if doc.modificado:
            self.barra_pestanas.setCurrentIndex(indice)
            if not self._confirmar_descartar(doc):
                return False
            indice = self._indice_de(doc)
        if self._documento_ejecutado is doc:
            self._documento_ejecutado = None
            self._enlaces_consola = {}
        self.barra_pestanas.removeTab(indice)
        self.pila_editores.removeWidget(doc.editor)
        doc.editor.deleteLater()
        self._documentos.remove(doc)
        if self.barra_pestanas.count() == 0:
            self._crear_documento()
        else:
            self._al_cambiar_pestana(self.barra_pestanas.currentIndex())
        return True

    def _zoom(self, paso):
        """Zoom igual para todas las pestañas."""
        tamano = EditorCodigo.TAMANO_BASE if paso == 0 else self._tamano_editor + paso
        self._tamano_editor = max(7, min(32, tamano))
        for doc in self._documentos:
            doc.editor.aplicar_tamano(self._tamano_editor)

    def _crear_panel_inferior(self):
        self.pestanas = QTabWidget()
        self.pestanas.setObjectName("panelInferior")
        self.pestanas.setDocumentMode(True)

        self.pestanas.addTab(self._crear_terminal(), ">_ Terminal")

        self.tabla_tokens = crear_tabla_tokens()
        self.pestanas.addTab(self.tabla_tokens, "Tokens")

        self.tabla_simbolos = crear_tabla_simbolos()
        self.pestanas.addTab(self.tabla_simbolos, "Tabla de Símbolos")

        self.codigo_intermedio = EditorCodigo(solo_lectura=True, tamano=10)
        self.codigo_intermedio.setObjectName("codigoIntermedio")
        self.resaltador_intermedio = ResaltadorIntermedio(self.codigo_intermedio.document())
        self.pestanas.addTab(self.codigo_intermedio, "Código Intermedio")

        self.arbol_sintactico = QTreeWidget()
        self.arbol_sintactico.setObjectName("arbolSintactico")
        self.arbol_sintactico.setColumnCount(2)
        self.arbol_sintactico.setHeaderLabels(["Nodo", "Valor"])
        self.arbol_sintactico.header().resizeSection(0, 320)
        self.pestanas.addTab(self.arbol_sintactico, "Árbol Sintáctico")

        return self.pestanas

    def _crear_terminal(self):
        """Una sola consola con la salida y sus apartados."""
        self.salida = QPlainTextEdit()
        self.salida.setObjectName("salidaTerminal")
        self.salida.setReadOnly(True)
        self.salida.setLineWrapMode(QPlainTextEdit.LineWrapMode.NoWrap)
        self.salida.viewport().setMouseTracking(True)
        self.salida.viewport().installEventFilter(self)
        return self.salida

    def _crear_barra_estado(self):
        """Barra de estado inferior: estado de validez a la izquierda,
        posicion del cursor y lenguaje a la derecha."""
        barra = self.statusBar()

        self.etiqueta_estado = QLabel()
        barra.addWidget(self.etiqueta_estado)
        self._poner_estado("Estado: Listo para analizar.")

        self.etiqueta_cursor = QLabel("Ln 1, Col 1")
        etiqueta_lenguaje = QLabel("UTF-8   EYKOL")
        etiqueta_lenguaje.setToolTip("Lenguaje del archivo")
        for etiqueta in (self.etiqueta_cursor, etiqueta_lenguaje):
            etiqueta.setStyleSheet("padding: 0px 10px;")
            barra.addPermanentWidget(etiqueta)
        self._actualizar_posicion_cursor()

    def _actualizar_posicion_cursor(self):
        if not hasattr(self, "etiqueta_cursor") or self.documento is None:
            return
        cursor = self.editor.textCursor()
        linea = cursor.blockNumber() + 1
        columna = cursor.positionInBlock() + 1
        seleccion = len(cursor.selectedText())
        extra = f"  ({seleccion} selecc.)" if seleccion else ""
        self.etiqueta_cursor.setText(f"Ln {linea}, Col {columna}{extra}")

    def _poner_estado(self, texto, color=TEXTO_GRIS, negrita=False):
        peso = "bold" if negrita else "normal"
        self.etiqueta_estado.setStyleSheet(f"padding-left: 8px; color: {color}; font-weight: {peso};")
        self.etiqueta_estado.setText(texto)

    # ---------------------------- Explorador y archivos ----------------------
    def _cargar_explorador(self):
        self.explorador.clear()
        raiz = QTreeWidgetItem(self.explorador, ["ejemplos"])
        raiz.setIcon(0, _crear_icono("folder"))

        if RUTA_EJEMPLOS.exists():
            for archivo in sorted(RUTA_EJEMPLOS.glob("*.txt")):
                item = QTreeWidgetItem(raiz, [archivo.name])
                item.setIcon(0, _crear_icono("file"))
                item.setData(0, Qt.ItemDataRole.UserRole, str(archivo))

        raiz.setExpanded(True)
        if self.archivo_actual:
            self._seleccionar_en_explorador(self.archivo_actual)

    def _seleccionar_en_explorador(self, archivo):
        raiz = self.explorador.topLevelItem(0)
        if not raiz:
            return
        for i in range(raiz.childCount()):
            item = raiz.child(i)
            if item.data(0, Qt.ItemDataRole.UserRole) == str(archivo):
                self.explorador.setCurrentItem(item)
                return

    def alternar_explorador(self):
        visible = self.isla_explorador.isHidden()
        self.isla_explorador.setVisible(visible)
        self.accion_explorador.setChecked(visible)

    def alternar_panel(self):
        self.isla_consola.setVisible(self.isla_consola.isHidden())

    def _al_seleccionar_archivo(self, item, _columna):
        ruta = item.data(0, Qt.ItemDataRole.UserRole)
        if ruta:
            self._cargar_archivo(Path(ruta))     # se abre en su propia pestaña

    def _abrir_archivo_inicial(self):
        inicial = RUTA_EJEMPLOS / "ciclo_durante.txt"
        if inicial.exists():
            self._cargar_archivo(inicial)
            self.ejecutar_codigo()

    def _cargar_archivo(self, archivo):
        """Abre el archivo en una pestaña. Si ya estaba abierto, solo cambia a ella;
        si la pestaña actual esta en blanco y sin tocar, la reutiliza."""
        archivo = Path(archivo)
        for doc in self._documentos:
            if doc.archivo and doc.archivo.resolve() == archivo.resolve():
                self.barra_pestanas.setCurrentIndex(self._indice_de(doc))
                return
        try:
            datos = archivo.read_bytes()
            contenido = datos.decode("utf-8-sig").replace("\r\n", "\n").replace("\r", "\n")
        except (OSError, UnicodeDecodeError) as error:
            QMessageBox.warning(self, "Error", f"No se pudo abrir el archivo:\n{error}")
            return

        if not self.documento.esta_vacio():
            self._crear_documento(sin_titulo=False)
        self.documento.nombre_nuevo = ""
        self.editor.setPlainText(contenido)
        self.editor.document().setModified(False)
        self.archivo_actual = archivo
        self._seleccionar_en_explorador(archivo)
        self._actualizar_titulo()
        self._poner_estado(f"Archivo abierto: {archivo.name}")

    def _confirmar_descartar(self, doc=None):
        """Si la pestaña tiene cambios sin guardar pregunta que hacer.
        Devuelve True si se puede continuar."""
        doc = doc or self.documento
        if not doc.modificado:
            return True
        caja = QMessageBox(self)
        caja.setIcon(QMessageBox.Icon.Question)
        caja.setWindowTitle("Cambios sin guardar")
        caja.setText(f"¿Deseas guardar los cambios de «{doc.nombre}»?")
        boton_guardar = caja.addButton("Guardar", QMessageBox.ButtonRole.AcceptRole)
        boton_descartar = caja.addButton("Descartar", QMessageBox.ButtonRole.DestructiveRole)
        boton_cancelar = caja.addButton("Cancelar", QMessageBox.ButtonRole.RejectRole)
        caja.setDefaultButton(boton_guardar)
        caja.setEscapeButton(boton_cancelar)
        caja.exec()

        elegido = caja.clickedButton()
        if elegido is boton_guardar:
            self.barra_pestanas.setCurrentIndex(self._indice_de(doc))
            return self.guardar_archivo()
        return elegido is boton_descartar

    def _actualizar_titulo(self, *_):
        if self.documento is None:
            return
        # Texto, tooltip y punto de cambios de cada pestaña
        for i in range(self.barra_pestanas.count()):
            doc = self.barra_pestanas.tabData(i)
            if doc is None:
                continue
            self.barra_pestanas.setTabText(i, doc.nombre)
            self.barra_pestanas.setTabToolTip(i, str(doc.archivo) if doc.archivo else doc.nombre)
            # Como en PyCharm: el punto solo aparece si hay cambios sin guardar
            doc.punto.setVisible(doc.modificado)

        nombre = self.documento.nombre
        modificado = self.documento.modificado
        self.setWindowTitle(f"{'● ' if modificado else ''}{nombre} — EYKOL IDE")

    def nuevo_documento(self):
        """Nueva pestaña en blanco (boton "+", Ctrl+N o Ctrl+T)."""
        self._crear_documento()
        self._poner_estado("Estado: Listo para analizar.")
        self.editor.setFocus()

    def abrir_archivo(self):
        ruta, _ = QFileDialog.getOpenFileName(
            self, "Abrir archivo", str(RUTA_EJEMPLOS),
            "Archivos de texto (*.txt);;Todos los archivos (*)",
        )
        if ruta:
            self._cargar_archivo(Path(ruta))

    def guardar_archivo(self):
        if self.archivo_actual is None:
            return self.guardar_como()
        return self._escribir_archivo(self.archivo_actual)

    def guardar_como(self):
        sugerido = self.archivo_actual or (RUTA_EJEMPLOS / "nuevo_programa.txt")
        ruta, _ = QFileDialog.getSaveFileName(
            self, "Guardar archivo", str(sugerido),
            "Archivos de texto (*.txt);;Todos los archivos (*)",
        )
        if not ruta:
            return False
        return self._escribir_archivo(Path(ruta))

    def _escribir_archivo(self, ruta):
        try:
            ruta.write_text(self.editor.toPlainText(), encoding="utf-8")
        except OSError as error:
            QMessageBox.warning(self, "Error", f"No se pudo guardar el archivo:\n{error}")
            return False
        self.archivo_actual = ruta
        self.editor.document().setModified(False)
        self._cargar_explorador()
        self._actualizar_titulo()
        self._poner_estado(f"Guardado: {ruta.name}", VERDE_SUAVE)
        return True

    def closeEvent(self, event):
        # Pregunta por cada pestaña que tenga cambios sin guardar
        for doc in list(self._documentos):
            if doc.modificado:
                self.barra_pestanas.setCurrentIndex(self._indice_de(doc))
                if not self._confirmar_descartar(doc):
                    event.ignore()
                    return
        event.accept()

    # ---------------------------- Edicion y busqueda -------------------------
    def editor_copiar(self):
        self.editor.copy()

    def editor_cortar(self):
        self.editor.cut()

    def editor_pegar(self):
        self.editor.paste()

    def _enfocar_buscador(self):
        cursor = self.editor.textCursor()
        if cursor.hasSelection() and " " not in cursor.selectedText():
            self.campo_buscar.setText(cursor.selectedText())
        self.campo_buscar.setFocus()
        self.campo_buscar.selectAll()

    def _contar_coincidencias(self, texto):
        if not texto:
            self._poner_estado("Estado: Listo para analizar.")
            return
        total = self.editor.toPlainText().lower().count(texto.lower())
        if total:
            self._poner_estado(f"{total} coincidencia(s) de '{texto}'", TEXTO)
        else:
            self._poner_estado(f"Texto no encontrado: '{texto}'", ROJO)

    def buscar_texto(self, atras=False):
        texto = self.campo_buscar.text()
        if not texto:
            self._enfocar_buscador()
            return

        banderas = QTextDocument.FindFlag.FindBackward if atras else QTextDocument.FindFlag(0)

        encontrado = self.editor.find(texto, banderas)
        if not encontrado:
            # Vuelve a empezar desde el otro extremo del documento
            cursor_actual = self.editor.textCursor()
            self.editor.moveCursor(
                QTextCursor.MoveOperation.End if atras else QTextCursor.MoveOperation.Start
            )
            encontrado = self.editor.find(texto, banderas)
            if not encontrado:
                self.editor.setTextCursor(cursor_actual)
                self._poner_estado(f"Texto no encontrado: '{texto}'", ROJO)
                return

        self.editor.centerCursor()
        self._contar_coincidencias(texto)

    def limpiar_editor(self):
        if not self._confirmar_descartar():
            return
        self.editor.clear()
        self.editor.document().setModified(False)
        self.campo_buscar.clear()
        self._limpiar_salida()
        self._mensaje_inicial_consola()
        self.codigo_intermedio.clear()
        self.arbol_sintactico.clear()
        self.archivo_actual = None
        self.explorador.clearSelection()
        self._actualizar_titulo()
        self._actualizar_posicion_cursor()
        self._poner_estado("Estado: Listo para analizar.")

        llenar_tabla_tokens(self.tabla_tokens, [])
        llenar_tabla_simbolos(self.tabla_simbolos, {})
        self._actualizar_titulos_pestanas(0, 0)

    # ---------------------------- Consola: salida ----------------------------
    def _escribir_linea(self, *segmentos):
        """Agrega una linea a la consola y regresa su numero de bloque.
        Cada segmento es (texto, color[, negrita[, subrayado]])."""
        cursor = self.salida.textCursor()
        cursor.movePosition(QTextCursor.MoveOperation.End)
        if not self.salida.document().isEmpty():
            cursor.insertBlock()
        for segmento in segmentos:
            texto, color = segmento[0], segmento[1]
            negrita = len(segmento) > 2 and segmento[2]
            subrayado = len(segmento) > 3 and segmento[3]
            formato = QTextCharFormat()
            formato.setForeground(QColor(color))
            formato.setFontWeight(QFont.Weight.Bold if negrita else QFont.Weight.Normal)
            formato.setFontUnderline(bool(subrayado))
            cursor.insertText(texto, formato)
        self.salida.setTextCursor(cursor)
        self.salida.ensureCursorVisible()
        return cursor.blockNumber()

    def _limpiar_salida(self):
        self.salida.clear()
        self._enlaces_consola = {}

    def _mensaje_inicial_consola(self):
        self._limpiar_salida()
        self._escribir_linea(("$ ", MORADO, True),
                             ("Ejecuta el código (F5) para ver aquí la salida y los errores", TEXTO_APAGADO))

    def _comando_terminal(self):
        if self.archivo_actual is not None:
            try:
                ruta_rel = self.archivo_actual.relative_to(RUTA_PROYECTO).as_posix()
            except ValueError:
                ruta_rel = self.archivo_actual.name
            return f"python main.py {ruta_rel}"
        return "python main.py <editor>"

    # ---------------------------- Consola: errores ---------------------------
    def _nombre_archivo(self):
        return self.documento.nombre

    @staticmethod
    def _texto_error(error):
        fase = getattr(error, "fase", None)
        mensaje = getattr(error, "mensaje", None)
        if fase and mensaje:
            return f"Error {fase.lower()}: {mensaje}"
        return str(error)

    def _escribir_errores(self, errores, separar=False):
        """Apartado ERRORES dentro de la misma consola. Cada ubicacion es un
        enlace: al hacer clic lleva a esa linea del editor."""
        if not errores:
            return
        if separar:
            self._escribir_linea(("", TEXTO))
        self._escribir_linea(("========== ERRORES ==========", ROJO, True))
        nombre = self._nombre_archivo()
        for numero, error in enumerate(errores):
            if numero:
                self._escribir_linea(("", TEXTO))
            linea = getattr(error, "linea", None)
            columna = getattr(error, "columna", None)
            self._escribir_linea(("✗ ", ROJO, True), (self._texto_error(error), ROJO))
            if linea:
                posicion = f"Ln {linea}, Col {columna}" if columna else f"Ln {linea}"
                bloque = self._escribir_linea(("  ", TEXTO), (f"{nombre} [{posicion}]", AZUL, False, True))
                self._enlaces_consola[bloque] = (linea, columna)
            else:
                self._escribir_linea((f"  {nombre} [fase: {getattr(error, 'fase', '—')}]", TEXTO_APAGADO))
            if getattr(error, "sugerencia", None):
                self._escribir_linea(("  → ", TEXTO_APAGADO), (error.sugerencia, TEXTO_GRIS))

    # ---------------------------- Paneles de analisis ------------------------
    def _llenar_arbol(self, arbol):
        self.arbol_sintactico.clear()

        def color_valor(valor):
            if isinstance(valor, bool):
                return CODIGO_PALABRA
            if isinstance(valor, (int, float)):
                return CODIGO_NUMERO
            if isinstance(valor, str):
                return CODIGO_CADENA
            return TEXTO

        def texto_valor(valor):
            if isinstance(valor, bool):
                return "vrd" if valor else "fals"
            if isinstance(valor, str):
                return f'"{valor}"' if " " in valor or not valor else valor
            return str(valor)

        def agregar(padre, valor, etiqueta=None):
            if isinstance(valor, list):
                item = QTreeWidgetItem(padre, [etiqueta or "bloque", f"{len(valor)} instrucción(es)"])
                item.setForeground(0, QColor(TEXTO_GRIS))
                item.setForeground(1, QColor(TEXTO_APAGADO))
                for hijo in valor:
                    agregar(item, hijo)
                return item

            if isinstance(valor, tuple) and valor and isinstance(valor[0], str):
                tipo, resto = valor[0], valor[1:]
                item = QTreeWidgetItem(padre, [tipo, ""])
                item.setForeground(0, QColor(MORADO))
                fuente = item.font(0)
                fuente.setBold(True)
                item.setFont(0, fuente)
                simples = [v for v in resto if not isinstance(v, (list, tuple))]
                if len(simples) == len(resto):
                    item.setText(1, "  ".join(texto_valor(v) for v in resto))
                    if len(resto) == 1:
                        item.setForeground(1, QColor(color_valor(resto[0])))
                else:
                    if simples:
                        item.setText(1, "  ".join(texto_valor(v) for v in simples))
                    for hijo in resto:
                        if isinstance(hijo, (list, tuple)):
                            agregar(item, hijo)
                return item

            item = QTreeWidgetItem(padre, ["", texto_valor(valor)])
            item.setForeground(1, QColor(color_valor(valor)))
            return item

        if isinstance(arbol, list):
            for instruccion in arbol:
                agregar(self.arbol_sintactico, instruccion)
        elif arbol:
            agregar(self.arbol_sintactico, arbol)
        self.arbol_sintactico.expandAll()

    def _actualizar_titulos_pestanas(self, tokens, simbolos):
        self.pestanas.setTabText(1, f"Tokens ({tokens})" if tokens else "Tokens")
        self.pestanas.setTabText(2, f"Tabla de Símbolos ({simbolos})" if simbolos else "Tabla de Símbolos")

    # ---------------------------- Compilacion --------------------------------
    def ejecutar_codigo(self):
        self._procesar_codigo(ejecutar=True)

    def analizar_codigo(self):
        """Revisa léxico, sintaxis y semántica y genera el código intermedio,
        pero sin ejecutar el programa (en lugar del "Depurar" de PyCharm)."""
        self._procesar_codigo(ejecutar=False)

    def _procesar_codigo(self, ejecutar):
        codigo = self.editor.toPlainText()
        if not codigo.strip():
            self._poner_estado("No hay código para ejecutar.", AMARILLO)
            return

        comando = self._comando_terminal() if ejecutar else f"analizar {self._comando_terminal()[len('python main.py '):]}"
        try:
            resultado = compilar(codigo, ejecutar=ejecutar)
        except Exception as error:  # fallo interno: se muestra en lugar de cerrar el IDE
            self._limpiar_salida()
            self._escribir_linea(("$ ", MORADO, True), (comando, TEXTO_SUAVE))
            self._escribir_linea((f"✗ Error interno del compilador: {error}", ROJO, True))
            self._poner_estado("Error interno del compilador", ROJO, True)
            return

        errores = list(resultado.errores)

        # ----- Consola: comando, salida, errores y prompt final -----
        self._limpiar_salida()
        self._documento_ejecutado = self.documento
        self._escribir_linea(("$ ", MORADO, True), (comando, TEXTO_SUAVE))
        if not ejecutar:
            self._escribir_linea(("(solo análisis: el programa no se ejecutó)", TEXTO_APAGADO))
        for linea in resultado.salida:
            self._escribir_linea((str(linea), TEXTO))
        if ejecutar and not resultado.salida and not errores:
            self._escribir_linea(("(el programa no mostró nada)", TEXTO_APAGADO))

        self._escribir_errores(errores, separar=bool(resultado.salida or not ejecutar))
        self._escribir_linea(("$ ", MORADO, True), ("█", MORADO))

        self.editor.marcar_errores(
            [(getattr(e, "linea", None), getattr(e, "columna", None)) for e in errores]
        )

        # ----- Paneles de analisis -----
        self.codigo_intermedio.setPlainText("\n".join(str(l) for l in resultado.codigo_intermedio))
        self._llenar_arbol(resultado.arbol)
        llenar_tabla_tokens(self.tabla_tokens, resultado.tokens)
        llenar_tabla_simbolos(self.tabla_simbolos, resultado.tabla_simbolos)
        self._actualizar_titulos_pestanas(len(resultado.tokens or []), len(resultado.tabla_simbolos or {}))

        # ----- Barra de estado -----
        if errores:
            self._poner_estado(f"Estado: Código inválido ({len(errores)} error(es) detectado(s))", ROJO, True)
            if self.isla_consola.isHidden():
                self.alternar_panel()
            self.pestanas.setCurrentIndex(0)
        else:
            self._poner_estado("Estado: Código válido (sin errores)", VERDE_SUAVE, True)

    def mostrar_acerca(self):
        QMessageBox.about(
            self,
            "Acerca de EYKOL IDE",
            "<b>EYKOL IDE</b> — Equipo 5<br>"
            "Editor, analizador con PLY y entorno en PyQt6.<br><br>"
            "<b>Atajos útiles</b><br>"
            "F5 / Ctrl+Enter: ejecutar<br>"
            "Ctrl+S / Ctrl+Shift+S: guardar / guardar como<br>"
            "Ctrl+F, F3, Shift+F3: buscar<br>"
            "Ctrl+/: comentar líneas<br>"
            "Tab / Shift+Tab: sangría<br>"
            "Ctrl + rueda, Ctrl +/-/0: zoom<br>"
            "Ctrl+B: explorador · Ctrl+J: consola",
        )


if __name__ == "__main__":
    app = QApplication(sys.argv)
    ventana = VentanaIDE()
    ventana.show()
    sys.exit(app.exec())
