import numpy as np
from Map import Map
from Path import Path
import matplotlib.pyplot as plt

choice = str(input('Which map creation option suits you:\nprint m for manual, a for automatic or f for file creation.\n'))
path = None

map_size = int(input("Enter the size of the field: "))
draught = float(input("Enter the draught in metres: "))


map = Map(map_size, draught, choice)
map.create_map_from_choice(choice)

map.plot_map_with_title()
plt.show()

path = Path(map, map_size)
path.find_paths()
path.visualize_path()
