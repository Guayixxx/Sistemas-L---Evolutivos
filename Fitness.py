# Fitness.py

def apply_rules(axiom, rules, iterations, max_length=10000):
    for _ in range(iterations):
        next_axiom = "".join([rules.get(ch, ch) for ch in axiom])
        if len(next_axiom) > max_length:
            break  # Detener si la longitud del string excede el máximo permitido
        axiom = next_axiom
    return axiom

def fitness(rule):
    """
    Calcula el fitness de una regla considerando:
    - Balance de corchetes: Penalización máxima si están desbalanceados.
    - Complejidad: Longitud de la regla.
    - Simetría: Balance de corchetes.
    - Penalización por secuencias largas de corchetes.
    - Penalización por balance incorrecto entre 'F' y otros símbolos.
    - Penalización por ausencia de 'F' dentro de bloques de corchetes.
    - Penalización por secuencias largas de 'F' consecutivas.
    """
    # Verificar balance de brackets
    brackets_balance = validate_brackets_balance(rule)
    if brackets_balance == float('-inf'):
        return brackets_balance  # Regla inválida, retorna penalización máxima

    complexity = len(rule)  # Longitud de la regla
    symmetry_score = calculate_symmetry(rule)  # Evalúa el balance de corchetes
    penalty_brackets = penalty_for_bracket_sequences(rule)  # Penaliza secuencias largas de `[`
    balance_penalty = penalty_for_symbol_balance(rule)  # Penaliza si 'F' no ocupa el 60%
    penalty_F_in_brackets = validate_F_in_brackets(rule)  # Penaliza si no hay 'F' en bloques de corchetes
    penalty_consecutive_Fs = penalty_for_consecutive_Fs(rule)  # Penaliza 'F' consecutivas largas

    # El fitness combina las métricas
    return (complexity + symmetry_score) - (
        penalty_brackets + balance_penalty + penalty_F_in_brackets + penalty_consecutive_Fs
    )




def calculate_symmetry(rule):
    open_brackets = rule.count('[')
    close_brackets = rule.count(']')
    imbalance = abs(open_brackets - close_brackets)
    return 0 if imbalance == 0 else imbalance * 5  # Penaliza más severamente

def penalty_for_bracket_sequences(rule):
    """
    Penaliza secuencias largas de corchetes consecutivos, incluyendo
    tanto '[' como ']'.
    """
    max_sequence_open = 0
    max_sequence_close = 0
    current_sequence_open = 0
    current_sequence_close = 0

    for char in rule:
        if char == '[':
            current_sequence_open += 1
            current_sequence_close = 0
            max_sequence_open = max(max_sequence_open, current_sequence_open)
        elif char == ']':
            current_sequence_close += 1
            current_sequence_open = 0
            max_sequence_close = max(max_sequence_close, current_sequence_close)
        else:
            current_sequence_open = 0
            current_sequence_close = 0

    # Penalización proporcional a la longitud máxima de secuencias de '[' o ']'
    return (max_sequence_open + max_sequence_close) * 2

def penalty_for_symbol_balance(rule):
    """
    Penaliza si las proporciones de símbolos en la regla no están cerca de:
    - F: 60%
    - [: 10%
    - ]: 10%
    - +: 10%
    - -: 10%
    """
    total_length = len(rule)
    if total_length == 0:
        return float('inf')  # Penalización máxima para reglas vacías

    # Contar los símbolos
    f_count = rule.count('F')
    open_bracket_count = rule.count('[')
    close_bracket_count = rule.count(']')
    plus_count = rule.count('+')
    minus_count = rule.count('-')

    # Ratios reales
    f_ratio = f_count / total_length
    open_bracket_ratio = open_bracket_count / total_length
    close_bracket_ratio = close_bracket_count / total_length
    plus_ratio = plus_count / total_length
    minus_ratio = minus_count / total_length

    # Ratios ideales
    ideal_ratios = {
        'F': 0.4,
        '[': 0.1,
        ']': 0.1,
        '+': 0.2,
        '-': 0.2
    }

    # Penalizar desviaciones de los ratios ideales
    penalty = 0
    penalty += abs(f_ratio - ideal_ratios['F']) * 100
    penalty += abs(open_bracket_ratio - ideal_ratios['[']) * 100
    penalty += abs(close_bracket_ratio - ideal_ratios[']']) * 100
    penalty += abs(plus_ratio - ideal_ratios['+']) * 100
    penalty += abs(minus_ratio - ideal_ratios['-']) * 100

    return penalty

def validate_brackets_balance(rule):
    """
    Verifica si los brackets en la regla están balanceados.
    Penaliza severamente si hay brackets desbalanceados.
    """
    stack = 0  # Contador para balanceo de corchetes
    for char in rule:
        if char == '[':
            stack += 1
        elif char == ']':
            stack -= 1
        # Si en cualquier momento hay más ']' que '[', está desbalanceado
        if stack < 0:
            return float('-inf')  # Penalización máxima para reglas inválidas

    # Penalizar si quedan brackets sin cerrar
    return 0 if stack == 0 else float('-inf')

def validate_F_in_brackets(rule):
    """
    Valida si cada bloque entre corchetes contiene al menos una 'F'.
    Penaliza bloques vacíos o sin 'F'.
    """
    stack = []
    penalty = 0

    for char in rule:
        if char == '[':
            stack.append("")  # Inicia un nuevo bloque dentro del corchete
        elif char == ']':
            if stack:
                block = stack.pop()
                if 'F' not in block:  # Penaliza si el bloque no contiene 'F'
                    penalty += 10
        elif stack:  # Si estamos dentro de un bloque, agregar caracteres
            stack[-1] += char

    # Penalizar cualquier bloque sin cerrar
    penalty += len(stack) * 10
    return penalty

def penalty_for_repeated_directions(rule):
    """
    Penaliza reglas que contienen:
    - Secuencias de '++' o '--'
    - Secuencias de '+-' o '-+'
    """
    penalty = 0
    invalid_sequences = ['++', '--', '+-', '-+']
    for seq in invalid_sequences:
        penalty += rule.count(seq) * 10  # Penalizar cada aparición de estas secuencias
    return penalty


def penalty_for_consecutive_Fs(rule):
    """
    Penaliza reglas con secuencias largas de 'F' consecutivas.
    """
    max_consecutive_Fs = 0
    current_consecutive_Fs = 0

    for char in rule:
        if char == 'F':
            current_consecutive_Fs += 1
            max_consecutive_Fs = max(max_consecutive_Fs, current_consecutive_Fs)
        else:
            current_consecutive_Fs = 0  # Reinicia el contador al encontrar otro símbolo

    # Penalización proporcional al tamaño de la secuencia más larga de 'F'
    return max_consecutive_Fs * 5  # Ajusta el peso de la penalización según lo necesario
