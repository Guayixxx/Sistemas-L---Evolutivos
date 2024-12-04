#Generate_P.py

import random

from Operadores_Geneticos.Flip_bit import *
from Operadores_Geneticos.One_point import *
from Operadores_Geneticos.Tournament import *


def generate_random_rule(length):
    """
    Genera una regla aleatoria de longitud dada.
    No garantiza el balance de corchetes.
    """
    symbols = ['F', '+', '-', '[', ']']
    rule = ''.join(random.choice(symbols) for _ in range(length))
    return rule