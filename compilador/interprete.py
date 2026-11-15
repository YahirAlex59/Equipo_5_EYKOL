# -----------------------------------------------------------------------------
# Fase 4: ejecución (intérprete)
# Recorre el árbol que armó el parser y lo ejecuta.
# En lugar de print(), guarda lo que el programa muestra en una lista para que
# el IDE lo pueda poner en su panel de salida.
# -----------------------------------------------------------------------------
import math
import operator

from .errores import ErrorCompilacion

OPERADORES = {
    '+': operator.add, '-': operator.sub, '*': operator.mul, '%': operator.mod,
    '<': operator.lt, '>': operator.gt, '<=': operator.le, '>=': operator.ge,
    '==': operator.eq, '!=': operator.ne,
}

# Tipo del lenguaje -> tipo de Python
TIPOS = {'ent': int, 'deci': float, 'txt': str, 'boli': bool}

# Evita que un ciclo infinito congele el IDE
MAX_ITERACIONES = 100_000


def _error(mensaje):
    raise ErrorCompilacion('Ejecución', mensaje)


def _convertir(tipo, valor, nombre):
    try:
        return TIPOS[tipo](valor)
    except (TypeError, ValueError):
        _error("no se puede guardar %r en la variable '%s' de tipo %s" % (valor, nombre, tipo))


def _texto(valor):
    """Cómo se muestra un valor en la salida."""
    if type(valor) is bool:
        return 'vrd' if valor else 'fals'
    return str(valor)


class Interprete:
    def __init__(self):
        self.tabla = {}      # tabla de símbolos: nombre -> (tipo, valor)
        self.salida = []     # líneas que el programa mostró

    # ---------------------------- Expresiones --------------------------------
    def evaluar(self, e):
        if e[0] == 'valor':
            return e[1]
        if e[0] == 'negativo':
            return -self.evaluar(e[1])
        if e[0] == 'not':
            return not self.evaluar(e[1])
        if e[0] == 'raiz':
            valor = self.evaluar(e[1])
            if type(valor) not in (int, float) or type(valor) is bool:
                _error("raiz() requiere un número, se recibió %s" % _texto(valor))
            if valor < 0:
                _error("no se puede calcular la raíz cuadrada de un número negativo (%s)" % valor)
            return math.sqrt(valor)
        if e[0] == 'id':
            if e[1] not in self.tabla:
                _error("la variable '%s' no está declarada" % e[1])
            return self.tabla[e[1]][1]

        # binaria
        op, izq = e[1], self.evaluar(e[2])
        if op == '&&':
            return bool(izq) and bool(self.evaluar(e[3]))
        if op == '||':
            return bool(izq) or bool(self.evaluar(e[3]))
        der = self.evaluar(e[3])
        try:
            if op in ('/', '%') and der == 0:
                _error('división entre cero')
            if op == '/':
                if type(izq) is int and type(der) is int:   # división entera, como en C
                    return int(izq / der)
                return izq / der
            if op == '+' and (type(izq) is str or type(der) is str):
                return _texto(izq) + _texto(der)           # concatenación: "x = " + 5
            return OPERADORES[op](izq, der)
        except TypeError:
            _error("no se puede aplicar '%s' a %s y %s" % (op, _texto(izq), _texto(der)))

    # ---------------------------- Instrucciones ------------------------------
    def ejecutar(self, instrucciones):
        for ins in instrucciones:
            tipo_ins = ins[0]

            if tipo_ins == 'declarar':
                _, tipo, nombre, expr = ins
                valor = self.evaluar(expr) if expr else TIPOS[tipo]()
                self.tabla[nombre] = (tipo, _convertir(tipo, valor, nombre))

            elif tipo_ins == 'asignar':
                _, nombre, expr = ins
                if nombre not in self.tabla:
                    _error("la variable '%s' no está declarada" % nombre)
                tipo = self.tabla[nombre][0]
                self.tabla[nombre] = (tipo, _convertir(tipo, self.evaluar(expr), nombre))

            elif tipo_ins == 'mostrar':
                self.salida.append(_texto(self.evaluar(ins[1])))

            elif tipo_ins == 'si':
                _, condicion, entonces, sino = ins
                self.ejecutar(entonces if self.evaluar(condicion) else sino)

            elif tipo_ins == 'mientras':
                _, condicion, cuerpo = ins
                vueltas = 0
                while self.evaluar(condicion):
                    vueltas = self._contar(vueltas)
                    self.ejecutar(cuerpo)

            elif tipo_ins == 'para':
                _, inicio, condicion, paso, cuerpo = ins
                self.ejecutar([inicio])
                vueltas = 0
                while self.evaluar(condicion):
                    vueltas = self._contar(vueltas)
                    self.ejecutar(cuerpo)
                    self.ejecutar([paso])

    def _contar(self, vueltas):
        vueltas += 1
        if vueltas > MAX_ITERACIONES:
            _error('el ciclo superó %d vueltas (¿ciclo infinito?)' % MAX_ITERACIONES)
        return vueltas


def ejecutar(arbol):
    """Ejecuta el árbol. Regresa (lineas_de_salida, tabla_de_simbolos)."""
    interprete = Interprete()
    interprete.ejecutar(arbol)
    return interprete.salida, interprete.tabla
