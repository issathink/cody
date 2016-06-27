from src.tool import random_time_links_generator
from src.tool import get_time_links
from src.tool import generate_plot_file
from src.method_one import compute_nb_in_out

filename = "test.txt"
links_size = 10
nb_nodes = 10
time_max = 10

test_length = [10, 100, 1000, 10000, 100000, 1000000]
nb_nodes = [10, 100, 100, 100, 150, 150]

random_time_links_generator(filename, links_size, nb_nodes, time_max)

(links, vertexes) = get_time_links(filename)
nb_vertexes = len(vertexes)
compute_nb_in_out(links, nb_vertexes)

