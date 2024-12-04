# Tournament.py

import random

from Fitness import *

def tournament_selection(population, fitness_scores, k=3):
    selected = random.sample(list(zip(population, fitness_scores)), k)
    selected = sorted(selected, key=lambda x: x[1], reverse=True)
    return selected[0][0]

