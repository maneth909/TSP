import math
import random
import time

# Initial Population of random paths
# Time Complexity: O(N * D), where N = 20000, D = total destinations
def generate_random_paths(total_destinations):
    random_paths = []
    for _ in range(20000):
        path = list(range(1, total_destinations))  #exclude the starting city
        random.shuffle(path) #shuffle those cities to create a random path
        path = [0] + path #add the starting city back at the beginning
        random_paths.append(path)
    return random_paths

# Calculate total distance between cities of the given path
# Time Complexity: O(N), where N = total destinations
def total_distance(points, path):
    distance = 0
    for i in range(1, len(path)):
        distance += math.dist(points[path[i-1]], points[path[i]]) #sum up distances between cities of the path
    distance += math.dist(points[path[-1]], points[path[0]]) #return to starting city
    return distance

# Reduce the initial population by half, keeping the paths with lower distances
# Time Complexity: O(N * D)
def choose_survivors(points, old_generation):
    survivors = []
    random.shuffle(old_generation) #shuffle the old generation to ensure randomness
    midway = len(old_generation) // 2 
    for i in range(midway):
        old1 = old_generation[i] #define the first half
        old2 = old_generation[midway + i] #define the second half
        if total_distance(points, old1) < total_distance(points, old2):
            survivors.append(old1)
        else:
            survivors.append(old2)
    return survivors

# Create offsprings by applying Order Crossover
# Time Complexity: O(N) 
def create_offspring(parent_a, parent_b):
    off_spring = []
    start = random.randint(0, len(parent_a) - 1)
    finish = random.randint(start, len(parent_a))
    sub_path_from_a = parent_a[start:finish] #select a random sub-path from parent_a
    remaining_path_from_b = [point for point in parent_b if point not in sub_path_from_a] #select remaining points from parent_b tha do not exist in the sub-path from parent_a
    for i in range(len(parent_a)): #append the points one by one in order from both parents
        if start <= i < finish:
            off_spring.append(sub_path_from_a.pop(0))
        else:
            off_spring.append(remaining_path_from_b.pop(0))
    return off_spring

# Apply Crossover to the survivors
# Time Complexity: O(S * N), where S = number of survivors, N = number of points
def apply_crossovers(survivors):
    offsprings = []
    midway = len(survivors) // 2
    for i in range(midway): #splits survivors into two halves and creates offsprings from each pair of parents
        parent_a = survivors[i]
        parent_b = survivors[midway + i]
        for _ in range(2): #Double the survivors 
            offsprings.append(create_offspring(parent_a, parent_b))
            offsprings.append(create_offspring(parent_b, parent_a))
    return offsprings

def apply_mutations(generation):
    gen_wt_mutations = []
    for path in generation:
        if random.randint(0, 1000) < 9: #pick 0.9% of the population to mutate
            # Swap two random cities in the path
            index1, index2 = random.randint(1, len(path) - 1), random.randint(1, len(path) - 1)
            path[index1], path[index2] = path[index2], path[index1]
        gen_wt_mutations.append(path)
    return gen_wt_mutations

# Execute onefull genreation: selection -> crossover -> mutation
def genetic_algorithm(points, old_generation):
    survivors = choose_survivors(points, old_generation)
    crossovers = apply_crossovers(survivors)
    new_population = apply_mutations(crossovers)
    return new_population

# reorder points to make the specified point the sarting point
# Time Complexity: O(N)
def remap_points_and_path(city_points, start_city):
    city_names = list(city_points.keys())
    start_index = city_names.index(start_city)

    # Move the specified point to front
    new_city_names = [city_names[start_index]] + city_names[:start_index] + city_names[start_index+1:]
    new_city_points = {name: city_points[name] for name in new_city_names}
    return list(new_city_points.values()), new_city_names


# ---------- Config ----------
city_points = {
    "A": (2, 3),
    "B": (7, 8),
    "C": (1, 9),
    "D": (4, 2),
    "E": (6, 5),
    "F": (0, 6),
    "G": (9, 1),
    "H": (3, 7),
    "I": (5, 9),
    "J": (8, 4),
    "K": (2, 8),
    "L": (6, 1),
    "M": (4, 6),
    "N": (0, 0),
    "O": (9, 9)
}

start_city = "A" # starting point

# ---------- Prepare ----------
points, city_names = remap_points_and_path(city_points, start_city) # reorder points
old_generation = generate_random_paths(len(points)) #initialize population

# ---------- Runt the operation 100 times ----------
start_time = time.time()
generations = 100
current_gen = old_generation
for _ in range(generations):
    current_gen = genetic_algorithm(points, current_gen)
end_time = time.time()

# ---------- Result ----------
best_path = min(current_gen, key=lambda path: total_distance(points, path))
named_best_path = [city_names[i] for i in best_path]
print("Best Path:", " → ".join(named_best_path))
print("Shortest Distance:", total_distance(points, best_path))
print(f"Time taken: {end_time - start_time:.4f} seconds")
