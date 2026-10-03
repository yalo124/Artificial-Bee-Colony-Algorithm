import random
import numpy as np

def objective_function(route, distance_matrix):
    total_distance = 0

    for i in range(len(route)-1):
        current_city = route[i]
        next_city = route[i + 1]
        total_distance += distance_matrix[current_city][next_city]

    last_city = route[len(route) - 1]
    first_city = route[0]
    total_distance += distance_matrix[last_city][first_city]

    return total_distance

def fitness(x):
    if x >= 0:
        return 1 / (1 + x)
    else:
        return 1 + abs(x)

def recreate_neighbor(route):
    new_route = np.copy(route)

    pos1 = random.randint(0, (len(route)-1))
    pos2 = random.randint(0, (len(route)-1))

    while pos1 == pos2:
        pos2 = random.randint(0, (len(route)-1))

    temp = new_route[pos1]
    new_route[pos1] = new_route[pos2]
    new_route[pos2] = temp

    return new_route
        

def abc_algorithm(objective_function, distance_matrix, num_cities, colony_Size, num_iterations):
    best_Solution = None
    best_Fitness = -np.inf
    colony = []
    trial = [0] * colony_Size
    limit = colony_Size * num_cities

    

    for _ in range(colony_Size):
        city_indices = list(range(num_cities))
        random.shuffle(city_indices)
        solution = city_indices
        obj_func = objective_function(solution, distance_matrix)
        fit = fitness(obj_func)
        colony.append((solution, fit))
        
        if fit > best_Fitness:
            best_Solution = solution
            best_Fitness = fit
    #ABC 
    for iterations in range(num_iterations):
        # Employed
        for i in range(colony_Size):
            solution = colony[i][0]
            new_Solution = recreate_neighbor(solution)

            new_obj_func = objective_function(new_Solution, distance_matrix)
            new_fitness = fitness(new_obj_func)

            if new_fitness > colony[i][1]:
                colony[i] = (new_Solution, new_fitness)
                trial[i] = 0
                if new_fitness > best_Fitness:
                    best_Fitness = new_fitness
                    best_Solution = new_Solution
            else :
                trial[i] += 1
      
        max_fit = max(colony[i][1] for i in range (colony_Size))
        probabilities = [0.9 * (colony[i][1] / max_fit) + 0.1 for i in range (colony_Size)]
        # onlooker
        for _ in range(colony_Size):
            r = random.uniform(0,1)
            selected_index = 0
            for i in range (colony_Size) :
                if r < probabilities[i]:
                    selected_index = i
                    
            selected_Solution = colony[selected_index][0]        

            new_Solution = recreate_neighbor(selected_Solution)
            new_obj_func = objective_function(new_Solution, distance_matrix)
            new_fitness = fitness(new_obj_func)

            if new_fitness > colony[selected_index][1]:
                colony[selected_index] = (new_Solution, new_fitness)
                trial[selected_index] = 0
                if new_fitness > best_Fitness:
                    best_Solution = new_Solution
                    best_Fitness = new_fitness
            else:
                trial[selected_index] += 1
        exceeded = []     
        # scout
        for i in range (colony_Size):
            if trial[i] > limit:
                exceeded.append(i)
        if len(exceeded) > 0:
            worst_index = exceeded[0]
            for k in exceeded:
                if colony[k][1] < colony[worst_index][1]:
                    worst_index = k
            new_city_indices = list(range(num_cities))
            random.shuffle(new_city_indices)
            new_solution = new_city_indices
            new_obj_func = objective_function(new_solution, distance_matrix)
            new_fit = fitness(new_obj_func)

            colony[worst_index] = (new_solution, new_fit)
            trial[worst_index] = 0

            if new_fit > best_Fitness:
                best_Solution = new_solution
                best_Fitness = new_fit

        if (iterations + 1) % 5 == 0:
            print(f"Iteration {iterations+1}: Best Fitness = {best_Fitness}")
            print(f"Best Solution = {best_Solution}\n")

    return best_Solution, best_Fitness



cities = [(0,0), (3,4), (1,5), (6,3), (10,5), (4, 9), (14, 34),(13,9),(43,21),(12,43), (76,34),(23,2),(54,67),(89,0), (12,3)]
num_cities = len(cities)
distance_matrix = np.zeros((num_cities, num_cities))

for i in range(num_cities):
    for j in range(num_cities):
            x1, y1 = cities[i]
            x2, y2 = cities[j]
            distance_matrix[i][j] = np.sqrt((x1 - x2)**2 + (y1 - y2)**2)

colony_Size = 50
num_iterations = 100

best_Solution, best_Fitness = abc_algorithm(objective_function, distance_matrix,num_cities, colony_Size, num_iterations)

print("Best solution:", best_Solution)
print("Best Fitness:", best_Fitness)
