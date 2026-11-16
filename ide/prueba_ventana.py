import sys
from pathlib import Path

from PyQt6.QtCore import QPoint, QSize, Qt
from PyQt6.QtGui import (
    QAction,
    QColor,
    QFont,
    QIcon,
    QPainter,
    QPalette,
    QPen,
    QPixmap,
    QPolygon,
)
from PyQt6.QtWidgets import (
    QApplication,
    QFileDialog,
    QMainWindow,
    QMessageBox,
    QPlainTextEdit,
    QToolBar,
)

RUTA_PROYECTO = Path(__file__).resolve().parent.parent
RUTA_EJEMPLOS = RUTA_PROYECTO / "ejemplos"

COLOR_ICONO = QColor("#333333")


def _crear_icono(tipo, color=None):
    """Dibuja un icono monocromatico de 24x24 para la barra de herramientas."""
    color_icono = color or COLOR_ICONO
    pixmap = QPixmap(24, 24)
    pixmap.fill(Qt.GlobalColor.transparent)

    p = QPainter(pixmap)
    p.setRenderHint(QPainter.RenderHint.Antialiasing)

    if tipo == "new":
        p.setPen(QPen(color_icono, 2.8, Qt.PenStyle.SolidLine, Qt.PenCapStyle.FlatCap))
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
        # Ventana superior y etiqueta inferior en tono claro
        p.setCompositionMode(QPainter.CompositionMode.CompositionMode_Clear)
        p.drawRect(7, 5, 8, 5)
        p.drawRect(7, 13, 10, 6)
        p.setCompositionMode(QPainter.CompositionMode.CompositionMode_SourceOver)
        p.setBrush(color_icono)
        p.drawRect(12, 6, 2, 3)

    elif tipo == "copy":
        # Hoja trasera
        p.setPen(Qt.PenStyle.NoPen)
        p.setBrush(color_icono)
        p.drawRoundedRect(5, 4, 10, 12, 1.5, 1.5)
        # Borde de separacion y hoja delantera
        p.setCompositionMode(QPainter.CompositionMode.CompositionMode_Clear)
        p.drawRoundedRect(8, 7, 11, 13, 1.5, 1.5)
        p.setCompositionMode(QPainter.CompositionMode.CompositionMode_SourceOver)
        p.setBrush(color_icono)
        p.drawRoundedRect(9, 8, 10, 12, 1.5, 1.5)

    elif tipo == "paste":
        p.setPen(Qt.PenStyle.NoPen)
        p.setBrush(color_icono)
        p.drawRoundedRect(6, 6, 12, 14, 2, 2)
        # Clip superior
        p.setCompositionMode(QPainter.CompositionMode.CompositionMode_Clear)
        p.drawRoundedRect(8, 3, 8, 5, 1.5, 1.5)
        p.setCompositionMode(QPainter.CompositionMode.CompositionMode_SourceOver)
        p.setBrush(color_icono)
        p.drawRoundedRect(9, 3, 6, 4, 1.5, 1.5)
        p.drawRect(11, 2, 2, 2)

    elif tipo == "cut":
        pen_hoja = QPen(color_icono, 2.0, Qt.PenStyle.SolidLine, Qt.PenCapStyle.RoundCap)
        p.setPen(pen_hoja)
        p.setBrush(Qt.BrushStyle.NoBrush)
        # Hojas cruzadas
        p.drawLine(7, 4, 15, 15)
        p.drawLine(17, 4, 9, 15)
        # Aros inferiores
        p.drawEllipse(5, 14, 5, 5)
        p.drawEllipse(14, 14, 5, 5)

    elif tipo == "about":
        p.setPen(Qt.PenStyle.NoPen)
        p.setBrush(color_icono)
        p.drawEllipse(4, 4, 16, 16)
        p.setCompositionMode(QPainter.CompositionMode.CompositionMode_Clear)
        fuente = QFont("Serif", 12, QFont.Weight.Bold)
        p.setFont(fuente)
        p.setPen(QColor(0, 0, 0))
        p.drawText(pixmap.rect(), Qt.AlignmentFlag.AlignCenter, "i")

    p.end()
    return QIcon(pixmap)


