import os
import numpy
import random
from decimal import Decimal
from src.timelink import Timelink
from src.algo import nb_in_out_distribution
from src.algo import nb_in_out_fixed_vertex
from src.algo import nb_in_out_delta
from src.algo import nb_in_out_delta_variance
from src.algo import nb_in_out

"""
    Check given string contain only digits
    :return boolean
"""
def check_int(s):
    if s[0] in '+':
        return s[1:].isdigit()
    return s.isdigit()


"""
    Given a filename, [instant], [ordering] it'll create a list of time links. If instant is
    not None only only time links with time < instant will be selected and ordering is to
    determine which sign (< or >=).
    :return (list of time links, vertexes ids)
"""
def get_time_links(filename, instant=None, ordering=None):
    l = []
    v = set()

    with open(filename, "r") as elems:
        for elem in elems:
            tmp = elem.split(" ")
            time = int(tmp[2])
            node_a = int(tmp[0])
            node_b = int(tmp[1])
            time_link = Timelink.create(node_a, node_b, time)
            l.append(time_link)
            v.add(node_a)
            v.add(node_b)

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


# Randomly generate time links.
def random_time_links_generator(filename, links_size, nb_nodes, time_max):
    result = []

    for i in range(links_size):
        sample = random.sample(range(nb_nodes), 2)
        time = random.randint(time_max)
        elem = Timelink.create(sample[0], sample[1], time)
        result.append(elem)

    result = sorted(result, key=lambda e: e.time_link)
    with open("./data/" + filename, "w+") as f:
        for r in result:
            f.write(str(r.node_a) + " " + str(r.node_b) + " " + str(r.time_link))

    return result


# Generate two rows file in order to plot with gnuplot.
def generate_plot_file(directory, filename, result):
    with open(directory + filename + "_nb_in.txt", "w+") as f:
        tmp = "0 " + str(result[0].get(0)[0])
        f.write(tmp)
        for i in range(1, len(result)):
            tmp = "\n" + str(i) + " " + str(result[i].get(i)[0])
            f.write(tmp)

    with open(directory + filename + "_nb_out.txt", "w+") as f:
        tmp = "0 " + str(result[0].get(0)[1])
        f.write(tmp)
        for i in range(1, len(result)):
            tmp = "\n" + str(i) + " " + str(result[i].get(i)[1])
            f.write(tmp)


# Generate plot file for statistical distribution
def plot_in_out_distribution(directory, filename, result, in_out):
    with open(directory + filename + ".txt", "w+") as f:
        for i in range(len(result)):
            tmp = str(i) + " " + str(nb_in_out_distribution(result, i, in_out)) + "\n"
            f.write(tmp)


# Generate plot file of the vertex evolution
def plot_vertex_evolution(directory, filename, vertex_id, each, delta):
    result = nb_in_out_fixed_vertex(filename, vertex_id, each, delta)
    with open(directory + filename + "_in.txt", "w+") as f:
        for r in result:
            tmp = str(r.get("time")) + " " + str(r.get("nb_in")) + "\n"
            f.write(tmp)

    with open(directory + filename + "_out.txt", "w+") as f:
        for r in result:
            tmp = str(r.get("time")) + " " + str(r.get("nb_out")) + "\n"
            f.write(tmp)


#  This method should be removed
def plot_delta_variance(filename, links, nb_vertexes, instant, delta):
    result = nb_in_out_delta_variance(links, nb_vertexes, instant, delta)
    with open("./data/" + filename + "_in.txt", "w+") as f:
        for i in range(len(result[0])):
            print str(result[0][i]) + " " + str(result[1][i])
            diff = result[1][i].get("nb_in") - result[0][i].get("nb_in")
            tmp = str(i) + " " + str(diff) + "\n"
            f.write(tmp)

    with open("./data/" + filename + "_out.txt", "w+") as f:
        for i in range(len(result[0])):
            diff = result[1][i].get("nb_out") - result[0][i].get("nb_out")
            tmp = str(i) + " " + str(diff) + "\n"
            f.write(tmp)


