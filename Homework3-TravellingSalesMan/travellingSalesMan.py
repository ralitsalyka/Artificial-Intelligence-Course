import random
from math import *


def find_distance(dot1, dot2):
    dist = sqrt(pow(dot1[0] - dot2[0], 2) + pow(dot1[1] - dot2[1], 2))
    return dist


def route_len(lst_of_dots):
    length = sum(find_distance(lst_of_dots[i], lst_of_dots[i + 1]) for i in range(0, len(lst_of_dots) - 1))
    return length


def generate_random_coordinates(n):
    list_of_coordinates = []
    count = n
    while count > 0:
        x = random.randint(0, n - 1)
        y = random.randint(0, n - 1)
        if (x, y) not in list_of_coordinates:
            list_of_coordinates.append((x, y))
            count = count - 1
    return list_of_coordinates


def exists(individual, population):
    for item in population:
        if item == individual:
            return True
    return False


def initial_route_create(n):
    route = generate_random_coordinates(n)
    return route


def create_diferent_variants_from_initial_route(n, initial_route):
    list_of_variants = []
    i = 0
    while i < n:
        new_individ = initial_route[:]
        random.shuffle(new_individ)
        if not exists(new_individ, list_of_variants):
            list_of_variants.append(new_individ)
            i += 1
        else:
            pass
    return list_of_variants


def create_childrens(first_part_of_parent, parent2, number_of_genes):
    child = first_part_of_parent
    for dot in parent2:
        if dot not in child:
            child.append(dot)
    return child


def crossover(parent1, parent2, n):
    list_of_childrens = []
    len_of_part_of_parent = 0
    if n % 2 == 0:
        len_of_part_of_parent = int(n / 2)
    else:
        len_of_part_of_parent = int(n / 2) + 1
    first_part1 = [parent1[i] for i in range(len_of_part_of_parent)]
    first_part2 = [parent2[i] for i in range(len_of_part_of_parent)]
    child1 = create_childrens(first_part1, parent2, len_of_part_of_parent)
    child2 = create_childrens(first_part2, parent1, len_of_part_of_parent)
    list_of_childrens.append(child1)
    list_of_childrens.append(child2)
    return list_of_childrens


def reproduce(population, n):
    children_reproduced = []
    i = 0
    while i < len(population) - 1:
        childrens = crossover(population[i], population[i + 1], n)
        children_reproduced.append(childrens[0])
        children_reproduced.append(childrens[1])
        i += 2
    return children_reproduced


def mutation(individual):
    firstIndex = random.randint(0, len(individual) - 1)
    secondIndex = random.randint(0, len(individual) - 1)
    while secondIndex == firstIndex:
        secondIndex = random.randint(0, len(individual) - 1)
    temp = individual[firstIndex]
    individual[firstIndex] = individual[secondIndex]
    individual[secondIndex] = temp
    return individual


def create_new_population(old_population, children_population):
    new_population = []
    for elem in old_population:
        new_population.append(elem)
    for elem in children_population:
        new_population.append(elem)
    return new_population


def find_index_of_element_in_list(elem, used_list):
    for i in range(0, len(used_list)):
        if elem is used_list[i]:
            return i


def find_best_route(population, n):
    list_of_best_results = []
    saved_part_of_old_generation = 0
    if n % 2 == 0:
        saved_part_of_old_generation = int(n / 4)
    else:
        saved_part_of_old_generation = int(n / 4 + 1)

    old_population = population[:saved_part_of_old_generation]
    best_from_population = population[0]
    best_distance = route_len(best_from_population)
    iteration = 0
    while iteration < 1000:
        next_generation = reproduce(population, n)
        new_population = create_new_population(old_population, next_generation)
        new_population.sort(key=lambda x: route_len(x))

        element = random.choice(new_population)
        index = find_index_of_element_in_list(element, new_population)
        new_mutated_element = mutation(element)
        new_population[index] = new_mutated_element[:]

        next_best_individual = new_population[0]
        next_best_distance = route_len(next_best_individual)

        population = next_generation
        best_from_population = next_best_individual
        best_distance = next_best_distance
        iteration += 1

        create_output_of_generations(iteration, best_distance, list_of_best_results)

    final_best_distance = min(list_of_best_results)
    return final_best_distance


def create_output_of_generations(count, best_distance, list_of_best_results):
    if count == 10:
        print('Best of 10 generation:')
        print(best_distance)
        list_of_best_results.append(best_distance)
    elif count == 20:
        print('---------')
        print('Best of 20 generation:')
        print(best_distance)
        list_of_best_results.append(best_distance)
    elif count == 30:
        print('---------')
        print('Best of 30 generation:')
        print(best_distance)
        list_of_best_results.append(best_distance)
    elif count == 40:
        print('---------')
        print('Best of 40 generation:')
        print(best_distance)
        list_of_best_results.append(best_distance)
    return list_of_best_results


if __name__ == '__main__':
    num = int(input("Input number of dots: "))
    initial_route = initial_route_create(num)
    list_of_new_shuffled = create_diferent_variants_from_initial_route(num, initial_route)
    list_of_new_shuffled.sort(key=lambda x: route_len(x))
    r = crossover(list_of_new_shuffled[0], list_of_new_shuffled[1], num)
    best_route = find_best_route(list_of_new_shuffled, num)
    print('           ')
    print('Best route:')
    print(best_route)
