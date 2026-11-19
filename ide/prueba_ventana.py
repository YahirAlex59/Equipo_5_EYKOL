import sys
import time
from pathlib import Path

from PyQt6.QtCore import QPoint, QPointF, QRect, QRectF, QRegularExpression, QSize, Qt
from PyQt6.QtGui import (
    QAction,
    QBrush,
    QColor,
    QFont,
    QIcon,
    QKeySequence,
    QLinearGradient,
    QPainter,
    QPainterPath,
    QPen,
    QPixmap,
    QPolygon,
    QSyntaxHighlighter,
    QTextCharFormat,
    QTextCursor,
    QTextDocument,
    QTextFormat,
)
from PyQt6.QtWidgets import (
    QApplication,
    QFileDialog,
    QFrame,
    QHBoxLayout,
    QLabel,
    QLineEdit,
    QMainWindow,
    QMessageBox,
    QPlainTextEdit,
    QSizePolicy,
    QSplitter,
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
CODIGO_CADENA = "#FFB08A"

COLOR_ICONO_CLARO = QColor(TEXTO)
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
    border: 1px solid {BORDE};
}}
QMenu::item:selected {{
    background-color: #252338;
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

/* ---------- Franja lateral y explorador (igual que antes) ---------- */
QFrame#railLateral {{
    background-color: {FONDO_LATERAL};
    border-right: 1px solid {BORDE};
}}
QFrame#panelExplorador {{
    background-color: {FONDO_EXPLORADOR};
    border-right: 1px solid {BORDE};
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
    background-color: {FONDO_BARRA};
    border-bottom: 1px solid {BORDE};
}}
QFrame#tabArchivoActivo {{
    background-color: {FONDO};
    border-right: 1px solid {BORDE};
    border-top: 2px solid {MORADO};
}}
QFrame#tabArchivoActivo QLabel {{
    background: transparent;
}}
QToolButton#btnCerrarTab {{
    color: {TEXTO_GRIS};
    font-size: 14px;
    padding: 0px 4px;
}}
QLabel#rutaArchivo {{
    color: {TEXTO_APAGADO};
    background: transparent;
    font-size: 12px;
}}

/* ---------- Editores de texto ---------- */
QPlainTextEdit {{
    background-color: {FONDO};
    color: {TEXTO};
    border: none;
    selection-background-color: #3730A3;
}}
QPlainTextEdit#salidaTerminal, QPlainTextEdit#codigoIntermedio {{
    font-family: {FUENTE_MONO};
    font-size: 10pt;
    padding: 6px 4px;
}}

