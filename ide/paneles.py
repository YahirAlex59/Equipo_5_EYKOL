from PyQt6.QtWidgets import (
    QAbstractItemView,
    QHeaderView,
    QTableWidget,
    QTableWidgetItem,
)


def _leer(obj, *nombres, defecto=""):
    """Obtiene un campo de un objeto o diccionario probando varios nombres."""
    for nombre in nombres:
        if isinstance(obj, dict) and nombre in obj:
            return obj[nombre]
        if hasattr(obj, nombre):
            return getattr(obj, nombre)
    return defecto


def _crear_tabla(columnas):
    tabla = QTableWidget()
    tabla.setColumnCount(len(columnas))
    tabla.setHorizontalHeaderLabels(columnas)
    tabla.setEditTriggers(QAbstractItemView.EditTrigger.NoEditTriggers)
    tabla.setAlternatingRowColors(False)
    tabla.verticalHeader().setVisible(False)
    tabla.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
    tabla.setStyleSheet(
        """
        QTableWidget {
            background-color: #12131A;
            color: #E5E7EB;
            gridline-color: #262837;
            border: none;
            selection-background-color: #252338;
            selection-color: #FFFFFF;
        }
        QHeaderView::section {
            background-color: #181924;
            color: #9CA3AF;
            border: none;
            border-bottom: 1px solid #262837;
            border-right: 1px solid #262837;
            padding: 6px;
            font-weight: bold;
        }
        """
    )
    return tabla


def _poner_fila(tabla, fila, valores):
    for columna, valor in enumerate(valores):
        tabla.setItem(fila, columna, QTableWidgetItem(str(valor)))


# ---------------- Tabla de Tokens ----------------
def crear_tabla_tokens():
    """Crea una tabla vacia con columnas Tipo, Valor y Linea."""
    return _crear_tabla(["Tipo", "Valor", "Línea"])


def llenar_tabla_tokens(tabla, tokens):
    """Llena la tabla con la lista de tokens del analizador lexico."""
    tabla.setRowCount(0)
    tokens = tokens or []
    tabla.setRowCount(len(tokens))

    for fila, tok in enumerate(tokens):
        if isinstance(tok, (tuple, list)):
            tipo = tok[0] if len(tok) > 0 else ""
            valor = tok[1] if len(tok) > 1 else ""
            linea = tok[2] if len(tok) > 2 else ""
        else:
            tipo = _leer(tok, "type", "tipo")
            valor = _leer(tok, "value", "valor")
            linea = _leer(tok, "lineno", "linea")
        _poner_fila(tabla, fila, [tipo, valor, linea])


# ---------------- Tabla de Simbolos ----------------
def crear_tabla_simbolos():
    """Crea una tabla vacia con columnas Variable, Tipo y Valor."""
    return _crear_tabla(["Variable", "Tipo", "Valor"])


def llenar_tabla_simbolos(tabla, tabla_simbolos):
    """Llena la tabla con las variables declaradas (nombre -> info)."""
    tabla.setRowCount(0)
    tabla_simbolos = tabla_simbolos or {}
    tabla.setRowCount(len(tabla_simbolos))

    for fila, (nombre, info) in enumerate(tabla_simbolos.items()):
        if isinstance(info, (tuple, list)):
            tipo = info[0] if len(info) > 0 else ""
            valor = info[1] if len(info) > 1 else ""
        elif isinstance(info, dict) or hasattr(info, "__dict__"):
            tipo = _leer(info, "tipo", "type")
            valor = _leer(info, "valor", "value")
        else:
            tipo, valor = "", info
        _poner_fila(tabla, fila, [nombre, tipo, valor])