import pprint
import sys
from pathlib import Path

from PyQt6.QtCore import QPoint, QRect, QSize, Qt
from PyQt6.QtGui import (
    QAction,
    QColor,
    QFont,
    QIcon,
    QPainter,
    QPen,
    QPixmap,
    QPolygon,
    QTextCursor,
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
    QMenu,
    QMessageBox,
    QPlainTextEdit,
    QPushButton,
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

COLOR_ICONO_CLARO = QColor("#E5E7EB")

ESTILO_OSCURO = """
QMainWindow, QWidget {
    background-color: #12131A;
    color: #E5E7EB;
    font-family: "Segoe UI", sans-serif;
    font-size: 13px;
}
QMenuBar {
    background-color: #181924;
    color: #D1D5DB;
    border-bottom: 1px solid #262837;
    padding: 2px 6px;
}
QMenuBar::item {
    background: transparent;
    padding: 4px 10px;
    border-radius: 4px;
}
QMenuBar::item:selected {
    background-color: #25273A;
    color: #FFFFFF;
}
QMenu {
    background-color: #181924;
    color: #E5E7EB;
    border: 1px solid #262837;
}
QMenu::item:selected {
    background-color: #252338;
}
QToolBar {
    background-color: #181924;
    border: none;
    border-bottom: 1px solid #262837;
    spacing: 4px;
    padding: 4px 8px;
}
QToolButton {
    background: transparent;
    border: none;
    border-radius: 5px;
    padding: 5px;
}
QToolButton:hover {
    background-color: #25273A;
}
QToolButton::menu-indicator {
    image: none;
}
QLineEdit#campoBuscar {
    background-color: #12131A;
    color: #E5E7EB;
    border: 1px solid #2E3044;
    border-radius: 5px;
    padding: 4px 10px;
    min-width: 210px;
}
QLineEdit#campoBuscar:focus {
    border: 1px solid #8B5CF6;
}
QPushButton#btnBuscar {
    background-color: #25273A;
    color: #E5E7EB;
    border: 1px solid #2E3044;
    border-radius: 5px;
    padding: 4px 12px;
}
QPushButton#btnBuscar:hover {
    background-color: #32354E;
}
QFrame#railLateral {
    background-color: #14151E;
    border-right: 1px solid #262837;
}
QFrame#panelExplorador {
    background-color: #161722;
    border-right: 1px solid #262837;
}
QLabel#tituloExplorador {
    background-color: #161722;
    color: #9CA3AF;
    font-weight: 600;
    font-size: 12px;
    padding: 10px 12px 6px 12px;
}
QTreeWidget {
    background-color: #161722;
    color: #D1D5DB;
    border: none;
    outline: none;
    padding: 2px 6px;
}
QTreeWidget::item {
    padding: 5px 6px;
    border-radius: 5px;
}
QTreeWidget::item:hover {
    background-color: #1F2130;
}
QTreeWidget::item:selected {
    background-color: #252338;
    color: #FFFFFF;
}
QFrame#barraTabEditor {
    background-color: #181924;
    border-bottom: 1px solid #262837;
}
QFrame#tabArchivoActivo {
    background-color: #12131A;
    border-right: 1px solid #262837;
    border-top: 2px solid #8B5CF6;
}
QPushButton#btnCerrarTab {
    background: transparent;
    color: #9CA3AF;
    border: none;
    font-size: 14px;
    padding: 0px 4px;
}
QPushButton#btnCerrarTab:hover {
    color: #FFFFFF;
}
QPushButton#btnEjecutar {
    background-color: transparent;
    border: none;
    border-radius: 5px;
    padding: 4px 8px;
}
QPushButton#btnEjecutar:hover {
    background-color: #232A27;
}
QPushButton#btnLimpiar {
    background-color: transparent;
    color: #9CA3AF;
    border: none;
    border-radius: 5px;
    padding: 4px 8px;
}
QPushButton#btnLimpiar:hover {
    background-color: #25273A;
    color: #E5E7EB;
}
QPlainTextEdit {
    background-color: #12131A;
    color: #E5E7EB;
    border: none;
    selection-background-color: #3730A3;
}
QTabWidget::pane {
    border: none;
    border-top: 1px solid #262837;
    background-color: #12131A;
}
QTabBar {
    background-color: #181924;
}
QTabBar::tab {
    background-color: #181924;
    color: #9CA3AF;
    padding: 7px 14px;
    border-right: 1px solid #262837;
}
QTabBar::tab:selected {
    background-color: #12131A;
    color: #E5E7EB;
    border-top: 2px solid #8B5CF6;
}
QTabBar::tab:hover:!selected {
    color: #FFFFFF;
}
QSplitter::handle {
    background-color: #262837;
}
QStatusBar {
    background-color: #181924;
    color: #9CA3AF;
    border-top: 1px solid #262837;
    font-size: 12px;
}
QStatusBar::item {
    border: none;
}
"""


def _crear_icono(tipo, color=None):
    """Dibuja iconos vectoriales con QPainter para no depender de imagenes externas."""
    color_icono = color or COLOR_ICONO_CLARO
    pixmap = QPixmap(24, 24)
    pixmap.fill(Qt.GlobalColor.transparent)

    p = QPainter(pixmap)
    p.setRenderHint(QPainter.RenderHint.Antialiasing)

    if tipo == "logo":
        p.setPen(Qt.PenStyle.NoPen)
        p.setBrush(QColor("#8B5CF6"))
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
            QPoint(3, 6),
            QPoint(10, 6),
            QPoint(12, 8),
            QPoint(21, 8),
            QPoint(21, 19),
            QPoint(3, 19),
        ])
        p.drawPolygon(carpeta)

    elif tipo == "save":
        p.setPen(Qt.PenStyle.NoPen)
        p.setBrush(color_icono)
        cuerpo = QPolygon([
            QPoint(4, 4),
            QPoint(17, 4),
            QPoint(20, 7),
            QPoint(20, 20),
            QPoint(4, 20),
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

    elif tipo == "play":
        p.setPen(Qt.PenStyle.NoPen)
        p.setBrush(QColor("#22C55E"))
        triangulo = QPolygon([
            QPoint(7, 5),
            QPoint(19, 12),
            QPoint(7, 19),
        ])
        p.drawPolygon(triangulo)

    elif tipo == "folder":
        p.setPen(QPen(QColor("#9CA3AF"), 1.6))
        p.setBrush(Qt.BrushStyle.NoBrush)
        carpeta = QPolygon([
            QPoint(3, 6),
            QPoint(9, 6),
            QPoint(11, 8),
            QPoint(21, 8),
            QPoint(21, 18),
            QPoint(3, 18),
        ])
        p.drawPolygon(carpeta)

    elif tipo == "file":
        p.setPen(QPen(QColor("#9CA3AF"), 1.5))
        p.setBrush(Qt.BrushStyle.NoBrush)
        p.drawRect(6, 4, 12, 16)
        p.drawLine(9, 9, 15, 9)
        p.drawLine(9, 13, 15, 13)

    elif tipo == "menu":
        p.setPen(QPen(color_icono, 2.1, Qt.PenStyle.SolidLine, Qt.PenCapStyle.FlatCap))
        for y in (6, 10, 14, 18):
            p.drawLine(4, y, 20, y)

    p.end()
    return QIcon(pixmap)


class _AreaNumerosLinea(QWidget):
    """Margen izquierdo con el numero de cada linea del editor."""

    def __init__(self, editor):
        super().__init__(editor)
        self.editor = editor

    def sizeHint(self):
        return QSize(self.editor.ancho_numeros_linea(), 0)

    def paintEvent(self, event):
        self.editor.pintar_numeros_linea(event)


class EditorCodigo(QPlainTextEdit):
    """Editor de codigo con numeros de linea y resaltado de la linea actual."""

    def __init__(self):
        super().__init__()
        self.setFont(QFont("Consolas", 11))
        self.setTabStopDistance(self.fontMetrics().horizontalAdvance(" ") * 4)
        self.setPlaceholderText("Escribe tu código EYKOL aquí...")

        self.area_numeros = _AreaNumerosLinea(self)

        self.blockCountChanged.connect(self._actualizar_margen)
        self.updateRequest.connect(self._actualizar_area_numeros)
        self.cursorPositionChanged.connect(self._resaltar_linea_actual)

        self._actualizar_margen(0)
        self._resaltar_linea_actual()

    def ancho_numeros_linea(self):
        digitos = len(str(max(1, self.blockCount())))
        return 20 + self.fontMetrics().horizontalAdvance("9") * max(2, digitos)

    def _actualizar_margen(self, _):
        self.setViewportMargins(self.ancho_numeros_linea(), 0, 0, 0)

    def _actualizar_area_numeros(self, rect, dy):
        if dy:
            self.area_numeros.scroll(0, dy)
        else:
            self.area_numeros.update(0, rect.y(), self.area_numeros.width(), rect.height())

        if rect.contains(self.viewport().rect()):
            self._actualizar_margen(0)

    def resizeEvent(self, event):
        super().resizeEvent(event)
        contenido = self.contentsRect()
        self.area_numeros.setGeometry(
            QRect(contenido.left(), contenido.top(), self.ancho_numeros_linea(), contenido.height())
        )

    def _resaltar_linea_actual(self):
        selecciones = []
        if not self.isReadOnly():
            seleccion = QTextEdit.ExtraSelection()
            seleccion.format.setBackground(QColor("#202235"))
            seleccion.format.setProperty(QTextFormat.Property.FullWidthSelection, True)
            seleccion.cursor = self.textCursor()
            seleccion.cursor.clearSelection()
            selecciones.append(seleccion)
        self.setExtraSelections(selecciones)
        self.area_numeros.update()

    def pintar_numeros_linea(self, event):
        painter = QPainter(self.area_numeros)
        painter.fillRect(event.rect(), QColor("#12131A"))
        painter.setFont(self.font())

        bloque = self.firstVisibleBlock()
        numero = bloque.blockNumber()
        linea_actual = self.textCursor().blockNumber()
        top = round(self.blockBoundingGeometry(bloque).translated(self.contentOffset()).top())
        bottom = top + round(self.blockBoundingRect(bloque).height())

        while bloque.isValid() and top <= event.rect().bottom():
            if bloque.isVisible() and bottom >= event.rect().top():
                painter.setPen(QColor("#E5E7EB") if numero == linea_actual else QColor("#6B7280"))
                painter.drawText(
                    0,
                    top,
                    self.area_numeros.width() - 10,
                    self.fontMetrics().height(),
                    Qt.AlignmentFlag.AlignRight | Qt.AlignmentFlag.AlignVCenter,
                    str(numero + 1),
                )

            bloque = bloque.next()
            top = bottom
            bottom = top + round(self.blockBoundingRect(bloque).height())
            numero += 1


class VentanaIDE(QMainWindow):

    def __init__(self):
        super().__init__()

        self.setWindowTitle("EYKOL IDE")
        self.resize(1120, 740)
        self.setStyleSheet(ESTILO_OSCURO)
        self.setWindowIcon(_crear_icono("logo"))

        self.archivo_actual = None

        self.editor = EditorCodigo()
        self.resaltador = ResaltadorEYKOL(self.editor.document())
        self.editor.cursorPositionChanged.connect(self._actualizar_posicion_cursor)

        self._crear_acciones()
        self._crear_menu()
        self._crear_barra_herramientas()
        self._construir_interfaz()
        self._crear_barra_estado()

        self._cargar_explorador()
        self._abrir_archivo_inicial()

    # ---------------------------- Acciones y menus ---------------------------
    def _crear_acciones(self):
        self.accion_nuevo = QAction(_crear_icono("new"), "&New", self)
        self.accion_nuevo.setShortcut("Ctrl+N")
        self.accion_nuevo.setToolTip("Nuevo documento (Ctrl+N)")
        self.accion_nuevo.triggered.connect(self.nuevo_documento)

        self.accion_abrir = QAction(_crear_icono("open"), "&Open", self)
        self.accion_abrir.setShortcut("Ctrl+O")
        self.accion_abrir.setToolTip("Abrir archivo (Ctrl+O)")
        self.accion_abrir.triggered.connect(self.abrir_archivo)

        self.accion_guardar = QAction(_crear_icono("save"), "&Save", self)
        self.accion_guardar.setShortcut("Ctrl+S")
        self.accion_guardar.setToolTip("Guardar archivo (Ctrl+S)")
        self.accion_guardar.triggered.connect(self.guardar_archivo)

        self.accion_salir = QAction("&Exit", self)
        self.accion_salir.setShortcut("Ctrl+Q")
        self.accion_salir.setToolTip("Salir del IDE")
        self.accion_salir.triggered.connect(self.close)

        self.accion_copiar = QAction(_crear_icono("copy"), "&Copy", self)
        self.accion_copiar.setShortcut("Ctrl+C")
        self.accion_copiar.setToolTip("Copiar texto seleccionado (Ctrl+C)")
        self.accion_copiar.triggered.connect(self.editor_copiar)

        self.accion_pegar = QAction(_crear_icono("paste"), "&Paste", self)
        self.accion_pegar.setShortcut("Ctrl+V")
        self.accion_pegar.setToolTip("Pegar texto (Ctrl+V)")
        self.accion_pegar.triggered.connect(self.editor_pegar)

        self.accion_cortar = QAction(_crear_icono("cut"), "Cu&t", self)
        self.accion_cortar.setShortcut("Ctrl+X")
        self.accion_cortar.setToolTip("Cortar texto seleccionado (Ctrl+X)")
        self.accion_cortar.triggered.connect(self.editor_cortar)

        self.accion_buscar = QAction("&Find", self)
        self.accion_buscar.setShortcut("Ctrl+F")
        self.accion_buscar.setToolTip("Buscar texto (Ctrl+F)")
        self.accion_buscar.triggered.connect(self._enfocar_buscador)

        self.accion_ejecutar = QAction(_crear_icono("play"), "&Run Code", self)
        self.accion_ejecutar.setShortcut("F5")
        self.accion_ejecutar.setToolTip("Ejecutar código (F5)")
        self.accion_ejecutar.triggered.connect(self.ejecutar_codigo)

        self.accion_explorador = QAction(_crear_icono("open"), "Explorador", self)
        self.accion_explorador.setToolTip("Mostrar / ocultar explorador")
        self.accion_explorador.triggered.connect(self.alternar_explorador)

        self.accion_acerca = QAction(_crear_icono("about"), "&About", self)
        self.accion_acerca.setShortcut("F1")
        self.accion_acerca.setToolTip("Acerca de EYKOL IDE")
        self.accion_acerca.triggered.connect(self.mostrar_acerca)

        self.addActions([
            self.accion_nuevo,
            self.accion_abrir,
            self.accion_guardar,
            self.accion_salir,
            self.accion_copiar,
            self.accion_pegar,
            self.accion_cortar,
            self.accion_buscar,
            self.accion_ejecutar,
            self.accion_acerca,
        ])

    def _crear_menu(self):
        self.menu_principal = QMenu(self)

        menu_archivo = self.menu_principal.addMenu("&File")
        menu_archivo.addAction(self.accion_nuevo)
        menu_archivo.addAction(self.accion_abrir)
        menu_archivo.addAction(self.accion_guardar)
        menu_archivo.addSeparator()
        menu_archivo.addAction(self.accion_salir)

        menu_edicion = self.menu_principal.addMenu("&Edit")
        menu_edicion.addAction(self.accion_copiar)
        menu_edicion.addAction(self.accion_pegar)
        menu_edicion.addAction(self.accion_cortar)
        menu_edicion.addSeparator()
        menu_edicion.addAction(self.accion_buscar)

        menu_ejecutar = self.menu_principal.addMenu("&Run")
        menu_ejecutar.addAction(self.accion_ejecutar)

        menu_ayuda = self.menu_principal.addMenu("&Help")
        menu_ayuda.addAction(self.accion_acerca)

    def _crear_barra_herramientas(self):
        barra = QToolBar("Herramientas", self)
        barra.setMovable(False)
        barra.setIconSize(QSize(18, 18))
        self.addToolBar(barra)

        # Insignia EYKOL
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

        # Boton de menu desplegable (File, Edit, Run, Help)
        self.boton_menu = QToolButton(self)
        self.boton_menu.setIcon(_crear_icono("menu"))
        self.boton_menu.setIconSize(QSize(18, 18))
        self.boton_menu.setFixedSize(32, 32)
        self.boton_menu.setToolTip("Menú (File, Edit, Run, Help)")
        self.boton_menu.setPopupMode(QToolButton.ToolButtonPopupMode.InstantPopup)
        self.boton_menu.setMenu(self.menu_principal)
        barra.addWidget(self.boton_menu)

        espaciador = QWidget()
        espaciador.setSizePolicy(espaciador.sizePolicy().Policy.Expanding, espaciador.sizePolicy().Policy.Preferred)
        barra.addWidget(espaciador)

        # Buscador
        buscador = QWidget()
        layout_buscar = QHBoxLayout(buscador)
        layout_buscar.setContentsMargins(0, 0, 4, 0)
        layout_buscar.setSpacing(6)

        self.campo_buscar = QLineEdit()
        self.campo_buscar.setObjectName("campoBuscar")
        self.campo_buscar.setFixedWidth(250)
        self.campo_buscar.setPlaceholderText("Buscar texto en el código...")
        self.campo_buscar.returnPressed.connect(self.buscar_texto)
        layout_buscar.addWidget(self.campo_buscar)

        self.boton_buscar = QPushButton("Buscar")
        self.boton_buscar.setObjectName("btnBuscar")
        self.boton_buscar.clicked.connect(self.buscar_texto)
        layout_buscar.addWidget(self.boton_buscar)

        barra.addWidget(buscador)

    # ---------------------------- Interfaz principal -------------------------
    def _construir_interfaz(self):
        central = QWidget()
        self.setCentralWidget(central)

        layout_principal = QHBoxLayout(central)
        layout_principal.setContentsMargins(0, 0, 0, 0)
        layout_principal.setSpacing(0)

        # Franja estrecha izquierda con botones de herramientas
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
                separador.setStyleSheet("background-color: #262837;")
                layout_rail.addWidget(separador)
            for accion in grupo:
                boton = QToolButton(rail)
                boton.setDefaultAction(accion)
                boton.setFixedSize(32, 32)
                boton.setIconSize(QSize(18, 18))
                layout_rail.addWidget(boton)

        layout_rail.addStretch()
        layout_principal.addWidget(rail)

        divisor_h = QSplitter(Qt.Orientation.Horizontal)
        divisor_h.setHandleWidth(1)

        # Panel izquierdo: Explorador
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

        divisor_h.addWidget(self.panel_explorador)

        # Panel derecho: Editor arriba + Terminal y pestañas abajo
        divisor_v = QSplitter(Qt.Orientation.Vertical)
        divisor_v.setHandleWidth(1)

        # Contenedor del editor
        panel_editor = QWidget()
        layout_editor = QVBoxLayout(panel_editor)
        layout_editor.setContentsMargins(0, 0, 0, 0)
        layout_editor.setSpacing(0)

        # Barra superior de pestaña activa + boton Play verde
        barra_tab = QFrame()
        barra_tab.setObjectName("barraTabEditor")
        barra_tab.setFixedHeight(38)
        layout_tab = QHBoxLayout(barra_tab)
        layout_tab.setContentsMargins(0, 0, 10, 0)
        layout_tab.setSpacing(4)

        tab_activo = QFrame()
        tab_activo.setObjectName("tabArchivoActivo")
        layout_tab_activo = QHBoxLayout(tab_activo)
        layout_tab_activo.setContentsMargins(12, 0, 10, 0)
        layout_tab_activo.setSpacing(8)

        punto_verde = QLabel("●")
        punto_verde.setStyleSheet("color: #22C55E; font-size: 11px; background: transparent;")
        self.etiqueta_archivo = QLabel("Sin título.txt")
        self.etiqueta_archivo.setStyleSheet("color: #E5E7EB; font-weight: 500; background: transparent;")
        boton_cerrar_tab = QPushButton("×")
        boton_cerrar_tab.setObjectName("btnCerrarTab")
        boton_cerrar_tab.setToolTip("Nuevo documento")
        boton_cerrar_tab.clicked.connect(self.nuevo_documento)

        layout_tab_activo.addWidget(punto_verde)
        layout_tab_activo.addWidget(self.etiqueta_archivo)
        layout_tab_activo.addWidget(boton_cerrar_tab)

        layout_tab.addWidget(tab_activo)
        layout_tab.addStretch()

        self.boton_ejecutar = QPushButton()
        self.boton_ejecutar.setObjectName("btnEjecutar")
        self.boton_ejecutar.setIcon(_crear_icono("play"))
        self.boton_ejecutar.setIconSize(QSize(18, 18))
        self.boton_ejecutar.setToolTip("Ejecutar código (F5)")
        self.boton_ejecutar.clicked.connect(self.ejecutar_codigo)
        layout_tab.addWidget(self.boton_ejecutar)

        self.boton_limpiar = QPushButton("Limpiar")
        self.boton_limpiar.setObjectName("btnLimpiar")
        self.boton_limpiar.setToolTip("Limpiar editor y resultados")
        self.boton_limpiar.clicked.connect(self.limpiar_editor)
        layout_tab.addWidget(self.boton_limpiar)

        layout_editor.addWidget(barra_tab)
        layout_editor.addWidget(self.editor)

        divisor_v.addWidget(panel_editor)

        # Panel inferior: pestañas de Terminal y analisis
        self.pestanas = QTabWidget()
        fuente_mono = QFont("Consolas", 10)

        self.salida = QPlainTextEdit()
        self.salida.setReadOnly(True)
        self.salida.setFont(fuente_mono)
        self.pestanas.addTab(self.salida, ">_ Terminal")

        self.tabla_tokens = crear_tabla_tokens()
        self.pestanas.addTab(self.tabla_tokens, "Tokens")

        self.tabla_simbolos = crear_tabla_simbolos()
        self.pestanas.addTab(self.tabla_simbolos, "Tabla de Símbolos")

        self.codigo_intermedio = QPlainTextEdit()
        self.codigo_intermedio.setReadOnly(True)
        self.codigo_intermedio.setFont(fuente_mono)
        self.pestanas.addTab(self.codigo_intermedio, "Código Intermedio")

        self.arbol_sintactico = QPlainTextEdit()
        self.arbol_sintactico.setReadOnly(True)
        self.arbol_sintactico.setFont(fuente_mono)
        self.pestanas.addTab(self.arbol_sintactico, "Árbol Sintáctico")

        divisor_v.addWidget(self.pestanas)
        divisor_v.setSizes([400, 260])

        divisor_h.addWidget(divisor_v)
        divisor_h.setSizes([235, 845])

        layout_principal.addWidget(divisor_h)

    def _crear_barra_estado(self):
        barra = self.statusBar()
        self.etiqueta_estado = QLabel("Estado: Listo para analizar.")
        self.etiqueta_estado.setStyleSheet("padding-left: 8px; background: transparent;")
        barra.addWidget(self.etiqueta_estado)

        self.etiqueta_cursor = QLabel("Ln 1, Col 1")
        self.etiqueta_cursor.setStyleSheet("padding-right: 14px; background: transparent;")
        barra.addPermanentWidget(self.etiqueta_cursor)

        etiqueta_lenguaje = QLabel("UTF-8   EYKOL")
        etiqueta_lenguaje.setStyleSheet("padding-right: 12px; background: transparent;")
        barra.addPermanentWidget(etiqueta_lenguaje)

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

    def _al_seleccionar_archivo(self, item, _columna):
        ruta = item.data(0, Qt.ItemDataRole.UserRole)
        if ruta:
            self._cargar_archivo(Path(ruta))

    def _abrir_archivo_inicial(self):
        inicial = RUTA_EJEMPLOS / "ciclo_durante.txt"
        if inicial.exists():
            self._cargar_archivo(inicial)
            self.ejecutar_codigo()

    def _cargar_archivo(self, archivo):
        try:
            contenido = archivo.read_text(encoding="utf-8-sig")
        except OSError as error:
            QMessageBox.warning(self, "Error", f"No se pudo abrir el archivo:\n{error}")
            return

        self.editor.setPlainText(contenido)
        self.archivo_actual = archivo
        self.etiqueta_archivo.setText(archivo.name)
        self._seleccionar_en_explorador(archivo)
        self.etiqueta_estado.setStyleSheet("padding-left: 8px; color: #9CA3AF; background: transparent;")
        self.etiqueta_estado.setText(f"Archivo abierto: {archivo.name}")

    def nuevo_documento(self):
        self.editor.clear()
        self.archivo_actual = None
        self.etiqueta_archivo.setText("Sin título.txt")
        self.explorador.clearSelection()
        self.etiqueta_estado.setStyleSheet("padding-left: 8px; color: #9CA3AF; background: transparent;")
        self.etiqueta_estado.setText("Estado: Listo para analizar.")

    def abrir_archivo(self):
        ruta, _ = QFileDialog.getOpenFileName(
            self,
            "Abrir archivo",
            str(RUTA_EJEMPLOS),
            "Archivos de texto (*.txt);;Todos los archivos (*)",
        )
        if ruta:
            self._cargar_archivo(Path(ruta))

    def guardar_archivo(self):
        if self.archivo_actual is None:
            ruta, _ = QFileDialog.getSaveFileName(
                self,
                "Guardar archivo",
                str(RUTA_EJEMPLOS / "nuevo_programa.txt"),
                "Archivos de texto (*.txt);;Todos los archivos (*)",
            )
            if not ruta:
                return
            self.archivo_actual = Path(ruta)

        try:
            self.archivo_actual.write_text(self.editor.toPlainText(), encoding="utf-8")
            self.etiqueta_archivo.setText(self.archivo_actual.name)
            self._cargar_explorador()
            self._seleccionar_en_explorador(self.archivo_actual)
            self.etiqueta_estado.setStyleSheet("padding-left: 8px; color: #34D399; background: transparent;")
            self.etiqueta_estado.setText(f"Guardado: {self.archivo_actual.name}")
        except OSError as error:
            QMessageBox.warning(self, "Error", f"No se pudo guardar el archivo:\n{error}")

    # ---------------------------- Edicion y busqueda -------------------------
    def editor_copiar(self):
        self.editor.copy()

    def editor_cortar(self):
        self.editor.cut()

    def editor_pegar(self):
        self.editor.paste()

    def _enfocar_buscador(self):
        self.campo_buscar.setFocus()
        self.campo_buscar.selectAll()

    def buscar_texto(self):
        texto = self.campo_buscar.text()
        if not texto:
            self._enfocar_buscador()
            return

        encontrado = self.editor.find(texto)
        if not encontrado:
            cursor_actual = self.editor.textCursor()
            self.editor.moveCursor(QTextCursor.MoveOperation.Start)
            encontrado = self.editor.find(texto)
            if not encontrado:
                self.editor.setTextCursor(cursor_actual)
                self.etiqueta_estado.setStyleSheet("padding-left: 8px; color: #F87171; background: transparent;")
                self.etiqueta_estado.setText(f"Texto no encontrado: '{texto}'")
                return

        self.editor.setFocus()
        self.etiqueta_estado.setStyleSheet("padding-left: 8px; color: #E5E7EB; background: transparent;")
        self.etiqueta_estado.setText(f"Coincidencia encontrada: '{texto}'")

    def limpiar_editor(self):
        self.editor.clear()
        self.campo_buscar.clear()
        self.salida.clear()
        self.codigo_intermedio.clear()
        self.arbol_sintactico.clear()
        self.archivo_actual = None
        self.etiqueta_archivo.setText("Sin título.txt")
        self.explorador.clearSelection()
        self.etiqueta_estado.setStyleSheet("padding-left: 8px; color: #9CA3AF; background: transparent;")
        self.etiqueta_estado.setText("Estado: Listo para analizar.")

        llenar_tabla_tokens(self.tabla_tokens, [])
        llenar_tabla_simbolos(self.tabla_simbolos, {})

    def _actualizar_posicion_cursor(self):
        cursor = self.editor.textCursor()
        linea = cursor.blockNumber() + 1
        columna = cursor.columnNumber() + 1
        self.etiqueta_cursor.setText(f"Ln {linea}, Col {columna}")

    # ---------------------------- Compilacion y salida -----------------------
    def _comando_terminal(self):
        if self.archivo_actual is not None:
            try:
                ruta_rel = self.archivo_actual.relative_to(RUTA_PROYECTO).as_posix()
            except ValueError:
                ruta_rel = self.archivo_actual.name
            return f"$ python main.py {ruta_rel}"
        return "$ python main.py <editor>"

    def ejecutar_codigo(self):
        codigo = self.editor.toPlainText()
        resultado = compilar(codigo)

        if resultado.exito:
            self.etiqueta_estado.setStyleSheet(
                "padding-left: 8px; color: #34D399; font-weight: bold; background: transparent;"
            )
            self.etiqueta_estado.setText("Estado: Código válido (sin errores)")
        else:
            self.etiqueta_estado.setStyleSheet(
                "padding-left: 8px; color: #F87171; font-weight: bold; background: transparent;"
            )
            self.etiqueta_estado.setText(
                f"Estado: Código inválido ({len(resultado.errores)} error(es) detectado(s))"
            )

        lineas_terminal = [self._comando_terminal()]
        if resultado.salida:
            lineas_terminal.extend(str(linea) for linea in resultado.salida)
        if resultado.errores:
            if resultado.salida:
                lineas_terminal.append("")
            lineas_terminal.append("========== ERRORES ==========")
            lineas_terminal.extend(str(error) for error in resultado.errores)
        lineas_terminal.append("$ █")

        self.salida.setPlainText("\n".join(lineas_terminal))

        texto_intermedio = "\n".join(str(linea) for linea in resultado.codigo_intermedio)
        self.codigo_intermedio.setPlainText(texto_intermedio)

        texto_arbol = pprint.pformat(resultado.arbol, indent=4, width=80)
        self.arbol_sintactico.setPlainText(texto_arbol)

        llenar_tabla_tokens(self.tabla_tokens, resultado.tokens)
        llenar_tabla_simbolos(self.tabla_simbolos, resultado.tabla_simbolos)

    def mostrar_acerca(self):
        QMessageBox.about(
            self,
            "Acerca de EYKOL IDE",
            "EYKOL IDE — Equipo 5\nEditor, analizador con PLY y entorno en PyQt6.",
        )


if __name__ == "__main__":
    app = QApplication(sys.argv)
    ventana = VentanaIDE()
    ventana.show()
    sys.exit(app.exec())
