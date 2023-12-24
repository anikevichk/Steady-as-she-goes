import matplotlib.pyplot as plt
from classes import Map, Path

n = int(input("Enter the size of the field: "))
draught = float(input("Enter the draught in metres: "))
map = Map(n, draught)

map.plot_map()
plt.show()

path = Path(map, n)
path.find_shortest_path()
path.visualize_path()
