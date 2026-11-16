
import sys
import pprint
from pathlib import Path

from PyQt6.QtWidgets import (
    QApplication,
    QMainWindow,
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
    QPlainTextEdit,
    QPushButton,
    QLabel,
    QFileDialog,
    QMessageBox,
    QTabWidget
)

RUTA_PROYECTO = Path(__file__).resolve().parent.parent
RUTA_EJEMPLOS = RUTA_PROYECTO / "ejemplos"

sys.path.insert(0, str(RUTA_PROYECTO))

from compilador.compilador import compilar


class VentanaIDE(QMainWindow):

    def __init__(self):
        super().__init__()

        self.setWindowTitle("EYKOL")
        self.resize(1000, 750)

        self.archivo_actual = None

        central = QWidget()
        self.setCentralWidget(central)

        layout = QVBoxLayout(central)

        # Barra de botones
        barra_botones = QHBoxLayout()

        self.boton_ejecutar = QPushButton("Ejecutar")
        self.boton_ejecutar.clicked.connect(self.ejecutar_codigo)
        barra_botones.addWidget(self.boton_ejecutar)

        self.boton_abrir = QPushButton("Abrir archivo")
        self.boton_abrir.clicked.connect(self.abrir_archivo)
        barra_botones.addWidget(self.boton_abrir)

        self.boton_guardar = QPushButton("Guardar")
        self.boton_guardar.clicked.connect(self.guardar_archivo)
        barra_botones.addWidget(self.boton_guardar)

        self.boton_limpiar = QPushButton("Limpiar")
        self.boton_limpiar.clicked.connect(self.limpiar_editor)
        barra_botones.addWidget(self.boton_limpiar)

        layout.addLayout(barra_botones)

        # Editor de código
        layout.addWidget(QLabel("Editor de código"))

        self.editor = QPlainTextEdit()
        self.editor.setPlaceholderText("Escribe tu código aquí...")
        layout.addWidget(self.editor)

        # Pestañas de resultados
        self.pestanas = QTabWidget()

        # Pestaña de salida y errores
        self.salida = QPlainTextEdit()
        self.salida.setReadOnly(True)
        self.pestanas.addTab(self.salida, "Salida / Errores")

        # Pestaña de código intermedio
        self.codigo_intermedio = QPlainTextEdit()
        self.codigo_intermedio.setReadOnly(True)
        self.pestanas.addTab(
            self.codigo_intermedio,
            "Código Intermedio"
        )

        # Pestaña del árbol sintáctico
        self.arbol_sintactico = QPlainTextEdit()
        self.arbol_sintactico.setReadOnly(True)
        self.pestanas.addTab(
            self.arbol_sintactico,
            "Árbol Sintáctico"
        )

        layout.addWidget(self.pestanas)

    def abrir_archivo(self):
        ruta, _ = QFileDialog.getOpenFileName(
            self,
            "Abrir archivo",
            str(RUTA_EJEMPLOS),
            "Archivos de texto (*.txt)"
        )

        if ruta:
            try:
                archivo = Path(ruta)
                contenido = archivo.read_text(encoding="utf-8-sig")

                self.editor.setPlainText(contenido)
                self.archivo_actual = archivo

            except OSError as error:
                QMessageBox.warning(
                    self,
                    "Error",
                    f"No se pudo abrir el archivo:\n{error}"
                )

    def guardar_archivo(self):
        if self.archivo_actual is None:
            ruta, _ = QFileDialog.getSaveFileName(
                self,
                "Guardar archivo",
                str(RUTA_EJEMPLOS / "nuevo_programa.txt"),
                "Archivos de texto (*.txt)"
            )

            if not ruta:
                return

            self.archivo_actual = Path(ruta)

        try:
            contenido = self.editor.toPlainText()

            self.archivo_actual.write_text(
                contenido,
                encoding="utf-8"
            )

            QMessageBox.information(
                self,
                "Guardado",
                "El archivo se guardó correctamente."
            )

        except OSError as error:
            QMessageBox.warning(
                self,
                "Error",
                f"No se pudo guardar el archivo:\n{error}"
            )

    def limpiar_editor(self):
        self.editor.clear()
        self.salida.clear()
        self.codigo_intermedio.clear()
        self.arbol_sintactico.clear()

    def ejecutar_codigo(self):
        codigo = self.editor.toPlainText()
        resultado = compilar(codigo)

        texto_salida = "\n".join(
            str(linea) for linea in resultado.salida
        )

        texto_errores = "\n".join(
            str(error) for error in resultado.errores
        )

        if texto_salida and texto_errores:
            texto = (
                "========== SALIDA ==========\n"
                + texto_salida
                + "\n\n========== ERRORES ==========\n"
                + texto_errores
            )
        elif texto_errores:
            texto = (
                "========== ERRORES ==========\n"
                + texto_errores
            )
        else:
            texto = (
                "========== SALIDA ==========\n"
                + texto_salida
            )

        self.salida.setPlainText(texto)

        # Mostrar código intermedio
        texto_intermedio = "\n".join(
            str(linea) for linea in resultado.codigo_intermedio
        )
        self.codigo_intermedio.setPlainText(texto_intermedio)

        # Mostrar árbol sintáctico
        texto_arbol = pprint.pformat(
            resultado.arbol,
            indent=4,
            width=80
        )
        self.arbol_sintactico.setPlainText(texto_arbol)


if __name__ == "__main__":
    app = QApplication(sys.argv)

    ventana = VentanaIDE()
    ventana.show()

    sys.exit(app.exec())
