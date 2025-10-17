# PARCIAL II – Paradigmas de Programación

Cada punto implementa un enfoque diferente de la programación y aplica los principios del paradigma correspondiente (orientado a objetos, basado en agentes, entre otros).

***

## Estructura del repositorio

Está organizado por carpetas, una para cada punto del parcial:
- Punto 1:
  - README.py
  - perceptronn.py
- Punto 2:
  - README.py
  - agent_calc_mesa.py
- Punto 3:
  - README.py
  - calculadoraCientifica.kt
 
***

## Puntos desarrollados

### 1. Perceptrón Simple
* **Paradigma:** Programación basada en agentes.
* **Lenguaje:** Python.
* **Descripción:**
    Implementa un modelo de **perceptrón** que aprende a clasificar entradas binarias mediante entrenamiento supervisado. Utiliza librerías como `numpy` y `matplotlib` para el procesamiento y la visualización del aprendizaje.

### 2. Calculadora basada en agentes
* **Paradigma:** Programación basada en agentes.
* **Lenguaje:** Python.
* **Descripción:**
  Implementación de una calculadora distribuida usando el paradigma de agentes en MESA, donde cada operación aritmética (suma, resta, multiplicación, división y potencia) es gestionada por un agente autónomo.

### 3. Calculadora Científica
* **Paradigma:** Programación Orientada a Objetos (POO).
* **Lenguaje:** Kotlin.
* **Descripción:**
    Desarrolla una calculadora científica que permite realizar operaciones básicas (suma, resta, multiplicación, división) y avanzadas (trigonometría, potencias, logaritmos, raíces). Aplica conceptos de **clases, herencia** y **encapsulamiento**.

## Ejecución general

1.  **Entra en la carpeta del punto que desees probar.**
2.  **Ejecuta según el lenguaje del punto:**
    * **Python:** `python nombre_archivo.py`
    * **Kotlin:** `kotlinc Main.kt -include-runtime -d archivo.jar && java -jar archivo.jar`
