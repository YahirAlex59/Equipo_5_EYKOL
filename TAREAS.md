
1. **Personalizar el lenguaje**: cambiar las palabras clave de la plantilla por las nuestras (por ejemplo `entero` → `ent`).
2. **Compilador**: que analice y ejecute programas escritos en nuestro lenguaje. Ya está la base.
3. **IDE con PyQt6**: una ventana donde se escribe el código, se presiona **Ejecutar** y se ve el resultado.

---

## como está organizado el proyecto

```
ProyectoPly/
├── main.py                  ejecuta un programa desde consola (para probar)
├── TAREAS.md                este archivo
├── compilador/              TODO el compilador vive aquí
│   ├── lexico.py            Fase 1: tokens y PALABRAS CLAVE
│   ├── sintactico.py        Fase 2: gramática (reglas del lenguaje)
│   ├── semantico.py         Fase 3: revisa que las variables existan
│   ├── interprete.py        Fase 4: ejecuta el programa
│   ├── generacion.py        Fase 5: código intermedio (t1 = a + b)
│   ├── compilador.py        une todas las fases: compilar(texto)
│   └── errores.py           tipo de error común a todas las fases
├── ejemplos/                programas de prueba en NUESTRO lenguaje (.txt)
│   ├── ejemplo.txt
│   └── errores.txt
├── plantilla_original/      código original de la plantilla (solo referencia, NO tocar)
└── ply/                     librería PLY (NO tocar)
```

### ¿Cómo fluye el programa?
```
texto ─► lexico.py ─► sintactico.py ─► semantico.py ─► interprete.py ─► salida
          (tokens)       (árbol)        (validación)     (ejecución)
```

---

## Cómo probar
Desde la carpeta `ProyectoPly`:

```bash
python main.py                              # ejecuta ejemplos/ejemplo.txt
python main.py ejemplos/hipotenusa.txt      # ejecuta otro archivo
python main.py ejemplos/ejemplo.txt --todo  # muestra tokens, árbol, código intermedio y tabla de símbolos
```

### Sintaxis ACTUAL (la de la plantilla, todavía sin personalizar)
```
entero x = 5;                       // tipos: entero, decimal, cadena, booleano
x = x + 1;                          // asignación
mostrar("x vale " + x);             // imprimir
si (x > 3) { ... } sino { ... }     // condicional
mientras (x < 10) { ... }           // ciclo
para (entero i = 0; i < 5; i = i + 1) { ... }
// comentario de una línea    /* comentario de varias */
```
Operadores: `+ - * / %`, `< > <= >= == !=`, `&& || !`

---

## TAREAS DE ESTA SEMANA (Fase 1: diseño)

> [!IMPORTANT]
> Por ahora **no se modifica el código del compilador**. Primero decidimos cómo se verá el lenguaje.

### Tarea 1: Palabras clave del lenguaje
**Dónde:** escribir la propuesta en este archivo (tabla de abajo) o mandarla al grupo.

Llenar la tabla con el nombre que tendrá cada palabra en nuestro lenguaje:

| Plantilla actual | Nuestro lenguaje | Para qué sirve |
|---|---|---|
| `entero` | `ent` | número entero |
| `decimal` | | número con punto |
| `cadena` | | texto |
| `booleano` | | verdadero/falso |
| `mostrar` | | imprimir en pantalla |
| `si` | | condicional |
| `sino` | | si no se cumple |
| `mientras` | | ciclo |
| `para` | | ciclo con contador |
| `verdadero` | | valor lógico |
| `falso` | | valor lógico |

**Opcional:** proponer si cambiamos símbolos, por ejemplo `&&` → `y`, `||` → `o`, o si las llaves `{ }` se quedan.

> [!NOTE]
> Más adelante el cambio se hará en **`compilador/lexico.py`**, en el diccionario `reservadas` (al inicio del archivo). Solo se cambia el texto de la izquierda:
> ```python
> 'entero' : 'RENTERO',   →   'ent' : 'RENTERO',
> ```