class VentanaIDE(QMainWindow):

    def __init__(self):
        super().__init__()

        self.setWindowTitle("Sample Editor")
        self.resize(900, 560)

        self.archivo_actual = None

        self.editor = QPlainTextEdit()
        self.setCentralWidget(self.editor)

        self._crear_acciones()
        self._crear_menu()
        self._crear_barra_herramientas()
        self.statusBar()

    def _crear_acciones(self):
        color = self.palette().color(QPalette.ColorRole.WindowText)

        self.accion_nuevo = QAction(_crear_icono("new", color), "&New", self)
        self.accion_nuevo.setShortcut("Ctrl+N")
        self.accion_nuevo.setToolTip("Create a New Document")
        self.accion_nuevo.triggered.connect(self.nuevo_documento)

        self.accion_abrir = QAction(_crear_icono("open", color), "&Open", self)
        self.accion_abrir.setShortcut("Ctrl+O")
        self.accion_abrir.setToolTip("Open an Existing Document")
        self.accion_abrir.triggered.connect(self.abrir_archivo)

        self.accion_guardar = QAction(_crear_icono("save", color), "&Save", self)
        self.accion_guardar.setShortcut("Ctrl+S")
        self.accion_guardar.setToolTip("Save the Current Document")
        self.accion_guardar.triggered.connect(self.guardar_archivo)

        self.accion_salir = QAction("&Exit", self)
        self.accion_salir.setShortcut("Ctrl+Q")
        self.accion_salir.setToolTip("Exit the Application")
        self.accion_salir.triggered.connect(self.close)

        self.accion_copiar = QAction(_crear_icono("copy", color), "&Copy", self)
        self.accion_copiar.setShortcut("Ctrl+C")
        self.accion_copiar.setToolTip("Copy Selected Text")
        self.accion_copiar.triggered.connect(self.editor.copy)

        self.accion_pegar = QAction(_crear_icono("paste", color), "&Paste", self)
        self.accion_pegar.setShortcut("Ctrl+V")
        self.accion_pegar.setToolTip("Paste Copied Text")
        self.accion_pegar.triggered.connect(self.editor.paste)

        self.accion_cortar = QAction(_crear_icono("cut", color), "Cu&t", self)
        self.accion_cortar.setShortcut("Ctrl+X")
        self.accion_cortar.setToolTip("Cut Selected Text")
        self.accion_cortar.triggered.connect(self.editor.cut)

        self.accion_acerca = QAction(_crear_icono("about", color), "&About", self)
        self.accion_acerca.setShortcut("F1")
        self.accion_acerca.setToolTip("About Sample Editor")
        self.accion_acerca.triggered.connect(self.mostrar_acerca)

    def _crear_menu(self):
        barra_menu = self.menuBar()

        menu_archivo = barra_menu.addMenu("&File")
        menu_archivo.addAction(self.accion_nuevo)
        menu_archivo.addAction(self.accion_abrir)
        menu_archivo.addAction(self.accion_guardar)
        menu_archivo.addSeparator()
        menu_archivo.addAction(self.accion_salir)

        menu_edicion = barra_menu.addMenu("&Edit")
        menu_edicion.addAction(self.accion_copiar)
        menu_edicion.addAction(self.accion_pegar)
        menu_edicion.addAction(self.accion_cortar)

        menu_ayuda = barra_menu.addMenu("&Help")
        menu_ayuda.addAction(self.accion_acerca)

    def _crear_barra_herramientas(self):
        barra = QToolBar("Herramientas", self)
        barra.setMovable(False)
        barra.setIconSize(QSize(20, 20))
        self.addToolBar(barra)

        barra.addAction(self.accion_nuevo)
        barra.addAction(self.accion_abrir)
        barra.addAction(self.accion_guardar)
        barra.addAction(self.accion_copiar)
        barra.addAction(self.accion_pegar)
        barra.addAction(self.accion_cortar)
        barra.addAction(self.accion_acerca)

    def nuevo_documento(self):
        self.editor.clear()
        self.archivo_actual = None

    def abrir_archivo(self):
        ruta, _ = QFileDialog.getOpenFileName(
            self,
            "Open File",
            str(RUTA_EJEMPLOS),
            "Text Files (*.txt);;All Files (*)"
        )
        if not ruta:
            return
        try:
            archivo = Path(ruta)
            self.editor.setPlainText(archivo.read_text(encoding="utf-8-sig"))
            self.archivo_actual = archivo
        except OSError as error:
            QMessageBox.warning(self, "Error", f"Could not open file:\n{error}")

    def guardar_archivo(self):
        if self.archivo_actual is None:
            ruta, _ = QFileDialog.getSaveFileName(
                self,
                "Save File",
                str(RUTA_EJEMPLOS / "nuevo_programa.txt"),
                "Text Files (*.txt);;All Files (*)"
            )
            if not ruta:
                return
            self.archivo_actual = Path(ruta)

        try:
            self.archivo_actual.write_text(self.editor.toPlainText(), encoding="utf-8")
            self.statusBar().showMessage(f"Saved: {self.archivo_actual.name}", 3000)
        except OSError as error:
            QMessageBox.warning(self, "Error", f"Could not save file:\n{error}")

    def mostrar_acerca(self):
        QMessageBox.about(
            self,
            "About Sample Editor",
            "Sample Editor - EYKOL (Equipo 5)\nEditor construido con PyQt6."
        )


if __name__ == "__main__":
    app = QApplication(sys.argv)
    ventana = VentanaIDE()
    ventana.show()
    sys.exit(app.exec())
