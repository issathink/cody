import os
from src.timelink import Timelink
from src.method_one import nb_in_out_with_fixed_value
from src.method_one import nb_in_out_fixed_vertex
from src.method_one import nb_in_out_delta_variance


def check_int(s):
    if s[0] in '+':
        return s[1:].isdigit()
    return s.isdigit()


def get_time_links(filename, instant=None):
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
        l = filter(lambda e: e.time < instant, l)

    return l, v


def get_time_low(l, time):
    return filter(lambda e: e.time < time, l)


def get_time_up(l, time):
    return filter(lambda e: e.time > time, l)


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


def plot_in_out_for_each_value(filename, result):
    with open("./../data/" + filename + ".txt", "w+") as f:
        for i in range(len(result)):
            tmp = str(i) + " " + str(nb_in_out_with_fixed_value(result, i)) + "\n"
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


"""
    To plot with gnuplot :)
    $ gnuplot
    $ set term jpeg size 800,600 font "Verdana,10"
    $ set output "filename.jpg"
    $ plot "file1.txt" w l title 'Label 1', "file2.txt" w l title 'Label 2'
"""