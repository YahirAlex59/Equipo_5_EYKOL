
import sys
from pathlib import Path

from PyQt6.QtWidgets import (
    QApplication,
    QMainWindow,
    QWidget,
    QVBoxLayout,
    QPlainTextEdit,
    QPushButton,
    QLabel
)

RUTA_PROYECTO = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(RUTA_PROYECTO))

from compilador.compilador import compilar


class VentanaIDE(QMainWindow):

    def __init__(self):
        super().__init__()

        self.setWindowTitle("EYKOL")
        self.resize(900, 650)

        central = QWidget()
        self.setCentralWidget(central)

        layout = QVBoxLayout(central)

        layout.addWidget(QLabel("Editor de código"))

        self.editor = QPlainTextEdit()
        self.editor.setPlaceholderText("Escribe tu código aquí...")
        layout.addWidget(self.editor)

        self.boton = QPushButton("Ejecutar")
        self.boton.clicked.connect(self.ejecutar_codigo)
        layout.addWidget(self.boton)

        layout.addWidget(QLabel("Salida"))

        self.salida = QPlainTextEdit()
        self.salida.setReadOnly(True)
        layout.addWidget(self.salida)

    def ejecutar_codigo(self):
        codigo = self.editor.toPlainText()
        resultado = compilar(codigo)

        if resultado.exito:
            texto = "\n".join(str(linea) for linea in resultado.salida)
        else:
            texto = "\n".join(str(error) for error in resultado.errores)

        self.salida.setPlainText(texto)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    ventana = VentanaIDE()
    ventana.show()
    sys.exit(app.exec())
