import numpy as np
from Map import Map
from Path import Path
import matplotlib.pyplot as plt

choice = str(
    input(
        "Which map creation option suits you:\nprint m for manual, a for automatic, or f for file creation.\n"
    )
).lower()

if choice == "f":
    print(
        "\033[92mIf you are using your own file, take these facts into account:\n"
        " - The first line must contain values for map_size and draught, separated by spaces.\n"
        " - The following lines must contain depths for each cell.\033[0m"
    )

    file_path = str(input("Enter the file path:"))
    first_line = np.loadtxt(file_path, max_rows=1)
    first_line_str = " ".join(map(str, first_line))
    map_size, draught = map(int, map(float, first_line_str.split(" ")))
else:
    file_path = None
    map_size = int(input("Enter the size of the field: "))
    draught = float(input("Enter the draught in metres: "))


map_instance = Map(map_size, draught, choice, file_path)
map_instance.create_map_from_choice(choice)

map_instance.plot_map()
plt.title("To see the path, close this window")
plt.show()

path_instance = Path(map_instance, map_size)
path_instance.find_paths()
path_instance.visualize_path()
