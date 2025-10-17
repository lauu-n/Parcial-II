# Calculadora Basada en Agentes (MESA)

## Descripción
Calculadora distribuida donde cada operación aritmética es un agente (suma, resta, multiplicación, división, potencia) y existe un agente IO que orquesta la evaluación de expresiones mediante notación postfija (RPN - Reverse Polish Notation).

## Requisitos
- Python 3.10–3.12  
- mesa==2.1.1 (o la versión que ya tengas; 2.1.1 funciona correctamente)

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

## Ejemplo rápido / Pruebas
- Ejecuta `agent_calc_mesa.py` y, escribe, por ejemplo:
```
("2 + 3 * 4 - 5 ^ 2 / 5")
```
- Resultado esperado: `9`


## Notas sobre funcionamiento
- El agente IO convierte la expresión infija a postfix (algoritmo shunting-yard) y envía solicitudes `compute` a los agentes de operación.
- Cada agente de operación recibe operandos y devuelve el resultado de su operación.
- El flujo es: IO monta la cola de operaciones en postfix → envía tareas a agentes → recibe resultados parciales → continúa hasta obtener resultado final.
- El sistema está pensado para ser extensible: puedes añadir agentes para funciones trigonométricas, logaritmos, etc.

## Sugerencias de pruebas adicionales
- Probar expresiones con paréntesis, distintos precedencias y con números decimales:
  - `("3 + (4 - 2) * 5")`
  - `("2.5 * 4 - 1.25 / 0.5")`
- Probar división por cero para ver manejo de errores en el agente división.
---
