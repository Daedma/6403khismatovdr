import math
import re
import sys
from typing import Callable


def create_y(a: float, b: float, c: float) -> float:
    """
    Создает функцию, которая вычисляет значение y в зависимости от значения x.

    Функция принимает три параметра a, b и c и возвращает анонимную функцию, которая вычисляет значение y по формуле:
    y = a * (sin(b * x) - (cos(c * x)) ** 2)

    Args:
        a (float): Коэффициент a в формуле.
        b (float): Коэффициент b в формуле.
        c (float): Коэффициент c в формуле.

    Returns:
        float: Значение y, вычисленное по формуле.
    """
    return lambda x: a * (math.sin(b * x) - (math.cos(c * x)) ** 2)


def load_params(filename: str) -> dict:
	"""
    Загружает параметры из файла.

    Файл должен содержать пары ключ-значение в формате "ключ": значение, разделенные запятыми или пробелами.
    Функция читает файл, извлекает пары ключ-значение с помощью регулярного выражения и возвращает словарь, содержащий параметры.

    Args:
        filename (str): Путь к файлу, содержащему параметры.

    Returns:
        dict: Словарь, содержащий параметры.
    """
    params = dict()
    content = open(filename, "r").read()
    pattern = re.compile(r'(?:"([^"]+)"\s*:\s*([^"]*?)\s*)[,\s]')
    fields = re.findall(pattern, content)
    for field in fields:
        params[field[0]] = float(field[1])
    return params


def calc_in_range(func: Callable, lower: float, upper: float, step: float) -> list:
	"""
    Вычисляет значения функции в заданном диапазоне.

    Функция принимает вызываемую функцию, нижнюю границу, верхнюю границу и размер шага. Она вычисляет значения функции
    для каждого значения в диапазоне от нижней границы до верхней границы (включительно) с заданным размером шага.
    Значения функции возвращаются в виде списка.

    Args:
        func (Callable): Функция, для которой необходимо вычислить значения.
        lower (float): Нижняя граница диапазона.
        upper (float): Верхняя граница диапазона.
        step (float): Размер шага между значениями в диапазоне.

    Returns:
        list: Список, содержащий значения функции в заданном диапазоне.
    """
    values = list()
    x = float(lower)
    while x <= upper:
        values.append(func(x))
        x += step
    return values


params = dict()
if len(sys.argv) > 1:
    params["n0"] = float(sys.argv[1])
    params["h"] = float(sys.argv[2])
    params["nk"] = float(sys.argv[3])
    params["a"] = float(sys.argv[4])
    params["b"] = float(sys.argv[5])
    params["c"] = float(sys.argv[6])
else:
    params = load_params("config")
y = create_y(params["a"], params["b"], params["c"])
values = calc_in_range(y, params["n0"], params["nk"], params["h"])
with open("result", "w") as file:
    file.write(str(values))
