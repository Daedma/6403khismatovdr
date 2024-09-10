import math
import re

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

def calc_in_range(func, lower, upper, step):
    values = list()
    x = float(lower)
    while x <= upper:
        values.append(func(x))
        x += step
    return values

params = load_params("config")
y = create_y(params['a'], params['b'], params['c'])
values = calc_in_range(y, params['n0'], params['nk'], params['h'])
with open("result", 'w') as file:
    file.write(str(values))
