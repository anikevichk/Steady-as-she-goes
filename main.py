import numpy as np
import matplotlib.pyplot as plt
import matplotlib.colors as mcolors
from matplotlib.widgets import Button
from collections import deque

class Map:
    def __init__(self, n, draught):
        self.n = n
        if n <= 0 or type(n) != int:
            raise TypeError('N should be a positive number')
        self.draught = draught
        if draught <= 0 or type(draught) != float:
            raise TypeError('Draught should be a positive number')
        self.map_matrix = self.create_map_random()


    def create_map_random(self):
        map_matrix = np.random.choice([-(self.draught*2), 1-self.draught, 1, 10], size=(self.n, self.n), p=[0.75, 0.10, 0.10, 0.05])
        map_matrix[0, 0] = -self.draught*2
        map_matrix[self.n-1, self.n-1] = -self.draught*2

        return map_matrix    

    def plot_map(self):
        cmap = mcolors.ListedColormap(["RoyalBlue", "CornflowerBlue", 'PaleGreen', "LemonChiffon"])
        bounds = [-int(self.draught*2), -self.draught, 0, 5, 10]
        norm = mcolors.BoundaryNorm(bounds, cmap.N, clip=True)
        plt.imshow(self.map_matrix, cmap=cmap, norm=norm)
        plt.colorbar(ticks=bounds)

class Path:
    def __init__(self, map_obj, n):
        self.map_obj = map_obj
        self.n = n
        self.path_matrix = None

    def is_valid_cell(self, row, column):
        is_row_within_bounds = 0 <= row < self.n
        is_col_within_bounds = 0 <= column < self.n

        if not is_row_within_bounds or not is_col_within_bounds:
            return False

        return self.map_obj.map_matrix[row, column] < -self.map_obj.draught

    def get_neighbors(self, cell):
        row, column = cell
        ways = [-1, 0], [0, -1], [1, 0], [0, 1]
        neighbors = []
        for new_row, new_column in ways:
            next_row, next_column = row + new_row, column + new_column

            if self.is_valid_cell(next_row, next_column):
                neighbors.append(((next_row, next_column), self.map_obj.map_matrix[next_row, next_column]))

        return neighbors

    def find_shortest_path(self):
        start = (0, 0)
        end = (self.n - 1, self.n - 1)

        queue = deque([start])

        visited = {start: None}

        while queue:
            current_cell = queue.popleft()

            if current_cell == end:
                break

            neighbors = self.get_neighbors(current_cell)

            for neighbor in neighbors:
                if neighbor[0] not in visited and self.is_valid_cell(*neighbor[0]):
                    queue.append(neighbor[0])
                    visited[neighbor[0]] = current_cell

        self.path_matrix = self.reconstruct_path(visited, end)

    def reconstruct_path(self, visited, end):
        if end not in visited:
            print("There is no valid path")
            return None

        path = []
        current_cell = end
        while current_cell:
            path.append(current_cell)
            current_cell = visited[current_cell]

        path.reverse()
        return path

    def visualize_path(self):
        if self.path_matrix is None:
            return

        x_coords, y_coords = zip(*self.path_matrix)

        self.map_obj.plot_map()

        plt.plot(y_coords, x_coords, marker='o', markersize=8, color='white', label='Path')
        plt.legend()
        plt.show()



n = int(input("Enter the size of the field: "))
draught = float(input("Enter the draught in metres: "))
map_obj = Map(n, draught)

map_obj.plot_map()
plt.show()

path = Path(map_obj, n)
path.find_shortest_path()
path.visualize_path()
