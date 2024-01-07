import numpy as np
import matplotlib.pyplot as plt
import matplotlib.colors as mcolors


# Define a class for creating and visualizing a map
class Map:
    def __init__(self, map_size, draught, choice, path=None):
        if map_size <= 1:
            raise ValueError("N should be a positive number bigger then 1")
        if draught <= 0:
            raise ValueError("Draught should be a positive number")

        self.map_size = map_size
        self.draught = draught
        self.choice = choice
        self.path = path
        self.map_matrix = [[0] * self.map_size for _ in range(self.map_size)]

    def create_map_from_choice(self, choice):
        if choice == "m":
            self.map_matrix = self.create_map_manually()
        elif choice == "a":
            self.map_matrix = self.create_map_random()
        elif choice == "f":
            self.map_matrix = self.create_map_from_file(self.path)
        else:
            raise ValueError(
                "Invalid choice. You can enter m for manual, a for automatic or f for file creation."
            )

    def create_map_random(self):
        probabilities = [0.75, 0.10, 0.10, 0.05]
        elevations = [-(self.draught * 2), 1 - self.draught, 1, 10]

        map_matrix = np.random.choice(
            elevations, size=(self.map_size, self.map_size), p=probabilities
        )
        map_matrix[0, 0] = -self.draught * 2
        map_matrix[-1, -1] = -self.draught * 2

        return map_matrix

    def create_map_manually(self):
        map_matrix = np.zeros((self.map_size, self.map_size))
        for row in range(self.map_size):
            for column in range(self.map_size):
                try:
                    map_matrix[row, column] = float(
                        input(
                            f"Enter the elevation at position ({row + 1},{column + 1}): "
                        )
                    )
                except ValueError:
                    raise ValueError(
                        "Invalid input. Please enter a valid numeric elevation."
                    )

        return map_matrix

    def create_map_from_file(self, path):
        if path is None:
            raise ValueError("File path is not provided.")
        map_matrix = np.loadtxt(path, skiprows=1)
        if map_matrix.shape != (self.map_size, self.map_size):
            raise ValueError(
                f"Invalid map dimensions. Expected ({self.map_size}, {self.map_size})."
            )
        return map_matrix

    def plot_map(self):
        cmap = mcolors.ListedColormap(
            ["RoyalBlue", "CornflowerBlue", "PaleGreen", "LemonChiffon"]
        )
        bounds = [-int(self.draught * 2), -self.draught, 0, 5, 10]
        norm = mcolors.BoundaryNorm(bounds, cmap.N, clip=True)
        plt.imshow(self.map_matrix, cmap=cmap, norm=norm)
        plt.colorbar(ticks=bounds)

    # Check if a given cell is within the map boundaries and has a valid elevation for the ship to enter
    def is_valid_cell(self, row, column):
        is_row_within_bounds = 0 <= row < self.map_size
        is_col_within_bounds = 0 <= column < self.map_size

        if not is_row_within_bounds or not is_col_within_bounds:
            return False

        return self.map_matrix[row][column] < -self.draught

    # Method to get valid neighboring cells of a given cell
    def get_neighbors(self, cell):
        row, column = cell
        ways = [-1, 0], [0, -1], [1, 0], [0, 1]
        neighbors = []
        for new_row, new_column in ways:
            next_row, next_column = row + new_row, column + new_column

            if self.is_valid_cell(next_row, next_column):
                neighbors.append(
                    ((next_row, next_column), self.map_matrix[next_row, next_column])
                )

        return neighbors
