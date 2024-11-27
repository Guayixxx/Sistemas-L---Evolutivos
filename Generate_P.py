import random

from Operadores_Geneticos.Flip_bit import *
from Operadores_Geneticos.One_point import *
from Operadores_Geneticos.Tournament import *


def generate_random_rule(length):
    symbols = ['F','G', '+', '-', '[', ']']
    rule = ""
    bracket_count = 0
    for _ in range(length):
        symbol = random.choice(symbols)
        if symbol == '[':
            bracket_count += 1
        elif symbol == ']' and bracket_count > 0:
            bracket_count -= 1
        rule += symbol
    # Balancear corchetes
    rule += ']' * bracket_count
    return rule