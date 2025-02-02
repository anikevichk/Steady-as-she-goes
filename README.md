# Documentation for project 'Steady as she goes!'

**Author:** Katsyaryna Anikevich  
**Group:** 105, PIPR23Z

## Project Objective:
Create a GUI program to optimize ship routes in shallow water areas.

## Project Description:
The project is a graphical program that visualizes and optimizes the shortest route of a vessel in shallow water areas, considering the depth of the terrain and the draft of the vessel.

By specifying the map parameters and the draft of his vessel, the user creates a map of size NxN through the interface, or the program creates it itself.

The program, using the shortest path algorithm, takes into account the depth of the terrain and the draft of the vessel. The result is a visualized shortest path from the top left corner of the map to the bottom right corner, providing the captain with a clear idea of the optimal route.

The program interface is implemented using the NumPy library for data processing and Matplotlib for map visualization.

## Classes

### Class `Map`
The `Map` class represents a two-dimensional map with given dimensions (`map_size`) and a given draught value. The map is initialized with random values, manually inputted parameters, or parameters read from a file based on a predefined probability distribution. The class provides methods for visualizing the map (`plot_map`), checking cell validity (`is_valid_cell`), and getting valid neighboring cells with their matching values (`get_neighbors`). Additionally, the class includes checks for input parameters (`map_size` and `draught`) during initialization.

### Class `Path`
The `Path` class represents a path-finding algorithm applied to a given map object. The class is initialized with a map object (`map_obj`) and a map size (`map_size`). It includes a method (`find_paths`) that uses a breadth-first search algorithm to find two minimum length paths from the top left corner to the bottom right corner of the map. The path is then regenerated and stored in the `path_matrix` attribute. The class also provides a method (`visualize_path`) to visualize the map along with the discovered path.

## User Guide

### Installation

Ensure that you have Python installed on your system. The project relies on the following libraries, which can be installed using the following command:

```bash
pip install numpy
pip install matplotlib
```

### Usage

1. **Start the program:**
    Open your Python environment and run the script "main.py".

2. **Enter map creation method, size, and draught:**
    - Enter the map creation method (manual, automatic, or reading from a file).
    - Enter the desired field size (`map_size`), and the ship's draught in meters when prompted or the path to the file (depending on the chosen creation method).
    - If you choose to create manually, enter values.

3. **Visualization:**
    - The program will generate a map based on the specified size and draft.
    - The map will be displayed using Matplotlib.

4. **Shortest Path Calculation:**
    - The program will calculate two minimum length paths using the BFS algorithm.
    - The specified path will be visualized on the map.

5. **View the result:**
    - Explore the displayed map to find the optimal paths from the top left corner to the bottom right corner.

## Reflexive Part 

### Unachieved Goals:
#### Display a path at a specific time interval

While writing the code, I was not able to achieve displaying a path after a certain time interval. However, I made it possible for the path to appear after the window is closed (or a notification appears that there is no valid path). To my knowledge, there is no such function in the Matplotlib library that would solve this problem.

#### Obstacles:
#### Writing a pathfinding algorithm
An unforeseen problem for me was writing a pathfinding algorithm. In the early version of the code, only one path was searched for (without searching through all possible paths), which often resulted in a highlighted message that there was no valid path, even though there was one. After reading the literature, I had to choose between Dijkstra, A*, breadth, and depth search algorithms.

#### Changes:
#### Pathfinding Algorithm
Initially, I wanted to use Dijkstra's algorithm, but I used the breadth-first search algorithm because edges have no weight, and it is more rational to use the breadth-first search algorithm. Also, I initially planned only for random mapping but later added the options to read from a file and input manually.
