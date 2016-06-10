from src.timelink import Timelink


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
    print result
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

"""
    To plot with gnuplot :)
    $ gnuplot
    $ set term jpeg size 800,600 font "Verdana,10"
    $ set output "filename.jpg"
    $ plot "file1.txt" w l title 'Label 1', "file2.txt" w l title 'Label 2'
"""