---

### Tarea 2: Script de la hipotenusa
**Dónde:** crear el archivo **`ejemplos/hipotenusa.txt`**

Escribir en **nuestro lenguaje** (con las palabras de la Tarea 1) un programa que:
1. Declare los catetos `a` y `b` (decimales).
2. Valide con un condicional que sean mayores que 0.
3. Calcule la hipotenusa: `c = √(a² + b²)`.
4. Muestre el resultado, por ejemplo: `La hipotenusa es 5.0`.

> [!WARNING]
> **El lenguaje todavía NO tiene raíz cuadrada ni potencia.** Escriban el programa **como les gustaría que se viera**, aunque aún no funcione. Deben proponer una de estas opciones:
> - **Opción A:** una función, por ejemplo `raiz(x)`.
> - **Opción B:** un operador de potencia, por ejemplo `x ^ 0.5`.
>
> Esa decisión define qué agregamos al compilador después.

---

### Tarea 3: Programas de prueba
**Dónde:** carpeta **`ejemplos/`**

Crear estos archivos en nuestro lenguaje:

| Archivo | Qué debe hacer |
|---|---|
| `ejemplos/factorial.txt` | calcular el factorial de un número con un ciclo |
| `ejemplos/tabla.txt` | mostrar la tabla de multiplicar de un número |
| `ejemplos/mayor.txt` | decir cuál de 3 números es el mayor (condicionales) |
| `ejemplos/con_errores.txt` | un programa con errores **a propósito**: un carácter raro (`@`), un `;` faltante, una variable sin declarar y una división entre 0 |

Pueden basarse en `ejemplos/ejemplo.txt` para ver cómo se escribe.

---

### Tarea 4: Entorno y PyQt6
**Dónde:** su computadora y luego una carpeta nueva **`ide/`**

1. Comprobar que `python main.py` funciona en su máquina.
2. Instalar PyQt6:
   ```bash
   pip install PyQt6
   ```
3. Crear **`ide/prueba_ventana.py`** con una ventana sencilla que tenga:
   - un cuadro de texto grande (`QPlainTextEdit`) para escribir código,
   - un botón **Ejecutar** (`QPushButton`),
   - un cuadro abajo para la salida (`QPlainTextEdit` de solo lectura).

   Por ahora el botón puede no hacer nada.
4. Investigar cómo conectar el botón a una función (`boton.clicked.connect(...)`).


---

## Entregables para la próxima reunión
- [ ] Tabla de palabras clave llena (Tarea 1)
- [ ] Decisión: ¿`raiz(x)` o `x ^ y`? (Tarea 2)
- [ ] `ejemplos/hipotenusa.txt` (Tarea 2)
- [ ] Programas de prueba en `ejemplos/` (Tarea 3)
- [ ] `ide/prueba_ventana.py` con la ventana vacía (Tarea 4)

---

## Lo que sigue después (fases siguientes)

| Fase | Qué se hará | Archivos |
|---|---|---|
| 2 | Cambiar las palabras clave a las nuestras | `compilador/lexico.py` |
| 3 | Agregar raíz o potencia para la hipotenusa | `lexico.py`, `sintactico.py`, `semantico.py`, `interprete.py`, `generacion.py` |
| 4 | Hacer el IDE completo (editor, ejecutar, salida, errores, abrir/guardar) | `ide/` |
| 5 | Probar todo con los programas de `ejemplos/` | `ejemplos/` |

---

## Reglas para trabajar en equipo
1. **No tocar** `ply/` ni `plantilla_original/`.
2. Antes de empezar: `git pull`. Al terminar: `git add`, `git commit -m "qué hice"` y `git push`.
3. Cada quien trabaja **en sus propios archivos** para no pisarse el trabajo.
4. Los archivos `parsetab.py` y `parser.out` se generan solos: **no se suben** (ya están en `.gitignore`).
5. Si algo falla, ejecuten `python main.py archivo.txt --todo` y manden la salida al grupo.
