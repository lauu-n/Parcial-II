# Calculadora Basada en Agentes (MESA)

## Descripción
Calculadora distribuida donde cada operación aritmética es un agente (suma, resta, multiplicación, división, potencia) y existe un agente IO que orquesta la evaluación de expresiones mediante notación postfija (RPN - Reverse Polish Notation).

## Requisitos
- Python 3.10–3.12  
- mesa==2.1.1

Instalación de dependencias:
```bash
pip install mesa==2.1.1
```

## Archivos principales
- `agent_calc_mesa.py` — implementación principal de la calculadora con agentes.  

## Cómo ejecutar
1. Activa tu entorno virtual (si corresponde).
2. Sitúate en la carpeta del proyecto y ejecuta:
```bash
python agent_calc_mesa.py
```
3. El resultado de la expresión configurada en `__main__` se imprimirá en la consola. Ejemplo:
```
Resultado final: 9
```

## Sugerencias de pruebas adicionales
- Probar expresiones con paréntesis, distintos precedencias y con números decimales:
  - `("3 + (4 - 2) * 5")`
  - `("2.5 * 4 - 1.25 / 0.5")`
- Probar división por cero para ver manejo de errores en el agente división.

---

# INFORME

## Objetivo
Desarrollar una calculadora distribuida basada en agentes utilizando el framework MESA, en la que cada agente representa una operación aritmética (suma, resta, multiplicación, división y potencia), mientras que un agente de entrada/salida (IO) coordina el flujo de mensajes y la resolución de expresiones.
El objetivo principal es simular el procesamiento concurrente y cooperativo de una expresión matemática mediante comunicación entre agentes.

## Metodología de funcionamiento
- El usuario escribe una expresión aritmética (por ejemplo, 2 + 3 * 4 - 5 ^ 2 / 5).
- El agente IO convierte la expresión infija a notación postfija (RPN) mediante el algoritmo shunting-yard.
- IO recorre la lista postfix y, cuando encuentra un operador, envía un mensaje compute al agente correspondiente (por ejemplo, mul o div) con los operandos.
- El agente de operación calcula el resultado y envía un mensaje result de vuelta al IO.
- IO reemplaza los operandos por el resultado y continúa el proceso hasta dejar un solo valor en la pila.
- El valor final se muestra en pantalla y se registra en el archivo trazas/result.txt.

## Ejemplo rápido / Pruebas
- Ejecuta `agent_calc_mesa.py` y, escribe, por ejemplo:
```
("2 + 3 * 4 - 5 ^ 2 / 5")
```
- Resultado esperado: `9`


