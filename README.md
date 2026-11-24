# EYKOL

**EYKOL** es un lenguaje de programación inventado por el Equipo 5, junto con su
compilador e IDE. El compilador realiza análisis léxico, sintáctico y semántico, genera
código intermedio y ejecuta el programa. Incluye un IDE gráfico con editor, resaltado de
sintaxis y paneles para ver cada fase.

## Equipo

- Yahir
- Karol
- Edsson

## Requisitos

- Python 3.10 o superior
- [PyQt6](https://pypi.org/project/PyQt6/) (para el IDE)
- [ply](https://pypi.org/project/ply/) (analizadores léxico y sintáctico)

```bash
pip install PyQt6 ply
```

## Cómo usar el compilador en consola

```bash
python main.py ejemplos/hipotenusa.ko
python main.py ejemplos/ejemplo.ko --todo
```

La opción `--todo` muestra todas las fases del compilador.

Los programas EYKOL usan la extensión **`.ko`**. El IDE guarda siempre con esa extensión;
los archivos `.txt` antiguos se pueden abrir y, al guardarlos, se guardan como `.ko`.

## Cómo abrir el IDE

```bash
python main.py
```

Sin argumentos se abre la ventana del IDE. También se puede abrir directamente con
`python ide/ventana_ide.py`.

## Palabras reservadas

`ent`, `deci`, `txt`, `boli`, `si`, `osi`, `durante`, `repetir`, `impt`, `vrd`, `fals`, `raiz`

La lista completa está en `PALABRAS_RESERVADAS.md`.

## Ejemplos

La carpeta `ejemplos/` contiene programas de muestra, entre ellos `ciclo_durante.ko`
y `logica_booleana.ko`.

## Estructura del proyecto

```
compilador/  Analizadores léxico, sintáctico, semántico, código intermedio e intérprete
ejemplos/    Programas de ejemplo en EYKOL
ide/         Interfaz gráfica (editor, resaltador, paneles)
main.py      Punto de entrada (consola e IDE)
```