# Generate file at each instant (each file will be plotted and the sequence will be a video magic)
def plot_in_out_for_each_instant(directory, filename, each):
    instants = set()
    (links, nb_vertexes) = get_time_links("./data/" + filename)

    for elem in links:
        instants.add(elem.time)

    print "Length of instants: " + str(len(instants))
    instants = list(instants)
    instants.sort()

    for i in range(1, instants[-1], each):
        result = nb_in_out("./data/" + filename, i)
        generate_plot_file(directory, filename + str(i), result)
        print ">> " + str(i)


# Generate plot file of statistical mean and deviation
def plot_mean_and_deviation(directory, filename, each, delta):
    instants = set()
    (links, vertexes) = get_time_links("./data/" + filename)

    for elem in links:
        instants.add(elem.time)
    instants = list(instants)
    instants.sort()

    l_in = [0.0] * len(vertexes)
    l_out = [0.0] * len(vertexes)
    nb_t = 0.0
    with open(directory + filename + "_in.txt", "w+") as f_in, open(directory + filename + "_out.txt", "w+") as f_out:
        i = j = 0
        if delta is not None:
            for i in range(len(instants)):
                if instants[i] > delta:
                    break
            for j in reversed(xrange(len(instants) - 1)):
                if instants[j] + delta < instants[-1]:
                    break
        u = instants[1] if delta is None else instants[i]
        v = instants[-1] if delta is None else instants[j]

        for k in range(u, v, each):
            t_in = []
            t_out = []
            result = nb_in_out("./data/" + filename, k) if delta is None \
                else nb_in_out_delta("./data/" + filename, k, delta)
            max_in = 0.0
            max_out = 0.0

            for i in range(len(result)):
                t_in.append(result[i].get(i)[0])
                t_out.append(result[i].get(i)[1])
                max_in = result[i].get(i)[0] if result[i].get(i)[0] > max_in else max_in
                max_out = result[i].get(i)[1] if result[i].get(i)[1] > max_out else max_out

            dev_in = numpy.std(t_in)
            dev_out = numpy.std(t_out)
            mean_in = numpy.mean(t_in)
            mean_out = numpy.mean(t_out)
            tmp = str(k) + " " + str(mean_in) + " " + str(dev_in) + "\n"
            f_in.write(tmp)
            tmp = str(k) + " " + str(mean_out) + " " + str(dev_out) + "\n"
            f_out.write(tmp)
            nb_t += 1.0
            for i in range(len(result)):
                # l_in[i] += 1.0 if result[i].get(i)[0] >= mean_in else 0.0
                # l_out[i] += 1.0 if result[i].get(i)[1] >= mean_out else 0.0
                l_in[i] += result[i].get(i)[0] / (max_in*1.0)
                l_out[i] += result[i].get(i)[1] / (max_out*1.0)

            print ">> " + str(k) + " mean_in: " + str(mean_in) + " dev_in: " + str(dev_in)

        print "t_in: " + str(l_in)
        print "t_out: " + str(l_out)
        for i in range(len(vertexes)):
            l_in[i] /= nb_t
            l_out[i] /= nb_t

    print "nb_t: " + str(nb_t)
    print "t_in: " + str(l_in)
    print "t_out: " + str(l_out)
    with open(directory + filename + "_percentage_in.txt", "w+") as f:
        for i in range(len(vertexes)):
            f.write(str(i) + " " + str(l_in[i]) + "\n")
    with open(directory + filename + "_percentage_out.txt", "w+") as f:
        for i in range(len(vertexes)):
            f.write(str(i) + " " + str(l_out[i]) + "\n")


"""
    To plot with gnuplot :)
    $ gnuplot
    $ set term jpeg size 800,600 font "Verdana,10"
    $ set output "filename.jpg"
    $ plot "file1.txt" w l title 'Label 1', "file2.txt" w l title 'Label 2'

    $ gnuplot -e "src='rollernet.dyn100_nb_in.txt'; dst='a.jpg'; xmax='70'; ymax='70'" ./../src/plot.plg
    $ plot "f.txt" using 1:2 with linespoints, "f.txt" w err  # for stat "standard deviation"

    $ paste -d" " file1 file2 > output  # concatenate two files content line by line with space
"""