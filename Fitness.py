def apply_rules(axiom, rules, iterations, max_length=10000):
    for _ in range(iterations):
        next_axiom = "".join([rules.get(ch, ch) for ch in axiom])
        if len(next_axiom) > max_length:
            break  # Detener si la longitud del string excede el máximo permitido
        axiom = next_axiom
    return axiom

def fitness(rule):
    complexity = len(rule)
    symmetry_score = calculate_symmetry(rule)  # Función personalizada para evaluar la simetría
    diversity = diversity_score(rule)  # Evalúa la diversidad de símbolos
    return (complexity + symmetry_score + diversity) / 3

def calculate_symmetry(rule):
    # Implementa una lógica para calcular la simetría
    open_brackets = rule.count('[')
    close_brackets = rule.count('[')
    return 0.5 if open_brackets == close_brackets else 2.5  # Simplificada para este ejemplo

def diversity_score(rule):
    # Logica para calcular la proporcion de simbolos
    possible_symbols = {'F', 'G', '+', '-', '[', ']'}
    unique_symbols = set(rule)  # Obtiene los símbolos únicos en la regla
    diversity = len(unique_symbols & possible_symbols) / len(possible_symbols)
    return diversity  # Retorna un valor entre 0 y 1
