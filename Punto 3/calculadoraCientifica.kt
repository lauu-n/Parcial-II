import kotlin.math.*

open class Calculadora {
    fun sumar(a: Double, b: Double) = a + b
    fun restar(a: Double, b: Double) = a - b
    fun multiplicar(a: Double, b: Double) = a * b
    fun dividir(a: Double, b: Double): Double {
        if (b == 0.0) throw ArithmeticException("División por cero")
        return a / b
    }
}

class CalculadoraCientifica: Calculadora() {
    fun senoGrados(g: Double) = sin(Math.toRadians(g))
    fun cosenoGrados(g: Double) = cos(Math.toRadians(g))
    fun tangenteGrados(g: Double) = tan(Math.toRadians(g))
    fun potencia(base: Double, exp: Double) = base.pow(exp)
    fun raiz(valor: Double, n: Double = 2.0) = valor.pow(1.0 / n)
    fun log10v(x: Double): Double {
        if (x <= 0.0) throw ArithmeticException("Logaritmo base 10 inválido")
        return log10(x)
    }
    fun ln(x: Double): Double {
        if (x <= 0.0) throw ArithmeticException("Logaritmo natural inválido")
        return ln(x)
    }
    fun expv(x: Double) = exp(x)
}

class Memoria {
    private var valor: Double = 0.0
    fun mPlus(v: Double) { valor += v }
    fun mMinus(v: Double) { valor -= v }
    fun mRecall(): Double = valor
    fun mClear() { valor = 0.0 }
}

object EvaluadorExpresiones {
    private val opsPrecedence = mapOf(
        "+" to 2, "-" to 2,
        "*" to 3, "/" to 3,
        "^" to 4
    )
    private val rightAssociative = setOf("^")
    private val functions = setOf("sin","cos","tan","log","ln","exp","sqrt")

    private fun isNumber(token: String) = token.toDoubleOrNull() != null
    private fun isFunction(token: String) = functions.contains(token.lowercase())
    private fun isOperator(token: String) = opsPrecedence.containsKey(token)

    fun evaluar(expr: String): Double {
        val rpn = toRPN(expr)
        return evalRPN(rpn)
    }

    private fun toRPN(expr: String): List<String> {
        val tokens = tokenize(expr)
        val output = mutableListOf<String>()
        val ops = ArrayDeque<String>()
        for (token in tokens) {
            when {
                isNumber(token) -> output.add(token)
                isFunction(token) -> ops.addFirst(token)
                token == "," -> {
                    while (ops.isNotEmpty() && ops.first() != "(") output.add(ops.removeFirst())
                }
                isOperator(token) -> {
                    while (ops.isNotEmpty() && isOperator(ops.first())) {
                        val top = ops.first()
                        val precTop = opsPrecedence[top] ?: 0
                        val precTok = opsPrecedence[token] ?: 0
                        if ((top in rightAssociative && precTop > precTok) || (top !in rightAssociative && precTop >= precTok)) {
                            output.add(ops.removeFirst())
                        } else break
                    }
                    ops.addFirst(token)
                }
                token == "(" -> ops.addFirst(token)
                token == ")" -> {
                    while (ops.isNotEmpty() && ops.first() != "(") output.add(ops.removeFirst())
                    if (ops.isEmpty()) throw IllegalArgumentException("Paréntesis desbalanceados")
                    ops.removeFirst()
                    if (ops.isNotEmpty() && isFunction(ops.first())) output.add(ops.removeFirst())
                }
                else -> throw IllegalArgumentException("Token inválido: $token")
            }
        }
        while (ops.isNotEmpty()) {
            val t = ops.removeFirst()
            if (t == "(" || t == ")") throw IllegalArgumentException("Paréntesis desbalanceados")
            output.add(t)
        }
        return output
    }

    private fun tokenize(input: String): List<String> {
        val s = input.replace(" ", "")
        val tokens = mutableListOf<String>()
        var i = 0
        while (i < s.length) {
            val c = s[i]
            when {
                c.isDigit() || c == '.' -> {
                    val start = i
                    i++
                    while (i < s.length && (s[i].isDigit() || s[i] == '.')) i++
                    tokens.add(s.substring(start, i))
                    continue
                }
                c.isLetter() -> {
                    val start = i
                    i++
                    while (i < s.length && s[i].isLetter()) i++
                    val name = s.substring(start, i)
                    tokens.add(name)
                    continue
                }
                c == '+' || c == '*' || c == '/' || c == '^' || c == ',' -> {
                    tokens.add(c.toString())
                }
                c == '-' -> {
                    val prev = if (tokens.isEmpty()) "" else tokens.last()
                    if (prev.isEmpty() || prev == "(" || isOperator(prev) || prev == ",") {
                        // unary minus: represent as (0 - x) by pushing "0" then "-"
                        tokens.add("0")
                        tokens.add("-")
                    } else tokens.add("-")
                }
                c == '(' || c == ')' -> tokens.add(c.toString())
                else -> throw IllegalArgumentException("Caracter inválido: $c")
            }
            i++
        }
        return tokens
    }

