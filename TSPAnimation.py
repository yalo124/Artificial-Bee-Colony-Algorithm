import random
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation

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
    best_route_history = []  

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

    best_route_history.append(list(best_Solution))   

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
            else:
                trial[i] += 1

        max_fit = max(colony[i][1] for i in range(colony_Size))
        probabilities = [0.9 * (colony[i][1] / max_fit) + 0.1 for i in range(colony_Size)]
        # onlooker
        for _ in range(colony_Size):
            r = random.uniform(0,1)
            selected_index = 0
            for i in range(colony_Size):
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
        for i in range(colony_Size):
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

        best_route_history.append(list(best_Solution))   

    return best_Solution, best_Fitness, best_route_history

random.seed(3)
np.random.seed(3)

cities = [(9,24),(2,18),(14,6),(6,27),(1,12),(11,30),(4,8),(15,20),(7,3),(3,25),(12,14),(8,22),(5,10),(13,4),(10,16)]
num_cities = len(cities)
distance_matrix = np.zeros((num_cities, num_cities))
for i in range(num_cities):
    for j in range(num_cities):
        x1, y1 = cities[i]
        x2, y2 = cities[j]
        distance_matrix[i][j] = np.sqrt((x1 - x2)**2 + (y1 - y2)**2)

colony_Size = 50
num_iterations = 100

best_Solution, best_Fitness, best_route_history = abc_algorithm(
    objective_function, distance_matrix, num_cities, colony_Size, num_iterations
)

print("Best solution:", best_Solution)
print("Best Fitness:", best_Fitness)
print("Frames recorded:", len(best_route_history))

# --- Animation ---
fig, ax = plt.subplots(figsize=(7, 7))
xs_all = [c[0] for c in cities]
ys_all = [c[1] for c in cities]

ax.scatter(xs_all, ys_all, c='red', zorder=5, s=60)
for idx, (x, y) in enumerate(cities):
    ax.annotate(str(idx), (x, y), textcoords="offset points", xytext=(6,6))

line, = ax.plot([], [], 'b-o', markersize=4, zorder=3)
title = ax.set_title("")
ax.set_xlabel("X")
ax.set_ylabel("Y")
margin = 5
ax.set_xlim(min(xs_all)-margin, max(xs_all)+margin)
ax.set_ylim(min(ys_all)-margin, max(ys_all)+margin)
ax.set_xticks(np.arange(min(xs_all)-margin, max(xs_all)+margin, 1))
ax.set_yticks(np.arange(min(ys_all)-margin, max(ys_all)+margin, + 1))
ax.grid(True)

def update(frame):
    route = best_route_history[frame]
    xs = [cities[i][0] for i in route] + [cities[route[0]][0]]
    ys = [cities[i][1] for i in route] + [cities[route[0]][1]]
    line.set_data(xs, ys)
    dist = objective_function(route, distance_matrix)
    title.set_text(f"TSP — Artificial Bee Colony — Iteration {frame}/{num_iterations}  (distance={dist:.1f})")
    return line, title

ani = animation.FuncAnimation(fig, update, frames=len(best_route_history), interval=150, blit=False, repeat=False)
plt.show();