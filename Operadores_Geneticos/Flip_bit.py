# Flip_bit.py

import random

def flip_bit_mutation(rule, mutation_rate=0.01):
    rule = list(rule)  # Convierte la regla en una lista para permitir cambios
    for i in range(len(rule)):
        if random.random() < mutation_rate:
            rule[i] = random.choice(['F', '+', '-', '[', ']'])  # Cambia el símbolo
    return ''.join(rule)  # Convierte de nuevo a string
