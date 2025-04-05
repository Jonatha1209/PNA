import re
import json
import os
import random
import time

class BreakSignal(Exception):
    pass

class ContinueSignal(Exception):
    pass


class Interprinter:
    def __init__(self):
        self.variables = {}
        self.builtin = {
            'upper': lambda x: str(x).upper(),
            'lower': lambda x: str(x).lower(),
            'len': lambda x: len(x),
            'int': lambda x: int(x),
            'str': lambda x: str(x),
            'bool': lambda x: bool(x),
            'not': lambda x: not x,
            'random': lambda a, b: random.randint(a, b),
            'randint': lambda a, b: random.randint(a, b),
            'sleep': lambda sec: time.sleep(float(sec)),
            'inlist': lambda val, csv: str(val) in csv.split(','),
            'contains': lambda s, sub: sub in s,
            'startswith': lambda s, prefix: s.startswith(prefix),
            'endswith': lambda s, suffix: s.endswith(suffix),
            'choice': lambda *args: random.choice(args),
            'capitalize': lambda s: str(s).capitalize(),
            'slice': lambda s, a, b: str(s)[int(a):int(b)],
        }

    def read(self, filename):
        if not filename.endswith(".pna"):
            raise ValueError("Only .pna files are supported.")
        if not os.path.exists(filename):
            raise FileNotFoundError(f"{filename} not found.")
        with open(filename, 'r', encoding='utf-8') as f:
            code = f.read()
        self.execute(code)

    def eval_expr(self, expr: str):
        expr = expr.strip()
        parts = expr.split()
        if parts[0] in self.builtin:
            func = self.builtin[parts[0]]
            args = [self.eval_expr(p) if p not in ['true', 'false'] else (p == 'true') for p in parts[1:]]
            return func(*args)
        
        for var in self.variables:
            for key in self.variables[var]:
                full_key = f"{var}.{key}"
                if full_key in expr:
                    val = self.variables[var][key]
                    if isinstance(val, str):
                        val = f'"{val}"'
                    expr = expr.replace(full_key, str(val))
        
        return eval(expr, {"__builtins__": {}}, self.builtin)

    def write(self, filename):
        with open(filename, 'w', encoding='utf-8') as f:
            for key, value in self.variables.items():
                f.write(f"{key}: {json.dumps(value)}\n")

    def execute(self, code):
        if isinstance(code, str):
            lines = [line.strip() for line in code.strip().split('\n') if line.strip()]
        else:
            lines = code
        i = 0
        while i < len(lines):
            line = lines[i]
            if re.match(r'^\w+:\s*{$', line):
                var = line.split(':')[0]
                obj = {}
                i += 1
                while not lines[i].startswith('}'):
                    key, val = lines[i].split(':')
                    key = key.strip()
                    val = val.strip().rstrip(',')
                    
                    try:
                        val = self.eval_expr(val)
                    except Exception as e:
                        print(f"[ObjectParseError] {e}")
                    
                    obj[key] = val
                    i += 1
                self.variables[var] = obj
            elif re.match(r'^\w+\.\w+\s*:', line):
                var_prop, val = line.split(':', 1)
                var, prop = var_prop.strip().split('.')
                val = val.strip().rstrip(',')
                try:
                    result = self.eval_expr(val)
                    self.variables[var][prop] = result
                except Exception as e:
                    print(f"[AssignError] {e}")

            elif line.startswith("log "):
                expr = line[4:].strip()
                try:
                    res = self.eval_expr(expr)
                    print(res)
                except Exception as e:
                    print(f"[LogError] {e}")
            elif line.startswith("cond"):
                match = re.match(r'cond\s*\((.*?)\)\s*->\s*{', line)
                if not match:
                    print(f"[error] Invalid cond syntax: {line}")
                    i += 1
                    continue
                condition = match.group(1)
                should_run = False
                try:
                    should_run = self.eval_expr(condition)
                except Exception as e:
                    print(f"[Conderror] {e}")
                block = []
                i += 1
                while i < len(lines) and lines[i] != "end":
                    block.append(lines[i])
                    i += 1
                if should_run:
                    self.execute(block)
            elif line.startswith("input "):
                match = re.match(r'input\s+"(.*?)"\s*->\s*(\w+)(?:\.(\w+))?', line)
                if match:
                    prompt = match.group(1)
                    var = match.group(2)
                    prop = match.group(3)
                    
                    if prompt == "NO":
                        user_input = input()
                    else:
                        user_input = input(prompt + " ")

                    if re.match(r'^-?\d+$', user_input):
                        user_input = int(user_input)
                    elif re.match(r'^-?\d+\.\d+$', user_input):
                        user_input = float(user_input)

                    if prop:
                        if var not in self.variables:
                            self.variables[var] = {}
                        self.variables[var][prop] = user_input
                    else:
                        self.variables[var] = user_input
                else:
                    print(f"[InputError] Invalid input syntax: {line}")
            
            elif line.startswith("loop"):
                match = re.match(r'loop\s*\((.*?)\)\s*->\s*{', line)
                if not match:
                    print(f"[error] Invalid loop syntax: {line}")
                    i += 1
                    continue
                cond_expr = match.group(1)
                block = []
                i += 1
                while i < len(lines) and lines[i] != "end":
                    block.append(lines[i])
                    i += 1
                try:
                    while self.eval_expr(cond_expr):
                        try:
                            self.execute(block)
                        except ContinueSignal:
                            continue
                        except BreakSignal:
                            break
                except Exception as e:
                    print(f"[LoopError] {e}")


            elif line.strip() == "break":
                raise BreakSignal()
            elif line.strip() == "continue":
                raise ContinueSignal()
            i += 1
