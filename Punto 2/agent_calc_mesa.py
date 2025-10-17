from mesa import Agent, Model
from mesa.time import BaseScheduler
import math
import uuid
import re
import os
import sys

class CalcModel(Model):
    def __init__(self):
        self.schedule = BaseScheduler(self)
        self.mailbox = {}
        self.running = True
        if not os.path.exists('trazas'):
            os.makedirs('trazas')
        open('trazas/mailbox_log.txt', 'w', encoding='utf-8').close()

    def add_agent(self, agent):
        self.schedule.add(agent)
        self.mailbox[agent.unique_id] = []

    def send_message(self, to_id, message):
        self.mailbox[to_id].append(message)
        with open('trazas/mailbox_log.txt', 'a', encoding='utf-8') as f:
            f.write(f"SEND -> to:{to_id} from:{message.get('from')} type:{message.get('type')} payload:{message.get('payload')}\n")

    def get_messages(self, agent_id):
        msgs = list(self.mailbox.get(agent_id, []))
        self.mailbox[agent_id] = []
        if msgs:
            with open('trazas/mailbox_log.txt', 'a', encoding='utf-8') as f:
                for m in msgs:
                    f.write(f"RECV -> at:{agent_id} from:{m.get('from')} type:{m.get('type')} payload:{m.get('payload')}\n")
        return msgs

    def step(self):
        self.schedule.step()

class OpAgent(Agent):
    def __init__(self, unique_id, model, op):
        super().__init__(unique_id, model)
        self.op = op

    def compute(self, a, b):
        if self.op == '+':
            return a + b
        if self.op == '-':
            return a - b
        if self.op == '*':
            return a * b
        if self.op == '/':
            if b == 0:
                raise ZeroDivisionError('division por cero')
            return a / b
        if self.op == '^':
            return a ** b
        raise ValueError('operador desconocido')

    def step(self):
        msgs = self.model.get_messages(self.unique_id)
        for m in msgs:
            if m.get('type') == 'compute':
                a = m['payload']['a']
                b = m['payload']['b']
                try:
                    res = self.compute(a, b)
                    resp = {
                        'from': self.unique_id,
                        'to': m['from'],
                        'type': 'result',
                        'payload': {'result': res, 'op_id': m['payload']['op_id']}
                    }
                except Exception as e:
                    resp = {
                        'from': self.unique_id,
                        'to': m['from'],
                        'type': 'error',
                        'payload': {'error': str(e), 'op_id': m['payload']['op_id']}
                    }
                self.model.send_message(m['from'], resp)

