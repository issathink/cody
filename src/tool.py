import os
import random
from src.timelink import Timelink
from src.method_one import nb_in_out_distribution
from src.method_one import nb_in_out_fixed_vertex
from src.method_one import nb_in_out_delta_variance
from src.method_one import compute_nb_in_out


def check_int(s):
    if s[0] in '+':
        return s[1:].isdigit()
    return s.isdigit()


def get_time_links(filename, instant=None, ordering=None):
    l = []
    v = set()

    with open(filename, "r") as elems:
        for elem in elems:
            tmp = elem.split(" ")
            time = int(tmp[2])
            nodeA = int(tmp[0])
            nodeB = int(tmp[1])
            timelink = Timelink.create(nodeA, nodeB, time)
            l.append(timelink)
            v.add(nodeA)
            v.add(nodeB)

    if instant is not None:
        if ordering is None:
            l = filter(lambda e: e.time < instant, l)
        else:
            l = filter(lambda e: e.time >= instant, l)

    return l, v


def get_time_low(l, time):
    return filter(lambda e: e.time < time, l)


def get_time_up(l, time):
    return filter(lambda e: e.time > time, l)


def random_time_links_generator(filename, links_size, nb_nodes, time_max):
    result = []

    for i in range(links_size):
        sample = random.sample(range(nb_nodes), 2)
        time = random.randint(time_max)
        elem = Timelink.create(sample[0], sample[1], time)
        result.append(elem)

    result = sorted(result, key=lambda e: e.timelink)
    with open("./../data/" + filename, "w+") as f:
        for r in result:
            f.write(str(r.nodeA) + " " + str(r.nodeB) + " " + str(r.timelink))

    return result


def generate_plot_file(filename, result):
    # print result
    with open("./../data/" + filename + "_nb_in.txt", "w+") as f:
        tmp = "0 " + str(result[0].get(0)[0])
        f.write(tmp)
        for i in range(1, len(result)):
            tmp = "\n" + str(i) + " " + str(result[i].get(i)[0])
            f.write(tmp)

    with open("./../data/" + filename + "_nb_out.txt", "w+") as f:
        tmp = "0 " + str(result[0].get(0)[1])
        f.write(tmp)
        for i in range(1, len(result)):
            tmp = "\n" + str(i) + " " + str(result[i].get(i)[1])
            f.write(tmp)


def plot_in_out_distribution(filename, result, in_out):
    with open("./data/" + filename + ".txt", "w+") as f:
        for i in range(len(result)):
            tmp = str(i) + " " + str(nb_in_out_distribution(result, i, in_out)) + "\n"
            f.write(tmp)


def plot_vertex_evolution(filename, links, vertex_id, nb_vertexes):
    result = nb_in_out_fixed_vertex(links, vertex_id, nb_vertexes)
    with open("./../data/" + filename + "_in.txt", "w+") as f:
        for r in result:
            tmp = str(r.get("time")) + " " + str(r.get("nb_in")) + "\n"
            f.write(tmp)

    with open("./../data/" + filename + "_out.txt", "w+") as f:
        for r in result:
            tmp = str(r.get("time")) + " " + str(r.get("nb_out")) + "\n"
            f.write(tmp)


def plot_delta_variance(filename, links, nb_vertexes, instant, delta):
    result = nb_in_out_delta_variance(links, nb_vertexes, instant, delta)
    with open("./../data/" + filename + "_in.txt", "w+") as f:
        for i in range(len(result[0])):
            print str(result[0][i]) + " " + str(result[1][i])
            diff = result[1][i].get("nb_in") - result[0][i].get("nb_in")
            tmp = str(i) + " " + str(diff) + "\n"
            f.write(tmp)

    with open("./../data/" + filename + "_out.txt", "w+") as f:
        for i in range(len(result[0])):
            diff = result[1][i].get("nb_out") - result[0][i].get("nb_out")
            tmp = str(i) + " " + str(diff) + "\n"
            f.write(tmp)


# Generate file at each instant (each file will be plotted and the sequence will be a video magic)
def plot_in_out_for_each_instant(filename, each):
    instants = set()
    (links, nb_vertexes) = get_time_links(filename)

    for elem in links:
        instants.add(elem.time)

    print "Length of instants: " + str(len(instants))
    instants = list(instants)
    instants.sort()

    if len(instants) < 10*each:
        for i in range(1, len(instants), 1):
            result = compute_nb_in_out(filename, instants[i])
            generate_plot_file(filename+str(i), result)
            print "> " + str(i)
    else:
        for i in range(1, len(instants), each):
            result = compute_nb_in_out(filename, instants[i])
            generate_plot_file(filename + str(i), result)
            print ">> " + str(i)

"""
    To plot with gnuplot :)
    $ gnuplot
    $ set term jpeg size 800,600 font "Verdana,10"
    $ set output "filename.jpg"
    $ plot "file1.txt" w l title 'Label 1', "file2.txt" w l title 'Label 2'

    $ gnuplot -e "src='rollernet.dyn100_nb_in.txt'; dst='a.jpg'; xmax='70'; ymax='70'" ./../src/plot.plg
"""