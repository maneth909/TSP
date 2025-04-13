import math
import time
import random

# Calculate distance between two points
def calculate_distance(p1, p2):
    return math.dist(p1, p2)

# Find the closest unvisited city
def find_nearest_neighbor(current_index, points, visited):
    nearest = None
    min_distance = float('inf')
    for i in range(len(points)):
        if i not in visited:
            dist = calculate_distance(points[current_index], points[i])
            if dist < min_distance:
                nearest = i
                min_distance = dist
    return nearest

# Greedy TSP algorithm
def greedy_tsp(city_points, start_city="A"):
    # Mapping city names to indices
    city_names = list(city_points.keys())
    points = list(city_points.values())  # Coordinates only, used internally
    
    # Get the index of the start city
    start_index = city_names.index(start_city)
    
    path = [start_index]
    visited = set(path)
    current = start_index

    while len(visited) < len(points):
        next_city = find_nearest_neighbor(current, points, visited)
        path.append(next_city)
        visited.add(next_city)
        current = next_city

    path.append(start_index)  # Return to starting city
    return path

# Compute total distance of the path
def total_distance(points, path):
    distance = 0
    for i in range(len(path) - 1):
        distance += calculate_distance(points[path[i]], points[path[i + 1]])
    return distance


city_points = {
"A": (0, 0),
"B": (1, 5),
"C": (5, 2),
"D": (6, 6),
"E": (8, 3)
}

# Choose a starting city
start_city = "A"

# Check if the input city is valid
if start_city not in city_points:
    print("Invalid city. Please choose from: A, B, C, D, E.")
else:
    start_time = time.time()
    path = greedy_tsp(city_points, start_city)
    elapsed = time.time() - start_time
    dist = total_distance(list(city_points.values()), path)

# Convert path from indices to city names
named_path = [list(city_points.keys())[i] for i in path]

print(f"Greedy TSP Path: {' → '.join(named_path)}")
print(f"Total Distance: {dist:.2f}")
print(f"Time Taken: {elapsed:.6f} seconds")