/* ---------- Panel inferior ---------- */
QTabWidget::pane {{
    border: none;
    border-top: 1px solid {BORDE};
    background-color: {FONDO};
}}
QTabBar {{
    background-color: {FONDO_BARRA};
}}
QTabBar::tab {{
    background-color: {FONDO_BARRA};
    color: {TEXTO_GRIS};
    font-size: 11px;
    font-weight: 600;
    padding: 9px 16px 7px 16px;
    border: none;
    border-bottom: 2px solid transparent;
}}
QTabBar::tab:selected {{
    color: {TEXTO};
    border-bottom: 2px solid {MORADO};
}}
QTabBar::tab:hover:!selected {{
    color: #FFFFFF;
}}
/* ---------- Consola (una sola, estilo PyCharm) ---------- */
QFrame#barraConsola {{
    background-color: {FONDO};
    border-right: 1px solid {BORDE};
}}
QFrame#barraConsola QToolButton:checked {{
    background-color: #252338;
}}
QFrame#separadorConsola {{
    background-color: {BORDE};
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
def _crear_icono(tipo, color=None):
    """Dibuja iconos vectoriales con QPainter para no depender de imagenes externas."""
    color_icono = color or COLOR_ICONO_CLARO
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

    elif tipo == "new":
        p.setPen(QPen(color_icono, 2.4, Qt.PenStyle.SolidLine, Qt.PenCapStyle.RoundCap))
        p.drawLine(12, 5, 12, 19)
        p.drawLine(5, 12, 19, 12)

    elif tipo == "open":
        p.setPen(Qt.PenStyle.NoPen)
        p.setBrush(color_icono)
        carpeta = QPolygon([
            QPoint(3, 6), QPoint(10, 6), QPoint(12, 8),
            QPoint(21, 8), QPoint(21, 19), QPoint(3, 19),
        ])
        p.drawPolygon(carpeta)

    elif tipo == "save":
        p.setPen(Qt.PenStyle.NoPen)
        p.setBrush(color_icono)
        cuerpo = QPolygon([
            QPoint(4, 4), QPoint(17, 4), QPoint(20, 7),
            QPoint(20, 20), QPoint(4, 20),
        ])
        p.drawPolygon(cuerpo)
        p.setCompositionMode(QPainter.CompositionMode.CompositionMode_Clear)
        p.drawRect(7, 5, 8, 5)
        p.drawRect(7, 13, 10, 6)
        p.setCompositionMode(QPainter.CompositionMode.CompositionMode_SourceOver)
        p.setBrush(color_icono)
        p.drawRect(12, 6, 2, 3)

    elif tipo == "copy":
        p.setPen(Qt.PenStyle.NoPen)
        p.setBrush(color_icono)
        p.drawRoundedRect(5, 4, 10, 12, 1.5, 1.5)
        p.setCompositionMode(QPainter.CompositionMode.CompositionMode_Clear)
        p.drawRoundedRect(8, 7, 11, 13, 1.5, 1.5)
        p.setCompositionMode(QPainter.CompositionMode.CompositionMode_SourceOver)
        p.setBrush(color_icono)
        p.drawRoundedRect(9, 8, 10, 12, 1.5, 1.5)

    elif tipo == "paste":
        p.setPen(Qt.PenStyle.NoPen)
        p.setBrush(color_icono)
        p.drawRoundedRect(6, 6, 12, 14, 2, 2)
        p.setCompositionMode(QPainter.CompositionMode.CompositionMode_Clear)
        p.drawRoundedRect(8, 3, 8, 5, 1.5, 1.5)
        p.setCompositionMode(QPainter.CompositionMode.CompositionMode_SourceOver)
        p.setBrush(color_icono)
        p.drawRoundedRect(9, 3, 6, 4, 1.5, 1.5)
        p.drawRect(11, 2, 2, 2)

    elif tipo == "cut":
        p.setPen(QPen(color_icono, 2.0, Qt.PenStyle.SolidLine, Qt.PenCapStyle.RoundCap))
        p.setBrush(Qt.BrushStyle.NoBrush)
        p.drawLine(7, 4, 15, 15)
        p.drawLine(17, 4, 9, 15)
        p.drawEllipse(5, 14, 5, 5)
        p.drawEllipse(14, 14, 5, 5)

    elif tipo == "about":
        p.setPen(Qt.PenStyle.NoPen)
        p.setBrush(color_icono)
        p.drawEllipse(4, 4, 16, 16)
        p.setCompositionMode(QPainter.CompositionMode.CompositionMode_Clear)
        p.setFont(QFont("Serif", 12, QFont.Weight.Bold))
        p.setPen(QColor(0, 0, 0))
        p.drawText(pixmap.rect(), Qt.AlignmentFlag.AlignCenter, "i")

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

    elif tipo == "error":
        p.setPen(Qt.PenStyle.NoPen)
        p.setBrush(QColor(ROJO))
        p.drawEllipse(QRectF(2, 2, 20, 20))
        p.setPen(QPen(QColor(FONDO), 2.4, Qt.PenStyle.SolidLine, Qt.PenCapStyle.RoundCap))
        p.drawLine(QPointF(8.5, 8.5), QPointF(15.5, 15.5))
        p.drawLine(QPointF(15.5, 8.5), QPointF(8.5, 15.5))

    elif tipo == "repetir":
        camino = QPainterPath()
        camino.arcMoveTo(QRectF(5, 5, 14, 14), 50)
        camino.arcTo(QRectF(5, 5, 14, 14), 50, 290)
        p.drawPath(camino)
        ruta((16.5, 3), (16.5, 7.5), (12, 7.5))

    elif tipo == "arriba":
        p.drawLine(QPointF(12, 19), QPointF(12, 5))
        ruta((6.5, 10.5), (12, 5), (17.5, 10.5))

    elif tipo == "abajo":
        p.drawLine(QPointF(12, 5), QPointF(12, 19))
        ruta((6.5, 13.5), (12, 19), (17.5, 13.5))

    elif tipo == "ajuste":
        p.drawLine(QPointF(4, 6), QPointF(20, 6))
        camino = QPainterPath(QPointF(4, 12))
        camino.lineTo(QPointF(16, 12))
        camino.cubicTo(QPointF(20.5, 12), QPointF(20.5, 18), QPointF(16, 18))
        camino.lineTo(QPointF(11, 18))
        p.drawPath(camino)
        ruta((13.5, 15.5), (11, 18), (13.5, 20.5))
        p.drawLine(QPointF(4, 18), QPointF(7, 18))

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


