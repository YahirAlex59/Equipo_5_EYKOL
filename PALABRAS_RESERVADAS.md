#palabras reservadas

| Antes (plantilla) | En **EYKOL** | Token | Para qué sirve |
|---|---|---|---|
| `entero` | `ent` | `RENTERO` | Número entero (`5`, `-10`) |
| `decimal` | `deci` | `RDECIMAL` | Número con punto decimal (`3.14`) |
| `cadena` | `txt` | `RCADENA` | Texto entre comillas (`"Hola"`) |
| `booleano` | `boli` | `RBOOLEANO` | Valor lógico |
| `mostrar` | `impt` | `RMOSTRAR` | Imprime un valor en la salida |
| `si` | `si` | `RSI` | Condicional |
| `sino` | `osi` | `RSINO` | Caso contrario (`osi` u `osi si`) |
| `mientras` | `durante` | `RMIENTRAS` | Ciclo mientras se cumpla la condición |
| `para` | `repetir` | `RPARA` | Ciclo con variable de control |
| `verdadero` | `vrd` | `RVERDADERO` | Booleano verdadero |
| `falso` | `fals` | `RFALSO` | Booleano falso |
| `Raiz`| `raiz(x)` | `RRAIZ` | Función integrada para raíz cuadrada |

> [!NOTE]
> El lenguaje distingue entre **mayúsculas y minúsculas**: `ent` es palabra reservada, mientras que `ENT` o `Ent` se consideran nombres de variables.

---

## Operadores y comentarios

- **Aritméticos:** `+`, `-`, `*`, `/`, `%`
- **Relacionales:** `<`, `>`, `<=`, `>=`, `==`, `!=`
- **Lógicos:** `&&` (AND), `||` (OR), `!` (NOT)
- **Comentarios:**
  - Una línea: `// comentario`
  - Varias líneas: `/* comentario */`

---

## Ejemplos
### Declaración y asignación
```
ent edad = 20;
deci promedio = 9.5;
txt nombre = "Ana";
boli activo = vrd;

edad = edad + 1;
```

### Imprimir en pantalla (`impt`)
```
impt("Hola " + nombre);
impt(edad * 2);
```

### Raíz cuadrada (`raiz`)
```
deci hip = raiz(3.0 * 3.0 + 4.0 * 4.0);
impt(hip);   // 5.0
```

### Condicionales (`si` / `osi`)
```
si (promedio >= 9) {
    impt("Excelente");
} osi si (promedio >= 7) {
    impt("Aprobado");
} osi {
    impt("Reprobado");
}
```

### Ciclo `durante`
```
ent c = 3;
durante (c > 0) {
    impt(c);
    c = c - 1;
}
```

### Ciclo `repetir`
```
repetir (ent i = 1; i <= 5; i = i + 1) {
    impt(i);
}
```