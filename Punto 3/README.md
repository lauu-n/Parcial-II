# Calculadora científica (pruebas en Kotlin Playground)

**título:** **implementación de una calculadora científica usando POO en Kotlin**

## Descripción
Es un archivo Kotlin pensado para ejecutar en **Kotlin Playground**. Implementa:

- Operaciones básicas (suma, resta, multiplicación, división).
- Funciones científicas (seno, coseno, tangente en grados; potencias; raíces; logaritmos base 10 y natural; exponencial).
- Evaluador de expresiones completas (algoritmo shunting-yard → RPN).
- Memoria (M+, M-, MR, MC).
- Manejo de excepciones para entradas inválidas y división por cero.

## Cómo usar
1. Abrir https://play.kotlinlang.org/
2. Pegar todo el código Kotlin proporcionado en un solo archivo.
3. Pulsar **Run**.
4. En la consola verás las pruebas básicas, funciones científicas, evaluación de expresiones, uso de memoria y manejo de errores.

## Ejemplos de expresiones que se pueden evaluar
- `2+3*4`
- `2 + 3 * sin(30)`
- `2 + 3 * sin(45) - log(10)`
- `3 + 4 * 2 / (1 - 5) ^ 2`
- `sqrt(16) + 2`

## Informe: aplicación de principios de POO

### Encapsulamiento
La calculadora está organizada en clases con responsabilidades claras:
- `Calculadora` (clase base) contiene las operaciones aritméticas básicas.
- `CalculadoraCientifica` (clase derivada) agrega funciones trigonométricas y científicas.
- `Memoria` encapsula la lógica para almacenar y recuperar un valor (M+, M-, MR, MC).
Cada clase mantiene su estado privado cuando corresponde (por ejemplo, `Memoria.valor` es privado) y expone métodos públicos para interactuar. Esto protege la integridad de los datos y oculta detalles de implementación.

### Herencia
`CalculadoraCientifica` hereda de `Calculadora`. Esto permite reutilizar las operaciones básicas (sumar, restar, multiplicar, dividir) y extender con nuevas funcionalidades sin duplicar código. La relación es clara: una calculadora científica **es** una calculadora básica con más capacidades.

### Polimorfismo
Se aplica polimorfismo en el sentido de que `CalculadoraCientifica` puede ser usada en contextos donde se espera una `Calculadora` (polimorfismo por subtipado). Además, el diseño permite sobrecargar métodos en futuras versiones (por ejemplo, si se necesitara sumar enteros o cadenas que representen números). En este ejemplo concreto se maneja entrada en `Double` para mantener precisión pero la arquitectura permite extender métodos para aceptar distintos tipos numéricos.

### Manejo de excepciones
Se implementan comprobaciones y excepciones claras:
- División por cero lanza `ArithmeticException("División por cero")`.
- Logaritmos con argumentos no válidos (≤ 0) lanzan excepciones con mensajes explicativos.
- El evaluador detecta paréntesis desbalanceados y tokens inválidos y lanza `IllegalArgumentException` con mensaje.
En `main` se muestran ejemplos de captura de excepciones y mensajes amigables que podrían mostrarse al usuario.

### Evaluación de expresiones completas
Se implementó el algoritmo shunting-yard para convertir una expresión infija a RPN (notación polaca inversa) y luego evaluarla. El evaluador reconoce:
- Números decimales.
- Operadores: `+ - * / ^`
- Funciones: `sin`, `cos`, `tan`, `log` (base 10), `ln`, `exp`, `sqrt`
- Paréntesis y comas (para futuras extensiones con funciones de varios parámetros).
Las funciones trigonométricas esperan grados (por conveniencia del usuario), y internamente se convierten a radianes antes de aplicar `sin`, `cos`, `tan`.

### Funcionalidades de memoria
La clase `Memoria` ofrece:
- `mPlus(valor)` suma al contenido de memoria.
- `mMinus(valor)` resta del contenido de memoria.
- `mRecall()` devuelve el valor almacenado.
- `mClear()` limpia la memoria.
---

