import turtle

from Fitness import *
from Operadores_Geneticos.Flip_bit import *
from Generate_P import *
from Operadores_Geneticos.One_point import *
from Operadores_Geneticos.Tournament import *

# Definición de los parámetros
angle = 22.5
iterations = 3
population_size = 100
generations = 50
mutation_rate = 0.01
rule_length = 20


# Función para dibujar el sistema L usando turtle
def draw_lsystem(t, instructions, angle, distance):
    stack = []
    for command in instructions:
        if command == 'F':
            t.forward(distance)
        elif command == '+':
            t.right(angle)
        elif command == '-':
            t.left(angle)
        elif command == '[':
            stack.append((t.heading(), t.pos()))
        elif command == ']':
            heading, position = stack.pop()
            t.penup()
            t.setheading(heading)
            t.goto(position)
            t.pendown()

# Generar población inicial
population = [generate_random_rule(rule_length) for _ in range(population_size)]

# Proceso evolutivo
for generation in range(generations):
    # Evaluar fitness
    fitness_scores = [fitness(rule) for rule in population]
    
    # Selección y reproducción
    next_population = []
    for _ in range(population_size // 2):
        parent1 = tournament_selection(population, fitness_scores)
        parent2 = tournament_selection(population, fitness_scores)
        child1, child2 = one_point_crossover(parent1, parent2)
        child1 = flip_bit_mutation(child1, mutation_rate)
        child2 = flip_bit_mutation(child2, mutation_rate)
        next_population.extend([child1, child2])
    population = next_population
    
    # Mostrar mejor individuo de la generación actual
    best_individual = population[fitness_scores.index(max(fitness_scores))]
    print(f"Generación {generation + 1}: {best_individual}")

    # Dibujar el mejor resultado cada 10 generaciones
    if (generation + 1) % 10 == 0:
        axiom = "F"  # Axioma inicial
        rules = {"F": best_individual}  # Usa la mejor regla como la producción de F
        lsystem_string = apply_rules(axiom, rules, iterations)

        # Configurar turtle
        t = turtle.Turtle()
        wn = turtle.Screen()
        wn.setup(width=800, height=800)
        wn.title(f"Generación {generation + 1}: Mejor Resultado")
        t.speed(0)
        t.penup()
        t.goto(0, -300)
        t.pendown()
        t.left(90)

        # Dibujar el sistema L
        draw_lsystem(t, lsystem_string, angle, distance=5)

        # Pausar hasta que el usuario cierre la ventana
        turtle.done()