import time
from src.tool import random_time_links_generator
from src.tool import get_time_links
from src.tool import generate_plot_file
from src.algo import nb_in_out

filename = "test.txt"
links_size = [10, 100, 1000, 10000, 100000, 1000000]
nb_nodes = [10, 100, 100, 100, 150, 150]
time_max = [10, 1000, 10000, 100000, 1000000, 10000000]

with open("./../data/stress.txt", "w+") as f:
    for i in range(len(links_size)):
        random_time_links_generator(filename, links_size[i], nb_nodes[i], time_max[i])
        (links, vertexes) = get_time_links(filename)
        nb_vertexes = len(vertexes)
        start = time.time()
        nb_in_out(links, nb_vertexes)
        tmp = str(links_size[i]) + " " + str(time.time()-start)