class IOAgent(Agent):
    def __init__(self, unique_id, model, expr=None):
        super().__init__(unique_id, model)
        self.expr = expr
        self.postfix = []
        self.stack = []
        self.waiting_op_id = None
        self.postfix_index = 0
        self.status = 'idle'

    def set_expression(self, expr):
        self.expr = expr
        self.postfix = self.infix_to_postfix(expr)
        self.stack = []
        self.postfix_index = 0
        self.waiting_op_id = None
        self.status = 'running'

    def infix_to_postfix(self, expr):
        tokens = re.findall(r'\d+\.\d+|\d+|[\+\-\*\/\^\(\)]', expr.replace(' ', ''))
        prec = {'+':1, '-':1, '*':2, '/':2, '^':3}
        out = []
        ops = []
        for t in tokens:
            if re.match(r'^\d+(\.\d+)?$', t):
                if '.' in t:
                    out.append(float(t))
                else:
                    out.append(int(t))
            elif t == '(':
                ops.append(t)
            elif t == ')':
                while ops and ops[-1] != '(':
                    out.append(ops.pop())
                if ops:
                    ops.pop()
            else:
                while ops and ops[-1] != '(' and ((prec.get(ops[-1],0) > prec.get(t,0)) or (prec.get(ops[-1],0) == prec.get(t,0) and t != '^')):
                    out.append(ops.pop())
                ops.append(t)
        while ops:
            out.append(ops.pop())
        return out

    def send_compute(self, operator, a, b):
        op_map = {'+':'sum','-':'sub','*':'mul','/':'div','^':'pow'}
        target = op_map[operator]
        op_agent_id = target
        op_id = str(uuid.uuid4())
        msg = {
            'from': self.unique_id,
            'to': op_agent_id,
            'type': 'compute',
            'payload': {'a': a, 'b': b, 'op_id': op_id}
        }
        self.waiting_op_id = op_id
        self.model.send_message(op_agent_id, msg)

    def process_result(self, res):
        self.stack.append(res)
        self.waiting_op_id = None

    def step(self):
        msgs = self.model.get_messages(self.unique_id)
        for m in msgs:
            if m.get('type') == 'result':
                if m['payload']['op_id'] == self.waiting_op_id:
                    self.process_result(m['payload']['result'])
            elif m.get('type') == 'error':
                if m['payload']['op_id'] == self.waiting_op_id:
                    with open('trazas/errors.txt', 'a', encoding='utf-8') as f:
                        f.write(f"ERROR -> op_id:{m['payload'].get('op_id')} error:{m['payload'].get('error')}\n")
                    print('Error en operación:', m['payload'].get('error'))
                    self.waiting_op_id = None
                    self.status = 'error'
                    return
        if self.status != 'running':
            return
        if self.postfix and self.postfix_index < len(self.postfix):
            if self.waiting_op_id is not None:
                return
            token = self.postfix[self.postfix_index]
            if isinstance(token, (int, float)):
                self.stack.append(token)
                self.postfix_index += 1
            else:
                if len(self.stack) < 2:
                    with open('trazas/errors.txt', 'a', encoding='utf-8') as f:
                        f.write(f"ERROR -> Stack underflow at index {self.postfix_index} postfix:{self.postfix}\n")
                    print('Error: Stack underflow. Expresión inválida o parser no admite unarios.')
                    self.status = 'error'
                    return
                b = self.stack.pop()
                a = self.stack.pop()
                self.send_compute(token, a, b)
                self.postfix_index += 1
        else:
            if self.postfix:
                if self.waiting_op_id is None:
                    if len(self.stack) == 1:
                        self.status = 'finished'
                        result = self.stack.pop()
                        print('Resultado final:', result)
                        with open('trazas/result.txt', 'w', encoding='utf-8') as f:
                            f.write(f"Resultado final: {result}\n")
                    else:
                        with open('trazas/errors.txt', 'a', encoding='utf-8') as f:
                            f.write(f"ERROR -> Final stack unexpected length:{len(self.stack)} stack:{self.stack}\n")
                        print('Error: resultado final inesperado. Revisa la expresión.')
                        self.status = 'error'
            else:
                self.status = 'idle'

def build_calculator():
    m = CalcModel()
    io = IOAgent('io', m)
    sum_a = OpAgent('sum', m, '+')
    sub_a = OpAgent('sub', m, '-')
    mul_a = OpAgent('mul', m, '*')
    div_a = OpAgent('div', m, '/')
    pow_a = OpAgent('pow', m, '^')
    m.add_agent(io)
    m.add_agent(sum_a)
    m.add_agent(sub_a)
    m.add_agent(mul_a)
    m.add_agent(div_a)
    m.add_agent(pow_a)
    return m, io

if __name__ == '__main__':
    print ("Calculadora basada en agentes")
    model, io = build_calculator()
    try:
        while True:
            expr = input("Escribe una expresión aritmética (ej: 2 + 3 * (4 - 1) ) o 'salir': ").strip()
            if expr.lower() in ('salir', 'exit', 'q'):
                print('Saliendo.')
                sys.exit(0)
            if expr == "":
                print("Expresión vacía. Intenta de nuevo.")
                continue
            if not re.match(r'^[0-9\.\+\-\*\/\^\(\)\s]+$', expr):
                print("Carácteres no permitidos. Usa solo números, operadores + - * / ^ y paréntesis.")
                continue
            io.set_expression(expr)
            steps = 0
            max_steps = 2000
            while io.status == 'running' and steps < max_steps:
                model.step()
                steps += 1
            if io.status == 'finished':
                pass
            elif io.status == 'error':
                print('Hubo un error durante el cálculo. Revisa traza en la carpeta trazas/.')
            else:
                print('No terminó en', steps, 'pasos — revisa posibles errores.')
    except KeyboardInterrupt:
        print("\nInterrumpido por el usuario.")
        sys.exit(0)
