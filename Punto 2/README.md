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
- `diseño_mba.md` — documento con el diseño del sistema.  
- `informe.docx` — informe para entrega (formato Word).  
- `trazas/` — carpeta con trazas/ejemplos de ejecución.

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
- Abre `agent_calc_mesa.py` y, en el bloque:
```python
if __name__ == '__main__':
    io.set_expression("2 + 3 * 4 - 5 ^ 2 / 5")
```
- Ejecuta el script:
```bash
python agent_calc_mesa.py
```
- Resultado esperado: `9`

Puedes modificar la expresión para probar enteros y decimales. La notación infija es convertida internamente a postfix (shunting-yard) por el agente IO.

## Notas sobre funcionamiento
- El agente IO convierte la expresión infija a postfix (algoritmo shunting-yard) y envía solicitudes `compute` a los agentes de operación.
- Cada agente de operación recibe operandos y devuelve el resultado de su operación.
- El flujo es: IO monta la cola de operaciones en postfix → envía tareas a agentes → recibe resultados parciales → continúa hasta obtener resultado final.
- El sistema está pensado para ser extensible: puedes añadir agentes para funciones trigonométricas, logaritmos, etc.

## Sugerencias de pruebas adicionales
- Probar expresiones con paréntesis, distintos precedencias y con números decimales:
  - `io.set_expression("3 + (4 - 2) * 5")`
  - `io.set_expression("2.5 * 4 - 1.25 / 0.5")`
- Probar división por cero para ver manejo de errores en el agente división.
- Añadir trazas/logging en `trazas/` para analizar mensajes entre agentes.

## Posibles mejoras
- Soportar variables y asignaciones (ej.: `a = 3; a * 4`).
- Añadir concurrencia real (mensajería asíncrona entre agentes).
- Interfaz simple (CLI interactiva) para introducir expresiones en tiempo real.
- Añadir tests unitarios automáticos (pytest) para las operaciones y la conversión infija→postfix.

---