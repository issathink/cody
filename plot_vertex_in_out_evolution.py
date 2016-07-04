from src.tool import get_time_links
from src.tool import plot_vertex_evolution

# Plotting for each instance can take very long time
# So, we'll plot each 2 weeks (1209600s) for enron data set and
# 4 minutes (240s) for rollernet.

each = 240
vertex_id = 15
delta = 360
filename = "rollernet.dyn"
directory = "./data/vertex_evolution/"

(links, vertexes) = get_time_links("./data/" + filename)
nb_vertexes = len(vertexes)

plot_vertex_evolution(directory, filename, vertex_id, each, None)
# plot_vertex_evolution(directory, filename, vertex_id, each, delta)

