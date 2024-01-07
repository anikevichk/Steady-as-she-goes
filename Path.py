import matplotlib.pyplot as plt
from collections import deque
from PathNotFound import PathNotFound


# Define a class for finding and visualizing the shortest path on the map
class Path:
    def __init__(self, map_obj, map_size):
        if map_size <= 0:
            raise ValueError("N should be a positive number")

        self.map_obj = map_obj
        self.map_size = map_size
        self.first_path = None
        self.second_path = None
        self.path_of_matrix = None

    # Method to find the shortest path using BFS
    def find_path(self, start, end):
        queue = deque([start])
        visited = {start: None}

        while queue:
            current_cell = queue.popleft()

            if current_cell == end:
                break

            neighbors = self.map_obj.get_neighbors(current_cell)

            for neighbor in neighbors:
                if neighbor[0] not in visited and self.map_obj.is_valid_cell(
                    *neighbor[0]
                ):
                    queue.append(neighbor[0])
                    visited[neighbor[0]] = current_cell

        return self.reconstruct_path(visited, end)

    def find_paths(self):
        start1, end1 = (0, 0), (self.map_size - 1, self.map_size - 1)
        self.first_path = self.find_path(start1, end1)

        start2, end2 = (self.map_size - 1, self.map_size - 1), (0, 0)
        self.second_path = self.find_path(start2, end2)

        if self.first_path is None:
            raise PathNotFound()
        else:
            # Check if paths are the same, if yes, keep only one
            if set(self.first_path) == set(self.second_path):
                self.path_of_matrix = self.first_path
            else:
                self.path_of_matrix = (self.first_path, self.second_path)
                return self.path_of_matrix

    # Reconstruct the path from the end to the start using the visited dictionary
    def reconstruct_path(self, visited, end):
        if end not in visited:
            return None

        path = []
        current_cell = end
        while current_cell:
            path.append(current_cell)
            current_cell = visited[current_cell]

        return path

    def visualize_path(
        self, path_color="white", alt_path_color="#F0E68C", marker_size=8
    ):
        if isinstance(self.path_of_matrix, tuple):
            self.first_path, self.second_path = self.path_of_matrix

            x1_coords, y1_coords = zip(*self.first_path)
            x2_coords, y2_coords = zip(*self.second_path)

            plt.plot(
                y1_coords,
                x1_coords,
                marker="o",
                markersize=marker_size,
                color=path_color,
                label="Path1",
            )
            plt.plot(
                y2_coords,
                x2_coords,
                marker="x",
                markersize=marker_size,
                color=alt_path_color,
                label="Path2",
            )

        else:
            x_coords, y_coords = zip(*self.path_of_matrix)
            plt.plot(
                y_coords,
                x_coords,
                marker="o",
                markersize=marker_size,
                color=path_color,
                label="Path",
            )

        self.map_obj.plot_map()
        plt.title("Close the window to escape")
        plt.legend()
        plt.show()
