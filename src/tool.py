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