    private fun evalRPN(rpn: List<String>): Double {
        val stack = ArrayDeque<Double>()
        for (token in rpn) {
            when {
                isNumber(token) -> stack.addFirst(token.toDouble())
                isOperator(token) -> {
                    if (stack.size < 2) throw IllegalArgumentException("Expresión inválida")
                    val b = stack.removeFirst()
                    val a = stack.removeFirst()
                    val res = when (token) {
                        "+" -> a + b
                        "-" -> a - b
                        "*" -> a * b
                        "/" -> {
                            if (b == 0.0) throw ArithmeticException("División por cero")
                            a / b
                        }
                        "^" -> a.pow(b)
                        else -> throw IllegalArgumentException("Operador desconocido $token")
                    }
                    stack.addFirst(res)
                }
                isFunction(token) -> {
                    if (stack.isEmpty()) throw IllegalArgumentException("Función sin argumento")
                    val x = stack.removeFirst()
                    val res = when (token.lowercase()) {
                        "sin" -> sin(Math.toRadians(x))
                        "cos" -> cos(Math.toRadians(x))
                        "tan" -> tan(Math.toRadians(x))
                        "log" -> if (x > 0.0) log10(x) else throw ArithmeticException("Log base 10 inválido")
                        "ln" -> if (x > 0.0) ln(x) else throw ArithmeticException("Log natural inválido")
                        "exp" -> exp(x)
                        "sqrt" -> if (x >= 0.0) sqrt(x) else throw ArithmeticException("Raíz cuadrada inválida")
                        else -> throw IllegalArgumentException("Función desconocida $token")
                    }
                    stack.addFirst(res)
                }
                else -> throw IllegalArgumentException("Token desconocido en RPN: $token")
            }
        }
        if (stack.size != 1) throw IllegalArgumentException("Expresión inválida")
        return stack.first()
    }
}

fun main() {
    val calc = CalculadoraCientifica()
    val mem = Memoria()

    println("Pruebas básicas:")
    println("3 + 4 = ${calc.sumar(3.0,4.0)}")
    println("10 - 2 = ${calc.restar(10.0,2.0)}")
    println("6 * 7 = ${calc.multiplicar(6.0,7.0)}")
    try {
        println("8 / 0 = ${calc.dividir(8.0,0.0)}")
    } catch (e: Exception) {
        println("8 / 0 → error: ${e.message}")
    }

    println("\nFunciones científicas:")
    println("sin(30°) = ${calc.senoGrados(30.0)}")
    println("cos(60°) = ${calc.cosenoGrados(60.0)}")
    println("tan(45°) = ${calc.tangenteGrados(45.0)}")
    println("2^8 = ${calc.potencia(2.0,8.0)}")
    println("raíz cúbica de 27 = ${calc.raiz(27.0,3.0)}")
    println("log10(100) = ${calc.log10v(100.0)}")
    println("ln(e) = ${calc.ln(E)}")
    println("exp(2) = ${calc.expv(2.0)}")

    println("\nEvaluador de expresiones:")
    val exps = listOf(
        "2+3*4",
        "2 + 3 * sin(30)",
        "2 + 3 * sin(45) - log(10)",
        "3 + 4 * 2 / (1 - 5) ^ 2",
        "-3 + 5",
        "sqrt(16) + 2"
    )
    for (e in exps) {
        try {
            val r = EvaluadorExpresiones.evaluar(e)
            println("$e = $r")
        } catch (ex: Exception) {
            println("$e → error: ${ex.message}")
        }
    }

    println("\nMemoria (M+, M-, MR, MC):")
    mem.mClear()
    mem.mPlus(5.0)
    println("M+5 → MR = ${mem.mRecall()}")
    mem.mPlus(3.2)
    println("M+3.2 → MR = ${mem.mRecall()}")
    mem.mMinus(1.0)
    println("M-1 → MR = ${mem.mRecall()}")
    mem.mClear()
    println("MC → MR = ${mem.mRecall()}")

    println("\nPruebas de errores del evaluador:")
    val bad = listOf("2 + (3 * 4", "log(-1)", "3 / (2-2)")
    for (b in bad) {
        try {
            val r = EvaluadorExpresiones.evaluar(b)
            println("$b = $r")
        } catch (ex: Exception) {
            println("$b → error: ${ex.message}")
        }
    }

    println("\nFin de pruebas.")
}