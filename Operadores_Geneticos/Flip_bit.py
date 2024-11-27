import random


def flip_bit_mutation(rule, mutation_rate=0.01):
    rule = list(rule)
    for i in range(len(rule)):
        if random.random() < mutation_rate:
            rule[i] = random.choice(['F','G', '+', '-', '[', ']'])
    # Balancear corchetes
    open_brackets = rule.count('[')
    close_brackets = rule.count(']')
    if open_brackets > close_brackets:
        rule += ']' * (open_brackets - close_brackets)
    elif close_brackets > open_brackets:
        rule = ['['] * (close_brackets - open_brackets) + rule
    return ''.join(rule)

