from mesa import Agent, Model
from mesa.time import BaseScheduler
import math
import uuid
import re

class CalcModel(Model):
    def __init__(self):
        self.schedule = BaseScheduler(self)
        self.mailbox = {}
        self.running = True

    def add_agent(self, agent):
        self.schedule.add(agent)
        self.mailbox[agent.unique_id] = []

    def send_message(self, to_id, message):
        self.mailbox[to_id].append(message)

    def get_messages(self, agent_id):
        msgs = list(self.mailbox.get(agent_id, []))
        self.mailbox[agent_id] = []
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
            return a / b
        if self.op == '^':
            return a ** b
        return None

    def step(self):
        msgs = self.model.get_messages(self.unique_id)
        for m in msgs:
            if m['type'] == 'compute':
                a = m['payload']['a']
                b = m['payload']['b']
                res = self.compute(a, b)
                resp = {
                    'from': self.unique_id,
                    'to': m['from'],
                    'type': 'result',
                    'payload': {'result': res, 'op_id': m['payload']['op_id']}
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
        self.finished = False

    def set_expression(self, expr):
        self.expr = expr
        self.postfix = self.infix_to_postfix(expr)
        self.stack = []
        self.postfix_index = 0
        self.waiting_op_id = None
        self.finished = False

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
            if m['type'] == 'result':
                if m['payload']['op_id'] == self.waiting_op_id:
                    self.process_result(m['payload']['result'])
        if self.finished:
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
                    raise Exception('Stack underflow')
                b = self.stack.pop()
                a = self.stack.pop()
                self.send_compute(token, a, b)
                self.postfix_index += 1
        else:
            if self.postfix:
                if self.waiting_op_id is None:
                    if len(self.stack) == 1:
                        self.finished = True
                        result = self.stack.pop()
                        print('Resultado final:', result)
            else:
                pass

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
    model, io = build_calculator()
    io.set_expression("2 + 3 * 4 - 5 ^ 2 / 5")
    steps = 0
    while not io.finished and steps < 200:
        model.step()
        steps += 1
    if io.finished:
        pass
    else:
        print('No terminó en', steps, 'pasos')
