import math
import re
import sys
from typing import Callable

def create_y(a:float, b:float, c:float) -> float:
    return lambda x : a * (math.sin(b * x) - (math.cos(c * x))**2)

def load_params(filename:str):
    params = dict()
    content = open(filename, 'r').read()
    pattern = re.compile(r'(?:"([^"]+)"\s*:\s*([^"]*?)\s*)[,\s]')
    fields = re.findall(pattern, content)
    for field in fields:
        params[field[0]] = float(field[1])
    return params

def calc_in_range(func:Callable, lower:float, upper:float, step:float):
    values = list()
    x = float(lower)
    while x <= upper:
        values.append(func(x))
        x += step
    return values

params = dict()
if len(sys.argv) > 1:
    params['n0'] = float(sys.argv[1])
    params['h'] = float(sys.argv[2])
    params['nk'] = float(sys.argv[3])
    params['a'] = float(sys.argv[4])
    params['b'] = float(sys.argv[5])
    params['c'] = float(sys.argv[6])
else:
    params = load_params("config")
y = create_y(params['a'], params['b'], params['c'])
values = calc_in_range(y, params['n0'], params['nk'], params['h'])
with open("result", 'w') as file:
    file.write(str(values))
