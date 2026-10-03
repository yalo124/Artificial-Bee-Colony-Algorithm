import random
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation

def objective_function(x):
    return sum(x**2)

def fitness(x):
    if x >= 0:
        return 1 / (1 + x)
    else:
        return 1 + abs(x)

def abc_algorithm(objective_function, num_Variables, colony_Size, num_iterations, LB, UB):
    best_Solution = None
    best_Fitness = -np.inf
    colony = []
    trial = [0] * colony_Size
    limit = colony_Size * num_Variables
    history = []
    trial_history = []
    positions_history = []

    for _ in range(colony_Size):
        solution = np.random.uniform(LB, UB, num_Variables)
        obj_func = objective_function(solution)
        fit = fitness(obj_func)
        colony.append((solution, fit))
        if fit > best_Fitness:
            best_Solution = solution
            best_Fitness = fit

    positions_history.append([c[0].copy() for c in colony])

    for iterations in range(num_iterations):
        for i in range(colony_Size):
            solution = colony[i][0]
            while True:
                j = random.randint(0, colony_Size - 1)
                if j != i:
                    break
            new_Solution = solution.copy()
            k = random.randint(0, num_Variables - 1)
            phi = random.uniform(-1, 1)
            new_Solution[k] = solution[k] + phi * (solution[k] - colony[j][0][k])
            new_Solution = np.clip(new_Solution, LB, UB)
            new_obj_func = objective_function(new_Solution)
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
        for _ in range(colony_Size):
            r = random.uniform(0, 1)
            selected_index = 0
            for i in range(colony_Size):
                if r < probabilities[i]:
                    selected_index = i
            selected_Solution = colony[selected_index][0]
            new_Solution = selected_Solution.copy()
            k = random.randint(0, num_Variables - 1)
            phi = random.uniform(-1, 1)
            while True:
                j = random.randint(0, colony_Size - 1)
                if j != selected_index:
                    break
            new_Solution[k] = selected_Solution[k] + phi * (selected_Solution[k] - colony[j][0][k])
            new_Solution = np.clip(new_Solution, LB, UB)
            new_obj_func = objective_function(new_Solution)
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
        for i in range(colony_Size):
            if trial[i] > limit:
                exceeded.append(i)
        if len(exceeded) > 0:
            worst_index = exceeded[0]
            for k in exceeded:
                if colony[k][1] < colony[worst_index][1]:
                    worst_index = k
            new_Solution = np.random.uniform(LB, UB, num_Variables)
            new_obj_func = objective_function(new_Solution)
            new_fit = fitness(new_obj_func)
            colony[worst_index] = (new_Solution, new_fit)
            trial[worst_index] = 0
            if new_fit > best_Fitness:
                best_Solution = new_Solution
                best_Fitness = new_fit

        print(f"Iteration {iterations+1}: Best Fitness = {best_Fitness}")
        print(f"Best Solution = {best_Solution}\n")

        history.append(best_Fitness)
        trial_history.append(trial.copy())
        positions_history.append([c[0].copy() for c in colony])

    return best_Solution, best_Fitness, trial, history, trial_history, positions_history


random.seed(7)
np.random.seed(7)

colony_Size = 50
num_Variables = 2
num_iterations = 80
LB = -5.0
UB = 5.0

best_Solution, best_Fitness, trial, history, trial_history, positions_history = abc_algorithm(
    objective_function, num_Variables, colony_Size, num_iterations, LB, UB
)

print("\n=====Artificial Bee Colony: Final Result=====\n")
print("Best solution:", best_Solution)
print("Best fitness:", best_Fitness)

grid = np.linspace(LB, UB, 200)
X, Y = np.meshgrid(grid, grid)
Z = X**2 + Y**2

fig, ax = plt.subplots(figsize=(7, 7))
ax.contourf(X, Y, Z, levels=30, cmap='viridis')  

colors = plt.cm.hsv(np.linspace(0, 1, colony_Size, endpoint=False))

scat = ax.scatter(np.array(positions_history[0])[:,0], np.array(positions_history[0])[:,1], c=colors, edgecolors='black', linewidths=0.5, s=50, zorder=5)
title = ax.set_title("")
ax.set_xlabel("x1")
ax.set_ylabel("x2")
ax.set_xlim(LB, UB)
ax.set_ylim(LB, UB)
ax.set_xticks(np.arange(LB, UB+1, 1))
ax.set_yticks(np.arange(LB, UB+1, 1))


def update(frame):
    pts = np.array(positions_history[frame])
    scat.set_offsets(pts)
    title.set_text(f"Artificial Bee Colony — Iteration {frame}/{num_iterations}")
    return scat, title

ani = animation.FuncAnimation(fig, update, frames=len(positions_history), interval=150, blit=False, repeat=True)
plt.show()