class _LogoEYKOL(QWidget):
    """Texto EYKOL con degradado morado -> azul."""

    def __init__(self):
        super().__init__()
        self.fuente = QFont("Segoe UI", 12, QFont.Weight.Bold)
        self.fuente.setLetterSpacing(QFont.SpacingType.AbsoluteSpacing, 4)
        self.setFixedSize(96, 30)
        self.setToolTip("EYKOL IDE")

    def paintEvent(self, _event):
        p = QPainter(self)
        p.setRenderHint(QPainter.RenderHint.Antialiasing)
        camino = QPainterPath()
        camino.addText(QPointF(4, 21), self.fuente, "EYKOL")
        caja = camino.boundingRect()
        degradado = QLinearGradient(caja.topLeft(), caja.topRight())
        degradado.setColorAt(0, QColor(MORADO))
        degradado.setColorAt(1, QColor(AZUL))
        p.fillPath(camino, QBrush(degradado))
        p.end()


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

    def restablecer_zoom(self):
        self.aplicar_tamano(self.TAMANO_BASE)

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
class VentanaIDE(QMainWindow):

    def __init__(self):
        super().__init__()

        self.resize(1240, 800)
        self.setMinimumSize(900, 560)
        self.setStyleSheet(ESTILO_OSCURO)
        self.setWindowIcon(_crear_icono("logo"))

        self.archivo_actual = None
        self._errores_actuales = []
        self._enlaces_consola = {}    # bloque de la consola -> (linea, columna) del error

        self.editor = EditorCodigo()
        self.resaltador = ResaltadorEYKOL(self.editor.document())
        self.editor.cursorPositionChanged.connect(self._actualizar_posicion_cursor)
        self.editor.document().modificationChanged.connect(self._actualizar_titulo)

        self._crear_acciones()
        self._crear_barra_superior()
        self._construir_interfaz()
        self._crear_barra_estado()

        self._cargar_explorador()
        self._mensaje_inicial_consola()
        self._actualizar_titulo()
        self._abrir_archivo_inicial()

    # ---------------------------- Acciones -----------------------------------
    def _accion(self, icono, texto, atajo, funcion, en_ventana=True):
        """Crea una accion con icono, tooltip (con su atajo) y conexion."""
        accion = QAction(icono or QIcon(), texto, self)
        if atajo:
            secuencia = QKeySequence(atajo)
            texto_atajo = secuencia.toString(QKeySequence.SequenceFormat.NativeText)
            accion.setToolTip(f"{texto} ({texto_atajo})")
            if en_ventana:
                accion.setShortcut(secuencia)
                self.addAction(accion)
        else:
            accion.setToolTip(texto)
        accion.triggered.connect(funcion)
        return accion

    def _crear_acciones(self):
        e = self.editor

        # --- Franja lateral (iconos de siempre) ---
        self.accion_nuevo = self._accion(_crear_icono("new"), "Nuevo documento", "Ctrl+N", self.nuevo_documento)
        self.accion_explorador = self._accion(_crear_icono("open"), "Mostrar / ocultar explorador", "Ctrl+B",
                                              self.alternar_explorador)
        self.accion_guardar = self._accion(_crear_icono("save"), "Guardar archivo", "Ctrl+S", self.guardar_archivo)
        # Copiar / pegar / cortar usan el teclado propio del editor (asi tambien
        # funcionan dentro del buscador); el boton solo actua sobre el editor.
        self.accion_copiar = self._accion(_crear_icono("copy"), "Copiar texto seleccionado", "Ctrl+C",
                                          self.editor_copiar, en_ventana=False)
        self.accion_pegar = self._accion(_crear_icono("paste"), "Pegar texto", "Ctrl+V",
                                         self.editor_pegar, en_ventana=False)
        self.accion_cortar = self._accion(_crear_icono("cut"), "Cortar texto seleccionado", "Ctrl+X",
                                          self.editor_cortar, en_ventana=False)
        self.accion_acerca = self._accion(_crear_icono("about"), "Acerca de EYKOL IDE", "F1", self.mostrar_acerca)

        # --- Barra superior ---
        self.accion_abrir = self._accion(_icono_barra("abrir"), "Abrir archivo", "Ctrl+O", self.abrir_archivo)
        self.accion_limpiar = self._accion(_icono_barra("limpiar"), "Limpiar editor y resultados", None,
                                           self.limpiar_editor)
        self.accion_ejecutar = self._accion(_icono_barra("ejecutar"), "Ejecutar código", "F5", self.ejecutar_codigo)

        # --- Solo atajos de teclado ---
        self._accion(None, "Guardar como", "Ctrl+Shift+S", self.guardar_como)
        self._accion(None, "Ejecutar código", "Ctrl+Return", self.ejecutar_codigo)
        self._accion(None, "Comentar / descomentar", "Ctrl+/", e.alternar_comentario)
        self._accion(None, "Buscar", "Ctrl+F", self._enfocar_buscador)
        self._accion(None, "Buscar siguiente", "F3", self.buscar_texto)
        self._accion(None, "Buscar anterior", "Shift+F3", lambda: self.buscar_texto(atras=True))
        self._accion(None, "Mostrar / ocultar consola", "Ctrl+J", self.alternar_panel)
        self._accion(None, "Aumentar zoom", "Ctrl++", e.acercar)
        self._accion(None, "Aumentar zoom", "Ctrl+=", e.acercar)
        self._accion(None, "Reducir zoom", "Ctrl+-", e.alejar)
        self._accion(None, "Restablecer zoom", "Ctrl+0", e.restablecer_zoom)
        self._accion(None, "Salir", "Ctrl+Q", self.close)

    # ---------------------------- Barra superior -----------------------------
    def _crear_barra_superior(self):
        barra = QToolBar("Herramientas", self)
        barra.setObjectName("barraSuperior")
        barra.setMovable(False)
        barra.setFloatable(False)
        barra.setIconSize(QSize(18, 18))
        barra.setContextMenuPolicy(Qt.ContextMenuPolicy.PreventContextMenu)
        self.addToolBar(barra)

        barra.addWidget(_LogoEYKOL())
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

        # Botones de icono: abrir, guardar, limpiar | ejecutar
        for accion in (self.accion_abrir, None, self.accion_limpiar):
            boton = QToolButton()
            if accion is None:
                # Guardar: misma funcion que en la franja lateral, icono de contorno
                boton.setIcon(_icono_barra("guardar"))
                boton.setToolTip(self.accion_guardar.toolTip())
                boton.clicked.connect(self.accion_guardar.trigger)
            else:
                boton.setDefaultAction(accion)
            boton.setIconSize(QSize(18, 18))
            boton.setFixedSize(32, 32)
            boton.setCursor(Qt.CursorShape.PointingHandCursor)
            barra.addWidget(boton)

        barra.addWidget(_separador_vertical())

        self.boton_ejecutar = QToolButton()
        self.boton_ejecutar.setObjectName("btnEjecutar")
        self.boton_ejecutar.setDefaultAction(self.accion_ejecutar)
        self.boton_ejecutar.setIconSize(QSize(18, 18))
        self.boton_ejecutar.setFixedSize(34, 32)
        self.boton_ejecutar.setCursor(Qt.CursorShape.PointingHandCursor)
        barra.addWidget(self.boton_ejecutar)

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

        self.divisor_h = QSplitter(Qt.Orientation.Horizontal)
        self.divisor_h.setHandleWidth(1)
        self.divisor_h.addWidget(self._crear_explorador())

        self.divisor_v = QSplitter(Qt.Orientation.Vertical)
        self.divisor_v.setHandleWidth(1)
        self.divisor_v.setChildrenCollapsible(False)
        self.divisor_v.addWidget(self._crear_panel_editor())
        self.divisor_v.addWidget(self._crear_panel_inferior())
        self.divisor_v.setStretchFactor(0, 3)
        self.divisor_v.setStretchFactor(1, 2)
        self.divisor_v.setSizes([450, 300])

        self.divisor_h.addWidget(self.divisor_v)
        self.divisor_h.setStretchFactor(1, 1)
        self.divisor_h.setSizes([235, 965])

        layout_principal.addWidget(self.divisor_h)

    def _crear_rail(self):
        """Franja estrecha izquierda con botones de herramientas (igual que antes)."""
        rail = QFrame()
        rail.setObjectName("railLateral")
        rail.setFixedWidth(44)
        layout_rail = QVBoxLayout(rail)
        layout_rail.setContentsMargins(6, 10, 6, 10)
        layout_rail.setSpacing(6)

        for grupo in (
            (self.accion_nuevo, self.accion_explorador, self.accion_guardar),
            (self.accion_copiar, self.accion_pegar, self.accion_cortar),
            (self.accion_acerca,),
        ):
            if layout_rail.count() > 0:
                separador = QFrame()
                separador.setFixedHeight(1)
                separador.setStyleSheet(f"background-color: {BORDE};")
                layout_rail.addWidget(separador)
            for accion in grupo:
                boton = QToolButton(rail)
                boton.setDefaultAction(accion)
                boton.setFixedSize(32, 32)
                boton.setIconSize(QSize(18, 18))
                layout_rail.addWidget(boton)

        layout_rail.addStretch()
        return rail

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
        barra_tab.setFixedHeight(38)
        layout_tab = QHBoxLayout(barra_tab)
        layout_tab.setContentsMargins(0, 0, 12, 0)
        layout_tab.setSpacing(10)

        tab_activo = QFrame()
        tab_activo.setObjectName("tabArchivoActivo")
        layout_activo = QHBoxLayout(tab_activo)
        layout_activo.setContentsMargins(12, 0, 6, 0)
        layout_activo.setSpacing(8)

        icono = QLabel()
        icono.setPixmap(_dibujar_icono("archivo", TEXTO_GRIS, 15))
        self.etiqueta_archivo = QLabel("Sin título.txt")
        self.etiqueta_archivo.setStyleSheet(f"color: {TEXTO}; font-weight: 500;")
        self.punto_modificado = QLabel("●")
        self.punto_modificado.setToolTip("Guardado")

        boton_cerrar = QToolButton()
        boton_cerrar.setObjectName("btnCerrarTab")
        boton_cerrar.setText("×")
        boton_cerrar.setToolTip("Cerrar (nuevo documento)")
        boton_cerrar.clicked.connect(self.nuevo_documento)

        layout_activo.addWidget(icono)
        layout_activo.addWidget(self.etiqueta_archivo)
        layout_activo.addWidget(self.punto_modificado)
        layout_activo.addWidget(boton_cerrar)

        layout_tab.addWidget(tab_activo)
        self.etiqueta_ruta = QLabel("")
        self.etiqueta_ruta.setObjectName("rutaArchivo")
        layout_tab.addWidget(self.etiqueta_ruta)
        layout_tab.addStretch()

        layout.addWidget(barra_tab)
        layout.addWidget(self.editor)
        return panel

    def _crear_panel_inferior(self):
        self.pestanas = QTabWidget()
        self.pestanas.setDocumentMode(True)
        fuente_tabs = self.pestanas.tabBar().font()
        fuente_tabs.setLetterSpacing(QFont.SpacingType.AbsoluteSpacing, 0.8)
        self.pestanas.tabBar().setFont(fuente_tabs)

        self.pestanas.addTab(self._crear_terminal(), "TERMINAL")

        self.codigo_intermedio = EditorCodigo(solo_lectura=True, tamano=10)
        self.codigo_intermedio.setObjectName("codigoIntermedio")
        self.resaltador_intermedio = ResaltadorIntermedio(self.codigo_intermedio.document())
        self.pestanas.addTab(self.codigo_intermedio, "CÓDIGO INTERMEDIO")

        self.arbol_sintactico = QTreeWidget()
        self.arbol_sintactico.setObjectName("arbolSintactico")
        self.arbol_sintactico.setColumnCount(2)
        self.arbol_sintactico.setHeaderLabels(["Nodo", "Valor"])
        self.arbol_sintactico.header().resizeSection(0, 320)
        self.pestanas.addTab(self.arbol_sintactico, "ÁRBOL SINTÁCTICO")

        self.tabla_tokens = crear_tabla_tokens()
        self.pestanas.addTab(self.tabla_tokens, "TOKENS")

        self.tabla_simbolos = crear_tabla_simbolos()
        self.pestanas.addTab(self.tabla_simbolos, "TABLA DE SÍMBOLOS")
        return self.pestanas

    def _crear_terminal(self):
        """Una sola consola (como el panel Run de PyCharm): barra de iconos a
        la izquierda y la salida con sus apartados."""
        panel = QWidget()
        layout = QVBoxLayout(panel)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)

        # ----- Cuerpo: barra de iconos + consola -----
        cuerpo = QHBoxLayout()
        cuerpo.setContentsMargins(0, 0, 0, 0)
        cuerpo.setSpacing(0)

        barra = QFrame()
        barra.setObjectName("barraConsola")
        barra.setFixedWidth(42)
        layout_barra = QVBoxLayout(barra)
        layout_barra.setContentsMargins(5, 8, 5, 8)
        layout_barra.setSpacing(4)

        self.boton_ajuste = None
        grupos = (
            (("repetir", VERDE, "Ejecutar de nuevo (F5)", self.ejecutar_codigo),),
            (("arriba", TEXTO_GRIS, "Ir al inicio de la consola", self._consola_al_inicio),
             ("abajo", TEXTO_GRIS, "Ir al final de la consola", self._consola_al_final)),
            (("ajuste", TEXTO_GRIS, "Ajustar líneas largas", self._alternar_ajuste_consola),
             ("copiar", TEXTO_GRIS, "Copiar toda la salida", self._copiar_consola)),
            (("limpiar", TEXTO_GRIS, "Limpiar consola", self._limpiar_salida),),
        )
        for indice, grupo in enumerate(grupos):
            if indice:
                separador = QFrame()
                separador.setObjectName("separadorConsola")
                separador.setFixedHeight(1)
                layout_barra.addWidget(separador)
            for tipo, color, tooltip, funcion in grupo:
                boton = QToolButton()
                boton.setIcon(_icono_barra(tipo, color))
                boton.setIconSize(QSize(17, 17))
                boton.setFixedSize(30, 30)
                boton.setToolTip(tooltip)
                boton.setCursor(Qt.CursorShape.PointingHandCursor)
                if tipo == "ajuste":
                    boton.setCheckable(True)
                    boton.toggled.connect(funcion)
                    self.boton_ajuste = boton
                else:
                    boton.clicked.connect(funcion)
                layout_barra.addWidget(boton, 0, Qt.AlignmentFlag.AlignHCenter)
        layout_barra.addStretch()
        cuerpo.addWidget(barra)

        self.salida = QPlainTextEdit()
        self.salida.setObjectName("salidaTerminal")
        self.salida.setReadOnly(True)
        self.salida.setLineWrapMode(QPlainTextEdit.LineWrapMode.NoWrap)
        self.salida.viewport().setMouseTracking(True)
        self.salida.viewport().installEventFilter(self)
        cuerpo.addWidget(self.salida)

        layout.addLayout(cuerpo)
        return panel

    # ---------------------------- Botones de la consola ----------------------
    def _consola_al_inicio(self):
        self.salida.moveCursor(QTextCursor.MoveOperation.Start)
        self.salida.ensureCursorVisible()

    def _consola_al_final(self):
        self.salida.moveCursor(QTextCursor.MoveOperation.End)
        self.salida.ensureCursorVisible()

    def _alternar_ajuste_consola(self, activo):
        modo = QPlainTextEdit.LineWrapMode.WidgetWidth if activo else QPlainTextEdit.LineWrapMode.NoWrap
        self.salida.setLineWrapMode(modo)

    def _copiar_consola(self):
        QApplication.clipboard().setText(self.salida.toPlainText())
        self._poner_estado("Salida de la consola copiada.", TEXTO)

    def _crear_barra_estado(self):
        barra = self.statusBar()
        self.etiqueta_estado = QLabel()
        barra.addWidget(self.etiqueta_estado)
        self._poner_estado("Estado: Listo para analizar.")

        self.etiqueta_errores_estado = QLabel()
        self.etiqueta_tiempo = QLabel("")
        self.etiqueta_cursor = QLabel("Ln 1, Col 1")
        etiqueta_lenguaje = QLabel("UTF-8   EYKOL")
        for etiqueta in (self.etiqueta_errores_estado, self.etiqueta_tiempo, self.etiqueta_cursor, etiqueta_lenguaje):
            etiqueta.setStyleSheet("padding: 0px 10px;")
            barra.addPermanentWidget(etiqueta)

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
        visible = not self.panel_explorador.isVisible()
        self.panel_explorador.setVisible(visible)

    def alternar_panel(self):
        self.pestanas.setVisible(not self.pestanas.isVisible())

    def _al_seleccionar_archivo(self, item, _columna):
        ruta = item.data(0, Qt.ItemDataRole.UserRole)
        if not ruta or (self.archivo_actual and str(self.archivo_actual) == ruta):
            return
        if self._confirmar_descartar():
            self._cargar_archivo(Path(ruta))
        elif self.archivo_actual:
            self._seleccionar_en_explorador(self.archivo_actual)

    def _abrir_archivo_inicial(self):
        inicial = RUTA_EJEMPLOS / "ciclo_durante.txt"
        if inicial.exists():
            self._cargar_archivo(inicial)
            self.ejecutar_codigo()

    def _cargar_archivo(self, archivo):
        try:
            contenido = archivo.read_text(encoding="utf-8-sig")
        except (OSError, UnicodeDecodeError) as error:
            QMessageBox.warning(self, "Error", f"No se pudo abrir el archivo:\n{error}")
            return

        self.editor.setPlainText(contenido)
        self.editor.document().setModified(False)
        self.archivo_actual = archivo
        self._seleccionar_en_explorador(archivo)
        self._actualizar_titulo()
        self._poner_estado(f"Archivo abierto: {archivo.name}")

    def _confirmar_descartar(self):
        """Si hay cambios sin guardar pregunta que hacer. Devuelve True si se puede continuar."""
        if not self.editor.document().isModified():
            return True
        nombre = self.archivo_actual.name if self.archivo_actual else "Sin título.txt"
        respuesta = QMessageBox.question(
            self,
            "Cambios sin guardar",
            f"¿Deseas guardar los cambios de «{nombre}»?",
            QMessageBox.StandardButton.Save
            | QMessageBox.StandardButton.Discard
            | QMessageBox.StandardButton.Cancel,
            QMessageBox.StandardButton.Save,
        )
        if respuesta == QMessageBox.StandardButton.Save:
            return self.guardar_archivo()
        return respuesta == QMessageBox.StandardButton.Discard

    def _actualizar_titulo(self, *_):
        nombre = self.archivo_actual.name if self.archivo_actual else "Sin título.txt"
        modificado = self.editor.document().isModified()
        self.etiqueta_archivo.setText(nombre)
        self.punto_modificado.setStyleSheet(
            f"color: {AMARILLO if modificado else VERDE}; font-size: 11px;"
        )
        self.punto_modificado.setToolTip("Cambios sin guardar" if modificado else "Guardado")
        if self.archivo_actual:
            try:
                ruta = self.archivo_actual.relative_to(RUTA_PROYECTO).parent.as_posix()
            except ValueError:
                ruta = str(self.archivo_actual.parent)
            self.etiqueta_ruta.setText(ruta)
        else:
            self.etiqueta_ruta.setText("")
        self.setWindowTitle(f"{'● ' if modificado else ''}{nombre} — EYKOL IDE")

    def nuevo_documento(self):
        if not self._confirmar_descartar():
            return
        self.editor.clear()
        self.editor.document().setModified(False)
        self.archivo_actual = None
        self.explorador.clearSelection()
        self._actualizar_titulo()
        self._poner_estado("Estado: Listo para analizar.")
        self.editor.setFocus()

    def abrir_archivo(self):
        if not self._confirmar_descartar():
            return
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
        if self._confirmar_descartar():
            event.accept()
        else:
            event.ignore()

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
        self.etiqueta_tiempo.setText("")
        self.etiqueta_errores_estado.setText("")
        self._actualizar_titulo()
        self._poner_estado("Estado: Listo para analizar.")

        llenar_tabla_tokens(self.tabla_tokens, [])
        llenar_tabla_simbolos(self.tabla_simbolos, {})
        self._actualizar_titulos_pestanas(0, 0)

    def _actualizar_posicion_cursor(self):
        cursor = self.editor.textCursor()
        linea = cursor.blockNumber() + 1
        columna = cursor.positionInBlock() + 1
        seleccion = len(cursor.selectedText())
        extra = f"  ({seleccion} selecc.)" if seleccion else ""
        self.etiqueta_cursor.setText(f"Ln {linea}, Col {columna}{extra}")

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
        self._escribir_linea(("> ", MORADO, True),
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
        return self.archivo_actual.name if self.archivo_actual else "Sin título.txt"

    @staticmethod
    def _texto_error(error):
        fase = getattr(error, "fase", None)
        mensaje = getattr(error, "mensaje", None)
        if fase and mensaje:
            return f"Error {fase.lower()}: {mensaje}"
        return str(error)

    def _escribir_errores(self, errores):
        """Apartado ERRORES dentro de la misma consola. Cada ubicacion es un
        enlace: al hacer clic lleva a esa linea del editor."""
        self._errores_actuales = list(errores)
        if not errores:
            return
        self._escribir_linea(("", TEXTO))
        self._escribir_linea((f"──────── ERRORES ({len(errores)}) ────────", ROJO, True))
        nombre = self._nombre_archivo()
        for error in errores:
            linea = getattr(error, "linea", None)
            columna = getattr(error, "columna", None)
            self._escribir_linea(("✗ ", ROJO, True), (self._texto_error(error), ROJO))
            if linea:
                posicion = f"Ln {linea}, Col {columna}" if columna else f"Ln {linea}"
                bloque = self._escribir_linea(("    ", TEXTO), (f"{nombre} [{posicion}]", AZUL, False, True))
                self._enlaces_consola[bloque] = (linea, columna)
            else:
                self._escribir_linea((f"    {nombre} [fase: {getattr(error, 'fase', '—')}]", TEXTO_APAGADO))
            if getattr(error, "sugerencia", None):
                self._escribir_linea((f"    Sugerencia: {error.sugerencia}", TEXTO_GRIS))

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
        self.pestanas.setTabText(3, f"TOKENS ({tokens})" if tokens else "TOKENS")
        self.pestanas.setTabText(4, f"TABLA DE SÍMBOLOS ({simbolos})" if simbolos else "TABLA DE SÍMBOLOS")

    # ---------------------------- Compilacion --------------------------------
    def ejecutar_codigo(self):
        codigo = self.editor.toPlainText()
        if not codigo.strip():
            self._poner_estado("No hay código para ejecutar.", AMARILLO)
            return

        inicio = time.perf_counter()
        try:
            resultado = compilar(codigo)
        except Exception as error:  # fallo interno: se muestra en lugar de cerrar el IDE
            self._limpiar_salida()
            self._escribir_linea(("> ", MORADO, True), (self._comando_terminal(), TEXTO_APAGADO))
            self._escribir_linea((f"✗ Error interno del compilador: {error}", ROJO, True))
            self._poner_estado("Error interno del compilador", ROJO, True)
            return
        milisegundos = (time.perf_counter() - inicio) * 1000

        errores = list(resultado.errores)

        # ----- Consola: comando, salida, errores y estado (todo en una) -----
        self._limpiar_salida()
        self._escribir_linea(("> ", MORADO, True), (self._comando_terminal(), TEXTO_APAGADO))
        for linea in resultado.salida:
            self._escribir_linea((str(linea), TEXTO))
        if not resultado.salida and not errores:
            self._escribir_linea(("(el programa no mostró nada)", TEXTO_APAGADO))

        self._escribir_errores(errores)

        self._escribir_linea(("", TEXTO))
        if errores:
            self._escribir_linea(
                (f"✗ Estado: Código inválido ({len(errores)} error(es) detectado(s))", ROJO, True)
            )
        else:
            self._escribir_linea(("✓ Estado: Código válido (sin errores)", VERDE_SUAVE, True))
        self._escribir_linea(
            (f"Proceso terminado con código de salida {1 if errores else 0} ({milisegundos:.0f} ms)",
             TEXTO_APAGADO)
        )

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
        # El estado (valido / invalido) ya no va aqui: se muestra en el panel ERRORES
        self.etiqueta_tiempo.setText(f"{milisegundos:.0f} ms")
        self._poner_estado("")
        if errores:
            self.etiqueta_errores_estado.setStyleSheet(f"padding: 0px 10px; color: {ROJO};")
            self.etiqueta_errores_estado.setText(f"✗ {len(errores)} error(es)")
            if not self.pestanas.isVisible():
                self.alternar_panel()
            self.pestanas.setCurrentIndex(0)
        else:
            self.etiqueta_errores_estado.setStyleSheet(f"padding: 0px 10px; color: {VERDE_SUAVE};")
            self.etiqueta_errores_estado.setText("✓ 0 errores")

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
