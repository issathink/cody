from src.tool import get_time_links
from src.tool import plot_vertex_evolution

each = 240
vertex_id = 15
filename = "rollernet.dyn"
directory = "./data/vertex_evolution/"

(links, vertexes) = get_time_links("./data/" + filename)
nb_vertexes = len(vertexes)

plot_vertex_evolution(directory, filename, vertex_id, each)
